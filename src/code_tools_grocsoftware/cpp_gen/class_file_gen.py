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
from code_tools_grocsoftware.base.project_json import ProjectDescription

from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList
from code_tools_grocsoftware.base.json_string_class_description import StringClassDescription
from code_tools_grocsoftware.base.translate_text_parser import TransTxtParser

from code_tools_grocsoftware.cpp_gen.string_class_tools import BaseCppStringClassGenerator

from code_tools_grocsoftware.cpp_gen.master_lang_select import MasterSelectFunctionGenerator
from code_tools_grocsoftware.cpp_gen.linux_lang_select import LinuxLangSelectFunctionGenerator
from code_tools_grocsoftware.cpp_gen.windows_lang_select import WindowsLangSelectFunctionGenerator
# Add additional OS lang select classes here

class GenerateLangFiles(BaseCppStringClassGenerator):
    """!
    Class takes the LanguageDescriptionList JSON data and StringClassDescription JSON
    data and generates the base and language specific source, include, mock and unittest
    files.
    """
    def __init__(self, project_data:ProjectDescription):
        """!
        @brief GenerateBaseLangFile constructor

        @param project_data {ProjectDescription} JSON project data object
        """
        ## Json project data object
        self.project_data = project_data
        ## Json language data list object
        self.json_lang_data:LanguageDescriptionList = project_data.get_lang_data()
        ## Json string class description object
        self.json_str_data:StringClassDescription = project_data.get_string_data()

        super().__init__(self.json_str_data.get_base_class_name(),
                         self.json_str_data.get_dynamic_compile_switch(),
                         self.project_data.get_version())

        ## OS specific language selection function generator list
        self.os_lang_sel_list = [LinuxLangSelectFunctionGenerator(self.project_data),
                                 WindowsLangSelectFunctionGenerator(self.project_data)
                                 # Add additional OS lang select classes here
                                 ]

        ## Master language selection function name
        self.master_function_name = self.json_str_data.get_base_selection_name()
        ## Name space name
        self.namespace_name = self.json_str_data.get_namespace_name()
        ## Master language selection function generator
        self.master_func_gen = MasterSelectFunctionGenerator(self.project_data,
                                                             self.master_function_name)

        ## Parameter test value dictionary
        #  {param_name: (value, is_text)}
        #  is_text is True if the value is a text string and should be quoted
        #  when used in the test code
        self.test_param_values = {}

        # Update the translation matrix
        uselist = []
        if project_data.get_include_using() is not None:
            uselist.extend(project_data.get_include_using())
        if project_data.get_base_src_using() is not None:
            uselist.extend(project_data.get_base_src_using())
        if project_data.get_lang_src_using() is not None:
            uselist.extend(project_data.get_lang_src_using())

        for entry in uselist:
            self.update_xlate_name(entry['stdName'], entry['localName'])

    def get_os_lang_sel_list(self)->list:
        """!
        @brief Return the os selector list
        @return list - os selection generation class list
        """
        return self.os_lang_sel_list

    def _get_param_test_value(self, param_name:str)->str:
        """!
        @brief Return the parameter test value
        @param param_name (string) Name fot the value
        @return string - Test value
        """
        if param_name in self.test_param_values:
            value, is_text = self.test_param_values[param_name]
            if is_text:
                retstr = "\""+value+"\""
            else:
                retstr = value
        else:
            retstr = "42"
        return retstr

    def _gen_property_code(self, lang_name:str, property_name:str, property_return:dict)->list:
        """!
        @brief Generate property function code
        @param lang_name {string} Language name
        @param property_name {string} Language property name
        @param property_return {dictionary} Property method return dictionary
        @return list of strings - Inline code
        """
        is_text = LanguageDescriptionList.is_property_text(property_name)
        code_text = []

        if ParamRetDict.is_return_list(property_return):
            # List case
            code_text.append(self.gen_function_ret_type(property_return)+"returnData;")
            data_list = self.json_lang_data.get_property_data(lang_name, property_name)

            # Determine data type
            for data_item in data_list:
                code_text.append(self.gen_add_list_statment("returnData", str(data_item), is_text))
            code_text.append("return returnData;")
        else:
            # Single item case
            data_item = self.json_lang_data.get_property_data(lang_name, property_name)
            code_text.append(self.gen_return_statment(str(data_item), is_text))

        return code_text

    def _write_inc_property_methods(self, hfile, base:bool = False):
        """!
        @brief Write the property method definitions

        @param hfile {File} File to write the data to
        @param base {boolean} True if this is for the base class,
                              False if this is for a language specific class.
        """
        # Add the property fetch methods
        if base:
            base_postfix = "= 0"
            prefix = '[[nodiscard]] virtual'
            skipdox = False
        else:
            base_postfix = "final"
            prefix = None
            skipdox = True

        method_list = self.json_str_data.get_property_method_list()
        for method_name in method_list:
            _, desc, params, ret = self.json_str_data.get_property_method_data(method_name)

            # Output final declaration
            hfile.writelines(self.write_method(method_name,
                                               desc,
                                               params,
                                               ret,
                                               prefix,
                                               base_postfix,
                                               skipdox))
            if not skipdox:
                hfile.writelines(["\n"]) # whitespace for readability

    def _write_src_property_methods(self, cppfile, lang_name:str):
        """!
        @brief Write the property method sourc file definitios

        @param hfile {File} File to write the data to
        @param lang_name {string} Language name or None this is for the base file
        """
        if lang_name is not None:
            class_name = self.json_str_data.get_language_class_name(lang_name)

            method_list = self.json_str_data.get_property_method_list()
            for method in method_list:
                name, desc, params, ret = self.json_str_data.get_property_method_data(method)

                # Translate the return type
                if len(params) == 0:
                    postfix = "const"
                else:
                    postfix = None

                # Output final declaration
                method_def = self.define_function_with_decorations(class_name+"::"+method,
                                                                   desc,
                                                                   params,
                                                                   ret,
                                                                   True,
                                                                   None,
                                                                   postfix)
                cppfile.writelines(method_def)

                # Get the language data replacements
                code_text = self._gen_property_code(lang_name, name, ret)

                # Output code body
                if len(code_text) == 1:
                    cppfile.writelines(["{"+code_text[0]+"}\n"])
                else:
                    body_indent = "".rjust(self.level_tab_size, ' ')
                    cppfile.writelines(["{\n"])
                    for line in code_text:
                        cppfile.writelines([body_indent+line+"\n"])
                    cppfile.writelines(["}\n"])

    def _gen_stream_code(self, stream_data:list)->str:
        """!
        @brief Generate the string output code
        @param stream_data {tuple list} Stream output tuple list
        @return string - Inline code
        """
        stream_name = "parserstr"
        stream_str = self.type_xlation_dict['strstream']+" "+stream_name+"; "
        stream_str += stream_name
        stream_str += TransTxtParser.assemble_stream(stream_data, "<<")
        stream_str += "; return "+stream_name+".str();"
        return stream_str

    def _write_inc_translate_methods(self, hfile, base:bool=False):
        """!
        @brief Write the property method definitions

        @param hfile {File} File to write the data to
        @param base {boolean} True if this is for the base class,
                              False if this is for a language specific class.
        """
        # Add the tranlate strings methods
        if base:
            postfix = "= 0"
            prefix = '[[nodiscard]] virtual'
            skipdox = False
        else:
            prefix = None
            postfix = "final"
            skipdox = True

        method_list = self.json_str_data.get_tranlate_method_list()
        for method_name in method_list:
            desc, params, ret = self.json_str_data.get_tranlate_method_function_data(method_name)

            hfile.writelines(self.write_method(method_name,
                                               desc,
                                               params,
                                               ret,
                                               prefix,
                                               postfix,
                                               skipdox))
            if not skipdox:
                hfile.writelines(["\n"]) # whitespace for readability

    def _write_src_translate_methods(self, cppfile, lang_name:str = None):
        """!
        @brief Write the property method definitions

        @param cppfile {File} File to write the data to
        @param lang_name {string} Language name or None this is for the base file
        """
        skipdox = bool(lang_name is None)
        class_name = self.json_str_data.get_language_class_name(lang_name)

        methods = self.json_str_data.get_tranlate_method_list()
        for name in methods:
            desc, params, ret = self.json_str_data.get_tranlate_method_function_data(name)

            # Translate the return type
            if len(params) == 0:
                postfix = "const"
            else:
                postfix = None

            # Output final declaration
            method_def = self.define_function_with_decorations(class_name+"::"+name,
                                                               desc,
                                                               params,
                                                               ret,
                                                               skipdox,
                                                               None,
                                                               postfix,
                                                               None)
            cppfile.writelines(method_def)

            # Get the language generation string if needed
            target_lang = self.json_lang_data.get_iso_code_data(lang_name)

            # Get the language data replacements
            stream_data = self.json_str_data.get_tranlate_method_text_data(name, target_lang)
            code_text = self._gen_stream_code(stream_data)

            # Output code body
            cppfile.writelines(["{"+code_text+"}\n"])

    def write_inc_file(self, hfile, lang_name:str = None):
        """!
        @brief Write the language specific include file

        @param hfile {File} File to write the data to
        @param lang_name {string} - Language name
        """
        # Set the class name and description
        decl_indent = self.level_tab_size*2
        class_name = self.json_str_data.get_language_class_name(lang_name)
        group_name = self.project_data.get_group_name()
        group_desc = self.project_data.get_group_desc()

        if lang_name is None:
            class_desc = "Parser error/help string generation interface"
            inheritence = None
            class_decoration = None
            skipdoxy = False
            virtual_destructor = True

        else:
            class_desc = "Language specific parser error/help string generation interface"
            inheritence = "public "+self.gen_h_fname()
            class_decoration = "final"
            skipdoxy = True
            virtual_destructor = False

        # Write the common header
        hfile.writelines(self._generate_file_header(self.project_data.get_eula(),
                                                    self.project_data.get_owner(),
                                                    self.project_data.get_creation_year()))
        hfile.writelines(["\n"]) # whitespace for readability

        # Write the include block
        if lang_name is None:
            # Base includes
            include_list = ["<cstddef>", "<cstdlib>", "<memory>", "<string>"]
            filename = self.gen_h_fname()
        else:
            # Language specific includes
            include_list = [self.gen_h_fname()]
            filename = self.gen_h_fname(lang_name)

        hfile.writelines(self.gen_include_block(include_list))
        hfile.writelines(["\n"]) # whitespace for readability

        if group_name is not None:
            hfile.writelines(self.doxy_comment_gen.gen_doxy_defgroup(filename,
                                                                     group_name,
                                                                     group_desc))
            hfile.writelines(["\n"]) # whitespace for readability

        # Class definition
        hfile.writelines(["#pragma once\n"])
        hfile.writelines(self.gen_namespace_open(self.namespace_name))
        hfile.writelines(["\n"]) # whitespace for readability

        # Add using statements
        if lang_name is None:
            using_list = self.project_data.get_include_using()
            if using_list is not None:
                using_code = []
                for using in using_list:
                    using_code.append(self.gen_using_statement(using['localName'],
                                                               using['stdName'],
                                                               using['desc']))
                hfile.writelines(using_code)
                hfile.writelines(["\n"]) # whitespace for readability

        # Start class definition
        hfile.writelines(self.gen_class_open(class_name, class_desc, inheritence, class_decoration))
        indent = "".rjust(self.level_tab_size, " ")
        hfile.writelines([indent+"public:\n"])

        # Add default Constructor/destructor definitions
        hfile.writelines(self.gen_class_default_constructor_destructor(class_name,
                                                                       decl_indent,
                                                                       virtual_destructor,
                                                                       not skipdoxy,
                                                                       False))

        # Add the property fetch methods
        self._write_inc_property_methods(hfile, bool(lang_name is None))
        hfile.writelines(["\n"]) # whitespace for readability

        # Add the string generation methods
        self._write_inc_translate_methods(hfile, bool(lang_name is None))

        if lang_name is None:
            # Add the static generation function declaration
            sname, sdesc, sret, sparams = self.master_func_gen.get_function_desc()
            sfunc = self.declare_function_with_decorations(sname,
                                                           sdesc,
                                                           sparams,
                                                           sret,
                                                           decl_indent,
                                                           False,
                                                           "static")
            hfile.writelines(sfunc)

        # Close the class
        hfile.writelines(self.gen_class_close(class_name))

        # Close the namespace
        hfile.writelines(["\n"]) # whitespace for readability
        hfile.writelines(self.gen_namespace_close(self.namespace_name))

        if group_name is not None:
            # Complete the doxygen group
            hfile.writelines(self.doxy_comment_gen.gen_doxy_group_end())

    def write_base_src_file(self, srcfile):
        """!
        @brief Write the language specific source file

        @param srcfile {File} File to write the data to
        """
        # Set the class name and description
        group_name = self.project_data.get_group_name()
        group_desc = self.project_data.get_group_desc()

        # Write the common header
        srcfile.writelines(self._generate_file_header(self.project_data.get_eula(),
                                                      self.project_data.get_owner(),
                                                      self.project_data.get_creation_year()))
        srcfile.writelines(["\n"]) # whitespace for readability

        # Write the include block
        include_list = [self.gen_h_fname()]
        lang_list = self.json_lang_data.get_language_list()
        for lang in lang_list:
            include_list.append(self.gen_h_fname(lang))

        srcfile.writelines(self.gen_include_block(include_list))
        srcfile.writelines(["\n"]) # whitespace for readability

        if group_name is not None:
            filename = self.gen_cpp_fname()
            srcfile.writelines(self.doxy_comment_gen.gen_doxy_defgroup(filename,
                                                                       group_name,
                                                                       group_desc))
            srcfile.writelines(["\n"]) # whitespace for readability

        # Set namespace
        srcfile.writelines(self.gen_using_namespace(self.namespace_name))
        srcfile.writelines(["\n"]) # whitespace for readability

        # Add using statements
        using_list = self.project_data.get_base_src_using()
        if using_list is not None:
            using_code = []
            for using in using_list:
                using_code.append(self.gen_using_statement(using['localName'],
                                                           using['stdName'],
                                                           using['desc']))
            srcfile.writelines(using_code)
            srcfile.writelines(["\n"]) # whitespace for readability

        for os_sel_gen in self.os_lang_sel_list:
            # Add the OS specific delection functions
            srcfile.writelines(os_sel_gen.gen_function())
            srcfile.writelines(["\n"]) # whitespace for readability

        # Add the master generation function declaration
        srcfile.writelines(self.master_func_gen.gen_function(self.os_lang_sel_list))
        srcfile.writelines(["\n"]) # whitespace for readability

        if group_name is not None:
            # Complete the doxygen group
            srcfile.writelines(self.doxy_comment_gen.gen_doxy_group_end())

    def write_lang_src_file(self, srcfile, lang_name:str):
        """!
        @brief Write the language specific source file

        @param hfile {File} File to write the data to
        @param lang_name {string} - Language name
        """
        # Set the class name and description
        group_name = self.project_data.get_group_name()
        group_desc = self.project_data.get_group_desc()

        # Write the common header
        srcfile.writelines(self._generate_file_header(self.project_data.get_eula(),
                                                      self.project_data.get_owner(),
                                                      self.project_data.get_creation_year()))
        srcfile.writelines(["\n"]) # whitespace for readability

        # Write the include block
        include_list = ["<sstream>",
                        self.gen_h_fname(lang_name)]

        srcfile.writelines(self.gen_include_block(include_list))
        srcfile.writelines(["\n"]) # whitespace for readability

        if group_name is not None:
            filename = self.gen_cpp_fname(lang_name)
            srcfile.writelines(self.doxy_comment_gen.gen_doxy_defgroup(filename,
                                                                       group_name,
                                                                       group_desc))
            srcfile.writelines(["\n"]) # whitespace for readability

        # Set namespace
        srcfile.writelines(self.gen_using_namespace(self.namespace_name))
        srcfile.writelines(["\n"]) # whitespace for readability

        # Add using statements
        using_list = self.project_data.get_lang_src_using()
        if using_list is not None:
            using_code = []
            for using in using_list:
                using_code.append(self.gen_using_statement(using['localName'],
                                                           using['stdName'],
                                                           using['desc']))
            srcfile.writelines(using_code)
            srcfile.writelines(["\n"]) # whitespace for readability

        # Add the property fetch methods
        self._write_src_property_methods(srcfile, lang_name)
        srcfile.writelines(["\n"]) # whitespace for readability

        # Add the string generation methods
        self._write_src_translate_methods(srcfile, lang_name)
        srcfile.writelines(["\n"]) # whitespace for readability

        if group_name is not None:
            # Complete the doxygen group
            srcfile.writelines(self.doxy_comment_gen.gen_doxy_group_end())

    def write_base_unittest_file(self, utfile):
        """!
        @brief Write the OS language selection CPP file
        @param utfile {File} File to write the data to
        """
        # Set the class name and description
        group_name = self.project_data.get_group_name()
        group_desc = self.project_data.get_group_desc()
        get_iso_name = self.json_str_data.get_iso_property_method_name()

        # Write the common header data
        utfile.writelines(self._generate_file_header(self.project_data.get_eula(),
                                                     self.project_data.get_owner(),
                                                     self.project_data.get_creation_year()))
        utfile.writelines(["\n"]) # whitespace for readability

        # Add the common includes
        include_list = ["<gtest/gtest.h>", self.gen_h_fname()]
        utfile.writelines(self.gen_include_block(include_list))
        utfile.writelines(["\n"]) # whitespace for readability

        # Add doxygen group start
        if group_name is not None:
            utfile.writelines(self.doxy_comment_gen.gen_doxy_defgroup(self.gen_unittest_fname(),
                                                                      group_name+'unittest',
                                                                      group_desc+'unit test'))

            utfile.writelines(["\n"]) # whitespace for readability

        # Add using namespace
        utfile.writelines(self.gen_using_namespace(self.namespace_name))

        # Add using statements
        using_list = self.project_data.get_base_src_using()
        if using_list is not None:
            using_code = []
            for using in using_list:
                using_code.append(self.gen_using_statement(using['localName'],
                                                           using['stdName'],
                                                           using['desc']))
            utfile.writelines(using_code)
            utfile.writelines(["\n"]) # whitespace for readability

        # Add the master selection function
        utfile.writelines(["\n"]) # whitespace for readability
        utfile.writelines(self.master_func_gen.gen_unit_test(get_iso_name, self.os_lang_sel_list))

        # Add the test main
        utfile.writelines(["\n"]) # whitespace for readability
        utfile.writelines(self.gen_unittest_main())

        # Complete the doxygen group
        if group_name is not None:
            utfile.writelines(["\n"]) # whitespace for readability
            utfile.writelines(self.doxy_comment_gen.gen_doxy_group_end())

    def write_selection_unittest_file(self, utfile, os_sel_gen):
        """!
        @brief Write the OS specific language selection CPP file
        @param utfile {File} File to write the data to
        """
        # Set the class name and description
        group_name = self.project_data.get_group_name()
        group_desc = self.project_data.get_group_desc()
        get_iso_name = self.json_str_data.get_iso_property_method_name()
        fname = os_sel_gen.get_unittest_file_name()

        # Write the common header data
        utfile.writelines(self._generate_file_header(self.project_data.get_eula(),
                                                     self.project_data.get_owner(),
                                                     self.project_data.get_creation_year()))
        utfile.writelines(["\n"]) # whitespace for readability

        # Add the common includes
        include_list = ["<gtest/gtest.h>", self.gen_h_fname()]
        utfile.writelines(self.gen_include_block(include_list))
        utfile.writelines(["\n"]) # whitespace for readability

        # Add doxygen group start
        if group_name is not None:
            utfile.writelines(self.doxy_comment_gen.gen_doxy_defgroup(fname,
                                                                      group_name+'unittest',
                                                                      group_desc+'unit test'))

            utfile.writelines(["\n"]) # whitespace for readability

        # Add using namespace
        utfile.writelines(self.gen_using_namespace(self.namespace_name))
        utfile.writelines(["\n"]) # whitespace for readability

        # Add using statements
        using_list = self.project_data.get_base_src_using()
        if using_list is not None:
            using_code = []
            for using in using_list:
                using_code.append(self.gen_using_statement(using['localName'],
                                                           using['stdName'],
                                                           using['desc']))
            utfile.writelines(using_code)
            utfile.writelines(["\n"]) # whitespace for readability

        # Add the language dependent selection functions
        utfile.writelines(os_sel_gen.gen_unit_test(get_iso_name))

        # Add the test main
        utfile.writelines(["\n"]) # whitespace for readability
        utfile.writelines(self.gen_unittest_main())

        # Complete the doxygen group
        if group_name is not None:
            utfile.writelines(["\n"]) # whitespace for readability
            utfile.writelines(self.doxy_comment_gen.gen_doxy_group_end())

    def _generate_property_unittest(self, method:str, langname:str)->list:
        """!
        @brief Generate the unit test for the input property method
        @param propertyMethod {string} Property function name
        @param langname {string} Language name
        @return list of strings - Test code to output
        """
        pname, _, pparams, pret = self.json_str_data.get_property_method_data(method)
        ut_section = self.json_str_data.get_language_class_name(langname)

        param_data = []
        for param in pparams:
            param_data.append(self._get_param_test_value(ParamRetDict.get_param_name(param)))

        # Build the test assertion expected data
        is_list = ParamRetDict.is_mod_list(ParamRetDict.get_return_type_mod(pret))
        if is_list:
            expected = []
            for item in self.json_lang_data.get_property_data(langname, pname):
                expected.append(item)
        else:
            expected = [self.json_lang_data.get_property_data(langname, pname)]

        return self.generate_property_unittest(method, ut_section, pret,
                                               expected, param_data,
                                               LanguageDescriptionList.is_property_text(pname))

    def _generate_translate_unittest(self, method:str, langname:str)->list:
        """!
        @brief Generate the unit test for the input property method
        @param method {string} Property function name
        @param langname {string} Language name
        @return list of strings - Test code to output
        """
        ut_section = self.json_str_data.get_language_class_name(langname)
        _, tparams, tret = self.json_str_data.get_tranlate_method_function_data(method)
        param_data = []
        for param in tparams:
            param_data.append(self._get_param_test_value(ParamRetDict.get_param_name(param)))

        # Build the expected string
        target_lang = self.json_lang_data.get_iso_code_data(langname)
        str_data = self.json_str_data.get_tranlate_method_text_data(method, target_lang)
        expected = TransTxtParser.assemble_test_return_string(str_data,
                                                              self.test_param_values)

        return self.generate_translate_unittest(method, ut_section, tret,
                                                expected, param_data)

    def write_lang_unittest_file(self, utfile, lang:str):
        """!
        @brief Write the OS specific language selection CPP file
        @param utfile {File} File to write the data to
        """
        # Set the class name and description
        group_name = self.project_data.get_group_name()
        group_desc = self.project_data.get_group_desc()
        fname = self.gen_unittest_fname(lang)

        # Write the common header data
        utfile.writelines(self._generate_file_header(self.project_data.get_eula(),
                                                     self.project_data.get_owner(),
                                                     self.project_data.get_creation_year()))
        utfile.writelines(["\n"]) # whitespace for readability

        # Add the common includes
        include_list = ["<gtest/gtest.h>",
                           self.gen_h_fname(),
                           self.gen_h_fname(lang)]
        utfile.writelines(self.gen_include_block(include_list))
        utfile.writelines(["\n"]) # whitespace for readability

        # Add doxygen group start
        if group_name is not None:
            utfile.writelines(self.doxy_comment_gen.gen_doxy_defgroup(fname,
                                                                      group_name+'unittest',
                                                                      group_desc+'unit test'))

            utfile.writelines(["\n"]) # whitespace for readability

        # Add using namespace
        utfile.writelines(self.gen_using_namespace(self.namespace_name))

        # Add using statements
        using_list = self.project_data.get_base_src_using()
        if using_list is not None:
            using_code = []
            for using in using_list:
                using_code.append(self.gen_using_statement(using['localName'],
                                                           using['stdName'],
                                                           using['desc']))
            utfile.writelines(using_code)
            utfile.writelines(["\n"]) # whitespace for readability

        # Add the property unittest methods
        method_list = self.json_str_data.get_property_method_list()
        for method_name in method_list:
            utfile.writelines(self._generate_property_unittest(method_name, lang))
            utfile.writelines(["\n"]) # whitespace for readability

        # Add the string generation methods
        method_list = self.json_str_data.get_tranlate_method_list()
        for method_name in method_list:
            utfile.writelines(self._generate_translate_unittest(method_name, lang))
            utfile.writelines(["\n"]) # whitespace for readability

        # Add the test main
        utfile.writelines(self.gen_unittest_main())

        # Complete the doxygen group
        if group_name is not None:
            utfile.writelines(["\n"]) # whitespace for readability
            utfile.writelines(self.doxy_comment_gen.gen_doxy_group_end())

    def write_mock_inc_file(self, mockfile):
        """!
        @brief Write the language specific include file

        @param hfile {File} File to write the data to
        """
        # Set the class name and description
        decl_indent = self.level_tab_size*2
        class_name = "mock_"+self.json_str_data.get_language_class_name()
        group_name = self.project_data.get_group_name()
        group_desc = self.project_data.get_group_desc()
        class_desc = "Mock Parser error/help string generation interface"
        inheritence = self.json_str_data.get_language_class_name()
        class_decoration = None
        skipdoxy = False
        virtual_destructor = True

        # Write the common header
        mockfile.writelines(self._generate_file_header(self.project_data.get_eula(),
                                                    self.project_data.get_owner(),
                                                    self.project_data.get_creation_year()))
        mockfile.writelines(["\n"]) # whitespace for readability

        # Write the include block
        include_list = ["<mock/gmock.h>", self.gen_h_fname()]
        filename = self.gen_mock_h_fname()

        mockfile.writelines(self.gen_include_block(include_list))
        mockfile.writelines(["\n"]) # whitespace for readability

        if group_name is not None:
            mockfile.writelines(self.doxy_comment_gen.gen_doxy_defgroup(filename,
                                                                     group_name,
                                                                     group_desc))
            mockfile.writelines(["\n"]) # whitespace for readability

        # Class definition
        mockfile.writelines(["#pragma once\n"])
        mockfile.writelines(self.gen_namespace_open(self.namespace_name))
        mockfile.writelines(["\n"]) # whitespace for readability

        # Start class definition
        mockfile.writelines(self.gen_class_open(class_name, class_desc, inheritence, class_decoration))
        indent = "".rjust(self.level_tab_size, " ")
        mockfile.writelines([indent+"public:\n"])

        # Add default Constructor/destructor definitions
        mockfile.writelines(self.gen_class_default_constructor_destructor(class_name,
                                                                       decl_indent,
                                                                       virtual_destructor,
                                                                       not skipdoxy,
                                                                       False))

        # Add the property unittest methods
        method_list = self.json_str_data.get_property_method_list()
        for method_name in method_list:
            _, _, params, ret = self.json_str_data.get_property_method_data(method_name)
            mockfile.writelines(self.write_mock_method(method_name, params,
                                                       ret, "final"))

        # Add the string generation methods
        method_list = self.json_str_data.get_tranlate_method_list()
        for method_name in method_list:
            _, params, ret = self.json_str_data.get_tranlate_method_function_data(method_name)
            mockfile.writelines(self.write_mock_method(method_name, params,
                                                       ret, "final"))
        # Close the class
        mockfile.writelines(self.gen_class_close(class_name))

        # Close the namespace
        mockfile.writelines(["\n"]) # whitespace for readability
        mockfile.writelines(self.gen_namespace_close(self.namespace_name))

        if group_name is not None:
            # Complete the doxygen group
            mockfile.writelines(self.doxy_comment_gen.gen_doxy_group_end())

    def write_mock_src_file(self, srcfile):
        """!
        @brief Write the mock source file

        @param srcfile {File} File to write the data to
        """
        # Set the class name and description
        group_name = self.project_data.get_group_name()
        group_desc = self.project_data.get_group_desc()
        class_name = "mock_"+self.json_str_data.get_language_class_name()

        # Write the common header
        srcfile.writelines(self._generate_file_header(self.project_data.get_eula(),
                                                      self.project_data.get_owner(),
                                                      self.project_data.get_creation_year()))
        srcfile.writelines(["\n"]) # whitespace for readability

        # Write the include block
        include_list = [self.gen_mock_h_fname()]
        lang_list = self.json_lang_data.get_language_list()
        for lang in lang_list:
            include_list.append(self.gen_h_fname(lang))

        srcfile.writelines(self.gen_include_block(include_list))
        srcfile.writelines(["\n"]) # whitespace for readability

        if group_name is not None:
            filename = self.gen_mock_cpp_fname()
            srcfile.writelines(self.doxy_comment_gen.gen_doxy_defgroup(filename,
                                                                       group_name,
                                                                       group_desc))
            srcfile.writelines(["\n"]) # whitespace for readability

        # Set namespace
        srcfile.writelines(self.gen_using_namespace(self.namespace_name))
        srcfile.writelines(["\n"]) # whitespace for readability

        # Add using statements
        using_code = []
        using_list = self.project_data.get_base_src_using()
        if using_list is not None:
            for using in using_list:
                using_code.append(self.gen_using_statement(using['localName'],
                                                           using['stdName'],
                                                           using['desc']))
        using_code.append("using ::testing::StrictMock;")
        using_code.append("using ::testing::Return;")
        using_code.append(self.gen_using_statement("stringMockptr",
                                                   "StrictMock<mock_ParserStringListInterface>*"))
        srcfile.writelines(using_code)
        srcfile.writelines(["\n"]) # whitespace for readability

        # Add the mock generation function declaration
        _, _, retdict, _ = self.master_func_gen.get_function_desc()
        body_indent = "".rjust(self.level_tab_size, " ")

        srcfile.writelines(self.master_func_gen.gen_function_define())
        ptr_code = self.gen_function_ret_type(retdict)
        ptr_code += " retPtr = std::make_shared< StrictMock<mock"
        ptr_code += class_name
        ptr_code += "> >();\n"
        srcfile.writelines([body_indent+ptr_code])
        extra = self.json_str_data.get_extra_mock()
        if extra:
            srcfile.writelines(["\n"]) # whitespace for readability
            srcfile.writelines(extra)
            srcfile.writelines(["\n"]) # whitespace for readability

        srcfile.writelines([body_indent+"return retPtr;\n"])
        srcfile.writelines([self.master_func_gen.gen_function_end()])
        srcfile.writelines(["\n"]) # whitespace for readability

        if group_name is not None:
            # Complete the doxygen group
            srcfile.writelines(self.doxy_comment_gen.gen_doxy_group_end())
