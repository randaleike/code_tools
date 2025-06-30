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



from dir_init import pathincsetup
pathincsetup()

from code_tools_grocsoftware.base.text_format import MultiLineFormat

class TestUnittest01MultiLineFormat:
    """!
    @brief Unit test for the MultiLineFormat function
    """
    def test01SingleLine(self):
        """!
        @brief Test simple case of a short line
        """
        strList = MultiLineFormat("Test return description")
        assert 1 == len(strList)
        assert "Test return description" == strList[0]

    def test02DoubleLine(self):
        """!
        @brief Test simple case of a short line
        """
        strList = MultiLineFormat("Test return description, longer line to induce wrap", 27)
        assert 2 == len(strList)
        assert "Test return description," == strList[0]
        assert "longer line to induce wrap" == strList[1]

    def test03DoubleLineWithPad(self):
        """!
        @brief Test simple case of a short line
        """
        strList = MultiLineFormat("Test return description, longer line to induce wrap", 27, '-')
        assert 2 == len(strList)
        assert "Test return description,---" == strList[0]
        assert "longer line to induce wrap-" == strList[1]

    def test04DoubleLineWithNoGoodBreak(self):
        """!
        @brief Test simple case of a short line
        """
        strList = MultiLineFormat("Testreturndescriptionlongerlinetoinducewrap", 27)
        assert 2 == len(strList)
        assert "Testreturndescriptionlonger" == strList[0]
        assert "linetoinducewrap" == strList[1]

    def test05TripleLine(self):
        """!
        @brief Test simple case of a short line
        """
        strList = MultiLineFormat("Test return description, longer line to induce wrap. More text to create another line", 32)
        assert 3 == len(strList)
        assert "Test return description, longer" == strList[0]
        assert "line to induce wrap. More text" == strList[1]
        assert "to create another line" == strList[2]
