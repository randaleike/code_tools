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
from code_tools_grocsoftware.cpp_gen.file_gen_base import GenerateCppFileHelper

class TestUnittest01CppFilehelper:
    """!
    @brief Unit test for the GenerateCppFileHelper class
    """
    def test01Constructor(self):
        """!
        @brief Test the constructor
        """
        helper = GenerateCppFileHelper()

        assert helper.copyrightGenerator is not None
        assert helper.eula is not None
        assert helper.doxyCommentGen is not None
        assert helper.headerCommentGen is not None
        assert helper.levelTabSize == 4

        assert len(list(helper.typeXlationDict.keys())) == 6
        assert helper.typeXlationDict['string'] == "std::string"
        assert helper.typeXlationDict['text'] == "std::string"
        assert helper.typeXlationDict['size'] == "size_t"
        assert helper.typeXlationDict['integer'] == "int"
        assert helper.typeXlationDict['unsigned'] == "unsigned"
        assert helper.typeXlationDict['char'] == "char"

        helper = GenerateCppFileHelper("GNU_V11")

        assert helper.copyrightGenerator is not None
        assert helper.eula is not None
        assert helper.doxyCommentGen is not None
        assert helper.headerCommentGen is not None
        assert helper.levelTabSize == 4

        assert len(list(helper.typeXlationDict.keys())) == 6
        assert helper.typeXlationDict['string'] == "std::string"
        assert helper.typeXlationDict['text'] == "std::string"
        assert helper.typeXlationDict['size'] == "size_t"
        assert helper.typeXlationDict['integer'] == "int"
        assert helper.typeXlationDict['unsigned'] == "unsigned"
        assert helper.typeXlationDict['char'] == "char"

    def test02DeclareTypeBase(self):
        """!
        @brief Test the _declareType method, no modification
        """
        helper = GenerateCppFileHelper()

        # Test the xlate path
        assert helper._declareType('string') == "std::string"
        assert helper._declareType('text') == "std::string"
        assert helper._declareType('size') == "size_t"
        assert helper._declareType('integer') == "int"
        assert helper._declareType('unsigned') == "unsigned"

        # Test the non-xlate path
        assert helper._declareType('MyClass') == "MyClass"

    def test03DeclareTypePtr(self):
        """!
        @brief Test the _declareType method, pointer modification
        """
        helper = GenerateCppFileHelper()

        # Test the xlate path
        assert helper._declareType('string', ParamRetDict.typeModPtr) == "std::string*"
        assert helper._declareType('text', ParamRetDict.typeModPtr) == "std::string*"
        assert helper._declareType('size', ParamRetDict.typeModPtr) == "size_t*"
        assert helper._declareType('integer', ParamRetDict.typeModPtr) == "int*"
        assert helper._declareType('unsigned', ParamRetDict.typeModPtr) == "unsigned*"

    def test04DeclareTypeRef(self):
        """!
        @brief Test the _declareType method, pointer modification
        """
        helper = GenerateCppFileHelper()

        # Test the xlate path
        assert helper._declareType('string', ParamRetDict.typeModRef) == "std::string&"
        assert helper._declareType('text', ParamRetDict.typeModRef) == "std::string&"
        assert helper._declareType('size', ParamRetDict.typeModRef) == "size_t&"
        assert helper._declareType('integer', ParamRetDict.typeModRef) == "int&"
        assert helper._declareType('unsigned', ParamRetDict.typeModRef) == "unsigned&"

    def test05DeclareTypeList(self):
        """!
        @brief Test the _declareType method, list modification
        """
        helper = GenerateCppFileHelper()

        # Test the xlate path
        assert helper._declareType('string', ParamRetDict.typeModList) == "std::list<std::string>"
        assert helper._declareType('text', ParamRetDict.typeModList) == "std::list<std::string>"
        assert helper._declareType('size', ParamRetDict.typeModList) == "std::list<size_t>"
        assert helper._declareType('integer', ParamRetDict.typeModList) == "std::list<int>"
        assert helper._declareType('unsigned', ParamRetDict.typeModList) == "std::list<unsigned>"

    def test06DeclareTypeListPtr(self):
        """!
        @brief Test the _declareType method, list and pointer modification
        """
        helper = GenerateCppFileHelper()

        # Test the xlate path
        typemod = ParamRetDict.typeModList | ParamRetDict.typeModPtr
        assert helper._declareType('string', typemod) == "std::list<std::string*>"
        assert helper._declareType('text', typemod) == "std::list<std::string*>"
        assert helper._declareType('size', typemod) == "std::list<size_t*>"
        assert helper._declareType('integer', typemod) == "std::list<int*>"
        assert helper._declareType('unsigned', typemod) == "std::list<unsigned*>"

    def test07DeclareTypeListRef(self):
        """!
        @brief Test the _declareType method, list and reference modification
        """
        helper = GenerateCppFileHelper()

        # Test the xlate path
        typemod = ParamRetDict.typeModList | ParamRetDict.typeModRef
        assert helper._declareType('string', typemod) == "std::list<std::string&>"
        assert helper._declareType('text', typemod) == "std::list<std::string&>"
        assert helper._declareType('size', typemod) == "std::list<size_t&>"
        assert helper._declareType('integer', typemod) == "std::list<int&>"
        assert helper._declareType('unsigned', typemod) == "std::list<unsigned&>"

    def test08DeclareTypeArray(self):
        """!
        @brief Test the _declareType method, array modification
        """
        helper = GenerateCppFileHelper()

        # Test the xlate path
        assert helper._declareType('string', 5 << ParamRetDict.typeModArrayShift) == "std::array<std::string, 5>"
        assert helper._declareType('text', 7 << ParamRetDict.typeModArrayShift) == "std::array<std::string, 7>"
        assert helper._declareType('size', 10 << ParamRetDict.typeModArrayShift) == "std::array<size_t, 10>"
        assert helper._declareType('integer', 20 << ParamRetDict.typeModArrayShift) == "std::array<int, 20>"
        assert helper._declareType('unsigned', 13 << ParamRetDict.typeModArrayShift) == "std::array<unsigned, 13>"

    def test09DeclareTypeArrayPtr(self):
        """!
        @brief Test the _declareType method, array and pointer modification
        """
        helper = GenerateCppFileHelper()

        # Test the xlate path
        typemod = (8 << ParamRetDict.typeModArrayShift) | ParamRetDict.typeModPtr
        assert helper._declareType('string', typemod) == "std::array<std::string*, 8>"
        assert helper._declareType('text', typemod) == "std::array<std::string*, 8>"
        assert helper._declareType('size', typemod) == "std::array<size_t*, 8>"
        assert helper._declareType('integer', typemod) == "std::array<int*, 8>"
        assert helper._declareType('unsigned', typemod) == "std::array<unsigned*, 8>"

    def test10DeclareTypeArrayRef(self):
        """!
        @brief Test the _declareType method, array and reference modification
        """
        helper = GenerateCppFileHelper()

        # Test the xlate path
        typemod = (8 << ParamRetDict.typeModArrayShift) | ParamRetDict.typeModRef
        assert helper._declareType('string', typemod) == "std::array<std::string&, 8>"
        assert helper._declareType('text', typemod) == "std::array<std::string&, 8>"
        assert helper._declareType('size', typemod) == "std::array<size_t&, 8>"
        assert helper._declareType('integer', typemod) == "std::array<int&, 8>"
        assert helper._declareType('unsigned', typemod) == "std::array<unsigned&, 8>"

    def test11DeclareTypeUndef(self):
        """!
        @brief Test the _declareType method, all with undef modification
        """
        helper = GenerateCppFileHelper()

        # Test the xlate path
        assert helper._declareType('string', ParamRetDict.typeModUndef) == "std::string"

        typemod = ParamRetDict.typeModUndef | ParamRetDict.typeModPtr
        assert helper._declareType('string', typemod) == "std::string*"

        typemod = ParamRetDict.typeModUndef | ParamRetDict.typeModRef
        assert helper._declareType('string', typemod) == "std::string&"

        typemod = (8 << ParamRetDict.typeModArrayShift) | ParamRetDict.typeModUndef
        assert helper._declareType('string', typemod) == "std::array<std::string, 8>"

        typemod = ParamRetDict.typeModUndef | ParamRetDict.typeModList
        assert helper._declareType('string', typemod) == "std::list<std::string>"

        typemod = (25 << ParamRetDict.typeModArrayShift) | ParamRetDict.typeModUndef | ParamRetDict.typeModPtr
        assert helper._declareType('string', typemod) == "std::array<std::string*, 25>"

        typemod = (7 << ParamRetDict.typeModArrayShift) | ParamRetDict.typeModUndef | ParamRetDict.typeModRef
        assert helper._declareType('string', typemod) == "std::array<std::string&, 7>"

        typemod = ParamRetDict.typeModUndef | ParamRetDict.typeModList
        assert helper._declareType('string', typemod) == "std::list<std::string>"

        typemod = ParamRetDict.typeModUndef | ParamRetDict.typeModList | ParamRetDict.typeModPtr
        assert helper._declareType('string', typemod) == "std::list<std::string*>"

        typemod = ParamRetDict.typeModUndef | ParamRetDict.typeModList | ParamRetDict.typeModRef
        assert helper._declareType('string', typemod) == "std::list<std::string&>"

    def test12XlateParamList(self):
        """!
        @brief Test the _xlateParams method
        """
        helper = GenerateCppFileHelper()
        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))
        genParamList.append(ParamRetDict.buildParamDictWithMod("goo", "string", "mystr", ParamRetDict.typeModList))

        xlateList = helper._xlateParams(genParamList)
        assert len(xlateList) == len(genParamList)
        assert ParamRetDict.getParamName(xlateList[0]) == ParamRetDict.getParamName(genParamList[0])
        assert ParamRetDict.getParamType(xlateList[0]) == "int"
        assert ParamRetDict.getParamDesc(xlateList[0]) == ParamRetDict.getParamDesc(genParamList[0])
        assert ParamRetDict.getParamTypeMod(xlateList[0]) == 0

        assert ParamRetDict.getParamName(xlateList[1]) == ParamRetDict.getParamName(genParamList[1])
        assert ParamRetDict.getParamType(xlateList[1]) == "size_t*"
        assert ParamRetDict.getParamDesc(xlateList[1]) == ParamRetDict.getParamDesc(genParamList[1])
        assert ParamRetDict.getParamTypeMod(xlateList[1]) == 0

        assert ParamRetDict.getParamName(xlateList[2]) == ParamRetDict.getParamName(genParamList[2])
        assert ParamRetDict.getParamType(xlateList[2]) == "std::list<std::string>"
        assert ParamRetDict.getParamDesc(xlateList[2]) == ParamRetDict.getParamDesc(genParamList[2])
        assert ParamRetDict.getParamTypeMod(xlateList[2]) == 0

    def test13XlateParamEmptyList(self):
        """!
        @brief Test the _xlateParams method, empty list input
        """
        helper = GenerateCppFileHelper()
        genParamList = []
        xlateList = helper._xlateParams(genParamList)
        assert len(xlateList) == 0

    def test14XlateRetDict(self):
        """!
        @brief Test the _xlateReturnDict method
        """
        helper = GenerateCppFileHelper()
        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "myint", 0)

        xlatedRet = helper._xlateReturnDict(genRetDict)
        assert ParamRetDict.getReturnType(xlatedRet) == "int"
        assert ParamRetDict.getParamDesc(xlatedRet) == ParamRetDict.getParamDesc(genRetDict)
        assert ParamRetDict.getParamTypeMod(genRetDict) == 0

    def test15XlateRetDictNone(self):
        """!
        @brief Test the _xlateReturnDict method, with no input
        """
        helper = GenerateCppFileHelper()
        xlatedRet = helper._xlateReturnDict(None)
        assert xlatedRet is None

    def test16GenReturnType(self):
        """!
        @brief Test the _genFunctionRetType method
        """
        helper = GenerateCppFileHelper()

        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "myint", 0)
        returnText = helper._genFunctionRetType(genRetDict)
        assert returnText == "int "

        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "myint", ParamRetDict.typeModList)
        returnText = helper._genFunctionRetType(genRetDict)
        assert returnText == "std::list<int> "

    def test17GenReturnType(self):
        """!
        @brief Test the _genFunctionRetType method, with none input
        """
        helper = GenerateCppFileHelper()

        returnText = helper._genFunctionRetType(None)
        assert returnText == ""

    def test18GenFunctionParams(self):
        """!
        @brief Test the _genFunctionParams method
        """
        helper = GenerateCppFileHelper()
        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))
        genParamList.append(ParamRetDict.buildParamDictWithMod("goo", "string", "mystr", ParamRetDict.typeModList))

        returnText = helper._genFunctionParams(genParamList)
        assert returnText == "(int foo, size_t* moo, std::list<std::string> goo)"

    def test19GenFunctionParamsEmpty(self):
        """!
        @brief Test the _genFunctionParams method, empty list
        """
        helper = GenerateCppFileHelper()
        genParamList = []
        returnText = helper._genFunctionParams(genParamList)
        assert returnText == "()"

    def test20DeclareFunction(self):
        """!
        @brief Test the _declareFunctionWithDecorations method, no decorations
        """
        helper = GenerateCppFileHelper()
        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "return int", 0)

        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))

        functionText = helper._declareFunctionWithDecorations("myTest", "My test function", genParamList, genRetDict)
        assert len(functionText) == 9
        assert functionText[0] == '/**\n'
        assert functionText[1] == ' * @brief My test function\n'
        assert functionText[2] == ' * \n'
        assert functionText[3] == ' * @param foo myint\n'
        assert functionText[4] == ' * @param moo mysize\n'
        assert functionText[5] == ' * \n'
        assert functionText[6] == ' * @return int - return int\n'
        assert functionText[7] == ' */\n'
        assert functionText[8] == 'int myTest(int foo, size_t* moo);\n'

    def test21DeclareFunctionWithPrefix(self):
        """!
        @brief Test the _declareFunctionWithDecorations method, prefix decoration
        """
        helper = GenerateCppFileHelper()
        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "return int", 0)

        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))

        functionText = helper._declareFunctionWithDecorations("myTest", "My test function", genParamList, genRetDict, 8, prefixDecaration='virtual')
        assert len(functionText) == 9
        assert functionText[0] == '        /**\n'
        assert functionText[1] == '         * @brief My test function\n'
        assert functionText[2] == '         * \n'
        assert functionText[3] == '         * @param foo myint\n'
        assert functionText[4] == '         * @param moo mysize\n'
        assert functionText[5] == '         * \n'
        assert functionText[6] == '         * @return int - return int\n'
        assert functionText[7] == '         */\n'
        assert functionText[8] == '        virtual int myTest(int foo, size_t* moo);\n'

    def test22DeclareFunctionWithPostfix(self):
        """!
        @brief Test the _declareFunctionWithDecorations method, postfix decoration
        """
        helper = GenerateCppFileHelper()
        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "return int", 0)

        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))

        functionText = helper._declareFunctionWithDecorations("myTest", "My test function", genParamList, genRetDict, 8, postfixDecaration='const override')
        assert len(functionText) == 9
        assert functionText[0] == '        /**\n'
        assert functionText[1] == '         * @brief My test function\n'
        assert functionText[2] == '         * \n'
        assert functionText[3] == '         * @param foo myint\n'
        assert functionText[4] == '         * @param moo mysize\n'
        assert functionText[5] == '         * \n'
        assert functionText[6] == '         * @return int - return int\n'
        assert functionText[7] == '         */\n'
        assert functionText[8] == '        int myTest(int foo, size_t* moo) const override;\n'

    def test23DeclareFunctionWithPreAndPostfix(self):
        """!
        @brief Test the _declareFunctionWithDecorations method, prefix, postfix decoration
        """
        helper = GenerateCppFileHelper()
        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "return int", 0)

        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))

        functionText = helper._declareFunctionWithDecorations("myTest", "My test function", genParamList, genRetDict,
                                                              8, prefixDecaration="[[nodiscard]]", postfixDecaration='const override')
        assert len(functionText) == 9
        assert functionText[0] == '        /**\n'
        assert functionText[1] == '         * @brief My test function\n'
        assert functionText[2] == '         * \n'
        assert functionText[3] == '         * @param foo myint\n'
        assert functionText[4] == '         * @param moo mysize\n'
        assert functionText[5] == '         * \n'
        assert functionText[6] == '         * @return int - return int\n'
        assert functionText[7] == '         */\n'
        assert functionText[8] == '        [[nodiscard]] int myTest(int foo, size_t* moo) const override;\n'

    def test24DeclareFunctionWithPreAndPostfixNoComment(self):
        """!
        @brief Test the _declareFunctionWithDecorations method, prefix, postfix decoration, no comment
        """
        helper = GenerateCppFileHelper()
        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "return int", 0)

        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))

        functionText = helper._declareFunctionWithDecorations("myTest", "My test function", genParamList, genRetDict,
                                                              8, True, "[[nodiscard]]", 'const override')
        assert len(functionText) == 1
        assert functionText[0] == '        [[nodiscard]] int myTest(int foo, size_t* moo) const override;\n'

    def test25DeclareFunctionWithNoCommentInlineSingleLine(self):
        """!
        @brief Test the _declareFunctionWithDecorations method, no comment inline code
        """
        helper = GenerateCppFileHelper()
        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "return int", 0)

        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))

        functionText = helper._declareFunctionWithDecorations("myTest", "My test function", genParamList, genRetDict,
                                                              8, True, "[[nodiscard]]", 'const override', ["return 15;"])
        assert len(functionText) == 2
        assert functionText[0] == '        [[nodiscard]] int myTest(int foo, size_t* moo) const override\n'
        assert functionText[1] == '        {return 15;}\n'

    def test26DeclareFunctionWithNoCommentInlineMultiLine(self):
        """!
        @brief Test the _declareFunctionWithDecorations method, no comment inline code
        """
        helper = GenerateCppFileHelper()
        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "return list", ParamRetDict.typeModList)

        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))

        inlineCode =["std::list<int> retvar;",
                     "retvar.push_back(15);",
                     "retvar.push_back(25);",
                     "return retvar;"]

        functionText = helper._declareFunctionWithDecorations("myTest", "My test function", genParamList, genRetDict,
                                                              8, True, "[[nodiscard]]", 'const override', inlineCode)
        assert len(functionText) == 7
        assert functionText[0] == '        [[nodiscard]] std::list<int> myTest(int foo, size_t* moo) const override\n'
        assert functionText[1] == '        {\n'
        assert functionText[2] == '            '+inlineCode[0]+'\n'
        assert functionText[3] == '            '+inlineCode[1]+'\n'
        assert functionText[4] == '            '+inlineCode[2]+'\n'
        assert functionText[5] == '            '+inlineCode[3]+'\n'
        assert functionText[6] == '        }\n'

    def test27EndFunction(self):
        """!
        @brief Test the _endFunction method
        """
        helper = GenerateCppFileHelper()
        functionText = helper._endFunction("myTest")
        assert functionText == '} // end of myTest()\n'

    def test28GenFileHeader(self):
        """!
        @brief Test the _generateGenericFileHeader method
        """
        helper = GenerateCppFileHelper()
        currentYear = datetime.now().year
        headerText = helper._generateGenericFileHeader("unittest", currentYear, "Me")
        copyrightMsg = "* Copyright (c) "+str(currentYear)+" Me"
        assert len(headerText) == 27
        assert headerText[0] == "/*------------------------------------------------------------------------------\n"
        assert headerText[1] == copyrightMsg+"\n"
        assert headerText[3] == "* MIT License\n"
        assert headerText[24] == "* This file was autogenerated by unittest do not edit\n"
        assert headerText[26] == "* ----------------------------------------------------------------------------*/\n"

        minText = helper._generateGenericFileHeader("unittest")
        assert len(minText) == 4
        assert minText[0] == "/*------------------------------------------------------------------------------\n"
        assert minText[1] == "* This file was autogenerated by unittest do not edit\n"
        assert minText[2] == "* \n"
        assert minText[3] == "* ----------------------------------------------------------------------------*/\n"

    def test29GenInclude(self):
        """!
        @brief Test the _genInclude method
        """
        helper = GenerateCppFileHelper()

        includeText = helper._genInclude("test.h")
        assert includeText == "#include \"test.h\"\n"

        includeText = helper._genInclude("<test>")
        assert includeText == "#include <test>\n"

    def test30GenIncludeBlock(self):
        """!
        @brief Test the _genIncludeBlock method
        """
        helper = GenerateCppFileHelper()
        includeList = ["<stdlib>", "<test>", "test.h", "foo.h"]
        includeText = helper._genIncludeBlock(includeList)
        assert len(includeText) == len(includeList) + 1
        assert includeText[0] == "// Includes\n"
        assert includeText[1] == "#include <stdlib>\n"
        assert includeText[2] == "#include <test>\n"
        assert includeText[3] == "#include \"test.h\"\n"
        assert includeText[4] == "#include \"foo.h\"\n"

    def test31GenOpenNamespace(self):
        """!
        @brief Test the _genNamespaceOpen method
        """
        helper = GenerateCppFileHelper()

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
        helper = GenerateCppFileHelper()

        testText = helper._genNamespaceClose("wonder")
        assert len(testText) == 1
        assert testText[0] == "}; // end of namespace wonder\n"

        testText = helper._genNamespaceClose("boy")
        assert len(testText) == 1
        assert testText[0] == "}; // end of namespace boy\n"

    def test33GenUsingNamespace(self):
        """!
        @brief Test the _genUsingNamespace method
        """
        helper = GenerateCppFileHelper()

        testText = helper._genUsingNamespace("wonder")
        assert len(testText) == 1
        assert testText[0] == "using namespace wonder;\n"

        testText = helper._genUsingNamespace("boy")
        assert len(testText) == 1
        assert testText[0] == "using namespace boy;\n"

    def test34GenClassOpen(self):
        """!
        @brief Test the _genClassOpen method, no decorations
        """
        helper = GenerateCppFileHelper()

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
        helper = GenerateCppFileHelper()

        testText = helper._genClassOpen("MyTestClassName", "My class description", "public MyBaseClass")
        assert len(testText) == 5
        assert testText[0] == "/**\n"
        assert testText[1] == " * @brief My class description\n"
        assert testText[2] == " */\n"
        assert testText[3] == "class MyTestClassName : public MyBaseClass\n"
        assert testText[4] == "{\n"

    def test36GenClassOpenDecoration(self):
        """!
        @brief Test the _genClassOpen method, with inheritence
        """
        helper = GenerateCppFileHelper()

        testText = helper._genClassOpen("MyTestClassName", "My class description", "public MyBaseClass", "final", 2)
        assert len(testText) == 5
        assert testText[0] == "  /**\n"
        assert testText[1] == "   * @brief My class description\n"
        assert testText[2] == "   */\n"
        assert testText[3] == "  class MyTestClassName final : public MyBaseClass\n"
        assert testText[4] == "  {\n"

    def test37GenClassClose(self):
        """!
        @brief Test the _genClassClose method, with inheritence
        """
        helper = GenerateCppFileHelper()

        testText = helper._genClassClose("MyTestClassName")
        assert len(testText) == 1
        assert testText[0] == "}; // end of MyTestClassName class\n"

        testText = helper._genClassClose("MyTestClassName", 2)
        assert len(testText) == 1
        assert testText[0] == "  }; // end of MyTestClassName class\n"

    def test38GenClassDefaultConDestrutor(self):
        """!
        @brief Test the _genClassDefaultConstructorDestructor method
        """
        helper = GenerateCppFileHelper()

        testText = helper._genClassDefaultConstructorDestructor("MyTestClassName")
        assert len(testText) == 46
        assert testText[0] == "        /**\n"
        assert testText[1] == "         * @brief Construct a new MyTestClassName object\n"
        assert testText[2] == "         * \n"
        assert testText[3] == "         */\n"
        assert testText[4] == "        MyTestClassName() = default;\n"
        assert testText[5] == "\n"
        assert testText[6] == "        /**\n"
        assert testText[7] == "         * @brief Copy constructor for a new MyTestClassName object\n"
        assert testText[8] == "         * \n"
        assert testText[9] == "         * @param other Reference to object to copy\n"
        assert testText[10] == "         * \n"
        assert testText[11] == "         */\n"
        assert testText[12] == "        MyTestClassName(const MyTestClassName& other) = default;\n"
        assert testText[13] == "\n"
        assert testText[14] == "        /**\n"
        assert testText[15] == "         * @brief Move constructor for a new MyTestClassName object\n"
        assert testText[16] == "         * \n"
        assert testText[17] == "         * @param other Reference to object to move\n"
        assert testText[18] == "         * \n"
        assert testText[19] == "         */\n"
        assert testText[20] == "        MyTestClassName(MyTestClassName&& other) = default;\n"
        assert testText[21] == "\n"
        assert testText[22] == "        /**\n"
        assert testText[23] == "         * @brief Equate constructor for a new MyTestClassName object\n"
        assert testText[24] == "         * \n"
        assert testText[25] == "         * @param other Reference to object to copy\n"
        assert testText[26] == "         * \n"
        assert testText[27] == "         * @return MyTestClassName& - *this\n"
        assert testText[28] == "         */\n"
        assert testText[29] == "        MyTestClassName& operator=(const MyTestClassName& other) = default;\n"
        assert testText[30] == "\n"
        assert testText[31] == "        /**\n"
        assert testText[32] == "         * @brief Equate move constructor for a new MyTestClassName object\n"
        assert testText[33] == "         * \n"
        assert testText[34] == "         * @param other Reference to object to move\n"
        assert testText[35] == "         * \n"
        assert testText[36] == "         * @return MyTestClassName& - *this\n"
        assert testText[37] == "         */\n"
        assert testText[38] == "        MyTestClassName& operator=(MyTestClassName&& other) = default;\n"
        assert testText[39] == "\n"
        assert testText[40] == "        /**\n"
        assert testText[41] == "         * @brief Destructor for MyTestClassName object\n"
        assert testText[42] == "         * \n"
        assert testText[43] == "         */\n"
        assert testText[44] == "        ~MyTestClassName() = default;\n"
        assert testText[45] == "\n"

    def test39GenClassDefaultConDestrutorNoDoxy(self):
        """!
        @brief Test the _genClassDefaultConstructorDestructor method, with no doxygen comments
        """
        helper = GenerateCppFileHelper()

        testText = helper._genClassDefaultConstructorDestructor("MyTestClassName", noDoxyCommentConstructor=True)
        assert len(testText) == 7
        assert testText[0] == "        MyTestClassName() = default;\n"
        assert testText[1] == "        MyTestClassName(const MyTestClassName& other) = default;\n"
        assert testText[2] == "        MyTestClassName(MyTestClassName&& other) = default;\n"
        assert testText[3] == "        MyTestClassName& operator=(const MyTestClassName& other) = default;\n"
        assert testText[4] == "        MyTestClassName& operator=(MyTestClassName&& other) = default;\n"
        assert testText[5] == "        ~MyTestClassName() = default;\n"
        assert testText[6] == "\n"

    def test40GenClassDefaultConDestrutorNoDoxyVirtualDestructor(self):
        """!
        @brief Test the _genClassDefaultConstructorDestructor method, with no doxygen comments, virtual destructor
        """
        helper = GenerateCppFileHelper()

        testText = helper._genClassDefaultConstructorDestructor("MyTestClassName", virtualDestructor=True, noDoxyCommentConstructor=True)
        assert len(testText) == 7
        assert testText[0] == "        MyTestClassName() = default;\n"
        assert testText[1] == "        MyTestClassName(const MyTestClassName& other) = default;\n"
        assert testText[2] == "        MyTestClassName(MyTestClassName&& other) = default;\n"
        assert testText[3] == "        MyTestClassName& operator=(const MyTestClassName& other) = default;\n"
        assert testText[4] == "        MyTestClassName& operator=(MyTestClassName&& other) = default;\n"
        assert testText[5] == "        virtual ~MyTestClassName() = default;\n"
        assert testText[6] == "\n"

    def test41GenClassDefaultConDestrutorNoDoxyNoCopy(self):
        """!
        @brief Test the _genClassDefaultConstructorDestructor method, with no doxycomment, no copy
        """
        helper = GenerateCppFileHelper()

        testText = helper._genClassDefaultConstructorDestructor("MyTestClassName", noDoxyCommentConstructor=True, noCopy=True)
        assert len(testText) == 7
        assert testText[0] == "        MyTestClassName() = default;\n"
        assert testText[1] == "        MyTestClassName(const MyTestClassName& other) = delete;\n"
        assert testText[2] == "        MyTestClassName(MyTestClassName&& other) = delete;\n"
        assert testText[3] == "        MyTestClassName& operator=(const MyTestClassName& other) = delete;\n"
        assert testText[4] == "        MyTestClassName& operator=(MyTestClassName&& other) = delete;\n"
        assert testText[5] == "        ~MyTestClassName() = default;\n"
        assert testText[6] == "\n"

    def test42GenClassDefaultConDestrutorNoDoxyNoCopy(self):
        """!
        @brief Test the _genClassDefaultConstructorDestructor method, with virtual destructor, no doxycomment, no copy
        """
        helper = GenerateCppFileHelper()

        testText = helper._genClassDefaultConstructorDestructor("MyTestClassName", 6, True, True, True)
        assert len(testText) == 7
        assert testText[0] == "      MyTestClassName() = default;\n"
        assert testText[1] == "      MyTestClassName(const MyTestClassName& other) = delete;\n"
        assert testText[2] == "      MyTestClassName(MyTestClassName&& other) = delete;\n"
        assert testText[3] == "      MyTestClassName& operator=(const MyTestClassName& other) = delete;\n"
        assert testText[4] == "      MyTestClassName& operator=(MyTestClassName&& other) = delete;\n"
        assert testText[5] == "      virtual ~MyTestClassName() = default;\n"
        assert testText[6] == "\n"

    def test43DeclareStructEmptyList(self):
        """!
        @brief Test the _declareStructure method, No decorations, empty list
        """
        helper = GenerateCppFileHelper()

        varList = []
        testText = helper._declareStructure("MyTestStructName", varList, 0, "Test structure")
        assert len(testText) == 6
        assert testText[0] == "/**\n"
        assert testText[1] == " * @brief Test structure\n"
        assert testText[2] == " */\n"
        assert testText[3] == "structure MyTestStructName\n"
        assert testText[4] == "{\n"
        assert testText[5] == "};\n"

    def test44DeclareStruct(self):
        """!
        @brief Test the _declareStructure method, No decorations
        """
        helper = GenerateCppFileHelper()

        member1 = ParamRetDict.buildParamDictWithMod("foo", "integer", "Test integer", 0)
        member2 = ParamRetDict.buildParamDictWithMod("moo", "unsigned", "Test unsigned", 0)
        varList = [member1, member2]
        testText = helper._declareStructure("MyTestStructName", varList, 0, "Test structure")
        assert len(testText) == 8
        assert testText[0] == "/**\n"
        assert testText[1] == " * @brief Test structure\n"
        assert testText[2] == " */\n"
        assert testText[3] == "structure MyTestStructName\n"
        assert testText[4] == "{\n"
        assert testText[5] == "    int foo;                                                //!< Test integer\n"
        assert testText[6] == "    unsigned moo;                                           //!< Test unsigned\n"
        assert testText[7] == "};\n"

    def test45DeclareStructWithDecorations(self):
        """!
        @brief Test the _declareStructure method, No decorations
        """
        helper = GenerateCppFileHelper()

        member1 = ParamRetDict.buildParamDictWithMod("foo", "integer", "Test integer", 0)
        member2 = ParamRetDict.buildParamDictWithMod("moo", "unsigned", "Test unsigned", 0)
        varList = [member1, member2]
        testText = helper._declareStructure("MyTestStructName", varList, 0, "Test structure", "public", "const")
        assert len(testText) == 8
        assert testText[0] == "/**\n"
        assert testText[1] == " * @brief Test structure\n"
        assert testText[2] == " */\n"
        assert testText[3] == "public structure MyTestStructName\n"
        assert testText[4] == "{\n"
        assert testText[5] == "    int foo;                                                //!< Test integer\n"
        assert testText[6] == "    unsigned moo;                                           //!< Test unsigned\n"
        assert testText[7] == "} const;\n"

    def test46DeclareVariable(self):
        """!
        @brief Test the _declareVarStatment method
        """
        helper = GenerateCppFileHelper()
        member1 = ParamRetDict.buildParamDictWithMod("foo", "integer", "Test integer", 0)
        member2 = ParamRetDict.buildParamDictWithMod("moo", "unsigned", "Test unsigned", 0)
        member3 = ParamRetDict.buildParamDictWithMod("goo", "string", "Test string", 0)

        testText = helper._declareVarStatment(member1, 30)
        assert testText == "int foo;                      //!< Test integer\n"

        testText = helper._declareVarStatment(member2, 32)
        assert testText == "unsigned moo;                   //!< Test unsigned\n"

        testText = helper._declareVarStatment(member3, 10)
        assert testText == "std::string goo; //!< Test string\n"

        testText = helper._declareVarStatment(member2, -1)
        assert testText == "unsigned moo;\n"

    def test47AddListEntry(self):
        """!
        @brief Test the _genAddListStatment method
        """
        helper = GenerateCppFileHelper()
        testText = helper._genAddListStatment("testList", "number", False)
        assert testText == "testList.emplace_back(number);"
        testText = helper._genAddListStatment("testList", "5", False)
        assert testText == "testList.emplace_back(5);"

        testText = helper._genAddListStatment("testList", "text", True)
        assert testText == "testList.emplace_back(\"text\");"
        testText = helper._genAddListStatment("testList", "AU", True)
        assert testText == "testList.emplace_back(\"AU\");"

    def test48GenerateReturn(self):
        """!
        @brief Test the _genReturnStatment method
        """
        helper = GenerateCppFileHelper()
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
        helper = GenerateCppFileHelper()
        retDict = ParamRetDict.buildReturnDictWithMod("integer", "return value", 0)
        paramList = [ParamRetDict.buildParamDictWithMod("foo", "unsigned", "Foo input", 0)]
        testText = helper._defineFunctionWithDecorations("MyDefineFunc", "Brief description", paramList, retDict)
        assert len(testText) == 8
        assert testText[0] == "/**\n"
        assert testText[1] == " * @brief Brief description\n"
        assert testText[2] == " * \n"
        assert testText[3] == " * @param foo Foo input\n"
        assert testText[4] == " * \n"
        assert testText[5] == " * @return int - return value\n"
        assert testText[6] == " */\n"
        assert testText[7] == "int MyDefineFunc(unsigned foo)\n"

    def test50DefineFunctionWithPreDecoration(self):
        """!
        @brief Test the _defineFunctionWithDecorations method, with prefix
        """
        helper = GenerateCppFileHelper()
        retDict = ParamRetDict.buildReturnDictWithMod("integer", "return value", 0)
        paramList = [ParamRetDict.buildParamDictWithMod("foo", "unsigned", "Foo input", 0)]
        testText = helper._defineFunctionWithDecorations("MyDefineFunc", "Brief description", paramList, retDict, False, "static")
        assert len(testText) == 8
        assert testText[0] == "/**\n"
        assert testText[1] == " * @brief Brief description\n"
        assert testText[2] == " * \n"
        assert testText[3] == " * @param foo Foo input\n"
        assert testText[4] == " * \n"
        assert testText[5] == " * @return int - return value\n"
        assert testText[6] == " */\n"
        assert testText[7] == "static int MyDefineFunc(unsigned foo)\n"

    def test51DefineFunctionWithPostDecoration(self):
        """!
        @brief Test the _defineFunctionWithDecorations method, with postfix
        """
        helper = GenerateCppFileHelper()
        retDict = ParamRetDict.buildReturnDictWithMod("integer", "return value", 0)
        paramList = [ParamRetDict.buildParamDictWithMod("foo", "unsigned", "Foo input", 0)]
        testText = helper._defineFunctionWithDecorations("MyDefineFunc", "Brief description", paramList, retDict, postfixDecaration="const")
        assert len(testText) == 8
        assert testText[0] == "/**\n"
        assert testText[1] == " * @brief Brief description\n"
        assert testText[2] == " * \n"
        assert testText[3] == " * @param foo Foo input\n"
        assert testText[4] == " * \n"
        assert testText[5] == " * @return int - return value\n"
        assert testText[6] == " */\n"
        assert testText[7] == "int MyDefineFunc(unsigned foo) const\n"

    def test52DefineFunctionWithPrePostDecoration(self):
        """!
        @brief Test the _defineFunctionWithDecorations method, with prefix and postfix
        """
        helper = GenerateCppFileHelper()
        retDict = ParamRetDict.buildReturnDictWithMod("integer", "return value", 0)
        paramList = [ParamRetDict.buildParamDictWithMod("foo", "unsigned", "Foo input", 0)]
        testText = helper._defineFunctionWithDecorations("MyDefineFunc", "Brief description", paramList, retDict,
                                                         prefixDecaration="static", postfixDecaration="const")
        assert len(testText) == 8
        assert testText[0] == "/**\n"
        assert testText[1] == " * @brief Brief description\n"
        assert testText[2] == " * \n"
        assert testText[3] == " * @param foo Foo input\n"
        assert testText[4] == " * \n"
        assert testText[5] == " * @return int - return value\n"
        assert testText[6] == " */\n"
        assert testText[7] == "static int MyDefineFunc(unsigned foo) const\n"

    def test53DefineFunctionNoComment(self):
        """!
        @brief Test the _defineFunctionWithDecorations method, with no comment
        """
        helper = GenerateCppFileHelper()
        retDict = ParamRetDict.buildReturnDictWithMod("integer", "return value", 0)
        paramList = [ParamRetDict.buildParamDictWithMod("foo", "unsigned", "Foo input", 0)]
        testText = helper._defineFunctionWithDecorations("MyDefineFunc", "Brief description", paramList, retDict, True)
        assert len(testText) == 1
        assert testText[0] == "int MyDefineFunc(unsigned foo)\n"

    def test54DefineFunctionEmptyParamList(self):
        """!
        @brief Test the _defineFunctionWithDecorations method, with empty param list
        """
        helper = GenerateCppFileHelper()
        retDict = ParamRetDict.buildReturnDictWithMod("integer", "return value", 0)
        testText = helper._defineFunctionWithDecorations("MyDefineFunc", "Brief description", [], retDict, True)
        assert len(testText) == 1
        assert testText[0] == "int MyDefineFunc()\n"

    def test55GenClassOpenNoDescrtiption(self):
        """!
        @brief Test the _genClassOpen method, with no description
        """
        helper = GenerateCppFileHelper()

        testText = helper._genClassOpen("MyTestClassName", None, "public MyBaseClass", "final", 2)
        assert len(testText) == 2
        assert testText[0] == "  class MyTestClassName final : public MyBaseClass\n"
        assert testText[1] == "  {\n"
