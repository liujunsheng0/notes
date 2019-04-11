cmake 是一个跨平台、开源的构建系统。它是一个集软件构建、测试、打包于一身的软件。它使用与平台和编译器独立的配置文件来对软件编译过程进行控制。

> make的简化版

## [常用命令](https://blog.csdn.net/afei__/article/details/81201039)

```cmake
# 指定 cmake 的最小版本, 可选项
cmake_minimum_required(VERSION 3.4.1)

# 设置项目名称，这个命令不是强制性的，但最好都加上。它会引入两个变量 demo_BINARY_DIR 和 demo_SOURCE_DIR
project(demo)

# 设置编译类型，add_library 默认生成是静态库
#   Linux           Windows
#   demo            demo.exe
# libcommon.a       common.lib
# libcommon.so      common.dll
add_executable(demo demo.cpp) # 生成可执行文件
add_library(common STATIC util.cpp ... x.cpp) # 生成静态库
add_library(common SHARED util.cpp ... x.cpp) # 生成动态库或共享库
# 指定编译包含的源文件
# 明确指定
add_library(demo demo.cpp test.cpp util.cpp)
# 发现一个目录下所有的源代码文件并将列表存储在一个变量中
aux_source_directory(. SRC_LIST) # 搜索当前目录下的所有.cpp文件, 存储到SRC_LIST中
add_library(demo ${SRC_LIST})
# 自定义搜索规则
file(GLOB SRC_LIST "*.cpp" "protocol/*.cpp")
add_library(demo ${SRC_LIST}

#　设置包含的目录
include_directories(${CMAKE_CURRENT_BINARY_DIR}
			　　　　　${CMAKE_CURRENT_SOURCE_DIR}/include)

# 设置库路径
LINK_DIRECTORIES(...)
库文件存放的目录，在程序连接库文件的时候要在这些目录下寻找对应的库文件

# 指定链接多个库
target_link_libraries(demo 
					  ${CMAKE_CURRENT_SOURCE_DIR}/libs/libface.a
					  boost_system.a
					  boost_thread)
demo 依赖指定的库文件
```

