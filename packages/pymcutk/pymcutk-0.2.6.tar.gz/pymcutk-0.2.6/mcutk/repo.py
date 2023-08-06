from __future__ import print_function
import os
import io
import glob
import logging
import subprocess

from distutils.version import LooseVersion
try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse
try:
    import ConfigParser as configparser
except ImportError:
    import configparser

from mcutk import util
from mcutk.exceptions import ProcessTimeout


class GitCommandError(Exception):
    pass

def _get_repo_url(path):
    try:
        subprocess.check_call('git rev-parse --is-inside-work-tree', cwd=path, shell=True)
    except subprocess.CalledProcessError:
        pass

    ret, output = util.run_command('git config --get remote.origin.url', cwd=path, stdout=True, shell=True)
    return output.replace('\\n', '').strip()


class Repo(object):
    """Class Repo provide an abstract model access for git repositories, it is warpper
    based on git tool. Many useful built in abstactions or shortcut functions make the
    git call is very easy so that you don't need to handle process call by subprocess
    or others.

    Exmaple 1:
        >>> repo = Repo("ssh://exmaple.git")
        >>> repo.is_ready
        >>> repo.Clone("/home/")

    Exmaple 2:
        >>> repo = Repo.frompath("C:/mcu-sdk-2.0")
        >>> print repo.repo_url
        >>> print repo.is_ready
        >>> print repo.get_branch_name()
        >>> print repo.get_latest_commit_message()
        >>> print repo.get_submodules()
        >>> repo.checkout_branch("dev")
        >>> repo.exec_commands(["git status", "git --version"])
    """

    @classmethod
    def frompath(cls, path):
        """Return a repo object from specific path."""
        if not os.path.exists(path):
            return
        url = _get_repo_url(path)
        if url is not None:
            return cls(url, path)

    @classmethod
    def fromurl(cls, url, parent_dir):
        """Return a repo object with url and parent_dir."""

        repo = cls(url)
        repo.repo_dir = os.path.join(parent_dir, repo.repo_name)
        return repo

    def __init__(self, repo_url, repo_dir=None):
        """Create a repo instance.

        params:
            - repo_url: repo remote address.
            - repo_dir: the directory of repo on your local file system.
        """
        self.repo_dir = repo_dir
        self.repo_url = repo_url
        self.print_git_console = False
        self.occupations = dict()
        self.try_to_remove_lock = True
        self.repo_name = repo_url.split("/")[-1].replace(".git", "")
        self.repo_domain = repo_url.replace(self.repo_name+".git", "")

    def __str__(self):
        return "Repo(name=%s, dir=%s)"%(self.repo_name, self.repo_dir)

    def __exec(self, cmd, cwd=None, timeout=3600, retry=2, ignore_errors=False):
        if cwd is None:
            cwd = self.repo_dir
        error = None
        for _ in range(retry):
            error = None
            logging.info(cmd)
            try:
                stdout = 'capture_print' if self.print_git_console else "capture"
                noerror, output = util.run_command(cmd, cwd=cwd, stdout=stdout, timeout=timeout)
                if ignore_errors:
                    return output

                if noerror == 0:
                    break
                # try to remove index.lock
                if self.try_to_remove_lock:
                    self.remove_index_lock(self.repo_dir)
            except ProcessTimeout as e:
                error = e
            logging.warning("retry again..")
        else:
            raise GitCommandError(cmd)

        if not ignore_errors and error:
            raise
        return output

    @property
    def is_ready(self):
        if not os.path.exists(str(self.repo_dir)):
            return False

        url_c = _get_repo_url(self.repo_dir)
        if not url_c:
            return False

        return True

    def check_url(self):
        """Check and compare url whether is match."""

        url_c = _get_repo_url(self.repo_dir)

        if not url_c:
            return False

        if urlparse(self.repo_url).path == urlparse(url_c).path:
            return True

        else:
            logging.warning("URL is mismatch, local url is: %s, but object is: %s",
                            url_c, self.repo_url)
            return False

    def exec_cmd(self, *args, **kwargs):
        """Execute a command."""

        return self.__exec(*args, **kwargs)

    def exec_cmds(self, cmds):
        """Execute a list of commands."""

        for cmd in cmds:
            self.__exec(cmd)

    def get_latest_commit_message(self, repo_dir=None):
        """Return the commit message on the head

        Default work directory is the main repo.
        """
        if not repo_dir:
            repo_dir = self.repo_dir

        return self.__exec("git log -n 1", cwd=repo_dir, timeout=10)

    def get_branch_name(self, repo_dir=None):
        """Return branch name.

        Default work directory is the main repo.
        """
        if not repo_dir:
            repo_dir = self.repo_dir
        return self.__exec("git rev-parse --abbrev-ref HEAD", cwd=repo_dir, timeout=10, ignore_errors=True).replace("\n", "").strip()

    def get_submodules(self, repo_dir=None):
        """Return a dictionary about all submodules.

        Default return the main submodules.
        """
        if not repo_dir:
            repo_dir = self.repo_dir

        gitmodules = os.path.join(repo_dir, ".gitmodules")
        if os.path.exists(gitmodules) is False:
            return None

        mod_parser = configparser.RawConfigParser()
        with open(gitmodules) as f:
            content = f.read().replace("\t", "").decode('utf-8')
            fakefile = io.StringIO(content)

        mod_parser.readfp(fakefile, filename=gitmodules)
        modules = mod_parser.sections()
        modules_dict = dict()

        for modname in modules:
            url = mod_parser.get(modname, "url")
            path = os.path.join(self.repo_dir, mod_parser.get(modname, "path"))
            modules_dict[modname.replace("submodule ", "").replace("\"", "")] = Repo(url, path)

        return modules_dict

    def update_submodules(self):
        """Update submodules
            functions instruction:
                # update submodules
                # 1> get commit message
                # 2> get current branch
                # 3> if need, update gitsubmodules configurations
                # 4> git submodule deinit -f .
                # 5> git submodule update --init
        """
        version_string = self.exec_cmd('git --version')
        git_version = version_string.split('.windows')[0].replace("git version", '').strip()

        # git version < 2.9.0  not support --jobs
        if LooseVersion(git_version) >= LooseVersion("2.9.0"):
            cmd = 'git submodule update --init --force --recursive --jobs 4'
        else:
            cmd = 'git submodule update --init --force --recursive'

        try:
            self.exec_cmd(cmd)
        except GitCommandError:
            Repo.remove_index_lock(self.repo_dir)
            self.exec_cmd('git submodule deinit -f .')
            self.exec_cmd(cmd)

    def get_head_hash(self):
        """Return commit hash from head."""
        return self.__exec("git rev-parse HEAD", timeout=10, ignore_errors=True).replace("\n", "").strip()

    def get_history_abbrev(self, since="1.weeks"):
        """Useful options for git log --pretty=format
            Option	Description of Output
            %H Commit hash
            %h Abbreviated commit hash
            %T Tree hash
            %t Abbreviated tree hash
            %an Author name
            %ae Author e-mail
            %ad Author date (format respects the -date= option)
            %ar Author date, relative
            %cn Committer name
            %ce Committer email
            %cd Committer date
            %cr Committer date, relative
            %s Subject

        Reference:
            https://git-scm.com/book/tr/v2/Git-Basics-Viewing-the-Commit-History
            https://git-scm.com/docs/git-log
        """
        if since.split(".")[1] not in ["days", "weeks"]:
            raise ValueError("argument is not valid format,")

        return util.run_command('git log --pretty=format:"#### %h - %cr - %an: %s" --since={0} --stat'.format(since),
                                cwd=self.repo_dir)[1]

    def get_history(self, since="1.weeks"):
        """Extract commits history details.

            git log -p --since=1.weeks
        """
        if since.split(".")[1] not in ["days", "weeks"]:
            raise ValueError("argument is not valid format,")

        return util.run_command('git log -p --since={0}'.format(since),
                                cwd=self.repo_dir)[1]

    def get_remote_branches(self):
        """Fetch all of branches from remote.

        Returns: A list of branches.
        """
        content = util.run_command("git ls-remote --heads", cwd=self.repo_dir, stdout=True, timeout=300)[1]
        branches = [line.split("heads/")[1].strip() for line in content.split("\n") \
                    if "refs/heads/" in line]

        return branches

    @staticmethod
    def quick_clone(url, clone_path, branch_name, foldername=None):
        repo = Repo.fromurl(url, clone_path)
        if foldername:
            repo.repo_dir = os.path.join(clone_path, foldername)
        else:
            foldername = repo.repo_name

        util.run_command('git init %s' % foldername, cwd=clone_path, need_raise=True)
        repo.exec_cmds([
            'git config remote.origin.url %s' % url,
            'git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"'
        ])
        return repo

    def clone(self, clone_path='.', branch_name=None, foldername=None, quick_clone=True):
        """Clone specific branch to specific directory.

        Arguments:
            clone_path {str} -- directory to clone

        Keyword Arguments:
            branch_name {str} -- branch name (default: {'master'})
            foldername {str} -- folder name (default: {None})

        Returns:
            repo_dir

        Documentation about git clone:
            --depth=<depth>
                Create a shallow clone with a history truncated to the specified number of commits.
                Implies --single-branch unless --no-single-branch is given to fetch the histories
                near the tips of allbranches. If you want to clone submodules shallowly also pass
                --shallow-submodules.

            --branch <name>
            -b <name>
                Instead of pointing the newly created HEAD to the branch pointed to by the cloned
                repository's HEAD, point to <name> branch instead. In a non-bare repository, this
                is the branch that will be checked out. --branch can also take tags and detaches
                the HEAD at that commit in the resulting repository.
        """
        logging.info("prepare to clone repo")

        if quick_clone:
            repo = Repo.quick_clone(self.repo_url, clone_path, branch_name, foldername)
            self.repo_dir = repo.repo_dir
            return self.repo_dir

        if self.repo_dir and clone_path == '.':
            clone_path = os.path.dirname(self.repo_dir)

        # clone single branch, instead of all branches
        if branch_name:
            clone_cmd = 'git clone --depth 10 -b {0} {1}'.format(branch_name, self.repo_url)
        else:
            clone_cmd = 'git clone --depth 10 {0}'.format(self.repo_url)

        # clone to specific dest folder
        if foldername:
            clone_cmd += " " + foldername
        else:
            # default folder
            dir_name = self.repo_name

        logging.info(clone_cmd)
        ret = util.run_command(clone_cmd, cwd=clone_path, timeout=3600)[0]

        if ret != 0:
            logging.error("clone command return none-zero code!")
            raise GitCommandError("Failed to clone repo!")

        if self.repo_dir is None:
            self.repo_dir = os.path.join(clone_path, dir_name)

        self.__exec('git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"')
        logging.info('---clone repo successfully---')
        return self.repo_dir

    def checkout_branch(self,
                        branch_name,
                        tag_name=None,
                        submodule_deinit=True,
                        submodule_update=True,
                        shallow_fetch=False):
        """Fetch and checkout to specific branch, and make the branch update to date.

        Execute git commands, and try several times if any steps are failed.
            1. git reset --hard
            2. git clean -fxd
            3. git deinit -f .
            4. git fetch -t origin <branch name>
            5. git checkout <branch name>
            6. git submodule update --init

        Arguments:
            branch_name {str} -- branch name or hash

        Keyword Arguments:
            tag_name {str} -- tag name (default: {None})
            submodule_deinit {bool} -- do submodule deinit (default: {True})
            submodule_update {bool} -- do submodule update (default: {True})
            shallow_fetch {bool} -- do shallow fetch (default: {False})

        Raises:
            GitCommandError -- When any git operation failed.

        Returns:
            bool -- success or not
        """
        logging.info("start to update repo...")

        if shallow_fetch:
            fetch_command = 'git fetch --depth 10 -t --force origin %s'%branch_name
        else:
            fetch_command = 'git fetch -t --force origin %s'%branch_name

        try:
            if submodule_deinit and submodule_update:
                self.__exec('git submodule deinit -f .')

            self.__exec('git reset --hard', retry=1)
            self.__exec('git clean -fxd', retry=1)
        except GitCommandError:
            if os.name == "nt":
                util.change_folder_security_win(self.repo_dir)
            Repo.remove_index_lock(self.repo_dir)

            self.__exec('git reset --hard')
            self.__exec('git clean -fxd')

        try:
            self.__exec(fetch_command, retry=4)
        except GitCommandError:
            raise GitCommandError("Fetch Branch Error!")

        self.__exec('git checkout -f %s'%branch_name)
        self.__exec('git merge origin/%s'%branch_name)
        if tag_name:
            self.__exec('git checkout %s'%tag_name)

        if submodule_update:
            return self.update_submodules()

    def autosync(self, repo_parent_dir, branchs="master", submodule_deinit=True, submodule_update=True):
        """Automatic sync this repo. Retrun True if sucess.

        This function can be used in bellow situations:
            1. We don't know it is ready in local.
            2. We hope to simple the repo update.

        Arguments:
            repo_parent_dir {str} -- the root directory of the repo is located

        Keyword Arguments:
            branch {str} -- branch name (default: {"master"})
            submodule_deinit {bool} -- do submodule deinit (default: {True})
            submodule_update {bool} -- do submodule update (default: {True})

        Returns:
            bool.
        """
        #Parser branch name and tag name
        branch_name, tag_name = branchs, None
        if "%" in branchs:
            try:
                name_list = branchs.split('%')
                branch_name = name_list[0]
                tag_name = name_list[1]
            except:
                pass

        logging.info("Repo url: %s, Branch: %s, Tag: %s.", self.repo_url, branch_name, tag_name)

        if not os.path.exists(repo_parent_dir):
            os.makedirs(repo_parent_dir)

        # Get repo dir from main repo parent
        if not self.repo_dir:
            self.repo_dir = get_repo_location(repo_parent_dir, self.repo_name, self.repo_url)


        # Clone repo to repo_parent_dir
        if not self.is_ready:
            self.repo_dir = self.clone(repo_parent_dir, branch_name)

        # checkout & update repo
        self.checkout_branch(branch_name, tag_name, submodule_deinit, submodule_update)

        logging.info("---- Sync successfully %s ----", self.repo_dir)
        return True


    @staticmethod
    def remove_index_lock(repo_dir):
        """Remove index.lock to recovery git operation."""

        gitdir = repo_dir+"/.git"
        if os.path.exists(gitdir) is False:
            return

        try:
            for parent, _, filenames in os.walk(gitdir):
                for filename in filenames:
                    if ".lock" in filename:
                        path = os.path.join(parent, filename)
                        os.remove(path)

        except Exception:
            logging.exception("remove git lock failure")


def _repo_is_match(repo_dir, repo_url):
    '''
    check if the specified repo is adentical with the repo_url
    '''
    if os.path.isdir(repo_dir) is False:
        return False
    output = subprocess.check_output('git remote -v', cwd=repo_dir, shell=True)
    return repo_url in output


def get_repo_location(maindir, repo_name, repo_url):
    '''
    Search local repo in maindir,
    Return True: This repo is ready to use.
    Return False: Need Clone.
    '''
    # Search local repo in repo_parent_dir
    dirlist = glob.glob(maindir+"/"+repo_name)
    try:
        path = dirlist[0]
        output = subprocess.check_output('git remote -v', cwd=path, shell=True)
        logging.debug(output)
        return path

    except IndexError:
        logging.warning("Not found repo")
        return None

    except subprocess.CalledProcessError as e:
        logging.error("Repo is damaged. %s", e)
        return None
