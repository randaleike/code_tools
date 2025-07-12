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
    def getExpectedReturn(expectedType:str, expectedDesc:str, expectedTypeMod:int)->str:
        """!
        @brief Return the expected print string for the input return values
        @param expectedType {string} Expected type string
        @param expectedDesc {string} Expected return description string
        @param expectedTypeMod {integer} Expected type modification value
        @return string - Expected print string
        """
        expectedStr = "'return': {'type': '"+expectedType+"', "
        expectedStr += "'desc': '"+expectedDesc+"', "
        expectedStr += "'typeMod': "+str(expectedTypeMod)+"}"
        return expectedStr

    @staticmethod
    def getExpectedParam(expectedName:str, expectedType:str, expectedDesc:str, expectedTypeMod:int)->str:
        """!
        @brief Return the expected print string for the input return values
        @param expectedName {string} Expected parameter name string
        @param expectedType {string} Expected type string
        @param expectedDesc {string} Expected parameter description string
        @param expectedTypeMod {integer} Expected type modification value
        @return string - Expected print string
        """
        expectedStr = "{'name': '"+expectedName+"', "
        expectedStr += "'type': '"+expectedType+"', "
        expectedStr += "'desc': '"+expectedDesc+"', "
        expectedStr += "'typeMod': "+str(expectedTypeMod)+"}"
        return expectedStr

    @staticmethod
    def getExpectedParamList(paramList:list)->str:
        """!
        @brief Return the expected print string for the input return values
        @param paramList {list} Expected parameter dictionary list
        @return string - Expected print string
        """
        expectedStr = "'params': ["
        if paramList is not None:
            paramPrefix = ""
            for param in paramList:
                expectedName, expectedType, expectedDesc, expectedTypeMod = ParamRetDict.getParamData(param)
                expectedStr += paramPrefix
                expectedStr += ExpectedStrHelper.getExpectedParam(expectedName, expectedType, expectedDesc, expectedTypeMod)
                paramPrefix = ", "
        expectedStr += "]"
        return expectedStr

    @staticmethod
    def getExpectedTranslationDescList(textText:str, langList:list = None)->str:
        """!
        @brief Generate the expected translation description text
        @param textText {string} Test translation text string
        @param langList {list} List of languages or None for default 'en'
        @return string - Expected print string
        """
        expectedStr = "'translateDesc': {"
        if langList is None:
            langList = ["en"]

        # Generate the translateDesc dictionary
        langListPrefix = ""
        for lang in langList:
            expectedStr += langListPrefix
            expectedStr += "'"+lang+"': ["

            # Generate the parsed text list data
            expectedTextList = TranslationTextParser.parseTranslateString(textText)
            elementPrefix = ""
            for element in expectedTextList:
                expectedStr += elementPrefix
                expectedStr += "('"+element[0]+"', '"+element[1]+"')"
                elementPrefix = ", "

            # Close the language parsed text list
            expectedStr += "]"
            langListPrefix = ", "

        # Close the translateDesc dictionary
        expectedStr += "}"
        return expectedStr

    @staticmethod
    def getExpectedNewTranslationEntry(briefDesc:str, returnData:dict, paramList:list = [], transText:str="", langList:list = None):
        """!
        @brief Get the expected new translation method entry print text

        @param briefDesc {str} Expected brief description string
        @param returnData {dict} Expected return dictionary data
        @param paramList {list} Expected parameter dictionary list
        @param transText {string} Test translation text string
        @param langList {list} List of languages or None for default 'en'

        @return string - Expected print string
        """
        expectedStr = "New Entry:\n"
        expectedStr += "{'briefDesc': '"+briefDesc+"', "
        expectedStr += ExpectedStrHelper.getExpectedParamList(paramList)
        expectedStr += ", "
        expectedStr += ExpectedStrHelper.getExpectedReturn(ParamRetDict.getReturnType(returnData),
                                              ParamRetDict.getReturnDesc(returnData),
                                              ParamRetDict.getReturnTypeMod(returnData))
        expectedStr += ", "
        expectedStr += ExpectedStrHelper.getExpectedTranslationDescList(transText, langList)
        expectedStr += "}\n"
        return expectedStr

    @staticmethod
    def getExpectedTransDescHelp()->str:
        """!
        Get the expected translation description help message
        """
        expectedStr = "Enter translation template string. Use @paramName@ in the string to indicate where the \n"
        expectedStr += "function parameters should be inserted.\n"
        expectedStr += "Example with single input parameter name \"keyString\": Found argument key @keyString@\n"
        return expectedStr

    @staticmethod
    def getExpectedNewPropertyStr(methodName:str, propertyId:str, returnData:dict):
        """!
        @brief Get the expected new translation method entry print text

        @param methodName {str} Expected method name string
        @param propertyId {str} Expected property id string
        @param returnData {dict} Expected return dictionary data
        @return string - Expected print string
        """
        expectedMethodDesc = "Get the "+ParamRetDict.getReturnDesc(returnData)+" for this object"

        expectedStr = methodName+":\n"
        expectedStr += "{'name': '"+propertyId+"', "
        expectedStr += "'briefDesc': '"+expectedMethodDesc+"', "
        expectedStr += "'params': [], "
        expectedStr += ExpectedStrHelper.getExpectedReturn(ParamRetDict.getReturnType(returnData),
                                              ParamRetDict.getReturnDesc(returnData),
                                              ParamRetDict.getReturnTypeMod(returnData))
        expectedStr += "}\n"
        return expectedStr

    @staticmethod
    def getExpectedOptionList()->tuple:
        """!
        @brief Get the expected property data list string for the unittest
        @return string - Expected property list string
        @return int - Maximum index for the list
        """
        propertyOptions = LanguageDescriptionList.getLanguagePropertyList()

        expectedStr = "Select language property, from options:\n"
        optionText = ""
        optionPrefix = "    "
        maxIndex = 0
        for index, propertyId in enumerate(propertyOptions):
            optionText += optionPrefix
            optionText += str(index)+": "
            optionText += propertyId
            optionPrefix = ", "
            maxIndex += 1

        expectedStr += optionText+"\n"
        return expectedStr, maxIndex

class Test03StringClassDescriptionMacroMethods:
    """!
    @brief Unit test for the StringClassDescription class
    """
    def test01NewTranslateMethodEntry(self):
        """!
        @brief Test newTranslateMethodEntry method, improper message
        """
        testParamlist = [ParamRetDict.buildParamDictWithMod("foo", "string", "Foo description", 0),
                         ParamRetDict.buildParamDictWithMod("moo", "integer", "Moo description", 0)]
        testReturn = ParamRetDict.buildReturnDictWithMod("string", "Return description", 0)
        testTransString = "Test string with input @foo@ and @moo@"
        inputStr = (text for text in ["getTestString",
                                      "Brief method description",
                                      str(len(testParamlist)),
                                      ParamRetDict.getParamName(testParamlist[0]),
                                      ParamRetDict.getParamType(testParamlist[0]),
                                      ParamRetDict.getParamDesc(testParamlist[0]),
                                      ParamRetDict.getParamName(testParamlist[1]),
                                      ParamRetDict.getParamType(testParamlist[1]),
                                      ParamRetDict.getParamDesc(testParamlist[1]),
                                      ParamRetDict.getReturnType(testReturn),
                                      ParamRetDict.getReturnDesc(testReturn),
                                      "en",
                                      testTransString,
                                      "y",
                                      "y"])
        def testMockIn(prompt):
            if ((prompt == "Is full type a list [y/n]:") or
                (prompt == "Is full type a pointer [y/n]:") or
                (prompt == "Is full type a reference [y/n]:") or
                (prompt == "Can value be undefined [y/n]:") or
                (prompt == "Is full type an array [y/n]:")):
                return 'n'
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription()
            assert testobj.newTranslateMethodEntry()
            assert isinstance(testobj.stringJasonData['translateMethods']['getTestString'], dict)
            assert testobj.stringJasonData['translateMethods']['getTestString']['briefDesc'] == "Brief method description"

            assert len(testobj.stringJasonData['translateMethods']['getTestString']['params']) == 2
            assert testobj.stringJasonData['translateMethods']['getTestString']['params'][0] == testParamlist[0]
            assert testobj.stringJasonData['translateMethods']['getTestString']['params'][1] == testParamlist[1]
            assert testobj.stringJasonData['translateMethods']['getTestString']['return'] == testReturn

            assert isinstance(testobj.stringJasonData['translateMethods']['getTestString']['translateDesc'], dict)
            assert len(testobj.stringJasonData['translateMethods']['getTestString']['translateDesc']) == 1
            assert isinstance(testobj.stringJasonData['translateMethods']['getTestString']['translateDesc']['en'], list)

            testParsedList = TranslationTextParser.parseTranslateString(testTransString)
            assert len(testobj.stringJasonData['translateMethods']['getTestString']['translateDesc']['en']) == len(testParsedList)

            for index, entry in enumerate(testParsedList):
                assert testobj.stringJasonData['translateMethods']['getTestString']['translateDesc']["en"][index] == entry

            expectedStr = ExpectedStrHelper.getExpectedTransDescHelp()
            expectedStr += ExpectedStrHelper.getExpectedNewTranslationEntry('Brief method description', testReturn, testParamlist, testTransString, ['en'])
            assert output.getvalue() == expectedStr

    def test02NewTranslateMethodEntryNoConfirm(self):
        """!
        @brief Test newTranslateMethodEntry method, improper message
        """
        testParamlist = [ParamRetDict.buildParamDictWithMod("foo", "string", "Foo description", 0),
                         ParamRetDict.buildParamDictWithMod("moo", "integer", "Moo description", 0)]
        testReturn = ParamRetDict.buildReturnDictWithMod("string", "Return description", 0)
        testTransString = "Test string with input @foo@ and @moo@"

        testParamlist2 = [ParamRetDict.buildParamDictWithMod("foo2", "integer", "Foo description2", 0),
                         ParamRetDict.buildParamDictWithMod("moo2", "integer", "Moo description2", 0)]
        testReturn2 = ParamRetDict.buildReturnDictWithMod("integer", "Return description2", 0)
        testTransString2 = "Test string with input @foo2@ and @moo2@"
        inputStr = (text for text in ["getTestString",
                                      "Brief method description",
                                      str(len(testParamlist)),
                                      ParamRetDict.getParamName(testParamlist[0]),
                                      ParamRetDict.getParamType(testParamlist[0]),
                                      ParamRetDict.getParamDesc(testParamlist[0]),
                                      ParamRetDict.getParamName(testParamlist[1]),
                                      ParamRetDict.getParamType(testParamlist[1]),
                                      ParamRetDict.getParamDesc(testParamlist[1]),
                                      ParamRetDict.getReturnType(testReturn),
                                      ParamRetDict.getReturnDesc(testReturn),
                                      "en",
                                      testTransString,
                                      "n",
                                      "getTestInt",
                                      "Brief method description2",
                                      str(len(testParamlist2)),
                                      ParamRetDict.getParamName(testParamlist2[0]),
                                      ParamRetDict.getParamType(testParamlist2[0]),
                                      ParamRetDict.getParamDesc(testParamlist2[0]),
                                      ParamRetDict.getParamName(testParamlist2[1]),
                                      ParamRetDict.getParamType(testParamlist2[1]),
                                      ParamRetDict.getParamDesc(testParamlist2[1]),
                                      ParamRetDict.getReturnType(testReturn2),
                                      ParamRetDict.getReturnDesc(testReturn2),
                                      "en",
                                      testTransString2,
                                      "y", "n"])
        def testMockIn(prompt):
            if ((prompt == "Is full type a list [y/n]:") or
                (prompt == "Is full type a pointer [y/n]:") or
                (prompt == "Is full type a reference [y/n]:") or
                (prompt == "Can value be undefined [y/n]:") or
                (prompt == "Is full type an array [y/n]:")):
                return 'n'
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription()
            assert not testobj.newTranslateMethodEntry()
            assert 'getTestString' not in testobj.stringJasonData['translateMethods']
            assert 'getTestInt' not in testobj.stringJasonData['translateMethods']

            expectedStr = ExpectedStrHelper.getExpectedTransDescHelp()
            expectedStr += ExpectedStrHelper.getExpectedNewTranslationEntry('Brief method description', testReturn, testParamlist, testTransString, ['en'])
            expectedStr += ExpectedStrHelper.getExpectedTransDescHelp()
            expectedStr += ExpectedStrHelper.getExpectedNewTranslationEntry('Brief method description2', testReturn2, testParamlist2, testTransString2, ['en'])
            assert output.getvalue() == expectedStr

    def test03AddTranslateMethodEntry(self):
        """!
        @brief Test addTranslateMethodEntry()
        """
        testobj = StringClassDescription()
        paramList = [ParamRetDict.buildParamDictWithMod("goo", "integer", "goo description", 0)]
        returnDict = ParamRetDict.buildReturnDictWithMod("string", "return description", 0)

        assert testobj.addTranslateMethodEntry('getTestInt', 'Brief getTestInt description',
                                                        paramList, returnDict, "en", "Test @goo@")

        assert 'getTestInt' in testobj.getTranlateMethodList()
        assert isinstance(testobj.stringJasonData['translateMethods']['getTestInt'], dict)
        assert testobj.stringJasonData['translateMethods']['getTestInt']['briefDesc'] == "Brief getTestInt description"
        assert len(testobj.stringJasonData['translateMethods']['getTestInt']['params']) == len(paramList)

        for index in range(0, len(paramList)):
            assert testobj.stringJasonData['translateMethods']['getTestInt']['params'][index] == paramList[index]

        assert testobj.stringJasonData['translateMethods']['getTestInt']['return'] == returnDict

        transDescList = TranslationTextParser.parseTranslateString("Test @goo@")
        assert len(testobj.stringJasonData['translateMethods']['getTestInt']['translateDesc']) == 1
        assert isinstance(testobj.stringJasonData['translateMethods']['getTestInt']['translateDesc']['en'], list)
        assert len(testobj.stringJasonData['translateMethods']['getTestInt']['translateDesc']['en']) == len(transDescList)

        for index in range(0, len(transDescList)):
            assert testobj.stringJasonData['translateMethods']['getTestInt']['translateDesc']["en"][index] == transDescList[index]

    def test04AddTranslateMethodEntryOverride(self):
        """!
        @brief Test addTranslateMethodEntry()
        """
        def testMockIn(prompt):
            return 'y'

        testobj = StringClassDescription()
        paramList = [ParamRetDict.buildParamDictWithMod("goo", "integer", "goo description", 0)]
        returnDict = ParamRetDict.buildReturnDictWithMod("string", "return description", 0)
        assert testobj.addTranslateMethodEntry('getTestInt', 'Brief getTestInt description', paramList, returnDict, "en", "Test @goo@")

        assert 'getTestInt' in testobj.getTranlateMethodList()
        assert isinstance(testobj.stringJasonData['translateMethods']['getTestInt'], dict)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            paramList = [ParamRetDict.buildParamDictWithMod("goo2", "unsigned", "goo2 description", 0)]
            returnDict = ParamRetDict.buildReturnDictWithMod("integer", "return int description", 0)
            assert testobj.addTranslateMethodEntry('getTestInt', 'Brief getTestInt override description',
                                                            paramList, returnDict, "en", "Test override @goo2@")

            assert 'getTestInt' in testobj.getTranlateMethodList()
            assert isinstance(testobj.stringJasonData['translateMethods']['getTestInt'], dict)
            assert testobj.stringJasonData['translateMethods']['getTestInt']['briefDesc'] == "Brief getTestInt override description"

            assert isinstance(testobj.stringJasonData['translateMethods']['getTestInt']['params'], list)
            assert len(testobj.stringJasonData['translateMethods']['getTestInt']['params']) == len(paramList)

            for index in range(0, len(paramList)):
                assert testobj.stringJasonData['translateMethods']['getTestInt']['params'][index] == paramList[index]

            assert isinstance(testobj.stringJasonData['translateMethods']['getTestInt']['return'], dict)
            assert testobj.stringJasonData['translateMethods']['getTestInt']['return'] == returnDict

            assert isinstance(testobj.stringJasonData['translateMethods']['getTestInt']['translateDesc'], dict)
            assert len(testobj.stringJasonData['translateMethods']['getTestInt']['translateDesc']) == 1

            transDescList = TranslationTextParser.parseTranslateString("Test override @goo2@")
            assert isinstance(testobj.stringJasonData['translateMethods']['getTestInt']['translateDesc']['en'], list)
            assert len(testobj.stringJasonData['translateMethods']['getTestInt']['translateDesc']['en']) == len(transDescList)
            for index in range(0, len(transDescList)):
                assert testobj.stringJasonData['translateMethods']['getTestInt']['translateDesc']["en"][index] == transDescList[index]

    def test05AddTranslateMethodEntryNoOverride(self):
        """!
        @brief Test addTranslateMethodEntry(), no overwrite
        """
        def testMockIn(prompt):
            return 'n'

        testobj = StringClassDescription()
        paramList = [ParamRetDict.buildParamDictWithMod("goo", "integer", "goo description", 0)]
        returnDict = ParamRetDict.buildReturnDictWithMod("string", "return description", 0)
        assert testobj.addTranslateMethodEntry('getTestInt', 'Brief getTestInt description', paramList, returnDict, "en", "Test @goo@")

        assert 'getTestInt' in testobj.getTranlateMethodList()
        assert isinstance(testobj.stringJasonData['translateMethods']['getTestInt'], dict)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            paramList2 = [ParamRetDict.buildParamDictWithMod("goo2", "unsigned", "goo2 description", 0)]
            returnDict2 = ParamRetDict.buildReturnDictWithMod("integer", "return int description", 0)
            assert not testobj.addTranslateMethodEntry('getTestInt', 'Brief getTestInt override description',
                                                             paramList2, returnDict2, "en", "Test override @goo2@")

            assert 'getTestInt' in testobj.getTranlateMethodList()
            assert isinstance(testobj.stringJasonData['translateMethods']['getTestInt'], dict)
            assert testobj.stringJasonData['translateMethods']['getTestInt']['briefDesc'] == "Brief getTestInt description"

            assert isinstance(testobj.stringJasonData['translateMethods']['getTestInt']['params'], list)
            assert len(testobj.stringJasonData['translateMethods']['getTestInt']['params']) == len(paramList)

            for index in range(0, len(paramList)):
                assert testobj.stringJasonData['translateMethods']['getTestInt']['params'][index] == paramList[index]

            assert isinstance(testobj.stringJasonData['translateMethods']['getTestInt']['return'], dict)
            assert testobj.stringJasonData['translateMethods']['getTestInt']['return'] == returnDict

            assert isinstance(testobj.stringJasonData['translateMethods']['getTestInt']['translateDesc'], dict)
            assert len(testobj.stringJasonData['translateMethods']['getTestInt']['translateDesc']) == 1

            transDescList = TranslationTextParser.parseTranslateString("Test @goo@")
            assert isinstance(testobj.stringJasonData['translateMethods']['getTestInt']['translateDesc']['en'], list)
            assert len(testobj.stringJasonData['translateMethods']['getTestInt']['translateDesc']['en']) == len(transDescList)
            for index in range(0, len(transDescList)):
                assert testobj.stringJasonData['translateMethods']['getTestInt']['translateDesc']["en"][index] == transDescList[index]

    def test06AddTranslateMethodEntryForceOverride(self):
        """!
        @brief Test addTranslateMethodEntry()
        """
        def testMockIn(prompt):
            return 'n'

        testobj = StringClassDescription()
        paramList = [ParamRetDict.buildParamDictWithMod("goo", "integer", "goo description", 0)]
        returnDict = ParamRetDict.buildReturnDictWithMod("string", "return description", 0)
        assert testobj.addTranslateMethodEntry('getTestInt', 'Brief getTestInt description', paramList, returnDict, "en", "Test @goo@")

        assert 'getTestInt' in testobj.getTranlateMethodList()
        assert isinstance(testobj.stringJasonData['translateMethods']['getTestInt'], dict)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            paramList = [ParamRetDict.buildParamDictWithMod("goo2", "unsigned", "goo2 description", 0)]
            returnDict = ParamRetDict.buildReturnDictWithMod("integer", "return int description", 0)
            assert testobj.addTranslateMethodEntry('getTestInt', 'Brief getTestInt override description',
                                                            paramList, returnDict, "en", "Test override @goo2@", True)

            assert 'getTestInt' in testobj.getTranlateMethodList()
            assert isinstance(testobj.stringJasonData['translateMethods']['getTestInt'], dict)
            assert testobj.stringJasonData['translateMethods']['getTestInt']['briefDesc'] == "Brief getTestInt override description"

            assert isinstance(testobj.stringJasonData['translateMethods']['getTestInt']['params'], list)
            assert len(testobj.stringJasonData['translateMethods']['getTestInt']['params']) == len(paramList)

            for index in range(0, len(paramList)):
                assert testobj.stringJasonData['translateMethods']['getTestInt']['params'][index] == paramList[index]

            assert isinstance(testobj.stringJasonData['translateMethods']['getTestInt']['return'], dict)
            assert testobj.stringJasonData['translateMethods']['getTestInt']['return'] == returnDict

            assert isinstance(testobj.stringJasonData['translateMethods']['getTestInt']['translateDesc'], dict)
            assert len(testobj.stringJasonData['translateMethods']['getTestInt']['translateDesc']) == 1

            transDescList = TranslationTextParser.parseTranslateString("Test override @goo2@")
            assert isinstance(testobj.stringJasonData['translateMethods']['getTestInt']['translateDesc']['en'], list)
            assert len(testobj.stringJasonData['translateMethods']['getTestInt']['translateDesc']['en']) == len(transDescList)
            for index in range(0, len(transDescList)):
                assert testobj.stringJasonData['translateMethods']['getTestInt']['translateDesc']["en"][index] == transDescList[index]

    def test07GetPropertyReturnData(self):
        """!
        @brief Test _getPropertyReturnData()
        """
        inputStr = (text for text in ["0", "1", "2", "3", "4", "5"])
        def testMockIn(prompt):
            return next(inputStr)

        testobj = StringClassDescription()
        propertyOptions = LanguageDescriptionList.getLanguagePropertyList()

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            for index in range(0,6):
                propertyId, methodName, returnType, returnDesc, isList = testobj._getPropertyReturnData()

                expectedReturnType, expectedReturnDesc, expectedIsList = LanguageDescriptionList.getLanguagePropertyReturnData(propertyOptions[index])
                expectedMethodName = LanguageDescriptionList.getLanguagePropertyMethodName(propertyOptions[index])

                assert propertyId == propertyOptions[index]
                assert methodName == expectedMethodName
                assert returnType == expectedReturnType
                assert returnDesc == expectedReturnDesc
                assert isList == expectedIsList

    def test08GetPropertyReturnDataBadInput(self):
        """!
        @brief Test _getPropertyReturnData()
        """
        inputStr = (text for text in ["8", "0"])
        def testMockIn(prompt):
            return next(inputStr)

        testobj = StringClassDescription()
        propertyOptions = LanguageDescriptionList.getLanguagePropertyList()

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            propertyId, methodName, returnType, returnDesc, isList = testobj._getPropertyReturnData()

            expectedReturnType, expectedReturnDesc, expectedIsList = LanguageDescriptionList.getLanguagePropertyReturnData(propertyOptions[0])
            expectedMethodName = LanguageDescriptionList.getLanguagePropertyMethodName(propertyOptions[0])

            assert propertyId == propertyOptions[0]
            assert methodName == expectedMethodName
            assert returnType == expectedReturnType
            assert returnDesc == expectedReturnDesc
            assert isList == expectedIsList

            expectedStr, maxIndex = ExpectedStrHelper.getExpectedOptionList()
            expectedStr += "Valid input values are 0 to "+str(maxIndex-1)+", try again\n"
            assert output.getvalue() == expectedStr

    def test09NewPropertyMethodEntry(self):
        """!
        @brief Test newPropertyMethodEntry()
        """
        inputStr = (text for text in ["0", "y", "y"])
        def testMockIn(prompt):
            return next(inputStr)

        testobj = StringClassDescription()
        propertyOptions = LanguageDescriptionList.getLanguagePropertyList()

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            assert testobj.newPropertyMethodEntry()

            returnType, returnDesc, isList = LanguageDescriptionList.getLanguagePropertyReturnData(propertyOptions[0])
            expectedReturn = ParamRetDict.buildReturnDict(returnType, returnDesc, isList)
            expectedMethodName = LanguageDescriptionList.getLanguagePropertyMethodName(propertyOptions[0])

            expectedStr, maxIndex = ExpectedStrHelper.getExpectedOptionList()
            expectedStr += ExpectedStrHelper.getExpectedNewPropertyStr(expectedMethodName, propertyOptions[0], expectedReturn)
            assert output.getvalue() == expectedStr

    def test10NewPropertyMethodEntryNo(self):
        """!
        @brief Test newPropertyMethodEntry()
        """
        inputStr = (text for text in ["0", "n", "1", "y", "y"])
        def testMockIn(prompt):
            return next(inputStr)

        testobj = StringClassDescription()
        propertyOptions = LanguageDescriptionList.getLanguagePropertyList()
        optionString, _ = ExpectedStrHelper.getExpectedOptionList()

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            assert testobj.newPropertyMethodEntry()

            returnType, returnDesc, isList = LanguageDescriptionList.getLanguagePropertyReturnData(propertyOptions[0])
            expectedReturn = ParamRetDict.buildReturnDict(returnType, returnDesc, isList)
            expectedMethodName = LanguageDescriptionList.getLanguagePropertyMethodName(propertyOptions[0])

            returnType1, returnDesc1, isList1 = LanguageDescriptionList.getLanguagePropertyReturnData(propertyOptions[1])
            expectedReturn1 = ParamRetDict.buildReturnDict(returnType1, returnDesc1, isList1)
            expectedMethodName1 = LanguageDescriptionList.getLanguagePropertyMethodName(propertyOptions[1])

            expectedStr = optionString
            expectedStr += ExpectedStrHelper.getExpectedNewPropertyStr(expectedMethodName, propertyOptions[0], expectedReturn)
            expectedStr += optionString
            expectedStr += ExpectedStrHelper.getExpectedNewPropertyStr(expectedMethodName1, propertyOptions[1], expectedReturn1)
            assert output.getvalue() == expectedStr

    def test11NewPropertyMethodEntryNoCommit(self):
        """!
        @brief Test newPropertyMethodEntry()
        """
        inputStr = (text for text in ["0", "y", "n"])
        def testMockIn(prompt):
            return next(inputStr)

        testobj = StringClassDescription()
        propertyOptions = LanguageDescriptionList.getLanguagePropertyList()
        optionString, _ = ExpectedStrHelper.getExpectedOptionList()

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            assert not testobj.newPropertyMethodEntry()

            returnType, returnDesc, isList = LanguageDescriptionList.getLanguagePropertyReturnData(propertyOptions[0])
            expectedReturn = ParamRetDict.buildReturnDict(returnType, returnDesc, isList)
            expectedMethodName = LanguageDescriptionList.getLanguagePropertyMethodName(propertyOptions[0])

            expectedStr = optionString
            expectedStr += ExpectedStrHelper.getExpectedNewPropertyStr(expectedMethodName, propertyOptions[0], expectedReturn)
            assert output.getvalue() == expectedStr

    def test12AddPropertyMethodEntry(self):
        """!
        @brief Test addPropertyMethodEntry()
        """
        inputStr = (text for text in ["y"])
        def testMockIn(prompt):
            return next(inputStr)

        testobj = StringClassDescription()
        propertyOptions = LanguageDescriptionList.getLanguagePropertyList()

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            assert testobj.addPropertyMethodEntry(propertyOptions[3])

            returnType, returnDesc, isList = LanguageDescriptionList.getLanguagePropertyReturnData(propertyOptions[3])
            expectedReturn = ParamRetDict.buildReturnDict(returnType, returnDesc, isList)
            expectedMethodName = LanguageDescriptionList.getLanguagePropertyMethodName(propertyOptions[3])

            assert expectedMethodName in testobj.getPropertyMethodList()
            assert isinstance(testobj.stringJasonData['propertyMethods'][expectedMethodName], dict)
            assert testobj.stringJasonData['propertyMethods'][expectedMethodName]['name'] == propertyOptions[3]
            assert testobj.stringJasonData['propertyMethods'][expectedMethodName]['briefDesc'] == "Get the "+returnDesc+" for this object"

            assert isinstance(testobj.stringJasonData['propertyMethods'][expectedMethodName]['params'], list)
            assert len(testobj.stringJasonData['propertyMethods'][expectedMethodName]['params']) == 0

            assert isinstance(testobj.stringJasonData['propertyMethods'][expectedMethodName]['return'], dict)
            assert testobj.stringJasonData['propertyMethods'][expectedMethodName]['return'] == expectedReturn

    def test13AddPropertyMethodEntryNoConfirm(self):
        """!
        @brief Test addPropertyMethodEntry(), confirm=no
        """
        inputStr = (text for text in ["n"])
        def testMockIn(prompt):
            return next(inputStr)

        testobj = StringClassDescription()
        propertyOptions = LanguageDescriptionList.getLanguagePropertyList()

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            assert not testobj.addPropertyMethodEntry(propertyOptions[3])
            expectedMethodName = LanguageDescriptionList.getLanguagePropertyMethodName(propertyOptions[3])
            assert expectedMethodName not in testobj.getPropertyMethodList()

    def test14AddTranslateMethodEntryBadtranslateString(self):
        """!
        @brief Test addTranslateMethodEntry(), bad translate string
        """
        def testMockIn(prompt):
            return 'n'

        testobj = StringClassDescription()
        paramList = [ParamRetDict.buildParamDictWithMod("goo", "integer", "goo description", 0)]
        returnDict = ParamRetDict.buildReturnDictWithMod("string", "return description", 0)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            assert not testobj.addTranslateMethodEntry('getTestInt',
                                                             'Brief getTestInt description',
                                                             paramList, returnDict,
                                                             "en", "Test @goo@ @foo@")

            assert 'getTestInt' not in testobj.getTranlateMethodList()
            assert output.getvalue() == "Error: Invalid translation string: Test @goo@ @foo@. paramCount= 2 matchCount= 1\n"
