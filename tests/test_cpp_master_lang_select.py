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

from unittest.mock import mock_open, patch

from code_tools_grocsoftware.base.param_return_tools import ParamRetDict
from code_tools_grocsoftware.base.doxygen_gen_tools import CDoxyCommentGenerator
from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList
from code_tools_grocsoftware.cpp_gen.string_class_tools import BaseCppStringClassGenerator
from code_tools_grocsoftware.cpp_gen.static_lang_select import StaticLangSelectFunctionGenerator
from code_tools_grocsoftware.cpp_gen.windows_lang_select import WindowsLangSelectFunctionGenerator
from code_tools_grocsoftware.cpp_gen.linux_lang_select import LinuxLangSelectFunctionGenerator
from code_tools_grocsoftware.cpp_gen.master_lang_select import MasterSelectFunctionGenerator

from tests.dir_init import TESTFILEPATH
testJsonList = os.path.join(TESTFILEPATH,"teststringlanglist.json")

def get_expected_extern(param_dict_list:list, intf_ret_ptr_type:str, select_function_name:str)->str:
    param_prefix = ""
    param_str = ""
    for param_dict in param_dict_list:
        param_type = ParamRetDict.get_param_type(param_dict)
        param_name = ParamRetDict.get_param_name(param_dict)
        param_str += param_prefix
        param_str += param_type
        param_str += " "
        param_str += param_name
        param_prefix = ", "

    expected_str = "extern "+intf_ret_ptr_type+" "+select_function_name+"("+param_str+");\n"
    return expected_str

class TestClass01MasterLangSelect:
    """!
    @brief Unit test for the BaseCppStringClassGenerator class
    """
    def test001_constructor_default(self):
        """!
        @brief Test constructor, default input
        """
        test_obj = MasterSelectFunctionGenerator()

        assert test_obj.base_class_name == "BaseClass"
        assert test_obj.select_base_function_name == "getLocalParserStringListInterface"
        assert test_obj.dynamic_compile_switch == "DYNAMIC_INTERNATIONALIZATION"
        assert test_obj.select_function_name == "BaseClass::getLocalParserStringListInterface"
        assert test_obj.brief_desc == "Determine the OS use OS specific functions to determine " \
                                      "the correct local language based on the OS specific " \
                                      "local language setting and return the correct class object"
        assert isinstance(test_obj.doxy_comment_gen, CDoxyCommentGenerator)

    def test002_constructor_non_default(self):
        """!
        @brief Test constructor, with input
        """
        test_obj = MasterSelectFunctionGenerator("George", "MIT_open", "TestBaseClass", "getLocalLang", "TEST_DYNAM_SWITCH")

        assert test_obj.base_class_name == "TestBaseClass"
        assert test_obj.select_base_function_name == "getLocalLang"
        assert test_obj.dynamic_compile_switch == "TEST_DYNAM_SWITCH"
        assert test_obj.select_function_name == "TestBaseClass::getLocalLang"
        assert test_obj.brief_desc == "Determine the OS use OS specific functions to determine " \
                                      "the correct local language based on the OS specific " \
                                      "local language setting and return the correct class object"
        assert isinstance(test_obj.doxy_comment_gen, CDoxyCommentGenerator)

    def test003_get_function_name(self):
        """!
        @brief Test get_function_name
        """
        test_obj = MasterSelectFunctionGenerator()
        assert test_obj.get_function_name() == "BaseClass::getLocalParserStringListInterface"

    def test004_get_function_desc(self):
        """!
        @brief Test get_function_desc
        """
        test_obj = MasterSelectFunctionGenerator()
        function_name, brief_desc, ret_ptr_dict, parma_list = test_obj.get_function_desc()
        assert function_name == test_obj.select_base_function_name
        assert brief_desc == test_obj.brief_desc
        assert ret_ptr_dict == test_obj.base_intf_ret_ptr_dict
        assert len(parma_list) == 0

    def test005_gen_function_define(self):
        """!
        @brief Test gen_function_define
        """
        cpp_gen = BaseCppStringClassGenerator()
        test_obj = MasterSelectFunctionGenerator(LanguageDescriptionList())
        expected_list = cpp_gen.define_function_with_decorations(test_obj.select_function_name,
                                                             test_obj.brief_desc,
                                                             [],
                                                             test_obj.base_intf_ret_ptr_dict)
        expected_list.append("{\n")

        test_list = test_obj.gen_function_define()
        assert len(test_list) == len(expected_list)
        for index, expected_text in enumerate(expected_list):
            assert test_list[index] == expected_text

    def test006_gen_function_end(self):
        """!
        @brief Test gen_function_end
        """
        test_obj = MasterSelectFunctionGenerator(LanguageDescriptionList())
        assert test_obj.gen_function_end() == "} // end of "+test_obj.select_function_name+"()\n"

    def test007_gen_function(self):
        """!
        @brief Test gen_function
        """
        cpp_gen = BaseCppStringClassGenerator()
        os_lang_selectors = [LinuxLangSelectFunctionGenerator(LanguageDescriptionList()),
                           WindowsLangSelectFunctionGenerator(LanguageDescriptionList())]
        test_obj = MasterSelectFunctionGenerator(os_lang_selectors)

        capture_list = test_obj.gen_function(os_lang_selectors)

        assert len(capture_list) == 18
        expected_list = cpp_gen.define_function_with_decorations(test_obj.select_function_name,
                                                             test_obj.brief_desc,
                                                             [],
                                                             test_obj.base_intf_ret_ptr_dict)
        expected_list.append("{\n")
        for index, expected_text in enumerate(expected_list):
            assert capture_list[index] == expected_text

        list_index = len(expected_list)
        first = True
        for os_selector in os_lang_selectors:
            if first:
                if_line = "#if "
                first = False
            else:
                if_line = "#elif "
            if_line += os_selector.get_os_define()+"\n"

            assert capture_list[list_index] == ""+if_line
            list_index += 1
            os_call_list = os_selector.gen_return_function_call(4)
            for os_index, expected_osCallLine in enumerate(os_call_list):
                assert capture_list[list_index+os_index] == expected_osCallLine

            list_index += len(os_call_list)

        assert capture_list[list_index] == "#else // not defined os\n"
        assert capture_list[list_index+1] == "    #error No language generation method defined for this OS\n"
        assert capture_list[list_index+2] == "#endif // defined os\n"
        assert capture_list[list_index+3] == "} // end of "+test_obj.select_function_name+"()\n"

    def test008_gen_return_function_call(self):
        """!
        @brief Test gen_return_function_call
        """
        test_obj = MasterSelectFunctionGenerator()
        str_list = test_obj.gen_return_function_call()
        assert len(str_list) == 1
        assert str_list[0] == "    return "+test_obj.select_function_name+"();\n"

    def test009_gen_unit_test(self):
        """!
        @brief Test gen_unit_test
        """
        os_lang_selectors = [LinuxLangSelectFunctionGenerator(LanguageDescriptionList()),
                           WindowsLangSelectFunctionGenerator(LanguageDescriptionList())]
        test_obj = MasterSelectFunctionGenerator()
        text_list = test_obj.gen_unit_test("get_iso_code", os_lang_selectors)

        # Test extern definitions
        assert len(text_list) == 31
        index = 0
        for os_selector in os_lang_selectors:
            expected_list = os_selector.get_unittest_extern_include()
            for expected_line in expected_list:
                assert text_list[index] == expected_line
                index += 1

        assert text_list[index] == "\n"

        # Test Doxygen generation
        doxy_gen = CDoxyCommentGenerator()
        doxy_desc = "Test "+test_obj.select_function_name+" selection case"
        doxy_body = doxy_gen.gen_doxy_method_comment(doxy_desc, [])

        assert text_list[index+1] == doxy_body[0]
        assert text_list[index+2] == doxy_body[1]
        assert text_list[index+3] == doxy_body[2]
        assert text_list[index+4] == doxy_body[3]
        index += 5

        text_list[index] == "TEST(SelectFunction, TestLocalSelectMethod)\n"
        text_list[index+1] == "{\n"

        first_os = True
        index += 2
        for os_selector in os_lang_selectors:
            if first_os:
                text_list[index] == "#if "+os_selector.get_os_define()+"\n"
                first_os = False
            else:
                text_list[index] == "#elif "+os_selector.get_os_define()+"\n"
            text_list[index+1] == "    // Get the expected value\n"
            index += 2

            expected_call_list = os_selector.gen_unittest_function_call("var_name", 4)
            for expected_line in expected_call_list:
                text_list[index] == expected_line
                index += 1

        # Add the #else case
        text_list[index] == "#else // not defined os\n"
        text_list[index+1] == "    #error No language generation defined for this OS\n"

        # Complete the function
        text_list[index+2] == "#endif // defined os\n"
        text_list[index+3] == "\n"
        text_list[index+4] == "    // Generate the test language string object\n"
        text_list[index+5] == "    "+test_obj.base_intf_ret_ptr_type+" test_var = "+test_obj.select_function_name+"();\n"
        text_list[index+6] == "    EXPECT_STREQ(var_name->get_iso_code().c_str(), test_var->get_iso_code().c_str());\n"
        text_list[index+7] == "} // end of "+test_obj.select_function_name+"()\n"
