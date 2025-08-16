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

from code_tools_grocsoftware.base.param_return_tools import ParamRetDict
from code_tools_grocsoftware.base.translate_text_parser import TransTxtParser
from code_tools_grocsoftware.base.eula import EulaText
from code_tools_grocsoftware.cpp_gen.string_class_tools import BaseCppStringClassGenerator

from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList
from code_tools_grocsoftware.base.json_string_class_description import StringClassDescription
from code_tools_grocsoftware.base.project_json import ProjectDescription
from code_tools_grocsoftware.cpp_gen.class_file_gen import GenerateLangFiles
from code_tools_grocsoftware.cpp_gen.master_lang_select import MasterSelectFunctionGenerator

from tests.dir_init import TESTFILEPATH

langfilename = os.path.join(TESTFILEPATH, "teststringlanglist.json")
strclass_filename = os.path.join(TESTFILEPATH, "teststrdesc.json")

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

# pylint: disable=protected-access

def test001_class_constructor():
    """!
    @brief Test class constructor
    """
    class_gen = GenerateLangFiles(MockProjectDescription())
    assert isinstance(class_gen.project_data,  MockProjectDescription)
    assert isinstance(class_gen.json_lang_data, LanguageDescriptionList)
    assert isinstance(class_gen.json_str_data, StringClassDescription)
    assert isinstance(class_gen.os_lang_sel_list, list)
    assert len(class_gen.os_lang_sel_list) == 2

    assert class_gen.os_lang_sel_list[0] is not None
    assert class_gen.os_lang_sel_list[1] is not None
    #assert class_gen.os_lang_sel_list[0] == LinuxLangSelectFunctionGenerator
    #assert class_gen.os_lang_sel_list[1] == WindowsLangSelectFunctionGenerator

    assert class_gen.master_function_name == class_gen.json_str_data.get_base_selection_name()
    assert class_gen.namespace_name == class_gen.json_str_data.get_namespace_name()

    assert class_gen.master_func_gen is not None
    assert isinstance(class_gen.master_func_gen, MasterSelectFunctionGenerator)

    assert isinstance(class_gen.fnames, dict)
    assert not class_gen.fnames
    assert isinstance(class_gen.inc_subdirs, list)
    assert not class_gen.inc_subdirs

    assert isinstance(class_gen.test_param_values, dict)
    assert len(class_gen.test_param_values) == 0
    assert not class_gen.test_param_values

def test002_add_inculde_dir():
    """!
    @brief Test add_include_dir method
    """
    class_gen = GenerateLangFiles(MockProjectDescription())
    assert not class_gen.inc_subdirs

    class_gen.add_inculde_dir("test_dir")
    assert "test_dir" in class_gen.inc_subdirs
    assert len(class_gen.inc_subdirs) == 1

    class_gen.add_inculde_dir("test_dir2")
    assert "test_dir2" in class_gen.inc_subdirs
    assert len(class_gen.inc_subdirs) == 2

def test003_add_file():
    """!
    @brief Test _add_file method
    """
    class_gen = GenerateLangFiles(MockProjectDescription())
    assert not class_gen.fnames

    class_gen._add_file("english", "source", "test_file.cpp")
    assert len(class_gen.fnames['english']) == 1

    class_gen._add_file("english", "source", "test_file2.cpp")
    assert len(class_gen.fnames['english']) == 1

    class_gen._add_file("english", "include", "test_file.h")
    assert len(class_gen.fnames['english']) == 2

    class_gen._add_file(None, "include", "base_file.h")
    assert len(class_gen.fnames['base']) == 1

    class_gen._add_file(None, "source", "base_file.cpp")
    assert len(class_gen.fnames['base']) == 2

    class_gen._add_file(None, "mockInclude", "mock_file.h")
    assert len(class_gen.fnames['base']) == 3

    class_gen._add_file(None, "mockSource", "mock_file.cpp")
    assert len(class_gen.fnames['base']) == 4

    class_gen._add_file("spanish", "unittest", "test_file.cpp")
    assert len(class_gen.fnames['spanish']) == 1

    # Check if the file names are correctly stored
    assert class_gen.fnames['english']['source'] == "test_file2.cpp"
    assert class_gen.fnames['english']['include'] == "test_file.h"
    assert class_gen.fnames['base']['source'] == "base_file.cpp"
    assert class_gen.fnames['base']['include'] == "base_file.h"
    assert class_gen.fnames['base']['mockInclude'] == "mock_file.h"
    assert class_gen.fnames['base']['mockSource'] == "mock_file.cpp"
    assert class_gen.fnames['spanish']['unittest'] == "test_file.cpp"

def test004_get_include_dirs():
    """!
    @brief Test _add_file method with no language specified
    """
    class_gen = GenerateLangFiles(MockProjectDescription())
    assert not class_gen.inc_subdirs

    class_gen.add_inculde_dir("test_dir")
    class_gen.add_inculde_dir("test_dir2")

    inc_dirs = class_gen.get_include_dirs()
    assert isinstance(inc_dirs, list)
    assert len(inc_dirs) == 2

    assert "test_dir" in inc_dirs
    assert "test_dir2" in inc_dirs

def test005_get_include_fnames():
    """!
    @brief Test get_include_fnames method
    """
    class_gen = GenerateLangFiles(MockProjectDescription())

    class_gen._add_file("english", "source", "test_file.cpp")
    class_gen._add_file("english", "include", "test_file.h")
    class_gen._add_file(None, "include", "base_file.h")
    class_gen._add_file(None, "source", "base_file.cpp")
    class_gen._add_file(None, "mockInclude", "mock_file.h")
    class_gen._add_file(None, "mockSource", "mock_file.cpp")
    class_gen._add_file("spanish", "unittest", "test_file.cpp")

    tstlist = class_gen.get_include_fnames()
    assert isinstance(tstlist, list)
    assert len(tstlist) == 2

    assert "test_file.h" in tstlist
    assert "base_file.h" in tstlist

def test006_get_source_fnames():
    """!
    @brief Test get_include_fnames method
    """
    class_gen = GenerateLangFiles(MockProjectDescription())

    class_gen._add_file("english", "source", "test_file.cpp")
    class_gen._add_file("english", "include", "test_file.h")
    class_gen._add_file(None, "include", "base_file.h")
    class_gen._add_file(None, "source", "base_file.cpp")
    class_gen._add_file(None, "mockInclude", "mock_file.h")
    class_gen._add_file(None, "mockSource", "mock_file.cpp")
    class_gen._add_file("spanish", "unittest", "test_file.cpp")

    tstlist = class_gen.get_source_fnames()
    assert isinstance(tstlist, list)
    assert len(tstlist) == 2

    assert "test_file.cpp" in tstlist
    assert "base_file.cpp" in tstlist

def test007_get_mock_include_fnames():
    """!
    @brief Test get_mock_include_fnames method
    """
    class_gen = GenerateLangFiles(MockProjectDescription())

    class_gen._add_file("english", "source", "test_file.cpp")
    class_gen._add_file("english", "include", "test_file.h")
    class_gen._add_file(None, "include", "base_file.h")
    class_gen._add_file(None, "source", "base_file.cpp")
    class_gen._add_file(None, "mockInclude", "mock_file.h")
    class_gen._add_file(None, "mockSource", "mock_file.cpp")
    class_gen._add_file("spanish", "unittest", "test_file.cpp")

    tstlist = class_gen.get_mock_include_fnames()
    assert isinstance(tstlist, list)
    assert len(tstlist) == 1

    assert "mock_file.h" in tstlist

def test008_get_unittest_set_names():
    """!
    @brief Test get_unittest_set_names method
    """
    class_gen = GenerateLangFiles(MockProjectDescription())

    class_gen._add_file("english", "source", "en_test_file.cpp")
    class_gen._add_file("english", "include", "en_test_file.h")
    class_gen._add_file(None, "include", "base_file.h")
    class_gen._add_file(None, "source", "base_file.cpp")
    class_gen._add_file(None, "mockInclude", "mock_file.h")
    class_gen._add_file(None, "mockSource", "mock_file.cpp")
    class_gen._add_file("spanish", "source", "es_test_file.cpp")
    class_gen._add_file("spanish", "unittest", "es_unittest_file.cpp")

    tstlist = class_gen.get_unittest_set_names()
    assert isinstance(tstlist, list)
    assert len(tstlist) == 1

    assert tstlist[0] == ('spanish', 'es_test_file.cpp',
                          'es_unittest_file.cpp', 'ParserStringListInterfaceSpanish_test')

    # Check if the unittest set names are generated correctly
    class_gen._add_file("english", "unittest", "en_test_file_unittest.cpp")
    tstlist = class_gen.get_unittest_set_names()
    assert len(tstlist) == 2
    entuple = ('english', 'en_test_file.cpp',
               'en_test_file_unittest.cpp', 'ParserStringListInterfaceEnglish_test')
    estuple = ('spanish', 'es_test_file.cpp',
               'es_unittest_file.cpp', 'ParserStringListInterfaceSpanish_test')

    assert entuple in tstlist
    assert estuple in tstlist

def test009_get_unittest_set_names_no_source():
    """!
    @brief Test get_unittest_set_names method with no source file
    """
    class_gen = GenerateLangFiles(MockProjectDescription())

    class_gen._add_file("english", "unittest", "en_test_file_unittest.cpp")
    class_gen._add_file("spanish", "unittest", "es_unittest_file.cpp")

    tstlist = class_gen.get_unittest_set_names()
    assert isinstance(tstlist, list)
    assert len(tstlist) == 0

    # Check if the unittest set names are generated correctly
    class_gen._add_file("english", "source", "en_test_file.cpp")
    tstlist = class_gen.get_unittest_set_names()
    assert len(tstlist) == 1
    entuple = ('english', 'en_test_file.cpp',
               'en_test_file_unittest.cpp', 'ParserStringListInterfaceEnglish_test')
    assert entuple in tstlist

    # Check if the unittest set names are generated correctly with no unittest file
    class_gen._add_file("spanish", "source", "es_test_file.cpp")
    tstlist = class_gen.get_unittest_set_names()
    assert len(tstlist) == 2
    estuple = ('english', 'en_test_file.cpp',
               'en_test_file_unittest.cpp', 'ParserStringListInterfaceEnglish_test')
    assert estuple in tstlist
    assert entuple in tstlist

def test010_get_unittest_set_names_no_unittest():
    """!
    @brief Test get_unittest_set_names method with no unittest file
    """
    class_gen = GenerateLangFiles(MockProjectDescription())

    class_gen._add_file("english", "source", "en_test_file.cpp")
    class_gen._add_file("spanish", "source", "es_test_file.cpp")

    tstlist = class_gen.get_unittest_set_names()
    assert isinstance(tstlist, list)
    assert len(tstlist) == 0

    # Check if the unittest set names are generated correctly
    class_gen._add_file("english", "unittest", "en_test_file_unittest.cpp")
    tstlist = class_gen.get_unittest_set_names()
    assert len(tstlist) == 1
    entuple = ('english', 'en_test_file.cpp',
               'en_test_file_unittest.cpp', 'ParserStringListInterfaceEnglish_test')
    assert entuple in tstlist

    # Check if the unittest set names are generated correctly with no unittest file
    class_gen._add_file("spanish", "unittest", "es_unittest_file.cpp")
    tstlist = class_gen.get_unittest_set_names()
    assert len(tstlist) == 2
    estuple = ('spanish', 'es_test_file.cpp',
               'es_unittest_file.cpp', 'ParserStringListInterfaceSpanish_test')
    assert estuple in tstlist
    assert entuple in tstlist

def test011_get_param_test_value():
    """!
    @brief Test get_param_test_value method
    """
    class_gen = GenerateLangFiles(MockProjectDescription())

    # Check if the test parameter values are empty
    assert not class_gen.test_param_values

    # Add a test parameter value
    class_gen.test_param_values['test_param'] = ("test_value", False)
    class_gen.test_param_values['test_param1'] = ("test_value", True)

    assert class_gen._get_param_test_value('test_param') == "test_value"
    assert class_gen._get_param_test_value('test_param1') == "\"test_value\""
    assert class_gen._get_param_test_value('test_param2') == "42"  # Default value if not found

def test012_gen_property_code_nolist():
    """!
    @brief Test get_param_test_value method with no value
    """
    class_gen = GenerateLangFiles(MockProjectDescription())

    prop_type, peop_desc, islist = LanguageDescriptionList.get_property_return_data('isoCode')
    property_ret = ParamRetDict.build_return_dict(prop_type, peop_desc, islist)

    # Generate property code with a value
    code_text = class_gen._gen_property_code("english", "isoCode", property_ret)
    assert isinstance(code_text, list)
    assert len(code_text) == 1
    assert code_text[0] == 'return "en";'

def test013_gen_property_code_list():
    """!
    @brief Test get_param_test_value method with no value
    """
    prop_type, peop_desc, islist = LanguageDescriptionList.get_property_return_data('LANGID')
    property_ret = ParamRetDict.build_return_dict(prop_type, peop_desc, islist)

    lang_data = LanguageDescriptionList(langfilename)
    id_list = lang_data.get_property_data("english", "LANGID")

    class_gen = GenerateLangFiles(MockProjectDescription())

    # Generate property code with a value
    code_text = class_gen._gen_property_code("english", "LANGID", property_ret)
    assert isinstance(code_text, list)
    assert len(code_text) == 2 + len(id_list)
    assert code_text[0] == 'std::list<LANGID> returnData;'
    for i, item in enumerate(id_list):
        assert code_text[i + 1] == f'returnData.emplace_back({item});'
    assert code_text[-1] == 'return returnData;'

def test014_write_inc_property_methods():
    """!
    @brief Test _write_inc_property_methods method with text value
    """
    mock_file = MockFile()
    base = BaseCppStringClassGenerator()
    prop_type, prop_desc, _ = LanguageDescriptionList.get_property_return_data('isoCode')
    retdict = ParamRetDict.build_return_dict(prop_type, prop_desc)
    mock_prop_list = 'code_tools_grocsoftware.base.' \
                     'json_string_class_description.StringClassDescription' \
                     '.get_property_method_list'
    mock_get_prop = 'code_tools_grocsoftware.base.' \
                    'json_string_class_description.StringClassDescription' \
                    '.get_property_method_data'

    expected = []
    expected.extend(base.write_method("getLangIsoCode",
                                      "Get the "+prop_desc+" for this object",
                                      [],
                                      retdict,
                                      '[[nodiscard]] virtual',
                                      "= 0",
                                      False))
    expected.append("\n")

    with patch(mock_prop_list) as mock_method_list:
        mock_method_list.return_value = ["getLangIsoCode"]
        with patch(mock_get_prop) as mock_property:
            mock_property.return_value = ("isoCode", "Mock description", [], retdict)

        # Mock the project description to return the expected data
        class_gen = GenerateLangFiles(MockProjectDescription())

        class_gen._write_inc_property_methods(mock_file, True)

        assert len(mock_file.mock_calls) == 2
        assert len(mock_file.writedata) == len(expected)
        for i, line in enumerate(expected):
            assert mock_file.writedata[i] == line

def test015_write_inc_property_methods_lang():
    """!
    @brief Test _write_inc_property_methods method with text value
    """
    mock_file = MockFile()
    base = BaseCppStringClassGenerator()
    retdict = ParamRetDict.build_return_dict('string', 'mock return desc')

    mock_prop_list = 'code_tools_grocsoftware.base.' \
                     'json_string_class_description.StringClassDescription' \
                     '.get_property_method_list'
    mock_get_prop = 'code_tools_grocsoftware.base.' \
                    'json_string_class_description.StringClassDescription' \
                    '.get_property_method_data'

    expected = []
    expected.extend(base.write_method("getLangIsoCode",
                                    "Mock description",
                                    [],
                                    retdict,
                                    None,
                                    "final",
                                    True))

    with patch(mock_prop_list) as mock_method_list:
        mock_method_list.return_value = ["getLangIsoCode"]
        with patch(mock_get_prop) as mock_property:
            mock_property.return_value = ("isoCode", "Mock description", [], retdict)

            # Mock the project description to return the expected data
            class_gen = GenerateLangFiles(MockProjectDescription())

            class_gen._write_inc_property_methods(mock_file, False)

            assert len(mock_file.mock_calls) == 1
            assert len(mock_file.writedata) == len(expected)
            for i, line in enumerate(expected):
                assert mock_file.writedata[i] == line

def test016_write_inc_property_methods_with_params():
    """!
    @brief Test _write_inc_property_methods method with text value
    """
    mock_file = MockFile()
    base = BaseCppStringClassGenerator()
    param = ParamRetDict.build_param_dict('foo', 'integer', 'foo desc')
    retdict = ParamRetDict.build_return_dict('string', 'mock return desc')

    mock_prop_list = 'code_tools_grocsoftware.base.' \
                     'json_string_class_description.StringClassDescription' \
                     '.get_property_method_list'
    mock_get_prop = 'code_tools_grocsoftware.base.' \
                    'json_string_class_description.StringClassDescription' \
                    '.get_property_method_data'

    expected = []
    expected.extend(base.write_method("getLangIsoCode",
                                    "Mock description",
                                    [param],
                                    retdict,
                                    None,
                                    "final",
                                    True))

    with patch(mock_prop_list) as mock_method_list:
        mock_method_list.return_value = ["getLangIsoCode"]
        with patch(mock_get_prop) as mock_property:
            mock_property.return_value = ("isoCode", "Mock description", [param], retdict)

            # Mock the project description to return the expected data
            class_gen = GenerateLangFiles(MockProjectDescription())
            class_gen._write_inc_property_methods(mock_file, False)

            assert len(mock_file.mock_calls) == 1
            assert len(mock_file.writedata) == len(expected)
            for i, line in enumerate(expected):
                assert mock_file.writedata[i] == line

def test017_write_src_property_methods():
    """!
    @brief Test _write_src_property_methods method with text value
    """
    mock_file = MockFile()
    str_data = StringClassDescription(strclass_filename)
    class_name = str_data.get_language_class_name("english")

    prop_type, prop_desc, _ = LanguageDescriptionList.get_property_return_data('isoCode')
    retdict = ParamRetDict.build_return_dict(prop_type, prop_desc)
    mock_prop_list = 'code_tools_grocsoftware.base.' \
                     'json_string_class_description.StringClassDescription' \
                     '.get_property_method_list'
    mock_get_prop = 'code_tools_grocsoftware.base.' \
                    'json_string_class_description.StringClassDescription' \
                    '.get_property_method_data'

    base = BaseCppStringClassGenerator()
    expected = []
    expected.extend(base.define_function_with_decorations(class_name+"::getLangIsoCode",
                                      "Get the "+prop_desc+" for this object",
                                      [],
                                      retdict,
                                      True,
                                      None,
                                      "const"))
    expected.append("{return \"en\";}\n")

    with patch(mock_prop_list) as mock_method_list:
        mock_method_list.return_value = ["getLangIsoCode"]
        with patch(mock_get_prop) as mock_property:
            mock_property.return_value = ("isoCode", "Mock description", [], retdict)

        # Mock the project description to return the expected data
        class_gen = GenerateLangFiles(MockProjectDescription())

        class_gen._write_src_property_methods(mock_file, "english")

        assert len(mock_file.mock_calls) == 2
        assert len(mock_file.writedata) == len(expected)

        for i, line in enumerate(expected):
            assert mock_file.writedata[i] == line

def test018_write_src_property_methods_with_param():
    """!
    @brief Test _write_src_property_methods method with param
    """
    mock_file = MockFile()
    str_data = StringClassDescription(strclass_filename)
    class_name = str_data.get_language_class_name("spanish")

    prop_type, prop_desc, _ = LanguageDescriptionList.get_property_return_data('isoCode')
    retdict = ParamRetDict.build_return_dict(prop_type, prop_desc)
    param = ParamRetDict.build_param_dict('foo', 'integer', 'foo desc')

    mock_prop_list = 'code_tools_grocsoftware.base.' \
                     'json_string_class_description.StringClassDescription' \
                     '.get_property_method_list'
    mock_get_prop = 'code_tools_grocsoftware.base.' \
                    'json_string_class_description.StringClassDescription' \
                    '.get_property_method_data'

    base = BaseCppStringClassGenerator()
    expected = []
    expected.extend(base.define_function_with_decorations(class_name+"::getLangIsoCode",
                                      "Get the "+prop_desc+" for this object",
                                      [param],
                                      retdict,
                                      True,
                                      None,
                                      None))
    expected.append("{return \"es\";}\n")

    with patch(mock_prop_list) as mock_method_list:
        mock_method_list.return_value = ["getLangIsoCode"]
        with patch(mock_get_prop) as mock_property:
            mock_property.return_value = ("isoCode", prop_desc, [param], retdict)

            # Mock the project description to return the expected data
            class_gen = GenerateLangFiles(MockProjectDescription())
            class_gen._write_src_property_methods(mock_file, "spanish")

            assert len(mock_file.mock_calls) == 2
            assert len(mock_file.writedata) == len(expected)

            for i, line in enumerate(expected):
                assert mock_file.writedata[i] == line

def test019_write_src_property_methods_with_list():
    """!
    @brief Test _write_src_property_methods method with list return
    """
    mock_file = MockFile()
    str_data = StringClassDescription(strclass_filename)
    class_name = str_data.get_language_class_name("spanish")

    prop_type, prop_desc, _ = LanguageDescriptionList.get_property_return_data('LANGID')
    retdict = ParamRetDict.build_return_dict(prop_type, prop_desc, True)

    mock_prop_list = 'code_tools_grocsoftware.base.' \
                     'json_string_class_description.StringClassDescription' \
                     '.get_property_method_list'
    mock_get_prop = 'code_tools_grocsoftware.base.' \
                    'json_string_class_description.StringClassDescription' \
                    '.get_property_method_data'

    base = BaseCppStringClassGenerator()
    expected = []
    expected.extend(base.define_function_with_decorations(class_name+"::getLANGIDCode",
                                      "Get the "+prop_desc+" for this object",
                                      [],
                                      retdict,
                                      True,
                                      None,
                                      "const"))
    expected.append("{\n")

    with patch(mock_prop_list) as mock_method_list:
        mock_method_list.return_value = ["getLANGIDCode"]
        with patch(mock_get_prop) as mock_property:
            mock_property.return_value = ("LANGID", prop_desc, [], retdict)

            # Mock the project description to return the expected data
            class_gen = GenerateLangFiles(MockProjectDescription())
            class_gen._write_src_property_methods(mock_file, "spanish")

            code_text = class_gen._gen_property_code("spanish", "LANGID", retdict)
            for line in code_text:
                expected.append("    "+line+"\n")
            expected.append("}\n")

            assert len(mock_file.mock_calls) == 6
            assert len(mock_file.writedata) == len(expected)

            for i, line in enumerate(expected):
                assert mock_file.writedata[i] == line

def test020_gen_stream_code():
    """!
    @brief Test gen_stream_code method with text value
    """
    stream_data = TransTxtParser().parse_translate_string("Test string")
    class_gen = GenerateLangFiles(MockProjectDescription())

    expected = class_gen.type_xlation_dict['strstream']+" parserstr; "
    expected += "parserstr"
    expected += TransTxtParser.assemble_stream(stream_data, "<<")
    expected += "; return parserstr.str();"
    assert class_gen._gen_stream_code(stream_data) == expected

def test021_write_inc_translate_methods_base():
    """!
    @brief Test write_inc_translate_methods method with text value
    """
    mock_file = MockFile()
    retdict = ParamRetDict.build_return_dict("string", "trans ret desc")

    mock_trans_list = 'code_tools_grocsoftware.base.' \
                      'json_string_class_description.StringClassDescription' \
                      '.get_tranlate_method_list'
    mock_get_trans = 'code_tools_grocsoftware.base.' \
                     'json_string_class_description.StringClassDescription' \
                     '.get_tranlate_method_function_data'

    base = BaseCppStringClassGenerator()
    expected = []
    expected.extend(base.write_method("getMessage",
                                      "brief func desc",
                                      [],
                                      retdict,
                                      "[[nodiscard]] virtual",
                                      "= 0",
                                      False))
    expected.append("\n")

    with patch(mock_trans_list) as mock_method_list:
        mock_method_list.return_value = ["getMessage"]
        with patch(mock_get_trans) as mock_trans_data:
            mock_trans_data.return_value = ("brief func desc", [], retdict)

            # Mock the project description to return the expected data
            class_gen = GenerateLangFiles(MockProjectDescription())
            class_gen._write_inc_translate_methods(mock_file, True)

            assert len(mock_file.mock_calls) == 2
            assert len(mock_file.writedata) == len(expected)

            for i, line in enumerate(expected):
                assert mock_file.writedata[i] == line

def test022_write_inc_translate_methods_notbase():
    """!
    @brief Test write_inc_translate_methods method with languge value
    """
    mock_file = MockFile()
    retdict = ParamRetDict.build_return_dict("string", "trans ret desc")

    mock_trans_list = 'code_tools_grocsoftware.base.' \
                      'json_string_class_description.StringClassDescription' \
                      '.get_tranlate_method_list'
    mock_get_trans = 'code_tools_grocsoftware.base.' \
                     'json_string_class_description.StringClassDescription' \
                     '.get_tranlate_method_function_data'

    base = BaseCppStringClassGenerator()
    expected = []
    expected.extend(base.write_method("getMessage",
                                      "brief func desc",
                                      [],
                                      retdict,
                                      None,
                                      "final",
                                      True))

    with patch(mock_trans_list) as mock_method_list:
        mock_method_list.return_value = ["getMessage"]
        with patch(mock_get_trans) as mock_trans_data:
            mock_trans_data.return_value = ("brief func desc", [], retdict)

            # Mock the project description to return the expected data
            class_gen = GenerateLangFiles(MockProjectDescription())
            class_gen._write_inc_translate_methods(mock_file, False)

            assert len(mock_file.mock_calls) == 1
            assert len(mock_file.writedata) == len(expected)

            for i, line in enumerate(expected):
                assert mock_file.writedata[i] == line

def test023_write_src_translate_methods_no_params():
    """!
    @brief Test write_src_translate_methods method no param
    """
    mock_file = MockFile()
    str_data = StringClassDescription(strclass_filename)
    class_name = str_data.get_language_class_name("english")

    retdict = ParamRetDict.build_return_dict("string", "trans ret desc")

    mock_trans_list = 'code_tools_grocsoftware.base.' \
                      'json_string_class_description.StringClassDescription' \
                      '.get_tranlate_method_list'
    mock_get_trans = 'code_tools_grocsoftware.base.' \
                     'json_string_class_description.StringClassDescription' \
                     '.get_tranlate_method_function_data'
    mock_get_text = 'code_tools_grocsoftware.base.' \
                     'json_string_class_description.StringClassDescription' \
                     '.get_tranlate_method_text_data'

    base = BaseCppStringClassGenerator()
    expected = []
    expected.extend(base.define_function_with_decorations(class_name+"::getMessage",
                                      "brief func desc",
                                      [],
                                      retdict,
                                      False,
                                      None,
                                      "const"))
    expected.append("{std::stringstream parserstr; parserstr << \"test text\"; return parserstr.str();}\n")

    with patch(mock_trans_list) as mock_method_list:
        mock_method_list.return_value = ["getMessage"]
        with patch(mock_get_trans) as mock_trans_data:
            mock_trans_data.return_value = ("brief func desc", [], retdict)
            with patch(mock_get_text) as mock_trans_text:
                mock_trans_text.return_value = [["text", "test text"]]

                # Mock the project description to return the expected data
                class_gen = GenerateLangFiles(MockProjectDescription())
                class_gen._write_src_translate_methods(mock_file, "english")

                assert len(mock_file.mock_calls) == 2
                assert len(mock_file.writedata) == len(expected)

                for i, line in enumerate(expected):
                    assert mock_file.writedata[i] == line

def test024_write_src_translate_methods_with_params():
    """!
    @brief Test write_src_translate_methods method with params
    """
    mock_file = MockFile()
    str_data = StringClassDescription(strclass_filename)
    class_name = str_data.get_language_class_name("english")

    retdict = ParamRetDict.build_return_dict("string", "trans ret desc")
    param = ParamRetDict.build_param_dict('foo', 'integer', 'foo desc')

    mock_trans_list = 'code_tools_grocsoftware.base.' \
                      'json_string_class_description.StringClassDescription' \
                      '.get_tranlate_method_list'
    mock_get_trans = 'code_tools_grocsoftware.base.' \
                     'json_string_class_description.StringClassDescription' \
                     '.get_tranlate_method_function_data'
    mock_get_text = 'code_tools_grocsoftware.base.' \
                     'json_string_class_description.StringClassDescription' \
                     '.get_tranlate_method_text_data'

    base = BaseCppStringClassGenerator()
    expected = []
    expected.extend(base.define_function_with_decorations(class_name+"::getMessage",
                                      "brief func desc",
                                      [param],
                                      retdict,
                                      False,
                                      None,
                                      None))
    expected.append("{std::stringstream parserstr; parserstr << \"test text foo = \"" \
                    " << foo; return parserstr.str();}\n")

    with patch(mock_trans_list) as mock_method_list:
        mock_method_list.return_value = ["getMessage"]
        with patch(mock_get_trans) as mock_trans_data:
            mock_trans_data.return_value = ("brief func desc", [param], retdict)
            with patch(mock_get_text) as mock_trans_text:
                mock_trans_text.return_value = [["text", "test text foo = "], ["param", "foo"]]

                # Mock the project description to return the expected data
                class_gen = GenerateLangFiles(MockProjectDescription())
                class_gen._write_src_translate_methods(mock_file, "english")

                assert len(mock_file.mock_calls) == 2
                assert len(mock_file.writedata) == len(expected)

                for i, line in enumerate(expected):
                    assert mock_file.writedata[i] == line

# pylint: enable=protected-access
