cmake_minimum_required(VERSION 3.0.0)
project(vscode_cmake_ext_helloworld VERSION 0.1.0)

include(CTest)
enable_testing()

# Just in cas we wanna move to mingw
if (MSVC)
    add_compile_options(/W4)
else()
	add_compile_options(-Wall -Wextra -Wpedantic)
endif()

add_executable(vscode_cmake_ext_helloworld main.cpp)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
