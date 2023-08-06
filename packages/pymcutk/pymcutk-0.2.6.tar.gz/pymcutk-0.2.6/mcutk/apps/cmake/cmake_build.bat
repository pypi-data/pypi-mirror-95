@echo off
cd /d %1

REM remove cached file
set list=CMakeFiles Makefile cmake_install.cmake CMakeCache.txt
(for %%a in (%list%) do (
    if exist %%a (
	del /S/Q/F %%a > NULL
    )
))

REM clean configuration folder
if exist %2 (
    rd /s /Q %2
)

cmake -Wno-deprecated -DCMAKE_TOOLCHAIN_FILE=%3 -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=%2 .

if not %errorlevel% == 0 (exit /b %errorlevel%)

mingw32-make -C . -j4

exit /b %errorlevel%
