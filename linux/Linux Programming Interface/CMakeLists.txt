cmake_minimum_required(VERSION 3.13)
project(Linux_Programming_Interface)

set(CMAKE_CXX_STANDARD 11)

# 搜索cpp目录下的所有.cpp文件
aux_source_directory(src SRC)
# 包含的头文件
include_directories(include/)

add_executable(main main.cpp)

# 第四章 通用IO模型
add_executable(4 test/part4/file.cpp ${SRC})

# 第五章 5.1
add_executable(5 test/part5/5.cpp ${SRC})

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
set(13_FILE test/part13/13.cpp ${SRC})
add_executable(13_cache_io ${13_FILE})

# 第15章
set(15_FILE test/part15/15.cpp ${SRC})
add_executable(15_file_attr ${15_FILE})

set(19_FILE test/part19/19.cpp ${SRC})
add_executable(19_inotify ${19_FILE})

add_executable(20_singal test/part20-22/20.cpp)
add_executable(21_singal test/part20-22/21.cpp)
target_link_libraries(21_singal crypt)

add_executable(23_interval_time test/part23/23.cpp)
target_link_libraries(23_interval_time rt)

add_executable(24_process_create test/part24-28/24.cpp)
add_executable(25_process_exit test/part24-28/25.cpp)
add_executable(26_process_monitor test/part24-28/26.cpp)
add_executable(27_process_run test/part24-28/27.cpp)

add_executable(29_thread test/part29-33/29.cpp)
target_link_libraries(29_thread pthread)
add_executable(30_thread_sync test/part29-33/30.cpp)
target_link_libraries(30_thread_sync pthread)
add_executable(31_thread_safe test/part29-33/31.cpp)
target_link_libraries(31_thread_safe pthread)
add_executable(32_thread_cancel test/part29-33/32.cpp)
target_link_libraries(32_thread_cancel pthread)
