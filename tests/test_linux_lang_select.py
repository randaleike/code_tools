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

from dir_init import pathincsetup
pathincsetup()
from dir_init import TESTFILEPATH

from code_tools_grocsoftware.base.param_return_tools import ParamRetDict
from code_tools_grocsoftware.base.doxygen_gen_tools import CDoxyCommentGenerator
from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList
from code_tools_grocsoftware.cpp_gen.string_class_tools import BaseCppStringClassGenerator
from code_tools_grocsoftware.cpp_gen.linux_lang_select import LinuxLangSelectFunctionGenerator

testJsonList = os.path.join(TESTFILEPATH,"teststringlanglist.json")

class fileCapture(object):
    """!
    Dummy file writelines capture class
    """
    def __init__(self):
        self.captureList = []
        self.callCount = 0
        self.lineCount = 0

    def writelines(self, writeList:list):
        """!
        @brief Capture the data
        @param writeList {list} - String list to capture
        """
        self.callCount += 1
        self.lineCount += len(writeList)
        self.captureList.extend(writeList)

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
        dummy = fileCapture()
        langList = LanguageDescriptionList(testJsonList)
        testObj = LinuxLangSelectFunctionGenerator(langList)

        testObj.genFunction(dummy)

        assert dummy.callCount == 1
        assert dummy.lineCount == 41

        assert dummy.captureList[0] == "#if (defined(__linux__) || defined(__unix__))\n"
        assert dummy.captureList[1] == cppGen._genInclude("<cstdlib>")
        assert dummy.captureList[2] == cppGen._genInclude("<regex>")
        assert dummy.captureList[3] == "\n"

        expectedList = cppGen._defineFunctionWithDecorations(testObj.selectFunctionName,
                                                             "Determine the correct local language class from the input LANG environment setting",
                                                             testObj.paramDictList,
                                                             testObj.baseIntfRetPtrDict)
        expectedList.append("{\n")
        for index, expectedText in enumerate(expectedList):
            assert dummy.captureList[index+4] == expectedText

        paramName = ParamRetDict.getParamName(testObj.paramDictList[0])
        assert dummy.captureList[13] == "    // Check for valid input\n"
        assert dummy.captureList[14] == "    if (nullptr != "+paramName+")\n"
        assert dummy.captureList[15] == "    {\n"
        assert dummy.captureList[16] == "        // Break the string into its components\n"
        assert dummy.captureList[17] == "        std::cmatch searchMatch;\n"
        assert dummy.captureList[18] == "        std::regex searchRegex(\"^([a-z]{2})_([A-Z]{2})\\\\.(UTF-[0-9]{1,2})\");\n"
        assert dummy.captureList[19] == "        bool matched = std::regex_match("+paramName+", searchMatch, searchRegex);\n"
        assert dummy.captureList[20] == "\n"
        assert dummy.captureList[21] == "        // Determine the language\n"

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
            assert dummy.captureList[listOffset] == "        "+ifLine
            assert dummy.captureList[listOffset+1] == "        {\n"
            assert dummy.captureList[listOffset+2] == "            "+cppGen._genMakePtrReturnStatement(langName)
            assert dummy.captureList[listOffset+3] == "        }\n"

        assert dummy.captureList[30] == "        else //unknown language code, use default language\n"
        assert dummy.captureList[31] == "        {\n"
        defaultLang, defaultIsoCode = langList.getDefaultData()
        assert dummy.captureList[32] == "            "+cppGen._genMakePtrReturnStatement(defaultLang)
        assert dummy.captureList[33] == "        }\n"
        assert dummy.captureList[34] == "    }\n"
        assert dummy.captureList[35] == "    else // null pointer input, use default language\n"
        assert dummy.captureList[36] == "    {\n"
        assert dummy.captureList[37] == "        "+cppGen._genMakePtrReturnStatement(defaultLang)
        assert dummy.captureList[38] == "    } // end of if(nullptr != "+paramName+")\n"
        assert dummy.captureList[39] == "} // end of "+testObj.selectFunctionName+"()\n"
        assert dummy.captureList[40] == "#endif // "+testObj.defOsString+"\n"

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
        paramType = ParamRetDict.getParamType(testObj.paramDictList[0])

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
