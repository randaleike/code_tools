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
from code_tools_grocsoftware.cpp_gen.file_gen_base import GenerateCppFileHelper
from code_tools_grocsoftware.base.eula import EulaText

class BaseCppStringClassGenerator(GenerateCppFileHelper):
    """!
    Base string class generation class
    """
    def __init__(self, base_class_name:str = "BaseClass",
                 dynamic_compile_switch:str = "DYNAMIC_INTERNATIONALIZATION",
                 version:str = "v0.0.0"):
        """!
        @brief BaseCppStringClassGenerator constructor
        @param base_class_name {string} Base class name for class definition generation
        @param dynamic_compile_switch {string} Dynamic language selection compile switch
        @param version {string} Version string
        """
        super().__init__()

        ## Base class name for class definition generations
        self.base_class_name = base_class_name

        ## Dynamic compile switch name for generation
        self.dynamic_compile_switch = dynamic_compile_switch

        ## Dynamic compile switch name for generation #if text
        self.if_dynamic_defined = "defined("+self.dynamic_compile_switch+")"

        ## CPP return type for the language selection static function
        self.base_intf_ret_ptr_type = "std::shared_ptr<"+self.base_class_name+">"

        ## CPP ParamRetDict return dictionary for the language selection static function
        retdesc = "Shared pointer to "+self.base_class_name+"<lang> based on OS local language"
        self.base_intf_ret_ptr_dict = ParamRetDict.build_return_dict('sharedptr', retdesc)

        # Add the specialty types
        self.type_xlation_dict['LANGID'] = "LANGID"
        self.type_xlation_dict['sharedptr'] = self.base_intf_ret_ptr_type
        self.type_xlation_dict['strstream'] = "std::stringstream"

        ## Autogeneration tool name
        self.auto_tool_name = str(self.__class__.__name__)+version

        ## Doxygen group name
        self.group_name = "LocalLanguageSelection"

        ## Doxygen group description
        self.group_desc = "Local language detection and selection utility"

        ## Default class method/variable declaration indentation
        self.declare_indent = 8

        ## Default method/function body indentation
        self.function_indent = 4

    def _get_string_type(self)->str:
        """!
        @brief Return the string type
        @return string - CPP string typ-e definition
        """
        return self.type_xlation_dict['string']

    def _get_char_type(self)->str:
        """!
        @brief Return the character type
        @return string - CPP character type definition
        """
        return self.type_xlation_dict['char']

    def _get_str_stream_type(self)->str:
        """!
        @brief Return the string stream type
        @return string - CPP string stream type definition
        """
        return self.type_xlation_dict['strstream']

    def _gen_make_ptr_return_statement(self, class_mod:str = None)->str:
        """!
        @brief Generate a language select return statement
        @param class_mod {string} Language name of the final parser string object
        @return string cpp code
        """
        if class_mod is not None:
            ptr_name = self.base_class_name+class_mod.capitalize()
        else:
            ptr_name = self.base_class_name

        ret_line = "return std::make_shared<"
        ret_line += ptr_name
        ret_line += ">();\n"
        return ret_line

    def _generate_file_header(self, eula:EulaText, owner:str='Unknown',
                              create_date:int=None)->list:
        """!
        @brief Generate the boiler plate file header with copyright and eula
        @return list - List of strings for the header
        """
        return super().generate_generic_file_header(eula, owner, create_date,
                                                    self.auto_tool_name)

    def gen_h_fname(self, lang_name:str = None)->str:
        """!
        @brief Generate the include file name based on the class and language names
        @return string - include file name
        """
        if lang_name is not None:
            retstr = self.base_class_name+lang_name.capitalize()+".h"
        else:
            retstr = self.base_class_name+".h"
        return retstr

    def gen_cpp_fname(self, lang_name:str = None)->str:
        """!
        @brief Generate the source file name based on the class and language names
        @return string - source file name
        """
        if lang_name is not None:
            retstr = self.base_class_name+lang_name.capitalize()+".cpp"
        else:
            retstr = self.base_class_name+".cpp"
        return retstr

    def gen_unittest_fname(self, lang_name:str = None)->str:
        """!
        @brief Generate the unittest source file name based on the class and language names
        @return string - unittest source file name
        """
        if lang_name is not None:
            retstr = self.base_class_name+lang_name.capitalize()+"_test.cpp"
        else:
            retstr = self.base_class_name+"_test.cpp"
        return retstr

    def gen_unittest_target_name(self, lang_name:str = None)->str:
        """!
        @brief Generate the unittest target class name based on the class and language names
        @return string - unittest target class name
        """
        if lang_name is not None:
            retstr = self.base_class_name+lang_name.capitalize()+"_test"
        else:
            retstr = self.base_class_name+"_test"
        return retstr

    def gen_mock_h_fname(self, lang_name:str = None)->str:
        """!
        @brief Generate the mock include file name based on the class and language names
        @return string - mock include file name
        """
        if lang_name is not None:
            retstr = "mock_"+self.base_class_name+lang_name.capitalize()+".h"
        else:
            retstr = "mock_"+self.base_class_name+".h"
        return retstr

    def gen_mock_cpp_fname(self, lang_name:str = None)->str:
        """!
        @brief Generate the mock source file name based on the class and language names
        @return string - mock source file name
        """
        if lang_name is not None:
            retstr = "mock_"+self.base_class_name+lang_name.capitalize()+".cpp"
        else:
            retstr = "mock_"+self.base_class_name+".cpp"
        return retstr

    def write_method(self, method_name:str, method_desc:str,
                     method_params:list, return_dict:dict, prefix:str, postfix:str,
                     skip_doxygen_comment:bool = True, inline_code:list = None)->list:
        """!
        @brief Write the property method definitions

        @param method_name {string} Property method name
        @param method_desc {string} Property description for doxygen comment block
        @param method_params {list of dictionaries} Method input parameter definitions(s)
        @param return_dict {dictionary} Return data definition
        @param prefix {string} Method declaration prefix
        @param postfix {string} Method declaration postfix
        @param skip_doxygen_comment {boolean} True = skip doxygen method comment generation,
                                              False = generate doxygen method comment
        @param inline_code {list of strings} Inline code strings or None if there is no inline code

        @return list of strings
        """
        if len(method_params) == 0:
            if postfix is not None:
                postfix_final = "const " + postfix
            else:
                postfix_final = "const"
        else:
            postfix_final = postfix

        # Output final declaration
        decl_text = self.declare_function_with_decorations(method_name,
                                                        method_desc,
                                                        method_params,
                                                        return_dict,
                                                        self.declare_indent,
                                                        skip_doxygen_comment,
                                                        prefix,
                                                        postfix_final,
                                                        inline_code)

        return decl_text

    def write_mock_method(self, method_name:str, method_params:list,
                          return_dict:dict, postfix:str)->list:
        """!
        @brief Write the property method definitions

        @param method_name {string} Property method name
        @param method_params {list of dictionaries} Method input parameter definitions(s)
        @param return_dict {dictionary} Return data definition
        @param postfix {string} Method declaration postfix

        @return list of strings - Mock method declaration
        """
        # Translate the param data
        if len(method_params) == 0:
            if postfix is not None:
                postfix_final = "const, " + postfix
            else:
                postfix_final = "const"
        else:
            postfix_final = postfix

        # Output mock declaration
        decl_text = "".rjust(self.declare_indent, ' ')
        decl_text += "MOCK_METHOD("
        decl_text += self.declare_type(ParamRetDict.get_return_type(return_dict),
                                       ParamRetDict.get_param_type_mod(return_dict))
        decl_text += ", "
        decl_text += method_name
        decl_text += ", "

        # Add the parameters
        decl_text += self.gen_function_params(method_params)

        # Add the post fix data
        if postfix_final is not None:
            decl_text += ", ("
            decl_text += postfix_final
            decl_text += ")"

        # Close the MOCK_METHOD macro and out put to file
        decl_text += ");\n"
        return [decl_text]

    def generate_property_unittest(self, method:str, ut_section:str,
                                   ret_dict:dict, expected:list,
                                   param_data,
                                   is_text:bool = False)->list:
        """!
        @brief Generate the unit test for the input property method
        @param propertyMethod {string} Property function name
        @param ut_section {string} Unittest section name
        @param ret_dict {dictionary} Method return dictionary definition
        @param expected {list} Expected data
        @param param_data {list} Property parameter test value list
        @return list of strings - Test code to output
        """
        code_txt = []
        body_indent = "".rjust(4, ' ')

        # Translate the return type
        code_txt.append("TEST("+ut_section+", fetch"+method+")\n")
        code_txt.append("{\n")
        vardecl = body_indent+ut_section+" testvar;\n"
        code_txt.append(vardecl)

        # Build the property function call
        fetch_code = self.gen_function_ret_type(ret_dict)
        fetch_code += "output = testvar."
        fetch_code += method
        fetch_code += "("
        param_prefix = ""
        for test_value in param_data:
            fetch_code += param_prefix
            fetch_code += test_value
            param_prefix = ", "
        fetch_code += ");\n"
        code_txt.append(body_indent+fetch_code)

        # Build the test assertion
        is_list = ParamRetDict.is_mod_list(ParamRetDict.get_return_type_mod(ret_dict))
        assert_pop = ""
        if is_list:
            assert_pop = ", output.pop_front()"
        else:
            assert_pop = ", output"

        for item in expected:
            if is_text:
                assert_start = "EXPECT_STREQ(\""+item+"\""
                assert_end = ".c_str());\n"
            else:
                assert_start = "EXPECT_EQ("+str(item)
                assert_end = ");\n"

            code_txt.append(body_indent+assert_start+assert_pop+assert_end)

        code_txt.append("}\n")
        return code_txt

    def generate_translate_unittest(self, method:str, ut_section:str,
                                    ret_dict:dict, expected:str,
                                    param_data:list)->list:
        """!
        @brief Generate the unit test for the input property method
        @param method {string} Tranlated string generation function name
        @param ut_section {string} Unittest section name
        @param ret_dict {dictionary} Method return dictionary definition
        @param expected {string} Expected response data
        @param param_data {list} Tranlated string generation function parameter
                                 test value list
        @return list of strings - Test code to output
        """
        code_txt = []
        body_indent = "".rjust(4, ' ')

        # Translate the return type
        code_txt.append("TEST("+ut_section+", print"+method+")\n")
        code_txt.append("{\n")
        code_txt.append(body_indent+ut_section+" testvar;\n")

        # Build the property function call
        fetch_code = self.gen_function_ret_type(ret_dict)
        fetch_code += "output = testvar."
        fetch_code += method
        fetch_code += "("
        param_prefix = ""
        for param_value in param_data:
            fetch_code += param_prefix
            fetch_code += param_value
            param_prefix = ", "
        fetch_code += ");\n"
        code_txt.append(body_indent+fetch_code)

        # Build the assertion test
        assert_txt = "EXPECT_STREQ(\""+expected+"\", output.c_str());\n"
        code_txt.append(body_indent+assert_txt)
        code_txt.append("}\n")
        return code_txt
