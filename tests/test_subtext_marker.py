"""@package test_programmer_tools
Unittest for programmer base tools utility

"""

#==========================================================================
# Copyright (c) 2024 Randal Eike
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

from code_tools.base.copyright_tools import SubTextMarker

class TestClass01CopyrightSubtextMarker(unittest.TestCase):
    """!
    @brief Unit test for the copyright SubTextMarker class
    """
    def test001ConstructorSimple(self):
        """!
        @brief Test simple input
        """
        testObj = SubTextMarker("test", 10)
        self.assertEqual(testObj.text, "test")
        self.assertEqual(testObj.start, 10)
        self.assertEqual(testObj.end, 14)

    def test002ConstructorPadded(self):
        """!
        @brief Test simple input
        """
        testObj = SubTextMarker(" test ", 10)
        self.assertEqual(testObj.text, "test")
        self.assertEqual(testObj.start, 11)
        self.assertEqual(testObj.end, 15)

    def test003ConstructorTabPadded(self):
        """!
        @brief Test simple input
        """
        testObj = SubTextMarker("\ttest\t", 10)
        self.assertEqual(testObj.text, "test")
        self.assertEqual(testObj.start, 11)
        self.assertEqual(testObj.end, 15)

    def test004ConstructorExtraPadded(self):
        """!
        @brief Test simple input
        """
        testObj = SubTextMarker("  test  ", 10)
        self.assertEqual(testObj.text, "test")
        self.assertEqual(testObj.start, 12)
        self.assertEqual(testObj.end, 16)

if __name__ == '__main__':
    unittest.main()