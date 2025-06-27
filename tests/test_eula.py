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

from code_tools.base.eula import EulaText
from code_tools.base.eula import eula as eulaData

class TestEula(unittest.TestCase):
    """!
    @brief Unit test for the EULAText class
    """
    def test01StaticGetEulaText(self):
        """!
        @brief Test the static get EULA text method
        """
        eula = EulaText.getEulaText('MIT_open')
        self.assertIsNotNone(eula)
        self.assertEqual(len(eula), 3)

        eula = EulaText.getEulaText('MIT_no_atrtrib')
        self.assertIsNotNone(eula)
        self.assertEqual(len(eula), 2)

        eula = EulaText.getEulaText('MIT_X11')
        self.assertIsNotNone(eula)
        self.assertEqual(len(eula), 4)

        eula = EulaText.getEulaText('GNU_V11')
        self.assertIsNotNone(eula)
        self.assertEqual(len(eula), 3)

        eula = EulaText.getEulaText('apache_v2_0')
        self.assertIsNotNone(eula)
        self.assertEqual(len(eula), 3)

        eula = EulaText.getEulaText('BSD_3clause')
        self.assertIsNotNone(eula)
        self.assertEqual(len(eula), 5)

        eula = EulaText.getEulaText('BSD_2clause')
        self.assertIsNotNone(eula)
        self.assertEqual(len(eula), 4)

        eula = EulaText.getEulaText('somethingelse')
        self.assertIsNone(eula)

    def test02StaticGetEulaName(self):
        """!
        @brief Test the static get EULA name method
        """
        eulaName = EulaText.getEulaName('MIT_open')
        self.assertIsNotNone(eulaName)
        self.assertEqual(eulaName, eulaData['MIT_open']['name'])

        eulaName = EulaText.getEulaName('MIT_no_atrtrib')
        self.assertIsNotNone(eulaName)
        self.assertEqual(eulaName, eulaData['MIT_no_atrtrib']['name'])

        eulaName = EulaText.getEulaName('MIT_X11')
        self.assertIsNotNone(eulaName)
        self.assertEqual(eulaName, eulaData['MIT_X11']['name'])

        eulaName = EulaText.getEulaName('GNU_V11')
        self.assertIsNotNone(eulaName)
        self.assertEqual(eulaName, eulaData['GNU_V11']['name'])

        eulaName = EulaText.getEulaName('apache_v2_0')
        self.assertIsNotNone(eulaName)
        self.assertEqual(eulaName, eulaData['apache_v2_0']['name'])

        eulaName = EulaText.getEulaName('BSD_3clause')
        self.assertIsNotNone(eulaName)
        self.assertEqual(eulaName, eulaData['BSD_3clause']['name'])

        eulaName = EulaText.getEulaName('BSD_2clause')
        self.assertIsNotNone(eulaName)
        self.assertEqual(eulaName, eulaData['BSD_2clause']['name'])

        eulaName = EulaText.getEulaName('somethingelse')
        self.assertIsNone(eulaName)

    def test11Constructor(self):
        """!
        @brief Test the EULA text constructor
        """
        eula = EulaText('MIT_open')
        self.assertIsNotNone(eula.rawEulaText)
        self.assertEqual(len(eula.rawEulaText), 3)

        eula = EulaText('MIT_no_atrtrib')
        self.assertIsNotNone(eula.rawEulaText)
        self.assertEqual(len(eula.rawEulaText), 2)

        eula = EulaText('MIT_X11')
        self.assertIsNotNone(eula.rawEulaText)
        self.assertEqual(len(eula.rawEulaText), 4)

        eula = EulaText('GNU_V11')
        self.assertIsNotNone(eula.rawEulaText)
        self.assertEqual(len(eula.rawEulaText), 3)

        eula = EulaText('apache_v2_0')
        self.assertIsNotNone(eula.rawEulaText)
        self.assertEqual(len(eula.rawEulaText), 3)

        eula = EulaText('BSD_3clause')
        self.assertIsNotNone(eula.rawEulaText)
        self.assertEqual(len(eula.rawEulaText), 5)

        eula = EulaText('BSD_2clause')
        self.assertIsNotNone(eula.rawEulaText)
        self.assertEqual(len(eula.rawEulaText), 4)

        eula = EulaText(None, ["Custom EULA message","Test message"])
        self.assertIsNotNone(eula.rawEulaText)
        self.assertEqual(len(eula.rawEulaText), 2)
        self.assertEqual(eula.rawEulaText[0], "Custom EULA message")

    def test12ConstructorError(self):
        """!
        @brief Test the EULA constructor error case
        """
        with self.assertRaises(Exception) as context:
            eula = EulaText()
        self.assertTrue("ERROR: Standard or custom EULA is required." in str(context.exception))


    def test13FormatEulaTextDefault(self):
        """!
        @brief Test the EULA text formatEulaText method
        """
        eula = EulaText('MIT_open')
        formatedtext = eula.formatEulaText()
        self.assertIsNotNone(formatedtext)
        self.assertEqual(len(formatedtext),18)
        for line in formatedtext:
            self.assertLessEqual(len(line),80)

        self.assertEqual(formatedtext[0], "Permission is hereby granted, free of charge, to any person obtaining a copy of")
        self.assertEqual(formatedtext[6], "")
        self.assertEqual(formatedtext[7], "The above copyright notice and self permission notice shall be included in all")
        self.assertEqual(formatedtext[9], "")
        self.assertEqual(formatedtext[10], "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR")
        self.assertEqual(formatedtext[16], "SOFTWARE.")
        self.assertEqual(formatedtext[17], "")

    def test14FormatEulaTextPad(self):
        """!
        @brief Test the EULA text formatEulaText method
        """
        eula = EulaText('MIT_open')
        formatedtext = eula.formatEulaText(pad=True)
        self.assertIsNotNone(formatedtext)
        self.assertEqual(len(formatedtext),18)
        for line in formatedtext:
            self.assertEqual(len(line),80)

        self.assertEqual(formatedtext[0], "Permission is hereby granted, free of charge, to any person obtaining a copy of ")
        self.assertEqual(formatedtext[6], "                                                                                ")
        self.assertEqual(formatedtext[7], "The above copyright notice and self permission notice shall be included in all  ")
        self.assertEqual(formatedtext[9], "                                                                                ")
        self.assertEqual(formatedtext[10], "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR      ")
        self.assertEqual(formatedtext[16], "SOFTWARE.                                                                       ")
        self.assertEqual(formatedtext[17], "                                                                                ")

    def test15FormatEulaTextLength50(self):
        """!
        @brief Test the EULA text formatEulaText method
        """
        eula = EulaText('GNU_V11')
        formatedtext = eula.formatEulaText(50)
        self.assertIsNotNone(formatedtext)
        self.assertEqual(len(formatedtext), 17)
        for line in formatedtext:
            self.assertLessEqual(len(line),50)

        self.assertEqual(formatedtext[0], "This program is free software: you can")
        self.assertEqual(formatedtext[5], "version.")
        self.assertEqual(formatedtext[6], "")
        self.assertEqual(formatedtext[7], "This program is distributed in the hope that it")
        self.assertEqual(formatedtext[11], "General Public License for more details.")
        self.assertEqual(formatedtext[12], "")
        self.assertEqual(formatedtext[13], "You should have received a copy of the GNU")
        self.assertEqual(formatedtext[15], "If not, see <https://www.gnu.org/licenses/>.")
        self.assertEqual(formatedtext[16], "")

    def test16FormatEulaTextSingleLine(self):
        """!
        @brief Test the EULA text formatEulaText method with a single eula line
        """
        eula = EulaText(None, ['No real EULA text'])
        formatedtext = eula.formatEulaText(80)
        self.assertIsNotNone(formatedtext)
        self.assertEqual(len(formatedtext), 2)
        self.assertEqual(formatedtext[0], 'No real EULA text')

    def test17FormatEulaName(self):
        """!
        @brief Test the EULA formatEulaName method
        """
        eula = EulaText('GNU_V11')

        nametext = eula.formatEulaName()
        self.assertEqual(nametext, eulaData['GNU_V11']['name'])

    def test18FormatEulaNameWithPad(self):
        """!
        @brief Test the EULA formatEulaName method
        """
        eula = EulaText('GNU_V11')
        nametext = eula.formatEulaName(80, True)
        self.assertEqual(nametext, eulaData['GNU_V11']['name'].ljust(80, ' '))

    def test19FormatEulaTextSingleLineNoBreak(self):
        """!
        @brief Test the EULA text formatEulaText method with a single eula line
        """
        eula = EulaText(None, ['Longlinewithnobreakstoforceawkwardbreak'])
        formatedtext = eula.formatEulaText(22)
        self.assertIsNotNone(formatedtext)
        self.assertEqual(len(formatedtext), 3)
        self.assertEqual(formatedtext[0], 'Longlinewithnobreaksto')
        self.assertEqual(formatedtext[1], 'forceawkwardbreak')
        self.assertEqual(formatedtext[2], '')

if __name__ == '__main__':
    unittest.main()