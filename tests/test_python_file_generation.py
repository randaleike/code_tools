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
from code_tools_grocsoftware.python_gen.file_gen_base import GeneratePythonFileHelper

class TestUnittest01CppFilehelper:
    """!
    @brief Unit test for the GeneratePythonFileHelper class
    """
    def test01Constructor(self):
        """!
        @brief Test the constructor
        """
        helper = GeneratePythonFileHelper()

        assert helper.copyrightGenerator is not None
        assert helper.eula is not None
        assert helper.doxyCommentGen is not None
        assert helper.headerCommentGen is not None
        assert helper.levelTabSize == 4

        assert len(list(helper.typeXlationDict.keys())) == 7
        assert helper.typeXlationDict['string'] == "str"
        assert helper.typeXlationDict['text'] == "str"
        assert helper.typeXlationDict['size'] == "int"
        assert helper.typeXlationDict['integer'] == "int"
        assert helper.typeXlationDict['unsigned'] == "int"
        assert helper.typeXlationDict['structure'] == "dict"
        assert helper.typeXlationDict['tuple'] == "tuple"

        helper = GeneratePythonFileHelper("GNU_V11")

        assert helper.copyrightGenerator is not None
        assert helper.eula is not None
        assert helper.doxyCommentGen is not None
        assert helper.headerCommentGen is not None
        assert helper.levelTabSize == 4

        assert len(list(helper.typeXlationDict.keys())) == 7
        assert helper.typeXlationDict['string'] == "str"
        assert helper.typeXlationDict['text'] == "str"
        assert helper.typeXlationDict['size'] == "int"
        assert helper.typeXlationDict['integer'] == "int"
        assert helper.typeXlationDict['unsigned'] == "int"
        assert helper.typeXlationDict['structure'] == "dict"
        assert helper.typeXlationDict['tuple'] == "tuple"

    def test02DeclareTypeBase(self):
        """!
        @brief Test the _declareType method, no modification
        """
        helper = GeneratePythonFileHelper()

        # Test the xlate path
        assert helper._declareType('string') == "str"
        assert helper._declareType('text') == "str"
        assert helper._declareType('size') == "int"
        assert helper._declareType('integer') == "int"
        assert helper._declareType('unsigned') == "int"
        assert helper._declareType('structure') == "dict"
        assert helper._declareType('tuple') == "tuple"

        # Test the non-xlate pathGN
        assert helper._declareType('MyClass') == "MyClass"

    def test03DeclareTypePtr(self):
        """!
        @brief Test the _declareType method, pointer modification
        """
        helper = GeneratePythonFileHelper()

        # Test the xlate path
        assert helper._declareType('string', ParamRetDict.typeModPtr) == "str"
        assert helper._declareType('text', ParamRetDict.typeModPtr) == "str"
        assert helper._declareType('size', ParamRetDict.typeModPtr) == "int"
        assert helper._declareType('integer', ParamRetDict.typeModPtr) == "int"
        assert helper._declareType('unsigned', ParamRetDict.typeModPtr) == "int"
        assert helper._declareType('structure', ParamRetDict.typeModPtr) == "dict"
        assert helper._declareType('tuple', ParamRetDict.typeModPtr) == "tuple"

    def test04DeclareTypeRef(self):
        """!
        @brief Test the _declareType method, pointer modification
        """
        helper = GeneratePythonFileHelper()

        # Test the xlate path
        assert helper._declareType('string', ParamRetDict.typeModRef) == "str"
        assert helper._declareType('text', ParamRetDict.typeModRef) == "str"
        assert helper._declareType('size', ParamRetDict.typeModRef) == "int"
        assert helper._declareType('integer', ParamRetDict.typeModRef) == "int"
        assert helper._declareType('unsigned', ParamRetDict.typeModRef) == "int"
        assert helper._declareType('structure', ParamRetDict.typeModRef) == "dict"
        assert helper._declareType('tuple', ParamRetDict.typeModRef) == "tuple"

    def test05DeclareTypeList(self):
        """!
        @brief Test the _declareType method, list modification
        """
        helper = GeneratePythonFileHelper()

        # Test the xlate path
        assert helper._declareType('string', ParamRetDict.typeModList) == "list"
        assert helper._declareType('text', ParamRetDict.typeModList) == "list"
        assert helper._declareType('size', ParamRetDict.typeModList) == "list"
        assert helper._declareType('integer', ParamRetDict.typeModList) == "list"
        assert helper._declareType('unsigned', ParamRetDict.typeModList) == "list"
        assert helper._declareType('structure', ParamRetDict.typeModList) == "list"
        assert helper._declareType('tuple', ParamRetDict.typeModList) == "list"

    def test06DeclareTypeListPtr(self):
        """!
        @brief Test the _declareType method, list and pointer modification
        """
        helper = GeneratePythonFileHelper()

        # Test the xlate path
        typemod = ParamRetDict.typeModList | ParamRetDict.typeModPtr
        assert helper._declareType('string', typemod) == "list"
        assert helper._declareType('text', typemod) == "list"
        assert helper._declareType('size', typemod) == "list"
        assert helper._declareType('integer', typemod) == "list"
        assert helper._declareType('unsigned', typemod) == "list"
        assert helper._declareType('structure', typemod) == "list"
        assert helper._declareType('tuple', typemod) == "list"

    def test07DeclareTypeListRef(self):
        """!
        @brief Test the _declareType method, list and reference modification
        """
        helper = GeneratePythonFileHelper()

        # Test the xlate path
        typemod = ParamRetDict.typeModList | ParamRetDict.typeModRef
        assert helper._declareType('string', typemod) == "list"
        assert helper._declareType('text', typemod) == "list"
        assert helper._declareType('size', typemod) == "list"
        assert helper._declareType('integer', typemod) == "list"
        assert helper._declareType('unsigned', typemod) == "list"
        assert helper._declareType('structure', typemod) == "list"
        assert helper._declareType('tuple', typemod) == "list"

    def test08DeclareTypeArray(self):
        """!
        @brief Test the _declareType method, array modification
        """
        helper = GeneratePythonFileHelper()

        # Test the xlate path
        assert helper._declareType('string', 5 << ParamRetDict.typeModArrayShift) == "list"
        assert helper._declareType('text', 7 << ParamRetDict.typeModArrayShift) == "list"
        assert helper._declareType('size', 10 << ParamRetDict.typeModArrayShift) == "list"
        assert helper._declareType('integer', 20 << ParamRetDict.typeModArrayShift) == "list"
        assert helper._declareType('unsigned', 13 << ParamRetDict.typeModArrayShift) == "list"
        assert helper._declareType('structure', 12 << ParamRetDict.typeModArrayShift) == "list"
        assert helper._declareType('tuple', 14 << ParamRetDict.typeModArrayShift) == "list"

    def test09DeclareTypeArrayPtr(self):
        """!
        @brief Test the _declareType method, array and pointer modification
        """
        helper = GeneratePythonFileHelper()

        # Test the xlate path
        typemod = (8 << ParamRetDict.typeModArrayShift) | ParamRetDict.typeModPtr
        assert helper._declareType('string', typemod) == "list"
        assert helper._declareType('text', typemod) == "list"
        assert helper._declareType('size', typemod) == "list"
        assert helper._declareType('integer', typemod) == "list"
        assert helper._declareType('unsigned', typemod) == "list"
        assert helper._declareType('structure', typemod) == "list"
        assert helper._declareType('tuple', typemod) == "list"

    def test10DeclareTypeArrayRef(self):
        """!
        @brief Test the _declareType method, array and reference modification
        """
        helper = GeneratePythonFileHelper()

        # Test the xlate path
        typemod = (8 << ParamRetDict.typeModArrayShift) | ParamRetDict.typeModRef
        assert helper._declareType('string', typemod) == "list"
        assert helper._declareType('text', typemod) == "list"
        assert helper._declareType('size', typemod) == "list"
        assert helper._declareType('integer', typemod) == "list"
        assert helper._declareType('unsigned', typemod) == "list"
        assert helper._declareType('structure', typemod) == "list"
        assert helper._declareType('tuple', typemod) == "list"

    def test11DeclareTypeUndef(self):
        """!
        @brief Test the _declareType method, all with undef modification
        """
        helper = GeneratePythonFileHelper()

        # Test the xlate path
        assert helper._declareType('string', ParamRetDict.typeModUndef) == "str|None"

        typemod = ParamRetDict.typeModUndef | ParamRetDict.typeModPtr
        assert helper._declareType('string', typemod) == "str|None"

        typemod = ParamRetDict.typeModUndef | ParamRetDict.typeModRef
        assert helper._declareType('string', typemod) == "str|None"

        typemod = (8 << ParamRetDict.typeModArrayShift) | ParamRetDict.typeModUndef
        assert helper._declareType('string', typemod) == "list|None"

        typemod = ParamRetDict.typeModUndef | ParamRetDict.typeModList
        assert helper._declareType('string', typemod) == "list|None"

        typemod = (25 << ParamRetDict.typeModArrayShift) | ParamRetDict.typeModUndef | ParamRetDict.typeModPtr
        assert helper._declareType('string', typemod) == "list|None"

        typemod = (7 << ParamRetDict.typeModArrayShift) | ParamRetDict.typeModUndef | ParamRetDict.typeModRef
        assert helper._declareType('string', typemod) == "list|None"

        typemod = ParamRetDict.typeModUndef | ParamRetDict.typeModList
        assert helper._declareType('string', typemod) == "list|None"

        typemod = ParamRetDict.typeModUndef | ParamRetDict.typeModList | ParamRetDict.typeModPtr
        assert helper._declareType('string', typemod) == "list|None"

        typemod = ParamRetDict.typeModUndef | ParamRetDict.typeModList | ParamRetDict.typeModRef
        assert helper._declareType('string', typemod) == "list|None"

    def test12XlateParamList(self):
        """!
        @brief Test the _xlateParams method
        """
        helper = GeneratePythonFileHelper()
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
        assert ParamRetDict.getParamType(xlateList[1]) == "int"
        assert ParamRetDict.getParamDesc(xlateList[1]) == ParamRetDict.getParamDesc(genParamList[1])
        assert ParamRetDict.getParamTypeMod(xlateList[1]) == 0

        assert ParamRetDict.getParamName(xlateList[2]) == ParamRetDict.getParamName(genParamList[2])
        assert ParamRetDict.getParamType(xlateList[2]) == "list"
        assert ParamRetDict.getParamDesc(xlateList[2]) == ParamRetDict.getParamDesc(genParamList[2])
        assert ParamRetDict.getParamTypeMod(xlateList[2]) == 0

    def test13XlateParamEmptyList(self):
        """!
        @brief Test the _xlateParams method, empty list input
        """
        helper = GeneratePythonFileHelper()
        genParamList = []
        xlateList = helper._xlateParams(genParamList)
        assert len(xlateList) == 0

    def test14XlateRetDict(self):
        """!
        @brief Test the _xlateReturnDict method
        """
        helper = GeneratePythonFileHelper()
        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "myint", 0)

        xlatedRet = helper._xlateReturnDict(genRetDict)
        assert ParamRetDict.getReturnType(xlatedRet) == "int"
        assert ParamRetDict.getParamDesc(xlatedRet) == ParamRetDict.getParamDesc(genRetDict)
        assert ParamRetDict.getParamTypeMod(genRetDict) == 0

    def test15XlateRetDictNone(self):
        """!
        @brief Test the _xlateReturnDict method, with no input
        """
        helper = GeneratePythonFileHelper()
        xlatedRet = helper._xlateReturnDict(None)
        assert xlatedRet is None

    def test16GenReturnType(self):
        """!
        @brief Test the _genFunctionRetType method
        """
        helper = GeneratePythonFileHelper()

        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "myint", 0)
        returnText = helper._genFunctionRetType(genRetDict)
        assert returnText == " -> int:"

        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "myint", ParamRetDict.typeModList)
        returnText = helper._genFunctionRetType(genRetDict)
        assert returnText == " -> list:"

    def test17GenReturnType(self):
        """!
        @brief Test the _genFunctionRetType method, with none input
        """
        helper = GeneratePythonFileHelper()

        returnText = helper._genFunctionRetType(None)
        assert returnText == ":"

    def test18GenFunctionParams(self):
        """!
        @brief Test the _genFunctionParams method
        """
        helper = GeneratePythonFileHelper()
        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))
        genParamList.append(ParamRetDict.buildParamDictWithMod("goo", "string", "mystr", ParamRetDict.typeModList))

        returnText = helper._genFunctionParams(genParamList)
        assert returnText == "(foo:int, moo:int, goo:list)"

    def test19GenFunctionParamsEmpty(self):
        """!
        @brief Test the _genFunctionParams method, empty list
        """
        helper = GeneratePythonFileHelper()
        genParamList = []
        returnText = helper._genFunctionParams(genParamList)
        assert returnText == "()"

    def test20DeclareFunction(self):
        """!
        @brief Test the _declareFunctionWithDecorations method, no decorations
        """
        helper = GeneratePythonFileHelper()
        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "return int", 0)

        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))

        functionText = helper._declareFunctionWithDecorations("myTest", "My test function", genParamList, genRetDict)
        assert len(functionText) == 10
        assert functionText[0] == '    def myTest(foo:int, moo:int) -> int:\n'
        assert functionText[1] == '        """!\n'
        assert functionText[2] == '          @brief My test function\n'
        assert functionText[3] == '          \n'
        assert functionText[4] == '          @param foo {int} myint\n'
        assert functionText[5] == '          @param moo {int} mysize\n'
        assert functionText[6] == '          \n'
        assert functionText[7] == '          @return int - return int\n'
        assert functionText[8] == '        """\n'
        assert functionText[9] == '        ## @todo Implement code\n'

    def test21DeclareFunctionWithPrefix(self):
        """!
        @brief Test the _declareFunctionWithDecorations method, prefix decoration
        """
        helper = GeneratePythonFileHelper()
        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "return int", 0)

        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))

        functionText = helper._declareFunctionWithDecorations("myTest", "My test function", genParamList, genRetDict, 8, prefixDecaration='@staticmethod')
        assert len(functionText) == 11
        assert functionText[0] == '        @staticmethod\n'
        assert functionText[1] == '        def myTest(foo:int, moo:int) -> int:\n'
        assert functionText[2] == '            """!\n'
        assert functionText[3] == '              @brief My test function\n'
        assert functionText[4] == '              \n'
        assert functionText[5] == '              @param foo {int} myint\n'
        assert functionText[6] == '              @param moo {int} mysize\n'
        assert functionText[7] == '              \n'
        assert functionText[8] == '              @return int - return int\n'
        assert functionText[9] == '            """\n'
        assert functionText[10] == '            ## @todo Implement code\n'

    def test22DeclareFunctionWithPostfix(self):
        """!
        @brief Test the _declareFunctionWithDecorations method, postfix decoration
        """
        helper = GeneratePythonFileHelper()
        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "return int", 0)

        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))

        functionText = helper._declareFunctionWithDecorations("myTest", "My test function", genParamList, genRetDict, 8, postfixDecaration='const override')
        assert len(functionText) == 10
        assert functionText[0] == '        def myTest(foo:int, moo:int) -> int:\n'
        assert functionText[1] == '            """!\n'
        assert functionText[2] == '              @brief My test function\n'
        assert functionText[3] == '              \n'
        assert functionText[4] == '              @param foo {int} myint\n'
        assert functionText[5] == '              @param moo {int} mysize\n'
        assert functionText[6] == '              \n'
        assert functionText[7] == '              @return int - return int\n'
        assert functionText[8] == '            """\n'
        assert functionText[9] == '            ## @todo Implement code\n'


    def test23DeclareFunctionWithPreAndPostfix(self):
        """!
        @brief Test the _declareFunctionWithDecorations method, prefix, postfix decoration
        """
        helper = GeneratePythonFileHelper()
        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "return int", 0)

        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))

        functionText = helper._declareFunctionWithDecorations("myTest", "My test function", genParamList, genRetDict,
                                                              8, prefixDecaration="@staticmethod", postfixDecaration='const override')
        assert len(functionText) == 11
        assert functionText[0] == '        @staticmethod\n'
        assert functionText[1] == '        def myTest(foo:int, moo:int) -> int:\n'
        assert functionText[2] == '            """!\n'
        assert functionText[3] == '              @brief My test function\n'
        assert functionText[4] == '              \n'
        assert functionText[5] == '              @param foo {int} myint\n'
        assert functionText[6] == '              @param moo {int} mysize\n'
        assert functionText[7] == '              \n'
        assert functionText[8] == '              @return int - return int\n'
        assert functionText[9] == '            """\n'
        assert functionText[10] == '            ## @todo Implement code\n'

    def test24DeclareFunctionWithPreAndPostfixNoComment(self):
        """!
        @brief Test the _declareFunctionWithDecorations method, prefix, postfix decoration, no comment
        """
        helper = GeneratePythonFileHelper()
        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "return int", 0)

        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))

        functionText = helper._declareFunctionWithDecorations("myTest", "My test function", genParamList, genRetDict,
                                                              8, True, "@staticmethod", 'const override')
        assert len(functionText) == 3
        assert functionText[0] == '        @staticmethod\n'
        assert functionText[1] == '        def myTest(foo:int, moo:int) -> int:\n'
        assert functionText[2] == '            ## @todo Implement code\n'

    def test25DeclareFunctionWithNoCommentInlineSingleLine(self):
        """!
        @brief Test the _declareFunctionWithDecorations method, no comment inline code
        """
        helper = GeneratePythonFileHelper()
        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "return int", 0)

        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))

        functionText = helper._declareFunctionWithDecorations("myTest", "My test function", genParamList, genRetDict,
                                                              8, True, "@staticmethod", 'const override', ["return 15"])
        assert len(functionText) == 3
        assert functionText[0] == '        @staticmethod\n'
        assert functionText[1] == '        def myTest(foo:int, moo:int) -> int:\n'
        assert functionText[2] == '            return 15\n'

    def test26DeclareFunctionWithNoCommentInlineMultiLine(self):
        """!
        @brief Test the _declareFunctionWithDecorations method, no comment inline code
        """
        helper = GeneratePythonFileHelper()
        genRetDict = ParamRetDict.buildReturnDictWithMod("integer", "return list", ParamRetDict.typeModList)

        genParamList = []
        genParamList.append(ParamRetDict.buildParamDictWithMod("foo", "integer", "myint", 0))
        genParamList.append(ParamRetDict.buildParamDictWithMod("moo", "size", "mysize", ParamRetDict.typeModPtr))

        inlineCode =["retvar = []",
                     "retvar.append(15)",
                     "retvar.append(25)",
                     "return retvar"]

        functionText = helper._declareFunctionWithDecorations("myTest", "My test function", genParamList, genRetDict,
                                                              8, True, inlinecode = inlineCode)
        assert len(functionText) == 5
        assert functionText[0] == '        def myTest(foo:int, moo:int) -> list:\n'
        assert functionText[1] == '            '+inlineCode[0]+'\n'
        assert functionText[2] == '            '+inlineCode[1]+'\n'
        assert functionText[3] == '            '+inlineCode[2]+'\n'
        assert functionText[4] == '            '+inlineCode[3]+'\n'

    def test27EndFunction(self):
        """!
        @brief Test the _endFunction method
        """
        helper = GeneratePythonFileHelper()
        functionText = helper._endFunction("myTest")
        assert functionText == '# end of function myTest\n'

    def test28GenFileHeader(self):
        """!
        @brief Test the _generateGenericFileHeader method
        """
        helper = GeneratePythonFileHelper()
        currentYear = datetime.now().year
        headerText = helper._generateGenericFileHeader("unittest", currentYear, "Me")
        copyrightMsg = "# Copyright (c) "+str(currentYear)+" Me"
        assert len(headerText) == 27
        assert headerText[0] == "#-------------------------------------------------------------------------------\n"
        assert headerText[1] == copyrightMsg+"\n"
        assert headerText[3] == "# MIT License\n"
        assert headerText[24] == "# This file was autogenerated by unittest do not edit\n"
        assert headerText[26] == "#-------------------------------------------------------------------------------\n"

        minText = helper._generateGenericFileHeader("unittest")
        assert len(minText) == 4
        assert minText[0] == "#-------------------------------------------------------------------------------\n"
        assert minText[1] == "# This file was autogenerated by unittest do not edit\n"
        assert minText[2] == "# \n"
        assert minText[3] == "#-------------------------------------------------------------------------------\n"

    def test29GenInclude(self):
        """!
        @brief Test the _genImport method
        """
        helper = GeneratePythonFileHelper()

        includeText = helper._genImport("MyImportClass", "importModuleName")
        assert includeText == "from importModuleName import MyImportClass\n"

        includeText = helper._genImport("os")
        assert includeText == "import os\n"

    def test30GenIncludeBlock(self):
        """!
        @brief Test the _genImportBlock method
        """
        helper = GeneratePythonFileHelper()
        includeList = [("re", None), ("datetime", "datetime"), ("MyImportClass", "importModuleName")]
        includeText = helper._genImportBlock(includeList)
        assert len(includeText) == len(includeList) + 1
        assert includeText[0] == "// Imports\n"
        assert includeText[1] == "import re\n"
        assert includeText[2] == "from datetime import datetime\n"
        assert includeText[3] == "from importModuleName import MyImportClass\n"

    def test31GenOpenNamespace(self):
        """!
        @brief Test the _genNamespaceOpen method
        """
        helper = GeneratePythonFileHelper()

        testText = helper._genNamespaceOpen("wonder")
        assert len(testText) == 0

        testText = helper._genNamespaceOpen("boy")
        assert len(testText) == 0

    def test32GenCloseNamespace(self):
        """!
        @brief Test the _genNamespaceClose method
        """
        helper = GeneratePythonFileHelper()

        testText = helper._genNamespaceClose("wonder")
        assert len(testText) == 0

        testText = helper._genNamespaceClose("boy")
        assert len(testText) == 0

    def test33GenUsingNamespace(self):
        """!
        @brief Test the _genUsingNamespace method
        """
        helper = GeneratePythonFileHelper()

        testText = helper._genUsingNamespace("wonder")
        assert len(testText) == 0

        testText = helper._genUsingNamespace("boy")
        assert len(testText) == 0

    def test34GenClassOpen(self):
        """!
        @brief Test the _genClassOpen method, no decorations
        """
        helper = GeneratePythonFileHelper()

        testText = helper._genClassOpen("MyTestClassName", "My class description")
        assert len(testText) == 4
        assert testText[0] == "class MyTestClassName(object):\n"
        assert testText[1] == '    """!\n'
        assert testText[2] == "      @brief My class description\n"
        assert testText[3] == '    """\n'

    def test35GenClassOpenWithInheritence(self):
        """!
        @brief Test the _genClassOpen method, with inheritence
        """
        helper = GeneratePythonFileHelper()

        testText = helper._genClassOpen("MyTestClassName", "My class description", "MyBaseClass")
        assert len(testText) == 4
        assert testText[0] == "class MyTestClassName(MyBaseClass):\n"
        assert testText[1] == '    """!\n'
        assert testText[2] == "      @brief My class description\n"
        assert testText[3] == '    """\n'

    def test36GenClassOpenDecoration(self):
        """!
        @brief Test the _genClassOpen method, with decoration
        """
        helper = GeneratePythonFileHelper()

        testText = helper._genClassOpen("MyTestClassName", "My class description", "MyBaseClass", "final", 2)
        assert len(testText) == 4
        assert testText[0] == "  class MyTestClassName(MyBaseClass):\n"
        assert testText[1] == '      """!\n'
        assert testText[2] == "        @brief My class description\n"
        assert testText[3] == '      """\n'

    def test37GenClassClose(self):
        """!
        @brief Test the _genClassClose method, with inheritence
        """
        helper = GeneratePythonFileHelper()

        testText = helper._genClassClose("MyTestClassName")
        assert len(testText) == 1
        assert testText[0] == "# end of MyTestClassName class\n"

        testText = helper._genClassClose("MyTestClassName", 2)
        assert len(testText) == 1
        assert testText[0] == "  # end of MyTestClassName class\n"

    def test38GenClassDefaultConstrutor(self):
        """!
        @brief Test the _genClassDefaultConstructor method
        """
        helper = GeneratePythonFileHelper()

        testText = helper._genClassDefaultConstructor("MyTestClassName")
        assert len(testText) == 6
        assert testText[0] == "    def __init__():\n"
        assert testText[1] == '        """!\n'
        assert testText[2] == "          @brief Construct a new MyTestClassName object\n"
        assert testText[3] == '          \n'
        assert testText[4] == '        """\n'
        assert testText[5] == '    \n'

    def test39GenClassDefaultConDestrutorNoDoxy(self):
        """!
        @brief Test the _genClassDefaultConstructor method, with no doxygen comments
        """
        helper = GeneratePythonFileHelper()

        testText = helper._genClassDefaultConstructor("MyTestClassName", noDoxyCommentConstructor=True)
        assert len(testText) == 2
        assert testText[0] == "    def __init__():\n"
        assert testText[1] == '    \n'

    def test40DeclareStructEmptyList(self):
        """!
        @brief Test the _declareStructure method, No decorations, empty list
        """
        helper = GeneratePythonFileHelper()

        varList = []
        testText = helper._declareStructure("MyTestStructName", varList, 0, "Test structure")
        assert len(testText) == 5
        assert testText[0] == "class MyTestStructName(object):\n"
        assert testText[1] == '    """!\n'
        assert testText[2] == "      @brief Test structure\n"
        assert testText[3] == '    """\n'
        assert testText[4] == '# end of MyTestStructName class\n'

    def test41DeclareStruct(self):
        """!
        @brief Test the _declareStructure method, No decorations
        """
        helper = GeneratePythonFileHelper()

        member1 = ParamRetDict.buildParamDictWithMod("foo", "integer", "Test integer", 0)
        member2 = ParamRetDict.buildParamDictWithMod("moo", "unsigned", "Test unsigned", 0)
        varList = [member1, member2]
        testText = helper._declareStructure("MyTestStructName", varList, 0, "Test structure")
        assert len(testText) == 7
        assert testText[0] == "class MyTestStructName(object):\n"
        assert testText[1] == '    """!\n'
        assert testText[2] == "      @brief Test structure\n"
        assert testText[3] == '    """\n'
        assert testText[4] == "    ## Test integer\n    foo:int\n"
        assert testText[5] == "    ## Test unsigned\n    moo:int\n"
        assert testText[6] == '# end of MyTestStructName class\n'

    def test42DeclareVariable(self):
        """!
        @brief Test the _declareVarStatment method
        """
        helper = GeneratePythonFileHelper()
        member1 = ParamRetDict.buildParamDictWithMod("foo", "integer", "Test integer", 0)
        member2 = ParamRetDict.buildParamDictWithMod("moo", "unsigned", "Test unsigned", 0)
        member3 = ParamRetDict.buildParamDictWithMod("goo", "string", "Test string", 0)

        testText = helper._declareVarStatment(member1, 4)
        assert testText == "    ## Test integer\n    foo:int\n"

        testText = helper._declareVarStatment(member2, 8)
        assert testText == "        ## Test unsigned\n        moo:int\n"

        testText = helper._declareVarStatment(member3)
        assert testText == "## Test string\ngoo:str\n"

    def test43AddListEntry(self):
        """!
        @brief Test the _genAddListStatment method
        """
        helper = GeneratePythonFileHelper()
        testText = helper._genAddListStatment("testList", "number", False)
        assert testText == "testList.append(number)"
        testText = helper._genAddListStatment("testList", "5", False)
        assert testText == "testList.append(5)"

        testText = helper._genAddListStatment("testList", "text", True)
        assert testText == "testList.append(\"text\")"
        testText = helper._genAddListStatment("testList", "AU", True)
        assert testText == "testList.append(\"AU\")"

    def test44GenerateReturn(self):
        """!
        @brief Test the _genReturnStatment method
        """
        helper = GeneratePythonFileHelper()
        testText = helper._genReturnStatment("number", False)
        assert testText == "return number"
        testText = helper._genReturnStatment("5", False)
        assert testText == "return 5"

        testText = helper._genReturnStatment("text", True)
        assert testText == "return \"text\""
        testText = helper._genReturnStatment("AU", True)
        assert testText == "return \"AU\""

    def test49DefineFunction(self):
        """!
        @brief Test the _defineFunctionWithDecorations method, no decarations
        """
        helper = GeneratePythonFileHelper()
        retDict = ParamRetDict.buildReturnDictWithMod("integer", "return value", 0)
        paramList = [ParamRetDict.buildParamDictWithMod("foo", "unsigned", "Foo input", 0)]
        testText = helper._defineFunctionWithDecorations("MyDefineFunc", "Brief description", paramList, retDict)
        assert len(testText) == 8
        assert testText[0] == 'def MyDefineFunc(foo:int) -> int:\n'
        assert testText[1] == '    """!\n'
        assert testText[2] == '      @brief Brief description\n'
        assert testText[3] == '      \n'
        assert testText[4] == '      @param foo {int} Foo input\n'
        assert testText[5] == '      \n'
        assert testText[6] == '      @return int - return value\n'
        assert testText[7] == '    """\n'

    def test50DefineFunctionWithPreDecoration(self):
        """!
        @brief Test the _defineFunctionWithDecorations method, with prefix
        """
        helper = GeneratePythonFileHelper()
        retDict = ParamRetDict.buildReturnDictWithMod("integer", "return value", 0)
        paramList = [ParamRetDict.buildParamDictWithMod("foo", "unsigned", "Foo input", 0)]
        testText = helper._defineFunctionWithDecorations("MyDefineFunc", "Brief description", paramList, retDict, False, "@static")
        assert len(testText) == 9
        assert testText[0] == '@static\n'
        assert testText[1] == 'def MyDefineFunc(foo:int) -> int:\n'
        assert testText[2] == '    """!\n'
        assert testText[3] == '      @brief Brief description\n'
        assert testText[4] == '      \n'
        assert testText[5] == '      @param foo {int} Foo input\n'
        assert testText[6] == '      \n'
        assert testText[7] == '      @return int - return value\n'
        assert testText[8] == '    """\n'

    def test51DefineFunctionWithPostDecoration(self):
        """!
        @brief Test the _defineFunctionWithDecorations method, with postfix
        """
        helper = GeneratePythonFileHelper()
        retDict = ParamRetDict.buildReturnDictWithMod("integer", "return value", 0)
        paramList = [ParamRetDict.buildParamDictWithMod("foo", "unsigned", "Foo input", 0)]
        testText = helper._defineFunctionWithDecorations("MyDefineFunc", "Brief description", paramList, retDict, postfixDecaration="const")
        assert len(testText) == 8
        assert testText[0] == 'def MyDefineFunc(foo:int) -> int:\n'
        assert testText[1] == '    """!\n'
        assert testText[2] == '      @brief Brief description\n'
        assert testText[3] == '      \n'
        assert testText[4] == '      @param foo {int} Foo input\n'
        assert testText[5] == '      \n'
        assert testText[6] == '      @return int - return value\n'
        assert testText[7] == '    """\n'

    def test52DefineFunctionWithPrePostDecoration(self):
        """!
        @brief Test the _defineFunctionWithDecorations method, with prefix and postfix
        """
        helper = GeneratePythonFileHelper()
        retDict = ParamRetDict.buildReturnDictWithMod("integer", "return value", 0)
        paramList = [ParamRetDict.buildParamDictWithMod("foo", "unsigned", "Foo input", 0)]
        testText = helper._defineFunctionWithDecorations("MyDefineFunc", "Brief description", paramList, retDict,
                                                         prefixDecaration="@static", postfixDecaration="const")
        assert len(testText) == 9
        assert testText[0] == '@static\n'
        assert testText[1] == 'def MyDefineFunc(foo:int) -> int:\n'
        assert testText[2] == '    """!\n'
        assert testText[3] == '      @brief Brief description\n'
        assert testText[4] == '      \n'
        assert testText[5] == '      @param foo {int} Foo input\n'
        assert testText[6] == '      \n'
        assert testText[7] == '      @return int - return value\n'
        assert testText[8] == '    """\n'

    def test53DefineFunctionNoComment(self):
        """!
        @brief Test the _defineFunctionWithDecorations method, with no comment
        """
        helper = GeneratePythonFileHelper()
        retDict = ParamRetDict.buildReturnDictWithMod("integer", "return value", 0)
        paramList = [ParamRetDict.buildParamDictWithMod("foo", "unsigned", "Foo input", 0)]
        testText = helper._defineFunctionWithDecorations("MyDefineFunc", "Brief description", paramList, retDict, True)
        assert len(testText) == 1
        assert testText[0] == 'def MyDefineFunc(foo:int) -> int:\n'

    def test54DefineFunctionEmptyParamList(self):
        """!
        @brief Test the _defineFunctionWithDecorations method, with empty param list
        """
        helper = GeneratePythonFileHelper()
        retDict = ParamRetDict.buildReturnDictWithMod("integer", "return value", 0)
        testText = helper._defineFunctionWithDecorations("MyDefineFunc", "Brief description", [], retDict, True)
        assert len(testText) == 1
        assert testText[0] == 'def MyDefineFunc() -> int:\n'

    def test55GenClassOpenNoDescription(self):
        """!
        @brief Test the _genClassOpen method, with no description
        """
        helper = GeneratePythonFileHelper()

        testText = helper._genClassOpen("MyTestClassName", None, "MyBaseClass", "final", 2)
        assert len(testText) == 1
        assert testText[0] == "  class MyTestClassName(MyBaseClass):\n"
