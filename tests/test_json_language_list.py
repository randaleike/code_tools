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
import io
import contextlib

from unittest.mock import patch
import pytest

from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList
from tests.dir_init import TESTFILEPATH

# pylint: disable=protected-access

class Test01JsonLanguageList:
    """!
    @brief Unit test for the LanguageDescriptionList class
    """

    @classmethod
    def setup_class(cls):
        cls.test_json = os.path.join(TESTFILEPATH, "testdata.json")


    @classmethod
    def teardown_class(cls):
        if os.path.exists("jsonLanguageDescriptionList.json"):
            os.remove("jsonLanguageDescriptionList.json")   # Delete in case it was accidently created


    def test01_default_constructor(self):
        """!
        @brief Test Default constructor()
        """
        testobj = LanguageDescriptionList()
        pytest.raises(FileNotFoundError)
        assert testobj.filename == "jsonLanguageDescriptionList.json"
        assert testobj.lang_json_data['default'] is not None
        assert testobj.lang_json_data['default']['name'] == "english"
        assert testobj.lang_json_data['default']['isoCode'] == "en"
        assert testobj.lang_json_data['languages'] is not None
        assert len(testobj.lang_json_data['languages']) == 0

    def test02_constructor_with_file(self):
        """!
        @brief Test constructor() with file name
        """
        testobj = LanguageDescriptionList(self.test_json)
        assert testobj.filename == self.test_json
        assert testobj.lang_json_data['default'] is not None
        assert testobj.lang_json_data['default']['name'] == "spanish"
        assert testobj.lang_json_data['default']['isoCode'] == "es"
        assert testobj.lang_json_data['languages'] is not None
        assert len(testobj.lang_json_data['languages']) == 1

        assert testobj.lang_json_data['languages']['english'] is not None
        key_list = list(testobj.lang_json_data['languages']['english'].keys())
        assert len(key_list) == 6

        assert 'LANG' in key_list
        assert testobj.lang_json_data['languages']['english']['LANG'] is not None
        assert testobj.lang_json_data['languages']['english']['LANG'] == 'en'

        assert 'LANG_regions' in key_list
        assert testobj.lang_json_data['languages']['english']['LANG_regions'] is not None
        assert len(testobj.lang_json_data['languages']['english']['LANG_regions']) == 13
        assert testobj.lang_json_data['languages']['english']['LANG_regions'][0] == 'AU'
        assert testobj.lang_json_data['languages']['english']['LANG_regions'][12] == 'ZW'

        assert 'LANGID' in key_list
        assert testobj.lang_json_data['languages']['english']['LANGID'] is not None
        assert len(testobj.lang_json_data['languages']['english']['LANGID']) == 1
        assert testobj.lang_json_data['languages']['english']['LANGID'][0] == 9

        assert 'LANGID_regions' in key_list
        assert testobj.lang_json_data['languages']['english']['LANGID_regions'] is not None
        assert len(testobj.lang_json_data['languages']['english']['LANGID_regions']) == 14
        assert testobj.lang_json_data['languages']['english']['LANGID_regions'][0] == 3081
        assert testobj.lang_json_data['languages']['english']['LANGID_regions'][13] == 12297

        assert 'isoCode' in key_list
        assert testobj.lang_json_data['languages']['english']['isoCode'] is not None
        assert testobj.lang_json_data['languages']['english']['isoCode'] == 'en'

        assert 'compileSwitch' in key_list
        assert testobj.lang_json_data['languages']['english']['compileSwitch'] is not None
        assert testobj.lang_json_data['languages']['english']['compileSwitch'] == "ENGLISH_ERRORS"

    def test03_clear(self):
        """!
        @brief Test clear method
        """
        testobj = LanguageDescriptionList(self.test_json)
        assert testobj.filename == self.test_json
        assert testobj.lang_json_data['default'] is not None
        assert testobj.lang_json_data['default']['isoCode'] == "es"
        assert testobj.lang_json_data['languages'] is not None
        assert len(testobj.lang_json_data['languages']) == 1

        testobj.clear()
        assert testobj.filename == self.test_json
        assert testobj.lang_json_data['default'] is not None
        assert testobj.lang_json_data['default']['name'] == "english"
        assert testobj.lang_json_data['default']['isoCode'] == "en"
        assert testobj.lang_json_data['languages'] is not None
        assert len(testobj.lang_json_data['languages']) == 0

    def test04_printerror(self):
        """!
        @brief Test _print_error method
        """
        testobj = LanguageDescriptionList()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            testobj._print_error("test error")
            assert output.getvalue() == "Error: test error\n"

    def test11_update(self):
        """!
        @brief Test update method
        """
        testobj = LanguageDescriptionList("temp.json")
        assert testobj.filename == "temp.json"
        testobj.lang_json_data['languages']['french'] = {'LANG':'fr', 'LANG_regions':['FR'],
                                                       'LANGID': [12], 'LANGID_regions': [1036, 5132],
                                                       'isoCode': 'fr', 'compileSwitch': "FRENCH_ERRORS"}
        testobj.update()

        updateobj = LanguageDescriptionList("temp.json")
        assert updateobj.filename == "temp.json"
        assert updateobj.lang_json_data['default'] is not None
        assert updateobj.lang_json_data['default']['name'] == "english"
        assert updateobj.lang_json_data['default']['isoCode'] == "en"
        assert updateobj.lang_json_data['languages'] is not None
        assert len(updateobj.lang_json_data['languages']) == 1

        assert updateobj.lang_json_data['languages']['french'] is not None
        key_list = list(updateobj.lang_json_data['languages']['french'].keys())
        assert len(key_list) == 6

        assert 'LANG' in key_list
        assert updateobj.lang_json_data['languages']['french']['LANG'] is not None
        assert updateobj.lang_json_data['languages']['french']['LANG'] == 'fr'

        assert 'LANG_regions' in key_list
        assert updateobj.lang_json_data['languages']['french']['LANG_regions'] is not None
        assert len(updateobj.lang_json_data['languages']['french']['LANG_regions']) == 1
        assert updateobj.lang_json_data['languages']['french']['LANG_regions'][0] == 'FR'

        assert 'LANGID' in key_list
        assert updateobj.lang_json_data['languages']['french']['LANGID'] is not None
        assert len(updateobj.lang_json_data['languages']['french']['LANGID']) == 1
        assert updateobj.lang_json_data['languages']['french']['LANGID'][0] == 12

        assert 'LANGID_regions' in key_list
        assert updateobj.lang_json_data['languages']['french']['LANGID_regions'] is not None
        assert len(updateobj.lang_json_data['languages']['french']['LANGID_regions']) == 2
        assert updateobj.lang_json_data['languages']['french']['LANGID_regions'][0] == 1036
        assert updateobj.lang_json_data['languages']['french']['LANGID_regions'][1] == 5132

        assert 'isoCode' in key_list
        assert updateobj.lang_json_data['languages']['french']['isoCode'] is not None
        assert updateobj.lang_json_data['languages']['french']['isoCode'] == 'fr'

        assert 'compileSwitch' in key_list
        assert updateobj.lang_json_data['languages']['french']['compileSwitch'] is not None
        assert updateobj.lang_json_data['languages']['french']['compileSwitch'] == "FRENCH_ERRORS"

        os.remove("temp.json")

    def test12_set_default_pass(self):
        """!
        @brief Test set_default method, pass
        """
        testobj = LanguageDescriptionList(self.test_json)
        assert testobj.filename == self.test_json
        assert testobj.lang_json_data['default'] is not None
        assert testobj.lang_json_data['default']['name'] == "spanish"
        assert testobj.lang_json_data['default']['isoCode'] == "es"
        assert testobj.lang_json_data['languages'] is not None
        assert len(testobj.lang_json_data['languages']) == 1

        testobj.set_default("english")
        assert testobj.lang_json_data['default']['name'] == "english"
        assert testobj.lang_json_data['default']['isoCode'] == "en"

    def test13_set_default_fail(self):
        """!
        @brief Test set_default method, fail
        """
        testobj = LanguageDescriptionList(self.test_json)
        assert testobj.lang_json_data['languages'] is not None
        assert len(testobj.lang_json_data['languages']) == 1

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            testobj.set_default("german")
            assert output.getvalue() == "Error: You must select a current language as the default.\nAvailable languages:\n  english\n"

            assert testobj.lang_json_data['default']['name'] == "spanish"
            assert testobj.lang_json_data['default']['isoCode'] == "es"

    def test14_get_default_data(self):
        """!
        @brief Test get_default_data method
        """
        testobj = LanguageDescriptionList()
        default_lang, default_iso_code = testobj.get_default_data()
        assert testobj.lang_json_data['default']['name'] == default_lang
        assert testobj.lang_json_data['default']['isoCode'] == default_iso_code

    def test15_create_entry(self):
        """!
        @brief Test static _create_language_entry method
        """
        entry_dict = LanguageDescriptionList._create_language_entry("en", ['AU','US'], [9], [100,200], 'en', "ENGLISH_SWITCH")
        key_list = list(entry_dict.keys())
        assert len(key_list) == 6

        assert 'LANG' in key_list
        assert entry_dict['LANG'] is not None
        assert entry_dict['LANG'] == 'en'

        assert 'LANG_regions' in key_list
        assert entry_dict['LANG_regions'] is not None
        assert len(entry_dict['LANG_regions']) == 2
        assert entry_dict['LANG_regions'][0] == 'AU'
        assert entry_dict['LANG_regions'][1] == 'US'

        assert 'LANGID' in key_list
        assert entry_dict['LANGID'] is not None
        assert len(entry_dict['LANGID']) == 1
        assert entry_dict['LANGID'][0] == 9

        assert 'LANGID_regions' in key_list
        assert entry_dict['LANGID_regions'] is not None
        assert len(entry_dict['LANGID_regions']) == 2
        assert entry_dict['LANGID_regions'][0] == 100
        assert entry_dict['LANGID_regions'][1] == 200

        assert 'isoCode' in key_list
        assert entry_dict['isoCode'] is not None
        assert entry_dict['isoCode'] == 'en'

        assert 'compileSwitch' in key_list
        assert entry_dict['compileSwitch'] is not None
        assert entry_dict['compileSwitch'] == "ENGLISH_SWITCH"

    def test16_get_language_property_data(self):
        """!
        @brief Test get_language_property_data method
        """
        testobj = LanguageDescriptionList(self.test_json)
        property = testobj.get_language_property_data('english', 'LANG')
        assert isinstance(property, str)
        assert property == "en"

        property = testobj.get_language_property_data('english', 'LANG_regions')
        assert isinstance(property, list)
        assert len(property) == 13

        property = testobj.get_language_property_data('english', 'LANGID')
        assert isinstance(property, list)
        assert len(property) == 1

        property = testobj.get_language_property_data('english', 'LANGID_regions')
        assert isinstance(property, list)
        assert len(property) == 14

        property = testobj.get_language_property_data('english', 'isoCode')
        assert isinstance(property, str)
        assert property == "en"

        property = testobj.get_language_property_data('english', 'compileSwitch')
        assert isinstance(property, str)
        assert property == "ENGLISH_ERRORS"

    def test17_get_language_iso_code_data(self):
        """!
        @brief Test get_language_iso_code_data method
        """
        testobj = LanguageDescriptionList(self.test_json)
        property = testobj.get_language_iso_code_data('english')
        assert property == "en"

    def test18_get_language_l_a_n_g_data(self):
        """!
        @brief Test get_language_lang_data method
        """
        testobj = LanguageDescriptionList(self.test_json)
        lang_code, region_list = testobj.get_language_lang_data('english')
        assert lang_code == "en"
        assert len(region_list) == 13

    def test19_get_language_l_a_n_g_i_d_data(self):
        """!
        @brief Test get_language_langid_data method
        """
        testobj = LanguageDescriptionList(self.test_json)
        lang_idCodes, region_idList = testobj.get_language_langid_data('english')
        assert len(lang_idCodes) == 1
        assert lang_idCodes[0] == 9
        assert len(region_idList) == 14

    def test20_get_language_compile_switch_data(self):
        """!
        @brief Test get_language_compile_switch_data method
        """
        testobj = LanguageDescriptionList(self.test_json)
        property = testobj.get_language_compile_switch_data('english')
        assert property == "ENGLISH_ERRORS"

    def test21_get_language_property_list(self):
        """!
        @brief Test get_language_property_list method
        """
        testobj = LanguageDescriptionList()
        property_list = testobj.get_language_property_list()
        assert len(property_list) == 6
        assert 'LANG' in property_list
        assert 'LANG_regions' in property_list
        assert 'LANGID' in property_list
        assert 'LANGID_regions' in property_list
        assert 'isoCode' in property_list
        assert 'compileSwitch' in property_list

    def test22_get_language_property_return_data(self):
        """!
        @brief Test get_language_property_return_data method
        """
        testobj = LanguageDescriptionList()
        type, description, is_list = testobj.get_language_property_return_data('LANG')
        assert type == "string"
        assert not is_list
        assert isinstance(description, str)

        type, description, is_list = testobj.get_language_property_return_data('LANG_regions')
        assert type == "string"
        assert is_list
        assert isinstance(description, str)

        type, description, is_list = testobj.get_language_property_return_data('LANGID')
        assert type == "LANGID"
        assert is_list
        assert isinstance(description, str)

        type, description, is_list = testobj.get_language_property_return_data('LANGID_regions')
        assert type == "LANGID"
        assert is_list
        assert isinstance(description, str)

        type, description, is_list = testobj.get_language_property_return_data('isoCode')
        assert type == "string"
        assert not is_list
        assert isinstance(description, str)

        type, description, is_list = testobj.get_language_property_return_data('compileSwitch')
        assert type == "string"
        assert not is_list
        assert isinstance(description, str)

        type, description, is_list = testobj.get_language_property_return_data('sillyString')
        assert type is None
        assert not is_list
        assert description is None

    def test23_is_property_text(self):
        """!
        @brief Test is_language_property_text method
        """
        testobj = LanguageDescriptionList()
        assert testobj.is_language_property_text('LANG')
        assert testobj.is_language_property_text('LANG_regions')
        assert not testobj.is_language_property_text('LANGID')
        assert not testobj.is_language_property_text('LANGID_regions')
        assert testobj.is_language_property_text('isoCode')
        assert testobj.is_language_property_text('compileSwitch')
        assert not testobj.is_language_property_text('sillyString')

    def test24_get_language_property_method_name(self):
        """!
        @brief Test get_language_property_method_name method
        """
        testobj = LanguageDescriptionList()
        assert testobj.get_language_property_method_name('LANG') == "getLANGLanguage"
        assert testobj.get_language_property_method_name('LANG_regions') == "getLANGRegionList"
        assert testobj.get_language_property_method_name('LANGID') == "getLANGIDCode"
        assert testobj.get_language_property_method_name('LANGID_regions') == "getLANGIDList"
        assert testobj.get_language_property_method_name('isoCode') == "getLangIsoCode"
        assert testobj.get_language_property_method_name('compileSwitch') == "getLanguageCompileSwitch"
        assert testobj.get_language_property_method_name('sillyString') is None

    def test25_get_language_iso_property_method_name(self):
        """!
        @brief Test get_languageIsoPropertyMethodName method
        """
        testobj = LanguageDescriptionList()
        assert testobj.get_language_iso_property_method_name() == "getLangIsoCode"

    def test26_add_language(self):
        """!
        @brief Test add_language method
        """
        testobj = LanguageDescriptionList()
        testobj.add_language('umpalumpa', 'ul', ['OR', 'WW'], [0x42], [0x1042, 0x2042], 'ul', "UMPA_LUMPA_ERRORS")
        assert testobj.lang_json_data['languages']['umpalumpa'] is not None
        assert testobj.lang_json_data['languages']['umpalumpa']['LANG'] == 'ul'

        assert len(testobj.lang_json_data['languages']['umpalumpa']['LANG_regions']) == 2
        assert testobj.lang_json_data['languages']['umpalumpa']['LANG_regions'][0] == 'OR'
        assert testobj.lang_json_data['languages']['umpalumpa']['LANG_regions'][1] == 'WW'

        assert len(testobj.lang_json_data['languages']['umpalumpa']['LANGID']) == 1
        assert testobj.lang_json_data['languages']['umpalumpa']['LANGID'][0] == 0x42

        assert len(testobj.lang_json_data['languages']['umpalumpa']['LANGID_regions']) == 2
        assert testobj.lang_json_data['languages']['umpalumpa']['LANGID_regions'][0] == 0x1042
        assert testobj.lang_json_data['languages']['umpalumpa']['LANGID_regions'][1] == 0x2042

        assert testobj.lang_json_data['languages']['umpalumpa']['isoCode'] == 'ul'
        assert testobj.lang_json_data['languages']['umpalumpa']['compileSwitch'] == 'UMPA_LUMPA_ERRORS'

    def test27_get_language_list(self):
        """!
        @brief Test add_language method
        """
        testobj = LanguageDescriptionList(self.test_json)
        lang_list = testobj.get_language_list()
        assert len(lang_list) == 1
        assert "english" in lang_list

class Test03JsonLanguageListInput:
    """!
    Test input methods
    """
    @classmethod
    def setup_class(cls):
        """!
        @brief Class setup method
        """
        cls.test_json = os.path.join(TESTFILEPATH, "testdata.json")


    @classmethod
    def teardown_class(cls):
        """!
        @brief Class teardown method
        """
        if os.path.exists("jsonLanguageDescriptionList.json"):
            os.remove("jsonLanguageDescriptionList.json")   # Delete in case it was accidently created

    def test01_input_language_name_good(self):
        """!
        @brief Test _input_language_name() method, good first try
        """
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', return_value='Klingon'):
            testobj = LanguageDescriptionList()
            assert testobj._input_language_name() == 'klingon'
            assert output.getvalue() == ""

    def test02_input_language_name_blank_good_second(self):
        """!
        @brief Test _input_language_name() method, blank first try, good second try
        """
        input_str = (text for text in ["", "Romulan"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            assert testobj._input_language_name() == 'romulan'
            assert output.getvalue() == "Error: Only characters a-z are allowed in the <lang> name, try again.\n"

    def test03_input_language_name_bad_inputs(self):
        """!
        @brief Test _input_language_name() method, bad tries, good at the end try
        """
        input_str = (text for text in ["Tech33", "romulan_home", "romulan-home", "Romulan"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            assert testobj._input_language_name() == 'romulan'
            expected = "Error: Only characters a-z are allowed in the <lang> name, try again.\n"
            expected += "Error: Only characters a-z are allowed in the <lang> name, try again.\n"
            expected += "Error: Only characters a-z are allowed in the <lang> name, try again.\n"
            assert output.getvalue() == expected

    def test04_input_iso_code_good(self):
        """!
        @brief Test _input_iso_translate_code() method, good first try
        """
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', return_value='kl'):
            testobj = LanguageDescriptionList()
            assert testobj._input_iso_translate_code() == 'kl'
            assert output.getvalue() == ""

    def test05_input_iso_code_blank_good_second(self):
        """!
        @brief Test _input_iso_translate_code() method, blank first try, good second try
        """
        input_str = (text for text in ["", "RM"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            assert testobj._input_iso_translate_code() == 'rm'
            assert output.getvalue() == "Error: Only two characters a-z are allowed in the code, try again.\n"

    def test06_input_iso_code_bad_good_second(self):
        """!
        @brief Test _input_iso_translate_code() method, bad first try, good second try
        """
        input_str = (text for text in ["r4", "rrf", "k", "rm"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            assert testobj._input_iso_translate_code() == 'rm'
            expected = "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected += "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected += "Error: Only two characters a-z are allowed in the code, try again.\n"
            assert output.getvalue() == expected

    def test07_input_linux_lang_code_good(self):
        """!
        @brief Test _input_linux_lang_code() method, good first try
        """
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', return_value='kl'):
            testobj = LanguageDescriptionList()
            assert testobj._input_linux_lang_code() == 'kl'
            assert output.getvalue() == ""

    def test08_input_linux_lang_code_blank_good_second(self):
        """!
        @brief Test _input_linux_lang_code() method, blank first try, good second try
        """
        input_str = (text for text in ["", "RM"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            assert testobj._input_linux_lang_code() == 'rm'
            assert output.getvalue() == "Error: Only two characters a-z are allowed in the code, try again.\n"

    def test09_input_linux_lang_code_bad_good_second(self):
        """!
        @brief Test _input_linux_lang_code() method, bad first try, good second try
        """
        input_str = (text for text in ["r4", "rrf", "k", "rm"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            assert testobj._input_linux_lang_code() == 'rm'
            expected = "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected += "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected += "Error: Only two characters a-z are allowed in the code, try again.\n"
            assert output.getvalue() == expected

    def test10_input_linux_lang_regions_good(self):
        """!
        @brief Test _input_linux_lang_regions() method, good first try
        """
        input_str = (text for text in ["hk", ""])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            region_list = testobj._input_linux_lang_regions()
            assert len(region_list) == 1
            assert region_list[0] == 'HK'

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            assert output.getvalue() == expected

    def test11_input_linux_lang_regions_bad_then_good2(self):
        """!
        @brief Test _input_linux_lang_regions() method, blank first try, good second try
        """
        input_str = (text for text in ["r4", "rrf", "k", "rh", "RL", ""])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            region_list = testobj._input_linux_lang_regions()
            assert len(region_list) == 2
            assert region_list[0] == 'RH'
            assert region_list[1] == 'RL'

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            expected += "Error: Only two characters A-Z are allowed in the code, try again.\n"
            expected += "Error: Only two characters A-Z are allowed in the code, try again.\n"
            expected += "Error: Only two characters A-Z are allowed in the code, try again.\n"
            assert output.getvalue() == expected

    def test12_input_windows_lang_ids_good(self):
        """!
        @brief Test _input_windows_lang_ids() method, single LANGID value, single LANGID code
        """
        input_str = (text for text in ["1157", "133", "0"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            windows_idCodes, windows_idCodeList = testobj._input_windows_lang_ids()
            assert len(windows_idCodes) == 1
            assert windows_idCodes[0] == (1157 & 0xFF)
            assert len(windows_idCodeList) == 2
            assert windows_idCodeList[0] == 1157
            assert windows_idCodeList[1] == 133

            expected = "Enter Windows LANGID values. A value of 0 will exit.\n"
            assert output.getvalue() == expected

    def test13_input_windows_lang_ids_multiple_id_one_code(self):
        """!
        @brief Test _input_windows_lang_ids() method, multiple LANGID values, single LANGID code
        """
        input_str = (text for text in ["3081", "10249", "4105", "0"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            windows_idCodes, windows_idCodeList = testobj._input_windows_lang_ids()
            assert len(windows_idCodes) == 1
            assert windows_idCodes[0] == 9
            assert len(windows_idCodeList) == 3
            assert windows_idCodeList[0] == 3081
            assert windows_idCodeList[1] == 10249
            assert windows_idCodeList[2] == 4105

            expected = "Enter Windows LANGID values. A value of 0 will exit.\n"
            assert output.getvalue() == expected

    def test14_input_windows_lang_ids_multiple_id_multiple_one_code(self):
        """!
        @brief Test _input_windows_lang_ids() method, multiple LANGID values, multiple LANGID codes
        """
        input_str = (text for text in ["3081", "10249", "4105", "2060", "11276", "9", "0"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            windows_idCodes, windows_idCodeList = testobj._input_windows_lang_ids()
            assert len(windows_idCodes) == 2
            assert windows_idCodes[0] == 9
            assert windows_idCodes[1] == 12
            assert len(windows_idCodeList) == 6
            assert windows_idCodeList[0] == 3081
            assert windows_idCodeList[1] == 10249
            assert windows_idCodeList[2] == 4105
            assert windows_idCodeList[3] == 2060
            assert windows_idCodeList[4] == 11276
            assert windows_idCodeList[5] == 9

            expected = "Enter Windows LANGID values. A value of 0 will exit.\n"
            assert output.getvalue() == expected

    def test15_new_language(self):
        """!
        @brief Test new_language() method
        """
        #                              name        iso   linux  linux          Windows LANGID list           correct, commit
        #                                                code   regions
        input_str = (text for text in ["testlang", "tl", "tl",  "AU", "US", "", "3081", "10249", "4105", "0", "y", "y"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            assert testobj.new_language()

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            expected += "Enter Windows LANGID values. A value of 0 will exit.\n"
            expected += "New Entry:\n"
            expected += "{'LANG': 'tl', 'LANG_regions': ['AU', 'US'], 'LANGID': [9], "
            expected += "'LANGID_regions': [3081, 10249, 4105], 'isoCode': 'tl', 'compileSwitch': 'TESTLANG_ERRORS'}\n"
            assert output.getvalue() == expected

            assert testobj.lang_json_data['languages']['testlang'] is not None
            assert testobj.lang_json_data['languages']['testlang']['LANG'] == 'tl'

            assert len(testobj.lang_json_data['languages']['testlang']['LANG_regions']) == 2
            assert testobj.lang_json_data['languages']['testlang']['LANG_regions'][0] == 'AU'
            assert testobj.lang_json_data['languages']['testlang']['LANG_regions'][1] == 'US'

            assert len(testobj.lang_json_data['languages']['testlang']['LANGID']) == 1
            assert testobj.lang_json_data['languages']['testlang']['LANGID'][0] == (3081 & 0x0FF)

            assert len(testobj.lang_json_data['languages']['testlang']['LANGID_regions']) == 3
            assert testobj.lang_json_data['languages']['testlang']['LANGID_regions'][0] == 3081
            assert testobj.lang_json_data['languages']['testlang']['LANGID_regions'][1] == 10249
            assert testobj.lang_json_data['languages']['testlang']['LANGID_regions'][2] == 4105

            assert testobj.lang_json_data['languages']['testlang']['isoCode'] == 'tl'
            assert testobj.lang_json_data['languages']['testlang']['compileSwitch'] == 'TESTLANG_ERRORS'

    def test16_new_language_no_commit(self):
        """!
        @brief Test new_language() method
        """
        #                              name        iso   linux  linux          Windows LANGID list           correct, commit
        #                                                code   regions
        input_str = (text for text in ["newlang", "tl", "tl",  "AU", "US", "", "3081", "10249", "4105", "0", "y", "n"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            assert not testobj.new_language()

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            expected += "Enter Windows LANGID values. A value of 0 will exit.\n"
            expected += "New Entry:\n"
            expected += "{'LANG': 'tl', 'LANG_regions': ['AU', 'US'], 'LANGID': [9], "
            expected += "'LANGID_regions': [3081, 10249, 4105], 'isoCode': 'tl', 'compileSwitch': 'NEWLANG_ERRORS'}\n"
            assert output.getvalue() == expected

            lang_keys = list(testobj.lang_json_data['languages'].keys())
            assert 'newlang' not in lang_keys

    def test17_new_language_not_right(self):
        """!
        @brief Test new_language() method, no on first verification, commit second
        """
        self.max_diff = None
        #                              name        iso   linux  linux          Windows LANGID list           correct, commit
        #                                                code   regions
        input_str = (text for text in ["newlang", "tl", "tl",  "AU", "US", "", "3081", "10249", "4105", "0", "n",
                                      "newtstlang", "nl", "nl",  "FR", "ES", "", "2060", "11276", "3084", "0", "y", "y"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            assert testobj.new_language()

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            expected += "Enter Windows LANGID values. A value of 0 will exit.\n"
            expected += "New Entry:\n"
            expected += "{'LANG': 'tl', 'LANG_regions': ['AU', 'US'], 'LANGID': [9], "
            expected += "'LANGID_regions': [3081, 10249, 4105], 'isoCode': 'tl', 'compileSwitch': 'NEWLANG_ERRORS'}\n"
            expected += "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            expected += "Enter Windows LANGID values. A value of 0 will exit.\n"
            expected += "New Entry:\n"
            expected += "{'LANG': 'nl', 'LANG_regions': ['FR', 'ES'], 'LANGID': [12], "
            expected += "'LANGID_regions': [2060, 11276, 3084], 'isoCode': 'nl', 'compileSwitch': 'NEWTSTLANG_ERRORS'}\n"
            assert output.getvalue() == expected

            lang_keys = list(testobj.lang_json_data['languages'].keys())
            assert 'newlang' not in lang_keys
            assert 'newtstlang' in lang_keys

    def test18_string(self):
        """!
        @brief Test __str__() method
        """
        self.max_diff = None
        testobj = LanguageDescriptionList(self.test_json)
        test_str = str(testobj)

        expected = ""
        for lang_name, lang_data in testobj.lang_json_data['languages'].items():
            expected += lang_name
            expected += ": {\n"
            expected += str(lang_data)
            expected += "} end "
            expected += lang_name
            expected +="\n"

        expected += "Default = "
        expected += str(testobj.lang_json_data['default']['name'])

        assert test_str == expected

class Test02JsonLanguageListInput:
    @classmethod
    def setup_class(cls):
        cls.test_json = os.path.join(TESTFILEPATH, "testdata.json")


    @classmethod
    def teardown_class(cls):
        if os.path.exists("jsonLanguageDescriptionList.json"):
            os.remove("jsonLanguageDescriptionList.json")   # Delete in case it was accidently created


    """!
    @brief Unit test for the LanguageDescriptionList class input functions
    """
    def test01_input_language_name_good(self):
        """!
        @brief Test _input_language_name() method, good first try
        """
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', return_value='Klingon'):
            testobj = LanguageDescriptionList()
            assert testobj._input_language_name() == 'klingon'
            assert output.getvalue() == ""

    def test02_input_language_name_blank_good_second(self):
        """!
        @brief Test _input_language_name() method, blank first try, good second try
        """
        input_str = (text for text in ["", "Romulan"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            assert testobj._input_language_name() == 'romulan'
            assert output.getvalue() == "Error: Only characters a-z are allowed in the <lang> name, try again.\n"

    def test03_input_language_name_bad_good_second(self):
        """!
        @brief Test _input_language_name() method, bad tries, good at the end try
        """
        input_str = (text for text in ["Tech33", "romulan_home", "romulan-home", "Romulan"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            assert testobj._input_language_name() == 'romulan'
            expected = "Error: Only characters a-z are allowed in the <lang> name, try again.\n"
            expected += "Error: Only characters a-z are allowed in the <lang> name, try again.\n"
            expected += "Error: Only characters a-z are allowed in the <lang> name, try again.\n"
            assert output.getvalue() == expected

    def test04_input_iso_code_good(self):
        """!
        @brief Test _input_iso_translate_code() method, good first try
        """
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', return_value='kl'):
            testobj = LanguageDescriptionList()
            assert testobj._input_iso_translate_code() == 'kl'
            assert output.getvalue() == ""

    def test05_input_iso_code_blank_good_second(self):
        """!
        @brief Test _input_iso_translate_code() method, blank first try, good second try
        """
        input_str = (text for text in ["", "RM"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            assert testobj._input_iso_translate_code() == 'rm'
            assert output.getvalue() == "Error: Only two characters a-z are allowed in the code, try again.\n"

    def test06_input_iso_code_bad_good_second(self):
        """!
        @brief Test _input_iso_translate_code() method, bad first try, good second try
        """
        input_str = (text for text in ["r4", "rrf", "k", "rm"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            assert testobj._input_iso_translate_code() == 'rm'
            expected = "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected += "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected += "Error: Only two characters a-z are allowed in the code, try again.\n"
            assert output.getvalue() == expected

    def test07_input_linux_lang_code_good(self):
        """!
        @brief Test _input_linux_lang_code() method, good first try
        """
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', return_value='kl'):
            testobj = LanguageDescriptionList()
            assert testobj._input_linux_lang_code() == 'kl'
            assert output.getvalue() == ""

    def test08_input_linux_lang_code_blank_good_second(self):
        """!
        @brief Test _input_linux_lang_code() method, blank first try, good second try
        """
        input_str = (text for text in ["", "RM"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            assert testobj._input_linux_lang_code() == 'rm'
            assert output.getvalue() == "Error: Only two characters a-z are allowed in the code, try again.\n"

    def test09_input_linux_lang_code_bad_good_second(self):
        """!
        @brief Test _input_linux_lang_code() method, bad first try, good second try
        """
        input_str = (text for text in ["r4", "rrf", "k", "rm"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            assert testobj._input_linux_lang_code() == 'rm'
            expected = "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected += "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected += "Error: Only two characters a-z are allowed in the code, try again.\n"
            assert output.getvalue() == expected

    def test10_input_linux_lang_regions_good(self):
        """!
        @brief Test _input_linux_lang_regions() method, good first try
        """
        input_str = (text for text in ["hk", ""])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            region_list = testobj._input_linux_lang_regions()
            assert len(region_list) == 1
            assert region_list[0] == 'HK'

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            assert output.getvalue() == expected

    def test11_input_linux_lang_regions_bad_then_good2(self):
        """!
        @brief Test _input_linux_lang_regions() method, blank first try, good second try
        """
        input_str = (text for text in ["r4", "rrf", "k", "rh", "RL", ""])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            region_list = testobj._input_linux_lang_regions()
            assert len(region_list) == 2
            assert region_list[0] == 'RH'
            assert region_list[1] == 'RL'

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            expected += "Error: Only two characters A-Z are allowed in the code, try again.\n"
            expected += "Error: Only two characters A-Z are allowed in the code, try again.\n"
            expected += "Error: Only two characters A-Z are allowed in the code, try again.\n"
            assert output.getvalue() == expected

    def test12_input_windows_lang_ids_good(self):
        """!
        @brief Test _input_windows_lang_ids() method, single LANGID value, single LANGID code
        """
        input_str = (text for text in ["1157", "0"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            windows_idCodes, windows_idCodeList = testobj._input_windows_lang_ids()
            assert len(windows_idCodes) == 1
            assert windows_idCodes[0] == (1157 & 0xFF)
            assert len(windows_idCodeList) == 1
            assert windows_idCodeList[0] == 1157

            expected = "Enter Windows LANGID values. A value of 0 will exit.\n"
            assert output.getvalue() == expected

    def test13_input_windows_lang_ids_multiple_id_one_code(self):
        """!
        @brief Test _input_windows_lang_ids() method, multiple LANGID values, single LANGID code
        """
        input_str = (text for text in ["3081", "10249", "4105", "0"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            windows_idCodes, windows_idCodeList = testobj._input_windows_lang_ids()
            assert len(windows_idCodes) == 1
            assert windows_idCodes[0] == 9
            assert len(windows_idCodeList) == 3
            assert windows_idCodeList[0] == 3081
            assert windows_idCodeList[1] == 10249
            assert windows_idCodeList[2] == 4105

            expected = "Enter Windows LANGID values. A value of 0 will exit.\n"
            assert output.getvalue() == expected

    def test14_input_windows_lang_ids_multiple_id_multiple_one_code(self):
        """!
        @brief Test _input_windows_lang_ids() method, multiple LANGID values, multiple LANGID codes
        """
        input_str = (text for text in ["3081", "10249", "4105", "2060", "11276", "0"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            windows_idCodes, windows_idCodeList = testobj._input_windows_lang_ids()
            assert len(windows_idCodes) == 2
            assert windows_idCodes[0] == 9
            assert windows_idCodes[1] == 12
            assert len(windows_idCodeList) == 5
            assert windows_idCodeList[0] == 3081
            assert windows_idCodeList[1] == 10249
            assert windows_idCodeList[2] == 4105
            assert windows_idCodeList[3] == 2060
            assert windows_idCodeList[4] == 11276

            expected = "Enter Windows LANGID values. A value of 0 will exit.\n"
            assert output.getvalue() == expected

    def test15_new_language(self):
        """!
        @brief Test new_language() method
        """
        #                              name        iso   linux  linux          Windows LANGID list           correct, commit
        #                                                code   regions
        input_str = (text for text in ["testlang", "tl", "tl",  "AU", "US", "", "3081", "10249", "4105", "0", "y", "y"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            assert testobj.new_language()

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            expected += "Enter Windows LANGID values. A value of 0 will exit.\n"
            expected += "New Entry:\n"
            expected += "{'LANG': 'tl', 'LANG_regions': ['AU', 'US'], 'LANGID': [9], "
            expected += "'LANGID_regions': [3081, 10249, 4105], 'isoCode': 'tl', 'compileSwitch': 'TESTLANG_ERRORS'}\n"
            assert output.getvalue() == expected

            assert testobj.lang_json_data['languages']['testlang'] is not None
            assert testobj.lang_json_data['languages']['testlang']['LANG'] == 'tl'

            assert len(testobj.lang_json_data['languages']['testlang']['LANG_regions']) == 2
            assert testobj.lang_json_data['languages']['testlang']['LANG_regions'][0] == 'AU'
            assert testobj.lang_json_data['languages']['testlang']['LANG_regions'][1] == 'US'

            assert len(testobj.lang_json_data['languages']['testlang']['LANGID']) == 1
            assert testobj.lang_json_data['languages']['testlang']['LANGID'][0] == (3081 & 0x0FF)

            assert len(testobj.lang_json_data['languages']['testlang']['LANGID_regions']) == 3
            assert testobj.lang_json_data['languages']['testlang']['LANGID_regions'][0] == 3081
            assert testobj.lang_json_data['languages']['testlang']['LANGID_regions'][1] == 10249
            assert testobj.lang_json_data['languages']['testlang']['LANGID_regions'][2] == 4105

            assert testobj.lang_json_data['languages']['testlang']['isoCode'] == 'tl'
            assert testobj.lang_json_data['languages']['testlang']['compileSwitch'] == 'TESTLANG_ERRORS'

    def test16_new_language_no_commit(self):
        """!
        @brief Test new_language() method
        """
        #                              name        iso   linux  linux          Windows LANGID list           correct, commit
        #                                                code   regions
        input_str = (text for text in ["newlang", "tl", "tl",  "AU", "US", "", "3081", "10249", "4105", "0", "y", "n"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            assert not testobj.new_language()

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            expected += "Enter Windows LANGID values. A value of 0 will exit.\n"
            expected += "New Entry:\n"
            expected += "{'LANG': 'tl', 'LANG_regions': ['AU', 'US'], 'LANGID': [9], "
            expected += "'LANGID_regions': [3081, 10249, 4105], 'isoCode': 'tl', 'compileSwitch': 'NEWLANG_ERRORS'}\n"
            assert output.getvalue() == expected

            lang_keys = list(testobj.lang_json_data['languages'].keys())
            assert 'newlang' not in lang_keys

    def test17_new_language_not_right(self):
        """!
        @brief Test new_language() method, no on first verification, commit second
        """
        self.max_diff = None
        #                              name        iso   linux  linux          Windows LANGID list           correct, commit
        #                                                code   regions
        input_str = (text for text in ["newlang", "tl", "tl",  "AU", "US", "", "3081", "10249", "4105", "0", "n",
                                      "newtstlang", "nl", "nl",  "FR", "ES", "", "2060", "11276", "3084", "0", "y", "y"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            assert testobj.new_language()

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            expected += "Enter Windows LANGID values. A value of 0 will exit.\n"
            expected += "New Entry:\n"
            expected += "{'LANG': 'tl', 'LANG_regions': ['AU', 'US'], 'LANGID': [9], "
            expected += "'LANGID_regions': [3081, 10249, 4105], 'isoCode': 'tl', 'compileSwitch': 'NEWLANG_ERRORS'}\n"
            expected += "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            expected += "Enter Windows LANGID values. A value of 0 will exit.\n"
            expected += "New Entry:\n"
            expected += "{'LANG': 'nl', 'LANG_regions': ['FR', 'ES'], 'LANGID': [12], "
            expected += "'LANGID_regions': [2060, 11276, 3084], 'isoCode': 'nl', 'compileSwitch': 'NEWTSTLANG_ERRORS'}\n"
            assert output.getvalue() == expected

            lang_keys = list(testobj.lang_json_data['languages'].keys())
            assert 'newlang' not in lang_keys
            assert 'newtstlang' in lang_keys

    def test18_string(self):
        """!
        @brief Test __str__() method
        """
        self.max_diff = None
        testobj = LanguageDescriptionList(self.test_json)
        test_str = str(testobj)

        expected = ""
        for lang_name, lang_data in testobj.lang_json_data['languages'].items():
            expected += lang_name
            expected += ": {\n"
            expected += str(lang_data)
            expected += "} end "
            expected += lang_name
            expected +="\n"

        expected += "Default = "
        expected += str(testobj.lang_json_data['default']['name'])

        assert test_str == expected

    def test19_input_windows_lang_ids_multiple_id_multiple_code(self):
        """!
        @brief Test _input_windows_lang_ids() method, multiple LANGID values, multiple LANGID codes
        """
        input_str = (text for text in ["3081", "2576", "2576", "0"])
        def test_mock_in(prompt):
            return next(input_str)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', test_mock_in):
            testobj = LanguageDescriptionList()
            windows_idCodes, windows_idCodeList = testobj._input_windows_lang_ids()
            assert len(windows_idCodes) == 2
            assert windows_idCodes[0] == 9
            assert windows_idCodes[1] == 16
            assert len(windows_idCodeList) == 2
            assert windows_idCodeList[0] == 3081
            assert windows_idCodeList[1] == 2576

            expected = "Enter Windows LANGID values. A value of 0 will exit.\n"
            assert output.getvalue() == expected

# pylint: enable=protected-access
