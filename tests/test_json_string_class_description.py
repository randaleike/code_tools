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

import pytest
import os

from unittest.mock import patch, MagicMock

import io
import contextlib

from dir_init import TESTFILEPATH
from dir_init import pathincsetup
pathincsetup()

from code_tools_grocsoftware.base.json_string_class_description import TranslationTextParser
from code_tools_grocsoftware.base.json_string_class_description import StringClassDescription
from code_tools_grocsoftware.base.param_return_tools import ParamRetDict
from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList

class TestUnittest02StringClassDescription:
    """!
    @brief Unit test for the StringClassDescription class
    """
    @classmethod
    def setup_class(cls):
        cls.testJson = os.path.join(TESTFILEPATH, "teststrdesc.json")
        cls.testlanglist = os.path.join(TESTFILEPATH, "teststringlanglist.json")


    @classmethod
    def teardown_class(cls):
        if os.path.exists("jsonStringClassDescription.json"):
            os.remove("jsonStringClassDescription.json")   # Delete in case it was accidently created
        if os.path.exists("temp.json"):
            os.remove("temp.json")   # Delete in case it was accidently not deleted


    def test01DefaultConstructor(self):
        """!
        @brief Test Default constructor()
        """
        testobj = StringClassDescription()
        pytest.raises(FileNotFoundError)
        assert testobj.filename == "jsonStringClassDescription.json"
        assert testobj.stringJasonData['baseClassName'] == "baseclass"
        assert testobj.stringJasonData['namespace'] == "myNamespace"
        assert testobj.stringJasonData['dynamicCompileSwitch'] == "DYNAMIC_INTERNATIONALIZATION"
        assert len(testobj.stringJasonData['propertyMethods']) == 0
        assert len(testobj.stringJasonData['translateMethods']) == 0

    def test02ConstructorWithFile(self):
        """!
        @brief Test Default constructor()
        """
        testobj = StringClassDescription(self.testJson)
        assert testobj.filename == self.testJson
        assert testobj.stringJasonData['baseClassName'] == "ParserStringListInterface"
        assert testobj.stringJasonData['namespace'] == "argparser"
        assert testobj.stringJasonData['dynamicCompileSwitch'] == "TEST_DYNAMIC_INTERNATIONALIZATION"
        assert len(testobj.stringJasonData['propertyMethods']) == 1
        assert list(testobj.stringJasonData['propertyMethods'])[0] == 'getLangIsoCode'
        assert len(testobj.stringJasonData['translateMethods']) == 1
        assert list(testobj.stringJasonData['translateMethods'])[0] == 'getNotListTypeMessage'

    def test03GetCommitOverwriteFlagNo(self):
        """!
        @brief Test _getCommitOverWriteFlag method, no answer
        """
        testobj = StringClassDescription()
        with patch('builtins.input', side_effect='n') as inMock:
            assert not testobj._getCommitOverWriteFlag("testEntry")
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='N') as inMock:
            assert not testobj._getCommitOverWriteFlag("testEntry")
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

        with patch('builtins.input', side_effect='No') as inMock:
            assert not testobj._getCommitOverWriteFlag("testEntry")
            inMock.assert_called_once_with("Overwrite existing testEntry entry? [Y/N]")

    def test04GetCommitOverwriteFlagYes(self):
        """!
        @brief Test _getCommitOverWriteFlag method, Yes answer
        """
        testobj = StringClassDescription()
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

    def test05GetCommitOverwriteFlagOverride(self):
        """!
        @brief Test _getCommitOverWriteFlag method, override=True
        """
        testobj = StringClassDescription()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            assert testobj._getCommitOverWriteFlag("testEntry", True)
            assert output.getvalue() == ""

    def test06GetCommitNewFlagNo(self):
        """!
        @brief Test _getCommitNewFlag method, no answer
        """
        testobj = StringClassDescription()
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

    def test07GetCommitNewFlagYes(self):
        """!
        @brief Test _getCommitNewFlag method, Yes answer
        """
        testobj = StringClassDescription()
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

    def test08GetCommitFlag(self):
        """!
        @brief Test _getCommitFlag method
        """
        testobj = StringClassDescription()
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

    def test09SetBaseClassName(self):
        """!
        @brief Test setBaseClassName method
        """
        testobj = StringClassDescription()
        assert testobj.stringJasonData['baseClassName'] == "baseclass"
        testobj.setBaseClassName("NewClassName")
        assert testobj.stringJasonData['baseClassName'] == "NewClassName"

    def test10GetBaseClassName(self):
        """!
        @brief Test getBaseClassName method
        """
        testobj = StringClassDescription()
        assert testobj.stringJasonData['baseClassName'] == testobj.getBaseClassName()

    def test11GetBaseClassNameWithNamespace(self):
        """!
        @brief Test getBaseClassNameWithNamespace method
        """
        testobj = StringClassDescription()
        assert testobj.getBaseClassNameWithNamespace("Foo",".") == "Foo.baseclass"

    def test12GetLanguageClassName(self):
        """!
        @brief Test getLanguageClassName method
        """
        testobj = StringClassDescription()
        assert testobj.getLanguageClassName() == "baseclass"
        assert testobj.getLanguageClassName("english") == "baseclassEnglish"

    def test13GetLanguageClassNameWithNamespace(self):
        """!
        @brief Test getLanguageClassNameWithNamespace method
        """
        testobj = StringClassDescription()
        assert testobj.getLanguageClassNameWithNamespace("Moo") == "Moo::baseclass"
        assert testobj.getLanguageClassNameWithNamespace("Moo", ",", "english") == "Moo,baseclassEnglish"

    def test14SetNamespaceName(self):
        """!
        @brief Test setNamespaceName method
        """
        testobj = StringClassDescription()
        assert testobj.stringJasonData['namespace'] == "myNamespace"
        testobj.setNamespaceName("NewNamespace")
        assert testobj.stringJasonData['namespace'] == "NewNamespace"

    def test15GetNamespaceName(self):
        """!
        @brief Test getNamespaceName method
        """
        testobj = StringClassDescription()
        assert testobj.stringJasonData['namespace'] == testobj.getNamespaceName()

    def test16SetDynamicCompileSwitch(self):
        """!
        @brief Test setDynamicCompileSwitch method
        """
        testobj = StringClassDescription()
        assert testobj.stringJasonData['dynamicCompileSwitch'] == "DYNAMIC_INTERNATIONALIZATION"
        testobj.setDynamicCompileSwitch("MY_DYNAMIC_SWITCH")
        assert testobj.stringJasonData['dynamicCompileSwitch'] == "MY_DYNAMIC_SWITCH"

    def test17GetDynamicCompileSwitch(self):
        """!
        @brief Test getDynamicCompileSwitch method
        """
        testobj = StringClassDescription()
        assert testobj.stringJasonData['dynamicCompileSwitch'] == testobj.getDynamicCompileSwitch()

    def test18DefinePropertyFunctionEntry(self):
        """!
        @brief Test _definePropertyFunctionEntry method
        """
        testobj = StringClassDescription()
        propertyDict = testobj._definePropertyFunctionEntry("silly", "Silly property", "integer", "Some number")
        assert propertyDict['name'] == "silly"
        assert propertyDict['briefDesc'] == "Silly property"
        assert isinstance(propertyDict['params'], list)
        assert len(propertyDict['params']) == 0
        assert isinstance(propertyDict['return'], dict)
        assert len(propertyDict['return']) == 3
        assert propertyDict['return']['type'] == "integer"
        assert propertyDict['return']['desc'] == "Some number"
        assert propertyDict['return']['typeMod'] == 0

        propertyDict = testobj._definePropertyFunctionEntry("billy", "Billy property", "size", "Some size list", True)
        assert propertyDict['name'] == "billy"
        assert propertyDict['briefDesc'] == "Billy property"
        assert isinstance(propertyDict['params'], list)
        assert len(propertyDict['params']) == 0
        assert isinstance(propertyDict['return'], dict)
        assert len(propertyDict['return']) == 3
        assert propertyDict['return']['type'] == "size"
        assert propertyDict['return']['desc'] == "Some size list"
        assert propertyDict['return']['typeMod'] == ParamRetDict.typeModList

    def test19GetPropertyMethodList(self):
        """!
        @brief Test getPropertyMethodList method
        """
        testobj = StringClassDescription(self.testJson)
        propertyList = testobj.getPropertyMethodList()
        assert len(propertyList) == 1
        assert propertyList[0] == 'getLangIsoCode'

    def test20GetIsoPropertyMethodName(self):
        """!
        @brief Test getIsoPropertyMethodName method
        """
        testobj = StringClassDescription(self.testJson)
        name = testobj.getIsoPropertyMethodName()
        assert name == 'getLangIsoCode'

    def test21GetIsoPropertyMethodNameFail(self):
        """!
        @brief Test getIsoPropertyMethodName method
        """
        testobj = StringClassDescription()
        name = testobj.getIsoPropertyMethodName()
        assert name is None

    def test22GetPropertyMethodData(self):
        """!
        @brief Test getPropertyMethodData method
        """
        testobj = StringClassDescription(self.testJson)
        propertyName, propertyDesc, paramList, returnDict = testobj.getPropertyMethodData('getLangIsoCode')
        assert propertyName == 'isoCode'
        assert propertyDesc == 'Get the ISO 639 set 1 language code for this object'
        assert isinstance(paramList, list)
        assert len(paramList) == 0
        assert isinstance(returnDict, dict)
        assert len(returnDict) == 3
        assert returnDict['type'] == 'string'
        assert returnDict['desc'] == 'ISO 639 set 1 language code'
        assert returnDict['typeMod'] == 0

    def test23DefineTranslationDict(self):
        """!
        @brief Test _defineTranslationDict method
        """
        transDataList = [(TranslationTextParser.parsedTypeText, "Simple text with "),
                         (TranslationTextParser.parsedTypeParam, "paramName")]

        testobj = StringClassDescription()
        returnDict = testobj._defineTranslationDict("es", transDataList)
        assert isinstance(returnDict, dict)
        assert len(returnDict) == 1
        assert isinstance(returnDict['es'], list)
        assert len(returnDict['es']) == 2
        assert returnDict['es'][0][0] == TranslationTextParser.parsedTypeText
        assert returnDict['es'][0][1] == "Simple text with "
        assert returnDict['es'][1][0] == TranslationTextParser.parsedTypeParam
        assert returnDict['es'][1][1] == "paramName"

    def test24DefineTranslationDictNoList(self):
        """!
        @brief Test _defineTranslationDict method, no translation text list
        """
        testobj = StringClassDescription()
        returnDict = testobj._defineTranslationDict("zh")
        assert isinstance(returnDict, dict)
        assert len(returnDict) == 1
        assert returnDict['zh'] is None

    def test25DefineTranslationDictDefault(self):
        """!
        @brief Test _defineTranslationDict method, no input
        """
        testobj = StringClassDescription()
        returnDict = testobj._defineTranslationDict()
        assert isinstance(returnDict, dict)
        assert len(returnDict) == 1
        assert returnDict['en'] is None

    def test26AddManualTranslation(self):
        """!
        @brief Test addManualTranslation method, success
        """
        transDataList = [(TranslationTextParser.parsedTypeText, "Simple text")]

        testobj = StringClassDescription(self.testJson)
        assert testobj.addManualTranslation('getNotListTypeMessage', "es", transDataList)
        assert isinstance(testobj.stringJasonData['translateMethods']['getNotListTypeMessage']['translateDesc']['es'], list)
        assert len(testobj.stringJasonData['translateMethods']['getNotListTypeMessage']['translateDesc']['es']) == 1
        assert testobj.stringJasonData['translateMethods']['getNotListTypeMessage']['translateDesc']['es'][0][0] == TranslationTextParser.parsedTypeText
        assert testobj.stringJasonData['translateMethods']['getNotListTypeMessage']['translateDesc']['es'][0][1] == "Simple text"

    def test27AddManualTranslationFailNoTextData(self):
        """!
        @brief Test addManualTranslation method, fail for no textData
        """
        testobj = StringClassDescription(self.testJson)
        assert not testobj.addManualTranslation('getNotListTypeMessage', "fr")

    def test28AddManualTranslationFailNoMethodName(self):
        """!
        @brief Test addManualTranslation method, fail for no textData
        """
        transDataList = [(TranslationTextParser.parsedTypeText, "Simple text")]
        testobj = StringClassDescription(self.testJson)
        assert not testobj.addManualTranslation('getSomethingElse', "fr", transDataList)

    def test29TranslateText(self):
        """!
        @brief Test _translateText method, dummy translate
        """
        class dummyTranslate:
            def translate(self, text, target_language, format_, source_language, model):
                return {'translatedText': "Translated Text"}

        testobj = StringClassDescription()
        testobj.transClient = dummyTranslate()
        assert testobj._translateText("en", "zh", "Some Text") == "Translated Text"

    def test30TranslateTextMockGoogle(self):
        """!
        @brief Test _translateText method, mock google.translate client
        """
        class mockDummyTranslate:
            def translate(self, text, target_language, format_, source_language, model):
                return {'translatedText': "Patch Translated Text"}

        testobj = StringClassDescription()
        with patch('google.cloud.translate_v2.Client', MagicMock(return_value=mockDummyTranslate())):
            assert testobj._translateText("fr", "en", "Some Other Text") == "Patch Translated Text"

    def test31TranslateMethodTextNoLangList(self):
        """!
        @brief Test _translateText method, no language list
        """
        testobj = StringClassDescription(self.testJson)
        testobj._translateMethodText("getNotListTypeMessage")
        transMethodDesc = testobj.stringJasonData['translateMethods']['getNotListTypeMessage']['translateDesc']
        assert len(transMethodDesc) == 1
        assert 'en' in list(transMethodDesc)

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
            assert len(transMethodDesc) == 2
            assert 'es' in list(transMethodDesc)

            transList = transMethodDesc['es']
            assert len(transList) ==2
            assert transList[0][0] == TranslationTextParser.parsedTypeText
            assert transList[0][1] == "Patch Translated Method Text "
            assert transList[1][0] == TranslationTextParser.parsedTypeParam
            assert transList[1][1] == "nargs"

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

        assert functionDict['briefDesc'] == "Brief Description"
        assert isinstance(functionDict['params'], list)
        assert len(functionDict['params']) == len(testparams)
        for index, parmDict in enumerate(testparams):
            assert isinstance(functionDict['params'][index], dict)
            for id in list(testret):
                assert len(functionDict['params'][index]) == len(parmDict)
                assert functionDict['params'][index][id] == parmDict[id]

        assert isinstance(functionDict['return'], dict)
        assert len(functionDict['return']) == len(testret)
        for id in list(testret):
            assert functionDict['return'][id] == testret[id]

        assert isinstance(functionDict['translateDesc'], dict)
        assert len(functionDict['translateDesc']) == 1
        assert len(functionDict['translateDesc']['en']) == len(transList)
        for index, transTuple in enumerate(transList):
            assert functionDict['translateDesc']['en'][index][0] == transTuple[0]
            assert functionDict['translateDesc']['en'][index][1] == transTuple[1]

    def test34GetTranlateMethodList(self):
        """!
        @brief Test getTranlateMethodList method
        """
        testobj = StringClassDescription(self.testJson)
        transFuncList = testobj.getTranlateMethodList()
        assert len(transFuncList) == 1
        assert transFuncList[0] == 'getNotListTypeMessage'

    def test35GetTranlateMethodFunctionData(self):
        """!
        @brief Test getTranlateMethodFunctionData method
        """
        testobj = StringClassDescription(self.testJson)
        briefDesc, paramData, returnData = testobj.getTranlateMethodFunctionData('getNotListTypeMessage')

        assert briefDesc == 'Return non-list varg error message'
        assert isinstance(paramData, list)
        assert len(paramData) == 1
        assert isinstance(paramData[0], dict)
        assert len(paramData[0]) == 4

        assert isinstance(returnData, dict)
        assert len(returnData) == 3

    def test36GetTranlateMethodTextData(self):
        """!
        @brief Test getTranlateMethodTextData method
        """
        testobj = StringClassDescription(self.testJson)
        transStringList = testobj.getTranlateMethodTextData('getNotListTypeMessage', 'en')
        assert isinstance(transStringList, list)
        assert len(transStringList) == 2
        assert transStringList[0][0] == TranslationTextParser.parsedTypeText
        assert transStringList[0][1] == "Only list type arguments can have an argument count of "
        assert transStringList[1][0] == TranslationTextParser.parsedTypeParam
        assert transStringList[1][1] == "nargs"

    def test37Update(self):
        """!
        @brief Test update()
        """

        testobj = StringClassDescription("temp.json")
        pytest.raises(FileNotFoundError)
        assert testobj.filename == "temp.json"
        assert testobj.stringJasonData['baseClassName'] == "baseclass"
        assert testobj.stringJasonData['namespace'] == "myNamespace"
        assert testobj.stringJasonData['dynamicCompileSwitch'] == "DYNAMIC_INTERNATIONALIZATION"
        assert len(testobj.stringJasonData['propertyMethods']) == 0
        assert len(testobj.stringJasonData['translateMethods']) == 0

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

        assert updateobj.filename == "temp.json"
        assert updateobj.stringJasonData['baseClassName'] == "foobar"
        assert updateobj.stringJasonData['namespace'] == "planetx"
        assert updateobj.stringJasonData['dynamicCompileSwitch'] == "MAGIC"

        assert len(updateobj.stringJasonData['propertyMethods']) == 1

        assert isinstance(updateobj.stringJasonData['propertyMethods']['testProperty'], dict)
        assert len(updateobj.stringJasonData['propertyMethods']['testProperty']) == 4
        assert updateobj.stringJasonData['propertyMethods']['testProperty']['name'] == 'Distance'
        assert updateobj.stringJasonData['propertyMethods']['testProperty']['briefDesc'] == 'Distance to star in AU'

        assert isinstance(updateobj.stringJasonData['propertyMethods']['testProperty']['params'], list)
        assert len(updateobj.stringJasonData['propertyMethods']['testProperty']['params']) == 0

        assert isinstance(updateobj.stringJasonData['propertyMethods']['testProperty']['return'], dict)
        assert len(updateobj.stringJasonData['propertyMethods']['testProperty']['return']) == 3
        assert updateobj.stringJasonData['propertyMethods']['testProperty']['return']['type'] == "integer"
        assert updateobj.stringJasonData['propertyMethods']['testProperty']['return']['desc'] == "AU to star"
        assert updateobj.stringJasonData['propertyMethods']['testProperty']['return']['typeMod'] == 0

        assert len(updateobj.stringJasonData['translateMethods']) == 1
        assert isinstance(updateobj.stringJasonData['translateMethods']['testXlate'], dict)
        assert len(updateobj.stringJasonData['translateMethods']['testXlate']) == 4
        assert isinstance(updateobj.stringJasonData['translateMethods']['testXlate']['params'], list)
        assert len(updateobj.stringJasonData['translateMethods']['testXlate']['params']) == 1
        assert isinstance(updateobj.stringJasonData['translateMethods']['testXlate']['params'][0], dict)
        assert len(updateobj.stringJasonData['translateMethods']['testXlate']['params'][0]) == 4
        assert updateobj.stringJasonData['translateMethods']['testXlate']['params'][0]['name'] == "units"
        assert updateobj.stringJasonData['translateMethods']['testXlate']['params'][0]['type'] == "integer"
        assert updateobj.stringJasonData['translateMethods']['testXlate']['params'][0]['desc'] == "Units to translate"
        assert updateobj.stringJasonData['translateMethods']['testXlate']['params'][0]['typeMod'] == 0

        assert isinstance(updateobj.stringJasonData['translateMethods']['testXlate']['return'], dict)
        assert len(updateobj.stringJasonData['translateMethods']['testXlate']['return']) == 3
        assert updateobj.stringJasonData['translateMethods']['testXlate']['return']['type'] == "integer"
        assert updateobj.stringJasonData['translateMethods']['testXlate']['return']['desc'] == "Xlated units"
        assert updateobj.stringJasonData['translateMethods']['testXlate']['return']['typeMod'] == 0

        assert isinstance(updateobj.stringJasonData['translateMethods']['testXlate']['translateDesc'], dict)
        assert len(updateobj.stringJasonData['translateMethods']['testXlate']['translateDesc']) == 1
        assert isinstance(updateobj.stringJasonData['translateMethods']['testXlate']['translateDesc']['en'], list)
        assert len(updateobj.stringJasonData['translateMethods']['testXlate']['translateDesc']['en']) == 2
        assert updateobj.stringJasonData['translateMethods']['testXlate']['translateDesc']['en'][0][0] == TranslationTextParser.parsedTypeText
        assert updateobj.stringJasonData['translateMethods']['testXlate']['translateDesc']['en'][0][1] == "Test string "
        assert updateobj.stringJasonData['translateMethods']['testXlate']['translateDesc']['en'][1][0] == TranslationTextParser.parsedTypeParam
        assert updateobj.stringJasonData['translateMethods']['testXlate']['translateDesc']['en'][1][1] == "units"

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
            assert len(testobj.stringJasonData['translateMethods'][methodName]['translateDesc']) == 1

        with patch('google.cloud.translate_v2.Client', MagicMock(return_value=mockDummyTranslate())):
            testobj.updateTranlations(langList)

            for methodName in testobj.getTranlateMethodList():
                assert len(testobj.stringJasonData['translateMethods'][methodName]['translateDesc']) == 2
