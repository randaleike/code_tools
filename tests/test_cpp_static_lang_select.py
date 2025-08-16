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

from code_tools_grocsoftware.base.eula import EulaText
from code_tools_grocsoftware.base.doxygen_gen_tools import CDoxyCommentGenerator
from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList
from code_tools_grocsoftware.cpp_gen.string_class_tools import BaseCppStringClassGenerator
from code_tools_grocsoftware.cpp_gen.static_lang_select import StaticLangSelectFunctionGenerator

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

class TestClass01StaticLangSelect:
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
        mock_project_data.get_version = mocker.Mock(return_value = "v1.0.0")

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
        mock_project_data.get_version = mocker.Mock(return_value = "v1.0.0")

        mock_string_data.get_base_class_name = mocker.Mock(return_value="BaseClass")
        mock_string_data.get_dynamic_compile_switch = mocker.Mock(return_value="DYNAMIC_INTERNATIONALIZATION")

        return mock_project_data

    def test001_constructor_default(self, mocker):
        """!
        @brief Test constructor, default input
        """
        test_obj = StaticLangSelectFunctionGenerator(self.default_setup(mocker))

        assert test_obj.base_class_name == "BaseClass"
        assert test_obj.dynamic_compile_switch == "DYNAMIC_INTERNATIONALIZATION"
        assert test_obj.select_function_name == "getBaseClass_Static"
        assert test_obj.def_static_string == "!defined(DYNAMIC_INTERNATIONALIZATION)"
        assert isinstance(test_obj.lang_json_data, LanguageDescriptionList)
        assert isinstance(test_obj.doxy_comment_gen, CDoxyCommentGenerator)

    def test002_constructor_non_default(self, mocker):
        """!
        @brief Test constructor, with input
        """
        mock_project_data = mocker.Mock()
        mock_string_data = mocker.Mock()
        mock_project_data.get_lang_data = mocker.Mock(return_value=LanguageDescriptionList())
        mock_project_data.get_string_data = mocker.Mock(return_value=mock_string_data)
        mock_project_data.get_owner = mocker.Mock(return_value="George")
        mock_project_data.get_eula = mocker.Mock(return_value=DummyEulaText())
        mock_project_data.get_version = mocker.Mock(return_value = "v1.0.0")

        mock_string_data.get_base_class_name = mocker.Mock(return_value="TestBaseClass")
        mock_string_data.get_dynamic_compile_switch = mocker.Mock(return_value="TEST_DYNAM_SWITCH")

        test_obj = StaticLangSelectFunctionGenerator(mock_project_data)

        assert test_obj.base_class_name == "TestBaseClass"
        assert test_obj.dynamic_compile_switch == "TEST_DYNAM_SWITCH"
        assert test_obj.select_function_name == "getTestBaseClass_Static"
        assert test_obj.def_static_string == "!defined(TEST_DYNAM_SWITCH)"
        assert isinstance(test_obj.lang_json_data, LanguageDescriptionList)
        assert isinstance(test_obj.doxy_comment_gen, CDoxyCommentGenerator)

    def test003_get_function_name(self, mocker):
        """!
        @brief Test get_function_name
        """
        test_obj = StaticLangSelectFunctionGenerator(self.default_setup(mocker))
        assert test_obj.get_function_name() == "getBaseClass_Static"

    def test004_get_os_define(self, mocker):
        """!
        @brief Test get_os_define
        """
        test_obj = StaticLangSelectFunctionGenerator(self.default_setup(mocker))
        assert test_obj.get_os_define() == "!defined(DYNAMIC_INTERNATIONALIZATION)"

    def test005_get_os_dynamic_define(self, mocker):
        """!
        @brief Test get_os_dynamic_define
        """
        test_obj = StaticLangSelectFunctionGenerator(self.default_setup(mocker))
        assert test_obj.get_os_dynamic_define() == "!defined(DYNAMIC_INTERNATIONALIZATION)"

    def test006_gen_function_define(self, mocker):
        """!
        @brief Test gen_function_define
        """
        cpp_gen = BaseCppStringClassGenerator()
        test_obj = StaticLangSelectFunctionGenerator(self.default_setup(mocker))
        desc = "Determine the correct local language class from the compile switch setting"
        expected_list = cpp_gen.define_function_with_decorations(test_obj.select_function_name,
                                                                 desc,
                                                                 [],
                                                                 test_obj.base_intf_ret_ptr_dict)
        expected_list.append("{\n")

        test_list = test_obj.gen_function_define()
        assert len(test_list) == len(expected_list)
        for index, expected_text in enumerate(expected_list):
            assert test_list[index] == expected_text

    def test007_gen_function_end(self, mocker):
        """!
        @brief Test gen_function_end
        """
        test_obj = StaticLangSelectFunctionGenerator(self.default_setup(mocker))
        assert test_obj.gen_function_end() == "} // end of "+test_obj.select_function_name+"()\n"

    def test008_gen_function(self, mocker):
        """!
        @brief Test gen_function
        """
        cpp_gen = BaseCppStringClassGenerator()
        lang_list = LanguageDescriptionList(test_json_list)
        test_obj = StaticLangSelectFunctionGenerator(self.langfile_setup(mocker, lang_list))

        capture_list = test_obj.gen_function()

        assert len(capture_list) == 17
        assert capture_list[0] == "#if !defined(DYNAMIC_INTERNATIONALIZATION)\n"

        desc = "Determine the correct local language class from the compile switch setting"
        expected_list = cpp_gen.define_function_with_decorations(test_obj.select_function_name,
                                                                 desc,
                                                                 [],
                                                                 test_obj.base_intf_ret_ptr_dict)
        expected_list.append("{\n")
        for index, expected_text in enumerate(expected_list):
            assert capture_list[index+1] == expected_text

        list_index = len(expected_list) + 1
        first = True
        for index, lang_name in enumerate(lang_list.get_language_list()):
            switch = lang_list.get_compile_switch_data(lang_name)
            if first:
                if_line = "#if "
                first = False
            else:
                if_line = "#elif "
            if_line += "defined("+switch+")\n"

            assert capture_list[list_index] == "  "+if_line
            retstr = cpp_gen._gen_make_ptr_return_statement(lang_name)
            assert capture_list[list_index+1] == "    "+retstr
            list_index += 2

        assert capture_list[list_index] == "  #else //undefined language compile switch, " \
                                           "use default\n"
        assert capture_list[list_index+1] == "    #error one of the language compile switches " \
                                             "must be defined\n"
        assert capture_list[list_index+2] == "  #endif //end of language #if/#elifcompile " \
                                             "switch chain\n"
        assert capture_list[list_index+3] == "} // end of "+test_obj.select_function_name+"()\n"
        assert capture_list[list_index+4] == "#endif // "+test_obj.def_static_string+"\n"

    def test009_gen_return_function_call(self, mocker):
        """!
        @brief Test gen_return_function_call
        """
        test_obj = StaticLangSelectFunctionGenerator(self.default_setup(mocker))
        str_list = test_obj.gen_return_function_call()
        assert len(str_list) == 1
        assert str_list[0] == "    return "+test_obj.select_function_name+"();\n"

    def test010_gen_extern_definition(self, mocker):
        """!
        @brief Test gen_extern_definition
        """
        test_obj = StaticLangSelectFunctionGenerator(self.default_setup(mocker))
        assert test_obj.gen_extern_definition() == "extern "+test_obj.base_intf_ret_ptr_type \
                                                   +" "+test_obj.select_function_name+"();\n"

    def test011_gen_unit_test(self, mocker):
        """!
        @brief Test gen_unit_test
        """
        lang_list = LanguageDescriptionList(test_json_list)
        test_obj = StaticLangSelectFunctionGenerator(self.langfile_setup(mocker, lang_list))
        text_list = test_obj.gen_unit_test("get_iso_code")

        # Test starting block
        assert len(text_list) == 26
        assert text_list[0] == "#if "+test_obj.def_static_string+"\n"
        assert text_list[1] == test_obj.gen_extern_definition()
        assert text_list[2] == "\n"

        doxy_gen = CDoxyCommentGenerator()
        doxy_desc = "Test "+test_obj.select_function_name+" selection case"
        doxy_body = doxy_gen.gen_doxy_method_comment(doxy_desc, [])

        assert text_list[3] == doxy_body[0]
        assert text_list[4] == doxy_body[1]
        assert text_list[5] == doxy_body[2]
        assert text_list[6] == doxy_body[3]

        # Match each test function
        text_index = 7
        for lang_name in lang_list.get_language_list():
            iso_code = lang_list.get_iso_code_data(lang_name)
            switch = lang_list.get_compile_switch_data(lang_name)

            # Match language
            expected_body = ["#if defined("+switch+")\n"]
            expected_body.append("TEST(StaticSelectFunction"+lang_name.capitalize() \
                                 +", CompileSwitchedValue)\n")
            expected_body.append("{\n")
            expected_body.append("    // Generate the test language string object\n")
            expected_body.append("    "+test_obj.base_intf_ret_ptr_type+" test_var = " \
                                 + test_obj.select_function_name+"();\n")
            expected_body.append("    EXPECT_STREQ(\""+iso_code+"\", " \
                                 "test_var->get_iso_code().c_str());\n")

            # Complete the function
            expected_body.append("}\n")
            expected_body.append("#endif //end of #if defined("+switch+")\n")
            expected_body.append("\n") # whitespace for readability

            assert text_list[text_index+0] == expected_body[0]
            assert text_list[text_index+1] == expected_body[1]
            assert text_list[text_index+2] == expected_body[2]
            assert text_list[text_index+3] == expected_body[3]
            assert text_list[text_index+4] == expected_body[4]
            assert text_list[text_index+5] == expected_body[5]
            assert text_list[text_index+6] == expected_body[6]
            assert text_list[text_index+7] == expected_body[7]
            assert text_list[text_index+8] == expected_body[8]
            text_index += 9

        # Match end
        assert text_list[text_index] == "#endif // "+test_obj.def_static_string+"\n"
        assert text_index == 25

    def test012_gen_unit_test_function_call(self, mocker):
        """!
        @brief Test gen_unittest_function_call
        """
        test_obj = StaticLangSelectFunctionGenerator(self.default_setup(mocker))
        text_list = test_obj.gen_unittest_function_call("check_var")

        assert len(text_list) == 1
        assert text_list[0] == "    "+test_obj.base_intf_ret_ptr_type+ \
                               " check_var = "+test_obj.select_function_name+"();\n"

    def test013_get_unittest_extern_include(self, mocker):
        """!
        @brief Test get_unittest_extern_include
        """
        test_obj = StaticLangSelectFunctionGenerator(self.default_setup(mocker))
        text_list = test_obj.get_unittest_extern_include()

        assert len(text_list) == 3
        assert text_list[0] == "#if "+test_obj.def_static_string+"\n"
        assert text_list[1] == get_expected_extern([],
                                                   test_obj.base_intf_ret_ptr_type,
                                                   test_obj.select_function_name)
        assert text_list[2] == "#endif // "+test_obj.def_static_string+"\n"

    def test014_get_unittest_file_name(self, mocker):
        """!
        @brief Test get_unittest_file_name
        """
        test_obj = StaticLangSelectFunctionGenerator(self.default_setup(mocker))
        cpp_name = test_obj.get_unittest_file_name()
        assert cpp_name == "LocalLanguageSelect_Static_test.cpp"

# pylint: enable=protected-access
