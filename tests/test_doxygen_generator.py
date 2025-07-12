"""@package test_programmer_tools
Unittest for programmer base tools utility

"""

#==========================================================================
# Copyright (c) 2024-2025 Randal Eike
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

import pytest
from code_tools_grocsoftware.base.param_return_tools import ParamRetDict
from code_tools_grocsoftware.base.doxygen_gen_tools import DoxyCommentGenerator

class UnittestDoxygenCommentBlock:
    """!
    Doxygen comment block test cases
    """
    def setUpParams(self, blockStart:str|None, blockEnd:str|None, blockLine:str|None, singleLine:str|None, addParam:bool):
        """!
        @brief Common test setUp routine

        @param blockStart {string|None} Doxygen comment block start for the programming language
        @param blockEnd {string|None} Doxygen comment block end for the programming language
        @param blockLine {string|None} Doxygen comment block line prefix for the programming language
        @param singleLine {string|None} Doxygen comment single line start for the programming language
        @param addParam {boolean} True, add parameter type to documentation comment, False, do not add type to comment
        """
        self.blockStart = blockStart
        self.blockEnd = blockEnd
        self.blockLine = blockLine
        self.singleLine = singleLine
        self.addParam = addParam

        self.tstGen = DoxyCommentGenerator(blockStart, blockEnd, blockLine, singleLine, addParam)
        if blockStart is not None:
            self.descFormatAdjust = len(blockStart)
            self.expectedBlockStart = blockStart
            if blockEnd == '"""':
                self.expectedBlockEnd = blockEnd
            else:
                self.expectedBlockEnd = " "+blockEnd
            self.expectedBlockPrefix = " "+blockLine+" "
        elif singleLine is not None:
            self.descFormatAdjust = len(singleLine)
            self.expectedBlockStart = singleLine
            self.expectedBlockEnd = ""
            self.expectedBlockPrefix = singleLine+" "

    """!
    @brief Unit test for the TextFileCommentBlock class
    """
    def test01DoxyGenConstructor(self):
        """!
        @brief Test the constructor
        """
        assert self.tstGen.blockStart == self.blockStart
        assert self.tstGen.blockEnd == self.blockEnd
        assert self.tstGen.blockLineStart == self.blockLine
        assert self.tstGen.singleLineStart == self.singleLine

        assert self.tstGen.formatMaxLength == 120
        assert self.tstGen.descFormatMax == 120-self.descFormatAdjust

        assert self.tstGen.addParamType == self.addParam
        assert self.tstGen.groupCounter == 0

    def test02GenBlockPrefix(self):
        """!
        @brief Test the block line prefix generation
        """
        tstStr = self.tstGen._genCommentBlockPrefix()
        assert tstStr == self.expectedBlockPrefix

    def test03GenBlockStart(self):
        """!
        @brief Test the block start generation
        """
        tstStr = self.tstGen._genBlockStart()
        assert tstStr == self.expectedBlockStart

    def test04GenBlockEnd(self):
        """!
        @brief Test the block end generation
        """
        tstStr = self.tstGen._genBlockEnd()
        assert tstStr == self.expectedBlockEnd

    def test05GenBriefDescShort(self):
        """!
        @brief Test the brief description block with short description
        """
        prefix = "  "+self.expectedBlockPrefix
        self.tstGen.descFormatMax = 80
        tstStrList = self.tstGen._genBriefDesc("Brief description short", prefix)
        assert len(tstStrList) == 1
        assert tstStrList[0] == prefix+"@brief Brief description short\n"

    def test06GenBriefDescLong(self):
        """!
        @brief Test the brief description block with long description
        """
        prefix = "  "+self.expectedBlockPrefix
        self.tstGen.descFormatMax = 79+len(prefix)
        tstStrList = self.tstGen._genBriefDesc("Brief description long. Long meandering description to make sure that the text wraps at least one line.  Just to make sure.",
                                               prefix)
        assert len(tstStrList) == 2
        assert tstStrList[0] == prefix+"@brief Brief description long. Long meandering description to make sure that the\n"
        assert tstStrList[1] == prefix+"       text wraps at least one line.  Just to make sure.\n"

    def test07GenLongDescShort(self):
        """!
        @brief Test the long description block with short description
        """
        prefix = "  "+self.expectedBlockPrefix
        self.tstGen.descFormatMax = 80+len(prefix)
        tstStrList = self.tstGen._genLongDesc(prefix, "Short description line")
        assert len(tstStrList) == 1
        assert tstStrList[0] == prefix+"Short description line\n"

    def test08GenLongDescShortLong(self):
        """!
        @brief Test the long description block with long description
        """
        prefix = "  "+self.expectedBlockPrefix
        self.tstGen.descFormatMax = 80+len(prefix)
        tstStrList = self.tstGen._genLongDesc(prefix,
                                              "Long description line. Long meandering description to make sure that the text wraps at least one line.  Just to make sure.")
        assert len(tstStrList) == 2
        assert tstStrList[0] == prefix+"Long description line. Long meandering description to make sure that the text wraps\n"
        assert tstStrList[1] == prefix+"at least one line.  Just to make sure.\n"

    def test09GenRetDocShortDesc(self):
        """!
        @brief Test the generate return documentation with short description
        """
        prefix = "  "+self.expectedBlockPrefix
        self.tstGen.descFormatMax = 80+len(prefix)
        retDict = ParamRetDict.buildReturnDict("string", "Short desciption")
        tstStrList = self.tstGen._genCommentReturnText(retDict, prefix)
        assert len(tstStrList) == 1
        expectedStr  = prefix
        expectedStr += "@return "
        expectedStr += ParamRetDict.getReturnType(retDict)
        expectedStr += " - "
        expectedStr += ParamRetDict.getReturnDesc(retDict)
        expectedStr += "\n"
        assert tstStrList[0] == expectedStr

    def test10GenRetDocLongDesc(self):
        """!
        @brief Test the generate return documentation with long description
        """
        prefix = "  "+self.expectedBlockPrefix
        self.tstGen.descFormatMax = 78+len(prefix)
        retDict = ParamRetDict.buildReturnDict("string", "Long meandering desciption of the return data designed to make sure that the line wraps")
        tstStrList = self.tstGen._genCommentReturnText(retDict, prefix)
        assert len(tstStrList) == 2

        expectedStr  = prefix
        expectedStr += "@return "
        expectedStr += ParamRetDict.getReturnType(retDict)
        expectedStr += " - Long meandering desciption of the return data designed to make\n"
        assert tstStrList[0] == expectedStr

        expectedStr1  = prefix
        expectedStr1 += "                 sure that the line wraps\n"
        assert tstStrList[1] == expectedStr1

    def test11GenParamDocShortDesc(self):
        """!
        @brief Test the generate parameter documentation with short description
        """
        prefix = "  "+self.expectedBlockPrefix
        self.tstGen.descFormatMax = 80+len(prefix)
        paramDict = ParamRetDict.buildParamDictWithMod("foo", "string", "Short desciption", 0)
        tstStrList = self.tstGen._genCommentParamText(paramDict, prefix)

        expectedStr  = prefix
        expectedStr += "@param "
        expectedStr += ParamRetDict.getParamName(paramDict)
        expectedStr += " "

        if self.addParam:
            expectedStr += "{"
            expectedStr += ParamRetDict.getParamType(paramDict)
            expectedStr += "} "

        expectedStr += ParamRetDict.getParamDesc(paramDict)
        expectedStr += "\n"

        assert len(tstStrList) == 1
        assert tstStrList[0] == expectedStr

    def test12GenParamDocLongDesc(self):
        """!
        @brief Test the generate parameter documentation with long description
        """
        prefix = "  "+self.expectedBlockPrefix
        self.tstGen.descFormatMax = 76+len(prefix)
        paramDict = ParamRetDict.buildParamDictWithMod("moo", "string", "Long meandering desciption of the return data designed to make sure that the line wraps")
        tstStrList = self.tstGen._genCommentParamText(paramDict, prefix)

        expectedStr  = prefix
        expectedStr += "@param "
        expectedStr += ParamRetDict.getParamName(paramDict)
        expectedStr += " "

        if self.addParam:
            expectedStr += "{"
            expectedStr += ParamRetDict.getParamType(paramDict)
            expectedStr += "} Long meandering desciption of the return data designed to\n"
        else:
            expectedStr += "Long meandering desciption of the return data designed to make sure\n"


        expectedStr1  = prefix
        if self.addParam:
            expectedStr1 += "                    make sure that the line wraps\n"
        else:
            expectedStr1 += "           that the line wraps\n"

        assert len(tstStrList) == 2
        assert tstStrList[0] == expectedStr
        assert tstStrList[1] == expectedStr1

    def test13GenMethodDocBriefOnly(self):
        """!
        @brief Test the generate method documentation
        """
        prefix = "".rjust(4, ' ')
        blockprefix = prefix+self.expectedBlockPrefix
        retDict = ParamRetDict.buildReturnDict("string", "Short return desciption")
        paramDictList = [ParamRetDict.buildParamDictWithMod("moo", "string", "Short str param desciption"),
                         ParamRetDict.buildParamDictWithMod("foo", "int", "Short int param desciption")]

        tstStrList = self.tstGen.genDoxyMethodComment("Brief method description", paramDictList, retDict, blockIndent=4)

        assert len(tstStrList) == 8
        assert tstStrList[0] == prefix+self.expectedBlockStart+"\n"
        assert tstStrList[1] == blockprefix+"@brief Brief method description\n"
        assert tstStrList[2] == blockprefix+"\n"

        paramPrefix = blockprefix+"@param "
        param1Expected = paramPrefix+ParamRetDict.getParamName(paramDictList[0])+" "
        if self.addParam:
            param1Expected += "{"
            param1Expected += ParamRetDict.getParamType(paramDictList[0])
            param1Expected += "} "

        param1Expected += "Short str param desciption\n"

        param2Expected = paramPrefix+ParamRetDict.getParamName(paramDictList[1])+" "
        if self.addParam:
            param2Expected += "{"
            param2Expected += ParamRetDict.getParamType(paramDictList[1])
            param2Expected += "} "

        param2Expected += "Short int param desciption\n"

        assert tstStrList[3] == param1Expected
        assert tstStrList[4] == param2Expected
        assert tstStrList[5] == blockprefix+"\n"

        returnExpected  = blockprefix+"@return "
        returnExpected += ParamRetDict.getReturnType(retDict)
        returnExpected += " - Short return desciption\n"
        assert tstStrList[6] == returnExpected

        assert tstStrList[7] == prefix+self.expectedBlockEnd+"\n"

    def test14GenMethodDocBriefAndLong(self):
        """!
        @brief Test the generate method documentation, with long description
        """
        prefix = "".rjust(4, ' ')
        blockprefix = prefix+self.expectedBlockPrefix
        self.tstGen.descFormatMax = 77+len(blockprefix)
        retDict = ParamRetDict.buildReturnDict("string", "Short return desciption")
        paramDictList = [ParamRetDict.buildParamDictWithMod("moo", "string", "Short str param desciption"),
                         ParamRetDict.buildParamDictWithMod("foo", "int", "Short int param desciption")]

        longMethodDesc = "Long meandering method description. Not sure what there is to say, just going on until I can make sure it will wrap"
        tstStrList = self.tstGen.genDoxyMethodComment("Brief method description", paramDictList, retDict, longMethodDesc, 4)

        assert len(tstStrList) == 11
        assert tstStrList[0] == prefix+self.expectedBlockStart+"\n"
        assert tstStrList[1] == blockprefix+"@brief Brief method description\n"
        assert tstStrList[2] == blockprefix+"\n"
        assert tstStrList[3] == blockprefix+"Long meandering method description. Not sure what there is to say, just going on\n"
        assert tstStrList[4] == blockprefix+"until I can make sure it will wrap\n"
        assert tstStrList[5] == blockprefix+"\n"

        paramPrefix = blockprefix+"@param "
        param1Expected = paramPrefix+ParamRetDict.getParamName(paramDictList[0])+" "
        if self.addParam:
            param1Expected += "{"
            param1Expected += ParamRetDict.getParamType(paramDictList[0])
            param1Expected += "} "

        param1Expected += "Short str param desciption\n"

        param2Expected = paramPrefix+ParamRetDict.getParamName(paramDictList[1])+" "
        if self.addParam:
            param2Expected += "{"
            param2Expected += ParamRetDict.getParamType(paramDictList[1])
            param2Expected += "} "

        param2Expected += "Short int param desciption\n"

        assert tstStrList[6] == param1Expected
        assert tstStrList[7] == param2Expected
        assert tstStrList[8] == blockprefix+"\n"

        returnExpected  = blockprefix+"@return "
        returnExpected += ParamRetDict.getReturnType(retDict)
        returnExpected += " - Short return desciption\n"
        assert tstStrList[9] == returnExpected

        assert tstStrList[10] == prefix+self.expectedBlockEnd+"\n"

    def test15GenClassDocBriefOnly(self):
        """!
        @brief Test the generate class documentation
        """
        prefix = "".rjust(4, ' ')
        blockprefix = prefix+self.expectedBlockPrefix
        self.tstGen.descFormatMax = 78+len(prefix)
        tstStrList = self.tstGen.genDoxyClassComment("Brief class description", blockIndent=4)

        assert len(tstStrList) == 3
        assert tstStrList[0] == prefix+self.expectedBlockStart+"\n"
        assert tstStrList[1] == blockprefix+"@brief Brief class description\n"
        assert tstStrList[2] == prefix+self.expectedBlockEnd+"\n"

    def test16GenClassDocBriefAndLong(self):
        """!
        @brief Test the generate class documentation
        """
        prefix = "".rjust(4, ' ')
        blockprefix = prefix+self.expectedBlockPrefix
        self.tstGen.descFormatMax = 78+len(prefix)
        longClassDesc = "Long meandering class description. Not sure what there is to say, just going on until I can make sure it will wrap"
        tstStrList = self.tstGen.genDoxyClassComment("Brief class description", longClassDesc, 4)

        assert len(tstStrList) == 6
        assert tstStrList[0] == prefix+self.expectedBlockStart+"\n"
        assert tstStrList[1] == blockprefix+"@brief Brief class description\n"
        assert tstStrList[2] == blockprefix+"\n"
        assert tstStrList[3] == blockprefix+"Long meandering class description. Not sure what there is to say, just going on\n"
        assert tstStrList[4] == blockprefix+"until I can make sure it will wrap\n"
        assert tstStrList[5] == prefix+self.expectedBlockEnd+"\n"

    def test17GenDefGroupFull(self):
        """!
        @brief Test the generate group definition documentation, full definition
        """
        tstStrList = self.tstGen.genDoxyDefgroup("test.x", "Fred", "Test Fred group")
        assert len(tstStrList) == 6
        assert tstStrList[0] == self.expectedBlockStart+"\n"
        assert tstStrList[1] == self.expectedBlockPrefix+"@file test.x\n"
        assert tstStrList[2] == self.expectedBlockPrefix+"@defgroup Fred Test Fred group\n"
        assert tstStrList[3] == self.expectedBlockPrefix+"@ingroup Fred\n"
        assert tstStrList[4] == self.expectedBlockPrefix+"@{\n"
        assert tstStrList[5] == self.expectedBlockEnd+"\n"

    def test18GenDefGroupOnly(self):
        """!
        @brief Test the generate group definition documentation, group only
        """
        tstStrList = self.tstGen.genDoxyDefgroup("test.x", "Fred")
        assert len(tstStrList) == 5
        assert tstStrList[0] == self.expectedBlockStart+"\n"
        assert tstStrList[1] == self.expectedBlockPrefix+"@file test.x\n"
        assert tstStrList[2] == self.expectedBlockPrefix+"@ingroup Fred\n"
        assert tstStrList[3] == self.expectedBlockPrefix+"@{\n"
        assert tstStrList[4] == self.expectedBlockEnd+"\n"

    def test18GenDefEndGroupWithNoOpen(self):
        """!
        @brief Test the generate end group documentation if no group was opened
        """
        assert self.tstGen.genDoxyGroupEnd() is None

    def test19GenDefEndGroupWithOneOpen(self):
        """!
        @brief Test the generate end group documentation where one group was opened
        """
        self.tstGen.genDoxyDefgroup("test.x", "Fred")
        tstStr = self.tstGen.genDoxyGroupEnd()
        assert tstStr is not None
        assert tstStr == self.expectedBlockStart+"@}"+self.expectedBlockEnd+"\n"

        # Verify the group counter is 0
        assert self.tstGen.genDoxyGroupEnd() is None

    def test20GenDefEndGroupWithTwoOpen(self):
        """!
        @brief Test the generate end group documentation where two groups were opened
        """
        self.tstGen.genDoxyDefgroup("test.x", "Fred")
        self.tstGen.genDoxyDefgroup("test.x", "Barney")
        tstStr = self.tstGen.genDoxyGroupEnd()
        assert tstStr is not None
        assert tstStr == self.expectedBlockStart+"@}"+self.expectedBlockEnd+"\n"

        tstStr1 = self.tstGen.genDoxyGroupEnd()
        assert tstStr1 is not None
        assert tstStr1 == self.expectedBlockStart+"@}"+self.expectedBlockEnd+"\n"

        # Verify the group counter is 0
        assert self.tstGen.genDoxyGroupEnd() is None

    def test21GenSingleLineComment(self):
        """!
        @brief Test the generate single line comment
        """
        assert self.tstGen.genSingleLineStart() == self.singleLine

    def test21GenVarDoc(self):
        """!
        @brief Test the generate single line comment
        """
        assert self.tstGen.genDoxyVarDocStr("Short description") == self.singleLine+"< Short description"
        assert self.tstGen.genDoxyVarDocStr("Foo description") == self.singleLine+"< Foo description"

    def test22GenMethodDocNoReturn(self):
        """!
        @brief Test the generate method documentation
        """
        prefix = "".rjust(4, ' ')
        blockprefix = prefix+self.expectedBlockPrefix
        paramDictList = [ParamRetDict.buildParamDictWithMod("moo", "string", "Short str param desciption"),
                         ParamRetDict.buildParamDictWithMod("foo", "int", "Short int param desciption")]

        tstStrList = self.tstGen.genDoxyMethodComment("Brief method description", paramDictList, None, blockIndent=4)

        assert len(tstStrList) == 7
        assert tstStrList[0] == prefix+self.expectedBlockStart+"\n"
        assert tstStrList[1] == blockprefix+"@brief Brief method description\n"
        assert tstStrList[2] == blockprefix+"\n"

        paramPrefix = blockprefix+"@param "
        param1Expected = paramPrefix+ParamRetDict.getParamName(paramDictList[0])+" "
        if self.addParam:
            param1Expected += "{"
            param1Expected += ParamRetDict.getParamType(paramDictList[0])
            param1Expected += "} "

        param1Expected += "Short str param desciption\n"

        param2Expected = paramPrefix+ParamRetDict.getParamName(paramDictList[1])+" "
        if self.addParam:
            param2Expected += "{"
            param2Expected += ParamRetDict.getParamType(paramDictList[1])
            param2Expected += "} "

        param2Expected += "Short int param desciption\n"

        assert tstStrList[3] == param1Expected
        assert tstStrList[4] == param2Expected
        assert tstStrList[5] == blockprefix+"\n"
        assert tstStrList[6] == prefix+self.expectedBlockEnd+"\n"

    def test23GenMethodDocEmptyParamList(self):
        """!
        @brief Test the generate method documentation
        """
        prefix = "".rjust(4, ' ')
        blockprefix = prefix+self.expectedBlockPrefix
        retDict = ParamRetDict.buildReturnDict("string", "Short return desciption")
        tstStrList = self.tstGen.genDoxyMethodComment("Brief method description", [], retDict, blockIndent=4)

        assert len(tstStrList) == 5
        assert tstStrList[0] == prefix+self.expectedBlockStart+"\n"
        assert tstStrList[1] == blockprefix+"@brief Brief method description\n"
        assert tstStrList[2] == blockprefix+"\n"
        returnExpected  = blockprefix+"@return "
        returnExpected += ParamRetDict.getReturnType(retDict)
        returnExpected += " - Short return desciption\n"
        assert tstStrList[3] == returnExpected

        assert tstStrList[4] == prefix+self.expectedBlockEnd+"\n"

    def test24GenMethodDocEmptyParamListNoReturn(self):
        """!
        @brief Test the generate method documentation
        """
        prefix = "".rjust(4, ' ')
        blockprefix = prefix+self.expectedBlockPrefix
        tstStrList = self.tstGen.genDoxyMethodComment("Brief method description", [], None, blockIndent=4)

        assert len(tstStrList) == 4
        assert tstStrList[0] == prefix+self.expectedBlockStart+"\n"
        assert tstStrList[1] == blockprefix+"@brief Brief method description\n"
        assert tstStrList[2] == blockprefix+"\n"
        assert tstStrList[3] == prefix+self.expectedBlockEnd+"\n"

    def test25GenLongNone(self):
        """!
        @brief Test the long description block with None long description
        """
        prefix = "  "+self.expectedBlockPrefix
        self.tstGen.descFormatMax = 80+len(prefix)
        tstStrList = self.tstGen._genLongDesc(prefix)
        assert len(tstStrList) == 0

    def test26GenClassDocBriefNone(self):
        """!
        @brief Test the generate class documentation
        """
        prefix = "".rjust(4, ' ')
        blockprefix = prefix+self.expectedBlockPrefix
        self.tstGen.descFormatMax = 78+len(prefix)
        tstStrList = self.tstGen.genDoxyClassComment(None, "Long class description", blockIndent=4)

        assert len(tstStrList) == 3
        assert tstStrList[0] == prefix+self.expectedBlockStart+"\n"
        assert tstStrList[1] == blockprefix+"Long class description\n"
        assert tstStrList[2] == prefix+self.expectedBlockEnd+"\n"

    def test27GenDefGroupNone(self):
        """!
        @brief Test the generate group definition documentation, None group
        """
        tstStrList = self.tstGen.genDoxyDefgroup("test.x")
        assert len(tstStrList) == 3
        assert tstStrList[0] == self.expectedBlockStart+"\n"
        assert tstStrList[1] == self.expectedBlockPrefix+"@file test.x\n"
        assert tstStrList[2] == self.expectedBlockEnd+"\n"

class TestUnittestDoxygenCCommentBlock(UnittestDoxygenCommentBlock):
    """!
    Doxygen comment block test cases
    """
    def setup_method(self):
        self.setUpParams('/**', '*/', '*', '//!', False)

class TestUnittestDoxygenPyCommentBlock(UnittestDoxygenCommentBlock):
    """!
    Doxygen comment block test cases
    """
    def setup_method(self):
        self.setUpParams('"""!', '"""', '', '##!', True)

class TestUnittestDoxygenJsTsCommentBlock(UnittestDoxygenCommentBlock):
    """!
    Doxygen comment block test cases
    """
    def setup_method(self):
        self.setUpParams('/**', '*/', '*', '//!', True)

class TestUnittestDoxygenSinglLineCommentBlock(UnittestDoxygenCommentBlock):
    """!
    Doxygen comment block test cases
    """
    def setup_method(self):
        self.setUpParams(None, None, None, '##!', True)

from code_tools_grocsoftware.base.doxygen_gen_tools import CDoxyCommentGenerator
from code_tools_grocsoftware.base.doxygen_gen_tools import PyDoxyCommentGenerator
from code_tools_grocsoftware.base.doxygen_gen_tools import TsDoxyCommentGenerator
from code_tools_grocsoftware.base.doxygen_gen_tools import JsDoxyCommentGenerator

class TestUnittestDoxygenProgCommentBlock:
    """!
    Doxygen comment block test cases
    """
    def test01CGeneratorConstructor(self):
        tstGen = CDoxyCommentGenerator()
        assert tstGen.blockStart == "/**"
        assert tstGen.blockEnd == "*/"
        assert tstGen.blockLineStart == "*"
        assert tstGen.singleLineStart == "//!"
        assert not tstGen.addParamType

    def test02TsGeneratorConstructor(self):
        tstGen = TsDoxyCommentGenerator()
        assert tstGen.blockStart == "/**"
        assert tstGen.blockEnd == "*/"
        assert tstGen.blockLineStart == "*"
        assert tstGen.singleLineStart == "//!"
        assert tstGen.addParamType

    def test03JsGeneratorConstructor(self):
        tstGen = JsDoxyCommentGenerator()
        assert tstGen.blockStart == "/**"
        assert tstGen.blockEnd == "*/"
        assert tstGen.blockLineStart == "*"
        assert tstGen.singleLineStart == "//!"
        assert tstGen.addParamType

    def test04PyGeneratorConstructor(self):
        tstGen = PyDoxyCommentGenerator()
        assert tstGen.blockStart == '"""!'
        assert tstGen.blockEnd == '"""'
        assert tstGen.blockLineStart == ""
        assert tstGen.singleLineStart == "##"
        assert tstGen.addParamType

    def test05NullGeneratorConstructor(self):
        tstGen = DoxyCommentGenerator(None, None, None, None)
        assert tstGen.blockStart is None
        assert tstGen.blockEnd is None
        assert tstGen.blockLineStart is None
        assert tstGen.singleLineStart is None
        assert not tstGen.addParamType

        with pytest.raises(Exception) as context:
            prefix = tstGen._genCommentBlockPrefix()
        assert "ERROR: Can't have a doxygen comment if there are no comment markers." in str(context.value)

        with pytest.raises(Exception) as context:
            prefix = tstGen._genBlockStart()
        assert "ERROR: Can't have a doxygen comment if there are no comment markers." in str(context.value)
