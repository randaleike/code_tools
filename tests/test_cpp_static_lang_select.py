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
from code_tools_grocsoftware.cpp_gen.static_lang_select import StaticLangSelectFunctionGenerator

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

class TestClass01StaticLangSelect:
    """!
    @brief Unit test for the BaseCppStringClassGenerator class
    """
    def test001ConstructorDefault(self):
        """!
        @brief Test constructor, default input
        """
        testObj = StaticLangSelectFunctionGenerator(LanguageDescriptionList())

        assert testObj.baseClassName == "BaseClass"
        assert testObj.dynamicCompileSwitch == "DYNAMIC_INTERNATIONALIZATION"
        assert testObj.selectFunctionName == "getBaseClass_Static"
        assert testObj.defStaticString == "!defined(DYNAMIC_INTERNATIONALIZATION)"
        assert isinstance(testObj.langJsonData, LanguageDescriptionList)
        assert isinstance(testObj.doxyCommentGen, CDoxyCommentGenerator)

    def test002ConstructorNonDefault(self):
        """!
        @brief Test constructor, with input
        """
        testObj = StaticLangSelectFunctionGenerator(LanguageDescriptionList(), "George", "MIT_open", "TestBaseClass", "TEST_DYNAM_SWITCH")

        assert testObj.baseClassName == "TestBaseClass"
        assert testObj.dynamicCompileSwitch == "TEST_DYNAM_SWITCH"
        assert testObj.selectFunctionName == "getTestBaseClass_Static"
        assert testObj.defStaticString == "!defined(TEST_DYNAM_SWITCH)"
        assert isinstance(testObj.langJsonData, LanguageDescriptionList)
        assert isinstance(testObj.doxyCommentGen, CDoxyCommentGenerator)

    def test003GetFunctionName(self):
        """!
        @brief Test getFunctionName
        """
        testObj = StaticLangSelectFunctionGenerator(LanguageDescriptionList())
        assert testObj.getFunctionName() == "getBaseClass_Static"

    def test004GetOsDefine(self):
        """!
        @brief Test getOsDefine
        """
        testObj = StaticLangSelectFunctionGenerator(LanguageDescriptionList())
        assert testObj.getOsDefine() == "!defined(DYNAMIC_INTERNATIONALIZATION)"

    def test005GetOsDynamicDefine(self):
        """!
        @brief Test getOsDynamicDefine
        """
        testObj = StaticLangSelectFunctionGenerator(LanguageDescriptionList())
        assert testObj.getOsDynamicDefine() == "!defined(DYNAMIC_INTERNATIONALIZATION)"

    def test006GenFunctionDefine(self):
        """!
        @brief Test genFunctionDefine
        """
        cppGen = BaseCppStringClassGenerator()
        testObj = StaticLangSelectFunctionGenerator(LanguageDescriptionList())
        expectedList = cppGen._defineFunctionWithDecorations(testObj.selectFunctionName,
                                                             "Determine the correct local language class from the compile switch setting",
                                                             [],
                                                             testObj.baseIntfRetPtrDict)
        expectedList.append("{\n")

        testList = testObj.genFunctionDefine()
        assert len(testList) == len(expectedList)
        for index, expectedText in enumerate(expectedList):
            assert testList[index] == expectedText

    def test007GenFunctionEnd(self):
        """!
        @brief Test genFunctionEnd
        """
        testObj = StaticLangSelectFunctionGenerator(LanguageDescriptionList())
        assert testObj.genFunctionEnd() == "} // end of "+testObj.selectFunctionName+"()\n"

    def test008GenFunction(self):
        """!
        @brief Test genFunction
        """
        cppGen = BaseCppStringClassGenerator()
        langList = LanguageDescriptionList(testJsonList)
        testObj = StaticLangSelectFunctionGenerator(langList)

        captureList = testObj.genFunction()

        assert len(captureList) == 17
        assert captureList[0] == "#if !defined(DYNAMIC_INTERNATIONALIZATION)\n"

        expectedList = cppGen._defineFunctionWithDecorations(testObj.selectFunctionName,
                                                             "Determine the correct local language class from the compile switch setting",
                                                             [],
                                                             testObj.baseIntfRetPtrDict)
        expectedList.append("{\n")
        for index, expectedText in enumerate(expectedList):
            assert captureList[index+1] == expectedText

        listIndex = len(expectedList) + 1
        first = True
        for index, langName in enumerate(langList.getLanguageList()):
            langCode, regionList = langList.getLanguageLANGData(langName)
            if first:
                ifLine = "#if "
                first = False
            else:
                ifLine = "#elif "
            ifLine += "defined("+langList.getLanguageCompileSwitchData(langName)+")\n"

            assert captureList[listIndex] == "  "+ifLine
            assert captureList[listIndex+1] == "    "+cppGen._genMakePtrReturnStatement(langName)
            listIndex += 2

        assert captureList[listIndex] == "  #else //undefined language compile switch, use default\n"
        assert captureList[listIndex+1] == "    #error one of the language compile switches must be defined\n"
        assert captureList[listIndex+2] == "  #endif //end of language #if/#elifcompile switch chain\n"
        assert captureList[listIndex+3] == "} // end of "+testObj.selectFunctionName+"()\n"
        assert captureList[listIndex+4] == "#endif // "+testObj.defStaticString+"\n"

    def test009GenReturnFunctionCall(self):
        """!
        @brief Test genReturnFunctionCall
        """
        testObj = StaticLangSelectFunctionGenerator(LanguageDescriptionList())
        strList = testObj.genReturnFunctionCall()
        assert len(strList) == 1
        assert strList[0] == "    return "+testObj.selectFunctionName+"();\n"

    def test010GenExternDefinition(self):
        """!
        @brief Test genExternDefinition
        """
        testObj = StaticLangSelectFunctionGenerator(LanguageDescriptionList())
        assert testObj.genExternDefinition() == "extern "+testObj.baseIntfRetPtrType+" "+testObj.selectFunctionName+"();\n"

    def test011GenUnitTest(self):
        """!
        @brief Test genUnitTest
        """
        langList = LanguageDescriptionList(testJsonList)
        testObj = StaticLangSelectFunctionGenerator(langList)
        textList = testObj.genUnitTest("getIsoCode")

        # Test starting block
        assert len(textList) == 26
        assert textList[0] == "#if "+testObj.defStaticString+"\n"
        assert textList[1] == testObj.genExternDefinition()
        assert textList[2] == "\n"

        doxyGen = CDoxyCommentGenerator()
        doxyDesc = "Test "+testObj.selectFunctionName+" selection case"
        doxyBody = doxyGen.genDoxyMethodComment(doxyDesc, [])

        assert textList[3] == doxyBody[0]
        assert textList[4] == doxyBody[1]
        assert textList[5] == doxyBody[2]
        assert textList[6] == doxyBody[3]

        # Match each test function
        textIndex = 7
        for langName in langList.getLanguageList():
            isoCode = langList.getLanguageIsoCodeData(langName)
            switch = langList.getLanguageCompileSwitchData(langName)

            # Match language
            expectedBody = ["#if defined("+switch+")\n"]
            expectedBody.append("TEST(StaticSelectFunction"+langName.capitalize()+", CompileSwitchedValue)\n")
            expectedBody.append("{\n")
            expectedBody.append("    // Generate the test language string object\n")
            expectedBody.append("    "+testObj.baseIntfRetPtrType+" testVar = "+testObj.selectFunctionName+"();\n")
            expectedBody.append("    EXPECT_STREQ(\""+isoCode+"\", testVar->getIsoCode().c_str());\n")

            # Complete the function
            expectedBody.append("}\n")
            expectedBody.append("#endif //end of #if defined("+switch+")\n")
            expectedBody.append("\n") # whitespace for readability

            assert textList[textIndex+0] == expectedBody[0]
            assert textList[textIndex+1] == expectedBody[1]
            assert textList[textIndex+2] == expectedBody[2]
            assert textList[textIndex+3] == expectedBody[3]
            assert textList[textIndex+4] == expectedBody[4]
            assert textList[textIndex+5] == expectedBody[5]
            assert textList[textIndex+6] == expectedBody[6]
            assert textList[textIndex+7] == expectedBody[7]
            assert textList[textIndex+8] == expectedBody[8]
            textIndex += 9

        # Match end
        assert textList[textIndex] == "#endif // "+testObj.defStaticString+"\n"
        assert textIndex == 25

    def test012GenUnitTestFunctionCall(self):
        """!
        @brief Test genUnitTestFunctionCall
        """
        testObj = StaticLangSelectFunctionGenerator(LanguageDescriptionList())
        textList = testObj.genUnitTestFunctionCall("checkVar")

        assert len(textList) == 1
        assert textList[0] == "    "+testObj.baseIntfRetPtrType+" checkVar = "+testObj.selectFunctionName+"();\n"

    def test013GetUnittestExternInclude(self):
        """!
        @brief Test getUnittestExternInclude
        """
        testObj = StaticLangSelectFunctionGenerator(LanguageDescriptionList())
        textList = testObj.getUnittestExternInclude()

        assert len(textList) == 3
        assert textList[0] == "#if "+testObj.defStaticString+"\n"
        assert textList[1] == getExpectedExtern([], testObj.baseIntfRetPtrType, testObj.selectFunctionName)
        assert textList[2] == "#endif // "+testObj.defStaticString+"\n"

    def test014GetUnittestFileName(self):
        """!
        @brief Test getUnittestFileName
        """
        testObj = StaticLangSelectFunctionGenerator(LanguageDescriptionList())
        cppName, testName = testObj.getUnittestFileName()
        assert cppName == "LocalLanguageSelect_Static_test.cpp"
        assert testName == "LocalLanguageSelect_Static_test"
