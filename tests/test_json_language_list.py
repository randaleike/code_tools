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

import pytest
from unittest.mock import patch, MagicMock, mock_open

from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList

from tests.dir_init import TESTFILEPATH

class Test01JsonLanguageList:
    """!
    @brief Unit test for the LanguageDescriptionList class
    """

    @classmethod
    def setup_class(cls):
        cls.testJson = os.path.join(TESTFILEPATH, "testdata.json")


    @classmethod
    def teardown_class(cls):
        if os.path.exists("jsonLanguageDescriptionList.json"):
            os.remove("jsonLanguageDescriptionList.json")   # Delete in case it was accidently created


    def test01DefaultConstructor(self):
        """!
        @brief Test Default constructor()
        """
        testobj = LanguageDescriptionList()
        pytest.raises(FileNotFoundError)
        assert testobj.filename == "jsonLanguageDescriptionList.json"
        assert testobj.langJsonData['default'] is not None
        assert testobj.langJsonData['default']['name'] == "english"
        assert testobj.langJsonData['default']['isoCode'] == "en"
        assert testobj.langJsonData['languages'] is not None
        assert len(testobj.langJsonData['languages']) == 0

    def test02ConstructorWithFile(self):
        """!
        @brief Test constructor() with file name
        """
        testobj = LanguageDescriptionList(self.testJson)
        assert testobj.filename == self.testJson
        assert testobj.langJsonData['default'] is not None
        assert testobj.langJsonData['default']['name'] == "spanish"
        assert testobj.langJsonData['default']['isoCode'] == "es"
        assert testobj.langJsonData['languages'] is not None
        assert len(testobj.langJsonData['languages']) == 1

        assert testobj.langJsonData['languages']['english'] is not None
        keyList = list(testobj.langJsonData['languages']['english'].keys())
        assert len(keyList) == 6

        assert 'LANG' in keyList
        assert testobj.langJsonData['languages']['english']['LANG'] is not None
        assert testobj.langJsonData['languages']['english']['LANG'] == 'en'

        assert 'LANG_regions' in keyList
        assert testobj.langJsonData['languages']['english']['LANG_regions'] is not None
        assert len(testobj.langJsonData['languages']['english']['LANG_regions']) == 13
        assert testobj.langJsonData['languages']['english']['LANG_regions'][0] == 'AU'
        assert testobj.langJsonData['languages']['english']['LANG_regions'][12] == 'ZW'

        assert 'LANGID' in keyList
        assert testobj.langJsonData['languages']['english']['LANGID'] is not None
        assert len(testobj.langJsonData['languages']['english']['LANGID']) == 1
        assert testobj.langJsonData['languages']['english']['LANGID'][0] == 9

        assert 'LANGID_regions' in keyList
        assert testobj.langJsonData['languages']['english']['LANGID_regions'] is not None
        assert len(testobj.langJsonData['languages']['english']['LANGID_regions']) == 14
        assert testobj.langJsonData['languages']['english']['LANGID_regions'][0] == 3081
        assert testobj.langJsonData['languages']['english']['LANGID_regions'][13] == 12297

        assert 'isoCode' in keyList
        assert testobj.langJsonData['languages']['english']['isoCode'] is not None
        assert testobj.langJsonData['languages']['english']['isoCode'] == 'en'

        assert 'compileSwitch' in keyList
        assert testobj.langJsonData['languages']['english']['compileSwitch'] is not None
        assert testobj.langJsonData['languages']['english']['compileSwitch'] == "ENGLISH_ERRORS"

    def test03Clear(self):
        """!
        @brief Test clear method
        """
        testobj = LanguageDescriptionList(self.testJson)
        assert testobj.filename == self.testJson
        assert testobj.langJsonData['default'] is not None
        assert testobj.langJsonData['default']['isoCode'] == "es"
        assert testobj.langJsonData['languages'] is not None
        assert len(testobj.langJsonData['languages']) == 1

        testobj.clear()
        assert testobj.filename == self.testJson
        assert testobj.langJsonData['default'] is not None
        assert testobj.langJsonData['default']['name'] == "english"
        assert testobj.langJsonData['default']['isoCode'] == "en"
        assert testobj.langJsonData['languages'] is not None
        assert len(testobj.langJsonData['languages']) == 0

    def test04Printerror(self):
        """!
        @brief Test _printError method
        """
        testobj = LanguageDescriptionList()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            testobj._printError("test error")
            assert output.getvalue() == "Error: test error\n"

    def test05GetCommitOverwriteFlagNo(self):
        """!
        @brief Test _getCommitOverWriteFlag method, no answer
        """
        testobj = LanguageDescriptionList()
        with patch('builtins.input', side_effect='n') as inMock:
            assert not testobj._getCommitOverWriteFlag("testEntry")
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='N') as inMock:
            assert not testobj._getCommitOverWriteFlag("testEntry")
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='no') as inMock:
            assert not testobj._getCommitOverWriteFlag("testEntry")
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='NO') as inMock:
            assert not testobj._getCommitOverWriteFlag("testEntry")
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='No') as inMock:
            assert not testobj._getCommitOverWriteFlag("testEntry")
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

    def test06GetCommitOverwriteFlagYes(self):
        """!
        @brief Test _getCommitOverWriteFlag method, Yes answer
        """
        testobj = LanguageDescriptionList()
        with patch('builtins.input', side_effect='y') as inMock:
            assert testobj._getCommitOverWriteFlag("testEntry")
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='Y') as inMock:
            assert testobj._getCommitOverWriteFlag("testEntry")
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='yes') as inMock:
            assert testobj._getCommitOverWriteFlag("testEntry")
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='YES') as inMock:
            assert testobj._getCommitOverWriteFlag("testEntry")
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='Yes') as inMock:
            assert testobj._getCommitOverWriteFlag("testEntry")
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

    def test07GetCommitOverwriteFlagOverride(self):
        """!
        @brief Test _getCommitOverWriteFlag method, override=True
        """
        testobj = LanguageDescriptionList()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            assert testobj._getCommitOverWriteFlag("testEntry", True)
            assert output.getvalue() == ""

    def test08GetCommitNewFlagNo(self):
        """!
        @brief Test _getCommitNewFlag method, no answer
        """
        testobj = LanguageDescriptionList()
        with patch('builtins.input', side_effect='n') as inMock:
            assert not testobj._getCommitNewFlag("testEntry")
            inMock.assert_called_once_with("Add new testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='N') as inMock:
            assert not testobj._getCommitNewFlag("testEntry")
            inMock.assert_called_once_with("Add new testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='no') as inMock:
            assert not testobj._getCommitNewFlag("testEntry")
            inMock.assert_called_once_with("Add new testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='NO') as inMock:
            assert not testobj._getCommitNewFlag("testEntry")
            inMock.assert_called_once_with("Add new testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='No') as inMock:
            assert not testobj._getCommitNewFlag("testEntry")
            inMock.assert_called_once_with("Add new testEntry entry? [Y/N]")

    def test09GetCommitNewFlagYes(self):
        """!
        @brief Test _getCommitNewFlag method, Yes answer
        """
        testobj = LanguageDescriptionList()
        with patch('builtins.input', side_effect='y') as inMock:
            assert testobj._getCommitNewFlag("testEntry")
            inMock.assert_called_once_with("Add new testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='Y') as inMock:
            assert testobj._getCommitNewFlag("testEntry")
            inMock.assert_called_once_with("Add new testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='yes') as inMock:
            assert testobj._getCommitNewFlag("testEntry")
            inMock.assert_called_once_with("Add new testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='YES') as inMock:
            assert testobj._getCommitNewFlag("testEntry")
            inMock.assert_called_once_with("Add new testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='Yes') as inMock:
            assert testobj._getCommitNewFlag("testEntry")
            inMock.assert_called_once_with("Add new testEntry entry? [Y/N]")

    def test10GetCommitFlag(self):
        """!
        @brief Test _getCommitFlag method
        """
        testobj = LanguageDescriptionList()
        with patch('builtins.input', side_effect='y') as inMock:
            assert testobj._getCommitFlag("testEntry",['testEntry'])
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")
        with patch('builtins.input', side_effect='n') as inMock:
            assert not testobj._getCommitFlag("testEntry",['testEntry'])
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='y') as inMock:
            assert testobj._getCommitFlag("test33",['testEntry'])
            inMock.assert_called_once_with("Add new test33 entry? [Y/N]")
        with patch('builtins.input', side_effect='n') as inMock:
            assert not testobj._getCommitFlag("test33",['testEntry'])
            inMock.assert_called_once_with("Add new test33 entry? [Y/N]")

        assert testobj._getCommitFlag("testEntry",['testEntry'], True)

        with patch('builtins.input', side_effect='y') as inMock:
            assert testobj._getCommitFlag("test33",['testEntry'], True)
            inMock.assert_called_once_with("Add new test33 entry? [Y/N]")
        with patch('builtins.input', side_effect='n') as inMock:
            assert not testobj._getCommitFlag("test33",['testEntry'], True)
            inMock.assert_called_once_with("Add new test33 entry? [Y/N]")

    def test11Update(self):
        """!
        @brief Test update method
        """
        testobj = LanguageDescriptionList("temp.json")
        assert testobj.filename == "temp.json"
        testobj.langJsonData['languages']['french'] = {'LANG':'fr', 'LANG_regions':['FR'],
                                                       'LANGID': [12], 'LANGID_regions': [1036, 5132],
                                                       'isoCode': 'fr', 'compileSwitch': "FRENCH_ERRORS"}
        testobj.update()

        updateobj = LanguageDescriptionList("temp.json")
        assert updateobj.filename == "temp.json"
        assert updateobj.langJsonData['default'] is not None
        assert updateobj.langJsonData['default']['name'] == "english"
        assert updateobj.langJsonData['default']['isoCode'] == "en"
        assert updateobj.langJsonData['languages'] is not None
        assert len(updateobj.langJsonData['languages']) == 1

        assert updateobj.langJsonData['languages']['french'] is not None
        keyList = list(updateobj.langJsonData['languages']['french'].keys())
        assert len(keyList) == 6

        assert 'LANG' in keyList
        assert updateobj.langJsonData['languages']['french']['LANG'] is not None
        assert updateobj.langJsonData['languages']['french']['LANG'] == 'fr'

        assert 'LANG_regions' in keyList
        assert updateobj.langJsonData['languages']['french']['LANG_regions'] is not None
        assert len(updateobj.langJsonData['languages']['french']['LANG_regions']) == 1
        assert updateobj.langJsonData['languages']['french']['LANG_regions'][0] == 'FR'

        assert 'LANGID' in keyList
        assert updateobj.langJsonData['languages']['french']['LANGID'] is not None
        assert len(updateobj.langJsonData['languages']['french']['LANGID']) == 1
        assert updateobj.langJsonData['languages']['french']['LANGID'][0] == 12

        assert 'LANGID_regions' in keyList
        assert updateobj.langJsonData['languages']['french']['LANGID_regions'] is not None
        assert len(updateobj.langJsonData['languages']['french']['LANGID_regions']) == 2
        assert updateobj.langJsonData['languages']['french']['LANGID_regions'][0] == 1036
        assert updateobj.langJsonData['languages']['french']['LANGID_regions'][1] == 5132

        assert 'isoCode' in keyList
        assert updateobj.langJsonData['languages']['french']['isoCode'] is not None
        assert updateobj.langJsonData['languages']['french']['isoCode'] == 'fr'

        assert 'compileSwitch' in keyList
        assert updateobj.langJsonData['languages']['french']['compileSwitch'] is not None
        assert updateobj.langJsonData['languages']['french']['compileSwitch'] == "FRENCH_ERRORS"

        os.remove("temp.json")

    def test12SetDefaultPass(self):
        """!
        @brief Test setDefault method, pass
        """
        testobj = LanguageDescriptionList(self.testJson)
        assert testobj.filename == self.testJson
        assert testobj.langJsonData['default'] is not None
        assert testobj.langJsonData['default']['name'] == "spanish"
        assert testobj.langJsonData['default']['isoCode'] == "es"
        assert testobj.langJsonData['languages'] is not None
        assert len(testobj.langJsonData['languages']) == 1

        testobj.setDefault("english")
        assert testobj.langJsonData['default']['name'] == "english"
        assert testobj.langJsonData['default']['isoCode'] == "en"

    def test13SetDefaultFail(self):
        """!
        @brief Test setDefault method, fail
        """
        testobj = LanguageDescriptionList(self.testJson)
        assert testobj.langJsonData['languages'] is not None
        assert len(testobj.langJsonData['languages']) == 1

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            testobj.setDefault("german")
            assert output.getvalue() == "Error: You must select a current language as the default.\nAvailable languages:\n  english\n"

            assert testobj.langJsonData['default']['name'] == "spanish"
            assert testobj.langJsonData['default']['isoCode'] == "es"

    def test14GetDefaultData(self):
        """!
        @brief Test getDefaultData method
        """
        testobj = LanguageDescriptionList()
        defaultLang, defaultIsoCode = testobj.getDefaultData()
        assert testobj.langJsonData['default']['name'] == defaultLang
        assert testobj.langJsonData['default']['isoCode'] == defaultIsoCode

    def test15CreateEntry(self):
        """!
        @brief Test static _createLanguageEntry method
        """
        entryDict = LanguageDescriptionList._createLanguageEntry("en", ['AU','US'], [9], [100,200], 'en', "ENGLISH_SWITCH")
        keyList = list(entryDict.keys())
        assert len(keyList) == 6

        assert 'LANG' in keyList
        assert entryDict['LANG'] is not None
        assert entryDict['LANG'] == 'en'

        assert 'LANG_regions' in keyList
        assert entryDict['LANG_regions'] is not None
        assert len(entryDict['LANG_regions']) == 2
        assert entryDict['LANG_regions'][0] == 'AU'
        assert entryDict['LANG_regions'][1] == 'US'

        assert 'LANGID' in keyList
        assert entryDict['LANGID'] is not None
        assert len(entryDict['LANGID']) == 1
        assert entryDict['LANGID'][0] == 9

        assert 'LANGID_regions' in keyList
        assert entryDict['LANGID_regions'] is not None
        assert len(entryDict['LANGID_regions']) == 2
        assert entryDict['LANGID_regions'][0] == 100
        assert entryDict['LANGID_regions'][1] == 200

        assert 'isoCode' in keyList
        assert entryDict['isoCode'] is not None
        assert entryDict['isoCode'] == 'en'

        assert 'compileSwitch' in keyList
        assert entryDict['compileSwitch'] is not None
        assert entryDict['compileSwitch'] == "ENGLISH_SWITCH"

    def test16GetLanguagePropertyData(self):
        """!
        @brief Test getLanguagePropertyData method
        """
        testobj = LanguageDescriptionList(self.testJson)
        property = testobj.getLanguagePropertyData('english', 'LANG')
        assert isinstance(property, str)
        assert property == "en"

        property = testobj.getLanguagePropertyData('english', 'LANG_regions')
        assert isinstance(property, list)
        assert len(property) == 13

        property = testobj.getLanguagePropertyData('english', 'LANGID')
        assert isinstance(property, list)
        assert len(property) == 1

        property = testobj.getLanguagePropertyData('english', 'LANGID_regions')
        assert isinstance(property, list)
        assert len(property) == 14

        property = testobj.getLanguagePropertyData('english', 'isoCode')
        assert isinstance(property, str)
        assert property == "en"

        property = testobj.getLanguagePropertyData('english', 'compileSwitch')
        assert isinstance(property, str)
        assert property == "ENGLISH_ERRORS"

    def test17GetLanguageIsoCodeData(self):
        """!
        @brief Test getLanguageIsoCodeData method
        """
        testobj = LanguageDescriptionList(self.testJson)
        property = testobj.getLanguageIsoCodeData('english')
        assert property == "en"

    def test18GetLanguageLANGData(self):
        """!
        @brief Test getLanguageLANGData method
        """
        testobj = LanguageDescriptionList(self.testJson)
        langCode, regionList = testobj.getLanguageLANGData('english')
        assert langCode == "en"
        assert len(regionList) == 13

    def test19GetLanguageLANGIDData(self):
        """!
        @brief Test getLanguageLANGIDData method
        """
        testobj = LanguageDescriptionList(self.testJson)
        langIdCodes, regionIdList = testobj.getLanguageLANGIDData('english')
        assert len(langIdCodes) == 1
        assert langIdCodes[0] == 9
        assert len(regionIdList) == 14

    def test20GetLanguageCompileSwitchData(self):
        """!
        @brief Test getLanguageCompileSwitchData method
        """
        testobj = LanguageDescriptionList(self.testJson)
        property = testobj.getLanguageCompileSwitchData('english')
        assert property == "ENGLISH_ERRORS"

    def test21GetLanguagePropertyList(self):
        """!
        @brief Test getLanguagePropertyList method
        """
        testobj = LanguageDescriptionList()
        propertyList = testobj.getLanguagePropertyList()
        assert len(propertyList) == 6
        assert 'LANG' in propertyList
        assert 'LANG_regions' in propertyList
        assert 'LANGID' in propertyList
        assert 'LANGID_regions' in propertyList
        assert 'isoCode' in propertyList
        assert 'compileSwitch' in propertyList

    def test22GetLanguagePropertyReturnData(self):
        """!
        @brief Test getLanguagePropertyReturnData method
        """
        testobj = LanguageDescriptionList()
        type, description, isList = testobj.getLanguagePropertyReturnData('LANG')
        assert type == "string"
        assert not isList
        assert isinstance(description, str)

        type, description, isList = testobj.getLanguagePropertyReturnData('LANG_regions')
        assert type == "string"
        assert isList
        assert isinstance(description, str)

        type, description, isList = testobj.getLanguagePropertyReturnData('LANGID')
        assert type == "LANGID"
        assert isList
        assert isinstance(description, str)

        type, description, isList = testobj.getLanguagePropertyReturnData('LANGID_regions')
        assert type == "LANGID"
        assert isList
        assert isinstance(description, str)

        type, description, isList = testobj.getLanguagePropertyReturnData('isoCode')
        assert type == "string"
        assert not isList
        assert isinstance(description, str)

        type, description, isList = testobj.getLanguagePropertyReturnData('compileSwitch')
        assert type == "string"
        assert not isList
        assert isinstance(description, str)

        type, description, isList = testobj.getLanguagePropertyReturnData('sillyString')
        assert type is None
        assert not isList
        assert description is None

    def test23IsPropertyText(self):
        """!
        @brief Test isLanguagePropertyText method
        """
        testobj = LanguageDescriptionList()
        assert testobj.isLanguagePropertyText('LANG')
        assert testobj.isLanguagePropertyText('LANG_regions')
        assert not testobj.isLanguagePropertyText('LANGID')
        assert not testobj.isLanguagePropertyText('LANGID_regions')
        assert testobj.isLanguagePropertyText('isoCode')
        assert testobj.isLanguagePropertyText('compileSwitch')
        assert not testobj.isLanguagePropertyText('sillyString')

    def test24GetLanguagePropertyMethodName(self):
        """!
        @brief Test getLanguagePropertyMethodName method
        """
        testobj = LanguageDescriptionList()
        assert testobj.getLanguagePropertyMethodName('LANG') == "getLANGLanguage"
        assert testobj.getLanguagePropertyMethodName('LANG_regions') == "getLANGRegionList"
        assert testobj.getLanguagePropertyMethodName('LANGID') == "getLANGIDCode"
        assert testobj.getLanguagePropertyMethodName('LANGID_regions') == "getLANGIDList"
        assert testobj.getLanguagePropertyMethodName('isoCode') == "getLangIsoCode"
        assert testobj.getLanguagePropertyMethodName('compileSwitch') == "getLanguageCompileSwitch"
        assert testobj.getLanguagePropertyMethodName('sillyString') is None

    def test25GetLanguageIsoPropertyMethodName(self):
        """!
        @brief Test getLanguageIsoPropertyMethodName method
        """
        testobj = LanguageDescriptionList()
        assert testobj.getLanguageIsoPropertyMethodName() == "getLangIsoCode"

    def test26AddLanguage(self):
        """!
        @brief Test addLanguage method
        """
        testobj = LanguageDescriptionList()
        testobj.addLanguage('umpalumpa', 'ul', ['OR', 'WW'], [0x42], [0x1042, 0x2042], 'ul', "UMPA_LUMPA_ERRORS")
        assert testobj.langJsonData['languages']['umpalumpa'] is not None
        assert testobj.langJsonData['languages']['umpalumpa']['LANG'] == 'ul'

        assert len(testobj.langJsonData['languages']['umpalumpa']['LANG_regions']) == 2
        assert testobj.langJsonData['languages']['umpalumpa']['LANG_regions'][0] == 'OR'
        assert testobj.langJsonData['languages']['umpalumpa']['LANG_regions'][1] == 'WW'

        assert len(testobj.langJsonData['languages']['umpalumpa']['LANGID']) == 1
        assert testobj.langJsonData['languages']['umpalumpa']['LANGID'][0] == 0x42

        assert len(testobj.langJsonData['languages']['umpalumpa']['LANGID_regions']) == 2
        assert testobj.langJsonData['languages']['umpalumpa']['LANGID_regions'][0] == 0x1042
        assert testobj.langJsonData['languages']['umpalumpa']['LANGID_regions'][1] == 0x2042

        assert testobj.langJsonData['languages']['umpalumpa']['isoCode'] == 'ul'
        assert testobj.langJsonData['languages']['umpalumpa']['compileSwitch'] == 'UMPA_LUMPA_ERRORS'

    def test27GetLanguageList(self):
        """!
        @brief Test addLanguage method
        """
        testobj = LanguageDescriptionList(self.testJson)
        langList = testobj.getLanguageList()
        assert len(langList) == 1
        assert "english" in langList

class Test02JsonLanguageListInput:
    """!
    Test input methods
    """
    @classmethod
    def setup_class(cls):
        cls.testJson = os.path.join(TESTFILEPATH, "testdata.json")


    @classmethod
    def teardown_class(cls):
        if os.path.exists("jsonLanguageDescriptionList.json"):
            os.remove("jsonLanguageDescriptionList.json")   # Delete in case it was accidently created


    """!
    @brief Unit test for the LanguageDescriptionList class input functions
    """
    def test01InputLanguageNameGood(self):
        """!
        @brief Test _inputLanguageName() method, good first try
        """
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', return_value='Klingon'):
            testobj = LanguageDescriptionList()
            assert testobj._inputLanguageName() == 'klingon'
            assert output.getvalue() == ""

    def test02InputLanguageNameBlankGoodSecond(self):
        """!
        @brief Test _inputLanguageName() method, blank first try, good second try
        """
        inputStr = (text for text in ["", "Romulan"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            assert testobj._inputLanguageName() == 'romulan'
            assert output.getvalue() == "Error: Only characters a-z are allowed in the <lang> name, try again.\n"

    def test03InputLanguageNameBadInputs(self):
        """!
        @brief Test _inputLanguageName() method, bad tries, good at the end try
        """
        inputStr = (text for text in ["Tech33", "romulan_home", "romulan-home", "Romulan"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            assert testobj._inputLanguageName() == 'romulan'
            expected = "Error: Only characters a-z are allowed in the <lang> name, try again.\n"
            expected += "Error: Only characters a-z are allowed in the <lang> name, try again.\n"
            expected += "Error: Only characters a-z are allowed in the <lang> name, try again.\n"
            assert output.getvalue() == expected

    def test04InputIsoCodeGood(self):
        """!
        @brief Test _inputIsoTranslateCode() method, good first try
        """
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', return_value='kl'):
            testobj = LanguageDescriptionList()
            assert testobj._inputIsoTranslateCode() == 'kl'
            assert output.getvalue() == ""

    def test05InputIsoCodeBlankGoodSecond(self):
        """!
        @brief Test _inputIsoTranslateCode() method, blank first try, good second try
        """
        inputStr = (text for text in ["", "RM"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            assert testobj._inputIsoTranslateCode() == 'rm'
            assert output.getvalue() == "Error: Only two characters a-z are allowed in the code, try again.\n"

    def test06InputIsoCodeBadGoodSecond(self):
        """!
        @brief Test _inputIsoTranslateCode() method, bad first try, good second try
        """
        inputStr = (text for text in ["r4", "rrf", "k", "rm"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            assert testobj._inputIsoTranslateCode() == 'rm'
            expected = "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected += "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected += "Error: Only two characters a-z are allowed in the code, try again.\n"
            assert output.getvalue() == expected

    def test07InputLinuxLangCodeGood(self):
        """!
        @brief Test _inputLinuxLangCode() method, good first try
        """
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', return_value='kl'):
            testobj = LanguageDescriptionList()
            assert testobj._inputLinuxLangCode() == 'kl'
            assert output.getvalue() == ""

    def test08InputLinuxLangCodeBlankGoodSecond(self):
        """!
        @brief Test _inputLinuxLangCode() method, blank first try, good second try
        """
        inputStr = (text for text in ["", "RM"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            assert testobj._inputLinuxLangCode() == 'rm'
            assert output.getvalue() == "Error: Only two characters a-z are allowed in the code, try again.\n"

    def test09InputLinuxLangCodeBadGoodSecond(self):
        """!
        @brief Test _inputLinuxLangCode() method, bad first try, good second try
        """
        inputStr = (text for text in ["r4", "rrf", "k", "rm"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            assert testobj._inputLinuxLangCode() == 'rm'
            expected = "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected += "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected += "Error: Only two characters a-z are allowed in the code, try again.\n"
            assert output.getvalue() == expected

    def test10InputLinuxLangRegionsGood(self):
        """!
        @brief Test _inputLinuxLangRegions() method, good first try
        """
        inputStr = (text for text in ["hk", ""])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            regionList = testobj._inputLinuxLangRegions()
            assert len(regionList) == 1
            assert regionList[0] == 'HK'

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            assert output.getvalue() == expected

    def test11InputLinuxLangRegionsBadThenGood2(self):
        """!
        @brief Test _inputLinuxLangRegions() method, blank first try, good second try
        """
        inputStr = (text for text in ["r4", "rrf", "k", "rh", "RL", ""])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            regionList = testobj._inputLinuxLangRegions()
            assert len(regionList) == 2
            assert regionList[0] == 'RH'
            assert regionList[1] == 'RL'

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            expected += "Error: Only two characters A-Z are allowed in the code, try again.\n"
            expected += "Error: Only two characters A-Z are allowed in the code, try again.\n"
            expected += "Error: Only two characters A-Z are allowed in the code, try again.\n"
            assert output.getvalue() == expected

    def test12InputWindowsLangIdsGood(self):
        """!
        @brief Test _inputWindowsLangIds() method, single LANGID value, single LANGID code
        """
        inputStr = (text for text in ["1157", "133", "0"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            windowsIdCodes, windowsIdCodeList = testobj._inputWindowsLangIds()
            assert len(windowsIdCodes) == 1
            assert windowsIdCodes[0] == (1157 & 0xFF)
            assert len(windowsIdCodeList) == 2
            assert windowsIdCodeList[0] == 1157
            assert windowsIdCodeList[1] == 133

            expected = "Enter Windows LANGID values. A value of 0 will exit.\n"
            assert output.getvalue() == expected

    def test13InputWindowsLangIdsMultipleIdOneCode(self):
        """!
        @brief Test _inputWindowsLangIds() method, multiple LANGID values, single LANGID code
        """
        inputStr = (text for text in ["3081", "10249", "4105", "0"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            windowsIdCodes, windowsIdCodeList = testobj._inputWindowsLangIds()
            assert len(windowsIdCodes) == 1
            assert windowsIdCodes[0] == 9
            assert len(windowsIdCodeList) == 3
            assert windowsIdCodeList[0] == 3081
            assert windowsIdCodeList[1] == 10249
            assert windowsIdCodeList[2] == 4105

            expected = "Enter Windows LANGID values. A value of 0 will exit.\n"
            assert output.getvalue() == expected

    def test14InputWindowsLangIdsMultipleIdMultipleOneCode(self):
        """!
        @brief Test _inputWindowsLangIds() method, multiple LANGID values, multiple LANGID codes
        """
        inputStr = (text for text in ["3081", "10249", "4105", "2060", "11276", "9", "0"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            windowsIdCodes, windowsIdCodeList = testobj._inputWindowsLangIds()
            assert len(windowsIdCodes) == 2
            assert windowsIdCodes[0] == 9
            assert windowsIdCodes[1] == 12
            assert len(windowsIdCodeList) == 6
            assert windowsIdCodeList[0] == 3081
            assert windowsIdCodeList[1] == 10249
            assert windowsIdCodeList[2] == 4105
            assert windowsIdCodeList[3] == 2060
            assert windowsIdCodeList[4] == 11276
            assert windowsIdCodeList[5] == 9

            expected = "Enter Windows LANGID values. A value of 0 will exit.\n"
            assert output.getvalue() == expected

    def test15NewLanguage(self):
        """!
        @brief Test newLanguage() method
        """
        #                              name        iso   linux  linux          Windows LANGID list           correct, commit
        #                                                code   regions
        inputStr = (text for text in ["testlang", "tl", "tl",  "AU", "US", "", "3081", "10249", "4105", "0", "y", "y"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            assert testobj.newLanguage()

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            expected += "Enter Windows LANGID values. A value of 0 will exit.\n"
            expected += "New Entry:\n"
            expected += "{'LANG': 'tl', 'LANG_regions': ['AU', 'US'], 'LANGID': [9], "
            expected += "'LANGID_regions': [3081, 10249, 4105], 'isoCode': 'tl', 'compileSwitch': 'TESTLANG_ERRORS'}\n"
            assert output.getvalue() == expected

            assert testobj.langJsonData['languages']['testlang'] is not None
            assert testobj.langJsonData['languages']['testlang']['LANG'] == 'tl'

            assert len(testobj.langJsonData['languages']['testlang']['LANG_regions']) == 2
            assert testobj.langJsonData['languages']['testlang']['LANG_regions'][0] == 'AU'
            assert testobj.langJsonData['languages']['testlang']['LANG_regions'][1] == 'US'

            assert len(testobj.langJsonData['languages']['testlang']['LANGID']) == 1
            assert testobj.langJsonData['languages']['testlang']['LANGID'][0] == (3081 & 0x0FF)

            assert len(testobj.langJsonData['languages']['testlang']['LANGID_regions']) == 3
            assert testobj.langJsonData['languages']['testlang']['LANGID_regions'][0] == 3081
            assert testobj.langJsonData['languages']['testlang']['LANGID_regions'][1] == 10249
            assert testobj.langJsonData['languages']['testlang']['LANGID_regions'][2] == 4105

            assert testobj.langJsonData['languages']['testlang']['isoCode'] == 'tl'
            assert testobj.langJsonData['languages']['testlang']['compileSwitch'] == 'TESTLANG_ERRORS'

    def test16NewLanguageNoCommit(self):
        """!
        @brief Test newLanguage() method
        """
        #                              name        iso   linux  linux          Windows LANGID list           correct, commit
        #                                                code   regions
        inputStr = (text for text in ["newlang", "tl", "tl",  "AU", "US", "", "3081", "10249", "4105", "0", "y", "n"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            assert not testobj.newLanguage()

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            expected += "Enter Windows LANGID values. A value of 0 will exit.\n"
            expected += "New Entry:\n"
            expected += "{'LANG': 'tl', 'LANG_regions': ['AU', 'US'], 'LANGID': [9], "
            expected += "'LANGID_regions': [3081, 10249, 4105], 'isoCode': 'tl', 'compileSwitch': 'NEWLANG_ERRORS'}\n"
            assert output.getvalue() == expected

            langKeys = list(testobj.langJsonData['languages'].keys())
            assert 'newlang' not in langKeys

    def test17NewLanguageNotRight(self):
        """!
        @brief Test newLanguage() method, no on first verification, commit second
        """
        self.maxDiff = None
        #                              name        iso   linux  linux          Windows LANGID list           correct, commit
        #                                                code   regions
        inputStr = (text for text in ["newlang", "tl", "tl",  "AU", "US", "", "3081", "10249", "4105", "0", "n",
                                      "newtstlang", "nl", "nl",  "FR", "ES", "", "2060", "11276", "3084", "0", "y", "y"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            assert testobj.newLanguage()

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

            langKeys = list(testobj.langJsonData['languages'].keys())
            assert 'newlang' not in langKeys
            assert 'newtstlang' in langKeys

    def test18String(self):
        """!
        @brief Test __str__() method
        """
        self.maxDiff = None
        testobj = LanguageDescriptionList(self.testJson)
        testStr = str(testobj)

        expected = ""
        for langName, langData in testobj.langJsonData['languages'].items():
            expected += langName
            expected += ": {\n"
            expected += str(langData)
            expected += "} end "
            expected += langName
            expected +="\n"

        expected += "Default = "
        expected += str(testobj.langJsonData['default']['name'])

        assert testStr == expected

class Test02JsonLanguageListInput:
    @classmethod
    def setup_class(cls):
        cls.testJson = os.path.join(TESTFILEPATH, "testdata.json")


    @classmethod
    def teardown_class(cls):
        if os.path.exists("jsonLanguageDescriptionList.json"):
            os.remove("jsonLanguageDescriptionList.json")   # Delete in case it was accidently created


    """!
    @brief Unit test for the LanguageDescriptionList class input functions
    """
    def test01InputLanguageNameGood(self):
        """!
        @brief Test _inputLanguageName() method, good first try
        """
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', return_value='Klingon'):
            testobj = LanguageDescriptionList()
            assert testobj._inputLanguageName() == 'klingon'
            assert output.getvalue() == ""

    def test02InputLanguageNameBlankGoodSecond(self):
        """!
        @brief Test _inputLanguageName() method, blank first try, good second try
        """
        inputStr = (text for text in ["", "Romulan"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            assert testobj._inputLanguageName() == 'romulan'
            assert output.getvalue() == "Error: Only characters a-z are allowed in the <lang> name, try again.\n"

    def test03InputLanguageNameBadGoodSecond(self):
        """!
        @brief Test _inputLanguageName() method, bad tries, good at the end try
        """
        inputStr = (text for text in ["Tech33", "romulan_home", "romulan-home", "Romulan"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            assert testobj._inputLanguageName() == 'romulan'
            expected = "Error: Only characters a-z are allowed in the <lang> name, try again.\n"
            expected += "Error: Only characters a-z are allowed in the <lang> name, try again.\n"
            expected += "Error: Only characters a-z are allowed in the <lang> name, try again.\n"
            assert output.getvalue() == expected

    def test04InputIsoCodeGood(self):
        """!
        @brief Test _inputIsoTranslateCode() method, good first try
        """
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', return_value='kl'):
            testobj = LanguageDescriptionList()
            assert testobj._inputIsoTranslateCode() == 'kl'
            assert output.getvalue() == ""

    def test05InputIsoCodeBlankGoodSecond(self):
        """!
        @brief Test _inputIsoTranslateCode() method, blank first try, good second try
        """
        inputStr = (text for text in ["", "RM"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            assert testobj._inputIsoTranslateCode() == 'rm'
            assert output.getvalue() == "Error: Only two characters a-z are allowed in the code, try again.\n"

    def test06InputIsoCodeBadGoodSecond(self):
        """!
        @brief Test _inputIsoTranslateCode() method, bad first try, good second try
        """
        inputStr = (text for text in ["r4", "rrf", "k", "rm"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            assert testobj._inputIsoTranslateCode() == 'rm'
            expected = "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected += "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected += "Error: Only two characters a-z are allowed in the code, try again.\n"
            assert output.getvalue() == expected

    def test07InputLinuxLangCodeGood(self):
        """!
        @brief Test _inputLinuxLangCode() method, good first try
        """
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', return_value='kl'):
            testobj = LanguageDescriptionList()
            assert testobj._inputLinuxLangCode() == 'kl'
            assert output.getvalue() == ""

    def test08InputLinuxLangCodeBlankGoodSecond(self):
        """!
        @brief Test _inputLinuxLangCode() method, blank first try, good second try
        """
        inputStr = (text for text in ["", "RM"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            assert testobj._inputLinuxLangCode() == 'rm'
            assert output.getvalue() == "Error: Only two characters a-z are allowed in the code, try again.\n"

    def test09InputLinuxLangCodeBadGoodSecond(self):
        """!
        @brief Test _inputLinuxLangCode() method, bad first try, good second try
        """
        inputStr = (text for text in ["r4", "rrf", "k", "rm"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            assert testobj._inputLinuxLangCode() == 'rm'
            expected = "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected += "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected += "Error: Only two characters a-z are allowed in the code, try again.\n"
            assert output.getvalue() == expected

    def test10InputLinuxLangRegionsGood(self):
        """!
        @brief Test _inputLinuxLangRegions() method, good first try
        """
        inputStr = (text for text in ["hk", ""])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            regionList = testobj._inputLinuxLangRegions()
            assert len(regionList) == 1
            assert regionList[0] == 'HK'

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            assert output.getvalue() == expected

    def test11InputLinuxLangRegionsBadThenGood2(self):
        """!
        @brief Test _inputLinuxLangRegions() method, blank first try, good second try
        """
        inputStr = (text for text in ["r4", "rrf", "k", "rh", "RL", ""])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            regionList = testobj._inputLinuxLangRegions()
            assert len(regionList) == 2
            assert regionList[0] == 'RH'
            assert regionList[1] == 'RL'

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            expected += "Error: Only two characters A-Z are allowed in the code, try again.\n"
            expected += "Error: Only two characters A-Z are allowed in the code, try again.\n"
            expected += "Error: Only two characters A-Z are allowed in the code, try again.\n"
            assert output.getvalue() == expected

    def test12InputWindowsLangIdsGood(self):
        """!
        @brief Test _inputWindowsLangIds() method, single LANGID value, single LANGID code
        """
        inputStr = (text for text in ["1157", "0"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            windowsIdCodes, windowsIdCodeList = testobj._inputWindowsLangIds()
            assert len(windowsIdCodes) == 1
            assert windowsIdCodes[0] == (1157 & 0xFF)
            assert len(windowsIdCodeList) == 1
            assert windowsIdCodeList[0] == 1157

            expected = "Enter Windows LANGID values. A value of 0 will exit.\n"
            assert output.getvalue() == expected

    def test13InputWindowsLangIdsMultipleIdOneCode(self):
        """!
        @brief Test _inputWindowsLangIds() method, multiple LANGID values, single LANGID code
        """
        inputStr = (text for text in ["3081", "10249", "4105", "0"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            windowsIdCodes, windowsIdCodeList = testobj._inputWindowsLangIds()
            assert len(windowsIdCodes) == 1
            assert windowsIdCodes[0] == 9
            assert len(windowsIdCodeList) == 3
            assert windowsIdCodeList[0] == 3081
            assert windowsIdCodeList[1] == 10249
            assert windowsIdCodeList[2] == 4105

            expected = "Enter Windows LANGID values. A value of 0 will exit.\n"
            assert output.getvalue() == expected

    def test14InputWindowsLangIdsMultipleIdMultipleOneCode(self):
        """!
        @brief Test _inputWindowsLangIds() method, multiple LANGID values, multiple LANGID codes
        """
        inputStr = (text for text in ["3081", "10249", "4105", "2060", "11276", "0"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            windowsIdCodes, windowsIdCodeList = testobj._inputWindowsLangIds()
            assert len(windowsIdCodes) == 2
            assert windowsIdCodes[0] == 9
            assert windowsIdCodes[1] == 12
            assert len(windowsIdCodeList) == 5
            assert windowsIdCodeList[0] == 3081
            assert windowsIdCodeList[1] == 10249
            assert windowsIdCodeList[2] == 4105
            assert windowsIdCodeList[3] == 2060
            assert windowsIdCodeList[4] == 11276

            expected = "Enter Windows LANGID values. A value of 0 will exit.\n"
            assert output.getvalue() == expected

    def test15NewLanguage(self):
        """!
        @brief Test newLanguage() method
        """
        #                              name        iso   linux  linux          Windows LANGID list           correct, commit
        #                                                code   regions
        inputStr = (text for text in ["testlang", "tl", "tl",  "AU", "US", "", "3081", "10249", "4105", "0", "y", "y"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            assert testobj.newLanguage()

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            expected += "Enter Windows LANGID values. A value of 0 will exit.\n"
            expected += "New Entry:\n"
            expected += "{'LANG': 'tl', 'LANG_regions': ['AU', 'US'], 'LANGID': [9], "
            expected += "'LANGID_regions': [3081, 10249, 4105], 'isoCode': 'tl', 'compileSwitch': 'TESTLANG_ERRORS'}\n"
            assert output.getvalue() == expected

            assert testobj.langJsonData['languages']['testlang'] is not None
            assert testobj.langJsonData['languages']['testlang']['LANG'] == 'tl'

            assert len(testobj.langJsonData['languages']['testlang']['LANG_regions']) == 2
            assert testobj.langJsonData['languages']['testlang']['LANG_regions'][0] == 'AU'
            assert testobj.langJsonData['languages']['testlang']['LANG_regions'][1] == 'US'

            assert len(testobj.langJsonData['languages']['testlang']['LANGID']) == 1
            assert testobj.langJsonData['languages']['testlang']['LANGID'][0] == (3081 & 0x0FF)

            assert len(testobj.langJsonData['languages']['testlang']['LANGID_regions']) == 3
            assert testobj.langJsonData['languages']['testlang']['LANGID_regions'][0] == 3081
            assert testobj.langJsonData['languages']['testlang']['LANGID_regions'][1] == 10249
            assert testobj.langJsonData['languages']['testlang']['LANGID_regions'][2] == 4105

            assert testobj.langJsonData['languages']['testlang']['isoCode'] == 'tl'
            assert testobj.langJsonData['languages']['testlang']['compileSwitch'] == 'TESTLANG_ERRORS'

    def test16NewLanguageNoCommit(self):
        """!
        @brief Test newLanguage() method
        """
        #                              name        iso   linux  linux          Windows LANGID list           correct, commit
        #                                                code   regions
        inputStr = (text for text in ["newlang", "tl", "tl",  "AU", "US", "", "3081", "10249", "4105", "0", "y", "n"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            assert not testobj.newLanguage()

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            expected += "Enter Windows LANGID values. A value of 0 will exit.\n"
            expected += "New Entry:\n"
            expected += "{'LANG': 'tl', 'LANG_regions': ['AU', 'US'], 'LANGID': [9], "
            expected += "'LANGID_regions': [3081, 10249, 4105], 'isoCode': 'tl', 'compileSwitch': 'NEWLANG_ERRORS'}\n"
            assert output.getvalue() == expected

            langKeys = list(testobj.langJsonData['languages'].keys())
            assert 'newlang' not in langKeys

    def test17NewLanguageNotRight(self):
        """!
        @brief Test newLanguage() method, no on first verification, commit second
        """
        self.maxDiff = None
        #                              name        iso   linux  linux          Windows LANGID list           correct, commit
        #                                                code   regions
        inputStr = (text for text in ["newlang", "tl", "tl",  "AU", "US", "", "3081", "10249", "4105", "0", "n",
                                      "newtstlang", "nl", "nl",  "FR", "ES", "", "2060", "11276", "3084", "0", "y", "y"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            assert testobj.newLanguage()

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

            langKeys = list(testobj.langJsonData['languages'].keys())
            assert 'newlang' not in langKeys
            assert 'newtstlang' in langKeys

    def test18String(self):
        """!
        @brief Test __str__() method
        """
        self.maxDiff = None
        testobj = LanguageDescriptionList(self.testJson)
        testStr = str(testobj)

        expected = ""
        for langName, langData in testobj.langJsonData['languages'].items():
            expected += langName
            expected += ": {\n"
            expected += str(langData)
            expected += "} end "
            expected += langName
            expected +="\n"

        expected += "Default = "
        expected += str(testobj.langJsonData['default']['name'])

        assert testStr == expected

    def test19InputWindowsLangIdsMultipleIdMultipleCode(self):
        """!
        @brief Test _inputWindowsLangIds() method, multiple LANGID values, multiple LANGID codes
        """
        inputStr = (text for text in ["3081", "2576", "2576", "0"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = LanguageDescriptionList()
            windowsIdCodes, windowsIdCodeList = testobj._inputWindowsLangIds()
            assert len(windowsIdCodes) == 2
            assert windowsIdCodes[0] == 9
            assert windowsIdCodes[1] == 16
            assert len(windowsIdCodeList) == 2
            assert windowsIdCodeList[0] == 3081
            assert windowsIdCodeList[1] == 2576

            expected = "Enter Windows LANGID values. A value of 0 will exit.\n"
            assert output.getvalue() == expected
