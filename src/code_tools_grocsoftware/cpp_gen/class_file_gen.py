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
    def __init__(self, languageList:LanguageDescriptionList, classStrings:StringClassDescription,
                 owner:str|None = None, eulaName:str|None = None):
        """!
        @brief GenerateBaseLangFile constructor

        @param languageList {StringClassDescription} JSON language list object
        @param classStrings {LanguageDescriptionList} JSON property/translate string
                                                      object to use
        @param owner {string|None} Owner name to use in the copyright header message or
                                   None to use tool name
        @param eulaName {string|None} EULA text to use in the header message or
                                      None to default MIT Open
        """
        super().__init__(owner, eulaName, classStrings.get_base_class_name(),
                         classStrings.get_dynamic_compile_switch())

        self.version = {'Major': 1,
                        'Minor': 0,
                        'Patch': 0}

        self.jsonLangData = languageList
        self.jsonStringsData = classStrings

        self.osLangSelectList = [LinuxLangSelectFunctionGenerator(self.jsonLangData,
                                                                  owner,
                                                                  eulaName,
                                                                  classStrings.get_base_class_name(),
                                                                  classStrings.get_dynamic_compile_switch()),
                                 WindowsLangSelectFunctionGenerator(self.jsonLangData,
                                                                    owner,
                                                                    eulaName,
                                                                    classStrings.get_base_class_name(),
                                                                    classStrings.get_dynamic_compile_switch())
                                 # Add additional OS lang select classes here
                                 ]

        self.masterFunctionName = classStrings.get_base_selection_name()
        self.nameSpaceName = classStrings.get_namespace_name()
        self.masterFunction = MasterSelectFunctionGenerator(owner,
                                                            eulaName,
                                                            classStrings.getBaseClassName(),
                                                            self.masterFunctionName,
                                                            classStrings.getDynamicCompileSwitch())

        self.fnames = {}
        self.inc_subdirs = []

        self.testParamValues = {'keyString': ("--myKey", True),
                                'envKeyString': ("MY_ENV_KEY", True),
                                'jsonKeyString': ("jsonkey:", True),
                                'xmlKeyString': ("<xmlkey>", True),
                                'nargs': ("3", False),
                                'nargsExpected': ("2", False),
                                'nargsFound': ("1", False),
                                'vargRange': ("<-100:100>", True),
                                'vargType': ("integer", True),
                                'valueString': ("23", True)
                                }

        self.mockClassName = "mock_"+self.jsonStringsData.getBaseClassName()



    def add_inculde_dir(self, subdir_name:str):
        """!
        @brief Add subdir name to the include dir list
        @param subdir_name {string} Subdirectory name
        """
        self.inc_subdirs.append(subdir_name)

    def _add_file(self, language_name:str, file_type:str, file_name:str):
        """!
        @brief Add File to the list of files
        @param language_name {string} Language name or None for base files
        @param file_type {string} Type 'include' | 'source' | 'mockInclude'
                                       | 'mockSource | 'unittest'
        """
        if language_name is None:
            language_name = 'base'

        if language_name in self.fnames:
            self.fnames[language_name][file_type] = file_name
        else:
            self.fnames[language_name] = {}
            self.fnames[language_name][file_type] = file_name

    def get_include_fnames(self)->list:
        """!
        @brief Generate a list of include file names
        @return list - list of generated include file names
        """
        file_list = []
        for _, file_dict in self.fnames.items():
            file_list.append(file_dict['include'])
        return file_list

    def get_include_dirs(self)->list:
        """!
        @brief Get the include subdirectory list
        @return list - List of include subdirectory strings that were added
                       using the add_inculde_dir method
        """
        return self.inc_subdirs

    def get_source_fnames(self)->list:
        """!
        @brief Generate a list of source file names
        @return list - list of generated source file names
        """
        file_list = []
        for _, file_dict in self.fnames.items():
            file_list.append(file_dict['source'])
        return file_list

    def get_unittest_set_names(self)->list:
        """!
        @brief Generate a list of source file names
        @return list - list of unittest source, unittest file names
        """
        unittestSets = []
        language_list = self.jsonLangData.get_language_list()
        for language_name in language_list:
            unittest_target = self.gen_unittest_target_name(language_name)
            unittestSets.append((language_name,
                                 self.fnames[language_name]['source'],
                                 self.fnames[language_name]['unittest'],
                                 unittest_target))

        return unittestSets

    def _get_param_test_value(self, param_name:str)->str:
        """!
        @brief Return the parameter test value
        @param param_name (string) Name fot the value
        @return string - Test value
        """
        if param_name in self.testParamValues:
            value, is_text = self.testParamValues[param_name]
            if is_text:
                return "\""+value+"\""
            else:
                return value
        else:
            return "42"

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
            data_list = self.jsonLangData.getLanguagePropertyData(lang_name, property_name)

            # Determine data type
            for data_item in data_list:
                code_text.append(self.gen_add_list_statment("returnData", data_item, is_text))
            code_text.append("return returnData;")
        else:
            # Single item case
            data_item = self.jsonLangData.get_property_data(lang_name, property_name)
            code_text.append(self.gen_return_statment(data_item, is_text))

        return code_text

    def write_inc_property_methods(self, hfile, base:bool = False):
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

        method_list = self.jsonStringsData.get_property_method_list()
        for method_name in method_list:
            _, desc, params, ret = self.jsonStringsData.get_property_method_data(method_name)
            if len(params) == 0:
                postfix = "const "+base_postfix
            else:
                postfix = base_postfix

            # Output final declaration
            hfile.writelines(self.write_method(method_name,
                                               desc,
                                               params,
                                               ret,
                                               prefix,
                                               postfix,
                                               skipdox))
            if not skipdox:
                hfile.writelines(["\n"]) # whitespace for readability

    def write_src_property_methods(self, cppfile, lang_name:str, class_name:str):
        """!
        @brief Write the property method sourc file definitios

        @param hfile {File} File to write the data to
        @param lang_name {string} Language name or None this is for the base file
        @param class_name {string} Class name decoration
        """
        skipdox = bool(lang_name is None)
        method_list = self.jsonStringsData.get_property_method_list()
        for method in method_list:
            name, desc, params, ret = self.jsonStringsData.get_property_method_data(method)

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
                                                               skipdox,
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
        stream_str += "; return parserstr.str();"
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

        method_list = self.jsonStringsData.get_tranlate_method_list()
        for method_name in method_list:
            desc, params, ret = self.jsonStringsData.get_tranlate_method_function_data(method_name)

            hfile.writelines(self.write_method(method_name,
                                               desc,
                                               params,
                                               ret,
                                               prefix,
                                               postfix,
                                               skipdox))
            if not skipdox:
                hfile.writelines(["\n"]) # whitespace for readability

    def _write_src_translate_methods(self, cppfile, lang_name:str, class_name:str):
        """!
        @brief Write the property method definitions

        @param cppfile {File} File to write the data to
        @param lang_name {string} Language name or None this is for the base file
        @param class_name {string} Class name decoration
        """
        skipdox = bool(lang_name is None)

        methods = self.jsonStringsData.get_tranlate_method_list()
        for name in methods:
            desc, params, ret = self.jsonStringsData.get_tranlate_method_function_data(name)

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
            target_lang = self.jsonLangData.get_iso_code_data(lang_name)

            # Get the language data replacements
            stream_data = self.jsonStringsData.get_tranlate_method_text_data(name, target_lang)
            code_text = self._gen_stream_code(stream_data)

            # Output code body
            cppfile.writelines(["{"+code_text+"}\n"])

    def write_inc_file(self, hfile, lang_name:str, group_name:str = None, group_desc:str = None):
        """!
        @brief Write the language specific include file

        @param hfile {File} File to write the data to
        @param lang_name {string} - Language name
        @param group_name {string} - Doxygen group name for the project
        @param group_desc {string} - Doxygen group description for the project
        """
        # Set the class name and description
        decl_indent = self.level_tab_size*2
        class_name = self.jsonStringsData.get_language_class_name(lang_name)
        if lang_name is None:
            class_desc = "Parser error/help string generation interface"
            inheritence = None
            class_decoration = None
            skipdoxy = True
            nocopy = False
        else:
            class_desc = "Language specific parser error/help string generation interface"
            inheritence = "public "+self.jsonStringsData.get_base_class_name()
            class_decoration = "final"
            skipdoxy = False
            nocopy = True

        # Write the common header
        hfile.writelines(self._generate_file_header())
        hfile.writelines(["\n"]) # whitespace for readability

        # Write the include block
        if lang_name is None:
            # Base includes
            include_list = ["<cstddef>", "<cstdlib>", "<memory>", "<string>"]
            filename = self.jsonStringsData.get_base_class_name()+".h"
        else:
            # Language specific includes
            include_list = [self.jsonStringsData.get_base_class_name()+".h"]
            filename = self.jsonStringsData.get_language_class_name(lang_name)+".h"

        hfile.writelines(self.gen_include_block(include_list))
        hfile.writelines(["\n"]) # whitespace for readability

        if group_name is not None:
            hfile.writelines(self.doxy_comment_gen.gen_doxy_defgroup(filename,
                                                                     group_name,
                                                                     group_desc))

        # Class definition
        hfile.writelines(["#pragma once\n"])
        hfile.writelines(self.gen_namespace_open(self.nameSpaceName))
        hfile.writelines(["\n"]) # whitespace for readability

        # Start class definition
        hfile.writelines(self.gen_class_open(class_name, class_desc, inheritence, class_decoration))
        indent = "".rjust(self.level_tab_size, "")
        hfile.writelines([indent+"public:\n"])

        # Add default Constructor/destructor definitions
        hfile.writelines(self.gen_class_default_constructor_destructor(class_name,
                                                                       decl_indent,
                                                                       skipdoxy,
                                                                       nocopy))

        # Add the property fetch methods
        self.write_inc_property_methods(hfile)
        hfile.writelines(["\n"]) # whitespace for readability

        # Add the string generation methods
        self._write_inc_translate_methods(hfile)

        if lang_name is None:
            # Add the static generation function declaration
            sname, sdesc, sret, sparams = self.masterFunction.get_function_desc()
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
        hfile.writelines(self.gen_namespace_close(self.nameSpaceName))

        if group_name is not None:
            # Complete the doxygen group
            hfile.writelines(self.doxy_comment_gen.gen_doxy_group_end())
