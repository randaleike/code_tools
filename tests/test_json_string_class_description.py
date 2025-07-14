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

from unittest.mock import patch, MagicMock
import pytest

from code_tools_grocsoftware.base.json_string_class_description import TransTxtParser
from code_tools_grocsoftware.base.json_string_class_description import StringClassDescription
from code_tools_grocsoftware.base.param_return_tools import ParamRetDict
from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList

from tests.dir_init import TESTFILEPATH

# pylint: disable=protected-access

class Test02StringClassDescription:
    """!
    @brief Unit test for the StringClassDescription class
    """
    @classmethod
    def setup_class(cls):
        """!
        @brief Setup the test class
        """
        cls.test_json = os.path.join(TESTFILEPATH, "teststrdesc.json")
        cls.testlanglist = os.path.join(TESTFILEPATH, "teststringlanglist.json")


    @classmethod
    def teardown_class(cls):
        """!
        @brief Tear down the test class
        """
        if os.path.exists("jsonStringClassDescription.json"):
            os.remove("jsonStringClassDescription.json")   # Delete in case it was accidently created
        if os.path.exists("temp.json"):
            os.remove("temp.json")   # Delete in case it was accidently not deleted


    def test01_default_constructor(self):
        """!
        @brief Test Default constructor()
        """
        testobj = StringClassDescription()
        pytest.raises(FileNotFoundError)
        assert testobj.filename == "jsonStringClassDescription.json"
        assert testobj.string_jason_data['baseClassName'] == "baseclass"
        assert testobj.string_jason_data['namespace'] == "myNamespace"
        assert testobj.string_jason_data['dynamicCompileSwitch'] == "DYNAMIC_INTERNATIONALIZATION"
        assert len(testobj.string_jason_data['propertyMethods']) == 0
        assert len(testobj.string_jason_data['translateMethods']) == 0

    def test02_constructor_with_file(self):
        """!
        @brief Test Default constructor()
        """
        testobj = StringClassDescription(self.test_json)
        assert testobj.filename == self.test_json
        assert testobj.string_jason_data['baseClassName'] == "ParserStringListInterface"
        assert testobj.string_jason_data['namespace'] == "argparser"
        assert testobj.string_jason_data['dynamicCompileSwitch'] == "TEST_DYNAMIC_INTERNATIONALIZATION"
        assert len(testobj.string_jason_data['propertyMethods']) == 1
        assert list(testobj.string_jason_data['propertyMethods'])[0] == 'getLangIsoCode'
        assert len(testobj.string_jason_data['translateMethods']) == 1
        assert list(testobj.string_jason_data['translateMethods'])[0] == 'getNotListTypeMessage'

    def test03_set_base_class_name(self):
        """!
        @brief Test set_base_class_name method
        """
        testobj = StringClassDescription()
        assert testobj.string_jason_data['baseClassName'] == "baseclass"
        testobj.set_base_class_name("NewClassName")
        assert testobj.string_jason_data['baseClassName'] == "NewClassName"

    def test04_get_base_class_name(self):
        """!
        @brief Test get_base_class_name method
        """
        testobj = StringClassDescription()
        assert testobj.string_jason_data['baseClassName'] == testobj.get_base_class_name()

    def test05_get_base_class_name_with_namespace(self):
        """!
        @brief Test get_base_class_nameWithNamespace method
        """
        testobj = StringClassDescription()
        assert testobj.get_base_class_name_with_namespace("Foo",".") == "Foo.baseclass"

    def test12_get_language_class_name(self):
        """!
        @brief Test get_language_class_name method
        """
        testobj = StringClassDescription()
        assert testobj.get_language_class_name() == "baseclass"
        assert testobj.get_language_class_name("english") == "baseclassEnglish"

    def test13_get_language_class_name_with_namespace(self):
        """!
        @brief Test get_language_class_name_with_namespace method
        """
        testobj = StringClassDescription()
        assert testobj.get_language_class_name_with_namespace("Moo") == "Moo::baseclass"
        assert testobj.get_language_class_name_with_namespace("Moo", ",", "english") == "Moo,baseclassEnglish"

    def test14_set_namespace_name(self):
        """!
        @brief Test set_namespace_name method
        """
        testobj = StringClassDescription()
        assert testobj.string_jason_data['namespace'] == "myNamespace"
        testobj.set_namespace_name("NewNamespace")
        assert testobj.string_jason_data['namespace'] == "NewNamespace"

    def test15_get_namespace_name(self):
        """!
        @brief Test get_namespace_name method
        """
        testobj = StringClassDescription()
        assert testobj.string_jason_data['namespace'] == testobj.get_namespace_name()

    def test16_set_dynamic_compile_switch(self):
        """!
        @brief Test set_dynamic_compile_switch method
        """
        testobj = StringClassDescription()
        assert testobj.string_jason_data['dynamicCompileSwitch'] == "DYNAMIC_INTERNATIONALIZATION"
        testobj.set_dynamic_compile_switch("MY_DYNAMIC_SWITCH")
        assert testobj.string_jason_data['dynamicCompileSwitch'] == "MY_DYNAMIC_SWITCH"

    def test17_get_dynamic_compile_switch(self):
        """!
        @brief Test get_dynamic_compile_switch method
        """
        testobj = StringClassDescription()
        assert testobj.string_jason_data['dynamicCompileSwitch'] == testobj.get_dynamic_compile_switch()

    def test18_define_property_function_entry(self):
        """!
        @brief Test _define_property_function_entry method
        """
        testobj = StringClassDescription()
        property_dict = testobj._define_property_function_entry("silly", "Silly property", "integer", "Some number")
        assert property_dict['name'] == "silly"
        assert property_dict['briefDesc'] == "Silly property"
        assert isinstance(property_dict['params'], list)
        assert len(property_dict['params']) == 0
        assert isinstance(property_dict['return'], dict)
        assert len(property_dict['return']) == 3
        assert property_dict['return']['type'] == "integer"
        assert property_dict['return']['desc'] == "Some number"
        assert property_dict['return']['typeMod'] == 0

        property_dict = testobj._define_property_function_entry("billy", "Billy property", "size", "Some size list", True)
        assert property_dict['name'] == "billy"
        assert property_dict['briefDesc'] == "Billy property"
        assert isinstance(property_dict['params'], list)
        assert len(property_dict['params']) == 0
        assert isinstance(property_dict['return'], dict)
        assert len(property_dict['return']) == 3
        assert property_dict['return']['type'] == "size"
        assert property_dict['return']['desc'] == "Some size list"
        assert property_dict['return']['typeMod'] == ParamRetDict.type_mod_list

    def test19_get_property_method_list(self):
        """!
        @brief Test get_property_method_list method
        """
        testobj = StringClassDescription(self.test_json)
        property_list = testobj.get_property_method_list()
        assert len(property_list) == 1
        assert property_list[0] == 'getLangIsoCode'

    def test20_get_iso_property_method_name(self):
        """!
        @brief Test get_iso_property_method_name method
        """
        testobj = StringClassDescription(self.test_json)
        name = testobj.get_iso_property_method_name()
        assert name == 'getLangIsoCode'

    def test21_get_iso_property_method_name_fail(self):
        """!
        @brief Test get_iso_property_method_name method
        """
        testobj = StringClassDescription()
        name = testobj.get_iso_property_method_name()
        assert name is None

    def test22_get_property_method_data(self):
        """!
        @brief Test get_property_method_data method
        """
        testobj = StringClassDescription(self.test_json)
        property_name, property_desc, param_list, return_dict = testobj.get_property_method_data('getLangIsoCode')
        assert property_name == 'isoCode'
        assert property_desc == 'Get the ISO 639 set 1 language code for this object'
        assert isinstance(param_list, list)
        assert len(param_list) == 0
        assert isinstance(return_dict, dict)
        assert len(return_dict) == 3
        assert return_dict['type'] == 'string'
        assert return_dict['desc'] == 'ISO 639 set 1 language code'
        assert return_dict['typeMod'] == 0

    def test23_define_translation_dict(self):
        """!
        @brief Test _define_translation_dict method
        """
        trans_data_list = [(TransTxtParser.parsed_type_text, "Simple text with "),
                         (TransTxtParser.parsed_type_param, "paramName")]

        testobj = StringClassDescription()
        return_dict = testobj._define_translation_dict("es", trans_data_list)
        assert isinstance(return_dict, dict)
        assert len(return_dict) == 1
        assert isinstance(return_dict['es'], list)
        assert len(return_dict['es']) == 2
        assert return_dict['es'][0][0] == TransTxtParser.parsed_type_text
        assert return_dict['es'][0][1] == "Simple text with "
        assert return_dict['es'][1][0] == TransTxtParser.parsed_type_param
        assert return_dict['es'][1][1] == "paramName"

    def test24_define_translation_dict_no_list(self):
        """!
        @brief Test _define_translation_dict method, no translation text list
        """
        testobj = StringClassDescription()
        return_dict = testobj._define_translation_dict("zh")
        assert isinstance(return_dict, dict)
        assert len(return_dict) == 1
        assert return_dict['zh'] is None

    def test25_define_translation_dict_default(self):
        """!
        @brief Test _define_translation_dict method, no input
        """
        testobj = StringClassDescription()
        return_dict = testobj._define_translation_dict()
        assert isinstance(return_dict, dict)
        assert len(return_dict) == 1
        assert return_dict['en'] is None

    def test26_add_manual_translation(self):
        """!
        @brief Test add_manual_translation method, success
        """
        trans_data_list = [(TransTxtParser.parsed_type_text, "Simple text")]

        testobj = StringClassDescription(self.test_json)
        assert testobj.add_manual_translation('getNotListTypeMessage', "es", trans_data_list)
        assert isinstance(testobj.string_jason_data['translateMethods']['getNotListTypeMessage']['translateDesc']['es'], list)
        assert len(testobj.string_jason_data['translateMethods']['getNotListTypeMessage']['translateDesc']['es']) == 1
        assert testobj.string_jason_data['translateMethods']['getNotListTypeMessage']['translateDesc']['es'][0][0] == TransTxtParser.parsed_type_text
        assert testobj.string_jason_data['translateMethods']['getNotListTypeMessage']['translateDesc']['es'][0][1] == "Simple text"

    def test27_add_manual_translation_fail_no_text_data(self):
        """!
        @brief Test add_manual_translation method, fail for no text_data
        """
        testobj = StringClassDescription(self.test_json)
        assert not testobj.add_manual_translation('getNotListTypeMessage', "fr")

    def test28_add_manual_translation_fail_no_method_name(self):
        """!
        @brief Test add_manual_translation method, fail for no text_data
        """
        trans_data_list = [(TransTxtParser.parsed_type_text, "Simple text")]
        testobj = StringClassDescription(self.test_json)
        assert not testobj.add_manual_translation('getSomethingElse', "fr", trans_data_list)

    def test29_translate_text(self):
        """!
        @brief Test _translate_text method, dummy translate
        """
        class dummy_translate:
            def translate(self, text, target_language, format_, source_language, model):
                return {'translatedText': "Translated Text"}

        testobj = StringClassDescription()
        testobj.trans_client = dummy_translate()
        assert testobj._translate_text("en", "zh", "Some Text") == "Translated Text"

    def test30_translate_text_mock_google(self):
        """!
        @brief Test _translate_text method, mock google.translate client
        """
        class mock_dummy_translate:
            def translate(self, text, target_language, format_, source_language, model):
                return {'translatedText': "Patch Translated Text"}

        testobj = StringClassDescription()
        with patch('google.cloud.translate_v2.Client', MagicMock(return_value=mock_dummy_translate())):
            assert testobj._translate_text("fr", "en", "Some Other Text") == "Patch Translated Text"

    def test31_translate_method_text_no_lang_list(self):
        """!
        @brief Test _translate_text method, no language list
        """
        testobj = StringClassDescription(self.test_json)
        testobj._translate_method_text("getNotListTypeMessage")
        trans_method_desc = testobj.string_jason_data['translateMethods']['getNotListTypeMessage']['translateDesc']
        assert len(trans_method_desc) == 1
        assert 'en' in list(trans_method_desc)

    def test32_translate_method_text_mock_google(self):
        """!
        @brief Test _translate_text method, mock google.translate client
        """
        class mock_dummy_translate:
            def translate(self, text, target_language, format_, source_language, model):
                return {'translatedText': "Patch Translated Method Text @nargs@"}

        lang_list = LanguageDescriptionList(self.testlanglist)
        testobj = StringClassDescription(self.test_json)
        with patch('google.cloud.translate_v2.Client', MagicMock(return_value=mock_dummy_translate())):
            testobj._translate_method_text("getNotListTypeMessage", lang_list)
            trans_method_desc = testobj.string_jason_data['translateMethods']['getNotListTypeMessage']['translateDesc']
            assert len(trans_method_desc) == 2
            assert 'es' in list(trans_method_desc)

            trans_list = trans_method_desc['es']
            assert len(trans_list) ==2
            assert trans_list[0][0] == TransTxtParser.parsed_type_text
            assert trans_list[0][1] == "Patch Translated Method Text "
            assert trans_list[1][0] == TransTxtParser.parsed_type_param
            assert trans_list[1][1] == "nargs"

    def test33_define_translate_function_entry(self):
        """!
        @brief Test _define_translate_function_entry method
        """
        testparams = [ParamRetDict.build_param_dict_with_mod("name", "string", "desc", 0)]
        testret = ParamRetDict.build_return_dict_with_mod("string","return string",0)
        trans_list = [(TransTxtParser.parsed_type_text, "Return text of "),
                     (TransTxtParser.parsed_type_param,"name")]
        testobj = StringClassDescription()
        function_dict = testobj._define_translate_function_entry("Brief Description", testparams, testret, "en", trans_list)

        assert function_dict['briefDesc'] == "Brief Description"
        assert isinstance(function_dict['params'], list)
        assert len(function_dict['params']) == len(testparams)
        for index, parm_dict in enumerate(testparams):
            assert isinstance(function_dict['params'][index], dict)
            for id in list(testret):
                assert len(function_dict['params'][index]) == len(parm_dict)
                assert function_dict['params'][index][id] == parm_dict[id]

        assert isinstance(function_dict['return'], dict)
        assert len(function_dict['return']) == len(testret)
        for id in list(testret):
            assert function_dict['return'][id] == testret[id]

        assert isinstance(function_dict['translateDesc'], dict)
        assert len(function_dict['translateDesc']) == 1
        assert len(function_dict['translateDesc']['en']) == len(trans_list)
        for index, trans_tuple in enumerate(trans_list):
            assert function_dict['translateDesc']['en'][index][0] == trans_tuple[0]
            assert function_dict['translateDesc']['en'][index][1] == trans_tuple[1]

    def test34_get_tranlate_method_list(self):
        """!
        @brief Test get_tranlate_method_list method
        """
        testobj = StringClassDescription(self.test_json)
        trans_func_list = testobj.get_tranlate_method_list()
        assert len(trans_func_list) == 1
        assert trans_func_list[0] == 'getNotListTypeMessage'

    def test35_get_tranlate_method_function_data(self):
        """!
        @brief Test get_tranlate_method_function_data method
        """
        testobj = StringClassDescription(self.test_json)
        brief_desc, param_data, return_data = testobj.get_tranlate_method_function_data('getNotListTypeMessage')

        assert brief_desc == 'Return non-list varg error message'
        assert isinstance(param_data, list)
        assert len(param_data) == 1
        assert isinstance(param_data[0], dict)
        assert len(param_data[0]) == 4

        assert isinstance(return_data, dict)
        assert len(return_data) == 3

    def test36_get_tranlate_method_text_data(self):
        """!
        @brief Test get_tranlate_method_text_data method
        """
        testobj = StringClassDescription(self.test_json)
        trans_string_list = testobj.get_tranlate_method_text_data('getNotListTypeMessage', 'en')
        assert isinstance(trans_string_list, list)
        assert len(trans_string_list) == 2
        assert trans_string_list[0][0] == TransTxtParser.parsed_type_text
        assert trans_string_list[0][1] == "Only list type arguments can have an argument count of "
        assert trans_string_list[1][0] == TransTxtParser.parsed_type_param
        assert trans_string_list[1][1] == "nargs"

    def test37_update(self):
        """!
        @brief Test update()
        """

        testobj = StringClassDescription("temp.json")
        pytest.raises(FileNotFoundError)
        assert testobj.filename == "temp.json"
        assert testobj.string_jason_data['baseClassName'] == "baseclass"
        assert testobj.string_jason_data['namespace'] == "myNamespace"
        assert testobj.string_jason_data['dynamicCompileSwitch'] == "DYNAMIC_INTERNATIONALIZATION"
        assert len(testobj.string_jason_data['propertyMethods']) == 0
        assert len(testobj.string_jason_data['translateMethods']) == 0

        testobj.string_jason_data['baseClassName'] = "foobar"
        testobj.string_jason_data['namespace'] = "planetx"
        testobj.string_jason_data['dynamicCompileSwitch'] = "MAGIC"
        new_property_entry = testobj._define_property_function_entry("Distance", "Distance to star in AU", "integer", "AU to star")
        testobj.string_jason_data['propertyMethods']['testProperty'] = new_property_entry

        xlate_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "Xlated units", 0)
        param_list = [ParamRetDict.build_param_dict_with_mod("units", "integer", "Units to translate", 0)]
        translate_text_list = TransTxtParser.parse_translate_string("Test string @units@")
        new_xlate_entry = testobj._define_translate_function_entry("Brief xlate desc", param_list, xlate_ret_dict, "en", translate_text_list)
        testobj.string_jason_data['translateMethods']['testXlate'] = new_xlate_entry

        testobj.update()
        updateobj = StringClassDescription("temp.json")

        assert updateobj.filename == "temp.json"
        assert updateobj.string_jason_data['baseClassName'] == "foobar"
        assert updateobj.string_jason_data['namespace'] == "planetx"
        assert updateobj.string_jason_data['dynamicCompileSwitch'] == "MAGIC"

        assert len(updateobj.string_jason_data['propertyMethods']) == 1

        assert isinstance(updateobj.string_jason_data['propertyMethods']['testProperty'], dict)
        assert len(updateobj.string_jason_data['propertyMethods']['testProperty']) == 4
        assert updateobj.string_jason_data['propertyMethods']['testProperty']['name'] == 'Distance'
        assert updateobj.string_jason_data['propertyMethods']['testProperty']['briefDesc'] == 'Distance to star in AU'

        assert isinstance(updateobj.string_jason_data['propertyMethods']['testProperty']['params'], list)
        assert len(updateobj.string_jason_data['propertyMethods']['testProperty']['params']) == 0

        assert isinstance(updateobj.string_jason_data['propertyMethods']['testProperty']['return'], dict)
        assert len(updateobj.string_jason_data['propertyMethods']['testProperty']['return']) == 3
        assert updateobj.string_jason_data['propertyMethods']['testProperty']['return']['type'] == "integer"
        assert updateobj.string_jason_data['propertyMethods']['testProperty']['return']['desc'] == "AU to star"
        assert updateobj.string_jason_data['propertyMethods']['testProperty']['return']['typeMod'] == 0

        assert len(updateobj.string_jason_data['translateMethods']) == 1
        assert isinstance(updateobj.string_jason_data['translateMethods']['testXlate'], dict)
        assert len(updateobj.string_jason_data['translateMethods']['testXlate']) == 4
        assert isinstance(updateobj.string_jason_data['translateMethods']['testXlate']['params'], list)
        assert len(updateobj.string_jason_data['translateMethods']['testXlate']['params']) == 1
        assert isinstance(updateobj.string_jason_data['translateMethods']['testXlate']['params'][0], dict)
        assert len(updateobj.string_jason_data['translateMethods']['testXlate']['params'][0]) == 4
        assert updateobj.string_jason_data['translateMethods']['testXlate']['params'][0]['name'] == "units"
        assert updateobj.string_jason_data['translateMethods']['testXlate']['params'][0]['type'] == "integer"
        assert updateobj.string_jason_data['translateMethods']['testXlate']['params'][0]['desc'] == "Units to translate"
        assert updateobj.string_jason_data['translateMethods']['testXlate']['params'][0]['typeMod'] == 0

        assert isinstance(updateobj.string_jason_data['translateMethods']['testXlate']['return'], dict)
        assert len(updateobj.string_jason_data['translateMethods']['testXlate']['return']) == 3
        assert updateobj.string_jason_data['translateMethods']['testXlate']['return']['type'] == "integer"
        assert updateobj.string_jason_data['translateMethods']['testXlate']['return']['desc'] == "Xlated units"
        assert updateobj.string_jason_data['translateMethods']['testXlate']['return']['typeMod'] == 0

        assert isinstance(updateobj.string_jason_data['translateMethods']['testXlate']['translateDesc'], dict)
        assert len(updateobj.string_jason_data['translateMethods']['testXlate']['translateDesc']) == 1
        assert isinstance(updateobj.string_jason_data['translateMethods']['testXlate']['translateDesc']['en'], list)
        assert len(updateobj.string_jason_data['translateMethods']['testXlate']['translateDesc']['en']) == 2
        assert updateobj.string_jason_data['translateMethods']['testXlate']['translateDesc']['en'][0][0] == TransTxtParser.parsed_type_text
        assert updateobj.string_jason_data['translateMethods']['testXlate']['translateDesc']['en'][0][1] == "Test string "
        assert updateobj.string_jason_data['translateMethods']['testXlate']['translateDesc']['en'][1][0] == TransTxtParser.parsed_type_param
        assert updateobj.string_jason_data['translateMethods']['testXlate']['translateDesc']['en'][1][1] == "units"

        os.remove("temp.json")

    def test38_update_tranlations(self):
        """!
        @brief Test update_tranlations()
        """
        class mock_dummy_translate:
            def translate(self, text, target_language, format_, source_language, model):
                return {'translatedText': text}

        testobj = StringClassDescription(self.test_json)
        lang_list = LanguageDescriptionList(self.testlanglist)

        for method_name in testobj.get_tranlate_method_list():
            assert len(testobj.string_jason_data['translateMethods'][method_name]['translateDesc']) == 1

        with patch('google.cloud.translate_v2.Client', MagicMock(return_value=mock_dummy_translate())):
            testobj.update_tranlations(lang_list)

            for method_name in testobj.get_tranlate_method_list():
                assert len(testobj.string_jason_data['translateMethods'][method_name]['translateDesc']) == 2

# pylint: enable=protected-access
