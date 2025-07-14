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

from code_tools_grocsoftware.base.comment_gen_tools import CCommentGenerator
from code_tools_grocsoftware.base.doxygen_gen_tools import CDoxyCommentGenerator
from code_tools_grocsoftware.base.param_return_tools import ParamRetDict

#============================================================================
#============================================================================
# File generation helper class
#============================================================================
#============================================================================
class GenerateCppFileHelper():
    """!
    @brief File generation helper class.

    This class implements boiler plate data and helper functions used by
    the parent file specific generation class to generate the file
    """
    def __init__(self, eula_name:str = None):
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
        self.doxy_comment_gen = CDoxyCommentGenerator()
        ## C/CPP comment generator for single line and block comments
        self.header_comment_gen = CCommentGenerator(80)

        ## Translation dictionary from generic data types to CPP specific data types
        self.type_xlation_dict = {'string':"std::string",
                                'text':"std::string",
                                'size':"size_t",
                                'integer':"int",
                                'unsigned':"unsigned",
                                'char':"char"}

        if eula_name is None:
            self.eula = EulaText("MIT_open")
        else:
            self.eula = EulaText(eula_name)

    def _declare_type(self, base_type:str, type_mod:int=0)->str:
        """!
        @brief Generate the type text based on the input type name and type modification data
        @param base_type (str) Delclaration type
        @param type_mod (int) ParamRetDict type modification code
        @return string C++ type specification
        """
        type_return = base_type
        if base_type in list(self.type_xlation_dict.keys()):
            type_return = self.type_xlation_dict[base_type]

        array_size = ParamRetDict.get_array_size(type_mod)
        if array_size > 0:
            if ParamRetDict.is_mod_pointer(type_mod):
                return "std::array<"+type_return+"*, "+str(array_size)+">"
            elif ParamRetDict.is_mod_reference(type_mod):
                return "std::array<"+type_return+"&, "+str(array_size)+">"
            else:
                return "std::array<"+type_return+", "+str(array_size)+">"
        elif ParamRetDict.is_mod_list(type_mod):
            if ParamRetDict.is_mod_pointer(type_mod):
                return "std::list<"+type_return+"*>"
            elif ParamRetDict.is_mod_reference(type_mod):
                return "std::list<"+type_return+"&>"
            else:
                return "std::list<"+type_return+">"
        else:
            if ParamRetDict.is_mod_pointer(type_mod):
                return type_return+"*"
            elif ParamRetDict.is_mod_reference(type_mod):
                return type_return+"&"
            else:
                return type_return

    def _xlate_params(self, param_dict_list:list)->list:
        """!
        @brief Translate the generic parameter list type strings to the cpp specific parameter type strings
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

    def _xlate_return_dict(self, ret_dict:dict)->dict:
        """!
        @brief Translate the generic return dictionary to the cpp specific return dictionary
        @param ret_dict {dictionary} ParamRetDict return dictionary to translate
        @return dictionary - ParamRetDict return dictionary with the translated type or None if input is None
        """
        if ret_dict is not None:
            xlated_type = self._declare_type(ParamRetDict.get_return_type(ret_dict), ParamRetDict.get_return_type_mod(ret_dict))
            return ParamRetDict.build_return_dict_with_mod(xlated_type, ParamRetDict.get_return_desc(ret_dict), 0)
        else:
            return None

    def _gen_function_ret_type(self, return_dict:dict)->str:
        """!
        @brief Generate the function return+name string
        @param return_dict (dict) Return ParamRetDict dictionary
        @return string - return_spec name
        """
        if return_dict is not None:
            type_name = ParamRetDict.get_return_type(return_dict)
            type_mod = ParamRetDict.get_return_type_mod(return_dict)
            return_text = self._declare_type(type_name, type_mod)
            return_text += " "
        else:
            return_text = ""
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
            param_text += self._declare_type(type_name, type_mod)
            param_text += " "
            param_text += ParamRetDict.get_param_name(param_dict)
            param_prefix = ", "
        param_text += ")"
        return param_text

    def _declare_function_with_decorations(self, name:str, briefdesc:str, param_dict_list:list, ret_dict:dict = None,
                                        indent:int = 0, no_doxygen:bool = False, prefix_decaration:str = None,
                                        postfix_decaration:str = None, inlinecode:list = None,
                                        long_desc:str = None)->list:
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

        # Add doxygen comment block
        if not no_doxygen:
            xlated_paramList = self._xlate_params(param_dict_list)
            xlated_ret = self._xlate_return_dict(ret_dict)
            func_declare_text.extend(self.doxy_comment_gen.gen_doxy_method_comment(briefdesc, xlated_paramList, xlated_ret, long_desc, indent))

        # Create function declaration line
        func_line = "".rjust(indent, ' ')

        # Add function prefix definitions if defined
        if prefix_decaration is not None:
            func_line += prefix_decaration
            func_line += " "

        # Construct main function declaration
        func_line += self._gen_function_ret_type(ret_dict)
        func_line += name

        # Add the function parameters
        func_line += self._gen_function_params(param_dict_list)

        # Add function post fix decorations if defined
        if postfix_decaration is not None:
            func_line += " "
            func_line += postfix_decaration

        # Add inline code if defined
        if inlinecode is None:
            func_line += ";\n"
            func_declare_text.append(func_line)
        else:
            func_line += "\n"
            func_declare_text.append(func_line)
            inline_indent = "".rjust(indent, ' ')
            inline_start = inline_indent+"{"
            if len(inlinecode) == 1:
                func_declare_text.append(inline_start+inlinecode[0]+"}\n")
            else:
                func_declare_text.append(inline_start+"\n")
                inline_body_indent = "".rjust(indent+self.level_tab_size, ' ')
                for code_line in inlinecode:
                    code_line += "\n"
                    func_declare_text.append(inline_body_indent+code_line)
                func_declare_text.append(inline_indent+"}\n")

        return func_declare_text


    def _define_function_with_decorations(self, name:str, briefdesc:str, param_dict_list:list, ret_dict:dict,
                                       no_doxygen:bool = False, prefix_decaration:str = None,
                                       postfix_decaration:str = None, long_desc:list = None)->list:
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
        func_line = ""

        # Add doxygen comment block
        if not no_doxygen:
            xlated_paramList = self._xlate_params(param_dict_list)
            xlated_ret = self._xlate_return_dict(ret_dict)
            func_define_text.extend(self.doxy_comment_gen.gen_doxy_method_comment(briefdesc, xlated_paramList, xlated_ret, long_desc))

        # Add function prefix definitions if defined
        if prefix_decaration is not None:
            func_line += prefix_decaration
            func_line += " "

        # Create function definition line
        func_line += self._gen_function_ret_type(ret_dict)
        func_line += name
        func_line += self._gen_function_params(param_dict_list)

        # Add function post fix decorations if defined
        if postfix_decaration is not None:
            func_line += " "
            func_line += postfix_decaration
        func_define_text.append(func_line+"\n")

        return func_define_text

    def _end_function(self, name:str)->str:
        """!
        @brief Get the function declaration string for the given name
        @param name (string) - Function name
        @return string - Function close with comment
        """
        return "} // end of "+name+"()\n"

    def _generate_generic_file_header(self, autotoolname:str, start_year:int=2025, owner:str = None)->list:
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

    def _gen_include(self, include_name:str)->str:
        """!
        @brief Add Include line to the output file
        @param include_name {string} Name of the include file to add
        @return string - Include statement
        """
        if -1 == include_name.find("<"):
            return "#include \""+include_name+"\"\n"
        else:
            return "#include "+include_name+"\n"

    def _gen_include_block(self, include_names:list)->list:
        """!
        @brief Generate a series if include line(s) for each name in the list
        @param include_names {list of strings} Name(s) of the include file to add
        @return list of strings - Include code block to output
        """
        include_block = ["// Includes\n"]
        for include_name in include_names:
            include_block.append(self._gen_include(include_name))
        return include_block

    def _gen_namespace_open(self, namespace_name:str)->list:
        """!
        @brief Generate namespace start code for include file
        @param namespace_name {string} Name of the namespace
        @return list of strings - Code to output
        """
        return ["namespace "+namespace_name+" {\n"]

    def _gen_namespace_close(self, namespace_name:str)->list:
        """!
        @brief Generate namespace start code for include file
        @param namespace_name {string} Name of the namespace
        @return list of strings - Code to output
        """
        return ["}; // end of namespace "+namespace_name+"\n"]

    def _gen_using_namespace(self, namespace_name:str)->list:
        """!
        @brief Generate namespace start code for include file
        @param namespace_name {string} Name of the namespace
        @return list of strings - Code to output
        """
        return ["using namespace "+namespace_name+";\n"]

    def _gen_class_open(self, class_name:str, class_desc:str = None, inheritence:str = None,
                      class_decoration:str = None, indent:int=0)->list:
        """!
        @brief Generate the class open code

        @param class_name {string} Name of the class
        @param class_desc {string} Description of the class
        @param inheritence {sting} Parent class and visability or None
        @param class_decoration {sting} Class decoration or None
        @param indent {integer} Space indentation for the declaration and comments

        @return list of strings - Code to output
        """
        code_text = []
        decl_indent = "".rjust(indent, ' ')

        # Generate Doxygen class description
        if class_desc is not None:
            code_text.extend(self.doxy_comment_gen.gen_doxy_class_comment(class_desc, block_indent=indent))

        # Generate class start
        decl_line = decl_indent+"class "+class_name
        if inheritence is not None:
            if class_decoration is not None:
                decl_line += " "
                decl_line += class_decoration
                decl_line += " : "
                decl_line += inheritence
            else:
                decl_line += " : "
                decl_line += inheritence

        code_text.append(decl_line+"\n")
        code_text.append(decl_indent+"{\n")

        return code_text

    def _gen_class_close(self, class_name:str, indent:int=0)->list:
        """!
        @brief Generate the class close code

        @param class_name {string} Name of the class
        @param indent {integer} Space indentation for the declaration and comments

        @return list of strings - Code to output
        """
        return ["".rjust(indent, ' ')+"}; // end of "+class_name+" class\n"]

    def _gen_class_default_constructor_destructor(self, class_name:str, indent:int = 8, virtual_destructor:bool = False,
                                              no_doxy_comment_constructor:bool = False, no_copy:bool = False)->list:
        """!
        @brief Generate default constructor(s)/destructor declarations for a class

        @param class_name {string} Name of the class
        @param indent {number} Indentation space count for the declarations (default = 8)
        @param virtual_destructor {boolean} False if destructor is not virtual (default)
                                           True if virtual decoration on destructor
        @param no_doxy_comment_constructor {boolean} Doxygen comment disable. False = generate doxygen comments,
                                                  True = ommit comments
        @param no_copy {boolean} Disable copy constructors, True: copy/move constructors = delete
                                                           False: copy/move constructors = default
        @return list of strings - Code to output
        """
        # Setup params for the different constructors
        other_reference = [ParamRetDict.build_param_dict("other", "const "+class_name+"&", "Reference to object to copy")]
        other_move = [ParamRetDict.build_param_dict("other", class_name+"&&", "Reference to object to move")]
        equate_return = ParamRetDict.build_return_dict(class_name+"&", "*this")
        destructor_prefix = None

        if no_copy:
            copy_constructor_postfix = "= delete"
        else:
            copy_constructor_postfix = "= default"

        if virtual_destructor:
            destructor_prefix = "virtual"

        # Declare default default constructor
        code_text = self._declare_function_with_decorations(class_name,
                                                       "Construct a new "+class_name+" object",
                                                       [],
                                                       None,
                                                       indent,
                                                       no_doxy_comment_constructor,
                                                       None,
                                                       "= default")
        if not no_doxy_comment_constructor:
            code_text.append("\n")      #whitespace for readability

        # Declare default copy constructor
        code_text.extend(self._declare_function_with_decorations(class_name,
                                                            "Copy constructor for a new "+class_name+" object",
                                                            other_reference,
                                                            None,
                                                            indent,
                                                            no_doxy_comment_constructor,
                                                            None,
                                                            copy_constructor_postfix))

        if not no_doxy_comment_constructor:
            code_text.append("\n")      #whitespace for readability

        # Declare default move constructor
        code_text.extend(self._declare_function_with_decorations(class_name,
                                                            "Move constructor for a new "+class_name+" object",
                                                            other_move,
                                                            None,
                                                            indent,
                                                            no_doxy_comment_constructor,
                                                            None,
                                                            copy_constructor_postfix))

        if not no_doxy_comment_constructor:
            code_text.append("\n")      #whitespace for readability

        # Declare default equate constructor
        code_text.extend(self._declare_function_with_decorations("operator=",
                                                            "Equate constructor for a new "+class_name+" object",
                                                            other_reference,
                                                            equate_return,
                                                            indent,
                                                            no_doxy_comment_constructor,
                                                            None,
                                                            copy_constructor_postfix))

        if not no_doxy_comment_constructor:
            code_text.append("\n")      #whitespace for readability

        # Declare default equate move constructor
        code_text.extend(self._declare_function_with_decorations("operator=",
                                                            "Equate move constructor for a new "+class_name+" object",
                                                            other_move,
                                                            equate_return,
                                                            indent,
                                                            no_doxy_comment_constructor,
                                                            None,
                                                            copy_constructor_postfix))

        if not no_doxy_comment_constructor:
            code_text.append("\n")      #whitespace for readability

        # Declare default destructor
        code_text.extend(self._declare_function_with_decorations("~"+class_name,
                                                            "Destructor for "+class_name+" object",
                                                            [],
                                                            None,
                                                            indent,
                                                            no_doxy_comment_constructor,
                                                            destructor_prefix,
                                                            "= default"))
        code_text.append("\n")      #whitespace for readability
        return code_text

    def _declare_structure(self, name:str, var_dist_list:list, indent:int=0,
                          struct_desc:str = None,
                          prefix_decoration:str = None,
                          postfix_decoration:str = None)->list:
        """!
        @brief Generate a structure declaration

        @param name {string} Name of the structure
        @param var_dist_list {list} List of ParamRetDict parameter dictionaries for the data elements
        @param indent {integer} Number of spaces to indent the code declarations, default = 0
        @param struct_desc {string} Doxygen structure description
        @param prefix_decoration {str} Structure definition prefix decorations
        @param postfix_decoration {str} Structure definition end decorations

        @return list of strings - Code to output
        """
        code_text = []
        decl_indent = "".rjust(indent, ' ')
        body_indent = "".rjust(indent+self.level_tab_size, ' ')

        # Generate the doxygen comment
        code_text.extend(self.doxy_comment_gen.gen_doxy_class_comment(struct_desc, None, indent))

        # Generate the structure
        if prefix_decoration is not None:
            code_text.append(decl_indent+prefix_decoration+" structure "+name+"\n")
        else:
            code_text.append(decl_indent+"structure "+name+"\n")
        code_text.append(decl_indent+"{\n")

        # Generate the body code
        for var_dict in var_dist_list:
            code_text.append(body_indent+self._declare_var_statment(var_dict, 60-self.level_tab_size))

        # Close the struture
        if postfix_decoration is not None:
            code_text.append(decl_indent+"} "+postfix_decoration+";\n")
        else:
            code_text.append(decl_indent+"};\n")
        return code_text

    def _declare_var_statment(self, var_dict:dict, doxy_comment_indent:int = -1)->str:
        """!
        @brief Declare a class/interface variable
        @param var_dict {dict} ParamRetDict parameter dictionary describing the variable
        @param doxy_comment_indent {int} Column to begin the doxygen comment
        @return string Variable declatation code
        """
        # Declare the variable
        type_name = ParamRetDict.get_param_type(var_dict)
        type_mod = ParamRetDict.get_param_type_mod(var_dict)
        var_type_decl = self._declare_type(type_name, type_mod)
        var_decl = var_type_decl+" "+ParamRetDict.get_param_name(var_dict)+";"

        # Test for doxycomment skip
        if doxy_comment_indent != -1:
            if doxy_comment_indent > len(var_decl):
                var_decl = var_decl.ljust(doxy_comment_indent, ' ')
            else:
                var_decl+= " "
            var_decl += self.doxy_comment_gen.gen_doxy_var_doc_str(ParamRetDict.get_param_desc(var_dict))

        # Return the final data
        return var_decl+"\n"

    def _gen_add_list_statment(self, list_name:str, value_name:str, is_text:bool=False)->str:
        """!
        @brief Generate a list add code statement
        @param list_name {string} Name of the list variable to add the value_name to
        @param value_name {string} Name of the value to add to the list object
        @param is_text {boolean} False if value_name is a variable name or numeric value,
                                True if value_name is a text string
                                default = False
        @return string - CPP code text
        """
        if is_text:
            return list_name+".emplace_back(\""+value_name+"\");"
        else:
            return list_name+".emplace_back("+value_name+");"

    def _gen_return_statment(self, ret_value:str, is_text:bool=False)->str:
        """!
        @brief Generate a list add code statement
        @param ret_value {string} Name of the return variable
        @param is_text {boolean} False if ret_value is a variable name or numeric value,
                                True if ret_value is a text string
                                default = False
        @return string - CPP code text
        """
        if is_text:
            return "return \""+ret_value+"\";"
        else:
            return "return "+ret_value+";"
