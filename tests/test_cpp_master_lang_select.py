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
from code_tools_grocsoftware.cpp_gen.windows_lang_select import WindowsLangSelectFunctionGenerator
from code_tools_grocsoftware.cpp_gen.linux_lang_select import LinuxLangSelectFunctionGenerator
from code_tools_grocsoftware.cpp_gen.master_lang_select import MasterSelectFunctionGenerator

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

class TestClass01MasterLangSelect:
    """!
    @brief Unit test for the BaseCppStringClassGenerator class
    """
    def test001ConstructorDefault(self):
        """!
        @brief Test constructor, default input
        """
        testObj = MasterSelectFunctionGenerator()

        assert testObj.baseClassName == "BaseClass"
        assert testObj.selectBaseFunctionName == "getLocalParserStringListInterface"
        assert testObj.dynamicCompileSwitch == "DYNAMIC_INTERNATIONALIZATION"
        assert testObj.selectFunctionName == "BaseClass::getLocalParserStringListInterface"
        assert testObj.briefDesc == "Determine the OS use OS specific functions to determine the correct local language" \
                                    "based on the OS specific local language setting and return the correct class object"
        assert isinstance(testObj.doxyCommentGen, CDoxyCommentGenerator)

    def test002ConstructorNonDefault(self):
        """!
        @brief Test constructor, with input
        """
        testObj = MasterSelectFunctionGenerator("George", "MIT_open", "TestBaseClass", "getLocalLang", "TEST_DYNAM_SWITCH")

        assert testObj.baseClassName == "TestBaseClass"
        assert testObj.selectBaseFunctionName == "getLocalLang"
        assert testObj.dynamicCompileSwitch == "TEST_DYNAM_SWITCH"
        assert testObj.selectFunctionName == "TestBaseClass::getLocalLang"
        assert testObj.briefDesc == "Determine the OS use OS specific functions to determine the correct local language" \
                                    "based on the OS specific local language setting and return the correct class object"
        assert isinstance(testObj.doxyCommentGen, CDoxyCommentGenerator)

    def test003GetFunctionName(self):
        """!
        @brief Test getFunctionName
        """
        testObj = MasterSelectFunctionGenerator()
        assert testObj.getFunctionName() == "BaseClass::getLocalParserStringListInterface"

    def test004GetFunctionDesc(self):
        """!
        @brief Test getFunctionDesc
        """
        testObj = MasterSelectFunctionGenerator()
        functionName, briefDesc, retPtrDict, parmaList = testObj.getFunctionDesc()
        assert functionName == testObj.selectBaseFunctionName
        assert briefDesc == testObj.briefDesc
        assert retPtrDict == testObj.baseIntfRetPtrDict
        assert len(parmaList) == 0

    def test005GenFunctionDefine(self):
        """!
        @brief Test genFunctionDefine
        """
        cppGen = BaseCppStringClassGenerator()
        testObj = MasterSelectFunctionGenerator(LanguageDescriptionList())
        expectedList = cppGen._defineFunctionWithDecorations(testObj.selectFunctionName,
                                                             testObj.briefDesc,
                                                             [],
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
        testObj = MasterSelectFunctionGenerator(LanguageDescriptionList())
        assert testObj.genFunctionEnd() == "} // end of "+testObj.selectFunctionName+"()\n"

    def test007GenFunction(self):
        """!
        @brief Test genFunction
        """
        cppGen = BaseCppStringClassGenerator()
        osLangSelectors = [LinuxLangSelectFunctionGenerator(LanguageDescriptionList()),
                           WindowsLangSelectFunctionGenerator(LanguageDescriptionList())]
        testObj = MasterSelectFunctionGenerator(osLangSelectors)

        captureList = testObj.genFunction(osLangSelectors)

        assert len(captureList) == 18
        expectedList = cppGen._defineFunctionWithDecorations(testObj.selectFunctionName,
                                                             testObj.briefDesc,
                                                             [],
                                                             testObj.baseIntfRetPtrDict)
        expectedList.append("{\n")
        for index, expectedText in enumerate(expectedList):
            assert captureList[index] == expectedText

        listIndex = len(expectedList)
        first = True
        for osSelector in osLangSelectors:
            if first:
                ifLine = "#if "
                first = False
            else:
                ifLine = "#elif "
            ifLine += osSelector.getOsDefine()+"\n"

            assert captureList[listIndex] == ""+ifLine
            listIndex += 1
            osCallList = osSelector.genReturnFunctionCall(4)
            for osIndex, expectedOsCallLine in enumerate(osCallList):
                assert captureList[listIndex+osIndex] == expectedOsCallLine

            listIndex += len(osCallList)

        assert captureList[listIndex] == "#else // not defined os\n"
        assert captureList[listIndex+1] == "    #error No language generation method defined for this OS\n"
        assert captureList[listIndex+2] == "#endif // defined os\n"
        assert captureList[listIndex+3] == "} // end of "+testObj.selectFunctionName+"()\n"

    def test008GenReturnFunctionCall(self):
        """!
        @brief Test genReturnFunctionCall
        """
        testObj = MasterSelectFunctionGenerator()
        strList = testObj.genReturnFunctionCall()
        assert len(strList) == 1
        assert strList[0] == "    return "+testObj.selectFunctionName+"();\n"

    def test009GenUnitTest(self):
        """!
        @brief Test genUnitTest
        """
        osLangSelectors = [LinuxLangSelectFunctionGenerator(LanguageDescriptionList()),
                           WindowsLangSelectFunctionGenerator(LanguageDescriptionList())]
        testObj = MasterSelectFunctionGenerator()
        textList = testObj.genUnitTest("getIsoCode", osLangSelectors)

        # Test extern definitions
        assert len(textList) == 31
        index = 0
        for osSelector in osLangSelectors:
            expectedList = osSelector.getUnittestExternInclude()
            for expectedLine in expectedList:
                assert textList[index] == expectedLine
                index += 1

        assert textList[index] == "\n"

        # Test Doxygen generation
        doxyGen = CDoxyCommentGenerator()
        doxyDesc = "Test "+testObj.selectFunctionName+" selection case"
        doxyBody = doxyGen.genDoxyMethodComment(doxyDesc, [])

        assert textList[index+1] == doxyBody[0]
        assert textList[index+2] == doxyBody[1]
        assert textList[index+3] == doxyBody[2]
        assert textList[index+4] == doxyBody[3]
        index += 5

        textList[index] == "TEST(SelectFunction, TestLocalSelectMethod)\n"
        textList[index+1] == "{\n"

        firstOs = True
        index += 2
        for osSelector in osLangSelectors:
            if firstOs:
                textList[index] == "#if "+osSelector.getOsDefine()+"\n"
                firstOs = False
            else:
                textList[index] == "#elif "+osSelector.getOsDefine()+"\n"
            textList[index+1] == "    // Get the expected value\n"
            index += 2

            expectedCallList = osSelector.genUnitTestFunctionCall("varName", 4)
            for expectedLine in expectedCallList:
                textList[index] == expectedLine
                index += 1

        # Add the #else case
        textList[index] == "#else // not defined os\n"
        textList[index+1] == "    #error No language generation defined for this OS\n"

        # Complete the function
        textList[index+2] == "#endif // defined os\n"
        textList[index+3] == "\n"
        textList[index+4] == "    // Generate the test language string object\n"
        textList[index+5] == "    "+testObj.baseIntfRetPtrType+" testVar = "+testObj.selectFunctionName+"();\n"
        textList[index+6] == "    EXPECT_STREQ(varName->getIsoCode().c_str(), testVar->getIsoCode().c_str());\n"
        textList[index+7] == "} // end of "+testObj.selectFunctionName+"()\n"
