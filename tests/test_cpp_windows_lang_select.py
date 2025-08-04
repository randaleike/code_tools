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

from code_tools_grocsoftware.base.param_return_tools import ParamRetDict
from code_tools_grocsoftware.base.eula import EulaText
from code_tools_grocsoftware.base.doxygen_gen_tools import CDoxyCommentGenerator
from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList
from code_tools_grocsoftware.cpp_gen.string_class_tools import BaseCppStringClassGenerator
from code_tools_grocsoftware.cpp_gen.windows_lang_select import WindowsLangSelectFunctionGenerator

from tests.dir_init import TESTFILEPATH
from tests.support_func import get_expected_extern

test_json_list = os.path.join(TESTFILEPATH,"teststringlanglist.json")

class DummyEulaText(EulaText):
    """!
    Dummy EulaText class for testing
    """
    def __init__(self):
        """!
        @brief DummyEulaText constructor
        """
        super().__init__(custom_eula=["Dummy EULA text for testing purposes"])

    @staticmethod
    def get_expected_eula()->list:
        """!
        @brief Get the expected EULA text
        @return {list} List of expected EULA text lines
        """
        return ["Dummy EULA text for testing purposes"]

# pylint: disable=protected-access

class TestClass01WindowsLangSelect:
    """!
    @brief Unit test for the BaseCppStringClassGenerator class
    """

    def default_setup(self, mocker):
        """!
        @brief Default setup for the tests
        """
        mock_project_data = mocker.Mock()
        mock_string_data = mocker.Mock()
        mock_project_data.get_string_data = mocker.Mock(return_value=mock_string_data)
        mock_project_data.get_lang_data = mocker.Mock(return_value=LanguageDescriptionList())
        mock_project_data.get_owner = mocker.Mock(return_value="TestOwner")
        mock_project_data.get_eula = mocker.Mock(return_value=DummyEulaText())

        mock_string_data.get_base_class_name = mocker.Mock(return_value="BaseClass")
        mock_string_data.get_dynamic_compile_switch = mocker.Mock(return_value="DYNAMIC_INTERNATIONALIZATION")

        return mock_project_data

    def langfile_setup(self, mocker, lang_list:LanguageDescriptionList):
        """!
        @brief Setup for the tests with a language list
        """
        mock_project_data = mocker.Mock()
        mock_string_data = mocker.Mock()
        mock_project_data.get_string_data = mocker.Mock(return_value=mock_string_data)
        mock_project_data.get_lang_data = mocker.Mock(return_value=lang_list)
        mock_project_data.get_owner = mocker.Mock(return_value="TestOwner")
        mock_project_data.get_eula = mocker.Mock(return_value=DummyEulaText())

        mock_string_data.get_base_class_name = mocker.Mock(return_value="BaseClass")
        mock_string_data.get_dynamic_compile_switch = mocker.Mock(return_value="DYNAMIC_INTERNATIONALIZATION")

        return mock_project_data
    
    def test001_constructor_default(self, mocker):
        """!
        @brief Test constructor, default input
        """
        test_obj = WindowsLangSelectFunctionGenerator(self.default_setup(mocker))

        assert test_obj.base_class_name == "BaseClass"
        assert test_obj.dynamic_compile_switch == "DYNAMIC_INTERNATIONALIZATION"
        assert test_obj.select_function_name == "getBaseClass_Windows"
        assert len(test_obj.param_dict_list) == 1
        desc = "Return value from GetUserDefaultUILanguage() call"
        assert test_obj.param_dict_list[0] == ParamRetDict.build_param_dict("lang_id",
                                                                            "LANGID",
                                                                            desc)
        assert test_obj.def_os_str == "(defined(_WIN64) || defined(_WIN32))"
        assert isinstance(test_obj.lang_json_data, LanguageDescriptionList)
        assert isinstance(test_obj.doxy_comment_gen, CDoxyCommentGenerator)

    def test002_constructor_non_default(self, mocker):
        """!
        @brief Test constructor, with input
        """
        mock_project_data = mocker.Mock()
        mock_string_data = mocker.Mock()
        mock_project_data.get_string_data = mocker.Mock(return_value=mock_string_data)
        mock_project_data.get_lang_data = mocker.Mock(return_value=LanguageDescriptionList())
        mock_project_data.get_owner = mocker.Mock(return_value="George")
        mock_project_data.get_eula = mocker.Mock(return_value=DummyEulaText())

        mock_string_data.get_base_class_name = mocker.Mock(return_value="TestBaseClass")
        mock_string_data.get_dynamic_compile_switch = mocker.Mock(return_value="TEST_DYNAM_SWITCH")

        test_obj = WindowsLangSelectFunctionGenerator(mock_project_data)

        assert test_obj.base_class_name == "TestBaseClass"
        assert test_obj.dynamic_compile_switch == "TEST_DYNAM_SWITCH"
        assert test_obj.select_function_name == "getTestBaseClass_Windows"
        assert len(test_obj.param_dict_list) == 1
        desc = "Return value from GetUserDefaultUILanguage() call"
        assert test_obj.param_dict_list[0] == ParamRetDict.build_param_dict("lang_id",
                                                                            "LANGID",
                                                                            desc)
        assert test_obj.def_os_str == "(defined(_WIN64) || defined(_WIN32))"
        assert isinstance(test_obj.lang_json_data, LanguageDescriptionList)
        assert isinstance(test_obj.doxy_comment_gen, CDoxyCommentGenerator)

    def test003_get_function_name(self, mocker):
        """!
        @brief Test get_function_name
        """
        test_obj = WindowsLangSelectFunctionGenerator(self.default_setup(mocker))
        assert test_obj.get_function_name() == "getBaseClass_Windows"

    def test004_get_os_define(self, mocker):
        """!
        @brief Test get_os_define
        """
        test_obj = WindowsLangSelectFunctionGenerator(self.default_setup(mocker))
        assert test_obj.get_os_define() == "(defined(_WIN64) || defined(_WIN32))"

    def test005_gen_function_define(self, mocker):
        """!
        @brief Test gen_function_define
        """
        cpp_gen = BaseCppStringClassGenerator()
        test_obj = WindowsLangSelectFunctionGenerator(self.default_setup(mocker))
        desc = "Determine the correct local language class from the input LANGID value"
        expected_list = cpp_gen.define_function_with_decorations(test_obj.select_function_name,
                                                                 desc,
                                                                 test_obj.param_dict_list,
                                                                 test_obj.base_intf_ret_ptr_dict)
        expected_list.append("{\n")

        test_list = test_obj.gen_function_define()
        assert len(test_list) == len(expected_list)
        for index, expected_text in enumerate(expected_list):
            assert test_list[index] == expected_text

    def test006_gen_function_end(self, mocker):
        """!
        @brief Test gen_function_end
        """
        test_obj = WindowsLangSelectFunctionGenerator(self.default_setup(mocker))
        assert test_obj.gen_function_end() == "} // end of "+test_obj.select_function_name+"()\n"

    def test007_gen_function(self, mocker):
        """!
        @brief Test gen_function
        """
        cpp_gen = BaseCppStringClassGenerator()
        lang_list = LanguageDescriptionList(test_json_list)
        test_obj = WindowsLangSelectFunctionGenerator(self.langfile_setup(mocker, lang_list))

        capture_list = test_obj.gen_function()

        assert len(capture_list) == 25

        assert capture_list[0] == "#if "+test_obj.def_os_str+"\n"
        assert capture_list[1] == cpp_gen.gen_include("<windows.h>")
        assert capture_list[2] == "\n"

        desc = "Determine the correct local language class from the input LANGID value"
        expected_list = cpp_gen.define_function_with_decorations(test_obj.select_function_name,
                                                                 desc,
                                                                 test_obj.param_dict_list,
                                                                 test_obj.base_intf_ret_ptr_dict)
        expected_list.append("{\n")
        for index, expected_text in enumerate(expected_list):
            assert capture_list[index+3] == expected_text

        capture_index = 3 + len(expected_list)
        param_name = ParamRetDict.get_param_name(test_obj.param_dict_list[0])
        assert capture_list[capture_index] == "    switch("+param_name+" & 0x0FF)\n"
        assert capture_list[capture_index+1] == "    {\n"

        capture_index += 2
        for lang_name in lang_list.get_language_list():
            lang_codes, _ = lang_list.get_langid_data(lang_name)
            for langid in lang_codes:
                assert capture_list[capture_index] == "        case "+hex(langid)+":\n"
                capture_index += 1

            retstr = cpp_gen._gen_make_ptr_return_statement(lang_name)
            assert capture_list[capture_index] == "            "+retstr
            assert capture_list[capture_index+1] == "            break;\n"
            capture_index += 2


        assert capture_list[capture_index] == "        default:\n"
        default_lang, _ = lang_list.get_default_data()
        retstr = cpp_gen._gen_make_ptr_return_statement(default_lang)
        assert capture_list[capture_index+1] == "            "+retstr
        assert capture_list[capture_index+2] == "    }\n"
        assert capture_list[capture_index+3] == "} // end of "+test_obj.select_function_name+"()\n"
        assert capture_list[capture_index+4] == "#endif // "+test_obj.def_os_str+"\n"

    def test008_gen_return_function_call(self, mocker):
        """!
        @brief Test gen_return_function_call
        """
        test_obj = WindowsLangSelectFunctionGenerator(self.default_setup(mocker))
        param_type = ParamRetDict.get_param_type(test_obj.param_dict_list[0])

        str_list = test_obj.gen_return_function_call()
        assert len(str_list) == 2
        assert str_list[0] == "    "+param_type+" lang_id = GetUserDefaultUILanguage();\n"
        assert str_list[1] == "    return "+test_obj.select_function_name+"(lang_id);\n"

    def test009_gen_unit_test_test(self, mocker):
        """!
        @brief Test _gen_unittest_test
        """
        test_obj = WindowsLangSelectFunctionGenerator(self.default_setup(mocker))

        doxy_gen = CDoxyCommentGenerator()
        doxy_desc = "Test "+test_obj.select_function_name+" 11 selection case"
        doxy_body = doxy_gen.gen_doxy_method_comment(doxy_desc, [])

        str_list = test_obj._gen_unittest_test("Foo", 11, "en", "get_iso_code")
        assert len(str_list) == 10
        assert str_list[0] == doxy_body[0]
        assert str_list[1] == doxy_body[1]
        assert str_list[2] == doxy_body[2]
        assert str_list[3] == doxy_body[3]

        assert str_list[4] == "TEST(WindowsSelectFunction, Foo)\n"
        assert str_list[5] == "{\n"
        assert str_list[6] == "    // Generate the test language string object\n"
        assert str_list[7] == "    "+test_obj.base_intf_ret_ptr_type+" test_var = " \
                              +test_obj.select_function_name+"(11);\n"
        assert str_list[8] == "    EXPECT_STREQ(\"en\", test_var->get_iso_code().c_str());\n"
        assert str_list[9] == "}\n"

    def test010_gen_extern_definition(self, mocker):
        """!
        @brief Test gen_extern_definition
        """
        test_obj = WindowsLangSelectFunctionGenerator(self.default_setup(mocker))
        expecteddef = get_expected_extern(test_obj.param_dict_list,
                                          test_obj.base_intf_ret_ptr_type,
                                          test_obj.select_function_name)
        assert test_obj.gen_extern_definition() == expecteddef

    def test011_gen_unit_test(self, mocker):
        """!
        @brief Test gen_unit_test
        """
        lang_list = LanguageDescriptionList(test_json_list)
        test_obj = WindowsLangSelectFunctionGenerator(self.langfile_setup(mocker, lang_list))
        text_list = test_obj.gen_unit_test("get_iso_code")

        # Test starting block
        assert len(text_list) == 423
        assert text_list[0] == "#if "+test_obj.def_os_str+"\n"
        assert text_list[1] == "\n"
        assert text_list[2] == "#include <windows.h>\n"
        assert text_list[3] == test_obj.gen_extern_definition()
        assert text_list[4] == "\n"

        # Match each test function
        text_index = 5
        for lang_name in lang_list.get_language_list():
            lang_codes, region_list = lang_list.get_langid_data(lang_name)
            iso_code = lang_list.get_iso_code_data(lang_name)
            for region in region_list:
                test_name = lang_name.capitalize()+"_"+str(region)+"_Selection"
                expected_test_text = test_obj._gen_unittest_test(test_name,
                                                                 region,
                                                                 iso_code,
                                                                 "get_iso_code")

                for index, expected_line in enumerate(expected_test_text):
                    assert text_list[text_index+index] == expected_line

                text_index += len(expected_test_text)
                assert text_list[text_index] == "\n"
                text_index += 1

            # Match unknown regions 00 test
            for lang_code in lang_codes:
                unkn_region_tstname = lang_name.capitalize()
                unkn_region_tstname += "_unknown_region_00"
                unkn_region_tstname += str(lang_code)
                unkn_region_tstname += "_Selection"
                expected_test_text = test_obj._gen_unittest_test(unkn_region_tstname,
                                                                  lang_code,
                                                                  iso_code,
                                                                  "get_iso_code")
                for index, expected_line in enumerate(expected_test_text):
                    assert text_list[text_index+index] == expected_line

                text_index += len(expected_test_text)
                assert text_list[text_index] == "\n"
                text_index += 1

            # Match unknown regions FFxx test
            for lang_code in lang_codes:
                unkn_region_tstname = lang_name.capitalize()
                unkn_region_tstname += "_unknown_region_FF"
                unkn_region_tstname += str(lang_code)
                unkn_region_tstname += "_Selection"
                expected_test_text = test_obj._gen_unittest_test(unkn_region_tstname,
                                                                 0xFF00+lang_code,
                                                                 iso_code,
                                                                 "get_iso_code")

                for index, expected_line in enumerate(expected_test_text):
                    assert text_list[text_index+index] == expected_line

                text_index += len(expected_test_text)
                assert text_list[text_index] == "\n"
                text_index += 1

        # Match default test
        _, default_iso_code = lang_list.get_default_data()
        unknown_lang_body = test_obj._gen_unittest_test("UnknownLanguageDefaultSelection",
                                                        0,
                                                        default_iso_code,
                                                        "get_iso_code")
        for index, expected_line in enumerate(unknown_lang_body):
            assert text_list[text_index+index] == expected_line

        text_index += len(expected_test_text)

        # Match end
        assert text_list[422] == "#endif // "+test_obj.def_os_str+"\n"
        assert text_index == 422

    def test012_gen_unit_test_function_call(self, mocker):
        """!
        @brief Test gen_unittest_function_call
        """
        test_obj = WindowsLangSelectFunctionGenerator(self.default_setup(mocker))
        text_list = test_obj.gen_unittest_function_call("check_var")

        param_type = ParamRetDict.get_param_type(test_obj.param_dict_list[0])

        assert len(text_list) == 2
        assert text_list[0] == "    "+param_type+" lang_id = GetUserDefaultUILanguage();\n"
        assert text_list[1] == "    "+test_obj.base_intf_ret_ptr_type+" check_var = " \
                               +test_obj.select_function_name+"(lang_id);\n"

    def test013_get_unittest_extern_include(self, mocker):
        """!
        @brief Test get_unittest_extern_include
        """
        test_obj = WindowsLangSelectFunctionGenerator(self.default_setup(mocker))
        text_list = test_obj.get_unittest_extern_include()

        assert len(text_list) == 4
        assert text_list[0] == "#if "+test_obj.def_os_str+"\n"
        assert text_list[1] == "#include <windows.h>\n"
        assert text_list[2] == get_expected_extern(test_obj.param_dict_list,
                                                   test_obj.base_intf_ret_ptr_type,
                                                   test_obj.select_function_name)
        assert text_list[3] == "#endif // "+test_obj.def_os_str+"\n"

    def test014_get_unittest_file_name(self, mocker):
        """!
        @brief Test get_unittest_file_name
        """
        test_obj = WindowsLangSelectFunctionGenerator(self.default_setup(mocker))
        cpp_name, test_name = test_obj.get_unittest_file_name()
        assert cpp_name == "LocalLanguageSelect_Windows_test.cpp"
        assert test_name == "LocalLanguageSelect_Windows_test"

# pylint: enable=protected-access
