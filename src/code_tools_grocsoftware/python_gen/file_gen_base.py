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

from datetime import datetime

from code_tools_grocsoftware.base.copyright_generator import CopyrightGenerator
from code_tools_grocsoftware.base.eula import EulaText

from code_tools_grocsoftware.base.comment_gen_tools import PyCommentGenerator
from code_tools_grocsoftware.base.doxygen_gen_tools import PyDoxyCommentGenerator
from code_tools_grocsoftware.base.param_return_tools import ParamRetDict

#============================================================================
#============================================================================
# File generation helper class
#============================================================================
#============================================================================
class GeneratePythonFileHelper():
    """!
    @brief File generation helper class.

    This class implements boiler plate data and helper functions used by
    the parent file specific generation class to generate the file
    """
    def __init__(self, eula_name:str|None = None):
        """!
        @brief GenerateFileHelper constructor

        @param eula_name {string} Name of the EULA from EulaText class to use.
        """
        super().__init__()

        ## Copyright string generator for the file header generation
        self.copyright_generator = CopyrightGenerator()
        ## End User Licence Agreement (EULA) for the file header generation
        self.eula = None
        ## Standard indentation for code blocks
        self.level_tab_size = 4

        ## C/CPP Doxygen comment generator for generating doxygen comment blocks
        self.doxy_comment_gen = PyDoxyCommentGenerator()
        ## C/CPP comment generator for single line and block comments
        self.header_comment_gen = PyCommentGenerator(80, use_single_line=True)

        ## Translation dictionary from generic data types to CPP specific data types
        self.type_xlation_dict = {'string':"str",
                                'text':"str",
                                'size':"int",
                                'integer':"int",
                                'unsigned':"int",
                                'structure':"dict",
                                'tuple':"tuple"}

        if eula_name is None:
            self.eula = EulaText("MIT_open")
        else:
            self.eula = EulaText(eula_name)

    def _declare_type(self, base_type:str, type_mod:int=0)->str:
        """!
        @brief Generate the type text based on the input type name and type modification data
        @param base_type (str) Delclaration type
        @param type_mod (int) ParamRetDict type modification code
        @return string - : Type(s)
        """
        array_size = ParamRetDict.get_array_size(type_mod)
        if ParamRetDict.is_mod_list(type_mod) or (array_size > 0):
            if ParamRetDict.is_or_undef_type(type_mod):
                return_text = "list|None"
            else:
                return_text = "list"
        else:
            lang_type = base_type
            if base_type in list(self.type_xlation_dict.keys()):
                lang_type = self.type_xlation_dict[base_type]

            if ParamRetDict.is_or_undef_type(type_mod):
                return_text = lang_type+"|None"
            else:
                return_text = lang_type
        return return_text

    def _xlate_params(self, param_dict_list:list)->list:
        """!
        @brief Translate the generic parameter list type strings to the python specific parameter type strings
        @param param_dict_list {list} List of ParamRetDict parameter dictionaries to translate
        @return list - List of ParamRetDict parameter dictionaries with the translated type
        """
        xlated_params = []
        for param in param_dict_list:
            xlated_type = self._declare_type(ParamRetDict.get_param_type(param), ParamRetDict.get_param_type_mod(param))
            xlated_param = ParamRetDict.build_param_dict_with_mod(ParamRetDict.get_param_name(param),
                                                             xlated_type,
                                                             ParamRetDict.get_param_desc(param),
                                                             0)
            xlated_params.append(xlated_param)
        return xlated_params

    def _xlate_return_dict(self, ret_dict:dict|None)->dict|None:
        """!
        @brief Translate the generic return dictionary to the python specific return dictionary
        @param ret_dict {dictionary} ParamRetDict return dictionary to translate
        @return dictionary|None - ParamRetDict return dictionary with the translated type or None if input is None
        """
        if ret_dict is not None:
            xlated_type = self._declare_type(ParamRetDict.get_return_type(ret_dict), ParamRetDict.get_return_type_mod(ret_dict))
            return ParamRetDict.build_return_dict_with_mod(xlated_type, ParamRetDict.get_return_desc(ret_dict), 0)
        else:
            return None

    def _gen_function_ret_type(self, return_dict:dict|None)->str:
        """!
        @brief Generate the function return+name string
        @param return_dict (dict|None) Return ParamRetDict dictionary
        @return string - return_spec name
        """
        return_text = ""
        if return_dict is not None:
            type_name = ParamRetDict.get_return_type(return_dict)
            type_mod = ParamRetDict.get_return_type_mod(return_dict)
            return_text += " -> "
            return_text += self._declare_type(type_name, type_mod)

        return_text += ":"
        return return_text

    def _gen_function_params(self, param_dict_list:list)->str:
        """!
        @brief Generate the parameter method string
        @param param_dict_list (list) List of parameter dictionaries
        @return string - (typespec name, ...)
        """
        param_prefix = ""
        param_text = "("
        for param_dict in param_dict_list:
            type_name = ParamRetDict.get_param_type(param_dict)
            type_mod = ParamRetDict.get_param_type_mod(param_dict)

            param_text += param_prefix
            param_text += ParamRetDict.get_param_name(param_dict)
            param_text += ":"
            param_text += self._declare_type(type_name, type_mod)
            param_prefix = ", "
        param_text += ")"
        return param_text

    def _declare_function_with_decorations(self, name:str, briefdesc:str, param_dict_list:list, ret_dict:dict|None = None,
                                       indent:int = 4, no_doxygen:bool = False, prefix_decaration:str|None = None,
                                       postfix_decaration:str|None = None, inlinecode:list|None = None,
                                       long_desc:str|None = None)->list:
        """!
        @brief Generate a function declatation text block with doxygen comment

        @param name {string} Function name
        @param briefdesc {string} Function description
        @param param_dict_list {list of dictionaries} - Return parameter data
        @param ret_dict {dictionary or None} - Return parameter data or None
        @param indent {integer} Comment and function declaration indentation
        @param no_doxygen {boolean} True skip doxygen comment generation, False generate doxygen comment block
        @param prefix_decaration {string} Valid C/C++ declaration prefix decoration, i.e "virtual"
        @param postfix_decaration {string} Valid C/C++ declaration postfix decoration, i.e "const" | "override" ...
        @param inlinecode {sting list or None} Inline code for the declaration or None id there is no inline definition
        @param long_desc {string or None} Long description of the function

        @return string list - Function doxygen comment block and declaration
        """
        func_declare_text = []
        decl_indent = "".rjust(indent, ' ')

        # Add fungen_doxy_method_commentction prefix definitions if defined
        if prefix_decaration is not None:
            func_declare_text.append(decl_indent+prefix_decaration+"\n")

        # Create function declaration line
        func_line = decl_indent
        func_line += "def "
        func_line += name

        # Add the function parameters
        func_line += self._gen_function_params(param_dict_list)
        func_line += self._gen_function_ret_type(ret_dict)
        func_line += "\n"
        func_declare_text.append(func_line)

        # Add doxygen comment block
        if not no_doxygen:
            xlated_paramList = self._xlate_params(param_dict_list)
            xlated_ret = self._xlate_return_dict(ret_dict)
            func_declare_text.extend(self.doxy_comment_gen.gen_doxy_method_comment(briefdesc, xlated_paramList, xlated_ret,
                                                                            long_desc, indent+self.level_tab_size))

        # Add inline code if defined
        inline_indent = "".rjust(indent+self.level_tab_size, ' ')
        if inlinecode is None:
            func_declare_text.append(inline_indent+self.doxy_comment_gen.gen_single_line_start()+" @todo Implement code\n")
        else:
            for code_line in inlinecode:
                func_declare_text.append(inline_indent+code_line+"\n")

        return func_declare_text

    def _define_function_with_decorations(self, name:str, briefdesc:str, param_dict_list:list, ret_dict:dict,
                                      no_doxygen:bool = False, prefix_decaration:str|None = None,
                                      postfix_decaration:str|None = None, long_desc:list|None = None)->list:
        """!
        @brief Generate a function definition start with doxygen comment

        @param name {string} Function name
        @param briefdesc {string} Function description
        @param param_dict_list {list of dictionaries} - Return parameter data
        @param ret_dict {dictionary} - Return parameter data
        @param no_doxygen {boolean} True skip doxygen comment generation, False generate doxygen comment block
        @param prefix_decaration {string or None} Valid C/C++ decldefine_function_with_decorationsaration prefix decoration, i.e "virtual"
        @param postfix_decaration {string or None} Valid C/C++ declaration postfix decoration, i.e "const" | "override" ...
        @param long_desc {string or None} Long description of the function

        @return string list - Function doxygen comment block and declaration start
        """
        func_define_text = []

        # Add function prefix definitions if defined
        if prefix_decaration is not None:
            func_define_text.append(prefix_decaration+"\n")

        # Create function declaration line
        func_line = "def "
        func_line += name

        # Add the function parameters
        func_line += self._gen_function_params(param_dict_list)
        func_line += self._gen_function_ret_type(ret_dict)
        func_line += "\n"
        func_define_text.append(func_line)

        # Add doxygen comment block
        if not no_doxygen:
            xlated_paramList = self._xlate_params(param_dict_list)
            xlated_ret = self._xlate_return_dict(ret_dict)
            func_define_text.extend(self.doxy_comment_gen.gen_doxy_method_comment(briefdesc, xlated_paramList, xlated_ret,
                                                                           long_desc, self.level_tab_size))
        return func_define_text

    def _end_function(self, name:str)->str:
        """!
        @brief Get the function declaration string for the given name
        @param name (string) - Function name
        @return string - Function close with comment
        """
        return "# end of function "+name+"\n"

    def _generate_generic_file_header(self, autotoolname:str, start_year:int=2025, owner:str|None = None)->list:
        """!
        @brief Generate the boiler plate file header with copyright and eula

        @param autotoolname {string} Auto generation tool name for comments
        @param start_year {number} First copyright year
        @param owner {string or None} File owner for copyright message or None
        @return list of strings - Code to output
        """
        comment_text = []
        copyright_eula_text = []
        if owner is not None:
            # Generate copyright and EULA text
            current_year = datetime.now().year
            copyright_eula_text.append(self.copyright_generator.create_new_copyright(owner, start_year, current_year))
            copyright_eula_text.append("") # white space for readability
            copyright_eula_text.append(self.eula.format_eula_name())
            copyright_eula_text.append("") # white space for readability
            copyright_eula_text.extend(self.eula.format_eula_text())
            copyright_eula_text.append("") # white space for readability

        copyright_eula_text.append("This file was autogenerated by "+autotoolname+" do not edit")
        copyright_eula_text.append("") # white space for readability

        # Generate comment header
        for line in self.header_comment_gen.build_comment_block_header():
            comment_text.append(line+"\n")

        # Wrap and output comment_text lines
        for line in copyright_eula_text:
            comment_text.append(self.header_comment_gen.wrap_comment_line(line)+"\n")

        # Generate comment footer
        for line in self.header_comment_gen.build_comment_block_footer():
            comment_text.append(line+"\n")
        return comment_text

    def _gen_import(self, class_name:str, module_name:str = None)->str:
        """!
        @brief Add Include line to the output file
        @param class_name {string} Name of the class to import
        @param module_name {string} Name of the module to import from
        @return string - Import statement
        """
        if module_name is not None:
            return "from "+module_name+" import "+class_name+"\n"
        else:
            return "import "+class_name+"\n"

    def _gen_importBlock(self, include_names:list)->list:
        """!
        @brief Generate a series if include line(s) for each name in the list
        @param include_names {list of tuples} Name(s) of class(es), Module name(s) of the class to import
        @return list of strings - Import code block to output
        """
        include_block = ["// Imports\n"]
        for class_name, module_name in include_names:
            include_block.append(self._gen_import(class_name, module_name))
        return include_block

    def _gen_namespace_open(self, namespace_name:str)->list:
        """!
        @brief Generate namespace start code for include file
        @param namespace_name {string} Name of the namespace
        @return list of strings - Code to output
        """
        return []

    def _gen_namespace_close(self, namespace_name:str)->list:
        """!
        @brief Generate namespace start code for include file
        @param namespace_name {string} Name of the namespace
        @return list of strings - Code to output
        """
        return []

    def _gen_using_namespace(self, namespace_name:str)->list:
        """!
        @brief Generate namespace start code for include file
        @param namespace_name {string} Name of the namespace
        @return list of strings - Code to output
        """
        return []

    def _gen_class_open(self, class_name:str, class_desc:str|None=None, inheritence:str|None = None,
                      class_decoration:str|None = None, indent:int=0)->list:
        """!
        @brief Generate the class open code

        @param class_name {string} Name of the class
        @param class_desc {string} Description of the class object
        @param inheritence {sting} Parent class and visability or None
        @param class_decoration {sting} Class decoration or None, ignored in python
        @param indent {integer} Space indentation for the declaration and comments

        @return list of strings - Code to output
        """
        code_text = []
        decl_indent = "".rjust(indent, ' ')

        # Generate class start
        if inheritence is None:
            inheritence = "object"
        code_text.append(decl_indent+"class "+class_name+"("+inheritence+"):\n")

        # Generate Doxygen class description
        if class_desc is not None:
            code_text.extend(self.doxy_comment_gen.gen_doxy_class_comment(class_desc, None, self.level_tab_size+indent))

        return code_text

    def _gen_class_close(self, class_name:str, indent:int=0)->list:
        """!
        @brief Generate the class close code

        @param class_name {string} Name of the class
        @param indent {integer} Space indentation for the declaration and comments

        @return list of strings - Code to output
        """
        return ["".rjust(indent, ' ')+"# end of "+class_name+" class\n"]

    def _gen_class_default_constructor(self, class_name:str, indent:int = 4, param_list:list=[],
                                   constructor_code:list= [], no_doxy_comment_constructor:bool = False)->list:
        """!
        @brief Generate default constructor(s)/destructor declarations for a class

        @param class_name {string} Name of the class
        @param indent {number} Indentation space count for the declarations (default = 8)
        @param param_list {list} List of parameter dictionaries
        @param constructor_code {list} Constructor code
        @param no_doxy_comment_constructor {boolean} Doxygen comment disable. False = generate doxygen comments,
                                                  True = ommit comments
        @return list of strings - Code to output
        """
        # Declare default default constructor
        code_text = self._declare_function_with_decorations("__init__",
                                                       "Construct a new "+class_name+" object",
                                                       param_list,
                                                       None,
                                                       indent,
                                                       no_doxy_comment_constructor,
                                                       None,
                                                       None,
                                                       constructor_code)
        code_text.append("".rjust(indent, ' ')+"\n")      #whitespace for readability
        return code_text

    def _declare_structure(self, name:str, var_dist_list:list, indent:int=0,
                          struct_desc:str|None = None)->list:
        """!
        @brief Generate a structure declaration

        @param name {string} Name of the structure
        @param var_dist_list {list} List of ParamRetDict parameter dictionaries for the data elements
        @param indent {integer} Number of spaces to indent the code declarations, default = 0
        @param struct_desc {string|None} Doxygen structure description

        @return list of strings - Code to output
        """
        # Generate the declaration
        code_text = self._gen_class_open(name, struct_desc, "object", indent=indent)

        # Generate the body code
        for var_dict in var_dist_list:
            code_text.append(self._declare_var_statment(var_dict, indent+self.level_tab_size))

        # Close the struture
        code_text.extend(self._gen_class_close(name, indent))
        return code_text

    def _declare_var_statment(self, var_dict:dict, doxy_comment_indent:int = -1)->str:
        """!
        @brief Declare a class/interface variable
        @param var_dict {dict} ParamRetDict parameter dictionary describing the variable
        @param doxy_comment_indent {int} Column to begin the doxygen comment
        @return string Variable declatation code
        """
        if doxy_comment_indent != -1:
            indent = "".ljust(doxy_comment_indent, ' ')
        else:
            indent = ""

        # Declare the variable
        type_name = ParamRetDict.get_param_type(var_dict)
        type_mod = ParamRetDict.get_param_type_mod(var_dict)

        var_type_decl = self._declare_type(type_name, type_mod)
        var_decl = indent+ParamRetDict.get_param_name(var_dict)+":"+var_type_decl

        # Generate documentation string
        doc_decl = indent+self.doxy_comment_gen.gen_doxy_var_doc_str(ParamRetDict.get_param_desc(var_dict))

        # Return the final data
        return doc_decl+"\n"+var_decl+"\n"

    def _gen_add_list_statment(self, list_name:str, value_name:str, is_text:bool=False)->str:
        """!
        @brief Generate a list add code statement
        @param list_name {string} Name of the list variable to add the value_name to
        @param value_name {string} Name of the value to add to the list object
        @param is_text {boolean} False if value_name is a variable name or numeric value,
                                True if value_name is a text string
                                default = False
        @return string - Python code text
        """
        if is_text:
            return list_name+".append(\""+value_name+"\")"
        else:
            return list_name+".append("+value_name+")"

    def _gen_return_statment(self, ret_value:str, is_text:bool=False)->str:
        """!
        @brief Generate a list add code statement
        @param ret_value {string} Name of the return variable
        @param is_text {boolean} False if ret_value is a variable name or numeric value,
                                True if ret_value is a text string
                                default = False
        @return string - Python code text
        """
        if is_text:
            return "return \""+ret_value+"\""
        else:
            return "return "+ret_value
