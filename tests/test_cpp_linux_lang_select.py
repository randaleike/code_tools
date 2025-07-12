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
from code_tools_grocsoftware.cpp_gen.linux_lang_select import LinuxLangSelectFunctionGenerator

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

class TestClass01LinuxLangSelect:
    """!
    @brief Unit test for the BaseCppStringClassGenerator class
    """
    def test001ConstructorDefault(self):
        """!
        @brief Test constructor, default input
        """
        testObj = LinuxLangSelectFunctionGenerator(LanguageDescriptionList())

        assert testObj.baseClassName == "BaseClass"
        assert testObj.dynamicCompileSwitch == "DYNAMIC_INTERNATIONALIZATION"
        assert testObj.selectFunctionName == "getBaseClass_Linux"
        assert len(testObj.paramDictList) == 1
        assert testObj.paramDictList[0] == ParamRetDict.buildParamDict("langId",
                                                                                   "const char*",
                                                                                   "Current LANG value from the program environment")
        assert testObj.defOsString == "(defined(__linux__) || defined(__unix__))"
        assert isinstance(testObj.langJsonData, LanguageDescriptionList)
        assert isinstance(testObj.doxyCommentGen, CDoxyCommentGenerator)

    def test002ConstructorNonDefault(self):
        """!
        @brief Test constructor, with input
        """
        testObj = LinuxLangSelectFunctionGenerator(LanguageDescriptionList(), "George", "MIT_open", "TestBaseClass", "TEST_DYNAM_SWITCH")

        assert testObj.baseClassName == "TestBaseClass"
        assert testObj.dynamicCompileSwitch == "TEST_DYNAM_SWITCH"
        assert testObj.selectFunctionName == "getTestBaseClass_Linux"
        assert len(testObj.paramDictList) == 1
        assert testObj.paramDictList[0] == ParamRetDict.buildParamDict("langId",
                                                                                   "const char*",
                                                                                   "Current LANG value from the program environment")
        assert testObj.defOsString == "(defined(__linux__) || defined(__unix__))"
        assert isinstance(testObj.langJsonData, LanguageDescriptionList)
        assert isinstance(testObj.doxyCommentGen, CDoxyCommentGenerator)

    def test003GetFunctionName(self):
        """!
        @brief Test getFunctionName
        """
        testObj = LinuxLangSelectFunctionGenerator(LanguageDescriptionList())
        assert testObj.getFunctionName() == "getBaseClass_Linux"

    def test004GetOsDefine(self):
        """!
        @brief Test getOsDefine
        """
        testObj = LinuxLangSelectFunctionGenerator(LanguageDescriptionList())
        assert testObj.getOsDefine() == "(defined(__linux__) || defined(__unix__))"

    def test005GenFunctionDefine(self):
        """!
        @brief Test genFunctionDefine
        """
        cppGen = BaseCppStringClassGenerator()
        testObj = LinuxLangSelectFunctionGenerator(LanguageDescriptionList())
        expectedList = cppGen._defineFunctionWithDecorations(testObj.selectFunctionName,
                                                             "Determine the correct local language class from the input LANG environment setting",
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
        testObj = LinuxLangSelectFunctionGenerator(LanguageDescriptionList())
        assert testObj.genFunctionEnd() == "} // end of "+testObj.selectFunctionName+"()\n"

    def test007GenFunction(self):
        """!
        @brief Test genFunction
        """
        cppGen = BaseCppStringClassGenerator()
        langList = LanguageDescriptionList(testJsonList)
        testObj = LinuxLangSelectFunctionGenerator(langList)

        captureList = testObj.genFunction()

        assert len(captureList) == 41

        assert captureList[0] == "#if (defined(__linux__) || defined(__unix__))\n"
        assert captureList[1] == cppGen._genInclude("<cstdlib>")
        assert captureList[2] == cppGen._genInclude("<regex>")
        assert captureList[3] == "\n"

        expectedList = cppGen._defineFunctionWithDecorations(testObj.selectFunctionName,
                                                             "Determine the correct local language class from the input LANG environment setting",
                                                             testObj.paramDictList,
                                                             testObj.baseIntfRetPtrDict)
        expectedList.append("{\n")
        for index, expectedText in enumerate(expectedList):
            assert captureList[index+4] == expectedText

        paramName = ParamRetDict.getParamName(testObj.paramDictList[0])
        assert captureList[13] == "    // Check for valid input\n"
        assert captureList[14] == "    if (nullptr != "+paramName+")\n"
        assert captureList[15] == "    {\n"
        assert captureList[16] == "        // Break the string into its components\n"
        assert captureList[17] == "        std::cmatch searchMatch;\n"
        assert captureList[18] == "        std::regex searchRegex(\"^([a-z]{2})_([A-Z]{2})\\\\.(UTF-[0-9]{1,2})\");\n"
        assert captureList[19] == "        bool matched = std::regex_match("+paramName+", searchMatch, searchRegex);\n"
        assert captureList[20] == "\n"
        assert captureList[21] == "        // Determine the language\n"

        first = True
        for index, langName in enumerate(langList.getLanguageList()):
            langCode, regionList = langList.getLanguageLANGData(langName)
            if first:
                ifLine = "if (matched && "
                first = False
            else:
                ifLine = "else if (matched && "
            ifLine += "(searchMatch[1].str() == \""
            ifLine += langCode
            ifLine += "\"))\n"

            listOffset = 22 + (index * 4)
            assert captureList[listOffset] == "        "+ifLine
            assert captureList[listOffset+1] == "        {\n"
            assert captureList[listOffset+2] == "            "+cppGen._genMakePtrReturnStatement(langName)
            assert captureList[listOffset+3] == "        }\n"

        assert captureList[30] == "        else //unknown language code, use default language\n"
        assert captureList[31] == "        {\n"
        defaultLang, defaultIsoCode = langList.getDefaultData()
        assert captureList[32] == "            "+cppGen._genMakePtrReturnStatement(defaultLang)
        assert captureList[33] == "        }\n"
        assert captureList[34] == "    }\n"
        assert captureList[35] == "    else // null pointer input, use default language\n"
        assert captureList[36] == "    {\n"
        assert captureList[37] == "        "+cppGen._genMakePtrReturnStatement(defaultLang)
        assert captureList[38] == "    } // end of if(nullptr != "+paramName+")\n"
        assert captureList[39] == "} // end of "+testObj.selectFunctionName+"()\n"
        assert captureList[40] == "#endif // "+testObj.defOsString+"\n"

    def test008GenReturnFunctionCall(self):
        """!
        @brief Test genReturnFunctionCall
        """
        testObj = LinuxLangSelectFunctionGenerator(LanguageDescriptionList())
        paramType = ParamRetDict.getParamType(testObj.paramDictList[0])

        strList = testObj.genReturnFunctionCall()
        assert len(strList) == 2
        assert strList[0] == "    "+paramType+" langId = getenv(\"LANG\");\n"
        assert strList[1] == "    return "+testObj.selectFunctionName+"(langId);\n"

    def test009GenUnitTestTest(self):
        """!
        @brief Test _genUnitTestTest
        """
        testObj = LinuxLangSelectFunctionGenerator(LanguageDescriptionList())

        doxyGen = CDoxyCommentGenerator()
        doxyDesc = "Test "+testObj.selectFunctionName+" envLang selection case"
        doxyBody = doxyGen.genDoxyMethodComment(doxyDesc, [])

        strList = testObj._genUnitTestTest("Foo", "envLang", "en", "getIsoCode")
        assert len(strList) == 11
        assert strList[0] == doxyBody[0]
        assert strList[1] == doxyBody[1]
        assert strList[2] == doxyBody[2]
        assert strList[3] == doxyBody[3]

        assert strList[4] == "TEST(LinuxSelectFunction, Foo)\n"
        assert strList[5] == "{\n"
        assert strList[6] == "    // Generate the test language string object\n"
        assert strList[7] == "    std::string testLangCode = \"envLang\";\n"
        assert strList[8] == "    "+testObj.baseIntfRetPtrType+" testVar = "+testObj.selectFunctionName+"(testLangCode.c_str());\n"
        assert strList[9] == "    EXPECT_STREQ(\"en\", testVar->getIsoCode().c_str());\n"
        assert strList[10] == "}\n"

    def test010GenExternDefinition(self):
        """!
        @brief Test genExternDefinition
        """
        testObj = LinuxLangSelectFunctionGenerator(LanguageDescriptionList())
        assert testObj.genExternDefinition() == getExpectedExtern(testObj.paramDictList, testObj.baseIntfRetPtrType, testObj.selectFunctionName)

    def test011GenUnitTest(self):
        """!
        @brief Test genUnitTest
        """
        langList = LanguageDescriptionList(testJsonList)
        testObj = LinuxLangSelectFunctionGenerator(langList)
        textList = testObj.genUnitTest("getIsoCode")

        # Test starting block
        assert len(textList) == 425
        assert textList[0] == "#if "+testObj.defOsString+"\n"
        assert textList[1] == "\n"
        assert textList[2] == "#include <cstdlib>\n"
        assert textList[3] == testObj.genExternDefinition()
        assert textList[4] == "\n"

        # Match each test function
        textIndex = 5
        for langName in langList.getLanguageList():
            langCode, regionList = langList.getLanguageLANGData(langName)
            isoCode = langList.getLanguageIsoCodeData(langName)
            for region in regionList:
                linuxEnvString = langCode+"_"+region+".UTF-8"
                testName = langName.capitalize()+"_"+region+"_Selection"
                expectedTestText = testObj._genUnitTestTest(testName, linuxEnvString, isoCode, "getIsoCode")

                for index, expectedLine in enumerate(expectedTestText):
                    assert textList[textIndex+index] == expectedLine

                textIndex += len(expectedTestText)
                assert textList[textIndex] == "\n"
                textIndex += 1

            # Match unknown region test
            unknownRegionTestName =langName.capitalize()+"_unknownRegion_Selection"
            unknownRegionEnv = langCode+"_XX.UTF-8"
            expectedTestText = testObj._genUnitTestTest(unknownRegionTestName, unknownRegionEnv, isoCode, "getIsoCode")
            for index, expectedLine in enumerate(expectedTestText):
                assert textList[textIndex+index] == expectedLine

            textIndex += len(expectedTestText)
            assert textList[textIndex] == "\n"
            textIndex += 1

        # Match default test
        defaultLang, defaultIsoCode = langList.getDefaultData()
        unknownLangBody = testObj._genUnitTestTest("UnknownLanguageDefaultSelection", "xx_XX.UTF-8", defaultIsoCode, "getIsoCode")
        for index, expectedLine in enumerate(unknownLangBody):
            assert textList[textIndex+index] == expectedLine

        textIndex += len(expectedTestText)

        # Match end
        assert textList[424] == "#endif // "+testObj.defOsString+"\n"
        assert textIndex == 424

    def test012GenUnitTestFunctionCall(self):
        """!
        @brief Test genUnitTestFunctionCall
        """
        testObj = LinuxLangSelectFunctionGenerator(LanguageDescriptionList())
        textList = testObj.genUnitTestFunctionCall("checkVar")

        paramType = ParamRetDict.getParamType(testObj.paramDictList[0])

        assert len(textList) == 2
        assert textList[0] == "    "+paramType+" langId = getenv(\"LANG\");\n"
        assert textList[1] == "    "+testObj.baseIntfRetPtrType+" checkVar = "+testObj.selectFunctionName+"(langId);\n"

    def test013GetUnittestExternInclude(self):
        """!
        @brief Test getUnittestExternInclude
        """
        testObj = LinuxLangSelectFunctionGenerator(LanguageDescriptionList())
        textList = testObj.getUnittestExternInclude()

        assert len(textList) == 4
        assert textList[0] == "#if "+testObj.defOsString+"\n"
        assert textList[1] == "#include <cstdlib>\n"
        assert textList[2] == getExpectedExtern(testObj.paramDictList, testObj.baseIntfRetPtrType, testObj.selectFunctionName)
        assert textList[3] == "#endif // "+testObj.defOsString+"\n"

    def test014GetUnittestFileName(self):
        """!
        @brief Test getUnittestFileName
        """
        testObj = LinuxLangSelectFunctionGenerator(LanguageDescriptionList())
        cppName, testName = testObj.getUnittestFileName()
        assert cppName == "LocalLanguageSelect_Linux_test.cpp"
        assert testName == "LocalLanguageSelect_Linux_test"
