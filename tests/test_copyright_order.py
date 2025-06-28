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

from code_tools_grocsoftware.base.copyright_tools import CopyrightParseOrder1
from code_tools_grocsoftware.base.copyright_tools import CopyrightParseOrder2

class TestClass04CopyrightParserOrder1(unittest.TestCase):
    """!
    @brief Unit test for the copyright parser order1 class
    """
    def setUp(self):
        self.tstParser = CopyrightParseOrder1(copyrightSearchMsg = r'Copyright|COPYRIGHT|copyright',
                                              copyrightSearchTag = r'\([cC]\)',
                                              copyrightSearchDate = r'(\d{4})',
                                              copyrightOwnerSpec = r'[a-zA-Z0-9,\./\- @]',
                                              useUnicode = False)

    def test001IsCopyright(self):
        """!
        @brief Test the isCopyrightLine method
        """
        self.assertTrue(self.tstParser.isCopyrightLine(" Copyright (c) 2024 Me"))
        self.assertTrue(self.tstParser.isCopyrightLine(" copyright (c)  2024 Me"))
        self.assertTrue(self.tstParser.isCopyrightLine(" COPYRIGHT (c)  2024  Me"))
        self.assertTrue(self.tstParser.isCopyrightLine(" Copyright  (c)   2024-2025   foo"))
        self.assertTrue(self.tstParser.isCopyrightLine(" copyright (c) 2024-2025 you"))
        self.assertTrue(self.tstParser.isCopyrightLine(" COPYRIGHT (c) 2024,2025 You"))

        self.assertTrue(self.tstParser.isCopyrightLine(" Copyright (C) 2024 her"))
        self.assertTrue(self.tstParser.isCopyrightLine(" copyright (C) 2024 them"))
        self.assertTrue(self.tstParser.isCopyrightLine(" COPYRIGHT (C) 2024 other"))
        self.assertTrue(self.tstParser.isCopyrightLine(" COPYRIGHT (C) 2024,2025 some body"))

        self.assertTrue(self.tstParser.isCopyrightLine("* COPYRIGHT (C) 2024,2025 some body     *"))

    def test002IsCopyrightMissingFail(self):
        """!
        @brief Test the isCopyrightLine() method, failed for missing components
        """
        self.assertFalse(self.tstParser.isCopyrightLine(" Copy right (c) 2024 Me"))
        self.assertFalse(self.tstParser.isCopyrightLine(" Copyright (a) 2024 Me"))
        self.assertFalse(self.tstParser.isCopyrightLine(" Copyright (c) Me"))
        self.assertFalse(self.tstParser.isCopyrightLine(" Copyright c 2024 Me"))
        self.assertFalse(self.tstParser.isCopyrightLine(" Random text 2024 Me"))
        self.assertFalse(self.tstParser.isCopyrightLine(" COPYRIGHT (C) 2024,2025"))

    def test003IsCopyrightOrderFail(self):
        """!
        @brief Test the isCopyrightLine() method, failed for invalid order
        """
        self.assertFalse(self.tstParser.isCopyrightLine(" (c) Copyright 2024 Me"))
        self.assertFalse(self.tstParser.isCopyrightLine(" 2024 Copyright (c) Me"))
        self.assertFalse(self.tstParser.isCopyrightLine(" me Copyright (c) 2024"))
        self.assertFalse(self.tstParser.isCopyrightLine(" Copyright (c) me 2024"))
        self.assertFalse(self.tstParser.isCopyrightLine(" Copyright 2022-2024 (c) me"))

    def test004ParseMsg(self):
        """!
        @brief Test the parseCopyrightMsg() method.

        Basic test as TestClass02CopyrightParserBase does a more complete job
        of testing the component functiions that this function calls
        """
        self.tstParser.parseCopyrightMsg(" Copyright (c) 2024 Me")
        self.assertTrue(self.tstParser.copyrightTextValid)
        self.assertEqual(self.tstParser.copyrightText, " Copyright (c) 2024 Me")
        self.assertEqual(self.tstParser.copyrightTextStart, " ")
        self.assertEqual(self.tstParser.copyrightTextMsg, "Copyright")
        self.assertEqual(self.tstParser.copyrightTextTag, "(c)")
        self.assertEqual(self.tstParser.copyrightTextOwner, "Me")
        self.assertIsNone(self.tstParser.copyrightTextEol)
        self.assertEqual(len(self.tstParser.copyrightYearList), 1)

    def test005ParseMsgWithEol(self):
        """!
        @brief Test the parseCopyrightMsg() method.

        Basic test as TestClass02CopyrightParserBase does a more complete job
        of testing the component functiions that this function calls
        """
        self.tstParser.parseCopyrightMsg(" * Copyright (c) 2024 Me                 *")
        self.assertTrue(self.tstParser.copyrightTextValid)
        self.assertEqual(self.tstParser.copyrightText, " * Copyright (c) 2024 Me                 *")
        self.assertEqual(self.tstParser.copyrightTextStart, " * ")
        self.assertEqual(self.tstParser.copyrightTextMsg, "Copyright")
        self.assertEqual(self.tstParser.copyrightTextTag, "(c)")
        self.assertEqual(self.tstParser.copyrightTextOwner, "Me")
        self.assertEqual(self.tstParser.copyrightTextEol, "*")
        self.assertEqual(len(self.tstParser.copyrightYearList), 1)

    def test006CreateMsg(self):
        """!
        @brief Test the _createCopyrightMsg() method.
        """
        testStr = self.tstParser._createCopyrightMsg("James Kirk", "Copyright", "(c)", 2024, 2024)
        self.assertEqual(testStr, "Copyright (c) 2024 James Kirk")

        testStr = self.tstParser._createCopyrightMsg("James Kirk", "Copyright", "(c)", 2022, 2024)
        self.assertEqual(testStr, "Copyright (c) 2022-2024 James Kirk")

        testStr = self.tstParser._createCopyrightMsg("Mr. Spock", "Copyright", "(c)", 2024, None)
        self.assertEqual(testStr, "Copyright (c) 2024 Mr. Spock")

        testStr = self.tstParser._createCopyrightMsg("Mr. Spock", "Copyright", "(c)", 2023)
        self.assertEqual(testStr, "Copyright (c) 2023 Mr. Spock")

    def test007BuildNewMsg(self):
        """!
        @brief Test the buildNewCopyrightMsg() method.
        """
        self.tstParser.parseCopyrightMsg(" * Copyright (c) 2022 James Kirk               *")
        testStr = self.tstParser.buildNewCopyrightMsg(2024)
        self.assertEqual(testStr, "Copyright (c) 2024 James Kirk")

        testStr = self.tstParser.buildNewCopyrightMsg(2023, None)
        self.assertEqual(testStr, "Copyright (c) 2023 James Kirk")

        testStr = self.tstParser.buildNewCopyrightMsg(2023, 2024)
        self.assertEqual(testStr, "Copyright (c) 2023-2024 James Kirk")

        testStr = self.tstParser.buildNewCopyrightMsg(2024, addStartEnd=True)
        self.assertEqual(testStr, " * Copyright (c) 2024 James Kirk               *")

        testStr = self.tstParser.buildNewCopyrightMsg(2023, None, True)
        self.assertEqual(testStr, " * Copyright (c) 2023 James Kirk               *")

        testStr = self.tstParser.buildNewCopyrightMsg(2023, 2024, True)
        self.assertEqual(testStr, " * Copyright (c) 2023-2024 James Kirk          *")

    def test008BuildNewMsgNoParse(self):
        """!
        @brief Test the buildNewCopyrightMsg() method with no parsed data
        """
        testStr = self.tstParser.buildNewCopyrightMsg(2024)
        self.assertIsNone(testStr)

        testStr = self.tstParser.buildNewCopyrightMsg(2023, None)
        self.assertIsNone(testStr)

        testStr = self.tstParser.buildNewCopyrightMsg(2023, 2024)
        self.assertIsNone(testStr)

        testStr = self.tstParser.buildNewCopyrightMsg(2024, addStartEnd=True)
        self.assertIsNone(testStr)

        testStr = self.tstParser.buildNewCopyrightMsg(2023, None, True)
        self.assertIsNone(testStr)

        testStr = self.tstParser.buildNewCopyrightMsg(2023, 2024, True)
        self.assertIsNone(testStr)

class TestClass05CopyrightParserOrder2(unittest.TestCase):
    """!
    @brief Unit test for the copyright parser order1 class
    """
    def setUp(self):
        self.tstParser = CopyrightParseOrder2(copyrightSearchMsg = r'Copyright|COPYRIGHT|copyright',
                                              copyrightSearchTag = r'\([cC]\)',
                                              copyrightSearchDate = r'(\d{4})',
                                              copyrightOwnerSpec = r'[a-zA-Z0-9,\./\- @]',
                                              useUnicode = False)

    def test001IsCopyright(self):
        """!
        @brief Test the isCopyrightLine method
        """
        self.assertTrue(self.tstParser.isCopyrightLine(" Me Copyright (c) 2024"))
        self.assertTrue(self.tstParser.isCopyrightLine(" Me copyright (c)  2024"))
        self.assertTrue(self.tstParser.isCopyrightLine(" ME COPYRIGHT (c)  2024"))
        self.assertTrue(self.tstParser.isCopyrightLine(" foo  Copyright  (c)   2024-2025"))
        self.assertTrue(self.tstParser.isCopyrightLine(" you copyright (c) 2024-2025"))
        self.assertTrue(self.tstParser.isCopyrightLine(" You COPYRIGHT (c) 2024,2025"))

        self.assertTrue(self.tstParser.isCopyrightLine(" her Copyright (C) 2024"))
        self.assertTrue(self.tstParser.isCopyrightLine(" them copyright (C) 2024"))
        self.assertTrue(self.tstParser.isCopyrightLine(" other COPYRIGHT (C) 2024"))
        self.assertTrue(self.tstParser.isCopyrightLine(" some body COPYRIGHT (C) 2024,2025"))

        self.assertTrue(self.tstParser.isCopyrightLine("* some body COPYRIGHT (C) 2024,2025      *"))

    def test002IsCopyrightMissingFail(self):
        """!
        @brief Test the isCopyrightLine() method, failed for missing components
        """
        self.assertFalse(self.tstParser.isCopyrightLine(" Me Copy right (c) 2024"))
        self.assertFalse(self.tstParser.isCopyrightLine(" Me Copyright (a) 2024"))
        self.assertFalse(self.tstParser.isCopyrightLine(" Me Copyright (c)"))
        self.assertFalse(self.tstParser.isCopyrightLine(" Me Copyright c 2024"))
        self.assertFalse(self.tstParser.isCopyrightLine(" Me Random text 2024"))
        self.assertFalse(self.tstParser.isCopyrightLine(" COPYRIGHT (C) 2024,2025"))

    def test003IsCopyrightOrderFail(self):
        """!
        @brief Test the isCopyrightLine() method, failed for invalid order
        """
        self.assertFalse(self.tstParser.isCopyrightLine(" (c) Copyright 2024 Me"))
        self.assertFalse(self.tstParser.isCopyrightLine(" 2024 Copyright (c) Me"))
        self.assertFalse(self.tstParser.isCopyrightLine(" Copyright (c) 2024 Me"))
        self.assertFalse(self.tstParser.isCopyrightLine(" Copyright (c) me 2024"))
        self.assertFalse(self.tstParser.isCopyrightLine(" Me Copyright 2022-2024 (c)"))

    def test004ParseMsg(self):
        """!
        @brief Test the parseCopyrightMsg() method.

        Basic test as TestClass02CopyrightParserBase does a more complete job
        of testing the component functiions that this function calls
        """
        self.tstParser.parseCopyrightMsg(" Me Copyright (c) 2024")
        self.assertTrue(self.tstParser.copyrightTextValid)
        self.assertEqual(self.tstParser.copyrightText, " Me Copyright (c) 2024")
        self.assertEqual(self.tstParser.copyrightTextStart, " ")
        self.assertEqual(self.tstParser.copyrightTextMsg, "Copyright")
        self.assertEqual(self.tstParser.copyrightTextTag, "(c)")
        self.assertEqual(self.tstParser.copyrightTextOwner, "Me")
        self.assertIsNone(self.tstParser.copyrightTextEol)
        self.assertEqual(len(self.tstParser.copyrightYearList), 1)

    def test005ParseMsgWithEol(self):
        """!
        @brief Test the parseCopyrightMsg() method.

        Basic test as TestClass02CopyrightParserBase does a more complete job
        of testing the component functiions that this function calls
        """
        self.tstParser.parseCopyrightMsg(" * Me Copyright (c) 2024                 *")
        self.assertTrue(self.tstParser.copyrightTextValid)
        self.assertEqual(self.tstParser.copyrightText, " * Me Copyright (c) 2024                 *")
        self.assertEqual(self.tstParser.copyrightTextStart, " * ")
        self.assertEqual(self.tstParser.copyrightTextMsg, "Copyright")
        self.assertEqual(self.tstParser.copyrightTextTag, "(c)")
        self.assertEqual(self.tstParser.copyrightTextOwner, "Me")
        self.assertEqual(self.tstParser.copyrightTextEol, "*")
        self.assertEqual(len(self.tstParser.copyrightYearList), 1)

    def test006ParseMsgWithError(self):
        """!
        @brief Test the parseCopyrightMsg() method.

        Basic test as TestClass02CopyrightParserBase does a more complete job
        of testing the component functiions that this function calls
        """
        self.tstParser.parseCopyrightMsg(" * Me (c) 2024                 *")
        self.assertFalse(self.tstParser.copyrightTextValid)
        self.assertEqual(self.tstParser.copyrightText, "")
        self.assertEqual(self.tstParser.copyrightTextStart, "")

        self.assertIsNone(self.tstParser.copyrightTextMsg)
        self.assertEqual(self.tstParser.copyrightTextTag, "(c)")
        self.assertIsNone(self.tstParser.copyrightTextOwner)
        self.assertEqual(self.tstParser.copyrightTextEol, "*")
        self.assertEqual(len(self.tstParser.copyrightYearList), 1)

    def test007CreateMsg(self):
        """!
        @brief Test the _createCopyrightMsg() method.
        """
        testStr = self.tstParser._createCopyrightMsg("James Kirk", "Copyright", "(c)", 2024, 2024)
        self.assertEqual(testStr, "James Kirk Copyright (c) 2024")

        testStr = self.tstParser._createCopyrightMsg("James Kirk", "Copyright", "(c)", 2022, 2024)
        self.assertEqual(testStr, "James Kirk Copyright (c) 2022-2024")

        testStr = self.tstParser._createCopyrightMsg("Mr. Spock", "Copyright", "(c)", 2024, None)
        self.assertEqual(testStr, "Mr. Spock Copyright (c) 2024")

        testStr = self.tstParser._createCopyrightMsg("Mr. Spock", "Copyright", "(c)", 2023)
        self.assertEqual(testStr, "Mr. Spock Copyright (c) 2023")

    def test008BuildNewMsg(self):
        """!
        @brief Test the buildNewCopyrightMsg() method.
        """
        self.tstParser.parseCopyrightMsg(" * James Kirk Copyright (c) 2022               *")
        testStr = self.tstParser.buildNewCopyrightMsg(2024)
        self.assertEqual(testStr, "James Kirk Copyright (c) 2024")

        testStr = self.tstParser.buildNewCopyrightMsg(2023, None)
        self.assertEqual(testStr, "James Kirk Copyright (c) 2023")

        testStr = self.tstParser.buildNewCopyrightMsg(2023, 2024)
        self.assertEqual(testStr, "James Kirk Copyright (c) 2023-2024")

        testStr = self.tstParser.buildNewCopyrightMsg(2024, addStartEnd=True)
        self.assertEqual(testStr, " * James Kirk Copyright (c) 2024               *")

        testStr = self.tstParser.buildNewCopyrightMsg(2023, None, True)
        self.assertEqual(testStr, " * James Kirk Copyright (c) 2023               *")

        testStr = self.tstParser.buildNewCopyrightMsg(2023, 2024, True)
        self.assertEqual(testStr, " * James Kirk Copyright (c) 2023-2024          *")

    def test009BuildNewMsgNoParse(self):
        """!
        @brief Test the buildNewCopyrightMsg() method with no parsed data
        """
        testStr = self.tstParser.buildNewCopyrightMsg(2024)
        self.assertIsNone(testStr)

        testStr = self.tstParser.buildNewCopyrightMsg(2023, None)
        self.assertIsNone(testStr)

        testStr = self.tstParser.buildNewCopyrightMsg(2023, 2024)
        self.assertIsNone(testStr)

        testStr = self.tstParser.buildNewCopyrightMsg(2024, addStartEnd=True)
        self.assertIsNone(testStr)

        testStr = self.tstParser.buildNewCopyrightMsg(2023, None, True)
        self.assertIsNone(testStr)

        testStr = self.tstParser.buildNewCopyrightMsg(2023, 2024, True)
        self.assertIsNone(testStr)

if __name__ == '__main__':
    unittest.main()