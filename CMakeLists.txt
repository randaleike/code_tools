# specify the cmake minimum version
cmake_minimum_required(VERSION 3.10)
get_filename_component(ProjectId ${CMAKE_CURRENT_SOURCE_DIR} NAME)

# set the project name
project(${ProjectId}
        VERSION 0.4.3
        DESCRIPTION "Code generation and maintenance tools for C/CPP/Python/Typescript files"
        HOMEPAGE_URL "www.grocsoftware.com")

set(PROJECT_AUTHOR grocsoftware)

find_package(Python3 REQUIRED)
#find_package(PythonInterp REQUIRED)
#find_package(PythonLibs REQUIRED)

file(REMOVE ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-reset-generated.cmake)
file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-reset-generated.cmake "# Project clean project generated files script\n")

file(REMOVE ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-clean-tempfiles.cmake)
file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-clean-tempfiles.cmake "# Project clean temporary files script\n")

####
# Python source
####
set(PYTHON_SRC_DIR
    ${CMAKE_CURRENT_LIST_DIR}/src
    )

set(PYTHON_BASE_SRC_DIR
    ${PYTHON_SRC_DIR}/code_tools_grocsoftware/base
    )

set(PYTHON_CODE_TOOL_BASE_SRC
    ${PYTHON_BASE_SRC_DIR}/text_format.py
    ${PYTHON_BASE_SRC_DIR}/comment_block.py
    ${PYTHON_BASE_SRC_DIR}/copyright_tools.py
    ${PYTHON_BASE_SRC_DIR}/eula.py
    ${PYTHON_BASE_SRC_DIR}/param_return_tools.py
    ${PYTHON_BASE_SRC_DIR}/comment_gen_tools.py
    ${PYTHON_BASE_SRC_DIR}/doxygen_gen_tools.py
    ${PYTHON_BASE_SRC_DIR}/json_language_list.py
    ${PYTHON_BASE_SRC_DIR}/json_string_class_description.py
    )

set(PYTHON_CPP_GEN_SRC_DIR
    ${PYTHON_SRC_DIR}/code_tools_grocsoftware/cpp_gen
    )

set(PYTHON_PY_GEN_SRC_DIR
    ${PYTHON_SRC_DIR}/code_tools_grocsoftware/python_gen
    )

set(PYTHON_TS_GEN_SRC_DIR
    ${PYTHON_SRC_DIR}/code_tools_grocsoftware/typescript_gen
    )


set(PYTHON_CODE_TOOL_SRC
    ${PYTHON_CPP_GEN_SRC_DIR}/file_gen_base.py
    ${PYTHON_CPP_GEN_SRC_DIR}/string_class_tools.py
    ${PYTHON_CPP_GEN_SRC_DIR}/linux_lang_select.py
    ${PYTHON_CPP_GEN_SRC_DIR}/windows_lang_select.py
    ${PYTHON_CPP_GEN_SRC_DIR}/static_lang_select.py
    ${PYTHON_CPP_GEN_SRC_DIR}/master_lang_select.py
    ${PYTHON_PY_GEN_SRC_DIR}/file_gen_base.py
    ${PYTHON_TS_GEN_SRC_DIR}/file_gen_base.py
    )

set(PYTHON_SRC
    ${PYTHON_CODE_TOOL_BASE_SRC}
    ${PYTHON_CODE_TOOL_SRC})

####
# Python test source
####
set(PYTHON_TEST_DIR
    ${CMAKE_CURRENT_LIST_DIR}/tests
    )

set(PYTHON_CODE_TOOL_BASE_TESTS
    ${CMAKE_CURRENT_LIST_DIR}/tests/test_subtext_marker.py
    ${CMAKE_CURRENT_LIST_DIR}/tests/test_copyright_years_list.py
    ${CMAKE_CURRENT_LIST_DIR}/tests/test_copyright_parse_base.py
    ${CMAKE_CURRENT_LIST_DIR}/tests/test_copyright_order.py
    ${CMAKE_CURRENT_LIST_DIR}/tests/test_copyright_parse.py
    ${CMAKE_CURRENT_LIST_DIR}/tests/test_comment_block.py
    ${CMAKE_CURRENT_LIST_DIR}/tests/test_text_format.py
    ${CMAKE_CURRENT_LIST_DIR}/tests/test_eula.py
    ${CMAKE_CURRENT_LIST_DIR}/tests/test_param_return_tools.py
    ${CMAKE_CURRENT_LIST_DIR}/tests/test_comment_generator.py
    ${CMAKE_CURRENT_LIST_DIR}/tests/test_doxygen_generator.py
    )

set(PYTHON_CODE_TOOL_JSON_DB_TESTS
    ${CMAKE_CURRENT_LIST_DIR}/tests/test_translation_text_parser.py
    ${CMAKE_CURRENT_LIST_DIR}/tests/test_json_language_list.py
    ${CMAKE_CURRENT_LIST_DIR}/tests/test_json_string_class_description.py
    ${CMAKE_CURRENT_LIST_DIR}/tests/test_json_string_class_input.py
    ${CMAKE_CURRENT_LIST_DIR}/tests/test_json_string_class_macro.py
    )

set(PYTHON_CODE_TOOL_LANG_GEN_TESTS
    ${CMAKE_CURRENT_LIST_DIR}/tests/test_cpp_file_generation.py
    ${CMAKE_CURRENT_LIST_DIR}/tests/test_python_file_generation.py
    ${CMAKE_CURRENT_LIST_DIR}/tests/test_ts_file_generation.py
    )

set(PYTHON_TEST_SRC
    ${PYTHON_CODE_TOOL_BASE_TESTS}
    ${PYTHON_CODE_TOOL_JSON_DB_TESTS}
    ${PYTHON_CODE_TOOL_LANG_GEN_TESTS}
    )

foreach(DIRNAME IN LISTS PYTHON_SRC_DIR PYTHON_TEST_DIR)
    file(APPEND ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-clean-tempfiles.cmake "file(REMOVE_RECURSE ${DIRNAME}/__pycache__/)\n")
endforeach()

# Unittests
message ("Python base = ${PYTHON_BASE_DIR}")
set(DIR_INIT_IN ${CMAKE_CURRENT_LIST_DIR}/tests/dir_init.py.in)
set(DIR_INIT_OUT ${CMAKE_CURRENT_LIST_DIR}/tests/dir_init.py)
configure_file(${DIR_INIT_IN} ${DIR_INIT_OUT} @ONLY)
file(APPEND ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-reset-generated.cmake "file(REMOVE ${DIR_INIT_OUT})\n")

enable_testing()

add_custom_target(${PROJECT_NAME}-unittest ALL
    DEPENDS ${PYTHON_SRC} ${PYTHON_TEST_SRC}
    WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
    COMMAND ${Python3_EXECUTABLE} -m coverage run -m unittest discover -s tests/
    COMMAND ${Python3_EXECUTABLE} -m coverage html --omit dir_init.py,test_*.py --fail-under=95
    COMMENT "Run Python ${PROJECT_NAME} Unittest"
)
file(APPEND ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-clean-tempfiles.cmake "file(REMOVE ${CMAKE_CURRENT_LIST_DIR}/tests/.coverage)\n")
file(APPEND ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-clean-tempfiles.cmake "file(REMOVE ${CMAKE_CURRENT_LIST_DIR}/.coverage)\n")
file(APPEND ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-clean-tempfiles.cmake "file(REMOVE_RECURSE ${CMAKE_CURRENT_LIST_DIR}/htmlcov/)\n")
file(APPEND ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-clean-tempfiles.cmake "file(REMOVE_RECURSE ${CMAKE_CURRENT_LIST_DIR}/tests/htmlcov/)\n")

####
# doxygen generation
####
find_package(Doxygen
             REQUIRED dot
             OPTIONAL_COMPONENTS mscgen dia)

# ReadMe config
set(README_IN ${CMAKE_CURRENT_LIST_DIR}/setup_files/README.md.in)
set(README_OUT ${CMAKE_CURRENT_LIST_DIR}/README.md)
configure_file(${README_IN} ${README_OUT} @ONLY)
file(APPEND ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-reset-generated.cmake "file(REMOVE ${README_OUT})\n")

# Update Doxygen config
set(DOXYGEN_OUTPUT_DIR ${CMAKE_CURRENT_LIST_DIR}/doc)
set(DOXYGEN_IN ${CMAKE_CURRENT_LIST_DIR}/setup_files/Doxyfile.in)
set(DOXYGEN_OUT ${CMAKE_CURRENT_LIST_DIR}/Doxyfile)
configure_file(${DOXYGEN_IN} ${DOXYGEN_OUT} @ONLY)
file(APPEND ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-reset-generated.cmake "file(REMOVE ${DOXYGEN_OUT})\n")

if ((CMAKE_BUILD_TYPE MATCHES "^[Rr]elease") AND DOXYGEN_FOUND)
    message("Master Doxygen build enabled")

    # Add Doxygen target
    add_custom_target(${PROJECT_NAME}-builddoc
        COMMAND ${DOXYGEN_EXECUTABLE} ${DOXYGEN_OUT}
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        COMMENT "Generating API documentation with Doxygen"
        DEPENDS ${PYTHON_SRC}
        VERBATIM )

endif()
file(APPEND ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-reset-generated.cmake "file(REMOVE_RECURSE ${CMAKE_CURRENT_LIST_DIR}/doc)\n")

####
# python package generation
####
if (CMAKE_BUILD_TYPE MATCHES "^[Rr]elease")
    # Update pyproject
    set(PYPROJECT_IN ${CMAKE_CURRENT_LIST_DIR}/setup_files/pyproject.toml.in)
    set(PYPROJECT_OUT ${CMAKE_CURRENT_LIST_DIR}/pyproject.toml)
    configure_file(${PYPROJECT_IN} ${PYPROJECT_OUT} @ONLY)
    message("Master Python package build enabled")

    add_custom_target(${PROJECT_NAME}-package
        COMMAND ${Python3_EXECUTABLE} -m build
        WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
        COMMENT "Python Package build"
        DEPENDS ${PYTHON_SRC}
        VERBATIM )
endif()
file(APPEND ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-clean-tempfiles.cmake "file(REMOVE_RECURSE ${CMAKE_CURRENT_LIST_DIR}/${PROJECT_NAME}_${PROJECT_AUTHOR}.egg-info)\n")
file(APPEND ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-clean-tempfiles.cmake "file(REMOVE_RECURSE ${CMAKE_CURRENT_LIST_DIR}/dist)\n")
file(APPEND ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-reset-generated.cmake "file(REMOVE ${PYPROJECT_OUT})\n")

####
# package build cleanup
####
add_custom_target(${PROJECT_NAME}-clean
    COMMENT "Build cleanup"
    COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-clean-tempfiles.cmake
    )

add_custom_target(${PROJECT_NAME}-reset
    COMMENT "Build cleanup, Reset generated files"
    COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-clean-tempfiles.cmake
    COMMAND ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}-reset-generated.cmake
    )
