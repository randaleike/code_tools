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
import pytest
from unittest.mock import mock_open, patch

from code_tools_grocsoftware.base.eula import EulaText
from code_tools_grocsoftware.base.json_string_class_description import StringClassDescription
from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList
from code_tools_grocsoftware.base.project_json import ProjectDescription

from tests.dir_init import TESTFILEPATH

test_json_property = os.path.join(TESTFILEPATH,"testproperty.json")
test_json_lang = os.path.join(TESTFILEPATH,"teststringlanglist.json")
test_json_string = os.path.join(TESTFILEPATH,"teststrdesc.json")

def test001_constructor_default():
    """!
    @brief Test constructor, default input
    """
    test_obj = ProjectDescription()

    assert test_obj.filename == "jsonProjectDescription.json"
    assert isinstance(test_obj.project_json_data, dict)
    assert test_obj.project_json_data['eula_name'] == "MIT_open"
    assert test_obj.project_json_data['custom_text'] == []
    assert test_obj.project_json_data['langDataFile'] is None
    assert test_obj.project_json_data['stringDataFile'] is None
    assert test_obj.project_json_data['baseDirName'] == ""
    assert test_obj.project_json_data['inc_subdir'] == ""
    assert test_obj.project_json_data['src_subdir'] == ""
    assert test_obj.project_json_data['test_subdir'] is None
    assert test_obj.project_json_data['mock_subdir'] is None
    assert test_obj.project_json_data['owner'] == "Unknown"
    assert test_obj.project_json_data['groupName'] is None
    assert test_obj.project_json_data['groupDesc'] is None

def test002_get_eula():
    """!
    @brief Test get_eula
    """
    test_obj = ProjectDescription()
    eula_text = test_obj.get_eula()

    assert isinstance(eula_text, EulaText)

def test003_set_eula_name():
    """!
    @brief Test set_eula_name
    """
    test_obj = ProjectDescription()
    test_obj.set_eula_name("TestEula")

    assert test_obj.project_json_data['eula_name'] == "TestEula"

def test004_get_lang_data():
    """!
    @brief Test get_lang_data
    """
    test_obj = ProjectDescription()
    lang_data = test_obj.get_lang_data()

    assert isinstance(lang_data, LanguageDescriptionList)

def test005_set_lang_data_name():
    """!
    @brief Test set_lang_data_name
    """
    test_obj = ProjectDescription()
    test_obj.set_lang_data_name("TestLangData")

    assert test_obj.project_json_data['langDataFile'] == "TestLangData"

def test006_get_string_data():
    """!
    @brief Test get_string_data
    """
    test_obj = ProjectDescription()
    string_data = test_obj.get_string_data()

    assert isinstance(string_data, StringClassDescription)

def test007_set_string_data_name():
    """!
    @brief Test set_string_data_name
    """
    test_obj = ProjectDescription()
    test_obj.set_string_data_name("TestStringData")

    assert test_obj.project_json_data['stringDataFile'] == "TestStringData"

def test008_get_owner():
    """!
    @brief Test get_owner
    """
    test_obj = ProjectDescription()
    owner = test_obj.get_owner()

    assert isinstance(owner, str)
    assert owner == "Unknown"

def test009_set_owner():
    """!
    @brief Test set_owner
    """
    test_obj = ProjectDescription()
    test_obj.set_owner("TestOwner")
    assert test_obj.get_owner() == "TestOwner"

def test010_get_base_dir_name():
    """!
    @brief Test get_base_dir_name
    """
    test_obj = ProjectDescription()
    base_dir_name = test_obj.get_base_dir_name()

    assert isinstance(base_dir_name, str)
    assert base_dir_name == ""

def test011_set_base_dir_name():
    """!
    @brief Test set_base_dir_name
    """
    test_obj = ProjectDescription()
    test_obj.set_base_dir_name("TestBaseDir")

    assert test_obj.get_base_dir_name() == "TestBaseDir"

def test012_get_inc_subdir():
    """!
    @brief Test get_inc_subdir
    """
    test_obj = ProjectDescription()
    inc_subdir = test_obj.get_inc_subdir()

    assert isinstance(inc_subdir, str)
    assert inc_subdir == ""

def test013_set_inc_subdir():
    """!
    @brief Test set_inc_subdir
    """
    test_obj = ProjectDescription()
    test_obj.set_inc_subdir("TestIncSubdir")

    assert test_obj.get_inc_subdir() == "TestIncSubdir"

def test014_get_src_subdir():
    """!
    @brief Test get_src_subdir
    """
    test_obj = ProjectDescription()
    src_subdir = test_obj.get_src_subdir()

    assert isinstance(src_subdir, str)
    assert src_subdir == ""

def test015_set_src_subdir():
    """!
    @brief Test set_src_subdir
    """
    test_obj = ProjectDescription()
    test_obj.set_src_subdir("TestSrcSubdir")

    assert test_obj.get_src_subdir() == "TestSrcSubdir"

def test016_get_test_subdir():
    """!
    @brief Test get_test_subdir
    """
    test_obj = ProjectDescription()
    test_subdir = test_obj.get_test_subdir()

    assert test_subdir is None

def test017_set_test_subdir():
    """!
    @brief Test set_test_subdir
    """
    test_obj = ProjectDescription()
    test_obj.set_test_subdir("TestTestSubdir")

    assert test_obj.get_test_subdir() == "TestTestSubdir"

def test018_get_mock_subdir():
    """!
    @brief Test get_mock_subdir
    """
    test_obj = ProjectDescription()
    mock_subdir = test_obj.get_mock_subdir()
    assert mock_subdir is None

def test019_set_mock_subdir():
    """!
    @brief Test set_mock_subdir
    """
    test_obj = ProjectDescription()
    test_obj.set_mock_subdir("TestMockSubdir")

    assert test_obj.get_mock_subdir() == "TestMockSubdir"

def test020_set_eula_text():
    """!
    @brief Test set_custom_eula_text
    """
    test_obj = ProjectDescription()
    test_obj.set_custom_eula_text(["Line 1", "Line 2"])

    assert test_obj.project_json_data['custom_text'] == ["Line 1", "Line 2"]
    assert isinstance(test_obj.get_eula(), EulaText)

def test021_get_group_name():
    """!
    @brief Test get_group_name
    """
    test_obj = ProjectDescription()
    group_name = test_obj.get_group_name()

    assert group_name is None

def test022_set_group_name():
    """!
    @brief Test set_group_name
    """
    test_obj = ProjectDescription()
    test_obj.set_group_name("TestGroup")

    assert test_obj.get_group_name() == "TestGroup"

def test023_get_group_desc():
    """!
    @brief Test get_group_desc
    """
    test_obj = ProjectDescription()
    group_desc = test_obj.get_group_desc()

    assert group_desc is None

def test024_set_group_desc():
    """!
    @brief Test set_group_desc
    """
    test_obj = ProjectDescription()
    test_obj.set_group_desc("TestGroupDesc")

    assert test_obj.get_group_desc() == "TestGroupDesc"

def test025_set_custom_eula_fail():
    """!
    @brief Test set_custom_eula_text
    """
    test_obj = ProjectDescription()

    with pytest.raises(TypeError):
        test_obj.set_custom_eula_text("Line 1")
        assert test_obj.project_json_data['custom_text'] == []

def test025_get_custom_eula():
    """!
    @brief Test get_custom_eula
    """
    test_obj = ProjectDescription()
    test_obj.set_custom_eula_text(["Line 1", "Line 2"])
    custom_eula = test_obj.get_eula()

    assert isinstance(custom_eula, EulaText)
    assert test_obj.project_json_data['custom_text'] == ["Line 1", "Line 2"]

def test026_get_custom_eula_text():
    """!
    @brief Test get_custom_eula_text
    """
    test_obj = ProjectDescription()
    testdata = test_obj.get_custom_text()
    assert isinstance(testdata, list)
    assert testdata == []

def test030_clear():
    """!
    @brief Test clear method
    """
    test_obj = ProjectDescription()
    test_obj.set_test_subdir("TestTestSubdir")
    test_obj.set_mock_subdir("TestMockSubdir")
    test_obj.set_inc_subdir("TestIncSubdir")
    test_obj.set_src_subdir("TestSrcSubdir")
    test_obj.set_base_dir_name("TestBaseDir")
    test_obj.set_lang_data_name("TestLangData")
    test_obj.set_string_data_name("TestStringData")
    test_obj.set_owner("TestOwner")
    test_obj.set_eula_name("Other")
    test_obj.set_group_name("TestGroup")
    test_obj.set_group_desc("TestGroupDesc")
    test_obj.clear()

    assert test_obj.project_json_data['eula_name'] == "MIT_open"
    assert test_obj.project_json_data['custom_text'] == []
    assert test_obj.project_json_data['langDataFile'] is None
    assert test_obj.project_json_data['stringDataFile'] is None
    assert test_obj.project_json_data['baseDirName'] == ""
    assert test_obj.project_json_data['inc_subdir'] == ""
    assert test_obj.project_json_data['src_subdir'] == ""
    assert test_obj.project_json_data['test_subdir'] is None
    assert test_obj.project_json_data['mock_subdir'] is None
    assert test_obj.project_json_data['owner'] == "Unknown"
    assert test_obj.project_json_data['groupName'] is None
    assert test_obj.project_json_data['groupDesc'] is None

def test031_constructor_with_file():
    """!
    @brief Test update method
    """
    testdata = '{\n'
    testdata += '  "eula_name":"MIT_closed",\n'
    testdata += '  "custom_text": [],\n'
    testdata += '  "langDataFile":"data/test_lang.json",\n'
    testdata += '  "stringDataFile":"data/test_string.json",\n'
    testdata += '  "baseDirName":"foo",\n'
    testdata += '  "inc_subdir": "inc",\n'
    testdata += '  "src_subdir": "src",\n'
    testdata += '  "test_subdir": "test",\n'
    testdata += '  "mock_subdir": "mock",\n'
    testdata += '  "owner": "Henry",\n'
    testdata += '  "groupName": "frank",\n'
    testdata += '  "groupDesc": "Group desc"\n'
    testdata += '}'

    # Mock the open function to return the test data
    with patch('builtins.open', mock_open(read_data = testdata)) as mocked_file:
        # Create a ProjectDescription object and set some values
        # This will also call the update method
        test_obj = ProjectDescription("temp_test_project.json")

        mocked_file.assert_called_once_with("temp_test_project.json", 'r', encoding='utf-8')

        # Check the attributes of the object
        assert test_obj.filename == "temp_test_project.json"
        assert isinstance(test_obj.project_json_data, dict)
        assert test_obj.project_json_data['eula_name'] == "MIT_closed"
        assert test_obj.project_json_data['custom_text'] == []
        assert test_obj.project_json_data['langDataFile'] == "data/test_lang.json"
        assert test_obj.project_json_data['stringDataFile'] == "data/test_string.json"
        assert test_obj.project_json_data['baseDirName'] == "foo"
        assert test_obj.project_json_data['inc_subdir'] == "inc"
        assert test_obj.project_json_data['src_subdir'] == "src"
        assert test_obj.project_json_data['test_subdir'] == "test"
        assert test_obj.project_json_data['mock_subdir'] == "mock"
        assert test_obj.project_json_data['owner'] == "Henry"
        assert test_obj.project_json_data['groupName'] == "frank"
        assert test_obj.project_json_data['groupDesc'] == "Group desc"

def test032_update():
    """!
    @brief Test update method
    """
    # Create a ProjectDescription object and set some values
    # This will also call the update method
    test_obj = ProjectDescription()
    test_obj.set_eula_name("TestEula")
    test_obj.set_lang_data_name("TestLangData")
    test_obj.set_string_data_name("TestStringData")
    test_obj.set_base_dir_name("TestBaseDir")
    test_obj.set_inc_subdir("TestIncSubdir")
    test_obj.set_src_subdir("TestSrcSubdir")
    test_obj.set_test_subdir("TestTestSubdir")
    test_obj.set_mock_subdir("TestMockSubdir")
    test_obj.set_owner("TestOwner")
    test_obj.set_group_name("TestGroup")
    test_obj.set_group_desc("TestGroupDesc")

    # Mock the open function to check if it is called correctly
    with patch('builtins.open', mock_open()) as mocked_file:
        # Update the JSON file
        test_obj.filename = "temp_test_project.json"  # Set a temporary filename
        test_obj.update()

        mocked_file.assert_called_once_with("temp_test_project.json", 'w', encoding='utf-8')

        # Check that the file was written with the expected content
        assert len(mocked_file.mock_calls) == 54
        mocked_file().write.assert_any_call(': ')    # add count
        mocked_file().write.assert_any_call(',\n  ') # add count

        mocked_file().write.assert_any_call('{')
        mocked_file().write.assert_any_call('\n')
        mocked_file().write.assert_any_call('"eula_name"')
        mocked_file().write.assert_any_call('"TestEula"')

        mocked_file().write.assert_any_call('"custom_text"')
        mocked_file().write.assert_any_call('[]')

        mocked_file().write.assert_any_call('"langDataFile"')
        mocked_file().write.assert_any_call('"TestLangData"')

        mocked_file().write.assert_any_call('"stringDataFile"')
        mocked_file().write.assert_any_call('"TestStringData"')

        mocked_file().write.assert_any_call('"baseDirName"')
        mocked_file().write.assert_any_call('"TestBaseDir"')

        mocked_file().write.assert_any_call('"inc_subdir"')
        mocked_file().write.assert_any_call('"TestIncSubdir"')

        mocked_file().write.assert_any_call('"src_subdir"')
        mocked_file().write.assert_any_call('"TestSrcSubdir"')

        mocked_file().write.assert_any_call('"test_subdir"')
        mocked_file().write.assert_any_call('"TestTestSubdir"')

        mocked_file().write.assert_any_call('"mock_subdir"')
        mocked_file().write.assert_any_call('"TestMockSubdir"')

        mocked_file().write.assert_any_call('"owner"')
        mocked_file().write.assert_any_call('"TestOwner"')

        mocked_file().write.assert_any_call('"groupName"')
        mocked_file().write.assert_any_call('"TestGroup"')

        mocked_file().write.assert_any_call('"groupDesc"')
        mocked_file().write.assert_any_call('"TestGroupDesc"')

        mocked_file().write.assert_any_call('}')

