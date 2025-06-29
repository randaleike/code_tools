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

import unittest

from dir_init import pathincsetup
pathincsetup()

from code_tools_grocsoftware.base.param_return_tools import ParamRetDict
from code_tools_grocsoftware.base.eula import EulaText
from code_tools_grocsoftware.cpp_gen.file_gen_base import GenerateCppFileHelper
from code_tools_grocsoftware.cpp_gen.string_class_tools import BaseCppStringClassGenerator

class TestClass01StringClass_tools(unittest.TestCase):
    """!
    @brief Unit test for the BaseCppStringClassGenerator class
    """
    def test001ConstructorDefault(self):
        """!
        @brief Test constructor, default input
        """
        testObj = BaseCppStringClassGenerator()

        self.assertEqual(testObj.owner, "BaseCppStringClassGenerator")
        self.assertEqual(testObj.baseClassName, "BaseClass")
        self.assertEqual(testObj.dynamicCompileSwitch, "DYNAMIC_INTERNATIONALIZATION")
        self.assertEqual(testObj.ifDynamicDefined, "defined(DYNAMIC_INTERNATIONALIZATION)")
        self.assertEqual(testObj.baseIntfRetPtrType, "std::shared_ptr<BaseClass>")
        self.assertDictEqual(testObj.baseIntfRetPtrDict, ParamRetDict.buildReturnDict('sharedptr',
                                                                                      "Shared pointer to BaseClass<lang> based on OS local language"))
        self.assertEqual(testObj.typeXlationDict['LANGID'], "LANGID")
        self.assertEqual(testObj.typeXlationDict['sharedptr'], "std::shared_ptr<BaseClass>")
        self.assertEqual(testObj.typeXlationDict['strstream'], "std::stringstream")

        self.assertEqual(testObj.versionMajor, 0)
        self.assertEqual(testObj.versionMinor, 4)
        self.assertEqual(testObj.versionPatch, 1)

        self.assertEqual(testObj.autoToolName, testObj.__class__.__name__+"V0.4.1")
        self.assertEqual(testObj.groupName, "LocalLanguageSelection")

        self.assertEqual(testObj.groupDesc, "Local language detection and selection utility")
        self.assertEqual(testObj.declareIndent, 8)
        self.assertEqual(testObj.functionIndent, 4)

    """!
    @brief Unit test for the BaseCppStringClassGenerator class
    """
    def test002ConstructorBasic(self):
        """!
        @brief Test constructor
        """
        testObj = BaseCppStringClassGenerator("me", "MIT_open", "TestBaseClass", "BASE_DYNAMIC_SWITCH")

        self.assertEqual(testObj.owner, "me")
        self.assertEqual(testObj.baseClassName, "TestBaseClass")
        self.assertEqual(testObj.dynamicCompileSwitch, "BASE_DYNAMIC_SWITCH")
        self.assertEqual(testObj.ifDynamicDefined, "defined(BASE_DYNAMIC_SWITCH)")
        self.assertEqual(testObj.baseIntfRetPtrType, "std::shared_ptr<TestBaseClass>")
        self.assertDictEqual(testObj.baseIntfRetPtrDict, ParamRetDict.buildReturnDict('sharedptr',
                                                                                      "Shared pointer to TestBaseClass<lang> based on OS local language"))
        self.assertEqual(testObj.typeXlationDict['LANGID'], "LANGID")
        self.assertEqual(testObj.typeXlationDict['sharedptr'], "std::shared_ptr<TestBaseClass>")
        self.assertEqual(testObj.typeXlationDict['strstream'], "std::stringstream")

        self.assertEqual(testObj.versionMajor, 0)
        self.assertEqual(testObj.versionMinor, 4)
        self.assertEqual(testObj.versionPatch, 1)

        self.assertEqual(testObj.autoToolName, testObj.__class__.__name__+"V0.4.1")
        self.assertEqual(testObj.groupName, "LocalLanguageSelection")

        self.assertEqual(testObj.groupDesc, "Local language detection and selection utility")
        self.assertEqual(testObj.declareIndent, 8)
        self.assertEqual(testObj.functionIndent, 4)

    def test003GetTypes(self):
        """!
        @brief Test _getStringType, _getCharType and _getStrStreamType
        """
        testObj = BaseCppStringClassGenerator()
        self.assertEqual(testObj._getStringType(), testObj.typeXlationDict['string'])
        self.assertEqual(testObj._getCharType(), testObj.typeXlationDict['char'])
        self.assertEqual(testObj._getStrStreamType(), testObj.typeXlationDict['strstream'])

    def test004GenMakePtrReturnStatement(self):
        """!
        @brief Test _genMakePtrReturnStatement
        """
        testObj = BaseCppStringClassGenerator()
        self.assertEqual(testObj._genMakePtrReturnStatement(), "return std::make_shared<BaseClass>();\n")
        self.assertEqual(testObj._genMakePtrReturnStatement("oompa"), "return std::make_shared<BaseClassOompa>();\n")

    def test005GetVersion(self):
        """!
        @brief Test _getVersion
        """
        testObj = BaseCppStringClassGenerator()
        self.assertEqual(testObj._getVersion(), "V"+str(testObj.versionMajor)+"."+str(testObj.versionMinor)+"."+str(testObj.versionPatch))

    def test006GenerateFileHeader(self):
        """!
        @brief Test _generateFileHeader
        """
        testObj = BaseCppStringClassGenerator("Tester", "MIT_open")
        strList = testObj._generateFileHeader()
        eulaData = EulaText('MIT_open')
        eulaName = eulaData.formatEulaName()
        eulaText = eulaData.formatEulaText()
        self.assertEqual(len(strList), 27)
        self.assertEqual(strList[0], "/*------------------------------------------------------------------------------\n")
        self.assertEqual(strList[1], "* Copyright (c) 2025 Tester\n")
        self.assertEqual(strList[2], "* \n")
        self.assertEqual(strList[3], "* "+eulaName+"\n")
        self.assertEqual(strList[4], "* \n")

        for index, eulaLine in enumerate(eulaText):
            self.assertEqual(strList[index+5], "* "+eulaLine+"\n")

        self.assertEqual(strList[23], "* \n")
        self.assertEqual(strList[24], "* This file was autogenerated by "+testObj.autoToolName+" do not edit\n")
        self.assertEqual(strList[25], "* \n")
        self.assertEqual(strList[26], "* ----------------------------------------------------------------------------*/\n")

    def test007GenerateHFileName(self):
        """!
        @brief Test _generateHFileName
        """
        testObj = BaseCppStringClassGenerator()
        self.assertEqual(testObj._generateHFileName(), testObj.baseClassName+".h")
        self.assertEqual(testObj._generateHFileName("klingon"), testObj.baseClassName+"klingon".capitalize()+".h")

    def test008GenerateCppFileName(self):
        """!
        @brief Test _generateCppFileName
        """
        testObj = BaseCppStringClassGenerator()
        self.assertEqual(testObj._generateCppFileName(), testObj.baseClassName+".cpp")
        self.assertEqual(testObj._generateCppFileName("romulan"), testObj.baseClassName+"romulan".capitalize()+".cpp")

    def test009GenerateUnittestFileName(self):
        """!
        @brief Test _generateUnittestFileName
        """
        testObj = BaseCppStringClassGenerator()
        self.assertEqual(testObj._generateUnittestFileName(), testObj.baseClassName+"_test.cpp")
        self.assertEqual(testObj._generateUnittestFileName("gorn"), testObj.baseClassName+"gorn".capitalize()+"_test.cpp")

    def test010GenerateUnittestTargetName(self):
        """!
        @brief Test _generateUnittestTargetName
        """
        testObj = BaseCppStringClassGenerator()
        self.assertEqual(testObj._generateUnittestTargetName(), testObj.baseClassName+"_test")
        self.assertEqual(testObj._generateUnittestTargetName("telerite"), testObj.baseClassName+"telerite".capitalize()+"_test")

    def test011GenerateMockHFileName(self):
        """!
        @brief Test _generateMockHFileName
        """
        testObj = BaseCppStringClassGenerator()
        self.assertEqual(testObj._generateMockHFileName(), "mock_"+testObj.baseClassName+".h")
        self.assertEqual(testObj._generateMockHFileName("latin"), "mock_"+testObj.baseClassName+"latin".capitalize()+".h")

    def test012GenerateMockCppFileName(self):
        """!
        @brief Test _generateMockCppFileName
        """
        testObj = BaseCppStringClassGenerator()
        self.assertEqual(testObj._generateMockCppFileName(), "mock_"+testObj.baseClassName+".cpp")
        self.assertEqual(testObj._generateMockCppFileName("latin"), "mock_"+testObj.baseClassName+"latin".capitalize()+".cpp")

    def test013WriteMethodMin(self):
        """!
        @brief Test _writeMethod, minimum
        """
        testObj = BaseCppStringClassGenerator()
        cGen = GenerateCppFileHelper()
        returnDict = ParamRetDict.buildReturnDict('string', "Return description")
        strList = testObj._writeMethod("TestMethod", "Test method description", [], returnDict, None, None)
        expectedList = cGen._declareFunctionWithDecorations("TestMethod",
                                                            "Test method description",
                                                            [],
                                                            returnDict,
                                                            testObj.declareIndent,
                                                            True,
                                                            None,
                                                            "const")
        self.assertEqual(len(strList), len(expectedList))
        for index, expectedStr in enumerate(expectedList):
            self.assertEqual(strList[index], expectedStr)

    def test014WriteMethodMinWithDoxygen(self):
        """!
        @brief Test _writeMethod, minimum with doxygen
        """
        testObj = BaseCppStringClassGenerator()
        cGen = GenerateCppFileHelper()
        returnDict = ParamRetDict.buildReturnDict('string', "Return description")
        strList = testObj._writeMethod("TestMethod", "Test method description", [], returnDict, None, None, False)
        expectedList = cGen._declareFunctionWithDecorations("TestMethod",
                                                            "Test method description",
                                                            [],
                                                            returnDict,
                                                            testObj.declareIndent,
                                                            False,
                                                            None,
                                                            "const")
        self.assertEqual(len(strList), len(expectedList))
        for index, expectedStr in enumerate(expectedList):
            self.assertEqual(strList[index], expectedStr)

    def test015WriteMethodWithPrefix(self):
        """!
        @brief Test _writeMethod, with prefix
        """
        testObj = BaseCppStringClassGenerator()
        cGen = GenerateCppFileHelper()
        returnDict = ParamRetDict.buildReturnDict('string', "Return description")
        strList = testObj._writeMethod("TestMethod", "Test method description", [], returnDict, "virtual", None)
        expectedList = cGen._declareFunctionWithDecorations("TestMethod",
                                                            "Test method description",
                                                            [],
                                                            returnDict,
                                                            testObj.declareIndent,
                                                            True,
                                                            "virtual",
                                                            "const")
        self.assertEqual(len(strList), len(expectedList))
        for index, expectedStr in enumerate(expectedList):
            self.assertEqual(strList[index], expectedStr)

    def test016WriteMethodWithPostfix(self):
        """!
        @brief Test _writeMethod, with postfix
        """
        testObj = BaseCppStringClassGenerator()
        cGen = GenerateCppFileHelper()
        returnDict = ParamRetDict.buildReturnDict('string', "Return description")
        paramDict = ParamRetDict.buildParamDict("foo", "integer", "Integer description")
        strList = testObj._writeMethod("TestMethod", "Test method description", [paramDict], returnDict, "virtual", "final")
        expectedList = cGen._declareFunctionWithDecorations("TestMethod",
                                                            "Test method description",
                                                            [paramDict],
                                                            returnDict,
                                                            testObj.declareIndent,
                                                            True,
                                                            "virtual",
                                                            "final")
        self.assertEqual(len(strList), len(expectedList))
        for index, expectedStr in enumerate(expectedList):
            self.assertEqual(strList[index], expectedStr)

    def test017WriteMethodWithPostfixOnly(self):
        """!
        @brief Test _writeMethod, with postfix
        """
        testObj = BaseCppStringClassGenerator()
        cGen = GenerateCppFileHelper()
        returnDict = ParamRetDict.buildReturnDict('string', "Return description")
        paramList = []
        strList = testObj._writeMethod("TestMethod", "Test method description", paramList, returnDict, "virtual", "final")
        expectedList = cGen._declareFunctionWithDecorations("TestMethod",
                                                            "Test method description",
                                                            paramList,
                                                            returnDict,
                                                            testObj.declareIndent,
                                                            True,
                                                            "virtual",
                                                            "const final")
        self.assertEqual(len(strList), len(expectedList))
        for index, expectedStr in enumerate(expectedList):
            self.assertEqual(strList[index], expectedStr)

    def test018WriteMockMethodMin(self):
        """!
        @brief Test _writeMethod, minimum
        """
        testObj = BaseCppStringClassGenerator()

        cGen = GenerateCppFileHelper()
        returnDict = ParamRetDict.buildReturnDict('string', "Return description")
        expectedDecl = cGen._declareType(ParamRetDict.getReturnType(returnDict), ParamRetDict.getParamTypeMod(returnDict))
        expectedParms = cGen._genFunctionParams([])
        expectedMock = "        MOCK_METHOD("+expectedDecl+", TestMethod, "+expectedParms+", (const));\n"

        strList = testObj._writeMockMethod("TestMethod", [], returnDict, None)
        self.assertEqual(len(strList), 1)
        self.assertEqual(strList[0], expectedMock)

    def test019WriteMockMethodWithParam(self):
        """!
        @brief Test _writeMethod, with param
        """
        testObj = BaseCppStringClassGenerator()

        cGen = GenerateCppFileHelper()
        returnDict = ParamRetDict.buildReturnDict('string', "Return description")
        paramList = [ParamRetDict.buildParamDict("foo", "integer", "Integer description")]
        expectedDecl = cGen._declareType(ParamRetDict.getReturnType(returnDict), ParamRetDict.getParamTypeMod(returnDict))
        expectedParms = cGen._genFunctionParams(paramList)
        expectedMock = "        MOCK_METHOD("+expectedDecl+", TestMethod, "+expectedParms+");\n"

        strList = testObj._writeMockMethod("TestMethod", paramList, returnDict, None)
        self.assertEqual(len(strList), 1)
        self.assertEqual(strList[0], expectedMock)

    def test020WriteMockMethodWithPostfix(self):
        """!
        @brief Test _writeMethod, with postfix
        """
        testObj = BaseCppStringClassGenerator()

        cGen = GenerateCppFileHelper()
        returnDict = ParamRetDict.buildReturnDict('string', "Return description")
        paramList = []
        expectedDecl = cGen._declareType(ParamRetDict.getReturnType(returnDict), ParamRetDict.getParamTypeMod(returnDict))
        expectedParms = cGen._genFunctionParams(paramList)
        expectedMock = "        MOCK_METHOD("+expectedDecl+", TestMethod, "+expectedParms+", (const, override));\n"

        strList = testObj._writeMockMethod("TestMethod", paramList, returnDict, "override")
        self.assertEqual(len(strList), 1)
        self.assertEqual(strList[0], expectedMock)

    def test021WriteMockMethodWithParamPostfix(self):
        """!
        @brief Test _writeMethod, with param and postfix
        """
        testObj = BaseCppStringClassGenerator()

        cGen = GenerateCppFileHelper()
        returnDict = ParamRetDict.buildReturnDict('string', "Return description")
        paramList = [ParamRetDict.buildParamDict("foo", "integer", "Integer description")]
        expectedDecl = cGen._declareType(ParamRetDict.getReturnType(returnDict), ParamRetDict.getParamTypeMod(returnDict))
        expectedParms = cGen._genFunctionParams(paramList)
        expectedMock = "        MOCK_METHOD("+expectedDecl+", TestMethod, "+expectedParms+", (override));\n"

        strList = testObj._writeMockMethod("TestMethod", paramList, returnDict, "override")
        self.assertEqual(len(strList), 1)
        self.assertEqual(strList[0], expectedMock)

if __name__ == '__main__':
    unittest.main()