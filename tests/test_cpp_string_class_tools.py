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

from code_tools_grocsoftware.base.param_return_tools import ParamRetDict
from code_tools_grocsoftware.base.eula import EulaText
from code_tools_grocsoftware.cpp_gen.file_gen_base import GenerateCppFileHelper
from code_tools_grocsoftware.cpp_gen.string_class_tools import BaseCppStringClassGenerator

class TestClass01StringClass_tools:
    """!
    @brief Unit test for the BaseCppStringClassGenerator class
    """
    def test001_constructor_default(self):
        """!
        @brief Test constructor, default input
        """
        test_obj = BaseCppStringClassGenerator()

        assert test_obj.owner == "BaseCppStringClassGenerator"
        assert test_obj.base_class_name == "BaseClass"
        assert test_obj.dynamic_compile_switch == "DYNAMIC_INTERNATIONALIZATION"
        assert test_obj.if_dynamic_defined == "defined(DYNAMIC_INTERNATIONALIZATION)"
        assert test_obj.base_intf_ret_ptr_type == "std::shared_ptr<BaseClass>"
        assert test_obj.base_intf_ret_ptr_dict == ParamRetDict.build_return_dict('sharedptr',
                                                                                      "Shared pointer to BaseClass<lang> based on OS local language")
        assert test_obj.type_xlation_dict['LANGID'] == "LANGID"
        assert test_obj.type_xlation_dict['sharedptr'] == "std::shared_ptr<BaseClass>"
        assert test_obj.type_xlation_dict['strstream'] == "std::stringstream"

        assert test_obj.version_major == 0
        assert test_obj.version_minor == 4
        assert test_obj.version_patch == 1

        assert test_obj.auto_tool_name == test_obj.__class__.__name__+"V0.4.1"
        assert test_obj.group_name == "LocalLanguageSelection"

        assert test_obj.group_desc == "Local language detection and selection utility"
        assert test_obj.declare_indent == 8
        assert test_obj.function_indent == 4

    """!
    @brief Unit test for the BaseCppStringClassGenerator class
    """
    def test002_constructor_basic(self):
        """!
        @brief Test constructor
        """
        test_obj = BaseCppStringClassGenerator("me", "MIT_open", "TestBaseClass", "BASE_DYNAMIC_SWITCH")

        assert test_obj.owner == "me"
        assert test_obj.base_class_name == "TestBaseClass"
        assert test_obj.dynamic_compile_switch == "BASE_DYNAMIC_SWITCH"
        assert test_obj.if_dynamic_defined == "defined(BASE_DYNAMIC_SWITCH)"
        assert test_obj.base_intf_ret_ptr_type == "std::shared_ptr<TestBaseClass>"
        assert test_obj.base_intf_ret_ptr_dict == ParamRetDict.build_return_dict('sharedptr',
                                                                                      "Shared pointer to TestBaseClass<lang> based on OS local language")
        assert test_obj.type_xlation_dict['LANGID'] == "LANGID"
        assert test_obj.type_xlation_dict['sharedptr'] == "std::shared_ptr<TestBaseClass>"
        assert test_obj.type_xlation_dict['strstream'] == "std::stringstream"

        assert test_obj.version_major == 0
        assert test_obj.version_minor == 4
        assert test_obj.version_patch == 1

        assert test_obj.auto_tool_name == test_obj.__class__.__name__+"V0.4.1"
        assert test_obj.group_name == "LocalLanguageSelection"

        assert test_obj.group_desc == "Local language detection and selection utility"
        assert test_obj.declare_indent == 8
        assert test_obj.function_indent == 4

    def test003_get_types(self):
        """!
        @brief Test _get_string_type, _get_char_type and _get_str_stream_type
        """
        test_obj = BaseCppStringClassGenerator()
        assert test_obj._get_string_type() == test_obj.type_xlation_dict['string']
        assert test_obj._get_char_type() == test_obj.type_xlation_dict['char']
        assert test_obj._get_str_stream_type() == test_obj.type_xlation_dict['strstream']

    def test004_gen_make_ptr_return_statement(self):
        """!
        @brief Test _gen_make_ptr_return_statement
        """
        test_obj = BaseCppStringClassGenerator()
        assert test_obj._gen_make_ptr_return_statement() == "return std::make_shared<BaseClass>();\n"
        assert test_obj._gen_make_ptr_return_statement("oompa") == "return std::make_shared<BaseClassOompa>();\n"

    def test005_get_version(self):
        """!
        @brief Test _get_version
        """
        test_obj = BaseCppStringClassGenerator()
        assert test_obj._get_version() == "V"+str(test_obj.version_major)+"."+str(test_obj.version_minor)+"."+str(test_obj.version_patch)

    def test006_generate_file_header(self):
        """!
        @brief Test _generate_file_header
        """
        test_obj = BaseCppStringClassGenerator("Tester", "MIT_open")
        str_list = test_obj._generate_file_header()
        eula_data = EulaText('MIT_open')
        eula_name = eula_data.format_eula_name()
        eula_text = eula_data.format_eula_text()
        assert len(str_list) == 27
        assert str_list[0] == "/*------------------------------------------------------------------------------\n"
        assert str_list[1] == "* Copyright (c) 2025 Tester\n"
        assert str_list[2] == "* \n"
        assert str_list[3] == "* "+eula_name+"\n"
        assert str_list[4] == "* \n"

        for index, eula_line in enumerate(eula_text):
            assert str_list[index+5] == "* "+eula_line+"\n"

        assert str_list[23] == "* \n"
        assert str_list[24] == "* This file was autogenerated by "+test_obj.auto_tool_name+" do not edit\n"
        assert str_list[25] == "* \n"
        assert str_list[26] == "* ----------------------------------------------------------------------------*/\n"

    def test007_generate_h_file_name(self):
        """!
        @brief Test _generateHFileName
        """
        test_obj = BaseCppStringClassGenerator()
        assert test_obj._generateHFileName() == test_obj.base_class_name+".h"
        assert test_obj._generateHFileName("klingon") == test_obj.base_class_name+"klingon".capitalize()+".h"

    def test008_generate_cpp_file_name(self):
        """!
        @brief Test _generate_cpp_file_name
        """
        test_obj = BaseCppStringClassGenerator()
        assert test_obj._generate_cpp_file_name() == test_obj.base_class_name+".cpp"
        assert test_obj._generate_cpp_file_name("romulan") == test_obj.base_class_name+"romulan".capitalize()+".cpp"

    def test009_generate_unittest_file_name(self):
        """!
        @brief Test _generate_unittest_file_name
        """
        test_obj = BaseCppStringClassGenerator()
        assert test_obj._generate_unittest_file_name() == test_obj.base_class_name+"_test.cpp"
        assert test_obj._generate_unittest_file_name("gorn") == test_obj.base_class_name+"gorn".capitalize()+"_test.cpp"

    def test010_generate_unittest_target_name(self):
        """!
        @brief Test _generate_unittest_target_name
        """
        test_obj = BaseCppStringClassGenerator()
        assert test_obj._generate_unittest_target_name() == test_obj.base_class_name+"_test"
        assert test_obj._generate_unittest_target_name("telerite") == test_obj.base_class_name+"telerite".capitalize()+"_test"

    def test011_generate_mock_h_file_name(self):
        """!
        @brief Test _generate_mockHFileName
        """
        test_obj = BaseCppStringClassGenerator()
        assert test_obj._generate_mockHFileName() == "mock_"+test_obj.base_class_name+".h"
        assert test_obj._generate_mockHFileName("latin") == "mock_"+test_obj.base_class_name+"latin".capitalize()+".h"

    def test012_generate_mock_cpp_file_name(self):
        """!
        @brief Test _generate_mockCppFileName
        """
        test_obj = BaseCppStringClassGenerator()
        assert test_obj._generate_mockCppFileName() == "mock_"+test_obj.base_class_name+".cpp"
        assert test_obj._generate_mockCppFileName("latin") == "mock_"+test_obj.base_class_name+"latin".capitalize()+".cpp"

    def test013_write_method_min(self):
        """!
        @brief Test _write_method, minimum
        """
        test_obj = BaseCppStringClassGenerator()
        c_gen = GenerateCppFileHelper()
        return_dict = ParamRetDict.build_return_dict('string', "Return description")
        str_list = test_obj._write_method("TestMethod", "Test method description", [], return_dict, None, None)
        expected_list = c_gen._declare_function_with_decorations("TestMethod",
                                                            "Test method description",
                                                            [],
                                                            return_dict,
                                                            test_obj.declare_indent,
                                                            True,
                                                            None,
                                                            "const")
        assert len(str_list) == len(expected_list)
        for index, expected_str in enumerate(expected_list):
            assert str_list[index] == expected_str

    def test014_write_method_min_with_doxygen(self):
        """!
        @brief Test _write_method, minimum with doxygen
        """
        test_obj = BaseCppStringClassGenerator()
        c_gen = GenerateCppFileHelper()
        return_dict = ParamRetDict.build_return_dict('string', "Return description")
        str_list = test_obj._write_method("TestMethod", "Test method description", [], return_dict, None, None, False)
        expected_list = c_gen._declare_function_with_decorations("TestMethod",
                                                            "Test method description",
                                                            [],
                                                            return_dict,
                                                            test_obj.declare_indent,
                                                            False,
                                                            None,
                                                            "const")
        assert len(str_list) == len(expected_list)
        for index, expected_str in enumerate(expected_list):
            assert str_list[index] == expected_str

    def test015_write_method_with_prefix(self):
        """!
        @brief Test _write_method, with prefix
        """
        test_obj = BaseCppStringClassGenerator()
        c_gen = GenerateCppFileHelper()
        return_dict = ParamRetDict.build_return_dict('string', "Return description")
        str_list = test_obj._write_method("TestMethod", "Test method description", [], return_dict, "virtual", None)
        expected_list = c_gen._declare_function_with_decorations("TestMethod",
                                                            "Test method description",
                                                            [],
                                                            return_dict,
                                                            test_obj.declare_indent,
                                                            True,
                                                            "virtual",
                                                            "const")
        assert len(str_list) == len(expected_list)
        for index, expected_str in enumerate(expected_list):
            assert str_list[index] == expected_str

    def test016_write_method_with_postfix(self):
        """!
        @brief Test _write_method, with postfix
        """
        test_obj = BaseCppStringClassGenerator()
        c_gen = GenerateCppFileHelper()
        return_dict = ParamRetDict.build_return_dict('string', "Return description")
        param_dict = ParamRetDict.build_param_dict("foo", "integer", "Integer description")
        str_list = test_obj._write_method("TestMethod", "Test method description", [param_dict], return_dict, "virtual", "final")
        expected_list = c_gen._declare_function_with_decorations("TestMethod",
                                                            "Test method description",
                                                            [param_dict],
                                                            return_dict,
                                                            test_obj.declare_indent,
                                                            True,
                                                            "virtual",
                                                            "final")
        assert len(str_list) == len(expected_list)
        for index, expected_str in enumerate(expected_list):
            assert str_list[index] == expected_str

    def test017_write_method_with_postfix_only(self):
        """!
        @brief Test _write_method, with postfix
        """
        test_obj = BaseCppStringClassGenerator()
        c_gen = GenerateCppFileHelper()
        return_dict = ParamRetDict.build_return_dict('string', "Return description")
        param_list = []
        str_list = test_obj._write_method("TestMethod", "Test method description", param_list, return_dict, "virtual", "final")
        expected_list = c_gen._declare_function_with_decorations("TestMethod",
                                                            "Test method description",
                                                            param_list,
                                                            return_dict,
                                                            test_obj.declare_indent,
                                                            True,
                                                            "virtual",
                                                            "const final")
        assert len(str_list) == len(expected_list)
        for index, expected_str in enumerate(expected_list):
            assert str_list[index] == expected_str

    def test018_write_mock_method_min(self):
        """!
        @brief Test _write_method, minimum
        """
        test_obj = BaseCppStringClassGenerator()

        c_gen = GenerateCppFileHelper()
        return_dict = ParamRetDict.build_return_dict('string', "Return description")
        expected_decl = c_gen._declare_type(ParamRetDict.get_return_type(return_dict), ParamRetDict.get_param_type_mod(return_dict))
        expected_parms = c_gen._gen_function_params([])
        expected_mock = "        MOCK_METHOD("+expected_decl+", TestMethod, "+expected_parms+", (const));\n"

        str_list = test_obj._write_mock_method("TestMethod", [], return_dict, None)
        assert len(str_list) == 1
        assert str_list[0] == expected_mock

    def test019_write_mock_method_with_param(self):
        """!
        @brief Test _write_method, with param
        """
        test_obj = BaseCppStringClassGenerator()

        c_gen = GenerateCppFileHelper()
        return_dict = ParamRetDict.build_return_dict('string', "Return description")
        param_list = [ParamRetDict.build_param_dict("foo", "integer", "Integer description")]
        expected_decl = c_gen._declare_type(ParamRetDict.get_return_type(return_dict), ParamRetDict.get_param_type_mod(return_dict))
        expected_parms = c_gen._gen_function_params(param_list)
        expected_mock = "        MOCK_METHOD("+expected_decl+", TestMethod, "+expected_parms+");\n"

        str_list = test_obj._write_mock_method("TestMethod", param_list, return_dict, None)
        assert len(str_list) == 1
        assert str_list[0] == expected_mock

    def test020_write_mock_method_with_postfix(self):
        """!
        @brief Test _write_method, with postfix
        """
        test_obj = BaseCppStringClassGenerator()

        c_gen = GenerateCppFileHelper()
        return_dict = ParamRetDict.build_return_dict('string', "Return description")
        param_list = []
        expected_decl = c_gen._declare_type(ParamRetDict.get_return_type(return_dict), ParamRetDict.get_param_type_mod(return_dict))
        expected_parms = c_gen._gen_function_params(param_list)
        expected_mock = "        MOCK_METHOD("+expected_decl+", TestMethod, "+expected_parms+", (const, override));\n"

        str_list = test_obj._write_mock_method("TestMethod", param_list, return_dict, "override")
        assert len(str_list) == 1
        assert str_list[0] == expected_mock

    def test021_write_mock_method_with_param_postfix(self):
        """!
        @brief Test _write_method, with param and postfix
        """
        test_obj = BaseCppStringClassGenerator()

        c_gen = GenerateCppFileHelper()
        return_dict = ParamRetDict.build_return_dict('string', "Return description")
        param_list = [ParamRetDict.build_param_dict("foo", "integer", "Integer description")]
        expected_decl = c_gen._declare_type(ParamRetDict.get_return_type(return_dict), ParamRetDict.get_param_type_mod(return_dict))
        expected_parms = c_gen._gen_function_params(param_list)
        expected_mock = "        MOCK_METHOD("+expected_decl+", TestMethod, "+expected_parms+", (override));\n"

        str_list = test_obj._write_mock_method("TestMethod", param_list, return_dict, "override")
        assert len(str_list) == 1
        assert str_list[0] == expected_mock
