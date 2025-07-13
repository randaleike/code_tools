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

import io
import contextlib
from unittest.mock import patch, MagicMock

from code_tools_grocsoftware.base.json_string_class_description import TranslationTextParser
from code_tools_grocsoftware.base.json_string_class_description import StringClassDescription
from code_tools_grocsoftware.base.param_return_tools import ParamRetDict
from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList

class ExpectedStrHelper(object):
    @staticmethod
    def get_expected_return(expected_type:str, expected_desc:str, expected_type_mod:int)->str:
        """!
        @brief Return the expected print string for the input return values
        @param expected_type {string} Expected type string
        @param expected_desc {string} Expected return description string
        @param expected_type_mod {integer} Expected type modification value
        @return string - Expected print string
        """
        expected_str = "'return': {'type': '"+expected_type+"', "
        expected_str += "'desc': '"+expected_desc+"', "
        expected_str += "'typeMod': "+str(expected_type_mod)+"}"
        return expected_str

    @staticmethod
    def get_expected_param(expected_name:str, expected_type:str, expected_desc:str, expected_type_mod:int)->str:
        """!
        @brief Return the expected print string for the input return values
        @param expected_name {string} Expected parameter name string
        @param expected_type {string} Expected type string
        @param expected_desc {string} Expected parameter description string
        @param expected_type_mod {integer} Expected type modification value
        @return string - Expected print string
        """
        expected_str = "{'name': '"+expected_name+"', "
        expected_str += "'type': '"+expected_type+"', "
        expected_str += "'desc': '"+expected_desc+"', "
        expected_str += "'typeMod': "+str(expected_type_mod)+"}"
        return expected_str

    @staticmethod
    def get_expected_param_list(param_list:list)->str:
        """!
        @brief Return the expected print string for the input return values
        @param param_list {list} Expected parameter dictionary list
        @return string - Expected print string
        """
        expected_str = "'params': ["
        if param_list is not None:
            param_prefix = ""
            for param in param_list:
                expected_name, expected_type, expected_desc, expected_type_mod = ParamRetDict.get_param_data(param)
                expected_str += param_prefix
                expected_str += ExpectedStrHelper.get_expected_param(expected_name, expected_type, expected_desc, expected_type_mod)
                param_prefix = ", "
        expected_str += "]"
        return expected_str

    @staticmethod
    def get_expected_translation_desc_list(text_text:str, lang_list:list = None)->str:
        """!
        @brief Generate the expected translation description text
        @param text_text {string} Test translation text string
        @param lang_list {list} List of languages or None for default 'en'
        @return string - Expected print string
        """
        expected_str = "'translateDesc': {"
        if lang_list is None:
            lang_list = ["en"]

        # Generate the translateDesc dictionary
        lang_listPrefix = ""
        for lang in lang_list:
            expected_str += lang_listPrefix
            expected_str += "'"+lang+"': ["

            # Generate the parsed text list data
            expected_text_list = TranslationTextParser.parse_translate_string(text_text)
            element_prefix = ""
            for element in expected_text_list:
                expected_str += element_prefix
                expected_str += "('"+element[0]+"', '"+element[1]+"')"
                element_prefix = ", "

            # Close the language parsed text list
            expected_str += "]"
            lang_listPrefix = ", "

        # Close the translateDesc dictionary
        expected_str += "}"
        return expected_str

    @staticmethod
    def get_expected_new_translation_entry(brief_desc:str, return_data:dict, param_list:list = [], trans_text:str="", lang_list:list = None):
        """!
        @brief Get the expected new translation method entry print text

        @param brief_desc {str} Expected brief description string
        @param return_data {dict} Expected return dictionary data
        @param param_list {list} Expected parameter dictionary list
        @param trans_text {string} Test translation text string
        @param lang_list {list} List of languages or None for default 'en'

        @return string - Expected print string
        """
        expected_str = "New Entry:\n"
        expected_str += "{'briefDesc': '"+brief_desc+"', "
        expected_str += ExpectedStrHelper.get_expected_param_list(param_list)
        expected_str += ", "
        expected_str += ExpectedStrHelper.get_expected_return(ParamRetDict.get_return_type(return_data),
                                              ParamRetDict.get_return_desc(return_data),
                                              ParamRetDict.get_return_type_mod(return_data))
        expected_str += ", "
        expected_str += ExpectedStrHelper.get_expected_translation_desc_list(trans_text, lang_list)
        expected_str += "}\n"
        return expected_str

    @staticmethod
    def get_expected_trans_desc_help()->str:
        """!
        Get the expected translation description help message
        """
        expected_str = "Enter translation template string. Use @paramName@ in the string to indicate where the \n"
        expected_str += "function parameters should be inserted.\n"
        expected_str += "Example with single input parameter name \"keyString\": Found argument key @keyString@\n"
        return expected_str

    @staticmethod
    def get_expected_new_property_str(method_name:str, property_id:str, return_data:dict):
        """!
        @brief Get the expected new translation method entry print text

        @param method_name {str} Expected method name string
        @param property_id {str} Expected property id string
        @param return_data {dict} Expected return dictionary data
        @return string - Expected print string
        """
        expected_method_desc = "Get the "+ParamRetDict.get_return_desc(return_data)+" for this object"

        expected_str = method_name+":\n"
        expected_str += "{'name': '"+property_id+"', "
        expected_str += "'briefDesc': '"+expected_method_desc+"', "
        expected_str += "'params': [], "
        expected_str += ExpectedStrHelper.get_expected_return(ParamRetDict.get_return_type(return_data),
                                              ParamRetDict.get_return_desc(return_data),
                                              ParamRetDict.get_return_type_mod(return_data))
        expected_str += "}\n"
        return expected_str

    @staticmethod
    def get_expected_option_list()->tuple:
        """!
        @brief Get the expected property data list string for the unittest
        @return string - Expected property list string
        @return int - Maximum index for the list
        """
        property_options = LanguageDescriptionList.get_language_property_list()

        expected_str = "Select language property, from options:\n"
        option_text = ""
        option_prefix = "    "
        max_index = 0
        for index, property_id in enumerate(property_options):
            option_text += option_prefix
            option_text += str(index)+": "
            option_text += property_id
            option_prefix = ", "
            max_index += 1

        expected_str += option_text+"\n"
        return expected_str, max_index

class Test03StringClassDescriptionMacroMethods:
    """!
    @brief Unit test for the StringClassDescription class
    """
    def test01_new_translate_method_entry(self):
        """!
        @brief Test new_translate_method_entry method, improper message
        """
        test_paramlist = [ParamRetDict.build_param_dict_with_mod("foo", "string", "Foo description", 0),
                         ParamRetDict.build_param_dict_with_mod("moo", "integer", "Moo description", 0)]
        test_return = ParamRetDict.build_return_dict_with_mod("string", "Return description", 0)
        test_trans_string = "Test string with input @foo@ and @moo@"
        input_str = (text for text in ["getTestString",
                                      "Brief method description",
                                      str(len(test_paramlist)),
                                      ParamRetDict.get_param_name(test_paramlist[0]),
                                      ParamRetDict.get_param_type(test_paramlist[0]),
                                      ParamRetDict.get_param_desc(test_paramlist[0]),
                                      ParamRetDict.get_param_name(test_paramlist[1]),
                                      ParamRetDict.get_param_type(test_paramlist[1]),
                                      ParamRetDict.get_param_desc(test_paramlist[1]),
                                      ParamRetDict.get_return_type(test_return),
                                      ParamRetDict.get_return_desc(test_return),
                                      "en",
                                      test_trans_string,
                                      "y",
                                      "y"])
        def test_mock_in(prompt):
            if ((prompt == "Is full type a list [y/n]:") or
                (prompt == "Is full type a pointer [y/n]:") or
                (prompt == "Is full type a reference [y/n]:") or
                (prompt == "Can value be undefined [y/n]:") or
                (prompt == "Is full type an array [y/n]:")):
                return 'n'
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()
            assert testobj.new_translate_method_entry()
            assert isinstance(testobj.string_jason_data['translateMethods']['getTestString'], dict)
            assert testobj.string_jason_data['translateMethods']['getTestString']['briefDesc'] == "Brief method description"

            assert len(testobj.string_jason_data['translateMethods']['getTestString']['params']) == 2
            assert testobj.string_jason_data['translateMethods']['getTestString']['params'][0] == test_paramlist[0]
            assert testobj.string_jason_data['translateMethods']['getTestString']['params'][1] == test_paramlist[1]
            assert testobj.string_jason_data['translateMethods']['getTestString']['return'] == test_return

            assert isinstance(testobj.string_jason_data['translateMethods']['getTestString']['translateDesc'], dict)
            assert len(testobj.string_jason_data['translateMethods']['getTestString']['translateDesc']) == 1
            assert isinstance(testobj.string_jason_data['translateMethods']['getTestString']['translateDesc']['en'], list)

            test_parsed_list = TranslationTextParser.parse_translate_string(test_trans_string)
            assert len(testobj.string_jason_data['translateMethods']['getTestString']['translateDesc']['en']) == len(test_parsed_list)

            for index, entry in enumerate(test_parsed_list):
                assert testobj.string_jason_data['translateMethods']['getTestString']['translateDesc']["en"][index] == entry

            expected_str = ExpectedStrHelper.get_expected_trans_desc_help()
            expected_str += ExpectedStrHelper.get_expected_new_translation_entry('Brief method description', test_return, test_paramlist, test_trans_string, ['en'])
            assert output.getvalue() == expected_str

    def test02_new_translate_method_entry_no_confirm(self):
        """!
        @brief Test new_translate_method_entry method, improper message
        """
        test_paramlist = [ParamRetDict.build_param_dict_with_mod("foo", "string", "Foo description", 0),
                         ParamRetDict.build_param_dict_with_mod("moo", "integer", "Moo description", 0)]
        test_return = ParamRetDict.build_return_dict_with_mod("string", "Return description", 0)
        test_trans_string = "Test string with input @foo@ and @moo@"

        test_paramlist2 = [ParamRetDict.build_param_dict_with_mod("foo2", "integer", "Foo description2", 0),
                         ParamRetDict.build_param_dict_with_mod("moo2", "integer", "Moo description2", 0)]
        test_return2 = ParamRetDict.build_return_dict_with_mod("integer", "Return description2", 0)
        test_trans_string2 = "Test string with input @foo2@ and @moo2@"
        input_str = (text for text in ["getTestString",
                                      "Brief method description",
                                      str(len(test_paramlist)),
                                      ParamRetDict.get_param_name(test_paramlist[0]),
                                      ParamRetDict.get_param_type(test_paramlist[0]),
                                      ParamRetDict.get_param_desc(test_paramlist[0]),
                                      ParamRetDict.get_param_name(test_paramlist[1]),
                                      ParamRetDict.get_param_type(test_paramlist[1]),
                                      ParamRetDict.get_param_desc(test_paramlist[1]),
                                      ParamRetDict.get_return_type(test_return),
                                      ParamRetDict.get_return_desc(test_return),
                                      "en",
                                      test_trans_string,
                                      "n",
                                      "get_test_int",
                                      "Brief method description2",
                                      str(len(test_paramlist2)),
                                      ParamRetDict.get_param_name(test_paramlist2[0]),
                                      ParamRetDict.get_param_type(test_paramlist2[0]),
                                      ParamRetDict.get_param_desc(test_paramlist2[0]),
                                      ParamRetDict.get_param_name(test_paramlist2[1]),
                                      ParamRetDict.get_param_type(test_paramlist2[1]),
                                      ParamRetDict.get_param_desc(test_paramlist2[1]),
                                      ParamRetDict.get_return_type(test_return2),
                                      ParamRetDict.get_return_desc(test_return2),
                                      "en",
                                      test_trans_string2,
                                      "y", "n"])
        def test_mock_in(prompt):
            if ((prompt == "Is full type a list [y/n]:") or
                (prompt == "Is full type a pointer [y/n]:") or
                (prompt == "Is full type a reference [y/n]:") or
                (prompt == "Can value be undefined [y/n]:") or
                (prompt == "Is full type an array [y/n]:")):
                return 'n'
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()
            assert not testobj.new_translate_method_entry()
            assert 'getTestString' not in testobj.string_jason_data['translateMethods']
            assert 'get_test_int' not in testobj.string_jason_data['translateMethods']

            expected_str = ExpectedStrHelper.get_expected_trans_desc_help()
            expected_str += ExpectedStrHelper.get_expected_new_translation_entry('Brief method description', test_return, test_paramlist, test_trans_string, ['en'])
            expected_str += ExpectedStrHelper.get_expected_trans_desc_help()
            expected_str += ExpectedStrHelper.get_expected_new_translation_entry('Brief method description2', test_return2, test_paramlist2, test_trans_string2, ['en'])
            assert output.getvalue() == expected_str

    def test03_add_translate_method_entry(self):
        """!
        @brief Test add_translate_method_entry()
        """
        testobj = StringClassDescription()
        param_list = [ParamRetDict.build_param_dict_with_mod("goo", "integer", "goo description", 0)]
        return_dict = ParamRetDict.build_return_dict_with_mod("string", "return description", 0)

        assert testobj.add_translate_method_entry('get_test_int', 'Brief get_test_int description',
                                                        param_list, return_dict, "en", "Test @goo@")

        assert 'get_test_int' in testobj.get_tranlate_method_list()
        assert isinstance(testobj.string_jason_data['translateMethods']['get_test_int'], dict)
        assert testobj.string_jason_data['translateMethods']['get_test_int']['briefDesc'] == "Brief get_test_int description"
        assert len(testobj.string_jason_data['translateMethods']['get_test_int']['params']) == len(param_list)

        for index in range(0, len(param_list)):
            assert testobj.string_jason_data['translateMethods']['get_test_int']['params'][index] == param_list[index]

        assert testobj.string_jason_data['translateMethods']['get_test_int']['return'] == return_dict

        trans_desc_list = TranslationTextParser.parse_translate_string("Test @goo@")
        assert len(testobj.string_jason_data['translateMethods']['get_test_int']['translateDesc']) == 1
        assert isinstance(testobj.string_jason_data['translateMethods']['get_test_int']['translateDesc']['en'], list)
        assert len(testobj.string_jason_data['translateMethods']['get_test_int']['translateDesc']['en']) == len(trans_desc_list)

        for index in range(0, len(trans_desc_list)):
            assert testobj.string_jason_data['translateMethods']['get_test_int']['translateDesc']["en"][index] == trans_desc_list[index]

    def test04_add_translate_method_entry_override(self):
        """!
        @brief Test add_translate_method_entry()
        """
        def test_mock_in(prompt):
            return 'y'

        testobj = StringClassDescription()
        param_list = [ParamRetDict.build_param_dict_with_mod("goo", "integer", "goo description", 0)]
        return_dict = ParamRetDict.build_return_dict_with_mod("string", "return description", 0)
        assert testobj.add_translate_method_entry('get_test_int', 'Brief get_test_int description', param_list, return_dict, "en", "Test @goo@")

        assert 'get_test_int' in testobj.get_tranlate_method_list()
        assert isinstance(testobj.string_jason_data['translateMethods']['get_test_int'], dict)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            param_list = [ParamRetDict.build_param_dict_with_mod("goo2", "unsigned", "goo2 description", 0)]
            return_dict = ParamRetDict.build_return_dict_with_mod("integer", "return int description", 0)
            assert testobj.add_translate_method_entry('get_test_int', 'Brief get_test_int override description',
                                                            param_list, return_dict, "en", "Test override @goo2@")

            assert 'get_test_int' in testobj.get_tranlate_method_list()
            assert isinstance(testobj.string_jason_data['translateMethods']['get_test_int'], dict)
            assert testobj.string_jason_data['translateMethods']['get_test_int']['briefDesc'] == "Brief get_test_int override description"

            assert isinstance(testobj.string_jason_data['translateMethods']['get_test_int']['params'], list)
            assert len(testobj.string_jason_data['translateMethods']['get_test_int']['params']) == len(param_list)

            for index in range(0, len(param_list)):
                assert testobj.string_jason_data['translateMethods']['get_test_int']['params'][index] == param_list[index]

            assert isinstance(testobj.string_jason_data['translateMethods']['get_test_int']['return'], dict)
            assert testobj.string_jason_data['translateMethods']['get_test_int']['return'] == return_dict

            assert isinstance(testobj.string_jason_data['translateMethods']['get_test_int']['translateDesc'], dict)
            assert len(testobj.string_jason_data['translateMethods']['get_test_int']['translateDesc']) == 1

            trans_desc_list = TranslationTextParser.parse_translate_string("Test override @goo2@")
            assert isinstance(testobj.string_jason_data['translateMethods']['get_test_int']['translateDesc']['en'], list)
            assert len(testobj.string_jason_data['translateMethods']['get_test_int']['translateDesc']['en']) == len(trans_desc_list)
            for index in range(0, len(trans_desc_list)):
                assert testobj.string_jason_data['translateMethods']['get_test_int']['translateDesc']["en"][index] == trans_desc_list[index]

    def test05_add_translate_method_entry_no_override(self):
        """!
        @brief Test add_translate_method_entry(), no overwrite
        """
        def test_mock_in(prompt):
            return 'n'

        testobj = StringClassDescription()
        param_list = [ParamRetDict.build_param_dict_with_mod("goo", "integer", "goo description", 0)]
        return_dict = ParamRetDict.build_return_dict_with_mod("string", "return description", 0)
        assert testobj.add_translate_method_entry('get_test_int', 'Brief get_test_int description', param_list, return_dict, "en", "Test @goo@")

        assert 'get_test_int' in testobj.get_tranlate_method_list()
        assert isinstance(testobj.string_jason_data['translateMethods']['get_test_int'], dict)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            param_list2 = [ParamRetDict.build_param_dict_with_mod("goo2", "unsigned", "goo2 description", 0)]
            return_dict2 = ParamRetDict.build_return_dict_with_mod("integer", "return int description", 0)
            assert not testobj.add_translate_method_entry('get_test_int', 'Brief get_test_int override description',
                                                             param_list2, return_dict2, "en", "Test override @goo2@")

            assert 'get_test_int' in testobj.get_tranlate_method_list()
            assert isinstance(testobj.string_jason_data['translateMethods']['get_test_int'], dict)
            assert testobj.string_jason_data['translateMethods']['get_test_int']['briefDesc'] == "Brief get_test_int description"

            assert isinstance(testobj.string_jason_data['translateMethods']['get_test_int']['params'], list)
            assert len(testobj.string_jason_data['translateMethods']['get_test_int']['params']) == len(param_list)

            for index in range(0, len(param_list)):
                assert testobj.string_jason_data['translateMethods']['get_test_int']['params'][index] == param_list[index]

            assert isinstance(testobj.string_jason_data['translateMethods']['get_test_int']['return'], dict)
            assert testobj.string_jason_data['translateMethods']['get_test_int']['return'] == return_dict

            assert isinstance(testobj.string_jason_data['translateMethods']['get_test_int']['translateDesc'], dict)
            assert len(testobj.string_jason_data['translateMethods']['get_test_int']['translateDesc']) == 1

            trans_desc_list = TranslationTextParser.parse_translate_string("Test @goo@")
            assert isinstance(testobj.string_jason_data['translateMethods']['get_test_int']['translateDesc']['en'], list)
            assert len(testobj.string_jason_data['translateMethods']['get_test_int']['translateDesc']['en']) == len(trans_desc_list)
            for index in range(0, len(trans_desc_list)):
                assert testobj.string_jason_data['translateMethods']['get_test_int']['translateDesc']["en"][index] == trans_desc_list[index]

    def test06_add_translate_method_entry_force_override(self):
        """!
        @brief Test add_translate_method_entry()
        """
        def test_mock_in(prompt):
            return 'n'

        testobj = StringClassDescription()
        param_list = [ParamRetDict.build_param_dict_with_mod("goo", "integer", "goo description", 0)]
        return_dict = ParamRetDict.build_return_dict_with_mod("string", "return description", 0)
        assert testobj.add_translate_method_entry('get_test_int', 'Brief get_test_int description', param_list, return_dict, "en", "Test @goo@")

        assert 'get_test_int' in testobj.get_tranlate_method_list()
        assert isinstance(testobj.string_jason_data['translateMethods']['get_test_int'], dict)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            param_list = [ParamRetDict.build_param_dict_with_mod("goo2", "unsigned", "goo2 description", 0)]
            return_dict = ParamRetDict.build_return_dict_with_mod("integer", "return int description", 0)
            assert testobj.add_translate_method_entry('get_test_int', 'Brief get_test_int override description',
                                                            param_list, return_dict, "en", "Test override @goo2@", True)

            assert 'get_test_int' in testobj.get_tranlate_method_list()
            assert isinstance(testobj.string_jason_data['translateMethods']['get_test_int'], dict)
            assert testobj.string_jason_data['translateMethods']['get_test_int']['briefDesc'] == "Brief get_test_int override description"

            assert isinstance(testobj.string_jason_data['translateMethods']['get_test_int']['params'], list)
            assert len(testobj.string_jason_data['translateMethods']['get_test_int']['params']) == len(param_list)

            for index in range(0, len(param_list)):
                assert testobj.string_jason_data['translateMethods']['get_test_int']['params'][index] == param_list[index]

            assert isinstance(testobj.string_jason_data['translateMethods']['get_test_int']['return'], dict)
            assert testobj.string_jason_data['translateMethods']['get_test_int']['return'] == return_dict

            assert isinstance(testobj.string_jason_data['translateMethods']['get_test_int']['translateDesc'], dict)
            assert len(testobj.string_jason_data['translateMethods']['get_test_int']['translateDesc']) == 1

            trans_desc_list = TranslationTextParser.parse_translate_string("Test override @goo2@")
            assert isinstance(testobj.string_jason_data['translateMethods']['get_test_int']['translateDesc']['en'], list)
            assert len(testobj.string_jason_data['translateMethods']['get_test_int']['translateDesc']['en']) == len(trans_desc_list)
            for index in range(0, len(trans_desc_list)):
                assert testobj.string_jason_data['translateMethods']['get_test_int']['translateDesc']["en"][index] == trans_desc_list[index]

    def test07_get_property_return_data(self):
        """!
        @brief Test _get_property_return_data()
        """
        input_str = (text for text in ["0", "1", "2", "3", "4", "5"])
        def test_mock_in(prompt):
            return next(input_str)

        testobj = StringClassDescription()
        property_options = LanguageDescriptionList.get_language_property_list()

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            for index in range(0,6):
                property_id, method_name, return_type, return_desc, is_list = testobj._get_property_return_data()

                expected_return_type, expected_return_desc, expected_is_list = LanguageDescriptionList.get_language_property_return_data(property_options[index])
                expected_method_name = LanguageDescriptionList.get_language_property_method_name(property_options[index])

                assert property_id == property_options[index]
                assert method_name == expected_method_name
                assert return_type == expected_return_type
                assert return_desc == expected_return_desc
                assert is_list == expected_is_list

    def test08_get_property_return_data_bad_input(self):
        """!
        @brief Test _get_property_return_data()
        """
        input_str = (text for text in ["8", "0"])
        def test_mock_in(prompt):
            return next(input_str)

        testobj = StringClassDescription()
        property_options = LanguageDescriptionList.get_language_property_list()

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            property_id, method_name, return_type, return_desc, is_list = testobj._get_property_return_data()

            expected_return_type, expected_return_desc, expected_is_list = LanguageDescriptionList.get_language_property_return_data(property_options[0])
            expected_method_name = LanguageDescriptionList.get_language_property_method_name(property_options[0])

            assert property_id == property_options[0]
            assert method_name == expected_method_name
            assert return_type == expected_return_type
            assert return_desc == expected_return_desc
            assert is_list == expected_is_list

            expected_str, max_index = ExpectedStrHelper.get_expected_option_list()
            expected_str += "Valid input values are 0 to "+str(max_index-1)+", try again\n"
            assert output.getvalue() == expected_str

    def test09_new_property_method_entry(self):
        """!
        @brief Test new_property_method_entry()
        """
        input_str = (text for text in ["0", "y", "y"])
        def test_mock_in(prompt):
            return next(input_str)

        testobj = StringClassDescription()
        property_options = LanguageDescriptionList.get_language_property_list()

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            assert testobj.new_property_method_entry()

            return_type, return_desc, is_list = LanguageDescriptionList.get_language_property_return_data(property_options[0])
            expected_return = ParamRetDict.build_return_dict(return_type, return_desc, is_list)
            expected_method_name = LanguageDescriptionList.get_language_property_method_name(property_options[0])

            expected_str, max_index = ExpectedStrHelper.get_expected_option_list()
            expected_str += ExpectedStrHelper.get_expected_new_property_str(expected_method_name, property_options[0], expected_return)
            assert output.getvalue() == expected_str

    def test10_new_property_method_entry_no(self):
        """!
        @brief Test new_property_method_entry()
        """
        input_str = (text for text in ["0", "n", "1", "y", "y"])
        def test_mock_in(prompt):
            return next(input_str)

        testobj = StringClassDescription()
        property_options = LanguageDescriptionList.get_language_property_list()
        option_string, _ = ExpectedStrHelper.get_expected_option_list()

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            assert testobj.new_property_method_entry()

            return_type, return_desc, is_list = LanguageDescriptionList.get_language_property_return_data(property_options[0])
            expected_return = ParamRetDict.build_return_dict(return_type, return_desc, is_list)
            expected_method_name = LanguageDescriptionList.get_language_property_method_name(property_options[0])

            return_type1, return_desc1, is_list1 = LanguageDescriptionList.get_language_property_return_data(property_options[1])
            expected_return1 = ParamRetDict.build_return_dict(return_type1, return_desc1, is_list1)
            expected_method_name1 = LanguageDescriptionList.get_language_property_method_name(property_options[1])

            expected_str = option_string
            expected_str += ExpectedStrHelper.get_expected_new_property_str(expected_method_name, property_options[0], expected_return)
            expected_str += option_string
            expected_str += ExpectedStrHelper.get_expected_new_property_str(expected_method_name1, property_options[1], expected_return1)
            assert output.getvalue() == expected_str

    def test11_new_property_method_entry_no_commit(self):
        """!
        @brief Test new_property_method_entry()
        """
        input_str = (text for text in ["0", "y", "n"])
        def test_mock_in(prompt):
            return next(input_str)

        testobj = StringClassDescription()
        property_options = LanguageDescriptionList.get_language_property_list()
        option_string, _ = ExpectedStrHelper.get_expected_option_list()

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            assert not testobj.new_property_method_entry()

            return_type, return_desc, is_list = LanguageDescriptionList.get_language_property_return_data(property_options[0])
            expected_return = ParamRetDict.build_return_dict(return_type, return_desc, is_list)
            expected_method_name = LanguageDescriptionList.get_language_property_method_name(property_options[0])

            expected_str = option_string
            expected_str += ExpectedStrHelper.get_expected_new_property_str(expected_method_name, property_options[0], expected_return)
            assert output.getvalue() == expected_str

    def test12_add_property_method_entry(self):
        """!
        @brief Test add_property_method_entry()
        """
        input_str = (text for text in ["y"])
        def test_mock_in(prompt):
            return next(input_str)

        testobj = StringClassDescription()
        property_options = LanguageDescriptionList.get_language_property_list()

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            assert testobj.add_property_method_entry(property_options[3])

            return_type, return_desc, is_list = LanguageDescriptionList.get_language_property_return_data(property_options[3])
            expected_return = ParamRetDict.build_return_dict(return_type, return_desc, is_list)
            expected_method_name = LanguageDescriptionList.get_language_property_method_name(property_options[3])

            assert expected_method_name in testobj.get_property_method_list()
            assert isinstance(testobj.string_jason_data['propertyMethods'][expected_method_name], dict)
            assert testobj.string_jason_data['propertyMethods'][expected_method_name]['name'] == property_options[3]
            assert testobj.string_jason_data['propertyMethods'][expected_method_name]['briefDesc'] == "Get the "+return_desc+" for this object"

            assert isinstance(testobj.string_jason_data['propertyMethods'][expected_method_name]['params'], list)
            assert len(testobj.string_jason_data['propertyMethods'][expected_method_name]['params']) == 0

            assert isinstance(testobj.string_jason_data['propertyMethods'][expected_method_name]['return'], dict)
            assert testobj.string_jason_data['propertyMethods'][expected_method_name]['return'] == expected_return

    def test13_add_property_method_entry_no_confirm(self):
        """!
        @brief Test add_property_method_entry(), confirm=no
        """
        input_str = (text for text in ["n"])
        def test_mock_in(prompt):
            return next(input_str)

        testobj = StringClassDescription()
        property_options = LanguageDescriptionList.get_language_property_list()

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            assert not testobj.add_property_method_entry(property_options[3])
            expected_method_name = LanguageDescriptionList.get_language_property_method_name(property_options[3])
            assert expected_method_name not in testobj.get_property_method_list()

    def test14_add_translate_method_entry_badtranslate_string(self):
        """!
        @brief Test add_translate_method_entry(), bad translate string
        """
        def test_mock_in(prompt):
            return 'n'

        testobj = StringClassDescription()
        param_list = [ParamRetDict.build_param_dict_with_mod("goo", "integer", "goo description", 0)]
        return_dict = ParamRetDict.build_return_dict_with_mod("string", "return description", 0)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            assert not testobj.add_translate_method_entry('get_test_int',
                                                             'Brief get_test_int description',
                                                             param_list, return_dict,
                                                             "en", "Test @goo@ @foo@")

            assert 'get_test_int' not in testobj.get_tranlate_method_list()
            assert output.getvalue() == "Error: Invalid translation string: Test @goo@ @foo@. param_count= 2 match_count= 1\n"
