cmake_minimum_required(VERSION 3.25)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_COMPILER msbuild)
set(CMAKE_C_COMPILER msbuild)

project(eng
        VERSION 0.0.1
        LANGUAGES CXX C
        )

add_executable(eng main.cpp)
