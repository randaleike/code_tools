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

from code_tools_grocsoftware.base.text_format import MultiLineFormat

class Test01MultiLineFormat:
    """!
    @brief Unit test for the MultiLineFormat function
    """
    def test01_single_line(self):
        """!
        @brief Test simple case of a short line
        """
        str_list = MultiLineFormat("Test return description")
        assert 1 == len(str_list)
        assert "Test return description" == str_list[0]

    def test02_double_line(self):
        """!
        @brief Test simple case of a short line
        """
        str_list = MultiLineFormat("Test return description, longer line to induce wrap", 27)
        assert 2 == len(str_list)
        assert "Test return description," == str_list[0]
        assert "longer line to induce wrap" == str_list[1]

    def test03_double_line_with_pad(self):
        """!
        @brief Test simple case of a short line
        """
        str_list = MultiLineFormat("Test return description, longer line to induce wrap", 27, '-')
        assert 2 == len(str_list)
        assert "Test return description,---" == str_list[0]
        assert "longer line to induce wrap-" == str_list[1]

    def test04_double_line_with_no_good_break(self):
        """!
        @brief Test simple case of a short line
        """
        str_list = MultiLineFormat("Testreturndescriptionlongerlinetoinducewrap", 27)
        assert 2 == len(str_list)
        assert "Testreturndescriptionlonger" == str_list[0]
        assert "linetoinducewrap" == str_list[1]

    def test05_triple_line(self):
        """!
        @brief Test simple case of a short line
        """
        str_list = MultiLineFormat("Test return description, longer line to induce wrap. More text to create another line", 32)
        assert 3 == len(str_list)
        assert "Test return description, longer" == str_list[0]
        assert "line to induce wrap. More text" == str_list[1]
        assert "to create another line" == str_list[2]
