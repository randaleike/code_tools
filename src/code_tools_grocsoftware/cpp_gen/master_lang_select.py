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

from code_tools_grocsoftware.base.doxygen_gen_tools import CDoxyCommentGenerator
from code_tools_grocsoftware.cpp_gen.string_class_tools import BaseCppStringClassGenerator

from code_tools_grocsoftware.base.project_json import ProjectDescription
from code_tools_grocsoftware.base.json_string_class_description import StringClassDescription

class MasterSelectFunctionGenerator(BaseCppStringClassGenerator):
    """!
    Methods for master language select function generation
    """
    def __init__(self, project_data:ProjectDescription,
                 method_name:str = "getLocalParserStringListInterface"):
        """!
        @brief MasterSelectFunctionGenerator constructor
        @param project_data {ProjectDescription} JSON project description data
        @param method_name {string} Function name to be used for generation
        """
        jsonstringdesc:StringClassDescription = project_data.get_string_data()
        base_class_name = jsonstringdesc.get_base_class_name()
        dynamic_compile_switch = jsonstringdesc.get_dynamic_compile_switch()

        super().__init__(base_class_name,
                         dynamic_compile_switch,
                         project_data.get_version())

        self.select_function_name = base_class_name+"::"+method_name
        self.select_base_function_name = method_name

        self.brief_desc = "Determine the OS use OS specific functions to determine the " \
                          "correct local language based on the OS specific local language " \
                          "setting and return the correct class object"
        self.doxy_comment_gen = CDoxyCommentGenerator()

    def get_function_name(self)->str:
        """!
        @brief Return the selection function name
        @return string - Selection function name
        """
        return self.select_function_name

    def get_function_desc(self)->tuple:
        """!
        @brief Generate a function declatation text block with doxygen comment
        @return tuple - Function (name, description, return dictionary, param list)
        """
        return self.select_base_function_name, self.brief_desc, self.base_intf_ret_ptr_dict, []

    def gen_function_define(self)->list:
        """!
        @brief Get the function declaration string for the given name
        @return string list - Function comment block and declaration start
        """
        code_list = self.define_function_with_decorations(self.select_function_name,
                                                          self.brief_desc,
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

    def gen_function(self, os_lang_selectors)->list:
        """!
        @brief Generate the function body text
        @param os_lang_selectors {list} List of OS language selector function generation objects
        @return list - Function body string list
        """
        # Generate function doxygen comment and start
        function_body = []
        function_body.extend(self.gen_function_define())
        body_indent = 4
        body_prefix = "".rjust(body_indent, ' ')

        # Generate OS calls
        first_os = True
        for os_selector in os_lang_selectors:
            if first_os:
                function_body.append("#if "+os_selector.get_os_define()+"\n")
                first_os = False
            else:
                function_body.append("#elif "+os_selector.get_os_define()+"\n")
            function_body.extend(os_selector.gen_return_function_call(body_indent))

        # Add the #else case
        function_body.append("#else // not defined os\n")
        errmsg = "#error No language generation method defined for this OS\n"
        function_body.append(body_prefix+errmsg)

        # Complete the function
        function_body.append("#endif // defined os\n")
        function_body.append(self.gen_function_end())
        return function_body

    def gen_return_function_call(self, indent:int = 4)->list:
        """!
        @brief Generate the call code for the linux dynamic lang selection function
        @param indent {number} Code indentation spaces
        @return list of strings Formatted code lines
        """
        do_call = "".rjust(indent, " ")+"return "+self.select_function_name+"();\n"
        return [do_call]

    def gen_unit_test(self, get_iso_method:str, os_lang_selectors)->list:
        """!
        @brief Generate all unit tests for the selection function

        @param get_iso_method {string} Name of the ParserStringListInterface return ISO code method
        @param os_lang_selectors {list} List of OS language selector function generation objects
        @return list - Unittest text list
        """
        test_body = []

        # generate the externals
        for os_selector in os_lang_selectors:
            test_body.extend(os_selector.get_unittest_extern_include())
        test_body.append("\n") # whitespace for readability

        # Generate the test
        test_block_name = "SelectFunction"
        body_indent_idx = 4
        body_indent = "".rjust(body_indent_idx, " ")
        breif_desc = "Test "+self.select_function_name+" selection case"
        test_body.extend(self.doxy_comment_gen.gen_doxy_method_comment(breif_desc, []))

        test_var = "test_var"
        test_var_decl = self.base_intf_ret_ptr_type+" "+test_var
        test_body.append("TEST("+test_block_name+", TestLocalSelectMethod)\n")
        test_body.append("{\n")

        # Generate OS calls
        first_os = True
        expected_parser = "localStringParser"
        for os_selector in os_lang_selectors:
            if first_os:
                test_body.append("#if "+os_selector.get_os_define()+"\n")
                first_os = False
            else:
                test_body.append("#elif "+os_selector.get_os_define()+"\n")
            test_body.append(body_indent+"// Get the expected value\n")
            test_body.extend(os_selector.gen_unittest_function_call(expected_parser,
                                                                    body_indent_idx))

        # Add the #else case
        test_body.append("#else // not defined os\n")
        test_body.append(body_indent+"#error No language generation defined for this OS\n")

        # Complete the function
        test_body.append("#endif // defined os\n")
        get_expected_val = expected_parser+"->"+get_iso_method+"().c_str()"
        expected_val = test_var+"->"+get_iso_method+"().c_str()"
        test_body.append("\n") # whitespace for readability

        test_body.append(body_indent+"// Generate the test language string object\n")
        test_body.append(body_indent+test_var_decl+" = "+self.select_function_name+"();\n")
        test_body.append(body_indent+"EXPECT_STREQ("+get_expected_val+", "+expected_val+");\n")
        test_body.append(self.gen_function_end())
        return test_body
