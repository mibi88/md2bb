cmake_minimum_required(VERSION 3.15)
project(md2bb VERSION 1.0 LANGUAGES C)

set(SOURCES
  src/targets/phpbb.c
  src/targets/planetcasio.c
  src/target_list.c
  src/convert.c
  src/main.c
)

add_executable(md2bb ${SOURCES})
set_property(TARGET md2bb PROPERTY C_STANDARD 90)
target_include_directories(md2bb PRIVATE inc)
target_compile_options(md2bb PRIVATE -g -Wall -Wextra -Wpedantic)
target_link_libraries(md2bb PRIVATE)

