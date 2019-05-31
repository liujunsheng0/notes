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

# 第五章 5.1
set(5_1_FILE test/part5/bad_exclusive_open.cpp ${CPP_LIST})
add_executable(5_1_bad_exclusive_open ${5_1_FILE})

set(5_3_FILE test/part5/fcntl_test.cpp ${CPP_LIST})
add_executable(5_3_fcntl ${5_3_FILE})

set(5_PARCTICE_FILE test/part5/copy_file_descriptor.cpp ${CPP_LIST})
add_executable(5_copy_file_descriptor ${5_PARCTICE_FILE})

set(5_PARCTICE_FILE test/part5/practices.cpp ${CPP_LIST})
add_executable(5_practice ${5_PARCTICE_FILE})

# 第六章
set(6_1_FILE test/part6/6_2.cpp)
add_executable(6_2_pid_and_ppid ${6_1_FILE})

# 第七章
set(7_1_FILE test/part7/7_1.cpp)
add_executable(7_1_memory ${7_1_FILE})

# 第10章
set(10_FILE test/part10/10.cpp)
add_executable(10_time ${10_FILE})

# 第10章
set(12_FILE test/part12/12.cpp)
add_executable(12_proc ${12_FILE})

# 第13章
set(13_FILE test/part13/13.cpp ${CPP_LIST})
add_executable(13_cache_io ${13_FILE})

# 第15章
set(15_FILE test/part15/15.cpp ${CPP_LIST})
add_executable(15_file_attr ${15_FILE})

set(19_FILE test/part19/19.cpp ${CPP_LIST})
add_executable(19_inotify ${19_FILE})

add_executable(20_singal test/part20-22/20.cpp)
add_executable(21_singal test/part20-22/21.cpp)
target_link_libraries(21_singal crypt)

add_executable(23_interval_time test/part23/23.cpp)
target_link_libraries(23_interval_time rt)