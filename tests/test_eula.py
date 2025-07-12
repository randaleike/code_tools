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

import pytest
from code_tools_grocsoftware.base.eula import EulaText
from code_tools_grocsoftware.base.eula import eula as eulaData

class TestEula:
    """!
    @brief Unit test for the EULAText class
    """
    def test01StaticGetEulaText(self):
        """!
        @brief Test the static get EULA text method
        """
        eula = EulaText.getEulaText('MIT_open')
        assert eula is not None
        assert len(eula) == 3

        eula = EulaText.getEulaText('MIT_no_atrtrib')
        assert eula is not None
        assert len(eula) == 2

        eula = EulaText.getEulaText('MIT_X11')
        assert eula is not None
        assert len(eula) == 4

        eula = EulaText.getEulaText('GNU_V11')
        assert eula is not None
        assert len(eula) == 3

        eula = EulaText.getEulaText('apache_v2_0')
        assert eula is not None
        assert len(eula) == 3

        eula = EulaText.getEulaText('BSD_3clause')
        assert eula is not None
        assert len(eula) == 5

        eula = EulaText.getEulaText('BSD_2clause')
        assert eula is not None
        assert len(eula) == 4

        eula = EulaText.getEulaText('somethingelse')
        assert eula is None

    def test02StaticGetEulaName(self):
        """!
        @brief Test the static get EULA name method
        """
        eulaName = EulaText.getEulaName('MIT_open')
        assert eulaName is not None
        assert eulaName == eulaData['MIT_open']['name']

        eulaName = EulaText.getEulaName('MIT_no_atrtrib')
        assert eulaName is not None
        assert eulaName == eulaData['MIT_no_atrtrib']['name']

        eulaName = EulaText.getEulaName('MIT_X11')
        assert eulaName is not None
        assert eulaName == eulaData['MIT_X11']['name']

        eulaName = EulaText.getEulaName('GNU_V11')
        assert eulaName is not None
        assert eulaName == eulaData['GNU_V11']['name']

        eulaName = EulaText.getEulaName('apache_v2_0')
        assert eulaName is not None
        assert eulaName == eulaData['apache_v2_0']['name']

        eulaName = EulaText.getEulaName('BSD_3clause')
        assert eulaName is not None
        assert eulaName == eulaData['BSD_3clause']['name']

        eulaName = EulaText.getEulaName('BSD_2clause')
        assert eulaName is not None
        assert eulaName == eulaData['BSD_2clause']['name']

        eulaName = EulaText.getEulaName('somethingelse')
        assert eulaName is None

    def test11Constructor(self):
        """!
        @brief Test the EULA text constructor
        """
        eula = EulaText('MIT_open')
        assert eula.rawEulaText is not None
        assert len(eula.rawEulaText) == 3

        eula = EulaText('MIT_no_atrtrib')
        assert eula.rawEulaText is not None
        assert len(eula.rawEulaText) == 2

        eula = EulaText('MIT_X11')
        assert eula.rawEulaText is not None
        assert len(eula.rawEulaText) == 4

        eula = EulaText('GNU_V11')
        assert eula.rawEulaText is not None
        assert len(eula.rawEulaText) == 3

        eula = EulaText('apache_v2_0')
        assert eula.rawEulaText is not None
        assert len(eula.rawEulaText) == 3

        eula = EulaText('BSD_3clause')
        assert eula.rawEulaText is not None
        assert len(eula.rawEulaText) == 5

        eula = EulaText('BSD_2clause')
        assert eula.rawEulaText is not None
        assert len(eula.rawEulaText) == 4

        eula = EulaText(None, ["Custom EULA message","Test message"])
        assert eula.rawEulaText is not None
        assert len(eula.rawEulaText) == 2
        assert eula.rawEulaText[0] == "Custom EULA message"

    def test12ConstructorError(self):
        """!
        @brief Test the EULA constructor error case
        """
        with pytest.raises(Exception) as context:
            eula = EulaText()
        assert "ERROR: Standard or custom EULA is required." in str(context.value)


    def test13FormatEulaTextDefault(self):
        """!
        @brief Test the EULA text formatEulaText method
        """
        eula = EulaText('MIT_open')
        formatedtext = eula.formatEulaText()
        assert formatedtext is not None
        assert len(formatedtext) ==18
        for line in formatedtext:
            assert len(line) <=80

        assert formatedtext[0] == "Permission is hereby granted, free of charge, to any person obtaining a copy of"
        assert formatedtext[6] == ""
        assert formatedtext[7] == "The above copyright notice and self permission notice shall be included in all"
        assert formatedtext[9] == ""
        assert formatedtext[10] == "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR"
        assert formatedtext[16] == "SOFTWARE."
        assert formatedtext[17] == ""

    def test14FormatEulaTextPad(self):
        """!
        @brief Test the EULA text formatEulaText method
        """
        eula = EulaText('MIT_open')
        formatedtext = eula.formatEulaText(pad=True)
        assert formatedtext is not None
        assert len(formatedtext) ==18
        for line in formatedtext:
            assert len(line) ==80

        assert formatedtext[0] == "Permission is hereby granted, free of charge, to any person obtaining a copy of "
        assert formatedtext[6] == "                                                                                "
        assert formatedtext[7] == "The above copyright notice and self permission notice shall be included in all  "
        assert formatedtext[9] == "                                                                                "
        assert formatedtext[10] == "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR      "
        assert formatedtext[16] == "SOFTWARE.                                                                       "
        assert formatedtext[17] == "                                                                                "

    def test15FormatEulaTextLength50(self):
        """!
        @brief Test the EULA text formatEulaText method
        """
        eula = EulaText('GNU_V11')
        formatedtext = eula.formatEulaText(50)
        assert formatedtext is not None
        assert len(formatedtext) == 17
        for line in formatedtext:
            assert len(line) <=50

        assert formatedtext[0] == "This program is free software: you can"
        assert formatedtext[5] == "version."
        assert formatedtext[6] == ""
        assert formatedtext[7] == "This program is distributed in the hope that it"
        assert formatedtext[11] == "General Public License for more details."
        assert formatedtext[12] == ""
        assert formatedtext[13] == "You should have received a copy of the GNU"
        assert formatedtext[15] == "If not, see <https://www.gnu.org/licenses/>."
        assert formatedtext[16] == ""

    def test16FormatEulaTextSingleLine(self):
        """!
        @brief Test the EULA text formatEulaText method with a single eula line
        """
        eula = EulaText(None, ['No real EULA text'])
        formatedtext = eula.formatEulaText(80)
        assert formatedtext is not None
        assert len(formatedtext) == 2
        assert formatedtext[0] == 'No real EULA text'

    def test17FormatEulaName(self):
        """!
        @brief Test the EULA formatEulaName method
        """
        eula = EulaText('GNU_V11')

        nametext = eula.formatEulaName()
        assert nametext == eulaData['GNU_V11']['name']

    def test18FormatEulaNameWithPad(self):
        """!
        @brief Test the EULA formatEulaName method
        """
        eula = EulaText('GNU_V11')
        nametext = eula.formatEulaName(80, True)
        assert nametext == eulaData['GNU_V11']['name'].ljust(80, ' ')

    def test19FormatEulaTextSingleLineNoBreak(self):
        """!
        @brief Test the EULA text formatEulaText method with a single eula line
        """
        eula = EulaText(None, ['Longlinewithnobreakstoforceawkwardbreak'])
        formatedtext = eula.formatEulaText(22)
        assert formatedtext is not None
        assert len(formatedtext) == 3
        assert formatedtext[0] == 'Longlinewithnobreaksto'
        assert formatedtext[1] == 'forceawkwardbreak'
        assert formatedtext[2] == ''

#if __name__ == '__main__':
#    unittest.main()
