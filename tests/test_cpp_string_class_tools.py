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

from code_tools_grocsoftware.base.param_return_tools import ParamRetDict
from code_tools_grocsoftware.base.eula import EulaText
from code_tools_grocsoftware.cpp_gen.file_gen_base import GenerateCppFileHelper
from code_tools_grocsoftware.cpp_gen.string_class_tools import BaseCppStringClassGenerator

class TestClass01StringClass_tools:
    """!
    @brief Unit test for the BaseCppStringClassGenerator class
    """
    def test001ConstructorDefault(self):
        """!
        @brief Test constructor, default input
        """
        testObj = BaseCppStringClassGenerator()

        assert testObj.owner == "BaseCppStringClassGenerator"
        assert testObj.baseClassName == "BaseClass"
        assert testObj.dynamicCompileSwitch == "DYNAMIC_INTERNATIONALIZATION"
        assert testObj.ifDynamicDefined == "defined(DYNAMIC_INTERNATIONALIZATION)"
        assert testObj.baseIntfRetPtrType == "std::shared_ptr<BaseClass>"
        assert testObj.baseIntfRetPtrDict == ParamRetDict.buildReturnDict('sharedptr',
                                                                                      "Shared pointer to BaseClass<lang> based on OS local language")
        assert testObj.typeXlationDict['LANGID'] == "LANGID"
        assert testObj.typeXlationDict['sharedptr'] == "std::shared_ptr<BaseClass>"
        assert testObj.typeXlationDict['strstream'] == "std::stringstream"

        assert testObj.versionMajor == 0
        assert testObj.versionMinor == 4
        assert testObj.versionPatch == 1

        assert testObj.autoToolName == testObj.__class__.__name__+"V0.4.1"
        assert testObj.groupName == "LocalLanguageSelection"

        assert testObj.groupDesc == "Local language detection and selection utility"
        assert testObj.declareIndent == 8
        assert testObj.functionIndent == 4

    """!
    @brief Unit test for the BaseCppStringClassGenerator class
    """
    def test002ConstructorBasic(self):
        """!
        @brief Test constructor
        """
        testObj = BaseCppStringClassGenerator("me", "MIT_open", "TestBaseClass", "BASE_DYNAMIC_SWITCH")

        assert testObj.owner == "me"
        assert testObj.baseClassName == "TestBaseClass"
        assert testObj.dynamicCompileSwitch == "BASE_DYNAMIC_SWITCH"
        assert testObj.ifDynamicDefined == "defined(BASE_DYNAMIC_SWITCH)"
        assert testObj.baseIntfRetPtrType == "std::shared_ptr<TestBaseClass>"
        assert testObj.baseIntfRetPtrDict == ParamRetDict.buildReturnDict('sharedptr',
                                                                                      "Shared pointer to TestBaseClass<lang> based on OS local language")
        assert testObj.typeXlationDict['LANGID'] == "LANGID"
        assert testObj.typeXlationDict['sharedptr'] == "std::shared_ptr<TestBaseClass>"
        assert testObj.typeXlationDict['strstream'] == "std::stringstream"

        assert testObj.versionMajor == 0
        assert testObj.versionMinor == 4
        assert testObj.versionPatch == 1

        assert testObj.autoToolName == testObj.__class__.__name__+"V0.4.1"
        assert testObj.groupName == "LocalLanguageSelection"

        assert testObj.groupDesc == "Local language detection and selection utility"
        assert testObj.declareIndent == 8
        assert testObj.functionIndent == 4

    def test003GetTypes(self):
        """!
        @brief Test _getStringType, _getCharType and _getStrStreamType
        """
        testObj = BaseCppStringClassGenerator()
        assert testObj._getStringType() == testObj.typeXlationDict['string']
        assert testObj._getCharType() == testObj.typeXlationDict['char']
        assert testObj._getStrStreamType() == testObj.typeXlationDict['strstream']

    def test004GenMakePtrReturnStatement(self):
        """!
        @brief Test _genMakePtrReturnStatement
        """
        testObj = BaseCppStringClassGenerator()
        assert testObj._genMakePtrReturnStatement() == "return std::make_shared<BaseClass>();\n"
        assert testObj._genMakePtrReturnStatement("oompa") == "return std::make_shared<BaseClassOompa>();\n"

    def test005GetVersion(self):
        """!
        @brief Test _getVersion
        """
        testObj = BaseCppStringClassGenerator()
        assert testObj._getVersion() == "V"+str(testObj.versionMajor)+"."+str(testObj.versionMinor)+"."+str(testObj.versionPatch)

    def test006GenerateFileHeader(self):
        """!
        @brief Test _generateFileHeader
        """
        testObj = BaseCppStringClassGenerator("Tester", "MIT_open")
        strList = testObj._generateFileHeader()
        eulaData = EulaText('MIT_open')
        eulaName = eulaData.formatEulaName()
        eulaText = eulaData.formatEulaText()
        assert len(strList) == 27
        assert strList[0] == "/*------------------------------------------------------------------------------\n"
        assert strList[1] == "* Copyright (c) 2025 Tester\n"
        assert strList[2] == "* \n"
        assert strList[3] == "* "+eulaName+"\n"
        assert strList[4] == "* \n"

        for index, eulaLine in enumerate(eulaText):
            assert strList[index+5] == "* "+eulaLine+"\n"

        assert strList[23] == "* \n"
        assert strList[24] == "* This file was autogenerated by "+testObj.autoToolName+" do not edit\n"
        assert strList[25] == "* \n"
        assert strList[26] == "* ----------------------------------------------------------------------------*/\n"

    def test007GenerateHFileName(self):
        """!
        @brief Test _generateHFileName
        """
        testObj = BaseCppStringClassGenerator()
        assert testObj._generateHFileName() == testObj.baseClassName+".h"
        assert testObj._generateHFileName("klingon") == testObj.baseClassName+"klingon".capitalize()+".h"

    def test008GenerateCppFileName(self):
        """!
        @brief Test _generateCppFileName
        """
        testObj = BaseCppStringClassGenerator()
        assert testObj._generateCppFileName() == testObj.baseClassName+".cpp"
        assert testObj._generateCppFileName("romulan") == testObj.baseClassName+"romulan".capitalize()+".cpp"

    def test009GenerateUnittestFileName(self):
        """!
        @brief Test _generateUnittestFileName
        """
        testObj = BaseCppStringClassGenerator()
        assert testObj._generateUnittestFileName() == testObj.baseClassName+"_test.cpp"
        assert testObj._generateUnittestFileName("gorn") == testObj.baseClassName+"gorn".capitalize()+"_test.cpp"

    def test010GenerateUnittestTargetName(self):
        """!
        @brief Test _generateUnittestTargetName
        """
        testObj = BaseCppStringClassGenerator()
        assert testObj._generateUnittestTargetName() == testObj.baseClassName+"_test"
        assert testObj._generateUnittestTargetName("telerite") == testObj.baseClassName+"telerite".capitalize()+"_test"

    def test011GenerateMockHFileName(self):
        """!
        @brief Test _generateMockHFileName
        """
        testObj = BaseCppStringClassGenerator()
        assert testObj._generateMockHFileName() == "mock_"+testObj.baseClassName+".h"
        assert testObj._generateMockHFileName("latin") == "mock_"+testObj.baseClassName+"latin".capitalize()+".h"

    def test012GenerateMockCppFileName(self):
        """!
        @brief Test _generateMockCppFileName
        """
        testObj = BaseCppStringClassGenerator()
        assert testObj._generateMockCppFileName() == "mock_"+testObj.baseClassName+".cpp"
        assert testObj._generateMockCppFileName("latin") == "mock_"+testObj.baseClassName+"latin".capitalize()+".cpp"

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
        assert len(strList) == len(expectedList)
        for index, expectedStr in enumerate(expectedList):
            assert strList[index] == expectedStr

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
        assert len(strList) == len(expectedList)
        for index, expectedStr in enumerate(expectedList):
            assert strList[index] == expectedStr

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
        assert len(strList) == len(expectedList)
        for index, expectedStr in enumerate(expectedList):
            assert strList[index] == expectedStr

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
        assert len(strList) == len(expectedList)
        for index, expectedStr in enumerate(expectedList):
            assert strList[index] == expectedStr

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
        assert len(strList) == len(expectedList)
        for index, expectedStr in enumerate(expectedList):
            assert strList[index] == expectedStr

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
        assert len(strList) == 1
        assert strList[0] == expectedMock

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
        assert len(strList) == 1
        assert strList[0] == expectedMock

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
        assert len(strList) == 1
        assert strList[0] == expectedMock

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
        assert len(strList) == 1
        assert strList[0] == expectedMock
