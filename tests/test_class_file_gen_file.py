# pylint: disable=protected-access

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
from unittest.mock import patch

from code_tools_grocsoftware.base.eula import EulaText
from code_tools_grocsoftware.base.param_return_tools import ParamRetDict
from code_tools_grocsoftware.base.translate_text_parser import TransTxtParser

from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList
from code_tools_grocsoftware.base.json_string_class_description import StringClassDescription
from code_tools_grocsoftware.base.project_json import ProjectDescription
from code_tools_grocsoftware.cpp_gen.class_file_gen import GenerateLangFiles

from tests.dir_init import TESTFILEPATH

langfilename = os.path.join(TESTFILEPATH, "teststringlanglist.json")
strclass_filename = os.path.join(TESTFILEPATH, "teststrdesc.json")

class MockEulaText():
    """!
    @brief Mock EulaText for testing
    """
    def format_eula_name(self):
        """!
        @brief Get the EULA name
        """
        return "Mock EULA"

    def format_eula_text(self):
        """!
        @brief Get the EULA text
        """
        return ["Mock EULA text"]


class MockProjectDescription(ProjectDescription):
    """!
    @brief Mock ProjectDescription for testing
    """
    def get_eula(self)->EulaText:
        """!
        @brief Get the EULA object from the JSON data
        @return (EulaText) - EULA object
        """
        return MockEulaText()

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

    def get_owner(self)->str:
        """!
        @brief Get the owner of the project
        @return (string) - Owner name
        """
        return "mock_owner"

    def get_base_selection_name(self):
        """!
        @brief Get the base selection name from the JSON data
        @return (string) - Base selection name
        """
        return "mockBaseSelection"

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

def test001_write_inc_file():
    """!
    @brief Test write_inc_file, base, no group
    """
    mock_file = MockFile()
    class_gen = GenerateLangFiles(MockProjectDescription())
    class_gen.write_inc_file(mock_file)

    assert len(mock_file.mock_calls) == 19
    assert len(mock_file.writedata) == 61

def test002_write_inc_file_lang():
    """!
    @brief Test write_inc_file, base, no group
    """
    mock_file = MockFile()

    class_gen = GenerateLangFiles(MockProjectDescription())
    class_gen.write_inc_file(mock_file, "english")

    assert len(mock_file.mock_calls) == 16
    assert len(mock_file.writedata) == 75

def test003_write_inc_file_with_group():
    """!
    @brief Test write_inc_file, base, no group
    """
    mock_file = MockFile()
    mock_gname = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_group_name'
    mock_gdesc = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_group_desc'

    with patch (mock_gname) as mock_group_name:
        mock_group_name.return_value = "TestGroup"
        with patch (mock_gdesc) as mock_group_desc:
            mock_group_desc.return_value = "Group desc"

            class_gen = GenerateLangFiles(MockProjectDescription())
            class_gen.write_inc_file(mock_file)

            assert len(mock_file.mock_calls) == 22
            assert len(mock_file.writedata) == 77

def test004_write_inc_file_with_using():
    """!
    @brief Test write_inc_file, base, no group
    """
    mock_file = MockFile()
    mock_ginc = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_include_using'

    with patch (mock_ginc) as mock_get_inc:
        mock_get_inc.return_value = [{'localName':"parserstr", 'stdName':"std::string", 'desc':None}]
        class_gen = GenerateLangFiles(MockProjectDescription())
        class_gen.write_inc_file(mock_file)

        assert len(mock_file.mock_calls) == 21
        assert len(mock_file.writedata) == 63

def test011_write_base_src_file():
    """!
    @brief Test write_base_src_file, no group, no using
    """
    mock_file = MockFile()
    class_gen = GenerateLangFiles(MockProjectDescription())
    class_gen.write_base_src_file(mock_file)

    assert len(mock_file.mock_calls) == 12
    assert len(mock_file.writedata) == 108

def test012_write_base_src_file_with_group():
    """!
    @brief Test write_base_src_file, with group, no using
    """
    mock_file = MockFile()
    mock_gname = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_group_name'
    mock_gdesc = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_group_desc'

    with patch (mock_gname) as mock_group_name:
        mock_group_name.return_value = "TestGroup"
        with patch (mock_gdesc) as mock_group_desc:
            mock_group_desc.return_value = "Group desc"

            class_gen = GenerateLangFiles(MockProjectDescription())
            class_gen.write_base_src_file(mock_file)

            assert len(mock_file.mock_calls) == 15
            assert len(mock_file.writedata) == 124

def test013_write_base_src_file_with_using():
    """!
    @brief Test write_base_src_file, with using, no group
    """
    mock_file = MockFile()
    mock_ginc = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_base_src_using'

    with patch (mock_ginc) as mock_get_inc:
        mock_get_inc.return_value = [{'localName':"parserstr", 'stdName':"std::string", 'desc':None}]

        class_gen = GenerateLangFiles(MockProjectDescription())
        class_gen.write_base_src_file(mock_file)

        assert len(mock_file.mock_calls) == 14
        assert len(mock_file.writedata) == 110

def test021_write_lang_src_file():
    """!
    @brief Test write_lang_src_file, no group, no using
    """
    mock_file = MockFile()
    class_gen = GenerateLangFiles(MockProjectDescription())
    class_gen.write_lang_src_file(mock_file, "english")

    assert len(mock_file.mock_calls) == 12
    assert len(mock_file.writedata) == 30

def test022_write_lang_src_file_with_group():
    """!
    @brief Test write_lang_src_file, with group, no using
    """
    mock_file = MockFile()
    mock_gname = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_group_name'
    mock_gdesc = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_group_desc'

    with patch (mock_gname) as mock_group_name:
        mock_group_name.return_value = "TestGroup"
        with patch (mock_gdesc) as mock_group_desc:
            mock_group_desc.return_value = "Group desc"

            class_gen = GenerateLangFiles(MockProjectDescription())
            class_gen.write_lang_src_file(mock_file, "english")

            assert len(mock_file.mock_calls) == 15
            assert len(mock_file.writedata) == 46

def test023_write_lang_src_file_with_using():
    """!
    @brief Test write_lang_src_file, no group, with using
    """
    mock_file = MockFile()
    mock_ginc = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_lang_src_using'

    with patch (mock_ginc) as mock_get_inc:
        mock_get_inc.return_value = [{'localName':"parserstr", 'stdName':"std::string", 'desc':None}]

        class_gen = GenerateLangFiles(MockProjectDescription())
        class_gen.write_lang_src_file(mock_file, "english")

        assert len(mock_file.mock_calls) == 14
        assert len(mock_file.writedata) == 32

def test030_write_lang_src_file():
    """!
    @brief Test write_lang_src_file, no group, no using
    """
    mock_file = MockFile()
    class_gen = GenerateLangFiles(MockProjectDescription())
    class_gen.write_base_unittest_file(mock_file)

    assert len(mock_file.mock_calls) == 9
    assert len(mock_file.writedata) == 55

def test031_write_base_unittest_file_with_group():
    """!
    @brief Test test030_write_base_unittest_file, with group, no using
    """
    mock_file = MockFile()
    mock_gname = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_group_name'
    mock_gdesc = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_group_desc'

    with patch (mock_gname) as mock_group_name:
        mock_group_name.return_value = "TestGroup"
        with patch (mock_gdesc) as mock_group_desc:
            mock_group_desc.return_value = "Group desc"

            class_gen = GenerateLangFiles(MockProjectDescription())
            class_gen.write_base_unittest_file(mock_file)

            assert len(mock_file.mock_calls) == 13
            assert len(mock_file.writedata) == 72

def test032_write_base_unittest_file_with_using():
    """!
    @brief Test test030_write_base_unittest_file, no group, with using
    """
    mock_file = MockFile()
    mock_ginc = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_base_src_using'

    with patch (mock_ginc) as mock_get_inc:
        mock_get_inc.return_value = [{'localName':"parserstr", 'stdName':"std::string", 'desc':None}]

        class_gen = GenerateLangFiles(MockProjectDescription())
        class_gen.write_base_unittest_file(mock_file)

        assert len(mock_file.mock_calls) == 11
        assert len(mock_file.writedata) == 57

def test040_write_selection_unittest_file():
    """!
    @brief Test write_selection_unittest_file, no group, no using
    """
    mock_file = MockFile()
    class_gen = GenerateLangFiles(MockProjectDescription())
    class_gen.write_selection_unittest_file(mock_file, class_gen.os_lang_sel_list[0])

    assert len(mock_file.mock_calls) == 9
    assert len(mock_file.writedata) == 449

def test041_write_selection_unittest_file_with_group():
    """!
    @brief Test write_selection_unittest_file, with group, no using
    """
    mock_file = MockFile()
    mock_gname = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_group_name'
    mock_gdesc = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_group_desc'

    with patch (mock_gname) as mock_group_name:
        mock_group_name.return_value = "TestGroup"
        with patch (mock_gdesc) as mock_group_desc:
            mock_group_desc.return_value = "Group desc"

            class_gen = GenerateLangFiles(MockProjectDescription())
            class_gen.write_selection_unittest_file(mock_file, class_gen.os_lang_sel_list[0])

            assert len(mock_file.mock_calls) == 13
            assert len(mock_file.writedata) == 466

def test042_write_selection_unittest_file_with_using():
    """!
    @brief Test write_selection_unittest_file, no group, with using
    """
    mock_file = MockFile()
    mock_ginc = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_base_src_using'

    with patch (mock_ginc) as mock_get_inc:
        mock_get_inc.return_value = [{'localName':"parserstr", 'stdName':"std::string", 'desc':None}]

        class_gen = GenerateLangFiles(MockProjectDescription())
        class_gen.write_selection_unittest_file(mock_file, class_gen.os_lang_sel_list[0])

        assert len(mock_file.mock_calls) == 11
        assert len(mock_file.writedata) == 451

def test050_write_lang_unittest_file():
    """!
    @brief Test write_lang_unittest_file, no group, no using
    """
    mock_file = MockFile()
    class_gen = GenerateLangFiles(MockProjectDescription())
    class_gen.test_param_values['nargs']= ("3", False)
    class_gen.write_lang_unittest_file(mock_file, "english")

    assert len(mock_file.mock_calls) == 10
    assert len(mock_file.writedata) == 37

def test051_write_lang_unittest_file_with_group():
    """!
    @brief Test write_lang_unittest_file, with group, no using
    """
    mock_file = MockFile()
    mock_gname = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_group_name'
    mock_gdesc = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_group_desc'

    with patch (mock_gname) as mock_group_name:
        mock_group_name.return_value = "TestGroup"
        with patch (mock_gdesc) as mock_group_desc:
            mock_group_desc.return_value = "Group desc"

            class_gen = GenerateLangFiles(MockProjectDescription())
            class_gen.test_param_values['nargs']= ("3", False)
            class_gen.write_lang_unittest_file(mock_file, "english")

            assert len(mock_file.mock_calls) == 14
            assert len(mock_file.writedata) == 54

def test052_write_lang_unittest_file_with_using():
    """!
    @brief Test write_lang_unittest_file, no group, with using
    """
    mock_file = MockFile()
    mock_ginc = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_base_src_using'

    with patch (mock_ginc) as mock_get_inc:
        mock_get_inc.return_value = [{'localName':"parserstr", 'stdName':"std::string", 'desc':None}]

        class_gen = GenerateLangFiles(MockProjectDescription())
        class_gen.test_param_values['nargs']= ("3", False)
        class_gen.write_lang_unittest_file(mock_file, "english")

        assert len(mock_file.mock_calls) == 12
        assert len(mock_file.writedata) == 39

def test060_generate_property_unittest():
    """!
    @brief Test _generate_property_unittest, no params, single return, non-text
    """
    mock_jsonstr = StringClassDescription
    mock_jsonlang = LanguageDescriptionList

    pparams = []
    pret = ParamRetDict.build_return_dict_with_mod("integer", "Test ret desc", 0)

    with patch.object(mock_jsonstr, 'get_property_method_data') as get_method_data:
        get_method_data.return_value = ("testData", "test desc", pparams, pret)
        with patch.object(mock_jsonlang, 'is_property_text') as lang_is_text:
            lang_is_text.return_value = False
            with patch.object(mock_jsonlang, 'get_property_data') as get_prop_data:
                get_prop_data.return_value = 42

                class_gen = GenerateLangFiles(MockProjectDescription())
                code_txt = class_gen._generate_property_unittest("mock_property",
                                                                    "english")

                get_method_data.assert_called_once_with("mock_property")
                lang_is_text.assert_called_once_with("testData")
                get_prop_data.assert_called_once_with("english", "testData")

                assert len(code_txt) == 6
                assert code_txt[0] == 'TEST(ParserStringListInterfaceEnglish, fetchmock_property)\n'
                assert code_txt[1] == '{\n'
                assert code_txt[2] == '    ParserStringListInterfaceEnglish testvar;\n'
                assert code_txt[3] == '    int output = testvar.mock_property();\n'
                assert code_txt[4] == '    EXPECT_EQ(42, output);\n'
                assert code_txt[5] == '}\n'

def test061_generate_property_unittest_text():
    """!
    @brief Test _generate_property_unittest, no params, single return, text
    """
    mock_jsonstr = StringClassDescription
    mock_jsonlang = LanguageDescriptionList

    pparams = []
    pret = ParamRetDict.build_return_dict_with_mod("string", "Test ret desc", 0)

    with patch.object(mock_jsonstr, 'get_property_method_data') as get_method_data:
        get_method_data.return_value = ("testData", "test desc", pparams, pret)
        with patch.object(mock_jsonlang, 'is_property_text') as lang_is_text:
            lang_is_text.return_value = True
            with patch.object(mock_jsonlang, 'get_property_data') as get_prop_data:
                get_prop_data.return_value = "42"

                class_gen = GenerateLangFiles(MockProjectDescription())
                code_txt = class_gen._generate_property_unittest("mock_property",
                                                                    "english")

                get_method_data.assert_called_once_with("mock_property")
                lang_is_text.assert_called_once_with("testData")
                get_prop_data.assert_called_once_with("english", "testData")

                assert len(code_txt) == 6
                assert code_txt[0] == 'TEST(ParserStringListInterfaceEnglish, fetchmock_property)\n'
                assert code_txt[1] == '{\n'
                assert code_txt[2] == '    ParserStringListInterfaceEnglish testvar;\n'
                assert code_txt[3] == '    std::string output = testvar.mock_property();\n'
                assert code_txt[4] == '    EXPECT_STREQ("42", output.c_str());\n'
                assert code_txt[5] == '}\n'

def test062_generate_property_unittest_list_int():
    """!
    @brief Test _generate_property_unittest, no params, list return, non-text
    """
    mock_jsonstr = StringClassDescription
    mock_jsonlang = LanguageDescriptionList

    pparams = []
    pret = ParamRetDict.build_return_dict_with_mod("integer", "Test ret desc", ParamRetDict.type_mod_list)

    with patch.object(mock_jsonstr, 'get_property_method_data') as get_method_data:
        get_method_data.return_value = ("testData", "test desc", pparams, pret)
        with patch.object(mock_jsonlang, 'is_property_text') as lang_is_text:
            lang_is_text.return_value = False
            with patch.object(mock_jsonlang, 'get_property_data') as get_prop_data:
                get_prop_data.return_value = [42, 24]

                class_gen = GenerateLangFiles(MockProjectDescription())
                code_txt = class_gen._generate_property_unittest("mock_property",
                                                                    "english")

                get_method_data.assert_called_once_with("mock_property")
                lang_is_text.assert_called_once_with("testData")
                get_prop_data.assert_called_once_with("english", "testData")

                assert len(code_txt) == 7
                assert code_txt[0] == 'TEST(ParserStringListInterfaceEnglish, fetchmock_property)\n'
                assert code_txt[1] == '{\n'
                assert code_txt[2] == '    ParserStringListInterfaceEnglish testvar;\n'
                assert code_txt[3] == '    std::list<int> output = testvar.mock_property();\n'
                assert code_txt[4] == '    EXPECT_EQ(42, output.pop_front());\n'
                assert code_txt[5] == '    EXPECT_EQ(24, output.pop_front());\n'
                assert code_txt[6] == '}\n'

def test063_generate_property_unittest_list_text():
    """!
    @brief Test _generate_property_unittest, no params, list return, non-text
    """
    mock_jsonstr = StringClassDescription
    mock_jsonlang = LanguageDescriptionList

    pparams = []
    pret = ParamRetDict.build_return_dict_with_mod("string", "Test ret desc", ParamRetDict.type_mod_list)

    with patch.object(mock_jsonstr, 'get_property_method_data') as get_method_data:
        get_method_data.return_value = ("testData", "test desc", pparams, pret)
        with patch.object(mock_jsonlang, 'is_property_text') as lang_is_text:
            lang_is_text.return_value = True
            with patch.object(mock_jsonlang, 'get_property_data') as get_prop_data:
                get_prop_data.return_value = ["foo", "goo", "moo"]

                class_gen = GenerateLangFiles(MockProjectDescription())
                code_txt = class_gen._generate_property_unittest("mock_property",
                                                                    "english")

                get_method_data.assert_called_once_with("mock_property")
                lang_is_text.assert_called_once_with("testData")
                get_prop_data.assert_called_once_with("english", "testData")

                assert len(code_txt) == 8
                assert code_txt[0] == 'TEST(ParserStringListInterfaceEnglish, fetchmock_property)\n'
                assert code_txt[1] == '{\n'
                assert code_txt[2] == '    ParserStringListInterfaceEnglish testvar;\n'
                assert code_txt[3] == '    std::list<std::string> output = testvar.mock_property();\n'
                assert code_txt[4] == '    EXPECT_STREQ("foo", output.pop_front().c_str());\n'
                assert code_txt[5] == '    EXPECT_STREQ("goo", output.pop_front().c_str());\n'
                assert code_txt[6] == '    EXPECT_STREQ("moo", output.pop_front().c_str());\n'
                assert code_txt[7] == '}\n'

def test064_generate_property_unittest_with_text_params():
    """!
    @brief Test _generate_property_unittest, with params, single return, non-text
    """
    mock_jsonstr = StringClassDescription
    mock_jsonlang = LanguageDescriptionList

    pparams = [ParamRetDict.build_param_dict("wtf", "integer", "What the f?")]
    pret = ParamRetDict.build_return_dict_with_mod("integer", "Test ret desc", 0)

    with patch.object(mock_jsonstr, 'get_property_method_data') as get_method_data:
        get_method_data.return_value = ("testData", "test desc", pparams, pret)
        with patch.object(mock_jsonlang, 'is_property_text') as lang_is_text:
            lang_is_text.return_value = False
            with patch.object(mock_jsonlang, 'get_property_data') as get_prop_data:
                get_prop_data.return_value = 42

                class_gen = GenerateLangFiles(MockProjectDescription())
                class_gen.test_param_values['wtf'] = ('yes', True)
                code_txt = class_gen._generate_property_unittest("mock_property",
                                                                    "english")

                get_method_data.assert_called_once_with("mock_property")
                lang_is_text.assert_called_once_with("testData")
                get_prop_data.assert_called_once_with("english", "testData")

                assert len(code_txt) == 6
                assert code_txt[0] == 'TEST(ParserStringListInterfaceEnglish, fetchmock_property)\n'
                assert code_txt[1] == '{\n'
                assert code_txt[2] == '    ParserStringListInterfaceEnglish testvar;\n'
                assert code_txt[3] == '    int output = testvar.mock_property("yes");\n'
                assert code_txt[4] == '    EXPECT_EQ(42, output);\n'
                assert code_txt[5] == '}\n'

def test065_generate_property_unittest_with_nontext_params():
    """!
    @brief Test _generate_property_unittest, with params, single return, non-text
    """
    mock_jsonstr = StringClassDescription
    mock_jsonlang = LanguageDescriptionList

    pparams = [ParamRetDict.build_param_dict("wtf", "integer", "What the f?")]
    pret = ParamRetDict.build_return_dict_with_mod("integer", "Test ret desc", 0)

    with patch.object(mock_jsonstr, 'get_property_method_data') as get_method_data:
        get_method_data.return_value = ("testData", "test desc", pparams, pret)
        with patch.object(mock_jsonlang, 'is_property_text') as lang_is_text:
            lang_is_text.return_value = False
            with patch.object(mock_jsonlang, 'get_property_data') as get_prop_data:
                get_prop_data.return_value = 42

                class_gen = GenerateLangFiles(MockProjectDescription())
                class_gen.test_param_values['wtf'] = ("1", False)
                code_txt = class_gen._generate_property_unittest("mock_property",
                                                                    "english")

                get_method_data.assert_called_once_with("mock_property")
                lang_is_text.assert_called_once_with("testData")
                get_prop_data.assert_called_once_with("english", "testData")

                assert len(code_txt) == 6
                assert code_txt[0] == 'TEST(ParserStringListInterfaceEnglish, fetchmock_property)\n'
                assert code_txt[1] == '{\n'
                assert code_txt[2] == '    ParserStringListInterfaceEnglish testvar;\n'
                assert code_txt[3] == '    int output = testvar.mock_property(1);\n'
                assert code_txt[4] == '    EXPECT_EQ(42, output);\n'
                assert code_txt[5] == '}\n'

def test070_generate_translate_unittest():
    """!
    @brief Test _generate_translate_unittest, no params
    """
    mock_jsonstr = StringClassDescription
    mock_jsonlang = LanguageDescriptionList

    pparams = []
    pret = ParamRetDict.build_return_dict_with_mod("string", "Test ret desc", 0)
    txt_list = TransTxtParser.parse_translate_string("this is a test")

    with patch.object(mock_jsonstr, 'get_tranlate_method_function_data') as get_method_data:
        get_method_data.return_value = ("test desc", pparams, pret)
        with patch.object(mock_jsonstr, 'get_tranlate_method_text_data') as get_trans_data:
            get_trans_data.return_value = txt_list
            with patch.object(mock_jsonlang, 'get_iso_code_data') as lang_iso:
                lang_iso.return_value = "en"

                class_gen = GenerateLangFiles(MockProjectDescription())
                code_txt = class_gen._generate_translate_unittest("mock_trans",
                                                                    "english")

                get_method_data.assert_called_once_with("mock_trans")
                get_trans_data.assert_called_once_with("mock_trans", "en")
                lang_iso.assert_called_once_with("english")

                assert len(code_txt) == 6
                assert code_txt[0] == 'TEST(ParserStringListInterfaceEnglish, printmock_trans)\n'
                assert code_txt[1] == '{\n'
                assert code_txt[2] == '    ParserStringListInterfaceEnglish testvar;\n'
                assert code_txt[3] == '    std::string output = testvar.mock_trans();\n'
                assert code_txt[4] == '    EXPECT_STREQ("this is a test", output.c_str());\n'
                assert code_txt[5] == '}\n'

def test071_generate_translate_unittest_nontext_param():
    """!
    @brief Test _generate_translate_unittest, no params
    """
    mock_jsonstr = StringClassDescription
    mock_jsonlang = LanguageDescriptionList

    pparams = [ParamRetDict.build_param_dict("wtf", "integer", "What the f?")]
    pret = ParamRetDict.build_return_dict_with_mod("string", "Test ret desc", 0)
    txt_list = TransTxtParser.parse_translate_string("this is a @wtf@ test")

    with patch.object(mock_jsonstr, 'get_tranlate_method_function_data') as get_method_data:
        get_method_data.return_value = ("test desc", pparams, pret)
        with patch.object(mock_jsonstr, 'get_tranlate_method_text_data') as get_trans_data:
            get_trans_data.return_value = txt_list
            with patch.object(mock_jsonlang, 'get_iso_code_data') as lang_iso:
                lang_iso.return_value = "en"

                class_gen = GenerateLangFiles(MockProjectDescription())
                class_gen.test_param_values['wtf'] = ("12", False)
                code_txt = class_gen._generate_translate_unittest("mock_trans",
                                                                    "english")

                get_method_data.assert_called_once_with("mock_trans")
                get_trans_data.assert_called_once_with("mock_trans", "en")
                lang_iso.assert_called_once_with("english")

                assert len(code_txt) == 6
                assert code_txt[0] == 'TEST(ParserStringListInterfaceEnglish, printmock_trans)\n'
                assert code_txt[1] == '{\n'
                assert code_txt[2] == '    ParserStringListInterfaceEnglish testvar;\n'
                assert code_txt[3] == '    std::string output = testvar.mock_trans(12);\n'
                assert code_txt[4] == '    EXPECT_STREQ("this is a 12 test", output.c_str());\n'
                assert code_txt[5] == '}\n'

def test072_generate_translate_unittest_text_param():
    """!
    @brief Test _generate_translate_unittest, no params
    """
    mock_jsonstr = StringClassDescription
    mock_jsonlang = LanguageDescriptionList

    pparams = [ParamRetDict.build_param_dict("wtf", "string", "What the f?")]
    pret = ParamRetDict.build_return_dict_with_mod("string", "Test ret desc", 0)
    txt_list = TransTxtParser.parse_translate_string("this is a @wtf@ test")

    with patch.object(mock_jsonstr, 'get_tranlate_method_function_data') as get_method_data:
        get_method_data.return_value = ("test desc", pparams, pret)
        with patch.object(mock_jsonstr, 'get_tranlate_method_text_data') as get_trans_data:
            get_trans_data.return_value = txt_list
            with patch.object(mock_jsonlang, 'get_iso_code_data') as lang_iso:
                lang_iso.return_value = "en"

                class_gen = GenerateLangFiles(MockProjectDescription())
                class_gen.test_param_values['wtf'] = ("foo", True)
                code_txt = class_gen._generate_translate_unittest("mock_trans",
                                                                    "english")

                get_method_data.assert_called_once_with("mock_trans")
                get_trans_data.assert_called_once_with("mock_trans", "en")
                lang_iso.assert_called_once_with("english")

                assert len(code_txt) == 6
                assert code_txt[0] == 'TEST(ParserStringListInterfaceEnglish, printmock_trans)\n'
                assert code_txt[1] == '{\n'
                assert code_txt[2] == '    ParserStringListInterfaceEnglish testvar;\n'
                assert code_txt[3] == '    std::string output = testvar.mock_trans("foo");\n'
                assert code_txt[4] == '    EXPECT_STREQ("this is a foo test", output.c_str());\n'
                assert code_txt[5] == '}\n'

def test081_write_mock_inc_file():
    """!
    @brief Test write_mock_inc_file, base, no group
    """
    mock_file = MockFile()
    class_gen = GenerateLangFiles(MockProjectDescription())
    class_gen.write_mock_inc_file(mock_file)

    assert len(mock_file.mock_calls) == 15
    assert len(mock_file.writedata) == 36

def test082_write_mock_inc_file_with_group():
    """!
    @brief Test write_mock_inc_file, base, no group
    """
    mock_file = MockFile()
    mock_gname = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_group_name'
    mock_gdesc = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_group_desc'

    with patch (mock_gname) as mock_group_name:
        mock_group_name.return_value = "TestGroup"
        with patch (mock_gdesc) as mock_group_desc:
            mock_group_desc.return_value = "Group desc"

            class_gen = GenerateLangFiles(MockProjectDescription())
            class_gen.write_mock_inc_file(mock_file)

            assert len(mock_file.mock_calls) == 18
            assert len(mock_file.writedata) == 52

def test091_write_mock_src_file():
    """!
    @brief Test write_mock_src_file, no group, no using, no extra
    """
    mock_file = MockFile()
    class_gen = GenerateLangFiles(MockProjectDescription())
    class_gen.write_mock_src_file(mock_file)

    assert len(mock_file.mock_calls) == 13
    assert len(mock_file.writedata) == 35

def test092_write_mock_src_file_with_group():
    """!
    @brief Test write_mock_src_file, with group, no using, no extra
    """
    mock_file = MockFile()
    mock_gname = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_group_name'
    mock_gdesc = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_group_desc'

    with patch (mock_gname) as mock_group_name:
        mock_group_name.return_value = "TestGroup"
        with patch (mock_gdesc) as mock_group_desc:
            mock_group_desc.return_value = "Group desc"

            class_gen = GenerateLangFiles(MockProjectDescription())
            class_gen.write_mock_src_file(mock_file)

            assert len(mock_file.mock_calls) == 16
            assert len(mock_file.writedata) == 51

def test093_write_mock_src_file_with_using():
    """!
    @brief Test write_mock_src_file, with using, no group, no extra
    """
    mock_file = MockFile()
    mock_ginc = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_base_src_using'

    with patch (mock_ginc) as mock_get_inc:
        mock_get_inc.return_value = [{'localName':"parserstr", 'stdName':"std::string", 'desc':None}]

        class_gen = GenerateLangFiles(MockProjectDescription())
        class_gen.write_mock_src_file(mock_file)

        assert len(mock_file.mock_calls) == 13
        assert len(mock_file.writedata) == 36

def test094_write_mock_src_file_with_extra():
    """!
    @brief Test write_mock_src_file, no using, no group, with extra
    """
    mock_file = MockFile()
    mock_extra = 'code_tools_grocsoftware.base.json_string_class_description.'
    mock_extra += 'StringClassDescription.get_extra_mock'

    with patch (mock_extra) as mock_get_extra:
        mock_get_extra.return_value = ['#if defined(foo)\n',
                                       '    //Comment\n',
                                       '    something.do();\n',
                                       '#endif //defined(foo)']

        class_gen = GenerateLangFiles(MockProjectDescription())
        class_gen.write_mock_src_file(mock_file)

        assert len(mock_file.mock_calls) == 16
        assert len(mock_file.writedata) == 41

# pylint: enable=protected-access
