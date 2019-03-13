cmake_minimum_required(VERSION 3.13)
project(Linux_Programming_Interface)

set(CMAKE_CXX_STANDARD 11)

# 搜索cpp目录下的所有.cpp文件
aux_source_directory(cpp CPP_LIST)
# 包含的头文件
include_directories(include/)

add_executable(main main.cpp)

# 第四章 通用IO模型
set(4_FILE test/part4/file.cpp ${CPP_LIST})
add_executable(4_file ${4_FILE})
