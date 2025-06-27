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
from unittest.mock import patch, MagicMock

import io
import contextlib

from dir_init import TESTFILEPATH
from dir_init import pathincsetup
pathincsetup()

from code_tools.base.json_string_class_description import TranslationTextParser
from code_tools.base.json_string_class_description import StringClassDescription
from code_tools.base.param_return_tools import ParamRetDict
from code_tools.base.json_language_list import LanguageDescriptionList

class Unittest02StringClassDescription(unittest.TestCase):
    """!
    @brief Unit test for the StringClassDescription class
    """
    @classmethod
    def setUpClass(cls):
        cls.testJson = os.path.join(TESTFILEPATH, "teststrdesc.json")
        cls.testlanglist = os.path.join(TESTFILEPATH, "teststringlanglist.json")
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("jsonStringClassDescription.json"):
            os.remove("jsonStringClassDescription.json")   # Delete in case it was accidently created
        if os.path.exists("temp.json"):
            os.remove("temp.json")   # Delete in case it was accidently not deleted
        return super().tearDownClass()

    def test01DefaultConstructor(self):
        """!
        @brief Test Default constructor()
        """
        testobj = StringClassDescription()
        self.assertRaises(FileNotFoundError)
        self.assertEqual(testobj.filename, "jsonStringClassDescription.json")
        self.assertEqual(testobj.stringJasonData['baseClassName'], "baseclass")
        self.assertEqual(testobj.stringJasonData['namespace'], "myNamespace")
        self.assertEqual(testobj.stringJasonData['dynamicCompileSwitch'], "DYNAMIC_INTERNATIONALIZATION")
        self.assertEqual(len(testobj.stringJasonData['propertyMethods']), 0)
        self.assertEqual(len(testobj.stringJasonData['translateMethods']), 0)

    def test02ConstructorWithFile(self):
        """!
        @brief Test Default constructor()
        """
        testobj = StringClassDescription(self.testJson)
        self.assertEqual(testobj.filename, self.testJson)
        self.assertEqual(testobj.stringJasonData['baseClassName'], "ParserStringListInterface")
        self.assertEqual(testobj.stringJasonData['namespace'], "argparser")
        self.assertEqual(testobj.stringJasonData['dynamicCompileSwitch'], "TEST_DYNAMIC_INTERNATIONALIZATION")
        self.assertEqual(len(testobj.stringJasonData['propertyMethods']), 1)
        self.assertEqual(list(testobj.stringJasonData['propertyMethods'])[0], 'getLangIsoCode')
        self.assertEqual(len(testobj.stringJasonData['translateMethods']), 1)
        self.assertEqual(list(testobj.stringJasonData['translateMethods'])[0], 'getNotListTypeMessage')

    def test03GetCommitOverwriteFlagNo(self):
        """!
        @brief Test _getCommitOverWriteFlag method, no answer
        """
        testobj = StringClassDescription()
        with patch('builtins.input', side_effect='n') as inMock:
            self.assertFalse(testobj._getCommitOverWriteFlag("testEntry"))
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='N') as inMock:
            self.assertFalse(testobj._getCommitOverWriteFlag("testEntry"))
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='No') as inMock:
            self.assertFalse(testobj._getCommitOverWriteFlag("testEntry"))
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

    def test04GetCommitOverwriteFlagYes(self):
        """!
        @brief Test _getCommitOverWriteFlag method, Yes answer
        """
        testobj = StringClassDescription()
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

    def test05GetCommitOverwriteFlagOverride(self):
        """!
        @brief Test _getCommitOverWriteFlag method, override=True
        """
        testobj = StringClassDescription()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertTrue(testobj._getCommitOverWriteFlag("testEntry", True))
            self.assertEqual(output.getvalue(), "")

    def test06GetCommitNewFlagNo(self):
        """!
        @brief Test _getCommitNewFlag method, no answer
        """
        testobj = StringClassDescription()
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

    def test07GetCommitNewFlagYes(self):
        """!
        @brief Test _getCommitNewFlag method, Yes answer
        """
        testobj = StringClassDescription()
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

    def test08GetCommitFlag(self):
        """!
        @brief Test _getCommitFlag method
        """
        testobj = StringClassDescription()
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

    def test09SetBaseClassName(self):
        """!
        @brief Test setBaseClassName method
        """
        testobj = StringClassDescription()
        self.assertEqual(testobj.stringJasonData['baseClassName'], "baseclass")
        testobj.setBaseClassName("NewClassName")
        self.assertEqual(testobj.stringJasonData['baseClassName'], "NewClassName")

    def test10GetBaseClassName(self):
        """!
        @brief Test getBaseClassName method
        """
        testobj = StringClassDescription()
        self.assertEqual(testobj.stringJasonData['baseClassName'], testobj.getBaseClassName())

    def test11GetBaseClassNameWithNamespace(self):
        """!
        @brief Test getBaseClassNameWithNamespace method
        """
        testobj = StringClassDescription()
        self.assertEqual(testobj.getBaseClassNameWithNamespace("Foo","."), "Foo.baseclass")

    def test12GetLanguageClassName(self):
        """!
        @brief Test getLanguageClassName method
        """
        testobj = StringClassDescription()
        self.assertEqual(testobj.getLanguageClassName(), "baseclass")
        self.assertEqual(testobj.getLanguageClassName("english"), "baseclassEnglish")

    def test13GetLanguageClassNameWithNamespace(self):
        """!
        @brief Test getLanguageClassNameWithNamespace method
        """
        testobj = StringClassDescription()
        self.assertEqual(testobj.getLanguageClassNameWithNamespace("Moo"), "Moo::baseclass")
        self.assertEqual(testobj.getLanguageClassNameWithNamespace("Moo", ",", "english"), "Moo,baseclassEnglish")

    def test14SetNamespaceName(self):
        """!
        @brief Test setNamespaceName method
        """
        testobj = StringClassDescription()
        self.assertEqual(testobj.stringJasonData['namespace'], "myNamespace")
        testobj.setNamespaceName("NewNamespace")
        self.assertEqual(testobj.stringJasonData['namespace'], "NewNamespace")

    def test15GetNamespaceName(self):
        """!
        @brief Test getNamespaceName method
        """
        testobj = StringClassDescription()
        self.assertEqual(testobj.stringJasonData['namespace'], testobj.getNamespaceName())

    def test16SetDynamicCompileSwitch(self):
        """!
        @brief Test setDynamicCompileSwitch method
        """
        testobj = StringClassDescription()
        self.assertEqual(testobj.stringJasonData['dynamicCompileSwitch'], "DYNAMIC_INTERNATIONALIZATION")
        testobj.setDynamicCompileSwitch("MY_DYNAMIC_SWITCH")
        self.assertEqual(testobj.stringJasonData['dynamicCompileSwitch'], "MY_DYNAMIC_SWITCH")

    def test17GetDynamicCompileSwitch(self):
        """!
        @brief Test getDynamicCompileSwitch method
        """
        testobj = StringClassDescription()
        self.assertEqual(testobj.stringJasonData['dynamicCompileSwitch'], testobj.getDynamicCompileSwitch())

    def test18DefinePropertyFunctionEntry(self):
        """!
        @brief Test _definePropertyFunctionEntry method
        """
        testobj = StringClassDescription()
        propertyDict = testobj._definePropertyFunctionEntry("silly", "Silly property", "integer", "Some number")
        self.assertEqual(propertyDict['name'], "silly")
        self.assertEqual(propertyDict['briefDesc'], "Silly property")
        self.assertIsInstance(propertyDict['params'], list)
        self.assertEqual(len(propertyDict['params']), 0)
        self.assertIsInstance(propertyDict['return'], dict)
        self.assertEqual(len(propertyDict['return']), 3)
        self.assertEqual(propertyDict['return']['type'], "integer")
        self.assertEqual(propertyDict['return']['desc'], "Some number")
        self.assertEqual(propertyDict['return']['typeMod'], 0)

        propertyDict = testobj._definePropertyFunctionEntry("billy", "Billy property", "size", "Some size list", True)
        self.assertEqual(propertyDict['name'], "billy")
        self.assertEqual(propertyDict['briefDesc'], "Billy property")
        self.assertIsInstance(propertyDict['params'], list)
        self.assertEqual(len(propertyDict['params']), 0)
        self.assertIsInstance(propertyDict['return'], dict)
        self.assertEqual(len(propertyDict['return']), 3)
        self.assertEqual(propertyDict['return']['type'], "size")
        self.assertEqual(propertyDict['return']['desc'], "Some size list")
        self.assertEqual(propertyDict['return']['typeMod'], ParamRetDict.typeModList)

    def test19GetPropertyMethodList(self):
        """!
        @brief Test getPropertyMethodList method
        """
        testobj = StringClassDescription(self.testJson)
        propertyList = testobj.getPropertyMethodList()
        self.assertEqual(len(propertyList), 1)
        self.assertEqual(propertyList[0], 'getLangIsoCode')

    def test20GetIsoPropertyMethodName(self):
        """!
        @brief Test getIsoPropertyMethodName method
        """
        testobj = StringClassDescription(self.testJson)
        name = testobj.getIsoPropertyMethodName()
        self.assertEqual(name, 'getLangIsoCode')

    def test21GetIsoPropertyMethodNameFail(self):
        """!
        @brief Test getIsoPropertyMethodName method
        """
        testobj = StringClassDescription()
        name = testobj.getIsoPropertyMethodName()
        self.assertIsNone(name)

    def test22GetPropertyMethodData(self):
        """!
        @brief Test getPropertyMethodData method
        """
        testobj = StringClassDescription(self.testJson)
        propertyName, propertyDesc, paramList, returnDict = testobj.getPropertyMethodData('getLangIsoCode')
        self.assertEqual(propertyName, 'isoCode')
        self.assertEqual(propertyDesc, 'Get the ISO 639 set 1 language code for this object')
        self.assertIsInstance(paramList, list)
        self.assertEqual(len(paramList), 0)
        self.assertIsInstance(returnDict, dict)
        self.assertEqual(len(returnDict), 3)
        self.assertEqual(returnDict['type'], 'string')
        self.assertEqual(returnDict['desc'], 'ISO 639 set 1 language code')
        self.assertEqual(returnDict['typeMod'], 0)

    def test23DefineTranslationDict(self):
        """!
        @brief Test _defineTranslationDict method
        """
        transDataList = [(TranslationTextParser.parsedTypeText, "Simple text with "),
                         (TranslationTextParser.parsedTypeParam, "paramName")]

        testobj = StringClassDescription()
        returnDict = testobj._defineTranslationDict("es", transDataList)
        self.assertIsInstance(returnDict, dict)
        self.assertEqual(len(returnDict), 1)
        self.assertIsInstance(returnDict['es'], list)
        self.assertEqual(len(returnDict['es']), 2)
        self.assertEqual(returnDict['es'][0][0], TranslationTextParser.parsedTypeText)
        self.assertEqual(returnDict['es'][0][1], "Simple text with ")
        self.assertEqual(returnDict['es'][1][0], TranslationTextParser.parsedTypeParam)
        self.assertEqual(returnDict['es'][1][1], "paramName")

    def test24DefineTranslationDictNoList(self):
        """!
        @brief Test _defineTranslationDict method, no translation text list
        """
        testobj = StringClassDescription()
        returnDict = testobj._defineTranslationDict("zh")
        self.assertIsInstance(returnDict, dict)
        self.assertEqual(len(returnDict), 1)
        self.assertIsNone(returnDict['zh'])

    def test25DefineTranslationDictDefault(self):
        """!
        @brief Test _defineTranslationDict method, no input
        """
        testobj = StringClassDescription()
        returnDict = testobj._defineTranslationDict()
        self.assertIsInstance(returnDict, dict)
        self.assertEqual(len(returnDict), 1)
        self.assertIsNone(returnDict['en'])

    def test26AddManualTranslation(self):
        """!
        @brief Test addManualTranslation method, success
        """
        transDataList = [(TranslationTextParser.parsedTypeText, "Simple text")]

        testobj = StringClassDescription(self.testJson)
        self.assertTrue(testobj.addManualTranslation('getNotListTypeMessage', "es", transDataList))
        self.assertIsInstance(testobj.stringJasonData['translateMethods']['getNotListTypeMessage']['translateDesc']['es'], list)
        self.assertEqual(len(testobj.stringJasonData['translateMethods']['getNotListTypeMessage']['translateDesc']['es']), 1)
        self.assertEqual(testobj.stringJasonData['translateMethods']['getNotListTypeMessage']['translateDesc']['es'][0][0], TranslationTextParser.parsedTypeText)
        self.assertEqual(testobj.stringJasonData['translateMethods']['getNotListTypeMessage']['translateDesc']['es'][0][1], "Simple text")

    def test27AddManualTranslationFailNoTextData(self):
        """!
        @brief Test addManualTranslation method, fail for no textData
        """
        testobj = StringClassDescription(self.testJson)
        self.assertFalse(testobj.addManualTranslation('getNotListTypeMessage', "fr"))

    def test28AddManualTranslationFailNoMethodName(self):
        """!
        @brief Test addManualTranslation method, fail for no textData
        """
        transDataList = [(TranslationTextParser.parsedTypeText, "Simple text")]
        testobj = StringClassDescription(self.testJson)
        self.assertFalse(testobj.addManualTranslation('getSomethingElse', "fr", transDataList))

    def test29TranslateText(self):
        """!
        @brief Test _translateText method, dummy translate
        """
        class dummyTranslate:
            def translate(self, text, target_language, format_, source_language, model):
                return {'translatedText': "Translated Text"}

        testobj = StringClassDescription()
        testobj.transClient = dummyTranslate()
        self.assertEqual(testobj._translateText("en", "zh", "Some Text"), "Translated Text")

    def test30TranslateTextMockGoogle(self):
        """!
        @brief Test _translateText method, mock google.translate client
        """
        class mockDummyTranslate:
            def translate(self, text, target_language, format_, source_language, model):
                return {'translatedText': "Patch Translated Text"}

        testobj = StringClassDescription()
        with patch('google.cloud.translate_v2.Client', MagicMock(return_value=mockDummyTranslate())):
            self.assertEqual(testobj._translateText("fr", "en", "Some Other Text"), "Patch Translated Text")

    def test31TranslateMethodTextNoLangList(self):
        """!
        @brief Test _translateText method, no language list
        """
        testobj = StringClassDescription(self.testJson)
        testobj._translateMethodText("getNotListTypeMessage")
        transMethodDesc = testobj.stringJasonData['translateMethods']['getNotListTypeMessage']['translateDesc']
        self.assertEqual(len(transMethodDesc), 1)
        self.assertIn('en', list(transMethodDesc))

    def test32TranslateMethodTextMockGoogle(self):
        """!
        @brief Test _translateText method, mock google.translate client
        """
        class mockDummyTranslate:
            def translate(self, text, target_language, format_, source_language, model):
                return {'translatedText': "Patch Translated Method Text @nargs@"}

        langList = LanguageDescriptionList(self.testlanglist)
        testobj = StringClassDescription(self.testJson)
        with patch('google.cloud.translate_v2.Client', MagicMock(return_value=mockDummyTranslate())):
            testobj._translateMethodText("getNotListTypeMessage", langList)
            transMethodDesc = testobj.stringJasonData['translateMethods']['getNotListTypeMessage']['translateDesc']
            self.assertEqual(len(transMethodDesc), 2)
            self.assertIn('es', list(transMethodDesc))

            transList = transMethodDesc['es']
            self.assertEqual(len(transList),2)
            self.assertEqual(transList[0][0], TranslationTextParser.parsedTypeText)
            self.assertEqual(transList[0][1], "Patch Translated Method Text ")
            self.assertEqual(transList[1][0], TranslationTextParser.parsedTypeParam)
            self.assertEqual(transList[1][1], "nargs")

    def test33DefineTranslateFunctionEntry(self):
        """!
        @brief Test _defineTranslateFunctionEntry method
        """
        testparams = [ParamRetDict.buildParamDictWithMod("name", "string", "desc", 0)]
        testret = ParamRetDict.buildReturnDictWithMod("string","return string",0)
        transList = [(TranslationTextParser.parsedTypeText, "Return text of "),
                     (TranslationTextParser.parsedTypeParam,"name")]
        testobj = StringClassDescription()
        functionDict = testobj._defineTranslateFunctionEntry("Brief Description", testparams, testret, "en", transList)

        self.assertEqual(functionDict['briefDesc'], "Brief Description")
        self.assertIsInstance(functionDict['params'], list)
        self.assertEqual(len(functionDict['params']), len(testparams))
        for index, parmDict in enumerate(testparams):
            self.assertIsInstance(functionDict['params'][index], dict)
            for id in list(testret):
                self.assertEqual(len(functionDict['params'][index]), len(parmDict))
                self.assertEqual(functionDict['params'][index][id], parmDict[id])

        self.assertIsInstance(functionDict['return'], dict)
        self.assertEqual(len(functionDict['return']), len(testret))
        for id in list(testret):
            self.assertEqual(functionDict['return'][id], testret[id])

        self.assertIsInstance(functionDict['translateDesc'], dict)
        self.assertEqual(len(functionDict['translateDesc']), 1)
        self.assertEqual(len(functionDict['translateDesc']['en']), len(transList))
        for index, transTuple in enumerate(transList):
            self.assertEqual(functionDict['translateDesc']['en'][index][0], transTuple[0])
            self.assertEqual(functionDict['translateDesc']['en'][index][1], transTuple[1])

    def test34GetTranlateMethodList(self):
        """!
        @brief Test getTranlateMethodList method
        """
        testobj = StringClassDescription(self.testJson)
        transFuncList = testobj.getTranlateMethodList()
        self.assertEqual(len(transFuncList), 1)
        self.assertEqual(transFuncList[0], 'getNotListTypeMessage')

    def test35GetTranlateMethodFunctionData(self):
        """!
        @brief Test getTranlateMethodFunctionData method
        """
        testobj = StringClassDescription(self.testJson)
        briefDesc, paramData, returnData = testobj.getTranlateMethodFunctionData('getNotListTypeMessage')

        self.assertEqual(briefDesc, 'Return non-list varg error message')
        self.assertIsInstance(paramData, list)
        self.assertEqual(len(paramData), 1)
        self.assertIsInstance(paramData[0], dict)
        self.assertEqual(len(paramData[0]), 4)

        self.assertIsInstance(returnData, dict)
        self.assertEqual(len(returnData), 3)

    def test36GetTranlateMethodTextData(self):
        """!
        @brief Test getTranlateMethodTextData method
        """
        testobj = StringClassDescription(self.testJson)
        transStringList = testobj.getTranlateMethodTextData('getNotListTypeMessage', 'en')
        self.assertIsInstance(transStringList, list)
        self.assertEqual(len(transStringList), 2)
        self.assertEqual(transStringList[0][0], TranslationTextParser.parsedTypeText)
        self.assertEqual(transStringList[0][1], "Only list type arguments can have an argument count of ")
        self.assertEqual(transStringList[1][0], TranslationTextParser.parsedTypeParam)
        self.assertEqual(transStringList[1][1], "nargs")

    def test37Update(self):
        """!
        @brief Test update()
        """

        testobj = StringClassDescription("temp.json")
        self.assertRaises(FileNotFoundError)
        self.assertEqual(testobj.filename, "temp.json")
        self.assertEqual(testobj.stringJasonData['baseClassName'], "baseclass")
        self.assertEqual(testobj.stringJasonData['namespace'], "myNamespace")
        self.assertEqual(testobj.stringJasonData['dynamicCompileSwitch'], "DYNAMIC_INTERNATIONALIZATION")
        self.assertEqual(len(testobj.stringJasonData['propertyMethods']), 0)
        self.assertEqual(len(testobj.stringJasonData['translateMethods']), 0)

        testobj.stringJasonData['baseClassName'] = "foobar"
        testobj.stringJasonData['namespace'] = "planetx"
        testobj.stringJasonData['dynamicCompileSwitch'] = "MAGIC"
        newPropertyEntry = testobj._definePropertyFunctionEntry("Distance", "Distance to star in AU", "integer", "AU to star")
        testobj.stringJasonData['propertyMethods']['testProperty'] = newPropertyEntry

        xlateRetDict = ParamRetDict.buildReturnDictWithMod("integer", "Xlated units", 0)
        paramList = [ParamRetDict.buildParamDictWithMod("units", "integer", "Units to translate", 0)]
        translateTextList = TranslationTextParser.parseTranslateString("Test string @units@")
        newXlateEntry = testobj._defineTranslateFunctionEntry("Brief xlate desc", paramList, xlateRetDict, "en", translateTextList)
        testobj.stringJasonData['translateMethods']['testXlate'] = newXlateEntry

        testobj.update()
        updateobj = StringClassDescription("temp.json")

        self.assertEqual(updateobj.filename, "temp.json")
        self.assertEqual(updateobj.stringJasonData['baseClassName'], "foobar")
        self.assertEqual(updateobj.stringJasonData['namespace'], "planetx")
        self.assertEqual(updateobj.stringJasonData['dynamicCompileSwitch'], "MAGIC")

        self.assertEqual(len(updateobj.stringJasonData['propertyMethods']), 1)

        self.assertIsInstance(updateobj.stringJasonData['propertyMethods']['testProperty'], dict)
        self.assertEqual(len(updateobj.stringJasonData['propertyMethods']['testProperty']), 4)
        self.assertEqual(updateobj.stringJasonData['propertyMethods']['testProperty']['name'], 'Distance')
        self.assertEqual(updateobj.stringJasonData['propertyMethods']['testProperty']['briefDesc'], 'Distance to star in AU')

        self.assertIsInstance(updateobj.stringJasonData['propertyMethods']['testProperty']['params'], list)
        self.assertEqual(len(updateobj.stringJasonData['propertyMethods']['testProperty']['params']), 0)

        self.assertIsInstance(updateobj.stringJasonData['propertyMethods']['testProperty']['return'], dict)
        self.assertEqual(len(updateobj.stringJasonData['propertyMethods']['testProperty']['return']), 3)
        self.assertEqual(updateobj.stringJasonData['propertyMethods']['testProperty']['return']['type'], "integer")
        self.assertEqual(updateobj.stringJasonData['propertyMethods']['testProperty']['return']['desc'], "AU to star")
        self.assertEqual(updateobj.stringJasonData['propertyMethods']['testProperty']['return']['typeMod'], 0)

        self.assertEqual(len(updateobj.stringJasonData['translateMethods']), 1)
        self.assertIsInstance(updateobj.stringJasonData['translateMethods']['testXlate'], dict)
        self.assertEqual(len(updateobj.stringJasonData['translateMethods']['testXlate']), 4)
        self.assertIsInstance(updateobj.stringJasonData['translateMethods']['testXlate']['params'], list)
        self.assertEqual(len(updateobj.stringJasonData['translateMethods']['testXlate']['params']), 1)
        self.assertIsInstance(updateobj.stringJasonData['translateMethods']['testXlate']['params'][0], dict)
        self.assertEqual(len(updateobj.stringJasonData['translateMethods']['testXlate']['params'][0]), 4)
        self.assertEqual(updateobj.stringJasonData['translateMethods']['testXlate']['params'][0]['name'], "units")
        self.assertEqual(updateobj.stringJasonData['translateMethods']['testXlate']['params'][0]['type'], "integer")
        self.assertEqual(updateobj.stringJasonData['translateMethods']['testXlate']['params'][0]['desc'], "Units to translate")
        self.assertEqual(updateobj.stringJasonData['translateMethods']['testXlate']['params'][0]['typeMod'], 0)

        self.assertIsInstance(updateobj.stringJasonData['translateMethods']['testXlate']['return'], dict)
        self.assertEqual(len(updateobj.stringJasonData['translateMethods']['testXlate']['return']), 3)
        self.assertEqual(updateobj.stringJasonData['translateMethods']['testXlate']['return']['type'], "integer")
        self.assertEqual(updateobj.stringJasonData['translateMethods']['testXlate']['return']['desc'], "Xlated units")
        self.assertEqual(updateobj.stringJasonData['translateMethods']['testXlate']['return']['typeMod'], 0)

        self.assertIsInstance(updateobj.stringJasonData['translateMethods']['testXlate']['translateDesc'], dict)
        self.assertEqual(len(updateobj.stringJasonData['translateMethods']['testXlate']['translateDesc']), 1)
        self.assertIsInstance(updateobj.stringJasonData['translateMethods']['testXlate']['translateDesc']['en'], list)
        self.assertEqual(len(updateobj.stringJasonData['translateMethods']['testXlate']['translateDesc']['en']), 2)
        self.assertEqual(updateobj.stringJasonData['translateMethods']['testXlate']['translateDesc']['en'][0][0], TranslationTextParser.parsedTypeText)
        self.assertEqual(updateobj.stringJasonData['translateMethods']['testXlate']['translateDesc']['en'][0][1], "Test string ")
        self.assertEqual(updateobj.stringJasonData['translateMethods']['testXlate']['translateDesc']['en'][1][0], TranslationTextParser.parsedTypeParam)
        self.assertEqual(updateobj.stringJasonData['translateMethods']['testXlate']['translateDesc']['en'][1][1], "units")

        os.remove("temp.json")

    def test38UpdateTranlations(self):
        """!
        @brief Test updateTranlations()
        """
        class mockDummyTranslate:
            def translate(self, text, target_language, format_, source_language, model):
                return {'translatedText': text}

        testobj = StringClassDescription(self.testJson)
        langList = LanguageDescriptionList(self.testlanglist)

        for methodName in testobj.getTranlateMethodList():
            self.assertEqual(len(testobj.stringJasonData['translateMethods'][methodName]['translateDesc']), 1)

        with patch('google.cloud.translate_v2.Client', MagicMock(return_value=mockDummyTranslate())):
            testobj.updateTranlations(langList)

            for methodName in testobj.getTranlateMethodList():
                self.assertEqual(len(testobj.stringJasonData['translateMethods'][methodName]['translateDesc']), 2)


if __name__ == '__main__':
    unittest.main()