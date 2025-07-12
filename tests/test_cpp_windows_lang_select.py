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
from unittest.mock import mock_open, patch

from code_tools_grocsoftware.base.param_return_tools import ParamRetDict
from code_tools_grocsoftware.base.doxygen_gen_tools import CDoxyCommentGenerator
from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList
from code_tools_grocsoftware.cpp_gen.string_class_tools import BaseCppStringClassGenerator
from code_tools_grocsoftware.cpp_gen.windows_lang_select import WindowsLangSelectFunctionGenerator

from tests.dir_init import TESTFILEPATH
testJsonList = os.path.join(TESTFILEPATH,"teststringlanglist.json")

def getExpectedExtern(paramDictList:list, intfRetPtrType:str, selectFunctionName:str)->str:
    paramPrefix = ""
    paramStr = ""
    for paramDict in paramDictList:
        paramType = ParamRetDict.getParamType(paramDict)
        paramName = ParamRetDict.getParamName(paramDict)
        paramStr += paramPrefix
        paramStr += paramType
        paramStr += " "
        paramStr += paramName
        paramPrefix = ", "

    expectedStr = "extern "+intfRetPtrType+" "+selectFunctionName+"("+paramStr+");\n"
    return expectedStr

class TestClass01WindowsLangSelect:
    """!
    @brief Unit test for the BaseCppStringClassGenerator class
    """
    def test001ConstructorDefault(self):
        """!
        @brief Test constructor, default input
        """
        testObj = WindowsLangSelectFunctionGenerator(LanguageDescriptionList())

        assert testObj.baseClassName == "BaseClass"
        assert testObj.dynamicCompileSwitch == "DYNAMIC_INTERNATIONALIZATION"
        assert testObj.selectFunctionName == "getBaseClass_Windows"
        assert len(testObj.paramDictList) == 1
        assert testObj.paramDictList[0] == ParamRetDict.buildParamDict("langId",
                                                                       "LANGID",
                                                                       "Return value from GetUserDefaultUILanguage() call")
        assert testObj.defOsString == "(defined(_WIN64) || defined(_WIN32))"
        assert isinstance(testObj.langJsonData, LanguageDescriptionList)
        assert isinstance(testObj.doxyCommentGen, CDoxyCommentGenerator)

    def test002ConstructorNonDefault(self):
        """!
        @brief Test constructor, with input
        """
        testObj = WindowsLangSelectFunctionGenerator(LanguageDescriptionList(), "George", "MIT_open", "TestBaseClass", "TEST_DYNAM_SWITCH")

        assert testObj.baseClassName == "TestBaseClass"
        assert testObj.dynamicCompileSwitch == "TEST_DYNAM_SWITCH"
        assert testObj.selectFunctionName == "getTestBaseClass_Windows"
        assert len(testObj.paramDictList) == 1
        assert testObj.paramDictList[0] == ParamRetDict.buildParamDict("langId",
                                                                       "LANGID",
                                                                       "Return value from GetUserDefaultUILanguage() call")
        assert testObj.defOsString == "(defined(_WIN64) || defined(_WIN32))"
        assert isinstance(testObj.langJsonData, LanguageDescriptionList)
        assert isinstance(testObj.doxyCommentGen, CDoxyCommentGenerator)

    def test003GetFunctionName(self):
        """!
        @brief Test getFunctionName
        """
        testObj = WindowsLangSelectFunctionGenerator(LanguageDescriptionList())
        assert testObj.getFunctionName() == "getBaseClass_Windows"

    def test004GetOsDefine(self):
        """!
        @brief Test getOsDefine
        """
        testObj = WindowsLangSelectFunctionGenerator(LanguageDescriptionList())
        assert testObj.getOsDefine() == "(defined(_WIN64) || defined(_WIN32))"

    def test005GenFunctionDefine(self):
        """!
        @brief Test genFunctionDefine
        """
        cppGen = BaseCppStringClassGenerator()
        testObj = WindowsLangSelectFunctionGenerator(LanguageDescriptionList())
        expectedList = cppGen._defineFunctionWithDecorations(testObj.selectFunctionName,
                                                             "Determine the correct local language class from the input LANGID value",
                                                             testObj.paramDictList,
                                                             testObj.baseIntfRetPtrDict)
        expectedList.append("{\n")

        testList = testObj.genFunctionDefine()
        assert len(testList) == len(expectedList)
        for index, expectedText in enumerate(expectedList):
            assert testList[index] == expectedText

    def test006GenFunctionEnd(self):
        """!
        @brief Test genFunctionEnd
        """
        testObj = WindowsLangSelectFunctionGenerator(LanguageDescriptionList())
        assert testObj.genFunctionEnd() == "} // end of "+testObj.selectFunctionName+"()\n"

    def test007GenFunction(self):
        """!
        @brief Test genFunction
        """
        cppGen = BaseCppStringClassGenerator()
        langList = LanguageDescriptionList(testJsonList)
        testObj = WindowsLangSelectFunctionGenerator(langList)

        captureList = testObj.genFunction()

        assert len(captureList) == 25

        assert captureList[0] == "#if "+testObj.defOsString+"\n"
        assert captureList[1] == cppGen._genInclude("<windows.h>")
        assert captureList[2] == "\n"

        expectedList = cppGen._defineFunctionWithDecorations(testObj.selectFunctionName,
                                                             "Determine the correct local language class from the input LANGID value",
                                                             testObj.paramDictList,
                                                             testObj.baseIntfRetPtrDict)
        expectedList.append("{\n")
        for index, expectedText in enumerate(expectedList):
            assert captureList[index+3] == expectedText

        captureIndex = 3 + len(expectedList)
        paramName = ParamRetDict.getParamName(testObj.paramDictList[0])
        assert captureList[captureIndex] == "    switch("+paramName+" & 0x0FF)\n"
        assert captureList[captureIndex+1] == "    {\n"

        captureIndex += 2
        for langName in langList.getLanguageList():
            langCodes, langRegionList = langList.getLanguageLANGIDData(langName)
            for id in langCodes:
                assert captureList[captureIndex] == "        case "+hex(id)+":\n"
                captureIndex += 1

            assert captureList[captureIndex] == "            "+cppGen._genMakePtrReturnStatement(langName)
            assert captureList[captureIndex+1] == "            break;\n"
            captureIndex += 2


        assert captureList[captureIndex] == "        default:\n"
        defaultLang, defaultIsoCode = langList.getDefaultData()
        assert captureList[captureIndex+1] == "            "+cppGen._genMakePtrReturnStatement(defaultLang)
        assert captureList[captureIndex+2] == "    }\n"
        assert captureList[captureIndex+3] == "} // end of "+testObj.selectFunctionName+"()\n"
        assert captureList[captureIndex+4] == "#endif // "+testObj.defOsString+"\n"

    def test008GenReturnFunctionCall(self):
        """!
        @brief Test genReturnFunctionCall
        """
        testObj = WindowsLangSelectFunctionGenerator(LanguageDescriptionList())
        paramType = ParamRetDict.getParamType(testObj.paramDictList[0])

        strList = testObj.genReturnFunctionCall()
        assert len(strList) == 2
        assert strList[0] == "    "+paramType+" langId = GetUserDefaultUILanguage();\n"
        assert strList[1] == "    return "+testObj.selectFunctionName+"(langId);\n"

    def test009GenUnitTestTest(self):
        """!
        @brief Test _genUnitTestTest
        """
        testObj = WindowsLangSelectFunctionGenerator(LanguageDescriptionList())

        doxyGen = CDoxyCommentGenerator()
        doxyDesc = "Test "+testObj.selectFunctionName+" 11 selection case"
        doxyBody = doxyGen.genDoxyMethodComment(doxyDesc, [])

        strList = testObj._genUnitTestTest("Foo", 11, "en", "getIsoCode")
        assert len(strList) == 10
        assert strList[0] == doxyBody[0]
        assert strList[1] == doxyBody[1]
        assert strList[2] == doxyBody[2]
        assert strList[3] == doxyBody[3]

        assert strList[4] == "TEST(WindowsSelectFunction, Foo)\n"
        assert strList[5] == "{\n"
        assert strList[6] == "    // Generate the test language string object\n"
        assert strList[7] == "    "+testObj.baseIntfRetPtrType+" testVar = "+testObj.selectFunctionName+"(11);\n"
        assert strList[8] == "    EXPECT_STREQ(\"en\", testVar->getIsoCode().c_str());\n"
        assert strList[9] == "}\n"

    def test010GenExternDefinition(self):
        """!
        @brief Test genExternDefinition
        """
        testObj = WindowsLangSelectFunctionGenerator(LanguageDescriptionList())
        assert testObj.genExternDefinition() == getExpectedExtern(testObj.paramDictList, testObj.baseIntfRetPtrType, testObj.selectFunctionName)

    def test011GenUnitTest(self):
        """!
        @brief Test genUnitTest
        """
        langList = LanguageDescriptionList(testJsonList)
        testObj = WindowsLangSelectFunctionGenerator(langList)
        textList = testObj.genUnitTest("getIsoCode")

        # Test starting block
        assert len(textList) == 423
        assert textList[0] == "#if "+testObj.defOsString+"\n"
        assert textList[1] == "\n"
        assert textList[2] == "#include <windows.h>\n"
        assert textList[3] == testObj.genExternDefinition()
        assert textList[4] == "\n"

        # Match each test function
        textIndex = 5
        for langName in langList.getLanguageList():
            langCodes, regionList = langList.getLanguageLANGIDData(langName)
            isoCode = langList.getLanguageIsoCodeData(langName)
            for region in regionList:
                testName = langName.capitalize()+"_"+str(region)+"_Selection"
                expectedTestText = testObj._genUnitTestTest(testName, region, isoCode, "getIsoCode")

                for index, expectedLine in enumerate(expectedTestText):
                    assert textList[textIndex+index] == expectedLine

                textIndex += len(expectedTestText)
                assert textList[textIndex] == "\n"
                textIndex += 1

            # Match unknown regions 00 test
            for langCode in langCodes:
                unknownRegionTestName = langName.capitalize()+"_unknownRegion_00"+str(langCode)+"_Selection"
                expectedTestText = testObj._genUnitTestTest(unknownRegionTestName, langCode, isoCode, "getIsoCode")
                for index, expectedLine in enumerate(expectedTestText):
                    assert textList[textIndex+index] == expectedLine

                textIndex += len(expectedTestText)
                assert textList[textIndex] == "\n"
                textIndex += 1

            # Match unknown regions FFxx test
            for langCode in langCodes:
                unknownRegionTestName = langName.capitalize()+"_unknownRegion_FF"+str(langCode)+"_Selection"
                expectedTestText = testObj._genUnitTestTest(unknownRegionTestName, 0xFF00+langCode, isoCode, "getIsoCode")

                for index, expectedLine in enumerate(expectedTestText):
                    assert textList[textIndex+index] == expectedLine

                textIndex += len(expectedTestText)
                assert textList[textIndex] == "\n"
                textIndex += 1

        # Match default test
        defaultLang, defaultIsoCode = langList.getDefaultData()
        unknownLangBody = testObj._genUnitTestTest("UnknownLanguageDefaultSelection", 0, defaultIsoCode, "getIsoCode")
        for index, expectedLine in enumerate(unknownLangBody):
            assert textList[textIndex+index] == expectedLine

        textIndex += len(expectedTestText)

        # Match end
        assert textList[422] == "#endif // "+testObj.defOsString+"\n"
        assert textIndex == 422

    def test012GenUnitTestFunctionCall(self):
        """!
        @brief Test genUnitTestFunctionCall
        """
        testObj = WindowsLangSelectFunctionGenerator(LanguageDescriptionList())
        textList = testObj.genUnitTestFunctionCall("checkVar")

        paramType = ParamRetDict.getParamType(testObj.paramDictList[0])

        assert len(textList) == 2
        assert textList[0] == "    "+paramType+" langId = GetUserDefaultUILanguage();\n"
        assert textList[1] == "    "+testObj.baseIntfRetPtrType+" checkVar = "+testObj.selectFunctionName+"(langId);\n"

    def test013GetUnittestExternInclude(self):
        """!
        @brief Test getUnittestExternInclude
        """
        testObj = WindowsLangSelectFunctionGenerator(LanguageDescriptionList())
        textList = testObj.getUnittestExternInclude()

        assert len(textList) == 4
        assert textList[0] == "#if "+testObj.defOsString+"\n"
        assert textList[1] == "#include <windows.h>\n"
        assert textList[2] == getExpectedExtern(testObj.paramDictList, testObj.baseIntfRetPtrType, testObj.selectFunctionName)
        assert textList[3] == "#endif // "+testObj.defOsString+"\n"

    def test014GetUnittestFileName(self):
        """!
        @brief Test getUnittestFileName
        """
        testObj = WindowsLangSelectFunctionGenerator(LanguageDescriptionList())
        cppName, testName = testObj.getUnittestFileName()
        assert cppName == "LocalLanguageSelect_Windows_test.cpp"
        assert testName == "LocalLanguageSelect_Windows_test"
