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

from code_tools_grocsoftware.base.doxygen_gen_tools import CDoxyCommentGenerator
from code_tools_grocsoftware.cpp_gen.string_class_tools import BaseCppStringClassGenerator

class StaticLangSelectFunctionGenerator(BaseCppStringClassGenerator):
    """!
    Methods for compile switch determined language select function generation
    """
    def __init__(self, json_project_data:ProjectDescription):
        """!
        @brief StaticLangSelectFunctionGenerator constructor
        @param json_project_data {ProjectDescription} JSON project description data
        """
        jsonstringdesc:StringClassDescription = json_project_data.get_string_data()
        base_class_name = jsonstringdesc.get_base_class_name()
        dynamic_compile_switch = jsonstringdesc.get_dynamic_compile_switch()

        super().__init__(base_class_name,
                         dynamic_compile_switch,
                         json_project_data.get_version())

        self.select_function_name = "get"+base_class_name+"_Static"

        self.def_static_string = "!defined("+dynamic_compile_switch+")"
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
        @brief Return the non-dynamic OS define string
        @return string - Static language detection C/CPP compile switch
        """
        return self.def_static_string

    def get_os_dynamic_define(self)->str:
        """!
        @brief Return the static language selection define
               compile switch string
        @return string - Static language selection define compile switch
        """
        return self.def_static_string

    def gen_function_define(self)->list:
        """!
        @brief Get the function declaration string for the given name
        @return string list - Function comment block and declaration start
        """
        desc = "Determine the correct local language class from the compile switch setting"
        code_list = self.define_function_with_decorations(self.select_function_name,
                                                          desc,
                                                          [],
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
        function_body = []
        function_body.append("#if "+self.def_static_string+"\n")

        # Generate function doxygen comment and start
        function_body.extend(self.gen_function_define())

        # Start function body generation
        body_indent = "".rjust(4, " ")

        # Generate #if #elf compile switch chain for each language in the dictionary
        first_loop = True
        for lang_name in self.lang_json_data.get_language_list():
            ifline = "  "
            if first_loop:
                ifline += "#if "
                first_loop = False
            else:
                ifline += "#elif "
            defname = self.lang_json_data.get_compile_switch_data(lang_name)
            ifline += "defined("+defname+")\n"
            function_body.append(ifline)
            function_body.append(body_indent+self._gen_make_ptr_return_statement(lang_name))

        # Add the final #else case
        function_body.append("  #else //undefined language compile switch, use default\n")
        errstr = "#error one of the language compile switches must be defined"
        function_body.append(body_indent+errstr+"\n")
        function_body.append("  #endif //end of language #if/#elifcompile switch chain\n")

        # Complete the function
        function_body.append(self.gen_function_end())
        function_body.append("#endif // "+self.def_static_string+"\n")
        return function_body

    def gen_return_function_call(self, indent:int = 4)->list:
        """!
        @brief Generate the call code for the linux dynamic lang selection function
        @param indent {number} Code indentation spaces
        @return list of strings Formatted code lines
        """
        indent_text = "".rjust(indent, " ")
        do_call = indent_text+"return "+self.select_function_name+"();\n"
        return [do_call]

    def gen_extern_definition(self)->str:
        """!
        @brief Return the external function definition
        @return string - External function definition line
        """
        extern_def = "extern "
        extern_def += self.base_intf_ret_ptr_type
        extern_def += " "
        extern_def += self.select_function_name
        extern_def += "();\n"
        return extern_def

    def gen_unit_test(self, get_iso_method:str)->list:
        """!
        @brief Generate all unit tests for the selection function
        @param get_iso_method {string} Name of the ParserStringListInterface return ISO code method
        @return list - Unittest string list
        """
        # Generate block start code
        unittest_text = []
        unittest_text.append("#if "+self.def_static_string+"\n")
        unittest_text.append(self.gen_extern_definition())
        unittest_text.append("\n") # white space for readability

        # Generate the testgen_doxy_method_comment
        breif_desc = "Test "+self.select_function_name+" selection case"
        test_header = self.doxy_comment_gen.gen_doxy_method_comment(breif_desc, [])
        unittest_text.extend(test_header)

        # Generate the tests
        body_indent = "".rjust(4, " ")
        test_var = "test_var"
        test_var_decl = self.base_intf_ret_ptr_type+" "+test_var
        expected_val = test_var+"->"+get_iso_method+"().c_str()"

        for lang_name in self.lang_json_data.get_language_list():
            switch = self.lang_json_data.get_compile_switch_data(lang_name)
            test_body = []
            test_body.append("#if defined("+switch+")\n")
            testblkname = "StaticSelectFunction"+lang_name.capitalize()
            test_body.append("TEST("+testblkname+", CompileSwitchedValue)\n")
            test_body.append("{\n")
            test_body.append(body_indent+"// Generate the test language string object\n")
            test_body.append(body_indent+test_var_decl+" = "+self.select_function_name+"();\n")
            getisoname = self.lang_json_data.get_iso_code_data(lang_name)
            test_body.append(body_indent+"EXPECT_STREQ(\""+getisoname+"\", "+expected_val+");\n")
            # Complete the function
            test_body.append("}\n")
            test_body.append("#endif //end of #if defined("+switch+")\n")
            test_body.append("\n") # whitespace for readability

            unittest_text.extend(test_body)

        # Generate block end code
        unittest_text.append("#endif // "+self.def_static_string+"\n")
        return unittest_text

    def gen_unittest_function_call(self, check_var_name:str, indent:int = 4)->list:
        """!
        @brief Generate the call code for the linux dynamic lang selection unit test
        @param check_var_name {string} Unit test expected variable name
        @param indent {number} Code indentation spaces
        @return list of strings Formatted code lines
        """
        indent_text = "".rjust(indent, " ")
        do_call = indent_text
        do_call += self.base_intf_ret_ptr_type
        do_call += " "
        do_call += check_var_name
        do_call += " = "
        do_call += self.select_function_name+"();\n"
        return [do_call]

    def get_unittest_extern_include(self)->list:
        """!
        @brief Return static specific include and external function definition strings
        @return list of strings - static specific #if, #include, external function and #endif code
        """
        inc_block = []
        inc_block.append("#if "+self.def_static_string+"\n")
        inc_block.append(self.gen_extern_definition())
        inc_block.append("#endif // "+self.def_static_string+"\n")
        return inc_block

    def get_unittest_file_name(self)->str:
        """!
        @return str - Unit test cpp file name
        """
        return "LocalLanguageSelect_Static_test.cpp"
