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


from datetime import datetime

from dir_init import pathincsetup
pathincsetup()

from code_tools_grocsoftware.base.param_return_tools import ParamRetDict
from code_tools_grocsoftware.typescript_gen.file_gen_base import GenerateTypeScriptFileHelper

class TestUnittest01CppFilehelper:
    """!
    @brief Unit test for the GenerateTypeScriptFileHelper class
    """
    def test01Constructor(self):
        """!
        @brief Test the constructor
        """
        helper = GenerateTypeScriptFileHelper()

        assert helper.copyrightGenerator is not None
        assert helper.eula is not None
        assert helper.doxyCommentGen is not None
        assert helper.headerCommentGen is not None
        assert helper.levelTabSize == 4

        assert len(list(helper.typeXlationDict.keys())) == 6
        assert helper.typeXlationDict['string'] == "string"
        assert helper.typeXlationDict['text'] == "string"
        assert helper.typeXlationDict['size'] == "number"
        assert helper.typeXlationDict['integer'] == "number"
        assert helper.typeXlationDict['unsigned'] == "number"
        assert helper.typeXlationDict['tuple'] == "tuple"

        helper = GenerateTypeScriptFileHelper("GNU_V11")

        assert helper.copyrightGenerator is not None
        assert helper.eula is not None
        assert helper.doxyCommentGen is not None
        assert helper.headerCommentGen is not None
        assert helper.levelTabSize == 4

        assert len(list(helper.typeXlationDict.keys())) == 6
        assert helper.typeXlationDict['string'] == "string"
        assert helper.typeXlationDict['text'] == "string"
        assert helper.typeXlationDict['size'] == "number"
        assert helper.typeXlationDict['integer'] == "number"
        assert helper.typeXlationDict['unsigned'] == "number"
        assert helper.typeXlationDict['tuple'] == "tuple"

    def test02DeclareTypeBase(self):
        """!
        @brief Test the _declareType method, no modification
        """
        helper = GenerateTypeScriptFileHelper()

        # Test the xlate path
        assert helper._declareType('string') == "string"
        assert helper._declareType('text') == "string"
        assert helper._declareType('size') == "number"
        assert helper._declareType('integer') == "number"
        assert helper._declareType('unsigned') == "number"
        assert helper._declareType('tuple') == "tuple"

        # Test the non-xlate path
        assert helper._declareType('MyClass') == "MyClass"

    def test03DeclareTypePtr(self):
        """!
        @brief Test the _declareType method, pointer modification
        """
        helper = GenerateTypeScriptFileHelper()

        # Test the xlate path
        assert helper._declareType('string', ParamRetDict.typeModPtr) == "string"
        assert helper._declareType('text', ParamRetDict.typeModPtr) == "string"
        assert helper._declareType('size', ParamRetDict.typeModPtr) == "number"
        assert helper._declareType('integer', ParamRetDict.typeModPtr) == "number"
        assert helper._declareType('unsigned', ParamRetDict.typeModPtr) == "number"
        assert helper._declareType('tuple', ParamRetDict.typeModPtr) == "tuple"

    def test04DeclareTypeRef(self):
        """!
        @brief Test the _declareType method, pointer modification
        """
        helper = GenerateTypeScriptFileHelper()

        # Test the xlate path
        assert helper._declareType('string', ParamRetDict.typeModRef) == "string"
        assert helper._declareType('text', ParamRetDict.typeModRef) == "string"
        assert helper._declareType('size', ParamRetDict.typeModRef) == "number"
        assert helper._declareType('integer', ParamRetDict.typeModRef) == "number"
        assert helper._declareType('unsigned', ParamRetDict.typeModRef) == "number"
        assert helper._declareType('tuple', ParamRetDict.typeModRef) == "tuple"

    def test05DeclareTypeList(self):
        """!
        @brief Test the _declareType method, list modification
        """
        helper = GenerateTypeScriptFileHelper()

        # Test the xlate path
        assert helper._declareType('string', ParamRetDict.typeModList) == "string[]"
        assert helper._declareType('text', ParamRetDict.typeModList) == "string[]"
        assert helper._declareType('size', ParamRetDict.typeModList) == "number[]"
        assert helper._declareType('integer', ParamRetDict.typeModList) == "number[]"
        assert helper._declareType('unsigned', ParamRetDict.typeModList) == "number[]"
        assert helper._declareType('tuple', ParamRetDict.typeModList) == "tuple[]"

    def test06DeclareTypeListPtr(self):
        """!
        @brief Test the _declareType method, list and pointer modification
        """
        helper = GenerateTypeScriptFileHelper()

        # Test the xlate path
        typemod = ParamRetDict.typeModList | ParamRetDict.typeModPtr
        assert helper._declareType('string', typemod) == "string[]"
        assert helper._declareType('text', typemod) == "string[]"
        assert helper._declareType('size', typemod) == "number[]"
        assert helper._declareType('integer', typemod) == "number[]"
        assert helper._declareType('unsigned', typemod) == "number[]"
        assert helper._declareType('tuple', typemod) == "tuple[]"

    def test07DeclareTypeListRef(self):
        """!
        @brief Test the _declareType method, list and reference modification
        """
        helper = GenerateTypeScriptFileHelper()

        # Test the xlate path
        typemod = ParamRetDict.typeModList | ParamRetDict.typeModRef
        assert helper._declareType('string', typemod) == "string[]"
        assert helper._declareType('text', typemod) == "string[]"
        assert helper._declareType('size', typemod) == "number[]"
        assert helper._declareType('integer', typemod) == "number[]"
        assert helper._declareType('unsigned', typemod) == "number[]"
        assert helper._declareType('tuple', typemod) == "tuple[]"

    def test08DeclareTypeArray(self):
        """!
        @brief Test the _declareType method, array modification
        """
        helper = GenerateTypeScriptFileHelper()

        # Test the xlate path
        assert helper._declareType('string', 5 << ParamRetDict.typeModArrayShift) == "string[]"
        assert helper._declareType('text', 7 << ParamRetDict.typeModArrayShift) == "string[]"
        assert helper._declareType('size', 10 << ParamRetDict.typeModArrayShift) == "number[]"
        assert helper._declareType('integer', 20 << ParamRetDict.typeModArrayShift) == "number[]"
        assert helper._declareType('unsigned', 13 << ParamRetDict.typeModArrayShift) == "number[]"
        assert helper._declareType('tuple', 14 << ParamRetDict.typeModArrayShift) == "tuple[]"

    def test09DeclareTypeArrayPtr(self):
        """!
        @brief Test the _declareType method, array and pointer modification
        """
        helper = GenerateTypeScriptFileHelper()

        # Test the xlate path
        typemod = (8 << ParamRetDict.typeModArrayShift) | ParamRetDict.typeModPtr
        assert helper._declareType('string', typemod) == "string[]"
        assert helper._declareType('text', typemod) == "string[]"
        assert helper._declareType('size', typemod) == "number[]"
        assert helper._declareType('integer', typemod) == "number[]"
        assert helper._declareType('unsigned', typemod) == "number[]"
        assert helper._declareType('tuple', typemod) == "tuple[]"

    def test10DeclareTypeArrayRef(self):
        """!
        @brief Test the _declareType method, array and reference modification
        """
        helper = GenerateTypeScriptFileHelper()

        # Test the xlate path
        typemod = (8 << ParamRetDict.typeModArrayShift) | ParamRetDict.typeModRef
        assert helper._declareType('string', typemod) == "string[]"
        assert helper._declareType('text', typemod) == "string[]"
        assert helper._declareType('size', typemod) == "number[]"
        assert helper._declareType('integer', typemod) == "number[]"
        assert helper._declareType('unsigned', typemod) == "number[]"

    def test11DeclareTypeUndef(self):
        """!
        @brief Test the _declareType method, all with undef modification
        """
        helper = GenerateTypeScriptFileHelper()

        # Test the xlate path
        assert helper._declareType('string', ParamRetDict.typeModUndef) == "string|undefined"

        typemod = ParamRetDict.typeModUndef | ParamRetDict.typeModPtr
        assert helper._declareType('string', typemod) == "string|undefined"

        typemod = ParamRetDict.typeModUndef | ParamRetDict.typeModRef
        assert helper._declareType('string', typemod) == "string|undefined"

        typemod = (8 << ParamRetDict.typeModArrayShift) | ParamRetDict.typeModUndef
        assert helper._declareType('string', typemod) == "string[]|undefined"

        typemod = ParamRetDict.typeModUndef | ParamRetDict.typeModList
        assert helper._declareType('string', typemod) == "string[]|undefined"

        typemod = (25 << ParamRetDict.typeModArrayShift) | ParamRetDict.typeModUndef | ParamRetDict.typeModPtr
        assert helper._declareType('string', typemod) == "string[]|undefined"

        typemod = (7 << ParamRetDict.typeModArrayShift) | ParamRetDict.typeModUndef | ParamRetDict.typeModRef
        assert helper._declareType('string', typemod) == "string[]|undefined"

        typemod = ParamRetDict.typeModUndef | ParamRetDict.typeModList
        assert helper._declareType('string', typemod) == "string[]|undefined"

        typemod = ParamRetDict.typeModUndef | ParamRetDict.typeModList | ParamRetDict.typeModPtr
        assert helper._declareType('string', typemod) == "string[]|undefined"

        typemod = ParamRetDict.typeModUndef | ParamRetDict.typeModList | ParamRetDict.typeModRef
        assert helper._declareType('string', typemod) == "string[]|undefined"

    def test12XlateParamList(self):
        """!
        @brief Test the _xlateParams method
        """
        helper = GenerateTypeScriptFileHelper()
        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))
        genParamList.append(ParamRetDict.buildParamDictWithMod("goo", "string", "mystr", ParamRetDict.typeModList))

        xlateList = helper._xlateParams(genParamList)
        assert len(xlateList) == len(genParamList)
        assert ParamRetDict.getParamName(xlateList[0]) == ParamRetDict.getParamName(genParamList[0])
        assert ParamRetDict.getParamType(xlateList[0]) == "number"
        assert ParamRetDict.getParamDesc(xlateList[0]) == ParamRetDict.getParamDesc(genParamList[0])
        assert ParamRetDict.getParamTypeMod(xlateList[0]) == 0

        assert ParamRetDict.getParamName(xlateList[1]) == ParamRetDict.getParamName(genParamList[1])
        assert ParamRetDict.getParamType(xlateList[1]) == "number"
        assert ParamRetDict.getParamDesc(xlateList[1]) == ParamRetDict.getParamDesc(genParamList[1])
        assert ParamRetDict.getParamTypeMod(xlateList[1]) == 0

        assert ParamRetDict.getParamName(xlateList[2]) == ParamRetDict.getParamName(genParamList[2])
        assert ParamRetDict.getParamType(xlateList[2]) == "string[]"
        assert ParamRetDict.getParamDesc(xlateList[2]) == ParamRetDict.getParamDesc(genParamList[2])
        assert ParamRetDict.getParamTypeMod(xlateList[2]) == 0

    def test13XlateParamEmptyList(self):
        """!
        @brief Test the _xlateParams method, empty list input
        """
        helper = GenerateTypeScriptFileHelper()
        genParamList = []
        xlateList = helper._xlateParams(genParamList)
        assert len(xlateList) == 0

    def test14XlateRetDict(self):
        """!
        @brief Test the _xlateReturnDict method
        """
        helper = GenerateTypeScriptFileHelper()
        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "myint", 0)

        xlatedRet = helper._xlateReturnDict(genRetDict)
        assert ParamRetDict.getReturnType(xlatedRet) == "number"
        assert ParamRetDict.getParamDesc(xlatedRet) == ParamRetDict.getParamDesc(genRetDict)
        assert ParamRetDict.getParamTypeMod(genRetDict) == 0

    def test15XlateRetDictNone(self):
        """!
        @brief Test the _xlateReturnDict method, with no input
        """
        helper = GenerateTypeScriptFileHelper()
        xlatedRet = helper._xlateReturnDict(None)
        assert xlatedRet is None

    def test16GenReturnType(self):
        """!
        @brief Test the _genFunctionRetType method
        """
        helper = GenerateTypeScriptFileHelper()

        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "myint", 0)
        returnText = helper._genFunctionRetType(genRetDict)
        assert returnText == ":number"

        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "myint", ParamRetDict.typeModList)
        returnText = helper._genFunctionRetType(genRetDict)
        assert returnText == ":number[]"

    def test17GenReturnType(self):
        """!
        @brief Test the _genFunctionRetType method, with none input
        """
        helper = GenerateTypeScriptFileHelper()

        returnText = helper._genFunctionRetType(None)
        assert returnText == ""

    def test18GenFunctionParams(self):
        """!
        @brief Test the _genFunctionParams method
        """
        helper = GenerateTypeScriptFileHelper()
        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))
        genParamList.append(ParamRetDict.buildParamDictWithMod("goo", "string", "mystr", ParamRetDict.typeModList))

        returnText = helper._genFunctionParams(genParamList)
        assert returnText == "(foo:number, moo:number, goo:string[])"

    def test19GenFunctionParamsEmpty(self):
        """!
        @brief Test the _genFunctionParams method, empty list
        """
        helper = GenerateTypeScriptFileHelper()
        genParamList = []
        returnText = helper._genFunctionParams(genParamList)
        assert returnText == "()"

    def test20DeclareFunction(self):
        """!
        @brief Test the _declareFunctionWithDecorations method, no decorations
        """
        helper = GenerateTypeScriptFileHelper()
        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "return int", 0)

        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))

        functionText = helper._declareFunctionWithDecorations("myTest", "My test function", genParamList, genRetDict)
        assert len(functionText) == 11
        assert functionText[0] == '/**\n'
        assert functionText[1] == ' * @brief My test function\n'
        assert functionText[2] == ' * \n'
        assert functionText[3] == ' * @param foo {number} myint\n'
        assert functionText[4] == ' * @param moo {number} mysize\n'
        assert functionText[5] == ' * \n'
        assert functionText[6] == ' * @return number - return int\n'
        assert functionText[7] == ' */\n'
        assert functionText[8] == 'public myTest(foo:number, moo:number):number\n'
        assert functionText[9] == '{\n'

    def test21DeclareFunctionWithPrefix(self):
        """!
        @brief Test the _declareFunctionWithDecorations method, prefix decoration
        """
        helper = GenerateTypeScriptFileHelper()
        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "return int", 0)

        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))

        functionText = helper._declareFunctionWithDecorations("myTest", "My test function", genParamList, genRetDict, 8, prefixDecaration='public')
        assert len(functionText) == 11
        assert functionText[0] == '        /**\n'
        assert functionText[1] == '         * @brief My test function\n'
        assert functionText[2] == '         * \n'
        assert functionText[3] == '         * @param foo {number} myint\n'
        assert functionText[4] == '         * @param moo {number} mysize\n'
        assert functionText[5] == '         * \n'
        assert functionText[6] == '         * @return number - return int\n'
        assert functionText[7] == '         */\n'
        assert functionText[8] == '        public myTest(foo:number, moo:number):number\n'
        assert functionText[9] == '        {\n'

    def test22DeclareFunctionWithPostfix(self):
        """!
        @brief Test the _declareFunctionWithDecorations method, postfix decoration
        """
        helper = GenerateTypeScriptFileHelper()
        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "return int", 0)

        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))

        functionText = helper._declareFunctionWithDecorations("myTest", "My test function", genParamList, genRetDict, 8,
                                                              postfixDecaration='@configurable(false)')
        assert len(functionText) == 12
        assert functionText[0] == '        /**\n'
        assert functionText[1] == '         * @brief My test function\n'
        assert functionText[2] == '         * \n'
        assert functionText[3] == '         * @param foo {number} myint\n'
        assert functionText[4] == '         * @param moo {number} mysize\n'
        assert functionText[5] == '         * \n'
        assert functionText[6] == '         * @return number - return int\n'
        assert functionText[7] == '         */\n'
        assert functionText[8] == '        @configurable(false)\n'
        assert functionText[9] == '        public myTest(foo:number, moo:number):number\n'
        assert functionText[10] == '        {\n'
        assert functionText[11] == '        }\n'

    def test23DeclareFunctionWithPreAndPostfix(self):
        """!
        @brief Test the _declareFunctionWithDecorations method, prefix, postfix decoration
        """
        helper = GenerateTypeScriptFileHelper()
        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "return int", 0)

        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))

        functionText = helper._declareFunctionWithDecorations("myTest", "My test function", genParamList, genRetDict,
                                                              8, prefixDecaration="private", postfixDecaration='@configurable(false)')
        assert len(functionText) == 12
        assert functionText[0] == '        /**\n'
        assert functionText[1] == '         * @brief My test function\n'
        assert functionText[2] == '         * \n'
        assert functionText[3] == '         * @param foo {number} myint\n'
        assert functionText[4] == '         * @param moo {number} mysize\n'
        assert functionText[5] == '         * \n'
        assert functionText[6] == '         * @return number - return int\n'
        assert functionText[7] == '         */\n'
        assert functionText[8] == '        @configurable(false)\n'
        assert functionText[9] == '        private myTest(foo:number, moo:number):number\n'
        assert functionText[10] == '        {\n'
        assert functionText[11] == '        }\n'

    def test24DeclareFunctionWithPreAndPostfixNoComment(self):
        """!
        @brief Test the _declareFunctionWithDecorations method, prefix, postfix decoration, no comment
        """
        helper = GenerateTypeScriptFileHelper()
        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "return int", 0)

        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))

        functionText = helper._declareFunctionWithDecorations("myTest", "My test function", genParamList, genRetDict,
                                                              8, True, "public", '@enumerable(false)')
        assert len(functionText) == 4
        assert functionText[0] == '        @enumerable(false)\n'
        assert functionText[1] == '        public myTest(foo:number, moo:number):number\n'
        assert functionText[2] == '        {\n'
        assert functionText[3] == '        }\n'

    def test25DeclareFunctionWithNoCommentInlineSingleLine(self):
        """!
        @brief Test the _declareFunctionWithDecorations method, no comment inline code
        """
        helper = GenerateTypeScriptFileHelper()
        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "return int", 0)

        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))

        functionText = helper._declareFunctionWithDecorations("myTest", "My test function", genParamList, genRetDict,
                                                              8, True, "public", '@enumerable(false)', ["return 15;"])
        assert len(functionText) == 3
        assert functionText[0] == '        @enumerable(false)\n'
        assert functionText[1] == '        public myTest(foo:number, moo:number):number\n'
        assert functionText[2] == '        {return 15;}\n'

    def test26DeclareFunctionWithNoCommentInlineMultiLine(self):
        """!
        @brief Test the _declareFunctionWithDecorations method, no comment inline code
        """
        helper = GenerateTypeScriptFileHelper()
        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "return list", ParamRetDict.typeModList)

        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))

        inlineCode =["number retvar[];",
                     "retvar.push_back(15);",
                     "retvar.push_back(25);",
                     "return retvar;"]

        functionText = helper._declareFunctionWithDecorations("myTest", "My test function", genParamList, genRetDict,
                                                              8, True, "public", '@enumerable(false)', inlineCode)
        assert len(functionText) == 8
        assert functionText[0] == '        @enumerable(false)\n'
        assert functionText[1] == '        public myTest(foo:number, moo:number):number[]\n'
        assert functionText[2] == '        {\n'
        assert functionText[3] == '            '+inlineCode[0]+'\n'
        assert functionText[4] == '            '+inlineCode[1]+'\n'
        assert functionText[5] == '            '+inlineCode[2]+'\n'
        assert functionText[6] == '            '+inlineCode[3]+'\n'
        assert functionText[7] == '        }\n'

    def test27EndFunction(self):
        """!
        @brief Test the _endFunction method
        """
        helper = GenerateTypeScriptFileHelper()
        functionText = helper._endFunction("myTest")
        assert functionText == '} // end of function myTest\n'

    def test28GenFileHeader(self):
        """!
        @brief Test the _generateGenericFileHeader method
        """
        helper = GenerateTypeScriptFileHelper()
        currentYear = datetime.now().year
        headerText = helper._generateGenericFileHeader("unittest", currentYear, "Me")
        copyrightMsg = "* Copyright (c) "+str(currentYear)+" Me"
        assert len(headerText) == 27
        assert headerText[0] == "/*------------------------------------------------------------------------------\n"
        assert headerText[1] == copyrightMsg+"\n"
        assert headerText[3] == "* MIT License\n"
        assert headerText[24] == "* This file was autogenerated by unittest do not edit\n"
        assert headerText[26] == "* ----------------------------------------------------------------------------*/\n"

    def test29GenImport(self):
        """!
        @brief Test the _genImport method
        """
        helper = GenerateTypeScriptFileHelper()

        includeText = helper._genImport("testclass", "testmodule")
        assert includeText == "import {testclass} from testmodule;\n"

        includeText = helper._genImport("testclass")
        assert includeText == "import 'testclass';\n"

    def test30GenImportBlock(self):
        """!
        @brief Test the _genImportBlock method
        """
        helper = GenerateTypeScriptFileHelper()
        includeList = [("class1", "module1"), ("class2", "module2"), ("class3", "module3"), ("class4", None)]
        includeText = helper._genImportBlock(includeList)
        assert len(includeText) == len(includeList) + 1
        assert includeText[0] == "// Imports\n"
        assert includeText[1] == "import {class1} from module1;\n"
        assert includeText[2] == "import {class2} from module2;\n"
        assert includeText[3] == "import {class3} from module3;\n"
        assert includeText[4] == "import 'class4';\n"

    def test31GenOpenNamespace(self):
        """!
        @brief Test the _genNamespaceOpen method
        """
        helper = GenerateTypeScriptFileHelper()

        testText = helper._genNamespaceOpen("wonder")
        assert len(testText) == 1
        assert testText[0] == "namespace wonder {\n"

        testText = helper._genNamespaceOpen("boy")
        assert len(testText) == 1
        assert testText[0] == "namespace boy {\n"

    def test32GenCloseNamespace(self):
        """!
        @brief Test the _genNamespaceClose method
        """
        helper = GenerateTypeScriptFileHelper()

        testText = helper._genNamespaceClose("wonder")
        assert len(testText) == 1
        assert testText[0] == "} // end of namespace wonder\n"

        testText = helper._genNamespaceClose("boy")
        assert len(testText) == 1
        assert testText[0] == "} // end of namespace boy\n"

    def test34GenClassOpen(self):
        """!
        @brief Test the _genClassOpen method, no decorations
        """
        helper = GenerateTypeScriptFileHelper()

        testText = helper._genClassOpen("MyTestClassName", "My class description")
        assert len(testText) == 5
        assert testText[0] == "/**\n"
        assert testText[1] == " * @brief My class description\n"
        assert testText[2] == " */\n"
        assert testText[3] == "class MyTestClassName\n"
        assert testText[4] == "{\n"

    def test35GenClassOpenWithInheritence(self):
        """!
        @brief Test the _genClassOpen method, with inheritence
        """
        helper = GenerateTypeScriptFileHelper()

        testText = helper._genClassOpen("MyTestClassName", "My class description", "MyBaseClass")
        assert len(testText) == 5
        assert testText[0] == "/**\n"
        assert testText[1] == " * @brief My class description\n"
        assert testText[2] == " */\n"
        assert testText[3] == "class MyTestClassName extends MyBaseClass\n"
        assert testText[4] == "{\n"

    def test36GenClassOpenDecoration(self):
        """!
        @brief Test the _genClassOpen method, with inheritence
        """
        helper = GenerateTypeScriptFileHelper()

        testText = helper._genClassOpen("MyTestClassName", "My class description", "MyBaseClass", "export", 2)
        assert len(testText) == 5
        assert testText[0] == "  /**\n"
        assert testText[1] == "   * @brief My class description\n"
        assert testText[2] == "   */\n"
        assert testText[3] == "  export class MyTestClassName extends MyBaseClass\n"
        assert testText[4] == "  {\n"

    def test37GenClassClose(self):
        """!
        @brief Test the _genClassClose method, with inheritence
        """
        helper = GenerateTypeScriptFileHelper()

        testText = helper._genClassClose("MyTestClassName")
        assert len(testText) == 1
        assert testText[0] == "} // end of MyTestClassName class\n"

        testText = helper._genClassClose("MyTestClassName", 2)
        assert len(testText) == 1
        assert testText[0] == "  } // end of MyTestClassName class\n"

    def test38GenClassDefaultConstrutor(self):
        """!
        @brief Test the _genClassDefaultConstructor method
        """
        helper = GenerateTypeScriptFileHelper()

        testText = helper._genClassDefaultConstructor("MyTestClassName")
        assert len(testText) == 8
        assert testText[0] == "        /**\n"
        assert testText[1] == "         * @brief Construct a new MyTestClassName object\n"
        assert testText[2] == "         * \n"
        assert testText[3] == "         */\n"
        assert testText[4] == "        public constructor()\n"
        assert testText[5] == "        {\n"
        assert testText[6] == "        }\n"
        assert testText[7] == "\n"

    def test39GenClassDefaultContrutorNoDoxy(self):
        """!
        @brief Test the _genClassDefaultConstructor method, with no doxygen comments
        """
        helper = GenerateTypeScriptFileHelper()

        testText = helper._genClassDefaultConstructor("MyTestClassName", noDoxyCommentConstructor=True)
        assert len(testText) == 4
        assert testText[0] == "        public constructor()\n"
        assert testText[1] == "        {\n"
        assert testText[2] == "        }\n"
        assert testText[3] == "\n"

    def test40GenClassDefaultConstrutorWithInputParams(self):
        """!
        @brief Test the _genClassDefaultConstructor method, with doxygen comments, and parameter list
        """
        helper = GenerateTypeScriptFileHelper()
        params = [ParamRetDict.buildParamDictWithMod("one", "string", "Parameter one", 0),
                  ParamRetDict.buildParamDictWithMod("two", "integer", "Parameter two", 0)]
        testText = helper._genClassDefaultConstructor("MyTestClassName", paramList=params)
        assert len(testText) == 11
        assert testText[0] == "        /**\n"
        assert testText[1] == "         * @brief Construct a new MyTestClassName object\n"
        assert testText[2] == "         * \n"
        assert testText[3] == "         * @param one {string} Parameter one\n"
        assert testText[4] == "         * @param two {number} Parameter two\n"
        assert testText[5] == "         * \n"
        assert testText[6] == "         */\n"
        assert testText[7] == "        public constructor(one:string, two:number)\n"
        assert testText[8] == "        {\n"
        assert testText[9] == "        }\n"
        assert testText[10] == "\n"

    def test41GenClassDefaultConstrutorNoDoxyInputParams(self):
        """!
        @brief Test the _genClassDefaultConstructor method, with no doxygen comments, and parameter list
        """
        helper = GenerateTypeScriptFileHelper()
        params = [ParamRetDict.buildParamDictWithMod("one", "string", "Parameter one", 0),
                  ParamRetDict.buildParamDictWithMod("two", "integer", "Parameter two", 0)]
        testText = helper._genClassDefaultConstructor("MyTestClassName", paramList=params, noDoxyCommentConstructor=True)
        assert len(testText) == 4
        assert testText[0] == "        public constructor(one:string, two:number)\n"
        assert testText[1] == "        {\n"
        assert testText[2] == "        }\n"
        assert testText[3] == "\n"

    def test42GenClassDefaultConstrutorNoDoxyWithInline(self):
        """!
        @brief Test the _genClassDefaultConstructor method, with virtual destructor, no doxycomment, no copy
        """
        helper = GenerateTypeScriptFileHelper()

        helper = GenerateTypeScriptFileHelper()
        params = [ParamRetDict.buildParamDictWithMod("one", "string", "Parameter one", 0),
                  ParamRetDict.buildParamDictWithMod("two", "integer", "Parameter two", 0)]
        inlineCode = ["this.one = one;", "this.two = two;"]
        testText = helper._genClassDefaultConstructor("MyTestClassName", 4, params, inlineCode, True)
        assert len(testText) == 6
        assert testText[0] == "    public constructor(one:string, two:number)\n"
        assert testText[1] == "    {\n"
        assert testText[2] == "        this.one = one;\n"
        assert testText[3] == "        this.two = two;\n"
        assert testText[4] == "    }\n"
        assert testText[5] == "\n"

    def test43DeclareStructEmptyList(self):
        """!
        @brief Test the _declareStructure method, No decorations, empty list
        """
        helper = GenerateTypeScriptFileHelper()

        varList = []
        testText = helper._declareStructure("MyTestStructName", varList, 0, "Test structure")
        assert len(testText) == 5
        assert testText[0] == "/**\n"
        assert testText[1] == " * @brief Test structure\n"
        assert testText[2] == " */\n"
        assert testText[3] == "interface MyTestStructName {\n"
        assert testText[4] == "}\n"

    def test44DeclareStruct(self):
        """!
        @brief Test the _declareStructure method, No decorations
        """
        helper = GenerateTypeScriptFileHelper()

        member1 = ParamRetDict.buildParamDictWithMod("foo", "integer", "Test integer", 0)
        member2 = ParamRetDict.buildParamDictWithMod("moo", "unsigned", "Test unsigned", 0)
        varList = [member1, member2]
        testText = helper._declareStructure("MyTestStructName", varList, 0, "Test structure")
        assert len(testText) == 7
        assert testText[0] == "/**\n"
        assert testText[1] == " * @brief Test structure\n"
        assert testText[2] == " */\n"
        assert testText[3] == "interface MyTestStructName {\n"
        assert testText[4] == "    foo:number;                                             //!< Test integer\n"
        assert testText[5] == "    moo:number;                                             //!< Test unsigned\n"
        assert testText[6] == "}\n"

    def test45DeclareStructWithDecorations(self):
        """!
        @brief Test the _declareStructure method, No decorations
        """
        helper = GenerateTypeScriptFileHelper()

        member1 = ParamRetDict.buildParamDictWithMod("foo", "integer", "Test integer", 0)
        member2 = ParamRetDict.buildParamDictWithMod("moo", "unsigned", "Test unsigned", 0)
        varList = [member1, member2]
        testText = helper._declareStructure("MyTestStructName", varList, 0, "Test structure", "export", "const")
        assert len(testText) == 7
        assert testText[0] == "/**\n"
        assert testText[1] == " * @brief Test structure\n"
        assert testText[2] == " */\n"
        assert testText[3] == "export interface MyTestStructName {\n"
        assert testText[4] == "    foo:number;                                             //!< Test integer\n"
        assert testText[5] == "    moo:number;                                             //!< Test unsigned\n"
        assert testText[6] == "} const\n"

    def test46DeclareVariable(self):
        """!
        @brief Test the _declareVarStatment method
        """
        helper = GenerateTypeScriptFileHelper()
        member1 = ParamRetDict.buildParamDictWithMod("foo", "integer", "Test integer", 0)
        member2 = ParamRetDict.buildParamDictWithMod("moo", "unsigned", "Test unsigned", 0)
        member3 = ParamRetDict.buildParamDictWithMod("goo", "string", "Test string", 0)

        testText = helper._declareVarStatment(member1, 30)
        assert testText == "foo:number;                   //!< Test integer\n"

        testText = helper._declareVarStatment(member2, 32)
        assert testText == "moo:number;                     //!< Test unsigned\n"

        testText = helper._declareVarStatment(member3, 10)
        assert testText == "goo:string; //!< Test string\n"

    def test47AddListEntry(self):
        """!
        @brief Test the _genAddListStatment method
        """
        helper = GenerateTypeScriptFileHelper()
        testText = helper._genAddListStatment("testList", "number", False)
        assert testText == "testList.push(number);"
        testText = helper._genAddListStatment("testList", "5", False)
        assert testText == "testList.push(5);"

        testText = helper._genAddListStatment("testList", "text", True)
        assert testText == "testList.push(\"text\");"
        testText = helper._genAddListStatment("testList", "AU", True)
        assert testText == "testList.push(\"AU\");"

    def test48GenerateReturn(self):
        """!
        @brief Test the _genReturnStatment method
        """
        helper = GenerateTypeScriptFileHelper()
        testText = helper._genReturnStatment("number", False)
        assert testText == "return number;"
        testText = helper._genReturnStatment("5", False)
        assert testText == "return 5;"

        testText = helper._genReturnStatment("text", True)
        assert testText == "return \"text\";"
        testText = helper._genReturnStatment("AU", True)
        assert testText == "return \"AU\";"

    def test49DefineFunction(self):
        """!
        @brief Test the _defineFunctionWithDecorations method, no decarations
        """
        helper = GenerateTypeScriptFileHelper()
        retDict = ParamRetDict.buildReturnDictWithMod("integer", "return value", 0)
        paramList = [ParamRetDict.buildParamDictWithMod("foo", "unsigned", "Foo input", 0)]
        testText = helper._defineFunctionWithDecorations("MyDefineFunc", "Brief description", paramList, retDict)
        assert len(testText) == 9
        assert testText[0] == "/**\n"
        assert testText[1] == " * @brief Brief description\n"
        assert testText[2] == " * \n"
        assert testText[3] == " * @param foo {number} Foo input\n"
        assert testText[4] == " * \n"
        assert testText[5] == " * @return number - return value\n"
        assert testText[6] == " */\n"
        assert testText[7] == "function MyDefineFunc(foo:number):number\n"
        assert testText[8] == "{\n"


    def test50DefineFunctionWithPreDecoration(self):
        """!
        @brief Test the _defineFunctionWithDecorations method, with prefix
        """
        helper = GenerateTypeScriptFileHelper()
        retDict = ParamRetDict.buildReturnDictWithMod("integer", "return value", 0)
        paramList = [ParamRetDict.buildParamDictWithMod("foo", "unsigned", "Foo input", 0)]
        testText = helper._defineFunctionWithDecorations("MyDefineFunc", "Brief description", paramList, retDict, False, "export")
        assert len(testText) == 9
        assert testText[0] == "/**\n"
        assert testText[1] == " * @brief Brief description\n"
        assert testText[2] == " * \n"
        assert testText[3] == " * @param foo {number} Foo input\n"
        assert testText[4] == " * \n"
        assert testText[5] == " * @return number - return value\n"
        assert testText[6] == " */\n"
        assert testText[7] == "export function MyDefineFunc(foo:number):number\n"
        assert testText[8] == "{\n"

    def test51DefineFunctionWithPostDecoration(self):
        """!
        @brief Test the _defineFunctionWithDecorations method, with postfix
        """
        helper = GenerateTypeScriptFileHelper()
        retDict = ParamRetDict.buildReturnDictWithMod("integer", "return value", 0)
        paramList = [ParamRetDict.buildParamDictWithMod("foo", "unsigned", "Foo input", 0)]
        testText = helper._defineFunctionWithDecorations("MyDefineFunc", "Brief description", paramList, retDict, postfixDecaration="const")
        assert len(testText) == 9
        assert testText[0] == "/**\n"
        assert testText[1] == " * @brief Brief description\n"
        assert testText[2] == " * \n"
        assert testText[3] == " * @param foo {number} Foo input\n"
        assert testText[4] == " * \n"
        assert testText[5] == " * @return number - return value\n"
        assert testText[6] == " */\n"
        assert testText[7] == "function MyDefineFunc(foo:number):number\n"
        assert testText[8] == "{\n"

    def test52DefineFunctionWithPrePostDecoration(self):
        """!
        @brief Test the _defineFunctionWithDecorations method, with prefix and postfix
        """
        helper = GenerateTypeScriptFileHelper()
        retDict = ParamRetDict.buildReturnDictWithMod("integer", "return value", 0)
        paramList = [ParamRetDict.buildParamDictWithMod("foo", "unsigned", "Foo input", 0)]
        testText = helper._defineFunctionWithDecorations("MyDefineFunc", "Brief description", paramList, retDict,
                                                         prefixDecaration="export", postfixDecaration="const")
        assert len(testText) == 9
        assert testText[0] == "/**\n"
        assert testText[1] == " * @brief Brief description\n"
        assert testText[2] == " * \n"
        assert testText[3] == " * @param foo {number} Foo input\n"
        assert testText[4] == " * \n"
        assert testText[5] == " * @return number - return value\n"
        assert testText[6] == " */\n"
        assert testText[7] == "export function MyDefineFunc(foo:number):number\n"
        assert testText[8] == "{\n"

    def test53DefineFunctionNoComment(self):
        """!
        @brief Test the _defineFunctionWithDecorations method, with no comment
        """
        helper = GenerateTypeScriptFileHelper()
        retDict = ParamRetDict.buildReturnDictWithMod("integer", "return value", 0)
        paramList = [ParamRetDict.buildParamDictWithMod("foo", "unsigned", "Foo input", 0)]
        testText = helper._defineFunctionWithDecorations("MyDefineFunc", "Brief description", paramList, retDict, True)
        assert len(testText) == 2
        assert testText[0] == "function MyDefineFunc(foo:number):number\n"
        assert testText[1] == "{\n"

    def test54DefineFunctionEmptyParamList(self):
        """!
        @brief Test the _defineFunctionWithDecorations method, with empty param list
        """
        helper = GenerateTypeScriptFileHelper()
        retDict = ParamRetDict.buildReturnDictWithMod("integer", "return value", 0)
        testText = helper._defineFunctionWithDecorations("MyDefineFunc", "Brief description", [], retDict, True)
        assert len(testText) == 2
        assert testText[0] == "function MyDefineFunc():number\n"
        assert testText[1] == "{\n"
