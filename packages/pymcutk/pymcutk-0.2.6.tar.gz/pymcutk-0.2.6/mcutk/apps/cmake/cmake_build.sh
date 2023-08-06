#!/bin/sh
cd $1
rm -rf CMakeFiles $2
rm -rf Makefile cmake_install.cmake CMakeCache.txt
cmake -Wno-deprecated -DCMAKE_TOOLCHAIN_FILE=$3 -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=$2 . && make -C . -j4
exit $?