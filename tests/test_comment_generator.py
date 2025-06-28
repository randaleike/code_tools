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

import unittest

from dir_init import pathincsetup
pathincsetup()

from code_tools_grocsoftware.base.comment_gen_tools import CommentGenerator

cCommentParms =   {'blockStart': "/*", 'blockEnd': "*/", 'blockLineStart': "", 'singleLine': "//"}
pyCommentParms =  {'blockStart': "\"\"\"", 'blockEnd':"\"\"\"", 'blockLineStart': "", 'singleLine': "#"}
shCommentParms =  {'blockStart': None, 'blockEnd': None, 'blockLineStart': "#", 'singleLine': "#"}
batCommentParms = {'blockStart': None, 'blockEnd': None, 'blockLineStart': "REM ", 'singleLine': "REM ",}

class Unittest07CommentGeneration(unittest.TestCase):
    """!
    @brief Unit test for the CommentGenerator class
    """
    def test001CHeaderGenerationDefault(self):
        """!
        @brief Test c file type files comment block header generation
        default constructor
        """
        generator = CommentGenerator(cCommentParms)

        header = generator.buildCommentBlockHeader()
        self.assertEqual(len(header), 1)
        self.assertEqual(header[0], "/*")

        header = generator.buildCommentBlockHeader(2)
        self.assertEqual(len(header), 2)
        self.assertEqual(header[0], "/*")
        self.assertEqual(header[1], "")

        header = generator.buildCommentBlockHeader(3)
        self.assertEqual(len(header), 3)
        self.assertEqual(header[0], "/*")
        self.assertEqual(header[1], "")
        self.assertEqual(header[2], "")

    def test002CHeaderGenerationPad(self):
        """!
        @brief Test c file type files comment block header generation
        padded line constructor
        """
        generator = CommentGenerator(cCommentParms, 10)

        header = generator.buildCommentBlockHeader(1, '=')
        self.assertEqual(len(header), 1)
        self.assertEqual(header[0], "/*========")

        header = generator.buildCommentBlockHeader(2, '=')
        self.assertEqual(len(header), 2)
        self.assertEqual(header[0], "/*========")
        self.assertEqual(header[1], "==========")

        header = generator.buildCommentBlockHeader(3, '=')
        self.assertEqual(len(header), 3)
        self.assertEqual(header[0], "/*========")
        self.assertEqual(header[1], "==========")
        self.assertEqual(header[2], "==========")

    def test003CHeaderGenerationPadAndEol(self):
        """!
        @brief Test c file type files comment block header generation
        padded line and end of line constructor
        """
        generator = CommentGenerator(cCommentParms, 10, "*")

        header = generator.buildCommentBlockHeader(1, '=')
        self.assertEqual(len(header), 1)
        self.assertEqual(header[0], "/*=======*")

        header = generator.buildCommentBlockHeader(2, '=')
        self.assertEqual(len(header), 2)
        self.assertEqual(header[0], "/*=======*")
        self.assertEqual(header[1], "=========*")

        header = generator.buildCommentBlockHeader(3, '=')
        self.assertEqual(len(header), 3)
        self.assertEqual(header[0], "/*=======*")
        self.assertEqual(header[1], "=========*")
        self.assertEqual(header[2], "=========*")

    def test004CHeaderGenerationPadAndEol2(self):
        """!
        @brief Test c file type files comment block header generation
        padded line and end of line constructor
        """
        generator = CommentGenerator(cCommentParms, 10, " *")

        header = generator.buildCommentBlockHeader(1, '=')
        self.assertEqual(len(header), 1)
        self.assertEqual(header[0], "/*====== *")

        header = generator.buildCommentBlockHeader(2, '=')
        self.assertEqual(len(header), 2)
        self.assertEqual(header[0], "/*====== *")
        self.assertEqual(header[1], "======== *")

        header = generator.buildCommentBlockHeader(3, '=')
        self.assertEqual(header[0], "/*====== *")
        self.assertEqual(header[1], "======== *")
        self.assertEqual(header[2], "======== *")


    def test005CHeaderGenerationForceSingle(self):
        """!
        @brief Test c file type files comment block header generation
        forced single line constructor
        """
        generator = CommentGenerator(cCommentParms, useSingleLine = True)

        header = generator.buildCommentBlockHeader()
        self.assertEqual(len(header), 1)
        self.assertEqual(header[0], "//")

        header = generator.buildCommentBlockHeader(2)
        self.assertEqual(len(header), 2)
        self.assertEqual(header[0], "//")
        self.assertEqual(header[1], "//")

        header = generator.buildCommentBlockHeader(3)
        self.assertEqual(len(header), 3)
        self.assertEqual(header[0], "//")
        self.assertEqual(header[1], "//")
        self.assertEqual(header[2], "//")

    def test006CHeaderGenerationForceSinglePad(self):
        """!
        @brief Test c file type files comment block header generation
        padded, forced single line constructor
        """
        generator = CommentGenerator(cCommentParms, 10, useSingleLine = True)

        header = generator.buildCommentBlockHeader(1)
        self.assertEqual(len(header), 1)
        self.assertEqual(header[0], "//--------")

        header = generator.buildCommentBlockHeader(2)
        self.assertEqual(len(header), 2)
        self.assertEqual(header[0], "//--------")
        self.assertEqual(header[1], "//--------")

        header = generator.buildCommentBlockHeader(3, '=')
        self.assertEqual(len(header), 3)
        self.assertEqual(header[0], "//========")
        self.assertEqual(header[1], "//========")
        self.assertEqual(header[2], "//========")

    def test007CHeaderGenerationForceSinglePadEol(self):
        """!
        @brief Test c file type files comment block header generation
        padded, end of line text, forced single line constructor
        """
        generator = CommentGenerator(cCommentParms, 10, " *", useSingleLine = True)

        header = generator.buildCommentBlockHeader(1, '=')
        self.assertEqual(len(header), 1)
        self.assertEqual(header[0], "//====== *")

        header = generator.buildCommentBlockHeader(2)
        self.assertEqual(len(header), 2)
        self.assertEqual(header[0], "//------ *")
        self.assertEqual(header[1], "//------ *")

        header = generator.buildCommentBlockHeader(3, '=')
        self.assertEqual(len(header), 3)
        self.assertEqual(header[0], "//====== *")
        self.assertEqual(header[1], "//====== *")
        self.assertEqual(header[2], "//====== *")

    def test011CFooterGenerationDefault(self):
        """!
        @brief Test c file type files comment block footer generation
        default constructor
        """
        generator = CommentGenerator(cCommentParms)

        footer = generator.buildCommentBlockFooter()
        self.assertEqual(len(footer), 1)
        self.assertEqual(footer[0], "*/")

        footer = generator.buildCommentBlockFooter(2)
        self.assertEqual(len(footer), 2)
        self.assertEqual(footer[0], "")
        self.assertEqual(footer[1], "*/")

        footer = generator.buildCommentBlockFooter(3)
        self.assertEqual(len(footer), 3)
        self.assertEqual(footer[0], "")
        self.assertEqual(footer[1], "")
        self.assertEqual(footer[2], "*/")

    def test012CFooterGenerationPad(self):
        """!
        @brief Test c file type files comment block footer generation
        padded line constructor
        """
        generator = CommentGenerator(cCommentParms, 10)

        footer = generator.buildCommentBlockFooter(1, '=')
        self.assertEqual(len(footer), 1)
        self.assertEqual(footer[0], "========*/")

        footer = generator.buildCommentBlockFooter(2, '=')
        self.assertEqual(len(footer), 2)
        self.assertEqual(footer[0], "==========")
        self.assertEqual(footer[1], "========*/")

        footer = generator.buildCommentBlockFooter(3, '=')
        self.assertEqual(len(footer), 3)
        self.assertEqual(footer[0], "==========")
        self.assertEqual(footer[1], "==========")
        self.assertEqual(footer[2], "========*/")

    def test013CFooterGenerationPadAndEol(self):
        """!
        @brief Test c file type files comment block footer generation
        padded line and end of line constructor
        """
        generator = CommentGenerator(cCommentParms, 10, "*")

        footer = generator.buildCommentBlockFooter(1, '=')
        self.assertEqual(len(footer), 1)
        self.assertEqual(footer[0], "========*/")

        footer = generator.buildCommentBlockFooter(2, '=')
        self.assertEqual(len(footer), 2)
        self.assertEqual(footer[0], "=========*")
        self.assertEqual(footer[1], "========*/")

        footer = generator.buildCommentBlockFooter(3, '=')
        self.assertEqual(len(footer), 3)
        self.assertEqual(footer[0], "=========*")
        self.assertEqual(footer[1], "=========*")
        self.assertEqual(footer[2], "========*/")

    def test014CFooterGenerationPadAndEol2(self):
        """!
        @brief Test c file type files comment block footer generation
        padded line and end of line constructor
        """
        generator = CommentGenerator(cCommentParms, 10, " *")

        footer = generator.buildCommentBlockFooter(1, '=')
        self.assertEqual(len(footer), 1)
        self.assertEqual(footer[0], "========*/")

        footer = generator.buildCommentBlockFooter(2, '=')
        self.assertEqual(len(footer), 2)
        self.assertEqual(footer[0], "======== *")
        self.assertEqual(footer[1], "========*/")

        footer = generator.buildCommentBlockFooter(3, '=')
        self.assertEqual(footer[0], "======== *")
        self.assertEqual(footer[1], "======== *")
        self.assertEqual(footer[2], "========*/")

    def test015CFooterGenerationForceSingle(self):
        """!
        @brief Test c file type files comment footer footer generation
        forced single line constructor
        """
        generator = CommentGenerator(cCommentParms, useSingleLine = True)

        footer = generator.buildCommentBlockFooter()
        self.assertEqual(len(footer), 1)
        self.assertEqual(footer[0], "//")

        footer = generator.buildCommentBlockFooter(2)
        self.assertEqual(len(footer), 2)
        self.assertEqual(footer[0], "//")
        self.assertEqual(footer[1], "//")

        footer = generator.buildCommentBlockFooter(3)
        self.assertEqual(len(footer), 3)
        self.assertEqual(footer[0], "//")
        self.assertEqual(footer[1], "//")
        self.assertEqual(footer[2], "//")

    def test016CFooterGenerationForceSinglePad(self):
        """!
        @brief Test c file type files comment block footer generation
        padded, forced single line constructor
        """
        generator = CommentGenerator(cCommentParms, 10, useSingleLine = True)

        footer = generator.buildCommentBlockFooter(1, '=')
        self.assertEqual(len(footer), 1)
        self.assertEqual(footer[0], "//========")

        footer = generator.buildCommentBlockFooter(2,)
        self.assertEqual(footer[0], "//--------")
        self.assertEqual(footer[1], "//--------")

        footer = generator.buildCommentBlockFooter(3, '=')
        self.assertEqual(len(footer), 3)
        self.assertEqual(footer[0], "//========")
        self.assertEqual(footer[1], "//========")
        self.assertEqual(footer[2], "//========")

    def test017CFooterGenerationForceSinglePadEol(self):
        """!
        @brief Test c file type files comment block footer generation
        padded, end of line text, forced single line constructor
        """
        generator = CommentGenerator(cCommentParms, 10, " *", useSingleLine = True)

        footer = generator.buildCommentBlockFooter(1, '=')
        self.assertEqual(len(footer), 1)
        self.assertEqual(footer[0], "//====== *")

        footer = generator.buildCommentBlockFooter(2)
        self.assertEqual(len(footer), 2)
        self.assertEqual(footer[0], "//------ *")
        self.assertEqual(footer[1], "//------ *")

        footer = generator.buildCommentBlockFooter(3, '=')
        self.assertEqual(len(footer), 3)
        self.assertEqual(footer[0], "//====== *")
        self.assertEqual(footer[1], "//====== *")
        self.assertEqual(footer[2], "//====== *")

    def test021CWrap(self):
        """!
        @brief Test c file type files comment line wrapper generation
        Default constructor
        """
        generator = CommentGenerator(cCommentParms)

        wrap = generator.wrapCommentLine("test line")
        self.assertEqual(wrap, "test line")

    def test022CWrapPad(self):
        """!
        @brief Test c file type files comment line wrapper generation
        padded
        """
        generator = CommentGenerator(cCommentParms, 10)

        wrap = generator.wrapCommentLine("test line")
        self.assertEqual(wrap, "test line")

    def test022CWrapPad1(self):
        """!
        @brief Test c file type files comment line wrapper generation
        padded
        """
        generator = CommentGenerator(cCommentParms, 12)

        wrap = generator.wrapCommentLine("test line")
        self.assertEqual(wrap, "test line")

    def test023CWrapSingle(self):
        """!
        @brief Test c file type files comment block footer generation
        forced single line constructor
        """
        generator = CommentGenerator(cCommentParms, useSingleLine = True)

        wrap = generator.wrapCommentLine("test line")
        self.assertEqual(wrap, "// test line")

    def test024CWrapSingle(self):
        """!
        @brief Test c file type files comment block footer generation
        padded, forced single line constructor
        """
        generator = CommentGenerator(cCommentParms, 15, useSingleLine = True)

        wrap = generator.wrapCommentLine("test line")
        self.assertEqual(wrap, "// test line")

    def test025CWrapPadAndEol(self):
        """!
        @brief Test c file type files comment line wrapper generation
        padded, end of line
        """
        generator = CommentGenerator(cCommentParms, 12, " *")

        wrap = generator.wrapCommentLine("test line")
        self.assertEqual(wrap, "test line  *")

    def test026CWrapPadAndEol(self):
        """!
        @brief Test c file type files comment line wrapper generation
        padded, end of line, forced single line
        """
        generator = CommentGenerator(cCommentParms, 15, " *", useSingleLine = True)

        wrap = generator.wrapCommentLine("test line")
        self.assertEqual(wrap, "// test line  *")

    def test031PythonDefault(self):
        """!
        @brief Test python file type files comment generation
        default constructor
        """
        generator = CommentGenerator(pyCommentParms)

        header = generator.buildCommentBlockHeader()
        footer = generator.buildCommentBlockFooter()
        self.assertEqual(len(header), 1)
        self.assertEqual(header[0], "\"\"\"")
        self.assertEqual(len(footer), 1)
        self.assertEqual(footer[0], "\"\"\"")

        header = generator.buildCommentBlockHeader(2)
        footer = generator.buildCommentBlockFooter(2)
        self.assertEqual(len(header), 2)
        self.assertEqual(header[0], "\"\"\"")
        self.assertEqual(header[1], "")
        self.assertEqual(len(footer), 2)
        self.assertEqual(footer[0], "")
        self.assertEqual(footer[1], "\"\"\"")

        wrap = generator.wrapCommentLine("test line")
        self.assertEqual(wrap, "test line")

    def test032PythonPad(self):
        """!
        @brief Test python file type files comment generation
        padded
        """
        generator = CommentGenerator(pyCommentParms, 10)

        header = generator.buildCommentBlockHeader()
        footer = generator.buildCommentBlockFooter()
        self.assertEqual(len(header), 1)
        self.assertEqual(header[0], "\"\"\"-------")
        self.assertEqual(len(footer), 1)
        self.assertEqual(footer[0], "-------\"\"\"")

        header = generator.buildCommentBlockHeader(2)
        footer = generator.buildCommentBlockFooter(2)
        self.assertEqual(len(header), 2)
        self.assertEqual(header[0], "\"\"\"-------")
        self.assertEqual(header[1], "----------")
        self.assertEqual(len(footer), 2)
        self.assertEqual(footer[0], "----------")
        self.assertEqual(footer[1], "-------\"\"\"")

        wrap = generator.wrapCommentLine("test line")
        self.assertEqual(wrap, "test line")

    def test033PythonPadEol(self):
        """!
        @brief Test python file type files comment generation
        padded, end of line
        """
        generator = CommentGenerator(pyCommentParms, 13, " *")

        header = generator.buildCommentBlockHeader()
        footer = generator.buildCommentBlockFooter()
        self.assertEqual(len(header), 1)
        self.assertEqual(header[0], "\"\"\"-------- *")
        self.assertEqual(len(footer), 1)
        self.assertEqual(footer[0], "----------\"\"\"")

        header = generator.buildCommentBlockHeader(2)
        footer = generator.buildCommentBlockFooter(2)
        self.assertEqual(len(header), 2)
        self.assertEqual(header[0], "\"\"\"-------- *")
        self.assertEqual(header[1], "----------- *")
        self.assertEqual(len(footer), 2)
        self.assertEqual(footer[0], "----------- *")
        self.assertEqual(footer[1], "----------\"\"\"")

        wrap = generator.wrapCommentLine("test line")
        self.assertEqual(wrap, "test line   *")

    def test034PythonForceSingle(self):
        """!
        @brief Test python file type files comment generation
        force single
        """
        generator = CommentGenerator(pyCommentParms, useSingleLine = True)

        header = generator.buildCommentBlockHeader()
        footer = generator.buildCommentBlockFooter()
        self.assertEqual(len(header), 1)
        self.assertEqual(header[0], "#")
        self.assertEqual(len(footer), 1)
        self.assertEqual(footer[0], "#")

        header = generator.buildCommentBlockHeader(2)
        footer = generator.buildCommentBlockFooter(2)
        self.assertEqual(len(header), 2)
        self.assertEqual(header[0], "#")
        self.assertEqual(header[1], "#")
        self.assertEqual(len(footer), 2)
        self.assertEqual(footer[0], "#")
        self.assertEqual(footer[1], "#")

        wrap = generator.wrapCommentLine("test line")
        self.assertEqual(wrap, "# test line")

    def test035PythonPadForceSingle(self):
        """!
        @brief Test python file type files comment generation
        padded, force single
        """
        generator = CommentGenerator(pyCommentParms, 12, useSingleLine = True)

        header = generator.buildCommentBlockHeader(1, '=')
        footer = generator.buildCommentBlockFooter(1, '=')
        self.assertEqual(len(header), 1)
        self.assertEqual(header[0], "#===========")
        self.assertEqual(len(footer), 1)
        self.assertEqual(footer[0], "#===========")

        header = generator.buildCommentBlockHeader(2, '=')
        footer = generator.buildCommentBlockFooter(2, '=')
        self.assertEqual(len(header), 2)
        self.assertEqual(header[0], "#===========")
        self.assertEqual(header[1], "#===========")
        self.assertEqual(len(footer), 2)
        self.assertEqual(footer[0], "#===========")
        self.assertEqual(footer[1], "#===========")

        wrap = generator.wrapCommentLine("test line")
        self.assertEqual(wrap, "# test line")

    def test036PythonPadEolForceSingle(self):
        """!
        @brief Test python file type files comment generation
        padded, end of line, force single
        """
        generator = CommentGenerator(pyCommentParms, 15, " *", useSingleLine = True)

        header = generator.buildCommentBlockHeader(1, '=')
        footer = generator.buildCommentBlockFooter(1, '=')
        self.assertEqual(len(header), 1)
        self.assertEqual(header[0], "#============ *")
        self.assertEqual(len(footer), 1)
        self.assertEqual(footer[0], "#============ *")

        header = generator.buildCommentBlockHeader(2, '=')
        footer = generator.buildCommentBlockFooter(2, '=')
        self.assertEqual(len(header), 2)
        self.assertEqual(header[0], "#============ *")
        self.assertEqual(header[1], "#============ *")
        self.assertEqual(len(footer), 2)
        self.assertEqual(footer[0], "#============ *")
        self.assertEqual(footer[1], "#============ *")

        wrap = generator.wrapCommentLine("test line")
        self.assertEqual(wrap, "# test line   *")

    def test041ShellDefault(self):
        """!
        @brief Test shell script file type files comment generation
        default constructor
        """
        generator = CommentGenerator(shCommentParms)

        header = generator.buildCommentBlockHeader()
        footer = generator.buildCommentBlockFooter()
        self.assertEqual(len(header), 1)
        self.assertEqual(header[0], "#")
        self.assertEqual(len(footer), 1)
        self.assertEqual(footer[0], "#")

        header = generator.buildCommentBlockHeader(2)
        footer = generator.buildCommentBlockFooter(2)
        self.assertEqual(len(header), 2)
        self.assertEqual(header[0], "#")
        self.assertEqual(header[1], "#")
        self.assertEqual(len(footer), 2)
        self.assertEqual(footer[0], "#")
        self.assertEqual(footer[1], "#")

        wrap = generator.wrapCommentLine("test line")
        self.assertEqual(wrap, "# test line")

    def test042ShellPad(self):
        """!
        @brief Test shell script file type files comment generation
        padded
        """
        generator = CommentGenerator(shCommentParms, 10)

        header = generator.buildCommentBlockHeader()
        footer = generator.buildCommentBlockFooter()
        self.assertEqual(len(header), 1)
        self.assertEqual(header[0], "#---------")
        self.assertEqual(len(footer), 1)
        self.assertEqual(footer[0], "#---------")

        header = generator.buildCommentBlockHeader(2)
        footer = generator.buildCommentBlockFooter(2)
        self.assertEqual(len(header), 2)
        self.assertEqual(header[0], "#---------")
        self.assertEqual(header[1], "#---------")
        self.assertEqual(len(footer), 2)
        self.assertEqual(footer[0], "#---------")
        self.assertEqual(footer[1], "#---------")

        wrap = generator.wrapCommentLine("test line")
        self.assertEqual(wrap, "# test line")

    def test043ShellPadEol(self):
        """!
        @brief Test shell script file type files comment generation
        padded, end of line
        """
        generator = CommentGenerator(shCommentParms, 13, " *")

        header = generator.buildCommentBlockHeader()
        footer = generator.buildCommentBlockFooter()
        self.assertEqual(len(header), 1)
        self.assertEqual(header[0], "#---------- *")
        self.assertEqual(len(footer), 1)
        self.assertEqual(footer[0], "#---------- *")

        header = generator.buildCommentBlockHeader(2)
        footer = generator.buildCommentBlockFooter(2)
        self.assertEqual(len(header), 2)
        self.assertEqual(header[0], "#---------- *")
        self.assertEqual(header[1], "#---------- *")
        self.assertEqual(len(footer), 2)
        self.assertEqual(footer[0], "#---------- *")
        self.assertEqual(footer[1], "#---------- *")

        wrap = generator.wrapCommentLine("test line")
        self.assertEqual(wrap, "# test line *")

    def test044ShellForce(self):
        """!
        @brief Test shell script file type files comment generation
        force single
        """
        generator = CommentGenerator(shCommentParms, useSingleLine = True)

        header = generator.buildCommentBlockHeader()
        footer = generator.buildCommentBlockFooter()
        self.assertEqual(len(header), 1)
        self.assertEqual(header[0], "#")
        self.assertEqual(len(footer), 1)
        self.assertEqual(footer[0], "#")

        header = generator.buildCommentBlockHeader(2)
        footer = generator.buildCommentBlockFooter(2)
        self.assertEqual(len(header), 2)
        self.assertEqual(header[0], "#")
        self.assertEqual(header[1], "#")
        self.assertEqual(len(footer), 2)
        self.assertEqual(footer[0], "#")
        self.assertEqual(footer[1], "#")

        wrap = generator.wrapCommentLine("test line")
        self.assertEqual(wrap, "# test line")

    def test045ShellForcePad(self):
        """!
        @brief Test shell script file type files comment generation
        force single, padded
        """
        generator = CommentGenerator(shCommentParms, 10, useSingleLine = True)

        header = generator.buildCommentBlockHeader()
        footer = generator.buildCommentBlockFooter()
        self.assertEqual(len(header), 1)
        self.assertEqual(header[0], "#---------")
        self.assertEqual(len(footer), 1)
        self.assertEqual(footer[0], "#---------")

        header = generator.buildCommentBlockHeader(2)
        footer = generator.buildCommentBlockFooter(2)
        self.assertEqual(len(header), 2)
        self.assertEqual(header[0], "#---------")
        self.assertEqual(header[1], "#---------")
        self.assertEqual(len(footer), 2)
        self.assertEqual(footer[0], "#---------")
        self.assertEqual(footer[1], "#---------")

        wrap = generator.wrapCommentLine("test line")
        self.assertEqual(wrap, "# test line")

    def test046ShellForcePadEol(self):
        """!
        @brief Test shell script file type files comment generation
        force single, padded, end of line
        """
        generator = CommentGenerator(shCommentParms, 13, " *", useSingleLine = True)

        header = generator.buildCommentBlockHeader()
        footer = generator.buildCommentBlockFooter()
        self.assertEqual(len(header), 1)
        self.assertEqual(header[0], "#---------- *")
        self.assertEqual(len(footer), 1)
        self.assertEqual(footer[0], "#---------- *")

        header = generator.buildCommentBlockHeader(2)
        footer = generator.buildCommentBlockFooter(2)
        self.assertEqual(len(header), 2)
        self.assertEqual(header[0], "#---------- *")
        self.assertEqual(header[1], "#---------- *")
        self.assertEqual(len(footer), 2)
        self.assertEqual(footer[0], "#---------- *")
        self.assertEqual(footer[1], "#---------- *")

        wrap = generator.wrapCommentLine("test line")
        self.assertEqual(wrap, "# test line *")

    def test050GenSingleLine(self):
        """!
        @brief Test file type files single line comment generation
        """
        generator = CommentGenerator(shCommentParms)
        self.assertEqual(generator.generateSingleLineComment("test text"), "# test text")

        generator1 = CommentGenerator(cCommentParms)
        self.assertEqual(generator1.generateSingleLineComment("test text"), "// test text")

        generator2 = CommentGenerator(pyCommentParms)
        self.assertEqual(generator2.generateSingleLineComment("test text"), "# test text")

    def test051TestCCommentConstructor(self):
        """!
        @brief Test all generatoe constructors
        """
        from code_tools_grocsoftware.base.comment_gen_tools import CCommentGenerator

        generator = CCommentGenerator()
        self.assertIsNone(generator.lineLength)
        self.assertIsNone(generator.eoltext)
        self.assertFalse(generator.useSingleLine)
        self.assertEqual(generator.eolLength, 0)
        self.assertEqual(generator.commentData['blockStart'], '/*')
        self.assertEqual(generator.commentData['blockEnd'], '*/')
        self.assertEqual(generator.commentData['blockLineStart'], '* ')
        self.assertEqual(generator.commentData['singleLine'], '//')
        self.assertEqual(generator.eolLength, 0)

    def test052TestPyCommentConstructor(self):
        """!
        @brief Test all generatoe constructors
        """
        from code_tools_grocsoftware.base.comment_gen_tools import PyCommentGenerator

        generator = PyCommentGenerator()
        self.assertIsNone(generator.lineLength)
        self.assertIsNone(generator.eoltext)
        self.assertFalse(generator.useSingleLine)
        self.assertEqual(generator.eolLength, 0)
        self.assertEqual(generator.commentData['blockStart'], '"""')
        self.assertEqual(generator.commentData['blockEnd'], '"""')
        self.assertEqual(generator.commentData['blockLineStart'], '')
        self.assertEqual(generator.commentData['singleLine'], '#')
        self.assertEqual(generator.eolLength, 0)

    def test053TestTsCommentConstructor(self):
        """!
        @brief Test all generatoe constructors
        """
        from code_tools_grocsoftware.base.comment_gen_tools import TsCommentGenerator

        generator = TsCommentGenerator()
        self.assertIsNone(generator.lineLength)
        self.assertIsNone(generator.eoltext)
        self.assertFalse(generator.useSingleLine)
        self.assertEqual(generator.eolLength, 0)
        self.assertEqual(generator.commentData['blockStart'], '/*')
        self.assertEqual(generator.commentData['blockEnd'], '*/')
        self.assertEqual(generator.commentData['blockLineStart'], '* ')
        self.assertEqual(generator.commentData['singleLine'], '//')
        self.assertEqual(generator.eolLength, 0)

    def test054TestJsCommentConstructor(self):
        """!
        @brief Test all generatoe constructors
        """
        from code_tools_grocsoftware.base.comment_gen_tools import JsCommentGenerator

        generator = JsCommentGenerator()
        self.assertIsNone(generator.lineLength)
        self.assertIsNone(generator.eoltext)
        self.assertFalse(generator.useSingleLine)
        self.assertEqual(generator.eolLength, 0)
        self.assertEqual(generator.commentData['blockStart'], '/*')
        self.assertEqual(generator.commentData['blockEnd'], '*/')
        self.assertEqual(generator.commentData['blockLineStart'], '* ')
        self.assertEqual(generator.commentData['singleLine'], '//')
        self.assertEqual(generator.eolLength, 0)

    def test055TestJsCommentConstructor(self):
        """!
        @brief Test all generatoe constructors
        """
        from code_tools_grocsoftware.base.comment_gen_tools import BashCommentGenerator

        generator = BashCommentGenerator()
        self.assertIsNone(generator.lineLength)
        self.assertIsNone(generator.eoltext)
        self.assertTrue(generator.useSingleLine)
        self.assertEqual(generator.eolLength, 0)
        self.assertIsNone(generator.commentData['blockStart'])
        self.assertIsNone(generator.commentData['blockEnd'])
        self.assertEqual(generator.commentData['blockLineStart'], '#')
        self.assertEqual(generator.commentData['singleLine'], '#')
        self.assertEqual(generator.eolLength, 0)

    def test056TestJsCommentConstructor(self):
        """!
        @brief Test all generatoe constructors
        """
        from code_tools_grocsoftware.base.comment_gen_tools import BatchCommentGenerator

        generator = BatchCommentGenerator()
        self.assertIsNone(generator.lineLength)
        self.assertIsNone(generator.eoltext)
        self.assertTrue(generator.useSingleLine)
        self.assertEqual(generator.eolLength, 0)
        self.assertIsNone(generator.commentData['blockStart'])
        self.assertIsNone(generator.commentData['blockEnd'])
        self.assertEqual(generator.commentData['blockLineStart'], 'REM ')
        self.assertEqual(generator.commentData['singleLine'], 'REM ')
        self.assertEqual(generator.eolLength, 0)


if __name__ == '__main__':
    unittest.main()