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
from code_tools_grocsoftware.base.doxygen_gen_tools import CDoxyCommentGenerator
from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList
from code_tools_grocsoftware.cpp_gen.string_class_tools import BaseCppStringClassGenerator
from code_tools_grocsoftware.cpp_gen.linux_lang_select import LinuxLangSelectFunctionGenerator

from tests.dir_init import TESTFILEPATH
from tests.support_func import get_expected_extern

test_json_list = os.path.join(TESTFILEPATH,"teststringlanglist.json")

# pylint: disable=protected-access

class TestClass01LinuxLangSelect:
    """!
    @brief Unit test for the BaseCppStringClassGenerator class
    """
    def test001_constructor_default(self):
        """!
        @brief Test constructor, default input
        """
        test_obj = LinuxLangSelectFunctionGenerator(LanguageDescriptionList())

        assert test_obj.base_class_name == "BaseClass"
        assert test_obj.dynamic_compile_switch == "DYNAMIC_INTERNATIONALIZATION"
        assert test_obj.select_function_name == "getBaseClass_Linux"
        assert len(test_obj.param_dict_list) == 1
        desc = "Current LANG value from the program environment"
        assert test_obj.param_dict_list[0] == ParamRetDict.build_param_dict("langId",
                                                                            "const char*",
                                                                            desc)
        assert test_obj.def_os_str == "(defined(__linux__) || defined(__unix__))"
        assert isinstance(test_obj.lang_json_data, LanguageDescriptionList)
        assert isinstance(test_obj.doxy_comment_gen, CDoxyCommentGenerator)

    def test002_constructor_non_default(self):
        """!
        @brief Test constructor, with input
        """
        test_obj = LinuxLangSelectFunctionGenerator(LanguageDescriptionList(),
                                                    "George",
                                                    "MIT_open",
                                                    "TestBaseClass",
                                                    "TEST_DYNAM_SWITCH")

        assert test_obj.base_class_name == "TestBaseClass"
        assert test_obj.dynamic_compile_switch == "TEST_DYNAM_SWITCH"
        assert test_obj.select_function_name == "getTestBaseClass_Linux"
        assert len(test_obj.param_dict_list) == 1
        desc = "Current LANG value from the program environment"
        assert test_obj.param_dict_list[0] == ParamRetDict.build_param_dict("langId",
                                                                            "const char*",
                                                                            desc)
        assert test_obj.def_os_str == "(defined(__linux__) || defined(__unix__))"
        assert isinstance(test_obj.lang_json_data, LanguageDescriptionList)
        assert isinstance(test_obj.doxy_comment_gen, CDoxyCommentGenerator)

    def test003_get_function_name(self):
        """!
        @brief Test get_function_name
        """
        test_obj = LinuxLangSelectFunctionGenerator(LanguageDescriptionList())
        assert test_obj.get_function_name() == "getBaseClass_Linux"

    def test004_get_os_define(self):
        """!
        @brief Test get_os_define
        """
        test_obj = LinuxLangSelectFunctionGenerator(LanguageDescriptionList())
        assert test_obj.get_os_define() == "(defined(__linux__) || defined(__unix__))"

    def test005_gen_function_define(self):
        """!
        @brief Test gen_function_define
        """
        cpp_gen = BaseCppStringClassGenerator()
        test_obj = LinuxLangSelectFunctionGenerator(LanguageDescriptionList())
        desc = "Determine the correct local language class from the input LANG environment setting"
        expected_list = cpp_gen.define_function_with_decorations(test_obj.select_function_name,
                                                             desc,
                                                             test_obj.param_dict_list,
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
        test_obj = LinuxLangSelectFunctionGenerator(LanguageDescriptionList())
        assert test_obj.gen_function_end() == "} // end of "+test_obj.select_function_name+"()\n"

    # pylint: disable=too-many-statements
    def test007_gen_function(self):
        """!
        @brief Test gen_function
        """
        cpp_gen = BaseCppStringClassGenerator()
        lang_list = LanguageDescriptionList(test_json_list)
        test_obj = LinuxLangSelectFunctionGenerator(lang_list)

        capture_list = test_obj.gen_function()

        assert len(capture_list) == 41

        assert capture_list[0] == "#if (defined(__linux__) || defined(__unix__))\n"
        assert capture_list[1] == cpp_gen.gen_include("<cstdlib>")
        assert capture_list[2] == cpp_gen.gen_include("<regex>")
        assert capture_list[3] == "\n"

        desc = "Determine the correct local language class from the input LANG environment setting"
        expected_list = cpp_gen.define_function_with_decorations(test_obj.select_function_name,
                                                             desc,
                                                             test_obj.param_dict_list,
                                                             test_obj.base_intf_ret_ptr_dict)
        expected_list.append("{\n")
        for index, expected_text in enumerate(expected_list):
            assert capture_list[index+4] == expected_text

        param_name = ParamRetDict.get_param_name(test_obj.param_dict_list[0])
        assert capture_list[13] == "    // Check for valid input\n"
        assert capture_list[14] == "    if (nullptr != "+param_name+")\n"
        assert capture_list[15] == "    {\n"
        assert capture_list[16] == "        // Break the string into its components\n"
        assert capture_list[17] == "        std::cmatch search_match;\n"
        assert capture_list[18] == "        std::regex search_regex(\"^([a-z]{2})_([A-Z]{2})" \
                                   "\\\\.(UTF-[0-9]{1,2})\");\n"
        assert capture_list[19] == "        bool matched = std::regex_match("+param_name+", " \
                                   "search_match, search_regex);\n"
        assert capture_list[20] == "\n"
        assert capture_list[21] == "        // Determine the language\n"

        first = True
        for index, lang_name in enumerate(lang_list.get_language_list()):
            lang_code, _ = lang_list.get_language_data(lang_name)
            if first:
                if_line = "if (matched && "
                first = False
            else:
                if_line = "else if (matched && "
            if_line += "(search_match[1].str() == \""
            if_line += lang_code
            if_line += "\"))\n"

            list_offset = 22 + (index * 4)
            assert capture_list[list_offset] == "        "+if_line
            assert capture_list[list_offset+1] == "        {\n"
            assert capture_list[list_offset+2] == "            " \
                                                  +cpp_gen._gen_make_ptr_return_statement(lang_name)
            assert capture_list[list_offset+3] == "        }\n"

        assert capture_list[30] == "        else //unknown language code, use default language\n"
        assert capture_list[31] == "        {\n"
        default_lang, _ = lang_list.get_default_data()
        assert capture_list[32] == "            " \
                                   +cpp_gen._gen_make_ptr_return_statement(default_lang)
        assert capture_list[33] == "        }\n"
        assert capture_list[34] == "    }\n"
        assert capture_list[35] == "    else // null pointer input, use default language\n"
        assert capture_list[36] == "    {\n"
        assert capture_list[37] == "        "+cpp_gen._gen_make_ptr_return_statement(default_lang)
        assert capture_list[38] == "    } // end of if(nullptr != "+param_name+")\n"
        assert capture_list[39] == "} // end of "+test_obj.select_function_name+"()\n"
        assert capture_list[40] == "#endif // "+test_obj.def_os_str+"\n"
    # pylint: enable=too-many-statements


    def test008_gen_return_function_call(self):
        """!
        @brief Test gen_return_function_call
        """
        test_obj = LinuxLangSelectFunctionGenerator(LanguageDescriptionList())
        param_type = ParamRetDict.get_param_type(test_obj.param_dict_list[0])

        str_list = test_obj.gen_return_function_call()
        assert len(str_list) == 2
        assert str_list[0] == "    "+param_type+" langId = getenv(\"LANG\");\n"
        assert str_list[1] == "    return "+test_obj.select_function_name+"(langId);\n"

    def test009_gen_unit_test_test(self):
        """!
        @brief Test _gen_unittest_test
        """
        test_obj = LinuxLangSelectFunctionGenerator(LanguageDescriptionList())

        doxy_gen = CDoxyCommentGenerator()
        doxy_desc = "Test "+test_obj.select_function_name+" env_lang selection case"
        doxy_body = doxy_gen.gen_doxy_method_comment(doxy_desc, [])

        str_list = test_obj._gen_unittest_test("Foo", "env_lang", "en", "get_iso_code")
        assert len(str_list) == 11
        assert str_list[0] == doxy_body[0]
        assert str_list[1] == doxy_body[1]
        assert str_list[2] == doxy_body[2]
        assert str_list[3] == doxy_body[3]

        assert str_list[4] == "TEST(LinuxSelectFunction, Foo)\n"
        assert str_list[5] == "{\n"
        assert str_list[6] == "    // Generate the test language string object\n"
        assert str_list[7] == "    std::string test_lang_code = \"env_lang\";\n"
        assert str_list[8] == "    "+test_obj.base_intf_ret_ptr_type+" test_var = " \
                              +test_obj.select_function_name+"(test_lang_code.c_str());\n"
        assert str_list[9] == "    EXPECT_STREQ(\"en\", test_var->get_iso_code().c_str());\n"
        assert str_list[10] == "}\n"

    def test010_gen_extern_definition(self):
        """!
        @brief Test gen_extern_definition
        """
        test_obj = LinuxLangSelectFunctionGenerator(LanguageDescriptionList())
        expected = get_expected_extern(test_obj.param_dict_list,
                                       test_obj.base_intf_ret_ptr_type,
                                       test_obj.select_function_name)
        assert test_obj.gen_extern_definition() == expected

    def test011_gen_unit_test(self):
        """!
        @brief Test gen_unit_test
        """
        lang_list = LanguageDescriptionList(test_json_list)
        test_obj = LinuxLangSelectFunctionGenerator(lang_list)
        text_list = test_obj.gen_unit_test("get_iso_code")

        # Test starting block
        assert len(text_list) == 425
        assert text_list[0] == "#if "+test_obj.def_os_str+"\n"
        assert text_list[1] == "\n"
        assert text_list[2] == "#include <cstdlib>\n"
        assert text_list[3] == test_obj.gen_extern_definition()
        assert text_list[4] == "\n"

        # Match each test function
        text_index = 5
        for lang_name in lang_list.get_language_list():
            lang_code, region_list = lang_list.get_language_data(lang_name)
            iso_code = lang_list.get_iso_code_data(lang_name)
            for region in region_list:
                linux_env_string = lang_code+"_"+region+".UTF-8"
                test_name = lang_name.capitalize()+"_"+region+"_Selection"
                expected_test_text = test_obj._gen_unittest_test(test_name,
                                                                 linux_env_string,
                                                                 iso_code,
                                                                 "get_iso_code")

                for index, expected_line in enumerate(expected_test_text):
                    assert text_list[text_index+index] == expected_line

                text_index += len(expected_test_text)
                assert text_list[text_index] == "\n"
                text_index += 1

            # Match unknown region test
            unkn_region_tstname =lang_name.capitalize()+"_unknown_region_Selection"
            unkn_region_env = lang_code+"_XX.UTF-8"
            expected_test_text = test_obj._gen_unittest_test(unkn_region_tstname,
                                                             unkn_region_env,
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
                                                        "xx_XX.UTF-8",
                                                        default_iso_code,
                                                        "get_iso_code")
        for index, expected_line in enumerate(unknown_lang_body):
            assert text_list[text_index+index] == expected_line

        text_index += len(expected_test_text)

        # Match end
        assert text_list[424] == "#endif // "+test_obj.def_os_str+"\n"
        assert text_index == 424

    def test012_gen_unit_test_function_call(self):
        """!
        @brief Test gen_unittest_function_call
        """
        test_obj = LinuxLangSelectFunctionGenerator(LanguageDescriptionList())
        text_list = test_obj.gen_unittest_function_call("check_var")

        param_type = ParamRetDict.get_param_type(test_obj.param_dict_list[0])

        assert len(text_list) == 2
        assert text_list[0] == "    "+param_type+" langId = getenv(\"LANG\");\n"
        assert text_list[1] == "    "+test_obj.base_intf_ret_ptr_type+" check_var = " \
                               +test_obj.select_function_name+"(langId);\n"

    def test013_get_unittest_extern_include(self):
        """!
        @brief Test get_unittest_extern_include
        """
        test_obj = LinuxLangSelectFunctionGenerator(LanguageDescriptionList())
        text_list = test_obj.get_unittest_extern_include()

        assert len(text_list) == 4
        assert text_list[0] == "#if "+test_obj.def_os_str+"\n"
        assert text_list[1] == "#include <cstdlib>\n"
        assert text_list[2] == get_expected_extern(test_obj.param_dict_list,
                                                   test_obj.base_intf_ret_ptr_type,
                                                   test_obj.select_function_name)
        assert text_list[3] == "#endif // "+test_obj.def_os_str+"\n"

    def test014_get_unittest_file_name(self):
        """!
        @brief Test get_unittest_file_name
        """
        test_obj = LinuxLangSelectFunctionGenerator(LanguageDescriptionList())
        cpp_name, test_name = test_obj.get_unittest_file_name()
        assert cpp_name == "LocalLanguageSelect_Linux_test.cpp"
        assert test_name == "LocalLanguageSelect_Linux_test"

# pylint: enable=protected-access
