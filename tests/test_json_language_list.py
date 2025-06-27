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
import unittest
from unittest.mock import patch, MagicMock, mock_open

import io
import contextlib

from dir_init import TESTFILEPATH
from dir_init import pathincsetup
pathincsetup()

from code_tools.base.json_language_list import LanguageDescriptionList


class Unittest01JsonLanguageList(unittest.TestCase):
    """!
    @brief Unit test for the LanguageDescriptionList class
    """

    @classmethod
    def setUpClass(cls):
        cls.testJson = os.path.join(TESTFILEPATH, "testdata.json")
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("jsonLanguageDescriptionList.json"):
            os.remove("jsonLanguageDescriptionList.json")   # Delete in case it was accidently created
        return super().tearDownClass()

    def test01DefaultConstructor(self):
        """!
        @brief Test Default constructor()
        """
        testobj = LanguageDescriptionList()
        self.assertRaises(FileNotFoundError)
        self.assertEqual(testobj.filename, "jsonLanguageDescriptionList.json")
        self.assertIsNotNone(testobj.langJsonData['default'])
        self.assertEqual(testobj.langJsonData['default']['name'], "english")
        self.assertEqual(testobj.langJsonData['default']['isoCode'], "en")
        self.assertIsNotNone(testobj.langJsonData['languages'])
        self.assertEqual(len(testobj.langJsonData['languages']), 0)

    def test02ConstructorWithFile(self):
        """!
        @brief Test constructor() with file name
        """
        testobj = LanguageDescriptionList(self.testJson)
        self.assertEqual(testobj.filename, self.testJson)
        self.assertIsNotNone(testobj.langJsonData['default'])
        self.assertEqual(testobj.langJsonData['default']['name'], "spanish")
        self.assertEqual(testobj.langJsonData['default']['isoCode'], "es")
        self.assertIsNotNone(testobj.langJsonData['languages'])
        self.assertEqual(len(testobj.langJsonData['languages']), 1)

        self.assertIsNotNone(testobj.langJsonData['languages']['english'])
        keyList = list(testobj.langJsonData['languages']['english'].keys())
        self.assertEqual(len(keyList), 6)

        self.assertIn('LANG', keyList)
        self.assertIsNotNone(testobj.langJsonData['languages']['english']['LANG'])
        self.assertEqual(testobj.langJsonData['languages']['english']['LANG'], 'en')

        self.assertIn('LANG_regions', keyList)
        self.assertIsNotNone(testobj.langJsonData['languages']['english']['LANG_regions'])
        self.assertEqual(len(testobj.langJsonData['languages']['english']['LANG_regions']), 13)
        self.assertEqual(testobj.langJsonData['languages']['english']['LANG_regions'][0], 'AU')
        self.assertEqual(testobj.langJsonData['languages']['english']['LANG_regions'][12], 'ZW')

        self.assertIn('LANGID', keyList)
        self.assertIsNotNone(testobj.langJsonData['languages']['english']['LANGID'])
        self.assertEqual(len(testobj.langJsonData['languages']['english']['LANGID']), 1)
        self.assertEqual(testobj.langJsonData['languages']['english']['LANGID'][0], 9)

        self.assertIn('LANGID_regions', keyList)
        self.assertIsNotNone(testobj.langJsonData['languages']['english']['LANGID_regions'])
        self.assertEqual(len(testobj.langJsonData['languages']['english']['LANGID_regions']), 14)
        self.assertEqual(testobj.langJsonData['languages']['english']['LANGID_regions'][0], 3081)
        self.assertEqual(testobj.langJsonData['languages']['english']['LANGID_regions'][13], 12297)

        self.assertIn('isoCode', keyList)
        self.assertIsNotNone(testobj.langJsonData['languages']['english']['isoCode'])
        self.assertEqual(testobj.langJsonData['languages']['english']['isoCode'], 'en')

        self.assertIn('compileSwitch', keyList)
        self.assertIsNotNone(testobj.langJsonData['languages']['english']['compileSwitch'])
        self.assertEqual(testobj.langJsonData['languages']['english']['compileSwitch'], "ENGLISH_ERRORS")

    def test03Clear(self):
        """!
        @brief Test clear method
        """
        testobj = LanguageDescriptionList(self.testJson)
        self.assertEqual(testobj.filename, self.testJson)
        self.assertIsNotNone(testobj.langJsonData['default'])
        self.assertEqual(testobj.langJsonData['default']['isoCode'], "es")
        self.assertIsNotNone(testobj.langJsonData['languages'])
        self.assertEqual(len(testobj.langJsonData['languages']), 1)

        testobj.clear()
        self.assertEqual(testobj.filename, self.testJson)
        self.assertIsNotNone(testobj.langJsonData['default'])
        self.assertEqual(testobj.langJsonData['default']['name'], "english")
        self.assertEqual(testobj.langJsonData['default']['isoCode'], "en")
        self.assertIsNotNone(testobj.langJsonData['languages'])
        self.assertEqual(len(testobj.langJsonData['languages']), 0)

    def test04Printerror(self):
        """!
        @brief Test _printError method
        """
        testobj = LanguageDescriptionList()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            testobj._printError("test error")
            self.assertEqual(output.getvalue(), "Error: test error\n")

    def test05GetCommitOverwriteFlagNo(self):
        """!
        @brief Test _getCommitOverWriteFlag method, no answer
        """
        testobj = LanguageDescriptionList()
        with patch('builtins.input', side_effect='n') as inMock:
            self.assertFalse(testobj._getCommitOverWriteFlag("testEntry"))
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='N') as inMock:
            self.assertFalse(testobj._getCommitOverWriteFlag("testEntry"))
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='no') as inMock:
            self.assertFalse(testobj._getCommitOverWriteFlag("testEntry"))
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='NO') as inMock:
            self.assertFalse(testobj._getCommitOverWriteFlag("testEntry"))
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='No') as inMock:
            self.assertFalse(testobj._getCommitOverWriteFlag("testEntry"))
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

    def test06GetCommitOverwriteFlagYes(self):
        """!
        @brief Test _getCommitOverWriteFlag method, Yes answer
        """
        testobj = LanguageDescriptionList()
        with patch('builtins.input', side_effect='y') as inMock:
            self.assertTrue(testobj._getCommitOverWriteFlag("testEntry"))
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='Y') as inMock:
            self.assertTrue(testobj._getCommitOverWriteFlag("testEntry"))
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='yes') as inMock:
            self.assertTrue(testobj._getCommitOverWriteFlag("testEntry"))
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='YES') as inMock:
            self.assertTrue(testobj._getCommitOverWriteFlag("testEntry"))
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='Yes') as inMock:
            self.assertTrue(testobj._getCommitOverWriteFlag("testEntry"))
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

    def test07GetCommitOverwriteFlagOverride(self):
        """!
        @brief Test _getCommitOverWriteFlag method, override=True
        """
        testobj = LanguageDescriptionList()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertTrue(testobj._getCommitOverWriteFlag("testEntry", True))
            self.assertEqual(output.getvalue(), "")

    def test08GetCommitNewFlagNo(self):
        """!
        @brief Test _getCommitNewFlag method, no answer
        """
        testobj = LanguageDescriptionList()
        with patch('builtins.input', side_effect='n') as inMock:
            self.assertFalse(testobj._getCommitNewFlag("testEntry"))
            inMock.assert_called_once_with("Add new testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='N') as inMock:
            self.assertFalse(testobj._getCommitNewFlag("testEntry"))
            inMock.assert_called_once_with("Add new testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='no') as inMock:
            self.assertFalse(testobj._getCommitNewFlag("testEntry"))
            inMock.assert_called_once_with("Add new testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='NO') as inMock:
            self.assertFalse(testobj._getCommitNewFlag("testEntry"))
            inMock.assert_called_once_with("Add new testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='No') as inMock:
            self.assertFalse(testobj._getCommitNewFlag("testEntry"))
            inMock.assert_called_once_with("Add new testEntry entry? [Y/N]")

    def test09GetCommitNewFlagYes(self):
        """!
        @brief Test _getCommitNewFlag method, Yes answer
        """
        testobj = LanguageDescriptionList()
        with patch('builtins.input', side_effect='y') as inMock:
            self.assertTrue(testobj._getCommitNewFlag("testEntry"))
            inMock.assert_called_once_with("Add new testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='Y') as inMock:
            self.assertTrue(testobj._getCommitNewFlag("testEntry"))
            inMock.assert_called_once_with("Add new testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='yes') as inMock:
            self.assertTrue(testobj._getCommitNewFlag("testEntry"))
            inMock.assert_called_once_with("Add new testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='YES') as inMock:
            self.assertTrue(testobj._getCommitNewFlag("testEntry"))
            inMock.assert_called_once_with("Add new testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='Yes') as inMock:
            self.assertTrue(testobj._getCommitNewFlag("testEntry"))
            inMock.assert_called_once_with("Add new testEntry entry? [Y/N]")

    def test10GetCommitFlag(self):
        """!
        @brief Test _getCommitFlag method
        """
        testobj = LanguageDescriptionList()
        with patch('builtins.input', side_effect='y') as inMock:
            self.assertTrue(testobj._getCommitFlag("testEntry",['testEntry']))
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")
        with patch('builtins.input', side_effect='n') as inMock:
            self.assertFalse(testobj._getCommitFlag("testEntry",['testEntry']))
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='y') as inMock:
            self.assertTrue(testobj._getCommitFlag("test33",['testEntry']))
            inMock.assert_called_once_with("Add new test33 entry? [Y/N]")
        with patch('builtins.input', side_effect='n') as inMock:
            self.assertFalse(testobj._getCommitFlag("test33",['testEntry']))
            inMock.assert_called_once_with("Add new test33 entry? [Y/N]")

        self.assertTrue(testobj._getCommitFlag("testEntry",['testEntry'], True))

        with patch('builtins.input', side_effect='y') as inMock:
            self.assertTrue(testobj._getCommitFlag("test33",['testEntry'], True))
            inMock.assert_called_once_with("Add new test33 entry? [Y/N]")
        with patch('builtins.input', side_effect='n') as inMock:
            self.assertFalse(testobj._getCommitFlag("test33",['testEntry'], True))
            inMock.assert_called_once_with("Add new test33 entry? [Y/N]")

    def test11Update(self):
        """!
        @brief Test update method
        """
        testobj = LanguageDescriptionList("temp.json")
        self.assertEqual(testobj.filename, "temp.json")
        testobj.langJsonData['languages']['french'] = {'LANG':'fr', 'LANG_regions':['FR'],
                                                       'LANGID': [12], 'LANGID_regions': [1036, 5132],
                                                       'isoCode': 'fr', 'compileSwitch': "FRENCH_ERRORS"}
        testobj.update()

        updateobj = LanguageDescriptionList("temp.json")
        self.assertEqual(updateobj.filename, "temp.json")
        self.assertIsNotNone(updateobj.langJsonData['default'])
        self.assertEqual(updateobj.langJsonData['default']['name'], "english")
        self.assertEqual(updateobj.langJsonData['default']['isoCode'], "en")
        self.assertIsNotNone(updateobj.langJsonData['languages'])
        self.assertEqual(len(updateobj.langJsonData['languages']), 1)

        self.assertIsNotNone(updateobj.langJsonData['languages']['french'])
        keyList = list(updateobj.langJsonData['languages']['french'].keys())
        self.assertEqual(len(keyList), 6)

        self.assertIn('LANG', keyList)
        self.assertIsNotNone(updateobj.langJsonData['languages']['french']['LANG'])
        self.assertEqual(updateobj.langJsonData['languages']['french']['LANG'], 'fr')

        self.assertIn('LANG_regions', keyList)
        self.assertIsNotNone(updateobj.langJsonData['languages']['french']['LANG_regions'])
        self.assertEqual(len(updateobj.langJsonData['languages']['french']['LANG_regions']), 1)
        self.assertEqual(updateobj.langJsonData['languages']['french']['LANG_regions'][0], 'FR')

        self.assertIn('LANGID', keyList)
        self.assertIsNotNone(updateobj.langJsonData['languages']['french']['LANGID'])
        self.assertEqual(len(updateobj.langJsonData['languages']['french']['LANGID']), 1)
        self.assertEqual(updateobj.langJsonData['languages']['french']['LANGID'][0], 12)

        self.assertIn('LANGID_regions', keyList)
        self.assertIsNotNone(updateobj.langJsonData['languages']['french']['LANGID_regions'])
        self.assertEqual(len(updateobj.langJsonData['languages']['french']['LANGID_regions']), 2)
        self.assertEqual(updateobj.langJsonData['languages']['french']['LANGID_regions'][0], 1036)
        self.assertEqual(updateobj.langJsonData['languages']['french']['LANGID_regions'][1], 5132)

        self.assertIn('isoCode', keyList)
        self.assertIsNotNone(updateobj.langJsonData['languages']['french']['isoCode'])
        self.assertEqual(updateobj.langJsonData['languages']['french']['isoCode'], 'fr')

        self.assertIn('compileSwitch', keyList)
        self.assertIsNotNone(updateobj.langJsonData['languages']['french']['compileSwitch'])
        self.assertEqual(updateobj.langJsonData['languages']['french']['compileSwitch'], "FRENCH_ERRORS")

        os.remove("temp.json")

    def test12SetDefaultPass(self):
        """!
        @brief Test setDefault method, pass
        """
        testobj = LanguageDescriptionList(self.testJson)
        self.assertEqual(testobj.filename, self.testJson)
        self.assertIsNotNone(testobj.langJsonData['default'])
        self.assertEqual(testobj.langJsonData['default']['name'], "spanish")
        self.assertEqual(testobj.langJsonData['default']['isoCode'], "es")
        self.assertIsNotNone(testobj.langJsonData['languages'])
        self.assertEqual(len(testobj.langJsonData['languages']), 1)

        testobj.setDefault("english")
        self.assertEqual(testobj.langJsonData['default']['name'], "english")
        self.assertEqual(testobj.langJsonData['default']['isoCode'], "en")

    def test13SetDefaultFail(self):
        """!
        @brief Test setDefault method, fail
        """
        testobj = LanguageDescriptionList(self.testJson)
        self.assertIsNotNone(testobj.langJsonData['languages'])
        self.assertEqual(len(testobj.langJsonData['languages']), 1)

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            testobj.setDefault("german")
            self.assertEqual(output.getvalue(), "Error: You must select a current language as the default.\nAvailable languages:\n  english\n")

            self.assertEqual(testobj.langJsonData['default']['name'], "spanish")
            self.assertEqual(testobj.langJsonData['default']['isoCode'], "es")

    def test14GetDefaultData(self):
        """!
        @brief Test getDefaultData method
        """
        testobj = LanguageDescriptionList()
        defaultLang, defaultIsoCode = testobj.getDefaultData()
        self.assertEqual(testobj.langJsonData['default']['name'], defaultLang)
        self.assertEqual(testobj.langJsonData['default']['isoCode'], defaultIsoCode)

    def test15CreateEntry(self):
        """!
        @brief Test static _createLanguageEntry method
        """
        entryDict = LanguageDescriptionList._createLanguageEntry("en", ['AU','US'], [9], [100,200], 'en', "ENGLISH_SWITCH")
        keyList = list(entryDict.keys())
        self.assertEqual(len(keyList), 6)

        self.assertIn('LANG', keyList)
        self.assertIsNotNone(entryDict['LANG'])
        self.assertEqual(entryDict['LANG'], 'en')

        self.assertIn('LANG_regions', keyList)
        self.assertIsNotNone(entryDict['LANG_regions'])
        self.assertEqual(len(entryDict['LANG_regions']), 2)
        self.assertEqual(entryDict['LANG_regions'][0], 'AU')
        self.assertEqual(entryDict['LANG_regions'][1], 'US')

        self.assertIn('LANGID', keyList)
        self.assertIsNotNone(entryDict['LANGID'])
        self.assertEqual(len(entryDict['LANGID']), 1)
        self.assertEqual(entryDict['LANGID'][0], 9)

        self.assertIn('LANGID_regions', keyList)
        self.assertIsNotNone(entryDict['LANGID_regions'])
        self.assertEqual(len(entryDict['LANGID_regions']), 2)
        self.assertEqual(entryDict['LANGID_regions'][0], 100)
        self.assertEqual(entryDict['LANGID_regions'][1], 200)

        self.assertIn('isoCode', keyList)
        self.assertIsNotNone(entryDict['isoCode'])
        self.assertEqual(entryDict['isoCode'], 'en')

        self.assertIn('compileSwitch', keyList)
        self.assertIsNotNone(entryDict['compileSwitch'])
        self.assertEqual(entryDict['compileSwitch'], "ENGLISH_SWITCH")

    def test16GetLanguagePropertyData(self):
        """!
        @brief Test getLanguagePropertyData method
        """
        testobj = LanguageDescriptionList(self.testJson)
        property = testobj.getLanguagePropertyData('english', 'LANG')
        self.assertIsInstance(property, str)
        self.assertEqual(property, "en")

        property = testobj.getLanguagePropertyData('english', 'LANG_regions')
        self.assertIsInstance(property, list)
        self.assertEqual(len(property), 13)

        property = testobj.getLanguagePropertyData('english', 'LANGID')
        self.assertIsInstance(property, list)
        self.assertEqual(len(property), 1)

        property = testobj.getLanguagePropertyData('english', 'LANGID_regions')
        self.assertIsInstance(property, list)
        self.assertEqual(len(property), 14)

        property = testobj.getLanguagePropertyData('english', 'isoCode')
        self.assertIsInstance(property, str)
        self.assertEqual(property, "en")

        property = testobj.getLanguagePropertyData('english', 'compileSwitch')
        self.assertIsInstance(property, str)
        self.assertEqual(property, "ENGLISH_ERRORS")

    def test17GetLanguageIsoCodeData(self):
        """!
        @brief Test getLanguageIsoCodeData method
        """
        testobj = LanguageDescriptionList(self.testJson)
        property = testobj.getLanguageIsoCodeData('english')
        self.assertEqual(property, "en")

    def test18GetLanguageLANGData(self):
        """!
        @brief Test getLanguageLANGData method
        """
        testobj = LanguageDescriptionList(self.testJson)
        langCode, regionList = testobj.getLanguageLANGData('english')
        self.assertEqual(langCode, "en")
        self.assertEqual(len(regionList), 13)

    def test19GetLanguageLANGIDData(self):
        """!
        @brief Test getLanguageLANGIDData method
        """
        testobj = LanguageDescriptionList(self.testJson)
        langIdCodes, regionIdList = testobj.getLanguageLANGIDData('english')
        self.assertEqual(len(langIdCodes), 1)
        self.assertEqual(langIdCodes[0], 9)
        self.assertEqual(len(regionIdList), 14)

    def test20GetLanguageCompileSwitchData(self):
        """!
        @brief Test getLanguageCompileSwitchData method
        """
        testobj = LanguageDescriptionList(self.testJson)
        property = testobj.getLanguageCompileSwitchData('english')
        self.assertEqual(property, "ENGLISH_ERRORS")

    def test21GetLanguagePropertyList(self):
        """!
        @brief Test getLanguagePropertyList method
        """
        testobj = LanguageDescriptionList()
        propertyList = testobj.getLanguagePropertyList()
        self.assertEqual(len(propertyList), 6)
        self.assertIn('LANG', propertyList)
        self.assertIn('LANG_regions', propertyList)
        self.assertIn('LANGID', propertyList)
        self.assertIn('LANGID_regions', propertyList)
        self.assertIn('isoCode', propertyList)
        self.assertIn('compileSwitch', propertyList)

    def test22GetLanguagePropertyReturnData(self):
        """!
        @brief Test getLanguagePropertyReturnData method
        """
        testobj = LanguageDescriptionList()
        type, description, isList = testobj.getLanguagePropertyReturnData('LANG')
        self.assertEqual(type, "string")
        self.assertFalse(isList)
        self.assertIsInstance(description, str)

        type, description, isList = testobj.getLanguagePropertyReturnData('LANG_regions')
        self.assertEqual(type, "string")
        self.assertTrue(isList)
        self.assertIsInstance(description, str)

        type, description, isList = testobj.getLanguagePropertyReturnData('LANGID')
        self.assertEqual(type, "LANGID")
        self.assertTrue(isList)
        self.assertIsInstance(description, str)

        type, description, isList = testobj.getLanguagePropertyReturnData('LANGID_regions')
        self.assertEqual(type, "LANGID")
        self.assertTrue(isList)
        self.assertIsInstance(description, str)

        type, description, isList = testobj.getLanguagePropertyReturnData('isoCode')
        self.assertEqual(type, "string")
        self.assertFalse(isList)
        self.assertIsInstance(description, str)

        type, description, isList = testobj.getLanguagePropertyReturnData('compileSwitch')
        self.assertEqual(type, "string")
        self.assertFalse(isList)
        self.assertIsInstance(description, str)

        type, description, isList = testobj.getLanguagePropertyReturnData('sillyString')
        self.assertIsNone(type, )
        self.assertFalse(isList)
        self.assertIsNone(description)

    def test23IsPropertyText(self):
        """!
        @brief Test isLanguagePropertyText method
        """
        testobj = LanguageDescriptionList()
        self.assertTrue(testobj.isLanguagePropertyText('LANG'))
        self.assertTrue(testobj.isLanguagePropertyText('LANG_regions'))
        self.assertFalse(testobj.isLanguagePropertyText('LANGID'))
        self.assertFalse(testobj.isLanguagePropertyText('LANGID_regions'))
        self.assertTrue(testobj.isLanguagePropertyText('isoCode'))
        self.assertTrue(testobj.isLanguagePropertyText('compileSwitch'))
        self.assertFalse(testobj.isLanguagePropertyText('sillyString'))

    def test24GetLanguagePropertyMethodName(self):
        """!
        @brief Test getLanguagePropertyMethodName method
        """
        testobj = LanguageDescriptionList()
        self.assertEqual(testobj.getLanguagePropertyMethodName('LANG'), "getLANGLanguage")
        self.assertEqual(testobj.getLanguagePropertyMethodName('LANG_regions'), "getLANGRegionList")
        self.assertEqual(testobj.getLanguagePropertyMethodName('LANGID'), "getLANGIDCode")
        self.assertEqual(testobj.getLanguagePropertyMethodName('LANGID_regions'), "getLANGIDList")
        self.assertEqual(testobj.getLanguagePropertyMethodName('isoCode'), "getLangIsoCode")
        self.assertEqual(testobj.getLanguagePropertyMethodName('compileSwitch'), "getLanguageCompileSwitch")
        self.assertIsNone(testobj.getLanguagePropertyMethodName('sillyString'))

    def test25GetLanguageIsoPropertyMethodName(self):
        """!
        @brief Test getLanguageIsoPropertyMethodName method
        """
        testobj = LanguageDescriptionList()
        self.assertEqual(testobj.getLanguageIsoPropertyMethodName(), "getLangIsoCode")

    def test26AddLanguage(self):
        """!
        @brief Test addLanguage method
        """
        testobj = LanguageDescriptionList()
        testobj.addLanguage('umpalumpa', 'ul', ['OR', 'WW'], [0x42], [0x1042, 0x2042], 'ul', "UMPA_LUMPA_ERRORS")
        self.assertIsNotNone(testobj.langJsonData['languages']['umpalumpa'])
        self.assertEqual(testobj.langJsonData['languages']['umpalumpa']['LANG'], 'ul')

        self.assertEqual(len(testobj.langJsonData['languages']['umpalumpa']['LANG_regions']), 2)
        self.assertEqual(testobj.langJsonData['languages']['umpalumpa']['LANG_regions'][0], 'OR')
        self.assertEqual(testobj.langJsonData['languages']['umpalumpa']['LANG_regions'][1], 'WW')

        self.assertEqual(len(testobj.langJsonData['languages']['umpalumpa']['LANGID']), 1)
        self.assertEqual(testobj.langJsonData['languages']['umpalumpa']['LANGID'][0], 0x42)

        self.assertEqual(len(testobj.langJsonData['languages']['umpalumpa']['LANGID_regions']), 2)
        self.assertEqual(testobj.langJsonData['languages']['umpalumpa']['LANGID_regions'][0], 0x1042)
        self.assertEqual(testobj.langJsonData['languages']['umpalumpa']['LANGID_regions'][1], 0x2042)

        self.assertEqual(testobj.langJsonData['languages']['umpalumpa']['isoCode'], 'ul')
        self.assertEqual(testobj.langJsonData['languages']['umpalumpa']['compileSwitch'], 'UMPA_LUMPA_ERRORS')

    def test27GetLanguageList(self):
        """!
        @brief Test addLanguage method
        """
        testobj = LanguageDescriptionList(self.testJson)
        langList = testobj.getLanguageList()
        self.assertEqual(len(langList), 1)
        self.assertIn("english", langList)

class Unittest02JsonLanguageListInputTests(unittest.TestCase):
    """!
    Test input methods
    """
    @classmethod
    def setUpClass(cls):
        cls.testJson = os.path.join(TESTFILEPATH, "testdata.json")
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("jsonLanguageDescriptionList.json"):
            os.remove("jsonLanguageDescriptionList.json")   # Delete in case it was accidently created
        return super().tearDownClass()

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
            self.assertEqual(testobj._inputLanguageName(), 'klingon')
            self.assertEqual(output.getvalue(), "")

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
            self.assertEqual(testobj._inputLanguageName(), 'romulan')
            self.assertEqual(output.getvalue(), "Error: Only characters a-z are allowed in the <lang> name, try again.\n")

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
            self.assertEqual(testobj._inputLanguageName(), 'romulan')
            expected = "Error: Only characters a-z are allowed in the <lang> name, try again.\n"
            expected += "Error: Only characters a-z are allowed in the <lang> name, try again.\n"
            expected += "Error: Only characters a-z are allowed in the <lang> name, try again.\n"
            self.assertEqual(output.getvalue(), expected)

    def test04InputIsoCodeGood(self):
        """!
        @brief Test _inputIsoTranslateCode() method, good first try
        """
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', return_value='kl'):
            testobj = LanguageDescriptionList()
            self.assertEqual(testobj._inputIsoTranslateCode(), 'kl')
            self.assertEqual(output.getvalue(), "")

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
            self.assertEqual(testobj._inputIsoTranslateCode(), 'rm')
            self.assertEqual(output.getvalue(), "Error: Only two characters a-z are allowed in the code, try again.\n")

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
            self.assertEqual(testobj._inputIsoTranslateCode(), 'rm')
            expected = "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected += "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected += "Error: Only two characters a-z are allowed in the code, try again.\n"
            self.assertEqual(output.getvalue(), expected)

    def test07InputLinuxLangCodeGood(self):
        """!
        @brief Test _inputLinuxLangCode() method, good first try
        """
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', return_value='kl'):
            testobj = LanguageDescriptionList()
            self.assertEqual(testobj._inputLinuxLangCode(), 'kl')
            self.assertEqual(output.getvalue(), "")

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
            self.assertEqual(testobj._inputLinuxLangCode(), 'rm')
            self.assertEqual(output.getvalue(), "Error: Only two characters a-z are allowed in the code, try again.\n")

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
            self.assertEqual(testobj._inputLinuxLangCode(), 'rm')
            expected = "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected += "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected += "Error: Only two characters a-z are allowed in the code, try again.\n"
            self.assertEqual(output.getvalue(), expected)

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
            self.assertEqual(len(regionList), 1)
            self.assertEqual(regionList[0], 'HK')

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            self.assertEqual(output.getvalue(), expected)

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
            self.assertEqual(len(regionList), 2)
            self.assertEqual(regionList[0], 'RH')
            self.assertEqual(regionList[1], 'RL')

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            expected += "Error: Only two characters A-Z are allowed in the code, try again.\n"
            expected += "Error: Only two characters A-Z are allowed in the code, try again.\n"
            expected += "Error: Only two characters A-Z are allowed in the code, try again.\n"
            self.assertEqual(output.getvalue(), expected)

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
            self.assertEqual(len(windowsIdCodes), 1)
            self.assertEqual(windowsIdCodes[0], (1157 & 0xFF))
            self.assertEqual(len(windowsIdCodeList), 1)
            self.assertEqual(windowsIdCodeList[0], 1157)

            expected = "Enter Windows LANGID values. A value of 0 will exit.\n"
            self.assertEqual(output.getvalue(), expected)

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
            self.assertEqual(len(windowsIdCodes), 1)
            self.assertEqual(windowsIdCodes[0], 9)
            self.assertEqual(len(windowsIdCodeList), 3)
            self.assertEqual(windowsIdCodeList[0], 3081)
            self.assertEqual(windowsIdCodeList[1], 10249)
            self.assertEqual(windowsIdCodeList[2], 4105)

            expected = "Enter Windows LANGID values. A value of 0 will exit.\n"
            self.assertEqual(output.getvalue(), expected)

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
            self.assertEqual(len(windowsIdCodes), 2)
            self.assertEqual(windowsIdCodes[0], 9)
            self.assertEqual(windowsIdCodes[1], 12)
            self.assertEqual(len(windowsIdCodeList), 5)
            self.assertEqual(windowsIdCodeList[0], 3081)
            self.assertEqual(windowsIdCodeList[1], 10249)
            self.assertEqual(windowsIdCodeList[2], 4105)
            self.assertEqual(windowsIdCodeList[3], 2060)
            self.assertEqual(windowsIdCodeList[4], 11276)

            expected = "Enter Windows LANGID values. A value of 0 will exit.\n"
            self.assertEqual(output.getvalue(), expected)

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
            self.assertTrue(testobj.newLanguage())

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            expected += "Enter Windows LANGID values. A value of 0 will exit.\n"
            expected += "New Entry:\n"
            expected += "{'LANG': 'tl', 'LANG_regions': ['AU', 'US'], 'LANGID': [9], "
            expected += "'LANGID_regions': [3081, 10249, 4105], 'isoCode': 'tl', 'compileSwitch': 'TESTLANG_ERRORS'}\n"
            self.assertEqual(output.getvalue(), expected)

            self.assertIsNotNone(testobj.langJsonData['languages']['testlang'])
            self.assertEqual(testobj.langJsonData['languages']['testlang']['LANG'], 'tl')

            self.assertEqual(len(testobj.langJsonData['languages']['testlang']['LANG_regions']), 2)
            self.assertEqual(testobj.langJsonData['languages']['testlang']['LANG_regions'][0], 'AU')
            self.assertEqual(testobj.langJsonData['languages']['testlang']['LANG_regions'][1], 'US')

            self.assertEqual(len(testobj.langJsonData['languages']['testlang']['LANGID']), 1)
            self.assertEqual(testobj.langJsonData['languages']['testlang']['LANGID'][0], (3081 & 0x0FF))

            self.assertEqual(len(testobj.langJsonData['languages']['testlang']['LANGID_regions']), 3)
            self.assertEqual(testobj.langJsonData['languages']['testlang']['LANGID_regions'][0], 3081)
            self.assertEqual(testobj.langJsonData['languages']['testlang']['LANGID_regions'][1], 10249)
            self.assertEqual(testobj.langJsonData['languages']['testlang']['LANGID_regions'][2], 4105)

            self.assertEqual(testobj.langJsonData['languages']['testlang']['isoCode'], 'tl')
            self.assertEqual(testobj.langJsonData['languages']['testlang']['compileSwitch'], 'TESTLANG_ERRORS')

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
            self.assertFalse(testobj.newLanguage())

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            expected += "Enter Windows LANGID values. A value of 0 will exit.\n"
            expected += "New Entry:\n"
            expected += "{'LANG': 'tl', 'LANG_regions': ['AU', 'US'], 'LANGID': [9], "
            expected += "'LANGID_regions': [3081, 10249, 4105], 'isoCode': 'tl', 'compileSwitch': 'NEWLANG_ERRORS'}\n"
            self.assertEqual(output.getvalue(), expected)

            langKeys = list(testobj.langJsonData['languages'].keys())
            self.assertNotIn('newlang', langKeys)

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
            self.assertTrue(testobj.newLanguage())

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
            self.assertEqual(output.getvalue(), expected)

            langKeys = list(testobj.langJsonData['languages'].keys())
            self.assertNotIn('newlang', langKeys)
            self.assertIn('newtstlang', langKeys)

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

        self.assertEqual(testStr, expected)

class Unittest02JsonLanguageListInputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.testJson = os.path.join(TESTFILEPATH, "testdata.json")
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("jsonLanguageDescriptionList.json"):
            os.remove("jsonLanguageDescriptionList.json")   # Delete in case it was accidently created
        return super().tearDownClass()

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
            self.assertEqual(testobj._inputLanguageName(), 'klingon')
            self.assertEqual(output.getvalue(), "")

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
            self.assertEqual(testobj._inputLanguageName(), 'romulan')
            self.assertEqual(output.getvalue(), "Error: Only characters a-z are allowed in the <lang> name, try again.\n")

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
            self.assertEqual(testobj._inputLanguageName(), 'romulan')
            expected = "Error: Only characters a-z are allowed in the <lang> name, try again.\n"
            expected += "Error: Only characters a-z are allowed in the <lang> name, try again.\n"
            expected += "Error: Only characters a-z are allowed in the <lang> name, try again.\n"
            self.assertEqual(output.getvalue(), expected)

    def test04InputIsoCodeGood(self):
        """!
        @brief Test _inputIsoTranslateCode() method, good first try
        """
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', return_value='kl'):
            testobj = LanguageDescriptionList()
            self.assertEqual(testobj._inputIsoTranslateCode(), 'kl')
            self.assertEqual(output.getvalue(), "")

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
            self.assertEqual(testobj._inputIsoTranslateCode(), 'rm')
            self.assertEqual(output.getvalue(), "Error: Only two characters a-z are allowed in the code, try again.\n")

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
            self.assertEqual(testobj._inputIsoTranslateCode(), 'rm')
            expected = "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected += "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected += "Error: Only two characters a-z are allowed in the code, try again.\n"
            self.assertEqual(output.getvalue(), expected)

    def test07InputLinuxLangCodeGood(self):
        """!
        @brief Test _inputLinuxLangCode() method, good first try
        """
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', return_value='kl'):
            testobj = LanguageDescriptionList()
            self.assertEqual(testobj._inputLinuxLangCode(), 'kl')
            self.assertEqual(output.getvalue(), "")

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
            self.assertEqual(testobj._inputLinuxLangCode(), 'rm')
            self.assertEqual(output.getvalue(), "Error: Only two characters a-z are allowed in the code, try again.\n")

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
            self.assertEqual(testobj._inputLinuxLangCode(), 'rm')
            expected = "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected += "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected += "Error: Only two characters a-z are allowed in the code, try again.\n"
            self.assertEqual(output.getvalue(), expected)

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
            self.assertEqual(len(regionList), 1)
            self.assertEqual(regionList[0], 'HK')

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            self.assertEqual(output.getvalue(), expected)

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
            self.assertEqual(len(regionList), 2)
            self.assertEqual(regionList[0], 'RH')
            self.assertEqual(regionList[1], 'RL')

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            expected += "Error: Only two characters A-Z are allowed in the code, try again.\n"
            expected += "Error: Only two characters A-Z are allowed in the code, try again.\n"
            expected += "Error: Only two characters A-Z are allowed in the code, try again.\n"
            self.assertEqual(output.getvalue(), expected)

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
            self.assertEqual(len(windowsIdCodes), 1)
            self.assertEqual(windowsIdCodes[0], (1157 & 0xFF))
            self.assertEqual(len(windowsIdCodeList), 1)
            self.assertEqual(windowsIdCodeList[0], 1157)

            expected = "Enter Windows LANGID values. A value of 0 will exit.\n"
            self.assertEqual(output.getvalue(), expected)

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
            self.assertEqual(len(windowsIdCodes), 1)
            self.assertEqual(windowsIdCodes[0], 9)
            self.assertEqual(len(windowsIdCodeList), 3)
            self.assertEqual(windowsIdCodeList[0], 3081)
            self.assertEqual(windowsIdCodeList[1], 10249)
            self.assertEqual(windowsIdCodeList[2], 4105)

            expected = "Enter Windows LANGID values. A value of 0 will exit.\n"
            self.assertEqual(output.getvalue(), expected)

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
            self.assertEqual(len(windowsIdCodes), 2)
            self.assertEqual(windowsIdCodes[0], 9)
            self.assertEqual(windowsIdCodes[1], 12)
            self.assertEqual(len(windowsIdCodeList), 5)
            self.assertEqual(windowsIdCodeList[0], 3081)
            self.assertEqual(windowsIdCodeList[1], 10249)
            self.assertEqual(windowsIdCodeList[2], 4105)
            self.assertEqual(windowsIdCodeList[3], 2060)
            self.assertEqual(windowsIdCodeList[4], 11276)

            expected = "Enter Windows LANGID values. A value of 0 will exit.\n"
            self.assertEqual(output.getvalue(), expected)

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
            self.assertTrue(testobj.newLanguage())

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            expected += "Enter Windows LANGID values. A value of 0 will exit.\n"
            expected += "New Entry:\n"
            expected += "{'LANG': 'tl', 'LANG_regions': ['AU', 'US'], 'LANGID': [9], "
            expected += "'LANGID_regions': [3081, 10249, 4105], 'isoCode': 'tl', 'compileSwitch': 'TESTLANG_ERRORS'}\n"
            self.assertEqual(output.getvalue(), expected)

            self.assertIsNotNone(testobj.langJsonData['languages']['testlang'])
            self.assertEqual(testobj.langJsonData['languages']['testlang']['LANG'], 'tl')

            self.assertEqual(len(testobj.langJsonData['languages']['testlang']['LANG_regions']), 2)
            self.assertEqual(testobj.langJsonData['languages']['testlang']['LANG_regions'][0], 'AU')
            self.assertEqual(testobj.langJsonData['languages']['testlang']['LANG_regions'][1], 'US')

            self.assertEqual(len(testobj.langJsonData['languages']['testlang']['LANGID']), 1)
            self.assertEqual(testobj.langJsonData['languages']['testlang']['LANGID'][0], (3081 & 0x0FF))

            self.assertEqual(len(testobj.langJsonData['languages']['testlang']['LANGID_regions']), 3)
            self.assertEqual(testobj.langJsonData['languages']['testlang']['LANGID_regions'][0], 3081)
            self.assertEqual(testobj.langJsonData['languages']['testlang']['LANGID_regions'][1], 10249)
            self.assertEqual(testobj.langJsonData['languages']['testlang']['LANGID_regions'][2], 4105)

            self.assertEqual(testobj.langJsonData['languages']['testlang']['isoCode'], 'tl')
            self.assertEqual(testobj.langJsonData['languages']['testlang']['compileSwitch'], 'TESTLANG_ERRORS')

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
            self.assertFalse(testobj.newLanguage())

            expected = "Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).\n"
            expected += "Enter empty string to exit.\n"
            expected += "Enter Windows LANGID values. A value of 0 will exit.\n"
            expected += "New Entry:\n"
            expected += "{'LANG': 'tl', 'LANG_regions': ['AU', 'US'], 'LANGID': [9], "
            expected += "'LANGID_regions': [3081, 10249, 4105], 'isoCode': 'tl', 'compileSwitch': 'NEWLANG_ERRORS'}\n"
            self.assertEqual(output.getvalue(), expected)

            langKeys = list(testobj.langJsonData['languages'].keys())
            self.assertNotIn('newlang', langKeys)

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
            self.assertTrue(testobj.newLanguage())

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
            self.assertEqual(output.getvalue(), expected)

            langKeys = list(testobj.langJsonData['languages'].keys())
            self.assertNotIn('newlang', langKeys)
            self.assertIn('newtstlang', langKeys)

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

        self.assertEqual(testStr, expected)

if __name__ == '__main__':
    unittest.main()