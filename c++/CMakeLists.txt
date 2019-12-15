cmake_minimum_required (VERSION 3.6)

add_executable(tsptdmd construction.cc
                        construction.h
                        genetic.cc
                        genetic.h
                        input.cc
                        input.h
                        main.cc
                        neighborhood.cc
                        neighborhood.h
                        search.cc
                        search.h
                        solution.cc
                        solution.h
                        validate.cc
                        validate.h
                    )
include_directories("${PROJECT_SOURCE_DIR}")
