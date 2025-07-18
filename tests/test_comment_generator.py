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

from code_tools_grocsoftware.base.comment_gen_tools import CommentGenerator

from code_tools_grocsoftware.base.comment_gen_tools import CCommentGenerator
from code_tools_grocsoftware.base.comment_gen_tools import PyCommentGenerator
from code_tools_grocsoftware.base.comment_gen_tools import TsCommentGenerator
from code_tools_grocsoftware.base.comment_gen_tools import JsCommentGenerator
from code_tools_grocsoftware.base.comment_gen_tools import BatchCommentGenerator
from code_tools_grocsoftware.base.comment_gen_tools import BashCommentGenerator

c_comment_parms =   {'blockStart': "/*", 'blockEnd': "*/", ''
                     'blockLineStart': "", 'singleLine': "//"}

py_comment_parms =  {'blockStart': "\"\"\"", 'blockEnd':"\"\"\"",
                     'blockLineStart': "", 'singleLine': "#"}

sh_comment_parms =  {'blockStart': None, 'blockEnd': None,
                     'blockLineStart': "#", 'singleLine': "#"}

bat_comment_parms = {'blockStart': None, 'blockEnd': None,
                     'blockLineStart': "REM ", 'singleLine': "REM ",}

class Test07CommentGeneration:
    """!
    @brief Unit test for the CommentGenerator class
    """
    def test001_c_header_generation_default(self):
        """!
        @brief Test c file type files comment block header generation
        default constructor
        """
        generator = CommentGenerator(c_comment_parms)

        header = generator.build_comment_block_header()
        assert len(header) == 1
        assert header[0] == "/*"

        header = generator.build_comment_block_header(2)
        assert len(header) == 2
        assert header[0] == "/*"
        assert header[1] == ""

        header = generator.build_comment_block_header(3)
        assert len(header) == 3
        assert header[0] == "/*"
        assert header[1] == ""
        assert header[2] == ""

    def test002_c_header_generation_pad(self):
        """!
        @brief Test c file type files comment block header generation
        padded line constructor
        """
        generator = CommentGenerator(c_comment_parms, 10)

        header = generator.build_comment_block_header(1, '=')
        assert len(header) == 1
        assert header[0] == "/*========"

        header = generator.build_comment_block_header(2, '=')
        assert len(header) == 2
        assert header[0] == "/*========"
        assert header[1] == "=========="

        header = generator.build_comment_block_header(3, '=')
        assert len(header) == 3
        assert header[0] == "/*========"
        assert header[1] == "=========="
        assert header[2] == "=========="

    def test003_c_header_generation_pad_and_eol(self):
        """!
        @brief Test c file type files comment block header generation
        padded line and end of line constructor
        """
        generator = CommentGenerator(c_comment_parms, 10, "*")

        header = generator.build_comment_block_header(1, '=')
        assert len(header) == 1
        assert header[0] == "/*=======*"

        header = generator.build_comment_block_header(2, '=')
        assert len(header) == 2
        assert header[0] == "/*=======*"
        assert header[1] == "=========*"

        header = generator.build_comment_block_header(3, '=')
        assert len(header) == 3
        assert header[0] == "/*=======*"
        assert header[1] == "=========*"
        assert header[2] == "=========*"

    def test004_c_header_generation_pad_and_eol2(self):
        """!
        @brief Test c file type files comment block header generation
        padded line and end of line constructor
        """
        generator = CommentGenerator(c_comment_parms, 10, " *")

        header = generator.build_comment_block_header(1, '=')
        assert len(header) == 1
        assert header[0] == "/*====== *"

        header = generator.build_comment_block_header(2, '=')
        assert len(header) == 2
        assert header[0] == "/*====== *"
        assert header[1] == "======== *"

        header = generator.build_comment_block_header(3, '=')
        assert header[0] == "/*====== *"
        assert header[1] == "======== *"
        assert header[2] == "======== *"


    def test005_c_header_generation_force_single(self):
        """!
        @brief Test c file type files comment block header generation
        forced single line constructor
        """
        generator = CommentGenerator(c_comment_parms, use_single_line = True)

        header = generator.build_comment_block_header()
        assert len(header) == 1
        assert header[0] == "//"

        header = generator.build_comment_block_header(2)
        assert len(header) == 2
        assert header[0] == "//"
        assert header[1] == "//"

        header = generator.build_comment_block_header(3)
        assert len(header) == 3
        assert header[0] == "//"
        assert header[1] == "//"
        assert header[2] == "//"

    def test006_c_header_generation_force_single_pad(self):
        """!
        @brief Test c file type files comment block header generation
        padded, forced single line constructor
        """
        generator = CommentGenerator(c_comment_parms, 10, use_single_line = True)

        header = generator.build_comment_block_header(1)
        assert len(header) == 1
        assert header[0] == "//--------"

        header = generator.build_comment_block_header(2)
        assert len(header) == 2
        assert header[0] == "//--------"
        assert header[1] == "//--------"

        header = generator.build_comment_block_header(3, '=')
        assert len(header) == 3
        assert header[0] == "//========"
        assert header[1] == "//========"
        assert header[2] == "//========"

    def test007_c_header_generation_force_single_pad_eol(self):
        """!
        @brief Test c file type files comment block header generation
        padded, end of line text, forced single line constructor
        """
        generator = CommentGenerator(c_comment_parms, 10, " *", use_single_line = True)

        header = generator.build_comment_block_header(1, '=')
        assert len(header) == 1
        assert header[0] == "//====== *"

        header = generator.build_comment_block_header(2)
        assert len(header) == 2
        assert header[0] == "//------ *"
        assert header[1] == "//------ *"

        header = generator.build_comment_block_header(3, '=')
        assert len(header) == 3
        assert header[0] == "//====== *"
        assert header[1] == "//====== *"
        assert header[2] == "//====== *"

    def test011_c_footer_generation_default(self):
        """!
        @brief Test c file type files comment block footer generation
        default constructor
        """
        generator = CommentGenerator(c_comment_parms)

        footer = generator.build_comment_block_footer()
        assert len(footer) == 1
        assert footer[0] == "*/"

        footer = generator.build_comment_block_footer(2)
        assert len(footer) == 2
        assert footer[0] == ""
        assert footer[1] == "*/"

        footer = generator.build_comment_block_footer(3)
        assert len(footer) == 3
        assert footer[0] == ""
        assert footer[1] == ""
        assert footer[2] == "*/"

    def test012_c_footer_generation_pad(self):
        """!
        @brief Test c file type files comment block footer generation
        padded line constructor
        """
        generator = CommentGenerator(c_comment_parms, 10)

        footer = generator.build_comment_block_footer(1, '=')
        assert len(footer) == 1
        assert footer[0] == "========*/"

        footer = generator.build_comment_block_footer(2, '=')
        assert len(footer) == 2
        assert footer[0] == "=========="
        assert footer[1] == "========*/"

        footer = generator.build_comment_block_footer(3, '=')
        assert len(footer) == 3
        assert footer[0] == "=========="
        assert footer[1] == "=========="
        assert footer[2] == "========*/"

    def test013_c_footer_generation_pad_and_eol(self):
        """!
        @brief Test c file type files comment block footer generation
        padded line and end of line constructor
        """
        generator = CommentGenerator(c_comment_parms, 10, "*")

        footer = generator.build_comment_block_footer(1, '=')
        assert len(footer) == 1
        assert footer[0] == "========*/"

        footer = generator.build_comment_block_footer(2, '=')
        assert len(footer) == 2
        assert footer[0] == "=========*"
        assert footer[1] == "========*/"

        footer = generator.build_comment_block_footer(3, '=')
        assert len(footer) == 3
        assert footer[0] == "=========*"
        assert footer[1] == "=========*"
        assert footer[2] == "========*/"

    def test014_c_footer_generation_pad_and_eol2(self):
        """!
        @brief Test c file type files comment block footer generation
        padded line and end of line constructor
        """
        generator = CommentGenerator(c_comment_parms, 10, " *")

        footer = generator.build_comment_block_footer(1, '=')
        assert len(footer) == 1
        assert footer[0] == "========*/"

        footer = generator.build_comment_block_footer(2, '=')
        assert len(footer) == 2
        assert footer[0] == "======== *"
        assert footer[1] == "========*/"

        footer = generator.build_comment_block_footer(3, '=')
        assert footer[0] == "======== *"
        assert footer[1] == "======== *"
        assert footer[2] == "========*/"

    def test015_c_footer_generation_force_single(self):
        """!
        @brief Test c file type files comment footer footer generation
        forced single line constructor
        """
        generator = CommentGenerator(c_comment_parms, use_single_line = True)

        footer = generator.build_comment_block_footer()
        assert len(footer) == 1
        assert footer[0] == "//"

        footer = generator.build_comment_block_footer(2)
        assert len(footer) == 2
        assert footer[0] == "//"
        assert footer[1] == "//"

        footer = generator.build_comment_block_footer(3)
        assert len(footer) == 3
        assert footer[0] == "//"
        assert footer[1] == "//"
        assert footer[2] == "//"

    def test016_c_footer_generation_force_single_pad(self):
        """!
        @brief Test c file type files comment block footer generation
        padded, forced single line constructor
        """
        generator = CommentGenerator(c_comment_parms, 10, use_single_line = True)

        footer = generator.build_comment_block_footer(1, '=')
        assert len(footer) == 1
        assert footer[0] == "//========"

        footer = generator.build_comment_block_footer(2,)
        assert footer[0] == "//--------"
        assert footer[1] == "//--------"

        footer = generator.build_comment_block_footer(3, '=')
        assert len(footer) == 3
        assert footer[0] == "//========"
        assert footer[1] == "//========"
        assert footer[2] == "//========"

    def test017_c_footer_generation_force_single_pad_eol(self):
        """!
        @brief Test c file type files comment block footer generation
        padded, end of line text, forced single line constructor
        """
        generator = CommentGenerator(c_comment_parms, 10, " *", use_single_line = True)

        footer = generator.build_comment_block_footer(1, '=')
        assert len(footer) == 1
        assert footer[0] == "//====== *"

        footer = generator.build_comment_block_footer(2)
        assert len(footer) == 2
        assert footer[0] == "//------ *"
        assert footer[1] == "//------ *"

        footer = generator.build_comment_block_footer(3, '=')
        assert len(footer) == 3
        assert footer[0] == "//====== *"
        assert footer[1] == "//====== *"
        assert footer[2] == "//====== *"

    def test021_c_wrap(self):
        """!
        @brief Test c file type files comment line wrapper generation
        Default constructor
        """
        generator = CommentGenerator(c_comment_parms)

        wrap = generator.wrap_comment_line("test line")
        assert wrap == "test line"

    def test022_c_wrap_pad(self):
        """!
        @brief Test c file type files comment line wrapper generation
        padded
        """
        generator = CommentGenerator(c_comment_parms, 10)

        wrap = generator.wrap_comment_line("test line")
        assert wrap == "test line"

    def test022_c_wrap_pad1(self):
        """!
        @brief Test c file type files comment line wrapper generation
        padded
        """
        generator = CommentGenerator(c_comment_parms, 12)

        wrap = generator.wrap_comment_line("test line")
        assert wrap == "test line"

    def test023_c_wrap_single(self):
        """!
        @brief Test c file type files comment block footer generation
        forced single line constructor
        """
        generator = CommentGenerator(c_comment_parms, use_single_line = True)

        wrap = generator.wrap_comment_line("test line")
        assert wrap == "// test line"

    def test024_c_wrap_single(self):
        """!
        @brief Test c file type files comment block footer generation
        padded, forced single line constructor
        """
        generator = CommentGenerator(c_comment_parms, 15, use_single_line = True)

        wrap = generator.wrap_comment_line("test line")
        assert wrap == "// test line"

    def test025_c_wrap_pad_and_eol(self):
        """!
        @brief Test c file type files comment line wrapper generation
        padded, end of line
        """
        generator = CommentGenerator(c_comment_parms, 12, " *")

        wrap = generator.wrap_comment_line("test line")
        assert wrap == "test line  *"

    def test026_c_wrap_pad_and_eol(self):
        """!
        @brief Test c file type files comment line wrapper generation
        padded, end of line, forced single line
        """
        generator = CommentGenerator(c_comment_parms, 15, " *", use_single_line = True)

        wrap = generator.wrap_comment_line("test line")
        assert wrap == "// test line  *"

    def test031_python_default(self):
        """!
        @brief Test python file type files comment generation
        default constructor
        """
        generator = CommentGenerator(py_comment_parms)

        header = generator.build_comment_block_header()
        footer = generator.build_comment_block_footer()
        assert len(header) == 1
        assert header[0] == "\"\"\""
        assert len(footer) == 1
        assert footer[0] == "\"\"\""

        header = generator.build_comment_block_header(2)
        footer = generator.build_comment_block_footer(2)
        assert len(header) == 2
        assert header[0] == "\"\"\""
        assert header[1] == ""
        assert len(footer) == 2
        assert footer[0] == ""
        assert footer[1] == "\"\"\""

        wrap = generator.wrap_comment_line("test line")
        assert wrap == "test line"

    def test032_python_pad(self):
        """!
        @brief Test python file type files comment generation
        padded
        """
        generator = CommentGenerator(py_comment_parms, 10)

        header = generator.build_comment_block_header()
        footer = generator.build_comment_block_footer()
        assert len(header) == 1
        assert header[0] == "\"\"\"-------"
        assert len(footer) == 1
        assert footer[0] == "-------\"\"\""

        header = generator.build_comment_block_header(2)
        footer = generator.build_comment_block_footer(2)
        assert len(header) == 2
        assert header[0] == "\"\"\"-------"
        assert header[1] == "----------"
        assert len(footer) == 2
        assert footer[0] == "----------"
        assert footer[1] == "-------\"\"\""

        wrap = generator.wrap_comment_line("test line")
        assert wrap == "test line"

    def test033_python_pad_eol(self):
        """!
        @brief Test python file type files comment generation
        padded, end of line
        """
        generator = CommentGenerator(py_comment_parms, 13, " *")

        header = generator.build_comment_block_header()
        footer = generator.build_comment_block_footer()
        assert len(header) == 1
        assert header[0] == "\"\"\"-------- *"
        assert len(footer) == 1
        assert footer[0] == "----------\"\"\""

        header = generator.build_comment_block_header(2)
        footer = generator.build_comment_block_footer(2)
        assert len(header) == 2
        assert header[0] == "\"\"\"-------- *"
        assert header[1] == "----------- *"
        assert len(footer) == 2
        assert footer[0] == "----------- *"
        assert footer[1] == "----------\"\"\""

        wrap = generator.wrap_comment_line("test line")
        assert wrap == "test line   *"

    def test034_python_force_single(self):
        """!
        @brief Test python file type files comment generation
        force single
        """
        generator = CommentGenerator(py_comment_parms, use_single_line = True)

        header = generator.build_comment_block_header()
        footer = generator.build_comment_block_footer()
        assert len(header) == 1
        assert header[0] == "#"
        assert len(footer) == 1
        assert footer[0] == "#"

        header = generator.build_comment_block_header(2)
        footer = generator.build_comment_block_footer(2)
        assert len(header) == 2
        assert header[0] == "#"
        assert header[1] == "#"
        assert len(footer) == 2
        assert footer[0] == "#"
        assert footer[1] == "#"

        wrap = generator.wrap_comment_line("test line")
        assert wrap == "# test line"

    def test035_python_pad_force_single(self):
        """!
        @brief Test python file type files comment generation
        padded, force single
        """
        generator = CommentGenerator(py_comment_parms, 12, use_single_line = True)

        header = generator.build_comment_block_header(1, '=')
        footer = generator.build_comment_block_footer(1, '=')
        assert len(header) == 1
        assert header[0] == "#==========="
        assert len(footer) == 1
        assert footer[0] == "#==========="

        header = generator.build_comment_block_header(2, '=')
        footer = generator.build_comment_block_footer(2, '=')
        assert len(header) == 2
        assert header[0] == "#==========="
        assert header[1] == "#==========="
        assert len(footer) == 2
        assert footer[0] == "#==========="
        assert footer[1] == "#==========="

        wrap = generator.wrap_comment_line("test line")
        assert wrap == "# test line"

    def test036_python_pad_eol_force_single(self):
        """!
        @brief Test python file type files comment generation
        padded, end of line, force single
        """
        generator = CommentGenerator(py_comment_parms, 15, " *", use_single_line = True)

        header = generator.build_comment_block_header(1, '=')
        footer = generator.build_comment_block_footer(1, '=')
        assert len(header) == 1
        assert header[0] == "#============ *"
        assert len(footer) == 1
        assert footer[0] == "#============ *"

        header = generator.build_comment_block_header(2, '=')
        footer = generator.build_comment_block_footer(2, '=')
        assert len(header) == 2
        assert header[0] == "#============ *"
        assert header[1] == "#============ *"
        assert len(footer) == 2
        assert footer[0] == "#============ *"
        assert footer[1] == "#============ *"

        wrap = generator.wrap_comment_line("test line")
        assert wrap == "# test line   *"

    def test041_shell_default(self):
        """!
        @brief Test shell script file type files comment generation
        default constructor
        """
        generator = CommentGenerator(sh_comment_parms)

        header = generator.build_comment_block_header()
        footer = generator.build_comment_block_footer()
        assert len(header) == 1
        assert header[0] == "#"
        assert len(footer) == 1
        assert footer[0] == "#"

        header = generator.build_comment_block_header(2)
        footer = generator.build_comment_block_footer(2)
        assert len(header) == 2
        assert header[0] == "#"
        assert header[1] == "#"
        assert len(footer) == 2
        assert footer[0] == "#"
        assert footer[1] == "#"

        wrap = generator.wrap_comment_line("test line")
        assert wrap == "# test line"

    def test042_shell_pad(self):
        """!
        @brief Test shell script file type files comment generation
        padded
        """
        generator = CommentGenerator(sh_comment_parms, 10)

        header = generator.build_comment_block_header()
        footer = generator.build_comment_block_footer()
        assert len(header) == 1
        assert header[0] == "#---------"
        assert len(footer) == 1
        assert footer[0] == "#---------"

        header = generator.build_comment_block_header(2)
        footer = generator.build_comment_block_footer(2)
        assert len(header) == 2
        assert header[0] == "#---------"
        assert header[1] == "#---------"
        assert len(footer) == 2
        assert footer[0] == "#---------"
        assert footer[1] == "#---------"

        wrap = generator.wrap_comment_line("test line")
        assert wrap == "# test line"

    def test043_shell_pad_eol(self):
        """!
        @brief Test shell script file type files comment generation
        padded, end of line
        """
        generator = CommentGenerator(sh_comment_parms, 13, " *")

        header = generator.build_comment_block_header()
        footer = generator.build_comment_block_footer()
        assert len(header) == 1
        assert header[0] == "#---------- *"
        assert len(footer) == 1
        assert footer[0] == "#---------- *"

        header = generator.build_comment_block_header(2)
        footer = generator.build_comment_block_footer(2)
        assert len(header) == 2
        assert header[0] == "#---------- *"
        assert header[1] == "#---------- *"
        assert len(footer) == 2
        assert footer[0] == "#---------- *"
        assert footer[1] == "#---------- *"

        wrap = generator.wrap_comment_line("test line")
        assert wrap == "# test line *"

    def test044_shell_force(self):
        """!
        @brief Test shell script file type files comment generation
        force single
        """
        generator = CommentGenerator(sh_comment_parms, use_single_line = True)

        header = generator.build_comment_block_header()
        footer = generator.build_comment_block_footer()
        assert len(header) == 1
        assert header[0] == "#"
        assert len(footer) == 1
        assert footer[0] == "#"

        header = generator.build_comment_block_header(2)
        footer = generator.build_comment_block_footer(2)
        assert len(header) == 2
        assert header[0] == "#"
        assert header[1] == "#"
        assert len(footer) == 2
        assert footer[0] == "#"
        assert footer[1] == "#"

        wrap = generator.wrap_comment_line("test line")
        assert wrap == "# test line"

    def test045_shell_force_pad(self):
        """!
        @brief Test shell script file type files comment generation
        force single, padded
        """
        generator = CommentGenerator(sh_comment_parms, 10, use_single_line = True)

        header = generator.build_comment_block_header()
        footer = generator.build_comment_block_footer()
        assert len(header) == 1
        assert header[0] == "#---------"
        assert len(footer) == 1
        assert footer[0] == "#---------"

        header = generator.build_comment_block_header(2)
        footer = generator.build_comment_block_footer(2)
        assert len(header) == 2
        assert header[0] == "#---------"
        assert header[1] == "#---------"
        assert len(footer) == 2
        assert footer[0] == "#---------"
        assert footer[1] == "#---------"

        wrap = generator.wrap_comment_line("test line")
        assert wrap == "# test line"

    def test046_shell_force_pad_eol(self):
        """!
        @brief Test shell script file type files comment generation
        force single, padded, end of line
        """
        generator = CommentGenerator(sh_comment_parms, 13, " *", use_single_line = True)

        header = generator.build_comment_block_header()
        footer = generator.build_comment_block_footer()
        assert len(header) == 1
        assert header[0] == "#---------- *"
        assert len(footer) == 1
        assert footer[0] == "#---------- *"

        header = generator.build_comment_block_header(2)
        footer = generator.build_comment_block_footer(2)
        assert len(header) == 2
        assert header[0] == "#---------- *"
        assert header[1] == "#---------- *"
        assert len(footer) == 2
        assert footer[0] == "#---------- *"
        assert footer[1] == "#---------- *"

        wrap = generator.wrap_comment_line("test line")
        assert wrap == "# test line *"

    def test050_gen_single_line(self):
        """!
        @brief Test file type files single line comment generation
        """
        generator = CommentGenerator(sh_comment_parms)
        assert generator.generate_single_line_comment("test text") == "# test text"

        generator1 = CommentGenerator(c_comment_parms)
        assert generator1.generate_single_line_comment("test text") == "// test text"

        generator2 = CommentGenerator(py_comment_parms)
        assert generator2.generate_single_line_comment("test text") == "# test text"

    def test051_test_c_comment_constructor(self):
        """!
        @brief Test all generatoe constructors
        """
        generator = CCommentGenerator()
        assert generator.line_length is None
        assert generator.eoltext is None
        assert not generator.use_single_line
        assert generator.eol_length == 0
        assert generator.comment_data['blockStart'] == '/*'
        assert generator.comment_data['blockEnd'] == '*/'
        assert generator.comment_data['blockLineStart'] == '* '
        assert generator.comment_data['singleLine'] == '//'
        assert generator.eol_length == 0

    def test052_test_py_comment_constructor(self):
        """!
        @brief Test all generatoe constructors
        """
        generator = PyCommentGenerator()
        assert generator.line_length is None
        assert generator.eoltext is None
        assert not generator.use_single_line
        assert generator.eol_length == 0
        assert generator.comment_data['blockStart'] == '"""'
        assert generator.comment_data['blockEnd'] == '"""'
        assert generator.comment_data['blockLineStart'] == ''
        assert generator.comment_data['singleLine'] == '#'
        assert generator.eol_length == 0

    def test053_test_ts_comment_constructor(self):
        """!
        @brief Test all generatoe constructors
        """
        generator = TsCommentGenerator()
        assert generator.line_length is None
        assert generator.eoltext is None
        assert not generator.use_single_line
        assert generator.eol_length == 0
        assert generator.comment_data['blockStart'] == '/*'
        assert generator.comment_data['blockEnd'] == '*/'
        assert generator.comment_data['blockLineStart'] == '* '
        assert generator.comment_data['singleLine'] == '//'
        assert generator.eol_length == 0

    def test054_test_js_comment_constructor(self):
        """!
        @brief Test all generatoe constructors
        """
        generator = JsCommentGenerator()
        assert generator.line_length is None
        assert generator.eoltext is None
        assert not generator.use_single_line
        assert generator.eol_length == 0
        assert generator.comment_data['blockStart'] == '/*'
        assert generator.comment_data['blockEnd'] == '*/'
        assert generator.comment_data['blockLineStart'] == '* '
        assert generator.comment_data['singleLine'] == '//'
        assert generator.eol_length == 0

    def test055_test_js_comment_constructor(self):
        """!
        @brief Test all generatoe constructors
        """
        generator = BashCommentGenerator()
        assert generator.line_length is None
        assert generator.eoltext is None
        assert generator.use_single_line
        assert generator.eol_length == 0
        assert generator.comment_data['blockStart'] is None
        assert generator.comment_data['blockEnd'] is None
        assert generator.comment_data['blockLineStart'] == '#'
        assert generator.comment_data['singleLine'] == '#'
        assert generator.eol_length == 0

    def test056_test_js_comment_constructor(self):
        """!
        @brief Test all generatoe constructors
        """
        generator = BatchCommentGenerator()
        assert generator.line_length is None
        assert generator.eoltext is None
        assert generator.use_single_line
        assert generator.eol_length == 0
        assert generator.comment_data['blockStart'] is None
        assert generator.comment_data['blockEnd'] is None
        assert generator.comment_data['blockLineStart'] == 'REM '
        assert generator.comment_data['singleLine'] == 'REM '
        assert generator.eol_length == 0
