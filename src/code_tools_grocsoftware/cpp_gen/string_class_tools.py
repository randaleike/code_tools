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

class BaseCppStringClassGenerator(GenerateCppFileHelper):
    def __init__(self, owner:str|None = None, eula_name:str|None = None,
                 base_class_name:str = "BaseClass", dynamic_compile_switch:str = "DYNAMIC_INTERNATIONALIZATION"):
        """!
        @brief BaseCppStringClassGenerator constructor
        @param owner {string} Owner string for the copyright/EULA file header comment
        @param eula_name {string} EULA name for the copyright/EULA file header comment
        @param base_class_name {string} Base class name for class definition generation
        @param dynamic_compile_switch {string} Dynamic language selection compile switch
        """
        super().__init__(eula_name)
        ## Owner name for file header copyright message generation
        self.owner = "BaseCppStringClassGenerator"
        if owner is not None:
            self.owner = owner

        ## Base class name for class definition generations
        self.base_class_name = base_class_name

        ## Dynamic compile switch name for generation
        self.dynamic_compile_switch = dynamic_compile_switch

        ## Dynamic compile switch name for generation #if text
        self.if_dynamic_defined = "defined("+self.dynamic_compile_switch+")"

        ## CPP return type for the language selection static function
        self.base_intf_ret_ptr_type = "std::shared_ptr<"+self.base_class_name+">"

        ## CPP ParamRetDict return dictionary for the language selection static function
        self.base_intf_ret_ptr_dict = ParamRetDict.build_return_dict('sharedptr',
                                                                "Shared pointer to "+self.base_class_name+"<lang> based on OS local language")

        # Add the specialty types
        self.type_xlation_dict['LANGID'] = "LANGID"
        self.type_xlation_dict['sharedptr'] = self.base_intf_ret_ptr_type
        self.type_xlation_dict['strstream'] = "std::stringstream"

        ## Major version number definition for  the genertator
        self.version_major = 0
        ## Minor version number definition for  the genertator
        self.version_minor = 4
        ## Patch version number definition for  the genertator
        self.version_patch = 1

        ## Autogeneration tool name
        self.auto_tool_name = self.__class__.__name__+self._get_version()

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

    def _gen_make_ptr_return_statement(self, class_mod:str|None = None)->str:
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

    def _get_version(self)->str:
        """!
        @brief Return the version number as a string
        @return string - Version number
        """
        return "V"+str(self.version_major)+"."+str(self.version_minor)+"."+str(self.version_patch)

    def _generate_file_header(self)->list:
        """!
        @brief Generate the boiler plate file header with copyright and eula
        @return list - List of strings for the header
        """
        return super()._generate_generic_file_header(self.auto_tool_name, 2025, self.owner)

    def _generateHFileName(self, lang_name:str|None = None)->str:
        """!
        @brief Generate the include file name based on the class and language names
        @return string - include file name
        """
        if lang_name is not None:
            return self.base_class_name+lang_name.capitalize()+".h"
        else:
            return self.base_class_name+".h"

    def _generate_cpp_file_name(self, lang_name:str|None = None)->str:
        """!
        @brief Generate the source file name based on the class and language names
        @return string - source file name
        """
        if lang_name is not None:
            return self.base_class_name+lang_name.capitalize()+".cpp"
        else:
            return self.base_class_name+".cpp"

    def _generate_unittest_file_name(self, lang_name:str|None = None)->str:
        """!
        @brief Generate the unittest source file name based on the class and language names
        @return string - unittest source file name
        """
        if lang_name is not None:
            return self.base_class_name+lang_name.capitalize()+"_test.cpp"
        else:
            return self.base_class_name+"_test.cpp"

    def _generate_unittest_target_name(self, lang_name:str|None = None)->str:
        """!
        @brief Generate the unittest target class name based on the class and language names
        @return string - unittest target class name
        """
        if lang_name is not None:
            return self.base_class_name+lang_name.capitalize()+"_test"
        else:
            return self.base_class_name+"_test"

    def _generate_mockHFileName(self, lang_name:str|None = None)->str:
        """!
        @brief Generate the mock include file name based on the class and language names
        @return string - mock include file name
        """
        if lang_name is not None:
            return "mock_"+self.base_class_name+lang_name.capitalize()+".h"
        else:
            return "mock_"+self.base_class_name+".h"

    def _generate_mockCppFileName(self, lang_name:str|None = None)->str:
        """!
        @brief Generate the mock source file name based on the class and language names
        @return string - mock source file name
        """
        if lang_name is not None:
            return "mock_"+self.base_class_name+lang_name.capitalize()+".cpp"
        else:
            return "mock_"+self.base_class_name+".cpp"

    def _write_method(self, method_name:str, method_desc:str,
                     method_params:list, return_dict:dict, prefix:str|None, postfix:str|None,
                     skip_doxygen_comment:bool = True, inline_code:list|None = None)->list:
        """!
        @brief Write the property method definitions

        @param method_name {string} Property method name
        @param method_desc {string} Property description for doxygen comment block
        @param method_params {list of dictionaries} Method input parameter definitions(s)
        @param return_dict {dictionary} Return data definition
        @param prefix {string} Method declaration prefix
        @param postfix {string} Method declaration postfix
        @param skip_doxygen_comment {boolean} True = skip doxygen method comment generation, False = generate doxygen method comment
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
        decl_text = self._declare_function_with_decorations(method_name,
                                                        method_desc,
                                                        method_params,
                                                        return_dict,
                                                        self.declare_indent,
                                                        skip_doxygen_comment,
                                                        prefix,
                                                        postfix_final,
                                                        inline_code)

        return decl_text

    def _write_mock_method(self, method_name:str, method_params:list, return_dict:dict, postfix:str|None)->list:
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
        decl_text += self._declare_type(ParamRetDict.get_return_type(return_dict), ParamRetDict.get_param_type_mod(return_dict))
        decl_text += ", "
        decl_text += method_name
        decl_text += ", "

        # Add the parameters
        decl_text += self._gen_function_params(method_params)

        # Add the post fix data
        if postfix_final is not None:
            decl_text += ", ("
            decl_text += postfix_final
            decl_text += ")"

        # Close the MOCK_METHOD macro and out put to file
        decl_text += ");\n"
        return [decl_text]
