"""@package test_programmer_tools
Unittest for programmer base tools utility
"""

#==========================================================================
# Copyright (c) 2025 Randal Eike
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of self software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and self permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#==========================================================================

import os
from unittest.mock import patch, mock_open

from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList
from code_tools_grocsoftware.base.json_string_class_description import StringClassDescription

from code_tools_grocsoftware.base.project_json import ProjectDescription
from code_tools_grocsoftware.cpp_gen.project_file_gen import ProjectFileGenerator
from code_tools_grocsoftware.cpp_gen.cmake_gen import GenerateCmakeFile

from tests.dir_init import TESTFILEPATH

langfilename = os.path.join(TESTFILEPATH, "teststringlanglist.json")
strclass_filename = os.path.join(TESTFILEPATH, "teststrdesc.json")


class MockProjectDescription(ProjectDescription):
    """!
    @brief Mock ProjectDescription for testing
    """
    def get_lang_data(self)-> LanguageDescriptionList:
        """!
        @brief Get the language description list from the JSON data
        @return (LanguageDescriptionList) - Language description list object
        """
        return LanguageDescriptionList(langfilename)

    def get_string_data(self)-> StringClassDescription:
        """!
        @brief Get the language description list from the JSON data
        @return (StringClassDescription) - String class description list object
        """
        return StringClassDescription(strclass_filename)

    def get_include_dirs(self)->list:
        """!
        @brief Get the include subdirectory name from the JSON data
        @return (string) - Include subdirectory name
        """
        return ['inc', 'test']

    def get_src_subdir(self)->str:
        """!
        @brief Get the source subdirectory name from the JSON data
        @return (string) - Source subdirectory name
        """
        return 'src'

    def get_test_subdir(self)->str:
        """!
        @brief Get the test subdirectory name from the JSON data
        @return (string) - Test subdirectory name
        """
        return 'test'

    def get_mock_subdir(self)->str:
        """!
        @brief Get the mock subdirectory name from the JSON data
        @return (string) - Mock subdirectory name
        """
        return 'mock'

class MockFile:
    """!
    @brief Mock file object for testing
    """
    def __init__(self):
        self.mock_calls = []
        self.writedata = []

    def writelines(self, lines):
        """!
        @brief Mock writelines method
        """
        self.mock_calls.append(('writelines', ""))
        self.writedata.extend(lines)

    def write(self, data):
        """!
        @brief Mock write method
        """
        self.mock_calls.append(('write', ""))
        self.writedata.append(data)

# pylint: disable=protected-access

def test001_constructor():
    """!
    @brief Test the constructor
    """
    proj_gen = GenerateCmakeFile(ProjectFileGenerator(MockProjectDescription()))
    assert isinstance(proj_gen, GenerateCmakeFile)
    assert isinstance(proj_gen.file_gen, ProjectFileGenerator)
    assert isinstance(proj_gen.proj_data, ProjectDescription)

def test002_open_file():
    """!
    @brief Test open_file
    """
    proj_gen = GenerateCmakeFile(ProjectFileGenerator(MockProjectDescription()))

    with patch('builtins.open', mock_open()) as mocked_file:
        proj_gen._open_file("baseDirName")
        mocked_file.assert_called_once_with("baseDirName/CMakeLists.txt",
                                            mode = 'wt',
                                            encoding="utf-8")

def test003_open_file_fail(capsys):
    """!
    @brief Test open_file, fail
    """
    proj_gen = GenerateCmakeFile(ProjectFileGenerator(MockProjectDescription()))

    with patch('builtins.open', mock_open()) as mocked_file:
        mocked_file.side_effect = OSError
        assert proj_gen._open_file("baseDirName") is None
        mocked_file.assert_called_once_with("baseDirName/CMakeLists.txt",
                                            mode = 'wt',
                                            encoding="utf-8")
        assert capsys.readouterr().out == "Failed to open cmake file 'baseDirName/CMakeLists.txt' for writing\n"

def test004_gen_comment_block():
    """!
    @brief Test _gen_comment_block
    """
    proj_gen = GenerateCmakeFile(ProjectFileGenerator(MockProjectDescription()))
    code_txt = proj_gen._gen_comment_block("Test comment")
    assert len(code_txt) == 3
    assert code_txt[0] == "####\n"
    assert code_txt[1] == "# Test comment\n"
    assert code_txt[2] == "####\n"

def test004_gen_header():
    """!
    @brief Test gen_header
    """
    proj_gen = GenerateCmakeFile(ProjectFileGenerator(MockProjectDescription()))

    code_txt = proj_gen.gen_header("TestProj", "1.2.3.4")
    assert len(code_txt) == 4
    assert code_txt[0] == "cmake_minimum_required(VERSION 3.14)\n"
    assert code_txt[1] == "project(TestProj VERSION 1.2.3.4 LANGUAGES C CXX)\n\n"
    assert code_txt[2] == "set(CMAKE_CXX_STANDARD 17)\n"
    assert code_txt[3] == "set(CMAKE_CXX_STANDARD_REQUIRED True)\n"

    code_txt = proj_gen.gen_header("TestProj1", "4.3.2.1", "test desc")
    assert len(code_txt) == 4
    assert code_txt[0] == "cmake_minimum_required(VERSION 3.14)\n"
    assert code_txt[1] == "project(TestProj1 VERSION 4.3.2.1 LANGUAGES C CXX " \
                          "DESCRIPTION \"test desc\")\n\n"
    assert code_txt[2] == "set(CMAKE_CXX_STANDARD 17)\n"
    assert code_txt[3] == "set(CMAKE_CXX_STANDARD_REQUIRED True)\n"

    code_txt = proj_gen.gen_header("TestProj2", "1.1.1.1", "test desc", "http://foo.com")
    assert len(code_txt) == 4
    assert code_txt[0] == "cmake_minimum_required(VERSION 3.14)\n"
    assert code_txt[1] == "project(TestProj2 VERSION 1.1.1.1 LANGUAGES C CXX DESCRIPTION " \
                          "\"test desc\" HOMEPAGE_URL \"http://foo.com\")\n\n"
    assert code_txt[2] == "set(CMAKE_CXX_STANDARD 17)\n"
    assert code_txt[3] == "set(CMAKE_CXX_STANDARD_REQUIRED True)\n"

    code_txt = proj_gen.gen_header("TestProj3", "1.1.1.1", url="http://foo.com")
    assert len(code_txt) == 4
    assert code_txt[0] == "cmake_minimum_required(VERSION 3.14)\n"
    assert code_txt[1] == "project(TestProj3 VERSION 1.1.1.1 LANGUAGES C CXX " \
                          "HOMEPAGE_URL \"http://foo.com\")\n\n"
    assert code_txt[2] == "set(CMAKE_CXX_STANDARD 17)\n"
    assert code_txt[3] == "set(CMAKE_CXX_STANDARD_REQUIRED True)\n"

def test005_gen_include_dirs_list():
    """!
    Test gen_include_dirs_list
    """
    gen = ProjectFileGenerator(MockProjectDescription())
    gen.add_include_dir('inc')
    gen.add_include_dir('test')

    proj_gen = GenerateCmakeFile(gen)

    code_txt, incname = proj_gen.gen_include_dirs_list("TestProj")
    assert incname == 'TestProjInclude'
    assert len(code_txt) == 7
    assert code_txt[0] == "####\n"
    assert code_txt[1] == "# TestProj include directories\n"
    assert code_txt[2] == "####\n"
    assert code_txt[3] == "set (TestProjInclude\n"
    assert code_txt[4] == "     ${CMAKE_CURRENT_LIST_DIR}/inc\n"
    assert code_txt[5] == "     ${CMAKE_CURRENT_LIST_DIR}/test\n"
    assert code_txt[6] == "    )\n"

def test006_gen_include_dirs_list_empty():
    """!
    Test gen_include_dirs_list, empty list
    """
    gen = ProjectFileGenerator(MockProjectDescription())
    gen.inc_subdirs = []

    proj_gen = GenerateCmakeFile(gen)

    code_txt, incname = proj_gen.gen_include_dirs_list("TestProj")
    assert incname is None
    assert len(code_txt) == 0

def test007_gen_source_file_list():
    """!
    Test gen_source_file_list
    """
    gen = ProjectFileGenerator(MockProjectDescription())
    gen._add_file('source', 'src/some.cpp')
    gen._add_file('source', 'src/some_english.cpp', 'english')

    proj_gen = GenerateCmakeFile(gen)

    code_txt, srcname = proj_gen.gen_source_file_list("TestProj")
    assert srcname == 'TestProjSources'
    assert len(code_txt) == 7
    assert code_txt[0] == "####\n"
    assert code_txt[1] == "# TestProj source files\n"
    assert code_txt[2] == "####\n"
    assert code_txt[3] == "set (TestProjSources\n"
    assert code_txt[4] == "     ${CMAKE_CURRENT_LIST_DIR}/src/some.cpp\n"
    assert code_txt[5] == "     ${CMAKE_CURRENT_LIST_DIR}/src/some_english.cpp\n"
    assert code_txt[6] == "    )\n"

def test008_gen_source_file_list_empty():
    """!
    Test gen_source_file_list, empty
    """
    gen = ProjectFileGenerator(MockProjectDescription())
    gen.fnames = {}

    proj_gen = GenerateCmakeFile(gen)

    code_txt, srcname = proj_gen.gen_source_file_list("TestProj")
    assert srcname is None
    assert len(code_txt) == 0

def test009_gen_lib_cmake():
    """!
    Test gen_lib_cmake
    """
    gen = ProjectFileGenerator(MockProjectDescription())
    gen.fnames = {}

    proj_gen = GenerateCmakeFile(gen)

    code_txt = proj_gen.gen_lib_target("TestProj", 'sources', 'inclist')
    assert len(code_txt) == 6
    assert code_txt[0] == "####\n"
    assert code_txt[1] == "# TestProj library\n"
    assert code_txt[2] == "####\n"
    assert code_txt[3] == "add_library(${PROJECT_NAME} OBJECT ${sources})\n"
    assert code_txt[4] == "target_include_directories(${PROJECT_NAME} PRIVATE ${inclist})\n"
    assert code_txt[5] == "set_target_properties(${PROJECT_NAME} " \
                          "PROPERTIES VERSION ${PROJECT_VERSION})\n"

def test010_gen_lib_cmake_noinc():
    """!
    Test gen_lib_cmake, no inclide list
    """
    gen = ProjectFileGenerator(MockProjectDescription())
    proj_gen = GenerateCmakeFile(gen)

    code_txt = proj_gen.gen_lib_target("TestProj", 'sources')
    assert len(code_txt) == 5
    assert code_txt[0] == "####\n"
    assert code_txt[1] == "# TestProj library\n"
    assert code_txt[2] == "####\n"
    assert code_txt[3] == "add_library(${PROJECT_NAME} OBJECT ${sources})\n"
    assert code_txt[4] == "set_target_properties(${PROJECT_NAME} " \
                          "PROPERTIES VERSION ${PROJECT_VERSION})\n"

def test011_gen_lib_cmake_noinc():
    """!
    Test gen_lib_cmake, no inclide list, no source
    """
    gen = ProjectFileGenerator(MockProjectDescription())
    proj_gen = GenerateCmakeFile(gen)

    code_txt = proj_gen.gen_lib_target("TestProj")
    assert len(code_txt) == 0

def test012_gen_enable_unittest():
    """!
    Test gen_enable_unittest
    """
    gen = ProjectFileGenerator(MockProjectDescription())
    proj_gen = GenerateCmakeFile(gen)

    code_txt = proj_gen.gen_enable_unittest()
    assert len(code_txt) == 4
    assert code_txt[0] == "####\n"
    assert code_txt[1] == "# Enable testing\n"
    assert code_txt[2] == "####\n"
    assert code_txt[3] == "enable_testing()\n"

def test013_gen_enable_unittest_google():
    """!
    Test gen_enable_unittest
    """
    gen = ProjectFileGenerator(MockProjectDescription())
    proj_gen = GenerateCmakeFile(gen)

    code_txt = proj_gen.gen_enable_unittest(True)
    assert len(code_txt) == 5
    assert code_txt[0] == "####\n"
    assert code_txt[1] == "# Enable testing\n"
    assert code_txt[2] == "####\n"
    assert code_txt[3] == "enable_testing()\n"
    assert code_txt[4] == "include(GoogleTest)\n"

def test014_gen_unittest_target():
    """!
    Test gen_unittest_target
    """
    gen = ProjectFileGenerator(MockProjectDescription())
    proj_gen = GenerateCmakeFile(gen)

    code_txt = proj_gen.gen_unittest_target('TestSome_test',
                                            ['src/some.cpp', 'test/some_test.cpp'],
                                            'inclist')
    assert len(code_txt) == 13
    assert code_txt[0] == "####\n"
    assert code_txt[1] == "# TestSome_test unit test build\n"
    assert code_txt[2] == "####\n"
    assert code_txt[3] == "add_executable(TestSome_test src/some.cpp test/some_test.cpp)\n"
    assert code_txt[4] == "target_include_directories(TestSome_test PUBLIC ${inclist})\n"
    assert code_txt[5] == "if((${CMAKE_SYSTEM_NAME} MATCHES \"Linux\") AND " \
                          "(CMAKE_BUILD_TYPE MATCHES \"^[Dd]ebug\"))\n"
    assert code_txt[6] == "    target_compile_options(TestSome_test PRIVATE --coverage)\n"
    assert code_txt[7] == "    target_link_options(TestSome_test PRIVATE --coverage)\n"
    assert code_txt[8] == "endif()\n\n"

    assert code_txt[9] == "gtest_add_tests (TARGET TestSome_test TEST_LIST TestSome_testAllTests)\n\n"

    assert code_txt[10] == "if(\"${CMAKE_SYSTEM_NAME}\" == \"Windows\")\n"
    assert code_txt[11] == "    set_tests_properties(TestSome_testAllTests " \
                           "PROPERTIES ENVIRONMENT \"PATH=$<SHELL_PATH:$<TARGET_FILE_DIR" \
                           ":gtest>>$<SEMICOLON>$ENV{PATH}\")\n"
    assert code_txt[12] == "endif()\n"

def test015_gen_unittest_target_noinc():
    """!
    Test gen_unittest_target
    """
    gen = ProjectFileGenerator(MockProjectDescription())
    proj_gen = GenerateCmakeFile(gen)

    code_txt = proj_gen.gen_unittest_target('TestSome_test',
                                            ['src/some.cpp', 'test/some_test.cpp'])
    assert len(code_txt) == 12
    assert code_txt[0] == "####\n"
    assert code_txt[1] == "# TestSome_test unit test build\n"
    assert code_txt[2] == "####\n"
    assert code_txt[3] == "add_executable(TestSome_test src/some.cpp test/some_test.cpp)\n"
    assert code_txt[4] == "if((${CMAKE_SYSTEM_NAME} MATCHES \"Linux\") AND " \
                          "(CMAKE_BUILD_TYPE MATCHES \"^[Dd]ebug\"))\n"
    assert code_txt[5] == "    target_compile_options(TestSome_test PRIVATE --coverage)\n"
    assert code_txt[6] == "    target_link_options(TestSome_test PRIVATE --coverage)\n"
    assert code_txt[7] == "endif()\n\n"

    assert code_txt[8] == "gtest_add_tests (TARGET TestSome_test TEST_LIST TestSome_testAllTests)\n\n"

    assert code_txt[9] == "if(\"${CMAKE_SYSTEM_NAME}\" == \"Windows\")\n"
    assert code_txt[10] == "    set_tests_properties(TestSome_testAllTests " \
                           "PROPERTIES ENVIRONMENT \"PATH=$<SHELL_PATH:$<TARGET_FILE_DIR" \
                           ":gtest>>$<SEMICOLON>$ENV{PATH}\")\n"
    assert code_txt[11] == "endif()\n"

def test016_gen_unittest_target_nosrc():
    """!
    Test gen_unittest_target
    """
    gen = ProjectFileGenerator(MockProjectDescription())
    proj_gen = GenerateCmakeFile(gen)

    code_txt = proj_gen.gen_unittest_target('TestSome_test')
    assert len(code_txt) == 0

def test017_gen_unittest_target_with_google():
    """!
    Test gen_unittest_target
    """
    gen = ProjectFileGenerator(MockProjectDescription())
    proj_gen = GenerateCmakeFile(gen)

    code_txt = proj_gen.gen_unittest_target('TestSome_test',
                                            ['src/some.cpp', 'test/some_test.cpp'],
                                            'inclist',
                                            True)
    assert len(code_txt) == 15
    assert code_txt[0] == "####\n"
    assert code_txt[1] == "# TestSome_test unit test build\n"
    assert code_txt[2] == "####\n"
    assert code_txt[3] == "add_executable(TestSome_test src/some.cpp test/some_test.cpp)\n"
    assert code_txt[4] == "target_include_directories(TestSome_test PUBLIC ${inclist} " \
                          "${GTEST_INCLUDE_DIR})\n"
    assert code_txt[5] == "target_link_libraries(TestSome_test PRIVATE ${GTEST_LIBRARIES})\n"
    assert code_txt[6] == "target_compile_options(TestSome_test PUBLIC -DGTEST_LINKED_AS_SHARED_LIBRARY=1)\n"
    assert code_txt[7] == "if((${CMAKE_SYSTEM_NAME} MATCHES \"Linux\") AND " \
                          "(CMAKE_BUILD_TYPE MATCHES \"^[Dd]ebug\"))\n"
    assert code_txt[8] == "    target_compile_options(TestSome_test PRIVATE --coverage)\n"
    assert code_txt[9] == "    target_link_options(TestSome_test PRIVATE --coverage)\n"
    assert code_txt[10] == "endif()\n\n"

    assert code_txt[11] == "gtest_add_tests (TARGET TestSome_test TEST_LIST TestSome_testAllTests)\n\n"

    assert code_txt[12] == "if(\"${CMAKE_SYSTEM_NAME}\" == \"Windows\")\n"
    assert code_txt[13] == "    set_tests_properties(TestSome_testAllTests " \
                           "PROPERTIES ENVIRONMENT \"PATH=$<SHELL_PATH:$<TARGET_FILE_DIR" \
                           ":gtest>>$<SEMICOLON>$ENV{PATH}\")\n"
    assert code_txt[14] == "endif()\n"

def test018_gen_unittest_target_noinc_with_google():
    """!
    Test gen_unittest_target, no inc, with google
    """
    gen = ProjectFileGenerator(MockProjectDescription())
    proj_gen = GenerateCmakeFile(gen)

    code_txt = proj_gen.gen_unittest_target('TestSome_test',
                                            ['src/some.cpp', 'test/some_test.cpp'],
                                            None,
                                            True)
    assert len(code_txt) == 15
    assert code_txt[0] == "####\n"
    assert code_txt[1] == "# TestSome_test unit test build\n"
    assert code_txt[2] == "####\n"
    assert code_txt[3] == "add_executable(TestSome_test src/some.cpp test/some_test.cpp)\n"
    assert code_txt[4] == "target_include_directories(TestSome_test PUBLIC " \
                          "${GTEST_INCLUDE_DIR})\n"
    assert code_txt[5] == "target_link_libraries(TestSome_test PRIVATE ${GTEST_LIBRARIES})\n"
    assert code_txt[6] == "target_compile_options(TestSome_test PUBLIC -DGTEST_LINKED_AS_SHARED_LIBRARY=1)\n"
    assert code_txt[7] == "if((${CMAKE_SYSTEM_NAME} MATCHES \"Linux\") AND " \
                          "(CMAKE_BUILD_TYPE MATCHES \"^[Dd]ebug\"))\n"
    assert code_txt[8] == "    target_compile_options(TestSome_test PRIVATE --coverage)\n"
    assert code_txt[9] == "    target_link_options(TestSome_test PRIVATE --coverage)\n"
    assert code_txt[10] == "endif()\n\n"

    assert code_txt[11] == "gtest_add_tests (TARGET TestSome_test TEST_LIST TestSome_testAllTests)\n\n"

    assert code_txt[12] == "if(\"${CMAKE_SYSTEM_NAME}\" == \"Windows\")\n"
    assert code_txt[13] == "    set_tests_properties(TestSome_testAllTests " \
                           "PROPERTIES ENVIRONMENT \"PATH=$<SHELL_PATH:$<TARGET_FILE_DIR" \
                           ":gtest>>$<SEMICOLON>$ENV{PATH}\")\n"
    assert code_txt[14] == "endif()\n"

def test020_generate_cmake():
    """!
    @brief Test generate_cmake
    """
    gen = ProjectFileGenerator(MockProjectDescription())
    gen.add_include_dir('inc')
    gen._add_file('source', 'src/some.cpp')
    gen._add_file('source', 'src/some_english.cpp', 'english')
    gen._add_file('unittest', 'test/some_test.cpp')
    gen._add_file('unittest', 'test/some_english_test.cpp', 'english')
    gen._add_select_file('LocalSelelect_linux_test.cpp', 'LocalSelelect_linux_test')
    mockfile = MockFile()
    proj_gen = GenerateCmakeFile(gen)

    with patch('builtins.open', mock_open()) as openmock:
        openmock.return_value = mockfile

        assert proj_gen.generate_cmake("baseDir", True)
        openmock.assert_called_once_with("baseDir/CMakeLists.txt",
                                          mode = 'wt',
                                          encoding="utf-8")

        assert len(mockfile.mock_calls) == 16

def test021_generate_cmake_open_error(capsys):
    """!
    @brief Test generate_cmake
    """
    gen = ProjectFileGenerator(MockProjectDescription())
    gen.add_include_dir('inc')
    gen._add_file('source', 'src/some.cpp')
    gen._add_file('source', 'src/some_english.cpp', 'english')
    gen._add_file('unittest', 'test/some_test.cpp')
    gen._add_file('unittest', 'test/some_english_test.cpp', 'english')

    proj_gen = GenerateCmakeFile(gen)

    with patch('builtins.open', mock_open()) as openmock:
        openmock.side_effect = OSError

        assert not proj_gen.generate_cmake("baseDir", True)
        openmock.assert_called_once_with("baseDir/CMakeLists.txt",
                                            mode = 'wt',
                                            encoding="utf-8")
        assert capsys.readouterr().out == "Failed to open cmake file 'baseDir/CMakeLists.txt' for writing\n"

# pylint: enable=protected-access
