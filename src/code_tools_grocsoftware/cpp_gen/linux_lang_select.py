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

from code_tools_grocsoftware.base.param_return_tools import ParamRetDict
from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList
from code_tools_grocsoftware.base.doxygen_gen_tools import CDoxyCommentGenerator
from code_tools_grocsoftware.cpp_gen.string_class_tools import BaseCppStringClassGenerator

class LinuxLangSelectFunctionGenerator(BaseCppStringClassGenerator):
    """!
    Methods for Linux language select function generation
    """
    def __init__(self, json_lang_data:LanguageDescriptionList, owner:str = None, eula_name:str = None, base_class_name:str = "BaseClass",
                 dynamic_compile_switch:str = "DYNAMIC_INTERNATIONALIZATION"):
        """!
        @brief LinuxLangSelectFunctionGenerator constructor
        @param json_lang_data {string} JSON language description list file name
        @param owner {string} Owner name to use in the copyright header message or None to use tool name
        @param eula_name {string} Name of the EULA to pass down to the BaseCppStringClassGenerator parent
        @param base_class_name {string} Name of the base class for name generation
        @param dynnamic_compile_switch {string} Dynamic compile switch for #if generation
        """
        super().__init__(owner, eula_name, base_class_name, dynamic_compile_switch)
        ## Name of the linux language class dynamic allocation function
        self.select_function_name = "get"+base_class_name+"_Linux"

        ## Dynamic allocation function input parameter dictionary list
        self.param_dict_list = [ParamRetDict.build_param_dict("langId", "const char*", "Current LANG value from the program environment")]

        ## Linux OS definition compile switch
        self.def_osString = "(defined(__linux__) || defined(__unix__))"

        ## Json language data list object
        self.lang_json_data = json_lang_data

        ## CPP Doxygen comment generator
        self.doxy_comment_gen = CDoxyCommentGenerator()

    def get_function_name(self)->str:
        return self.select_function_name

    def get_os_define(self)->str:
        return self.def_osString

    def gen_function_define(self)->list:
        """!
        @brief Get the function declaration string for the given name
        @return string list - Function comment block and declaration start
        """
        code_list = self._define_function_with_decorations(self.select_function_name,
                                                       "Determine the correct local language class from the input LANG environment setting",
                                                       self.param_dict_list,
                                                       self.base_intf_ret_ptr_dict)
        code_list.append("{\n")
        return code_list

    def gen_function_end(self)->str:
        """!
        @brief Get the function declaration string for the given name
        @return string - Function close with comment
        """
        return self._end_function(self.select_function_name)

    def gen_function(self)->list:
        """!
        @brief Generate the function body text
        @return list - Function body string list
        """
        # Generate the #if and includes
        function_body = []
        function_body.append("#if "+self.def_osString+"\n")
        function_body.append(self._gen_include("<cstdlib>"))
        function_body.append(self._gen_include("<regex>"))
        function_body.append("\n")  # whitespace for readability

        # Generate function doxygen comment and start
        function_body.extend(self.gen_function_define())

        # Start function body generation
        param_name = ParamRetDict.get_param_name(self.param_dict_list[0])
        body_indent = "".rjust(self.level_tab_size, " ")
        function_body.append(body_indent+"// Check for valid input\n")
        function_body.append(body_indent+"if (nullptr != "+param_name+")\n")
        function_body.append(body_indent+"{\n")

        # Generate if/else if chain for each language in the dictionary
        if1BodyIndent = body_indent+"".rjust(self.level_tab_size, " ")
        function_body.append(if1BodyIndent+"// Break the string into its components\n")
        function_body.append(if1BodyIndent+"std::cmatch search_match;\n")
        function_body.append(if1BodyIndent+"std::regex search_regex(\"^([a-z]{2})_([A-Z]{2})\\\\.(UTF-[0-9]{1,2})\");\n")
        function_body.append(if1BodyIndent+"bool matched = std::regex_match("+param_name+", search_match, search_regex);\n")
        function_body.append("\n")  # whitespace for readability
        function_body.append(if1BodyIndent+"// Determine the language\n")

        if2BodyIndent = if1BodyIndent+"".rjust(self.level_tab_size, " ")
        first_check = True
        for lang_name in self.lang_json_data.get_language_list():
            lang_code, region_list = self.lang_json_data.get_language_lang_data(lang_name)
            ifline = ""
            if first_check:
                ifline += "if (matched && "
                first_check = False
            else:
                ifline += "else if (matched && "

            ifline += "(search_match[1].str() == \""
            ifline += lang_code
            ifline += "\"))\n"

            function_body.append(if1BodyIndent+ifline)
            function_body.append(if1BodyIndent+"{\n")
            function_body.append(if2BodyIndent+self._gen_make_ptr_return_statement(lang_name))
            function_body.append(if1BodyIndent+"}\n")

        # Add the final else (unknown language) case
        default_lang, default_iso_code = self.lang_json_data.get_default_data()
        function_body.append(if1BodyIndent+"else //unknown language code, use default language\n")
        function_body.append(if1BodyIndent+"{\n")
        function_body.append(if2BodyIndent+self._gen_make_ptr_return_statement(default_lang))
        function_body.append(if1BodyIndent+"}\n")

        # Add the else if nullptr case
        function_body.append(body_indent+"}\n")
        function_body.append(body_indent+"else // null pointer input, use default language\n")
        function_body.append(body_indent+"{\n")
        function_body.append(if1BodyIndent+self._gen_make_ptr_return_statement(default_lang))
        function_body.append(body_indent+"} // end of if(nullptr != "+param_name+")\n")

        # Complete the function
        function_body.append(self.gen_function_end())
        function_body.append("#endif // "+self.def_osString+"\n")
        return function_body

    def gen_return_function_call(self, indent:int = 4)->list:
        """!
        @brief Generate the call code for the linux dynamic lang selection function
        @param indent {number} Code indentation spaces
        @return list of strings Formatted code lines
        """
        indent_text = "".rjust(indent, " ")
        local_var_name = "langId"

        get_param =  indent_text
        get_param += ParamRetDict.get_param_type(self.param_dict_list[0])
        get_param += " "
        get_param += local_var_name
        get_param += " = getenv(\"LANG\");\n"

        do_call = indent_text
        do_call += "return "
        do_call += self.select_function_name
        do_call += "("
        do_call += local_var_name
        do_call += ");\n"

        return [get_param, do_call]

    def _gen_unittest_test(self, test_name:str, linux_env_string:str, expected_iso:str, get_iso_method:str)->list:
        """!
        @brief Generate single selection function unit test instance

        @param test_name {string} Name of the test
        @param linux_env_string {string} Environment string value to send to the select function
        @param expected_iso {string} Expected ISO return code for the test variable
        @param get_iso_method {string} Name of the ParserStringListInterface return ISO code method

        @return list of strings - Output C code
        """
        test_block_name = "LinuxSelectFunction"
        body_indent = "".rjust(self.level_tab_size, " ")
        breif_desc = "Test "+self.select_function_name+" "+linux_env_string+" selection case"
        test_body = self.doxy_comment_gen.gen_doxy_method_comment(breif_desc, [])

        test_var = "test_var"
        test_varDecl = self.base_intf_ret_ptr_type+" "+test_var
        test_varTest = test_var+"->"+get_iso_method+"().c_str()"
        test_body.append("TEST("+test_block_name+", "+test_name+")\n")
        test_body.append("{\n")
        test_body.append(body_indent+"// Generate the test language string object\n")
        test_body.append(body_indent+"std::string test_lang_code = \""+linux_env_string+"\";\n")
        test_body.append(body_indent+test_varDecl+" = "+self.select_function_name+"(test_lang_code.c_str());\n")
        test_body.append(body_indent+"EXPECT_STREQ(\""+expected_iso+"\", "+test_varTest+");\n")
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
        unittest_block = ["#if "+self.def_osString+"\n"]
        unittest_block.append("\n") # white space for readability
        unittest_block.append(self._gen_include("<cstdlib>"))
        unittest_block.append(self.gen_extern_definition())
        unittest_block.append("\n") # white space for readability

        # Generate the tests
        for lang_name in self.lang_json_data.get_language_list():
            lang_code, region_list = self.lang_json_data.get_language_lang_data(lang_name)
            iso_code = self.lang_json_data.get_language_iso_code_data(lang_name)

            for region in region_list:
                # Generate test for each region of known language
                linux_env_string = lang_code+"_"+region+".UTF-8"
                test_name = lang_name.capitalize()+"_"+region+"_Selection"
                test_body = self._gen_unittest_test(test_name,
                                                 linux_env_string,
                                                 iso_code,
                                                 get_iso_method)
                test_body.append("\n") # whitespace for readability
                unittest_block.extend(test_body)

            # Generate test for unknown region of known language
            unknown_regionTestName =lang_name.capitalize()+"_unknown_region_Selection"
            unknown_regionEnv = lang_code+"_XX.UTF-8"
            unknown_regionBody = self._gen_unittest_test(unknown_regionTestName,
                                                      unknown_regionEnv,
                                                      iso_code,
                                                      get_iso_method)
            unknown_regionBody.append("\n") # whitespace for readability
            unittest_block.extend(unknown_regionBody)

        # Generate test for unknown region of unknown language and expect default
        default_lang, default_iso_code = self.lang_json_data.get_default_data()
        unknown_lang_body = self._gen_unittest_test("UnknownLanguageDefaultSelection",
                                                "xx_XX.UTF-8",
                                                default_iso_code,
                                                get_iso_method)
        unittest_block.extend(unknown_lang_body)

        # Generate block end code
        unittest_block.append("#endif // "+self.def_osString+"\n")
        return unittest_block

    def gen_unittest_function_call(self, check_var_name:str, indent:int = 4)->list:
        """!
        @brief Generate the call code for the linux dynamic lang selection unit test
        @param check_var_name {string} Unit test expected variable name
        @param indent {number} Code indentation spaces
        @return list of strings Formatted code lines
        """
        indent_text = "".rjust(indent, " ")
        local_var_name = "langId"

        get_param =  indent_text
        get_param += ParamRetDict.get_param_type(self.param_dict_list[0])
        get_param += " "
        get_param += local_var_name
        get_param += " = getenv(\"LANG\");\n"

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
        @brief Return linux specific include and external function definition strings
        @return list of strings - linux specific #if, #include, external function and #endif code
        """
        inc_block = []
        inc_block.append("#if "+self.def_osString+"\n")
        inc_block.append(self._gen_include("<cstdlib>"))
        inc_block.append(self.gen_extern_definition())
        inc_block.append("#endif // "+self.def_osString+"\n")
        return inc_block

    def get_unittest_file_name(self)->tuple:
        """!
        @return tuple(str,str) - Unit test cpp file name, Test name
        """
        return "LocalLanguageSelect_Linux_test.cpp", "LocalLanguageSelect_Linux_test"
