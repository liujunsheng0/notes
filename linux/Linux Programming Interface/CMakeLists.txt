cmake_minimum_required(VERSION 3.13)
project(Linux_Programming_Interface)

set(CMAKE_CXX_STANDARD 11)

set(SOURCE_FILES main.cpp lib/tlpi_hdr.cpp include/error_function.h)
add_executable(main ${SOURCE_FILES})