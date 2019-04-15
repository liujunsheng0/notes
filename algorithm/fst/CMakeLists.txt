cmake_minimum_required(VERSION 3.13)
project(fst)

set(CMAKE_CXX_STANDARD 11)

add_executable(main main.cpp)

target_link_libraries(main fst)