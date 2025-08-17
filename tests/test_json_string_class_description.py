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

import pytest

from code_tools_grocsoftware.base.json_string_class_description import TransTxtParser
from code_tools_grocsoftware.base.json_string_class_description import StringClassDescription
from code_tools_grocsoftware.base.param_return_tools import ParamRetDict
from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList

from tests.dir_init import TESTFILEPATH

# pylint: disable=protected-access

# pylint: disable=too-few-public-methods
class MockTranslator():
    """!
    Mock Translator class for testing
    """

    def translate_text(self, source_lang:str, target_lang:str, text:str="")->str:
        """!
        @brief Mock Translate the input text
        @param source_lang {string} ISO 639-1 language code of the input text
        @param target_lang {string} ISO 639-1 language code for the output text
        @param text {string} text to translate
        @return string - Mock translated text
        """
        return source_lang+"->"+target_lang+":"+text
# pylint: enable=too-few-public-methods

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
            # Delete in case it was accidently created
            os.remove("jsonStringClassDescription.json")

        if os.path.exists("temp.json"):
            # Delete in case it was accidently not deleted
            os.remove("temp.json")

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
        switch = testobj.string_jason_data['dynamicCompileSwitch']
        assert switch == "TEST_DYNAMIC_INTERNATIONALIZATION"
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
        tststr = testobj.get_language_class_name_with_namespace("Moo")
        tststr1 = testobj.get_language_class_name_with_namespace("Moo", ",", "english")
        assert tststr == "Moo::baseclass"
        assert tststr1 == "Moo,baseclassEnglish"

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
        switch = testobj.string_jason_data['dynamicCompileSwitch']
        assert switch == testobj.get_dynamic_compile_switch()

    def test18_define_property_function_entry(self):
        """!
        @brief Test _define_property_function_entry method
        """
        testobj = StringClassDescription()
        property_dict = testobj._define_property_function_entry("silly",
                                                                "Silly property",
                                                                "integer",
                                                                "Some number")
        assert property_dict['name'] == "silly"
        assert property_dict['briefDesc'] == "Silly property"
        assert isinstance(property_dict['params'], list)
        assert len(property_dict['params']) == 0
        assert isinstance(property_dict['return'], dict)
        assert len(property_dict['return']) == 3
        assert property_dict['return']['type'] == "integer"
        assert property_dict['return']['desc'] == "Some number"
        assert property_dict['return']['typeMod'] == 0

        property_dict = testobj._define_property_function_entry("billy",
                                                                "Billy property",
                                                                "size",
                                                                "Some size list",
                                                                True)
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
        name, desc, plist, rdict = testobj.get_property_method_data('getLangIsoCode')
        assert name == 'isoCode'
        assert desc == 'Get the ISO 639 set 1 language code for this object'
        assert isinstance(plist, list)
        assert len(plist) == 0
        assert isinstance(rdict, dict)
        assert len(rdict) == 3
        assert rdict['type'] == 'string'
        assert rdict['desc'] == 'ISO 639 set 1 language code'
        assert rdict['typeMod'] == 0

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
        json_data = testobj.string_jason_data
        tst_list = json_data['translateMethods']['getNotListTypeMessage']['translateDesc']['es']
        assert isinstance(tst_list, list)
        assert len(tst_list) == 1
        assert tst_list[0][0] == TransTxtParser.parsed_type_text
        assert tst_list[0][1] == "Simple text"

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
        testobj = StringClassDescription()
        testobj.trans_client = MockTranslator()
        assert testobj._translate_text("en", "zh", "Some Text") == "en->zh:Some Text"

    def test31_translate_method_text_no_lang_list(self):
        """!
        @brief Test _translate_text method, no language list
        """
        testobj = StringClassDescription(self.test_json)
        testobj.trans_client = MockTranslator()
        testobj._translate_method_text("getNotListTypeMessage")
        jsondata = testobj.string_jason_data
        tm_desc = jsondata['translateMethods']['getNotListTypeMessage']['translateDesc']
        assert len(tm_desc) == 1
        assert 'en' in list(tm_desc)

    def test32_translate_method_text_mock_google(self):
        """!
        @brief Test _translate_text method, mock google.translate client
        """
        lang_list = LanguageDescriptionList(self.testlanglist)
        testobj = StringClassDescription(self.test_json)
        testobj.trans_client = MockTranslator()

        testobj._translate_method_text("getNotListTypeMessage", lang_list)
        jsondata = testobj.string_jason_data
        tm_desc = jsondata['translateMethods']['getNotListTypeMessage']['translateDesc']
        assert len(tm_desc) == 2
        assert 'es' in list(tm_desc)

        trans_list = tm_desc['es']
        assert len(trans_list) == 2
        assert trans_list[0][0] == TransTxtParser.parsed_type_text
        assert trans_list[0][1] == "en->es:Only list type arguments can have an argument count of "
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
        function_dict = testobj._define_translate_function_entry("Brief Description",
                                                                 testparams,
                                                                 testret,
                                                                 "en",
                                                                 trans_list)

        assert function_dict['briefDesc'] == "Brief Description"
        assert isinstance(function_dict['params'], list)
        assert len(function_dict['params']) == len(testparams)
        for index, parm_dict in enumerate(testparams):
            assert isinstance(function_dict['params'][index], dict)
            for paramfield in list(parm_dict):
                assert len(function_dict['params'][index]) == len(parm_dict)
                assert function_dict['params'][index][paramfield] == parm_dict[paramfield]

        assert isinstance(function_dict['return'], dict)
        assert len(function_dict['return']) == len(testret)
        for retfield in list(testret):
            assert function_dict['return'][retfield] == testret[retfield]

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
        desc, pdata, rdata = testobj.get_tranlate_method_function_data('getNotListTypeMessage')

        assert desc == 'Return non-list varg error message'
        assert isinstance(pdata, list)
        assert len(pdata) == 1
        assert isinstance(pdata[0], dict)
        assert len(pdata[0]) == 4

        assert isinstance(rdata, dict)
        assert len(rdata) == 3

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

    # pylint: disable=too-many-statements
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
        new_property_entry = testobj._define_property_function_entry("Distance",
                                                                     "Distance to star in AU",
                                                                     "integer",
                                                                     "AU to star")
        testobj.string_jason_data['propertyMethods']['testProperty'] = new_property_entry

        xlate_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "Xlated units", 0)
        param_list = [ParamRetDict.build_param_dict_with_mod("units",
                                                             "integer",
                                                             "Units to translate",
                                                             0)]
        translate_text_list = TransTxtParser.parse_translate_string("Test string @units@")
        new_xlate_entry = testobj._define_translate_function_entry("Brief xlate desc",
                                                                   param_list,
                                                                   xlate_ret_dict,
                                                                   "en",
                                                                   translate_text_list)
        testobj.string_jason_data['translateMethods']['testXlate'] = new_xlate_entry

        testobj.update()
        updateobj = StringClassDescription("temp.json")

        assert updateobj.filename == "temp.json"
        assert updateobj.string_jason_data['baseClassName'] == "foobar"
        assert updateobj.string_jason_data['namespace'] == "planetx"
        assert updateobj.string_jason_data['dynamicCompileSwitch'] == "MAGIC"

        assert len(updateobj.string_jason_data['propertyMethods']) == 1

        tst_prop_dict = updateobj.string_jason_data['propertyMethods']['testProperty']
        assert isinstance(tst_prop_dict, dict)
        assert len(tst_prop_dict) == 4
        assert tst_prop_dict['name'] == 'Distance'
        assert tst_prop_dict['briefDesc'] == 'Distance to star in AU'

        assert isinstance(tst_prop_dict['params'], list)
        assert len(tst_prop_dict['params']) == 0

        assert isinstance(tst_prop_dict['return'], dict)
        assert len(tst_prop_dict['return']) == 3
        assert tst_prop_dict['return']['type'] == "integer"
        assert tst_prop_dict['return']['desc'] == "AU to star"
        assert tst_prop_dict['return']['typeMod'] == 0

        tst_tm_dict = updateobj.string_jason_data['translateMethods']['testXlate']
        assert len(updateobj.string_jason_data['translateMethods']) == 1
        assert isinstance(tst_tm_dict, dict)
        assert len(tst_tm_dict) == 4
        assert isinstance(tst_tm_dict['params'], list)
        assert len(tst_tm_dict['params']) == 1
        assert isinstance(tst_tm_dict['params'][0], dict)
        assert len(tst_tm_dict['params'][0]) == 4
        assert tst_tm_dict['params'][0]['name'] == "units"
        assert tst_tm_dict['params'][0]['type'] == "integer"
        assert tst_tm_dict['params'][0]['desc'] == "Units to translate"
        assert tst_tm_dict['params'][0]['typeMod'] == 0

        assert isinstance(tst_tm_dict['return'], dict)
        assert len(tst_tm_dict['return']) == 3
        assert tst_tm_dict['return']['type'] == "integer"
        assert tst_tm_dict['return']['desc'] == "Xlated units"
        assert tst_tm_dict['return']['typeMod'] == 0

        assert isinstance(tst_tm_dict['translateDesc'], dict)
        assert len(tst_tm_dict['translateDesc']) == 1
        assert isinstance(tst_tm_dict['translateDesc']['en'], list)
        assert len(tst_tm_dict['translateDesc']['en']) == 2
        assert tst_tm_dict['translateDesc']['en'][0][0] == TransTxtParser.parsed_type_text
        assert tst_tm_dict['translateDesc']['en'][0][1] == "Test string "
        assert tst_tm_dict['translateDesc']['en'][1][0] == TransTxtParser.parsed_type_param
        assert tst_tm_dict['translateDesc']['en'][1][1] == "units"

        os.remove("temp.json")
    # pylint: enable=too-many-statements

    def test38_update_tranlations(self):
        """!
        @brief Test update_tranlations()
        """
        testobj = StringClassDescription(self.test_json)
        testobj.trans_client = MockTranslator

        for method_name in testobj.get_tranlate_method_list():
            temp = testobj.string_jason_data['translateMethods']
            assert len(temp[method_name]['translateDesc']) == 1

        lang_list = LanguageDescriptionList(self.testlanglist)
        testobj.update_tranlations(lang_list)
        temp = testobj.string_jason_data['translateMethods']

        for method_name in testobj.get_tranlate_method_list():
            assert len(temp[method_name]['translateDesc']) == 2

    def test39_get_base_selection_name(self):
        """!
        @brief Test get_base_selection_name()
        """
        testobj = StringClassDescription()
        assert testobj.string_jason_data['baseSelectionFunction'] == testobj.get_base_selection_name()

    def test40_set_base_selection_name(self):
        """!
        @brief Test set_base_selection_name()
        """
        testobj = StringClassDescription()
        assert testobj.string_jason_data['baseSelectionFunction'] == "getLocalStringListInterface"
        testobj.set_base_selection_name("NewBaseSelection")
        assert testobj.string_jason_data['baseSelectionFunction'] == "NewBaseSelection"

    def test41_set_extra_mock(self):
        """!
        @brief Test set_extra_mock
        """
        testobj = StringClassDescription()
        testobj.set_extra_mock(["#ifdef (foo)\n",
                                "#endif\n"])
        assert len(testobj.string_jason_data['extraMock']) == 2
        assert testobj.string_jason_data['extraMock'][0] == "#ifdef (foo)\n"
        assert testobj.string_jason_data['extraMock'][1] == "#endif\n"

    def test42_get_extra_mock(self):
        """!
        @brief Test get_extra_mock
        """
        testobj = StringClassDescription()
        testobj.set_extra_mock(["#ifdef (foo)\n",
                                "#endif\n"])

        extra = testobj.get_extra_mock()
        assert len(extra) == 2
        assert extra[0] == "#ifdef (foo)\n"
        assert extra[1] == "#endif\n"

# pylint: enable=protected-access
