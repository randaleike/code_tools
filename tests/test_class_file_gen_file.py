# pylint: disable=protected-access

"""@package test_programmer_tools
Unittest for programmer base tools utility
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

import os
from unittest.mock import patch

from code_tools_grocsoftware.base.eula import EulaText
from code_tools_grocsoftware.cpp_gen.string_class_tools import BaseCppStringClassGenerator

from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList
from code_tools_grocsoftware.base.json_string_class_description import StringClassDescription
from code_tools_grocsoftware.base.project_json import ProjectDescription
from code_tools_grocsoftware.cpp_gen.class_file_gen import GenerateLangFiles

from tests.dir_init import TESTFILEPATH

langfilename = os.path.join(TESTFILEPATH, "teststringlanglist.json")
strclass_filename = os.path.join(TESTFILEPATH, "teststrdesc.json")

class MockEulaText():
    """!
    @brief Mock EulaText for testing
    """
    def format_eula_name(self):
        """!
        @brief Get the EULA name
        """
        return "Mock EULA"

    def format_eula_text(self):
        """!
        @brief Get the EULA text
        """
        return ["Mock EULA text"]


class MockProjectDescription(ProjectDescription):
    """!
    @brief Mock ProjectDescription for testing
    """
    def get_eula(self)->EulaText:
        """!
        @brief Get the EULA object from the JSON data
        @return (EulaText) - EULA object
        """
        return MockEulaText()

    def get_lang_data(self)-> LanguageDescriptionList:
        """!
        @brief Get the language description list from the JSON data
        @return (LanguageDescriptionList) - Language description list object
        """
        return LanguageDescriptionList(langfilename)

    def get_string_data(self)-> StringClassDescription:
        """!
        @brief Get the language description list from the JSON data
        @return (StringClassDescription) - String class description list object
        """
        return StringClassDescription(strclass_filename)

    def get_owner(self)->str:
        """!
        @brief Get the owner of the project
        @return (string) - Owner name
        """
        return "mock_owner"

    def get_base_selection_name(self):
        """!
        @brief Get the base selection name from the JSON data
        @return (string) - Base selection name
        """
        return "mockBaseSelection"

class MockFile:
    """!
    @brief Mock file object for testing
    """
    def __init__(self):
        self.mock_calls = []
        self.writedata = []

    def writelines(self, lines):
        """!
        @brief Mock writelines method
        """
        self.mock_calls.append(('writelines', ""))
        self.writedata.extend(lines)

def gen_inc_expected(class_gen:GenerateLangFiles, lang_name:str = None,
                     group_name:str = None, group_desc:str = None)->list:
    """!
    @brief Generate the expected inc file text
    @param class_gen class generator
    @param lang_name {string} Language name or None for base code
    @param group_name {string} doxygen group name or None for base code
    @param group_desc {string} doxygen description or None for base code
    """
    str_data = StringClassDescription(strclass_filename)
    class_name = str_data.get_language_class_name(lang_name)

    base = BaseCppStringClassGenerator("mock_owner", MockEulaText())

    if lang_name is None:
        include_list = ["<cstddef>", "<cstdlib>", "<memory>", "<string>"]
        class_desc = "Parser error/help string generation interface"
        inheritence = None
        class_decoration = None
        prefix = '[[nodiscard]] virtual'
        postfix = '= 0'
        skipdoxy = False
        virtual_destructor = True
    else:
        include_list = [str_data.get_base_class_name()+".h"]
        class_desc = "Language specific parser error/help string generation interface"
        inheritence = "public "+str_data.get_base_class_name()
        class_decoration = "final"
        prefix = None
        postfix = 'final'
        skipdoxy = True
        virtual_destructor = False

    expected = []
    expected.extend(class_gen._generate_file_header())
    expected.append("\n")
    expected.extend(base.gen_include_block(include_list))
    expected.append("\n")

    if group_name is not None:
        filename = str_data.get_language_class_name(lang_name)+".h"
        expected.extend(base.doxy_comment_gen.gen_doxy_defgroup(filename,
                                                                group_name,
                                                                group_desc))
        expected.append("\n")

    expected.append("#pragma once\n")
    expected.extend(base.gen_namespace_open(class_gen.namespace_name))
    expected.append("\n")

    if lang_name is None:
        using_list = class_gen.project_data.get_include_using()
        if using_list is not None:
            using_code = []
            for using in using_list:
                base.update_xlate_name(using['stdName'], using['localName'])
                using_code.append(base.gen_using_statement(using['localName'],
                                                            using['stdName'],
                                                            using['desc']))
            expected.extend(using_code)
            expected.append("\n") # whitespace for readability

    expected.extend(base.gen_class_open(class_name,
                                        class_desc,
                                        inheritence,
                                        class_decoration))
    indent = "".rjust(base.level_tab_size, " ")
    expected.append(indent+"public:\n")

    # Add default Constructor/destructor definitions
    expected.extend(base.gen_class_default_constructor_destructor(class_name,
                                                                  base.level_tab_size*2,
                                                                  virtual_destructor,
                                                                  not skipdoxy))

    prop_list = str_data.get_property_method_list()
    for methodname in prop_list:
        _, pdesc, pparams, pret = str_data.get_property_method_data(methodname)
        expected.extend(base.write_method(methodname,
                                        pdesc,
                                        pparams,
                                        pret,
                                        prefix,
                                        postfix,
                                        skipdoxy))
        if not skipdoxy:
            expected.append("\n")
    expected.append("\n")

    trans_list = str_data.get_tranlate_method_list()
    for methodname in trans_list:
        tdesc, tparams, tret = str_data.get_tranlate_method_function_data(methodname)

        expected.extend(base.write_method(methodname,
                                        tdesc,
                                        tparams,
                                        tret,
                                        prefix,
                                        postfix,
                                        skipdoxy))
        if not skipdoxy:
            expected.append("\n")

    if lang_name is None:
        sname, sdesc, sret, sparams = class_gen.master_func_gen.get_function_desc()
        sfunc = class_gen.declare_function_with_decorations(sname,
                                                        sdesc,
                                                        sparams,
                                                        sret,
                                                        base.level_tab_size*2,
                                                        skipdoxy,
                                                        "static")
        expected.extend(sfunc)

    expected.extend(base.gen_class_close(class_name))
    expected.append("\n")
    expected.extend(base.gen_namespace_close(class_gen.namespace_name))

    if group_name is not None:
        # Complete the doxygen group
        expected.extend(base.doxy_comment_gen.gen_doxy_group_end())

    return expected

def gen_base_src_expected(class_gen:GenerateLangFiles, group_name:str = None,
                          group_desc:str = None)->list:
    """!
    @brief Generate the expected base file text
    @param class_gen class generator
    @param group_name {string} doxygen group name or None for base code
    @param group_desc {string} doxygen description or None for base code
    """
    str_data = StringClassDescription(strclass_filename)
    base = BaseCppStringClassGenerator("mock_owner", MockEulaText())
    include_list = [str_data.get_language_class_name()+".h"]

    expected = []
    expected.extend(class_gen._generate_file_header())
    expected.append("\n")

    lang_list = class_gen.json_lang_data.get_language_list()
    for lang in lang_list:
        include_list.append(class_gen.json_str_data.get_language_class_name(lang)+".h")
    expected.extend(base.gen_include_block(include_list))
    expected.append("\n")

    if group_name is not None:
        filename = str_data.get_language_class_name()+".cpp"
        expected.extend(base.doxy_comment_gen.gen_doxy_defgroup(filename,
                                                                group_name,
                                                                group_desc))
        expected.append("\n")

    expected.extend(base.gen_using_namespace(class_gen.namespace_name))
    expected.append("\n")

    using_list = class_gen.project_data.get_base_src_using()
    if using_list is not None:
        using_code = []
        for using in using_list:
            base.update_xlate_name(using['stdName'], using['localName'])
            using_code.append(base.gen_using_statement(using['localName'],
                                                        using['stdName'],
                                                        using['desc']))
        expected.extend(using_code)
        expected.append("\n") # whitespace for readability

    for os_sel_gen in class_gen.os_lang_sel_list:
        # Add the OS specific delection functions
        expected.extend(os_sel_gen.gen_function())
        expected.append("\n")

    # Add the master generation function declaration
    expected.extend(class_gen.master_func_gen.gen_function(class_gen.os_lang_sel_list))
    expected.append("\n")

    if group_name is not None:
        # Complete the doxygen group
        expected.extend(base.doxy_comment_gen.gen_doxy_group_end())

    return expected

    str_data = StringClassDescription(strclass_filename)
def gen_property_code(class_gen:GenerateLangFiles,
                      str_data:StringClassDescription,
                      lang_name:str)->list:
    """!
    @brief Generate expected property code
    @param class_gen {GenerateLangFiles} class generator
    @param str_data {StringClassDescription} String description data
    @param lang_name {string} Language name
    @return list - Expected code strings
    """
    expected = []
    class_name = str_data.get_language_class_name(lang_name)
    method_list = str_data.get_property_method_list()
    for method in method_list:
        name, desc, params, ret = str_data.get_property_method_data(method)

        # Translate the return type
        if len(params) == 0:
            postfix = "const"
        else:
            postfix = None

        # Output final declaration
        method_def = class_gen.define_function_with_decorations(class_name+"::"+method,
                                                            desc,
                                                            params,
                                                            ret,
                                                            True,
                                                            None,
                                                            postfix)
        expected.extend(method_def)

        # Get the language data replacements
        code_text = class_gen._gen_property_code(lang_name, name, ret)

        # Output code body
        if len(code_text) == 1:
            expected.extend(["{"+code_text[0]+"}\n"])
        else:
            body_indent = "".rjust(class_gen.level_tab_size, ' ')
            expected.extend(["{\n"])
            for line in code_text:
                expected.extend([body_indent+line+"\n"])
            expected.extend(["}\n"])
    return expected

def gen_src_translate_methods(class_gen:GenerateLangFiles,
                              str_data:StringClassDescription,
                              lang_name:str)->list:
    """!
    @brief Generate the property method definitions
    @param class_gen {GenerateLangFiles} class generator
    @param str_data {StringClassDescription} String description data
    @param lang_name {string} Language name
    @return list - Expected code strings
    """
    expected = []
    skipdox = bool(lang_name is None)
    class_name = str_data.get_language_class_name(lang_name)

    methods = str_data.get_tranlate_method_list()
    for name in methods:
        desc, params, ret = str_data.get_tranlate_method_function_data(name)

        # Translate the return type
        if len(params) == 0:
            postfix = "const"
        else:
            postfix = None

        # Output final declaration
        method_def = class_gen.define_function_with_decorations(class_name+"::"+name,
                                                            desc,
                                                            params,
                                                            ret,
                                                            skipdox,
                                                            None,
                                                            postfix,
                                                            None)
        expected.extend(method_def)

        # Get the language generation string if needed
        target_lang = class_gen.json_lang_data.get_iso_code_data(lang_name)

        # Get the language data replacements
        stream_data = str_data.get_tranlate_method_text_data(name, target_lang)
        code_text = class_gen._gen_stream_code(stream_data)

        # Output code body
        expected.append("{"+code_text+"}\n")
    return expected

def gen_lang_src_expected(class_gen:GenerateLangFiles,
                          lang_name:str,
                          group_name:str = None,
                          group_desc:str = None)->list:
    """!
    @brief Generate the expected base file text
    @param class_gen {GenerateLangFiles} class generator
    @param lang_name {string} Language name or None for base code
    @param group_name {string} doxygen group name or None for base code
    @param group_desc {string} doxygen description or None for base code
    """
    str_data = StringClassDescription(strclass_filename)
    base = BaseCppStringClassGenerator("mock_owner", MockEulaText())
    include_list = ["<sstream>",
                    str_data.get_language_class_name(lang_name)+".h"]

    expected = []
    expected.extend(class_gen._generate_file_header())
    expected.append("\n")
    expected.extend(base.gen_include_block(include_list))
    expected.append("\n")

    if group_name is not None:
        filename = str_data.get_language_class_name(lang_name)+".cpp"
        expected.extend(base.doxy_comment_gen.gen_doxy_defgroup(filename,
                                                                group_name,
                                                                group_desc))
        expected.append("\n")

    expected.extend(base.gen_using_namespace(class_gen.namespace_name))
    expected.append("\n")

    using_list = class_gen.project_data.get_lang_src_using()
    if using_list is not None:
        using_code = []
        for using in using_list:
            base.update_xlate_name(using['stdName'], using['localName'])
            using_code.append(base.gen_using_statement(using['localName'],
                                                        using['stdName'],
                                                        using['desc']))
        expected.extend(using_code)
        expected.append("\n") # whitespace for readability

    # Add the property fetch methods
    expected.extend(gen_property_code(class_gen, str_data, lang_name))
    expected.append("\n")

    # Add the string generation methods
    expected.extend(gen_src_translate_methods(class_gen, str_data, lang_name))
    expected.append("\n")

    if group_name is not None:
        # Complete the doxygen group
        expected.extend(base.doxy_comment_gen.gen_doxy_group_end())

    return expected

def test001_write_inc_file():
    """!
    @brief Test write_inc_file, base, no group
    """
    mock_file = MockFile()
    class_gen = GenerateLangFiles(MockProjectDescription())
    class_gen.write_inc_file(mock_file)

    expected = gen_inc_expected(class_gen)
    assert len(mock_file.mock_calls) == 19
    assert len(mock_file.writedata) == len(expected)

    for i, line in enumerate(expected):
        assert mock_file.writedata[i] == line

def test002_write_inc_file_lang():
    """!
    @brief Test write_inc_file, base, no group
    """
    mock_file = MockFile()

    class_gen = GenerateLangFiles(MockProjectDescription())
    class_gen.write_inc_file(mock_file, "english")

    expected = gen_inc_expected(class_gen, "english")

    assert len(mock_file.mock_calls) == 16
    assert len(mock_file.writedata) == len(expected)

    for i, line in enumerate(expected):
        assert mock_file.writedata[i] == line

def test003_write_inc_file_with_group():
    """!
    @brief Test write_inc_file, base, no group
    """
    mock_file = MockFile()
    mock_gname = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_group_name'
    mock_gdesc = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_group_desc'

    with patch (mock_gname) as mock_group_name:
        mock_group_name.return_value = "TestGroup"
        with patch (mock_gdesc) as mock_group_desc:
            mock_group_desc.return_value = "Group desc"

            class_gen = GenerateLangFiles(MockProjectDescription())
            class_gen.write_inc_file(mock_file)

            expected = gen_inc_expected(class_gen, None, "TestGroup", "Group desc")
            assert len(mock_file.mock_calls) == 22
            assert len(mock_file.writedata) == len(expected)

            for i, line in enumerate(expected):
                assert mock_file.writedata[i] == line

def test004_write_inc_file_with_using():
    """!
    @brief Test write_inc_file, base, no group
    """
    mock_file = MockFile()
    mock_ginc = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_include_using'

    with patch (mock_ginc) as mock_get_inc:
        mock_get_inc.return_value = [{'localName':"parserstr", 'stdName':"std::string", 'desc':None}]
        class_gen = GenerateLangFiles(MockProjectDescription())
        class_gen.write_inc_file(mock_file)

        expected = gen_inc_expected(class_gen)
        assert len(mock_file.mock_calls) == 21
        assert len(mock_file.writedata) == len(expected)

        for i, line in enumerate(expected):
            assert mock_file.writedata[i] == line

def test011_write_base_src_file():
    """!
    @brief Test write_base_src_file, no group, no using
    """
    mock_file = MockFile()
    class_gen = GenerateLangFiles(MockProjectDescription())
    class_gen.write_base_src_file(mock_file)

    expected = gen_base_src_expected(class_gen)
    assert len(mock_file.mock_calls) == 12
    assert len(mock_file.writedata) == len(expected)

    for i, line in enumerate(expected):
        assert mock_file.writedata[i] == line

def test012_write_base_src_file_with_group():
    """!
    @brief Test write_base_src_file, with group, no using
    """
    mock_file = MockFile()
    mock_gname = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_group_name'
    mock_gdesc = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_group_desc'

    with patch (mock_gname) as mock_group_name:
        mock_group_name.return_value = "TestGroup"
        with patch (mock_gdesc) as mock_group_desc:
            mock_group_desc.return_value = "Group desc"

            class_gen = GenerateLangFiles(MockProjectDescription())
            class_gen.write_base_src_file(mock_file)

            expected = gen_base_src_expected(class_gen, "TestGroup", "Group desc")
            assert len(mock_file.mock_calls) == 15
            assert len(mock_file.writedata) == len(expected)

            for i, line in enumerate(expected):
                assert mock_file.writedata[i] == line

def test013_write_base_src_file_with_using():
    """!
    @brief Test write_base_src_file, with using, no group
    """
    mock_file = MockFile()
    mock_ginc = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_base_src_using'

    with patch (mock_ginc) as mock_get_inc:
        mock_get_inc.return_value = [{'localName':"parserstr", 'stdName':"std::string", 'desc':None}]

        class_gen = GenerateLangFiles(MockProjectDescription())
        class_gen.write_base_src_file(mock_file)

        expected = gen_base_src_expected(class_gen)
        assert len(mock_file.mock_calls) == 14
        assert len(mock_file.writedata) == len(expected)

        for i, line in enumerate(expected):
            assert mock_file.writedata[i] == line

def test021_write_lang_src_file():
    """!
    @brief Test write_lang_src_file, no group, no using
    """
    mock_file = MockFile()
    class_gen = GenerateLangFiles(MockProjectDescription())
    class_gen.write_lang_src_file(mock_file, "english")

    expected = gen_lang_src_expected(class_gen, "english")
    assert len(mock_file.mock_calls) == 12
    assert len(mock_file.writedata) == len(expected)

    for i, line in enumerate(expected):
        assert mock_file.writedata[i] == line

def test022_write_lang_src_file_with_group():
    """!
    @brief Test write_lang_src_file, with group, no using
    """
    mock_file = MockFile()
    mock_gname = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_group_name'
    mock_gdesc = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_group_desc'

    with patch (mock_gname) as mock_group_name:
        mock_group_name.return_value = "TestGroup"
        with patch (mock_gdesc) as mock_group_desc:
            mock_group_desc.return_value = "Group desc"

            class_gen = GenerateLangFiles(MockProjectDescription())
            class_gen.write_lang_src_file(mock_file, "english")

            expected = gen_lang_src_expected(class_gen, "english", "TestGroup", "Group desc")
            assert len(mock_file.mock_calls) == 15
            assert len(mock_file.writedata) == len(expected)

            for i, line in enumerate(expected):
                assert mock_file.writedata[i] == line

def test023_write_lang_src_file_with_using():
    """!
    @brief Test write_lang_src_file, no group, with using
    """
    mock_file = MockFile()
    mock_ginc = 'code_tools_grocsoftware.base.project_json.ProjectDescription.get_lang_src_using'

    with patch (mock_ginc) as mock_get_inc:
        mock_get_inc.return_value = [{'localName':"parserstr", 'stdName':"std::string", 'desc':None}]

        class_gen = GenerateLangFiles(MockProjectDescription())
        class_gen.write_lang_src_file(mock_file, "english")

        expected = gen_lang_src_expected(class_gen, "english")
        assert len(mock_file.mock_calls) == 14
        assert len(mock_file.writedata) == len(expected)

        for i, line in enumerate(expected):
            assert mock_file.writedata[i] == line

# pylint: enable=protected-access
