cmake_minimum_required(VERSION 3.24)
#set(CMAKE_TOOLCHAIN_FILE C:/tools/vcpkg/scripts/buildsystems/vcpkg.cmake CACHE STRING "Vcpkg toolchain file")
project(sidelines)

set(CMAKE_CXX_STANDARD 20)

add_executable(sidelines_cli main.cpp)
find_package(SQLiteCpp CONFIG REQUIRED)
target_link_libraries(sidelines_cli PRIVATE SQLiteCpp)

include(FetchContent)
FetchContent_Declare(
        googletest
        URL https://github.com/google/googletest/archive/03597a01ee50ed33e9dfd640b249b4be3799d395.zip
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

enable_testing()
add_executable(sidelines_test sanity_test.cpp)
target_link_libraries(sidelines_test GTest::gtest_main)
include(GoogleTest)
gtest_discover_tests(sidelines_test)