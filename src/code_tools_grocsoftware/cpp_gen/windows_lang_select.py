"""@package langstringautogen
Utility to automatically generate language strings using google translate api
for a language string generation library
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

from code_tools_grocsoftware.base.project_json import ProjectDescription
from code_tools_grocsoftware.base.json_string_class_description import StringClassDescription

from code_tools_grocsoftware.base.param_return_tools import ParamRetDict
from code_tools_grocsoftware.base.doxygen_gen_tools import CDoxyCommentGenerator
from code_tools_grocsoftware.cpp_gen.string_class_tools import BaseCppStringClassGenerator

class WindowsLangSelectFunctionGenerator(BaseCppStringClassGenerator):
    """!
    Methods for Windows language select function generation
    """
    def __init__(self, json_project_data:ProjectDescription):
        """!
        @brief WindowsLangSelectFunctionGenerator constructor
        @param json_project_data {ProjectDescription} JSON project description data
        """
        jsonstringdesc:StringClassDescription = json_project_data.get_string_data()
        base_class_name = jsonstringdesc.get_base_class_name()
        dynamic_compile_switch = jsonstringdesc.get_dynamic_compile_switch()

        super().__init__(json_project_data.get_owner(),
                         json_project_data.get_eula(),
                         base_class_name,
                         dynamic_compile_switch)

        self.select_function_name = "get"+base_class_name+"_Windows"

        desc = "Return value from GetUserDefaultUILanguage() call"
        self.param_dict_list = [ParamRetDict.build_param_dict("lang_id",
                                                              "LANGID",
                                                              desc)]
        self.def_os_str = "(defined(_WIN64) || defined(_WIN32))"
        self.lang_json_data = json_project_data.get_lang_data()
        self.doxy_comment_gen = CDoxyCommentGenerator()

    def get_function_name(self)->str:
        """!
        @brief Return the selection function name
        @return string - Selection function name
        """
        return self.select_function_name

    def get_os_define(self)->str:
        """!
        @brief Return the windows OS define string
        @return string - Windows OS C/CPP compile switch
        """
        return self.def_os_str

    def gen_function_define(self)->list:
        """!
        @brief Get the function declaration string for the given name

        @param name {string}  Function name

        @return string list - Function comment block and declaration start
        """
        desc = "Determine the correct local language class from the input LANGID value"
        code_list = self.define_function_with_decorations(self.select_function_name,
                                                          desc,
                                                          self.param_dict_list,
                                                          self.base_intf_ret_ptr_dict)
        code_list.append("{\n")
        return code_list

    def gen_function_end(self)->str:
        """!
        @brief Get the function declaration string for the given name
        @return string - Function close with comment
        """
        return self.end_function(self.select_function_name)

    def gen_function(self)->list:
        """!
        @brief Generate the function body text
        @return list - Function body string list
        """
        # Generate the #if and includes
        param_name = ParamRetDict.get_param_name(self.param_dict_list[0])
        function_body = []
        function_body.append("#if "+self.def_os_str+"\n")
        function_body.append(self.gen_include("<windows.h>"))
        function_body.append("\n")  # whitespace for readability

        # Generate function doxygen comment and start
        function_body.extend(self.gen_function_define())

        # Start function body generation
        body_indent = "    "
        function_body.append(body_indent+"switch("+param_name+" & 0x0FF)\n")
        function_body.append(body_indent+"{\n")

        # Generate case if chain for each language in the dictionary
        case_indent = body_indent+"".rjust(4, " ")
        case_body_indent = case_indent+"".rjust(4, " ")
        for lang_name in self.lang_json_data.get_language_list():
            lang_codes, _ = self.lang_json_data.get_langid_data(lang_name)
            for langid in lang_codes:
                caseline =  case_indent+"case "
                caseline += hex(langid)
                caseline += ":\n"
                function_body.append(caseline)
            case_assign = case_body_indent+self._gen_make_ptr_return_statement(lang_name)
            function_body.append(case_assign)
            function_body.append(case_body_indent+"break;\n")

        # Add the final default case
        default_lang, _ = self.lang_json_data.get_default_data()
        function_body.append(case_indent+"default:\n")
        function_body.append(case_body_indent+self._gen_make_ptr_return_statement(default_lang))
        function_body.append(body_indent+"}\n")

        # Complete the function
        function_body.append(self.gen_function_end())
        function_body.append("#endif // "+self.def_os_str+"\n")
        return function_body

    def gen_return_function_call(self, indent:int = 4)->list:
        """!
        @brief Generate the call code for the linux dynamic lang selection function
        @param indent {number} Code indentation spaces
        @return list of strings Formatted code lines
        """
        indent_text = "".rjust(indent, " ")
        local_var_name = "lang_id"

        get_param = indent_text
        get_param += ParamRetDict.get_param_type(self.param_dict_list[0])
        get_param += " "
        get_param += local_var_name
        get_param += " = GetUserDefaultUILanguage();\n"

        do_call = indent_text
        do_call += "return "
        do_call += self.select_function_name
        do_call += "("
        do_call += local_var_name
        do_call += ");\n"

        return [get_param, do_call]

    def _gen_unittest_test(self, test_name:str, langid:int,
                           expected_iso:str, get_iso_method:str)->list:
        """!
        @brief Generate single selection function unit test instance

        @param test_name {string} Name of the test
        @param langid {number} LANGID value to test
        @param expected_iso {string} Expected ISO return code for the test variable
        @param get_iso_method {string} Name of the ParserStringListInterface return
                                       ISO code method

        @return list of strings - Output C code
        """
        test_block_name = "WindowsSelectFunction"
        body_indent = "".rjust(4, " ")
        breif_desc = "Test "+self.select_function_name+" "+str(langid)+" selection case"
        test_body = self.doxy_comment_gen.gen_doxy_method_comment(breif_desc, [])

        test_var = "test_var"
        test_var_decl = self.base_intf_ret_ptr_type+" "+test_var
        expected_val = test_var+"->"+get_iso_method+"().c_str()"
        test_body.append("TEST("+test_block_name+", "+test_name+")\n")
        test_body.append("{\n")
        test_body.append(body_indent+"// Generate the test language string object\n")
        nxtline = test_var_decl+" = "+self.select_function_name+"("+str(langid)+");\n"
        test_body.append(body_indent+nxtline)
        test_body.append(body_indent+"EXPECT_STREQ(\""+expected_iso+"\", "+expected_val+");\n")
        test_body.append("}\n")
        return test_body

    def gen_extern_definition(self)->str:
        """!
        @brief Return the external function definition
        @return string - External function definition line
        """
        extern_def = "extern "
        extern_def += self.base_intf_ret_ptr_type
        extern_def += " "
        extern_def += self.select_function_name
        extern_def += "("
        extern_def += ParamRetDict.get_param_type(self.param_dict_list[0])
        extern_def += " "
        extern_def += ParamRetDict.get_param_name(self.param_dict_list[0])
        extern_def += ");\n"
        return extern_def

    def gen_unit_test(self, get_iso_method:str)->list:
        """!
        @brief Generate all unit tests for the selection function
        @param get_iso_method {string} Name of the ParserStringListInterface return ISO code method
        @return list - Unittest text list
        """
        # Generate block start code
        unittest_text = []
        unittest_text.append("#if "+self.def_os_str+"\n")
        unittest_text.append("\n") # white space for readability
        unittest_text.append(self.gen_include("<windows.h>"))
        unittest_text.append(self.gen_extern_definition())
        unittest_text.append("\n") # white space for readability

        # Generate the tests
        for lang_name in self.lang_json_data.get_language_list():
            lang_codes, region_list = self.lang_json_data.get_langid_data(lang_name)
            for lang_id in region_list:
                # Generate test for each region of known language
                test_name = lang_name.capitalize()+"_"+str(lang_id)+"_Selection"
                lang_iso = self.lang_json_data.get_iso_code_data(lang_name)
                test_body = self._gen_unittest_test(test_name,
                                                    lang_id,
                                                    lang_iso,
                                                    get_iso_method)
                test_body.append("\n") # whitespace for readability
                unittest_text.extend(test_body)

            # Generate test for unknown region of known language(s)
            for lang_code in lang_codes:
                lang_iso = self.lang_json_data.get_iso_code_data(lang_name)
                unkn_region_tstname = lang_name.capitalize()
                unkn_region_tstname += "_unknown_region_00"
                unkn_region_tstname += str(lang_code)
                unkn_region_tstname += "_Selection"
                unkn_region_body = self._gen_unittest_test(unkn_region_tstname,
                                                           lang_code,
                                                           lang_iso,
                                                           get_iso_method)
                unkn_region_body.append("\n") # whitespace for readability
                unittest_text.extend(unkn_region_body)

            # Generate test for unknown region of known language(s)
            for lang_code in lang_codes:
                region_iso = self.lang_json_data.get_iso_code_data(lang_name)
                unkn_region_tstname = lang_name.capitalize()
                unkn_region_tstname += "_unknown_region_FF"
                unkn_region_tstname += str(lang_code)
                unkn_region_tstname +="_Selection"
                unkn_region_body = self._gen_unittest_test(unkn_region_tstname,
                                                          0xFF00+lang_code,
                                                          region_iso,
                                                          get_iso_method)
                unkn_region_body.append("\n") # whitespace for readability
                unittest_text.extend(unkn_region_body)

        # Generate test for unknown region of unknown language and expect default
        _, default_iso_code = self.lang_json_data.get_default_data()
        unknown_lang_body = self._gen_unittest_test("UnknownLanguageDefaultSelection",
                                                0,
                                                default_iso_code,
                                                get_iso_method)
        unittest_text.extend(unknown_lang_body)

        # Generate block end code
        unittest_text.append("#endif // "+self.def_os_str+"\n")
        return unittest_text

    def gen_unittest_function_call(self, check_var_name:str, indent:int = 4)->list:
        """!
        @brief Generate the call code for the linux dynamic lang selection unit test
        @param check_var_name {string} Unit test expected variable name
        @param indent {number} Code indentation spaces
        @return list of strings Formatted code lines
        """
        indent_text = "".rjust(indent, " ")
        local_var_name = "lang_id"

        get_param = indent_text
        get_param += ParamRetDict.get_param_type(self.param_dict_list[0])
        get_param += " "
        get_param += local_var_name
        get_param += " = GetUserDefaultUILanguage();\n"

        do_call = indent_text
        do_call += self.base_intf_ret_ptr_type
        do_call += " "
        do_call += check_var_name
        do_call += " = "
        do_call += self.select_function_name
        do_call += "("
        do_call += local_var_name
        do_call += ");\n"

        return [get_param, do_call]

    def get_unittest_extern_include(self)->list:
        """!
        @brief Return windows specific include and external function definition strings
        @return list of strings - windows specific #if, #include, external function and #endif code
        """
        inc_block = []
        inc_block.append("#if "+self.def_os_str+"\n")
        inc_block.append(self.gen_include("<windows.h>"))
        inc_block.append(self.gen_extern_definition())
        inc_block.append("#endif // "+self.def_os_str+"\n")
        return inc_block

    def get_unittest_file_name(self)->tuple:
        """!
        @return tuple(str,str) - Unit test cpp file name, Test name
        """
        return "LocalLanguageSelect_Windows_test.cpp", "LocalLanguageSelect_Windows_test"
