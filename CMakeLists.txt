cmake_minimum_required(VERSION 3.21)
set(CMAKE_CXX_STANDARD 11)

project(Codeforces)

add_executable(Codeforces source/main.cpp)

enable_testing()

find_package(Python3 COMPONENTS Interpreter)

add_test(NAME Test COMMAND
        Python3::Interpreter
        ${CMAKE_SOURCE_DIR}/tool/tester.py
        $<TARGET_FILE:Codeforces>
        ${CMAKE_SOURCE_DIR}/source/in.txt
        ${CMAKE_SOURCE_DIR}/source/oracle.txt)
