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
import pytest

from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList
from code_tools_grocsoftware.base.json_string_class_description import StringClassDescription

from code_tools_grocsoftware.base.project_json import ProjectDescription
from code_tools_grocsoftware.cpp_gen.project_file_gen import ProjectFileGenerator

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

    def get_inc_subdir(self)->str:
        """!
        @brief Get the include subdirectory name from the JSON data
        @return (string) - Include subdirectory name
        """
        return 'inc'

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

# pylint: disable=protected-access

def test002_add_inculde_dir():
    """!
    @brief Test add_include_dir method
    """
    proj_gen = ProjectFileGenerator(MockProjectDescription())
    assert not proj_gen.inc_subdirs

    proj_gen.add_inculde_dir("test_dir")
    assert "test_dir" in proj_gen.inc_subdirs
    assert len(proj_gen.inc_subdirs) == 1

    proj_gen.add_inculde_dir("test_dir2")
    assert "test_dir2" in proj_gen.inc_subdirs
    assert len(proj_gen.inc_subdirs) == 2

def test003_add_file():
    """!
    @brief Test _add_file method
    """
    proj_gen = ProjectFileGenerator(MockProjectDescription())
    assert not proj_gen.fnames

    proj_gen._add_file("source", "test_file.cpp", "english")
    assert len(proj_gen.fnames['english']) == 1

    proj_gen._add_file("source", "test_file2.cpp", "english")
    assert len(proj_gen.fnames['english']) == 1

    proj_gen._add_file("include", "test_file.h", "english")
    assert len(proj_gen.fnames['english']) == 2

    proj_gen._add_file("include", "base_file.h")
    assert len(proj_gen.fnames['base']) == 1

    proj_gen._add_file("source", "base_file.cpp")
    assert len(proj_gen.fnames['base']) == 2

    proj_gen._add_file("mockInclude", "mock_file.h")
    assert len(proj_gen.fnames['base']) == 3

    proj_gen._add_file("mockSource", "mock_file.cpp")
    assert len(proj_gen.fnames['base']) == 4

    proj_gen._add_file("unittest", "test_file.cpp", "spanish")
    assert len(proj_gen.fnames['spanish']) == 1

    # Check if the file names are correctly stored
    assert proj_gen.fnames['english']['source'] == "test_file2.cpp"
    assert proj_gen.fnames['english']['include'] == "test_file.h"
    assert proj_gen.fnames['base']['source'] == "base_file.cpp"
    assert proj_gen.fnames['base']['include'] == "base_file.h"
    assert proj_gen.fnames['base']['mockInclude'] == "mock_file.h"
    assert proj_gen.fnames['base']['mockSource'] == "mock_file.cpp"
    assert proj_gen.fnames['spanish']['unittest'] == "test_file.cpp"

def test004_get_include_dirs():
    """!
    @brief Test _add_file method with no language specified
    """
    proj_gen = ProjectFileGenerator(MockProjectDescription())
    assert not proj_gen.inc_subdirs

    proj_gen.add_inculde_dir("test_dir")
    proj_gen.add_inculde_dir("test_dir2")

    inc_dirs = proj_gen.get_include_dirs()
    assert isinstance(inc_dirs, list)
    assert len(inc_dirs) == 2

    assert "test_dir" in inc_dirs
    assert "test_dir2" in inc_dirs

def test005_get_include_fnames():
    """!
    @brief Test get_include_fnames method
    """
    proj_gen = ProjectFileGenerator(MockProjectDescription())

    proj_gen._add_file("source", "test_file.cpp", "english")
    proj_gen._add_file("include", "test_file.h", "english")
    proj_gen._add_file("include", "base_file.h")
    proj_gen._add_file("source", "base_file.cpp")
    proj_gen._add_file("mockInclude", "mock_file.h")
    proj_gen._add_file("mockSource", "mock_file.cpp")
    proj_gen._add_file("unittest", "test_file.cpp", "spanish")

    tstlist = proj_gen.get_include_fnames()
    assert isinstance(tstlist, list)
    assert len(tstlist) == 2

    assert "test_file.h" in tstlist
    assert "base_file.h" in tstlist

def test006_get_source_fnames():
    """!
    @brief Test get_include_fnames method
    """
    proj_gen = ProjectFileGenerator(MockProjectDescription())

    proj_gen._add_file("source", "test_file.cpp", "english")
    proj_gen._add_file("include", "test_file.h", "english")
    proj_gen._add_file("include", "base_file.h")
    proj_gen._add_file("source", "base_file.cpp")
    proj_gen._add_file("mockInclude", "mock_file.h")
    proj_gen._add_file("mockSource", "mock_file.cpp")
    proj_gen._add_file("unittest", "test_file.cpp", "spanish")

    tstlist = proj_gen.get_source_fnames()
    assert isinstance(tstlist, list)
    assert len(tstlist) == 2

    assert "test_file.cpp" in tstlist
    assert "base_file.cpp" in tstlist

def test007_get_mock_include_fnames():
    """!
    @brief Test get_mock_include_fnames method
    """
    proj_gen = ProjectFileGenerator(MockProjectDescription())

    proj_gen._add_file("source", "test_file.cpp", "english")
    proj_gen._add_file("include", "test_file.h", "english")
    proj_gen._add_file("include", "base_file.h")
    proj_gen._add_file("source", "base_file.cpp")
    proj_gen._add_file("mockInclude", "mock_file.h")
    proj_gen._add_file("mockSource", "mock_file.cpp")
    proj_gen._add_file("unittest", "test_file.cpp", "spanish")

    tstlist = proj_gen.get_mock_include_fnames()
    assert isinstance(tstlist, list)
    assert len(tstlist) == 1

    assert "mock_file.h" in tstlist

def test008_get_unittest_set_names():
    """!
    @brief Test get_unittest_set_names method
    """
    proj_gen = ProjectFileGenerator(MockProjectDescription())

    proj_gen._add_file("source", "entest_file.cpp", "english")
    proj_gen._add_file("include", "entest_file.h", "english")
    proj_gen._add_file("source", "estest_file.cpp", "spanish")
    proj_gen._add_file("include", "estest_file.h", "spanish")

    proj_gen._add_file("include", "base_file.h")
    proj_gen._add_file("source", "base_file.cpp")
    proj_gen._add_file("mockInclude", "mock_file.h")
    proj_gen._add_file("mockSource", "mock_file.cpp")
    proj_gen._add_file("unittest", "en_unittest_file.cpp", "english")
    proj_gen._add_file("unittest", "es_unittest_file.cpp", "spanish")

    # Check if the unittest set names are generated correctly
    tstlist = proj_gen.get_unittest_set_names()
    assert len(tstlist) == 2
    entuple = ('english', 'entest_file.cpp',
               'en_unittest_file.cpp', 'ParserStringListInterfaceEnglish_test')
    estuple = ('spanish', 'estest_file.cpp',
               'es_unittest_file.cpp', 'ParserStringListInterfaceSpanish_test')

    assert entuple in tstlist
    assert estuple in tstlist

def test009_get_unittest_set_names_no_source():
    """!
    @brief Test get_unittest_set_names method with no source file
    """
    proj_gen = ProjectFileGenerator(MockProjectDescription())

    proj_gen._add_file("unittest", "en_test_file_unittest.cpp", "english")
    proj_gen._add_file("unittest", "es_unittest_file.cpp", "spanish")

    tstlist = proj_gen.get_unittest_set_names()
    assert isinstance(tstlist, list)
    assert len(tstlist) == 0

    # Check if the unittest set names are generated correctly
    proj_gen._add_file("source", "en_test_file.cpp", "english")
    tstlist = proj_gen.get_unittest_set_names()
    assert len(tstlist) == 1

    # Check if the unittest set names are generated correctly with no unittest file
    proj_gen._add_file("source", "es_test_file.cpp", "spanish")
    tstlist = proj_gen.get_unittest_set_names()
    assert len(tstlist) == 2
    entuple = ('english', 'en_test_file.cpp',
               'en_test_file_unittest.cpp', 'ParserStringListInterfaceEnglish_test')
    estuple = ('english', 'en_test_file.cpp',
               'en_test_file_unittest.cpp', 'ParserStringListInterfaceEnglish_test')
    assert estuple in tstlist
    assert entuple in tstlist

def test010_get_unittest_set_names_no_unittest():
    """!
    @brief Test get_unittest_set_names method with no unittest file
    """
    proj_gen = ProjectFileGenerator(MockProjectDescription())

    proj_gen._add_file("source", "en_test_file.cpp", "english")
    proj_gen._add_file("source", "es_test_file.cpp", "spanish")

    tstlist = proj_gen.get_unittest_set_names()
    assert isinstance(tstlist, list)
    assert len(tstlist) == 0

    # Check if the unittest set names are generated correctly
    proj_gen._add_file("unittest", "en_test_file_unittest.cpp", "english")
    tstlist = proj_gen.get_unittest_set_names()
    assert len(tstlist) == 1
    entuple = ('english', 'en_test_file.cpp',
               'en_test_file_unittest.cpp', 'ParserStringListInterfaceEnglish_test')
    assert entuple in tstlist

    # Check if the unittest set names are generated correctly with no unittest file
    proj_gen._add_file("unittest", "es_unittest_file.cpp", "spanish")
    tstlist = proj_gen.get_unittest_set_names()
    assert len(tstlist) == 2
    estuple = ('spanish', 'es_test_file.cpp',
               'es_unittest_file.cpp', 'ParserStringListInterfaceSpanish_test')
    assert estuple in tstlist
    assert entuple in tstlist

def test011_make_subdir_exist():
    """!
    @brief Test _make_subdir, already exists
    """
    with patch('os.path.exists') as path_exists:
        path_exists.return_value = True

        proj_gen = ProjectFileGenerator(MockProjectDescription())
        proj_gen._make_subdir("test")

        path_exists.assert_called_once_with("test")

def test012_make_subdir_notexist():
    """!
    @brief Test _make_subdir, exists = false
    """
    with patch('os.path.exists') as path_exists:
        path_exists.return_value = False
        with patch('os.mkdir') as os_mkdir:
            os_mkdir.return_value = True

            proj_gen = ProjectFileGenerator(MockProjectDescription())
            proj_gen._make_subdir("test")

            path_exists.assert_called_once_with("test")
            os_mkdir.assert_called_once_with("test")

def test013_make_subdir_make_permission_fail(capsys):
    """!
    @brief Test _make_subdir, exists = false, make fail = permission
    """
    with patch('os.path.exists') as path_exists:
        path_exists.return_value = False
        with patch('os.mkdir') as os_mkdir:
            os_mkdir.return_value = False
            os_mkdir.side_effect = PermissionError

            proj_gen = ProjectFileGenerator(MockProjectDescription())
            proj_gen._make_subdir("test")

            path_exists.assert_called_once_with("test")
            os_mkdir.assert_called_once_with("test")
            captured = capsys.readouterr()
            assert captured.out == "Permission denied: Unable to create 'test'.\n"

def test014_make_subdir_make_oserror_fail(capsys):
    """!
    @brief Test _make_subdir, exists = false, make fail = OSError
    """
    with patch('os.path.exists') as path_exists:
        path_exists.return_value = False
        with patch('os.mkdir') as os_mkdir:
            os_mkdir.return_value = False
            os_mkdir.side_effect = OSError

            proj_gen = ProjectFileGenerator(MockProjectDescription())
            proj_gen._make_subdir("test")

            path_exists.assert_called_once_with("test")
            os_mkdir.assert_called_once_with("test")
            captured = capsys.readouterr()
            assert captured.out == "OS Error occurred creating: test.\n"

def test015_make_dirs_nobase(capsys):
    """!
    @brief Test _make_subdir, exists = True
    """
    with patch('os.path.exists') as path_exists:
        path_exists.return_value = False
        with pytest.raises(NameError):

            proj_gen = ProjectFileGenerator(MockProjectDescription())
            assert not proj_gen.make_dirs("baseDirName")

            path_exists.assert_called_once_with("baseDirName")
            captured = capsys.readouterr()
            assert captured.out == "ERROR: base directory 'baseDirName' does not exist\n"

def test016_make_dirs_existing():
    """!
    @brief Test make_dirs, exists = True
    """
    with patch('os.path.exists') as path_exists:
        path_exists.return_value = True
        with patch('os.mkdir') as os_mkdir:
            os_mkdir.return_value = True

            proj_gen = ProjectFileGenerator(MockProjectDescription())
            assert proj_gen.make_dirs("baseDirName")

            assert path_exists.call_count == 5
            assert os_mkdir.call_count == 0

            path_exists.assert_any_call("baseDirName")
            path_exists.assert_any_call("baseDirName/inc")
            path_exists.assert_any_call("baseDirName/src")
            path_exists.assert_any_call("baseDirName/test")
            path_exists.assert_any_call("baseDirName/mock")

def test017_make_dirs():
    """!
    @brief Test make_dirs, exists = false
    """
    with patch('os.path.exists') as path_exists:
        path_exists.side_effect = [True, False, False, False, False]
        with patch('os.mkdir') as os_mkdir:
            os_mkdir.return_value = True

            proj_gen = ProjectFileGenerator(MockProjectDescription())
            assert proj_gen.make_dirs("baseDirName")

            assert path_exists.call_count == 5
            assert os_mkdir.call_count == 4

            path_exists.assert_any_call("baseDirName")

            path_exists.assert_any_call("baseDirName/inc")
            os_mkdir.assert_any_call("baseDirName/inc")

            path_exists.assert_any_call("baseDirName/src")
            os_mkdir.assert_any_call("baseDirName/src")

            path_exists.assert_any_call("baseDirName/test")
            os_mkdir.assert_any_call("baseDirName/test")

            path_exists.assert_any_call("baseDirName/mock")
            os_mkdir.assert_any_call("baseDirName/mock")

def test018_make_dirs_fail():
    """!
    @brief Test make_dirs, make failure
    """
    with patch('os.path.exists') as path_exists:
        path_exists.side_effect = [True, False, False, False, False]
        with patch('os.mkdir') as os_mkdir:
            os_mkdir.return_value = False
            os_mkdir.side_effect = OSError

            proj_gen = ProjectFileGenerator(MockProjectDescription())
            assert not proj_gen.make_dirs("baseDirName")

            assert path_exists.call_count == 5
            assert os_mkdir.call_count == 4

def test020_generate_files():
    """!
    @brief Test generate_files, exists = false
    """
    proj_gen = ProjectFileGenerator(MockProjectDescription())
    class_gen = 'code_tools_grocsoftware.cpp_gen.class_file_gen.GenerateLangFiles.'

    with patch(class_gen+'write_inc_file') as wrt_inc:
        with patch(class_gen+'write_base_src_file') as wrt_base:
            with patch(class_gen+'write_lang_src_file') as wrt_lang_src:
                with patch(class_gen+'write_base_unittest_file') as wrt_baseut:
                    with patch(class_gen+'write_selection_unittest_file') as wrt_slct_ut:
                        with patch(class_gen+'write_lang_unittest_file') as wrt_lang_ut:
                            with patch(class_gen+'write_mock_inc_file') as wrt_mock_inc:
                                with patch(class_gen+'write_mock_src_file') as wrt_mock_src:
                                    with patch('builtins.open', mock_open()) as mocked_file:
                                        proj_gen.generate_files("baseDirName")


                                        mocked_file.assert_any_call("baseDirName/inc/" \
                                                                    "ParserStringListInterface.h",
                                                                    mode = 'wt',
                                                                    encoding="utf-8")
                                        mocked_file.assert_any_call("baseDirName/src/" \
                                                                    "ParserStringListInterface.cpp",
                                                                    mode = 'wt',
                                                                    encoding="utf-8")

                                        mocked_file.assert_any_call("baseDirName/test/" \
                                                                    "ParserStringListInterface" \
                                                                    "_test.cpp",
                                                                    mode = 'wt',
                                                                    encoding="utf-8")

                                        mocked_file.assert_any_call("baseDirName/mock/" \
                                                                    "mock_" \
                                                                    "ParserStringListInterface.h",
                                                                    mode = 'wt',
                                                                    encoding="utf-8")
                                        mocked_file.assert_any_call("baseDirName/mock/" \
                                                                    "mock_" \
                                                                    "ParserStringListInterface.cpp",
                                                                    mode = 'wt',
                                                                    encoding="utf-8")

                                        mocked_file.assert_any_call("baseDirName/test/" \
                                                                    "LocalLanguageSelect_" \
                                                                    "Linux_test.cpp",
                                                                    mode = 'wt',
                                                                    encoding="utf-8")
                                        mocked_file.assert_any_call("baseDirName/test/" \
                                                                    "LocalLanguageSelect_" \
                                                                    "Windows_test.cpp",
                                                                    mode = 'wt',
                                                                    encoding="utf-8")

                                        mocked_file.assert_any_call("baseDirName/inc/" \
                                                                    "ParserStringListInterface" \
                                                                    "English.h",
                                                                    mode = 'wt',
                                                                    encoding="utf-8")
                                        mocked_file.assert_any_call("baseDirName/inc/" \
                                                                    "ParserStringListInterface" \
                                                                    "Spanish.h",
                                                                    mode = 'wt',
                                                                    encoding="utf-8")
                                        mocked_file.assert_any_call("baseDirName/src/" \
                                                                    "ParserStringListInterface" \
                                                                    "English.cpp",
                                                                    mode = 'wt',
                                                                    encoding="utf-8")
                                        mocked_file.assert_any_call("baseDirName/src/" \
                                                                    "ParserStringListInterface" \
                                                                    "Spanish.cpp",
                                                                    mode = 'wt',
                                                                    encoding="utf-8")

                                        mocked_file.assert_any_call("baseDirName/test/" \
                                                                    "ParserStringListInterface" \
                                                                    "English_test.cpp",
                                                                    mode = 'wt',
                                                                    encoding="utf-8")
                                        mocked_file.assert_any_call("baseDirName/test/" \
                                                                    "ParserStringListInterface" \
                                                                    "Spanish_test.cpp",
                                                                    mode = 'wt',
                                                                    encoding="utf-8")

                                        assert wrt_inc.call_count == 3
                                        assert wrt_base.call_count == 1
                                        assert wrt_lang_src.call_count == 2
                                        assert wrt_baseut.call_count == 1
                                        assert wrt_slct_ut.call_count == 2
                                        assert wrt_lang_ut.call_count == 2
                                        assert wrt_mock_inc.call_count == 1
                                        assert wrt_mock_src.call_count == 1

# pylint: enable=protected-access
