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

import re
import unittest

from dir_init import pathincsetup
pathincsetup()

from code_tools_grocsoftware.base.copyright_tools import SubTextMarker
from code_tools_grocsoftware.base.copyright_tools import CopyrightYearsList
from code_tools_grocsoftware.base.copyright_tools import CopyrightParse

class TestClass01CopyrightParserBase(unittest.TestCase):
    """!
    @brief Unit test for the copyright parser class
    """
    def setUp(self):
        self.tstParser = CopyrightParse(copyrightSearchMsg = r'Copyright|COPYRIGHT|copyright',
                                        copyrightSearchTag = r'\([cC]\)',
                                        copyrightSearchDate = r'(\d{4})',
                                        copyrightOwnerSpec = r'[a-zA-Z0-9,\./\- @]',
                                        useUnicode = False)

    def test001CopyrightCheckDefault(self):
        """!
        @brief Test the default CopyrightParse constructor
        """
        # Test default values
        self.assertEqual(self.tstParser.copyrightTextStart, "")
        self.assertIsNone(self.tstParser.copyrightTextMsg)
        self.assertIsNone(self.tstParser.copyrightTextTag)
        self.assertIsNone(self.tstParser.copyrightTextOwner)
        self.assertIsNone(self.tstParser.copyrightTextEol)
        self.assertFalse(self.tstParser.copyrightTextValid)
        self.assertEqual(len(self.tstParser.copyrightYearList), 0)

    def test002CopyrightCheckAccessors(self):
        """!
        @brief Test the CopyrightParse accessor functions
        """
        # Test accessor functions
        self.assertEqual(self.tstParser.isCopyrightTextValid(), self.tstParser.copyrightTextValid)
        self.assertEqual(self.tstParser.getCopyrightText(), self.tstParser.copyrightText)
        yearList = self.tstParser.getCopyrightDates()
        self.assertEqual(len(yearList), len(self.tstParser.copyrightYearList))

    def test003CopyrightAddOwnerNoParse(self):
        """!
        @brief Test the addOwner with noe parsed data
        """
        # False because no message parsed to add owner to
        self.assertFalse(self.tstParser.addOwner("New Owner"))

    def test004CopyrightReplaceOwnerNoParse(self):
        """!
        @brief Test the replace owner method
        """
        self.tstParser.replaceOwner("new owner")
        self.assertEqual(self.tstParser.copyrightTextOwner, "new owner")

        self.tstParser.replaceOwner("second city")
        self.assertEqual(self.tstParser.copyrightTextOwner, "second city")

        self.tstParser.replaceOwner("prince")
        self.assertEqual(self.tstParser.copyrightTextOwner, "prince")

    def test005CopyrightParseEOLNoTail(self):
        """!
        @brief Test the parse eol method, no EOL text
        """
        eolTextMarker = self.tstParser._parseEolString("", 20)
        self.assertIsNone(eolTextMarker)

        eolTextMarker = self.tstParser._parseEolString(" ", 20)
        self.assertIsNone(eolTextMarker)

    def test006CopyrightParseEOLWithTail(self):
        """!
        @brief Test the parse eol method, with EOL text
        """
        eolTextMarker = self.tstParser._parseEolString("*", 20)
        self.assertIsNotNone(eolTextMarker)
        self.assertEqual(eolTextMarker.text, "*")
        self.assertEqual(eolTextMarker.start, 20)
        self.assertEqual(eolTextMarker.end, 21)

        eolTextMarker = self.tstParser._parseEolString(" *", 20)
        self.assertIsNotNone(eolTextMarker)
        self.assertEqual(eolTextMarker.text, "*")
        self.assertEqual(eolTextMarker.start, 21)
        self.assertEqual(eolTextMarker.end, 22)

        eolTextMarker = self.tstParser._parseEolString(" * ", 30)
        self.assertIsNotNone(eolTextMarker)
        self.assertEqual(eolTextMarker.text, "*")
        self.assertEqual(eolTextMarker.start, 31)
        self.assertEqual(eolTextMarker.end, 32)

        eolTextMarker = self.tstParser._parseEolString(" ** ", 30)
        self.assertIsNotNone(eolTextMarker)
        self.assertEqual(eolTextMarker.text, "**")
        self.assertEqual(eolTextMarker.start, 31)
        self.assertEqual(eolTextMarker.end, 33)

        eolTextMarker = self.tstParser._parseEolString("   ** ", 30)
        self.assertIsNotNone(eolTextMarker)
        self.assertEqual(eolTextMarker.text, "**")
        self.assertEqual(eolTextMarker.start, 33)
        self.assertEqual(eolTextMarker.end, 35)

    def test007CopyrightParseOwnerEmptyString(self):
        """!
        @brief Test the parse eol method, no EOL text
        """
        textMarker = self.tstParser._parseOwnerString("", 20)
        self.assertIsNone(textMarker)

        textMarker = self.tstParser._parseOwnerString(" ", 20)
        self.assertIsNone(textMarker)

        textMarker = self.tstParser._parseOwnerString("\t", 20)
        self.assertIsNone(textMarker)

        textMarker = self.tstParser._parseOwnerString("::", 20)
        self.assertIsNone(textMarker)

        textMarker = self.tstParser._parseOwnerString(";;", 20)
        self.assertIsNone(textMarker)

    def test008CopyrightParseOwnerString(self):
        """!
        @brief Test the parse owner method
        """
        ownerList = ["Wolverine", "Professor X", "professor.x@xavier.edu", "3M Corp."]
        for owner in ownerList:
            textMarker = self.tstParser._parseOwnerString(owner, 15)
            self.assertIsNotNone(textMarker)
            self.assertEqual(textMarker.text, owner)
            self.assertEqual(textMarker.start, 15)
            self.assertEqual(textMarker.end, 15+len(owner))

            textMarker = self.tstParser._parseOwnerString(" "+owner, 15)
            self.assertIsNotNone(textMarker)
            self.assertEqual(textMarker.text, owner)
            self.assertEqual(textMarker.start, 16)
            self.assertEqual(textMarker.end, 16+len(owner))

            textMarker = self.tstParser._parseOwnerString(" "+owner+" ", 15)
            self.assertIsNotNone(textMarker)
            self.assertEqual(textMarker.text, owner)
            self.assertEqual(textMarker.start, 16)
            self.assertEqual(textMarker.end, 16+len(owner))

            textMarker = self.tstParser._parseOwnerString(" "+owner+"        *", 15)
            self.assertIsNotNone(textMarker)
            self.assertEqual(textMarker.text, owner)
            self.assertEqual(textMarker.start, 16)
            self.assertEqual(textMarker.end, 16+len(owner))

    def test009CopyrightParseYears(self):
        """!
        @brief Test the parse years
        """
        yearParser = self.tstParser._parseYears(" 2024 ")
        self.assertTrue(yearParser.isValid())

        yearList = yearParser.getNumericYearList()
        self.assertEqual(len(yearList), 1)

        self.assertEqual(yearParser.getFirstEntry(), 2024)
        self.assertEqual(yearParser.getLastEntry(), 2024)
        self.assertEqual(yearParser.getStartingStringIndex(), 1)
        self.assertEqual(yearParser.getEndingStringIndex(), 5)

        yearParser = self.tstParser._parseYears(" 2024-2025 ")
        self.assertTrue(yearParser.isValid())

        yearList = yearParser.getNumericYearList()
        self.assertEqual(len(yearList), 2)

        self.assertEqual(yearParser.getFirstEntry(), 2024)
        self.assertEqual(yearParser.getLastEntry(), 2025)
        self.assertEqual(yearParser.getStartingStringIndex(), 1)
        self.assertEqual(yearParser.getEndingStringIndex(), 10)

    def test010CopyrightParseComponents(self):
        """!
        @brief Test the parse copyright parse components, standard order, with fluff, no failure
        """
        copyrightMsgList = ["Copyright", "COPYRIGHT", "copyright"]
        copyrightTagList = ["(c)", "(C)"]
        startFluffList = ["", " ", "Owners name ", "Random text "]
        endFluffList = ["", " ", " Owners name", " Random text    *"]
        for crtag in copyrightTagList:
            for crmsg in copyrightMsgList:
                for startFluff in startFluffList:
                    for endFluff in  endFluffList:
                        testStr = startFluff+crmsg+" "+crtag+" 2024"+endFluff
                        msgMarker, tagMarker, yearList = self.tstParser._parseCopyrightComponents(testStr)
                        self.assertIsNotNone(msgMarker)
                        self.assertEqual(msgMarker.group(), crmsg)
                        self.assertIsNotNone(tagMarker)
                        self.assertEqual(tagMarker.group(), crtag)
                        self.assertIsNotNone(yearList)
                        self.assertTrue(yearList.isValid())

    def test011CopyrightParseComponentsFail(self):
        """!
        @brief Test the parse copyright parse components, standard order, failure
        """
        # Message fail
        msgMarker, tagMarker, yearList = self.tstParser._parseCopyrightComponents("Random (c) 2024 owner")
        self.assertIsNone(msgMarker)
        self.assertIsNotNone(tagMarker)
        self.assertEqual(tagMarker.group(), "(c)")
        self.assertIsNotNone(yearList)
        self.assertTrue(yearList.isValid())

        # Tag fail
        msgMarker, tagMarker, yearList = self.tstParser._parseCopyrightComponents("copyright (r) 2024 owner")
        self.assertIsNotNone(msgMarker)
        self.assertEqual(msgMarker.group(), "copyright")
        self.assertIsNone(tagMarker)
        self.assertIsNotNone(yearList)
        self.assertTrue(yearList.isValid())

        # Year fail
        msgMarker, tagMarker, yearList = self.tstParser._parseCopyrightComponents("copyright (c) notyear owner")
        self.assertIsNotNone(msgMarker)
        self.assertEqual(msgMarker.group(), "copyright")
        self.assertIsNotNone(tagMarker)
        self.assertEqual(tagMarker.group(), "(c)")
        self.assertIsNotNone(yearList)
        self.assertFalse(yearList.isValid())

    def test012CopyrightParseComponentsDifferentOrders(self):
        """!
        @brief Test the parse copyright parse components, different orders
        """
        # Year first
        msgMarker, tagMarker, yearList = self.tstParser._parseCopyrightComponents("2024 Copyright (c) owner")
        self.assertIsNotNone(msgMarker)
        self.assertEqual(msgMarker.group(), "Copyright")
        self.assertIsNotNone(tagMarker)
        self.assertEqual(tagMarker.group(), "(c)")
        self.assertIsNotNone(yearList)
        self.assertTrue(yearList.isValid())

        # owner, year first
        msgMarker, tagMarker, yearList = self.tstParser._parseCopyrightComponents("2024 owner Copyright (c)")
        self.assertIsNotNone(msgMarker)
        self.assertEqual(msgMarker.group(), "Copyright")
        self.assertIsNotNone(tagMarker)
        self.assertEqual(tagMarker.group(), "(c)")
        self.assertIsNotNone(yearList)
        self.assertTrue(yearList.isValid())

        # msg tag weird
        msgMarker, tagMarker, yearList = self.tstParser._parseCopyrightComponents("2024 owner (c) Copyright")
        self.assertIsNotNone(msgMarker)
        self.assertEqual(msgMarker.group(), "Copyright")
        self.assertIsNotNone(tagMarker)
        self.assertEqual(tagMarker.group(), "(c)")
        self.assertIsNotNone(yearList)
        self.assertTrue(yearList.isValid())

        # owner year
        msgMarker, tagMarker, yearList = self.tstParser._parseCopyrightComponents("owner 2024-2025 (c) Copyright")
        self.assertIsNotNone(msgMarker)
        self.assertEqual(msgMarker.group(), "Copyright")
        self.assertIsNotNone(tagMarker)
        self.assertEqual(tagMarker.group(), "(c)")
        self.assertIsNotNone(yearList)
        self.assertTrue(yearList.isValid())

    def test013CopyrightCheckComponents(self):
        """!
        @brief Test the parse copyright check components
        """
        msgMarker = re.Match
        tagMarker = re.Match
        yearList = CopyrightYearsList('2022', r'(\d{4})', 25)
        ownerData = SubTextMarker("Owner", 34)

        # Test None inputs
        self.assertFalse(self.tstParser._checkComponents(None, tagMarker, yearList, ownerData))
        self.assertFalse(self.tstParser._checkComponents(msgMarker, None, yearList, ownerData))
        self.assertFalse(self.tstParser._checkComponents(msgMarker, tagMarker, yearList, None))

        # Test Invalid date inputs
        yearListBad = CopyrightYearsList('', r'(\d{4})', 25)
        self.assertFalse(yearListBad.isValid())
        self.assertFalse(self.tstParser._checkComponents(msgMarker, tagMarker, yearListBad, ownerData))

        # Test passing case
        self.assertTrue(self.tstParser._checkComponents(msgMarker, tagMarker, yearList, ownerData))

    def test014CopyrightBuild(self):
        """!
        @brief Test the parse copyright build year string method
        """
        yearStr = self.tstParser._buildCopyrightYearString(2025,None)
        self.assertEqual(yearStr, "2025")
        yearStr = self.tstParser._buildCopyrightYearString(2022,2022)
        self.assertEqual(yearStr, "2022")
        yearStr = self.tstParser._buildCopyrightYearString(2022,2024)
        self.assertEqual(yearStr, "2022-2024")

class TestClass02CopyrightParserBase(unittest.TestCase):
    def setUp(self):
        self.tstParser = CopyrightParse(copyrightSearchMsg = r'Copyright|COPYRIGHT|copyright',
                                        copyrightSearchTag = r'\([cC]\)',
                                        copyrightSearchDate = r'(\d{4})',
                                        copyrightOwnerSpec = r'[a-zA-Z0-9,\./\- @]',
                                        useUnicode = False)

        self.tstMessage = " * Copyright (c) 2024-2025 Jean Grey             *"
        self.tstSolText = " * "
        self.tstEolMarker = SubTextMarker("*", len(self.tstMessage)-1)
        self.tstMsgMarker, self.tstTagMarker, self.tstYearList = self.tstParser._parseCopyrightComponents(self.tstMessage)
        self.tstOwnerData = SubTextMarker("Jean Grey", 27)

    def test001CopyrightSetParsedDataMsgNone(self):
        """!
        @brief Test the parse copyright set parsed data, msg=None
        """
        # Test msg none
        self.tstParser._setParsedCopyrightData("currentMsg", None, self.tstTagMarker, self.tstYearList,
                                               self.tstOwnerData, self.tstSolText, self.tstEolMarker)
        self.assertFalse(self.tstParser.copyrightTextValid)
        self.assertEqual(self.tstParser.copyrightText, "")
        self.assertEqual(self.tstParser.copyrightTextStart, "")

        self.assertIsNone(self.tstParser.copyrightTextMsg)
        self.assertEqual(self.tstParser.copyrightTextTag, self.tstTagMarker.group())
        self.assertEqual(self.tstParser.copyrightTextOwner, self.tstOwnerData.text)
        self.assertEqual(self.tstParser.copyrightTextEol, self.tstEolMarker.text)
        self.assertEqual(len(self.tstParser.copyrightYearList), 2)

    def test002CopyrightSetParsedDataTagNone(self):
        """!
        @brief Test the parse copyright set parsed data, tag=None
        """
        # Test tag none
        self.tstParser._setParsedCopyrightData("currentMsg", self.tstMsgMarker, None, self.tstYearList,
                                               self.tstOwnerData, self.tstSolText, self.tstEolMarker)
        self.assertFalse(self.tstParser.copyrightTextValid)
        self.assertEqual(self.tstParser.copyrightText, "")

        self.assertEqual(self.tstParser.copyrightTextStart, self.tstSolText)
        self.assertEqual(self.tstParser.copyrightTextMsg, self.tstMsgMarker.group())
        self.assertIsNone(self.tstParser.copyrightTextTag)
        self.assertEqual(self.tstParser.copyrightTextOwner, self.tstOwnerData.text)
        self.assertEqual(self.tstParser.copyrightTextEol, self.tstEolMarker.text)
        self.assertEqual(len(self.tstParser.copyrightYearList), 2)

    def test003CopyrightSetParsedDataYearInvalid(self):
        """!
        @brief Test the parse copyright set parsed data, invalid year data
        """
        # Test year invalid
        invalidYearList = CopyrightYearsList("", r'(\d{4})', 10)
        self.tstParser._setParsedCopyrightData("currentMsg", self.tstMsgMarker, self.tstTagMarker, invalidYearList,
                                               self.tstOwnerData, self.tstSolText, self.tstEolMarker)
        self.assertFalse(self.tstParser.copyrightTextValid)
        self.assertEqual(self.tstParser.copyrightText, "")

        self.assertEqual(self.tstParser.copyrightTextStart, self.tstSolText)
        self.assertEqual(self.tstParser.copyrightTextMsg, self.tstMsgMarker.group())
        self.assertEqual(self.tstParser.copyrightTextTag, self.tstTagMarker.group())
        self.assertEqual(self.tstParser.copyrightTextOwner, self.tstOwnerData.text)
        self.assertEqual(self.tstParser.copyrightTextEol, self.tstEolMarker.text)
        self.assertEqual(len(self.tstParser.copyrightYearList), 0)

    def test004CopyrightSetParsedDataEOLNone(self):
        """!
        @brief Test the parse copyright set parsed data, eol text = None
        """
        # Test year invalid
        self.tstParser._setParsedCopyrightData("currentMsg", self.tstMsgMarker, self.tstTagMarker, self.tstYearList,
                                               self.tstOwnerData, self.tstSolText, None)

        self.assertTrue(self.tstParser.copyrightTextValid)
        self.assertEqual(self.tstParser.copyrightText, "currentMsg")

        self.assertEqual(self.tstParser.copyrightTextStart, self.tstSolText)
        self.assertEqual(self.tstParser.copyrightTextMsg, self.tstMsgMarker.group())
        self.assertEqual(self.tstParser.copyrightTextTag, self.tstTagMarker.group())
        self.assertEqual(self.tstParser.copyrightTextOwner, self.tstOwnerData.text)
        self.assertIsNone(self.tstParser.copyrightTextEol)
        self.assertEqual(len(self.tstParser.copyrightYearList), 2)

    def test005CopyrightSetParsedDataEOLNone(self):
        """!
        @brief Test the parse copyright set parsed data, eol text = None
        """
        # Test year invalid
        self.tstParser._setParsedCopyrightData("currentMsg", self.tstMsgMarker, self.tstTagMarker, self.tstYearList,
                                               self.tstOwnerData, self.tstSolText, self.tstEolMarker)

        self.assertTrue(self.tstParser.copyrightTextValid)
        self.assertEqual(self.tstParser.copyrightText, "currentMsg")

        self.assertEqual(self.tstParser.copyrightTextStart, self.tstSolText)
        self.assertEqual(self.tstParser.copyrightTextMsg, self.tstMsgMarker.group())
        self.assertEqual(self.tstParser.copyrightTextTag, self.tstTagMarker.group())
        self.assertEqual(self.tstParser.copyrightTextOwner, self.tstOwnerData.text)
        self.assertEqual(self.tstParser.copyrightTextEol, self.tstEolMarker.text)
        self.assertEqual(len(self.tstParser.copyrightYearList), 2)

    def test006CopyrightAddEOLNone(self):
        """!
        @brief Test the parse copyright add eol marker with eol marker = None
        """
        # Set the EOL marker
        self.tstParser.copyrightTextEol = None

        newCopyRightMsg = self.tstParser._addEolText("Current text")
        self.assertEqual(newCopyRightMsg, "Current text")

    def test007CopyrightAddEOL(self):
        """!
        @brief Test the parse copyright add eol marker with eol marker = *
        """
        # Set the EOL marker
        self.tstParser.copyrightText = "* Copyright (c) 2024 X-Men        *"
        self.tstParser.copyrightTextEol = '*'

        newCopyRightMsg = self.tstParser._addEolText("* Copyright (c) 2024-2025 X-Men")
        self.assertEqual(newCopyRightMsg, "* Copyright (c) 2024-2025 X-Men   *")

    def test008CopyrightAddEOLShort(self):
        """!
        @brief Test the parse copyright add eol marker with eol marker = *
        """
        # Set the EOL marker
        self.tstParser.copyrightText = "* Copyright (c) 2024 X-Men *"
        self.tstParser.copyrightTextEol = '*'

        newCopyRightMsg = self.tstParser._addEolText("* Copyright (c) 2024-2025 X-Men")
        self.assertEqual(newCopyRightMsg, "* Copyright (c) 2024-2025 X-Men*")

class TestClass03CopyrightParserBaseUniCode(unittest.TestCase):
    """!
    @brief Unit test for the copyright parser class
    """
    def setUp(self):
        self.tstParser = CopyrightParse(copyrightSearchMsg = r'Copyright|COPYRIGHT|copyright',
                                        copyrightSearchTag = r'\([cC]\)',
                                        copyrightSearchDate = r'(\d{4})',
                                        copyrightOwnerSpec = r'[a-zA-Z0-9,\./\- @]',
                                        useUnicode = True)

    def test001CopyrightCheckDefault(self):
        """!
        @brief Test the default CopyrightParse constructor
        """
        # Test default values
        self.assertEqual(self.tstParser.copyrightTextStart, "")
        self.assertIsNone(self.tstParser.copyrightTextMsg)
        self.assertIsNone(self.tstParser.copyrightTextTag)
        self.assertIsNone(self.tstParser.copyrightTextOwner)
        self.assertIsNone(self.tstParser.copyrightTextEol)
        self.assertFalse(self.tstParser.copyrightTextValid)
        self.assertEqual(len(self.tstParser.copyrightYearList), 0)

if __name__ == '__main__':
    unittest.main()