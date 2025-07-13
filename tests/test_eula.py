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
from code_tools_grocsoftware.base.eula import eula as eula_data

class TestEula:
    """!
    @brief Unit test for the EULAText class
    """
    def test01_static_get_eula_text(self):
        """!
        @brief Test the static get EULA text method
        """
        eula = EulaText.get_eula_text('MIT_open')
        assert eula is not None
        assert len(eula) == 3

        eula = EulaText.get_eula_text('MIT_no_atrtrib')
        assert eula is not None
        assert len(eula) == 2

        eula = EulaText.get_eula_text('MIT_X11')
        assert eula is not None
        assert len(eula) == 4

        eula = EulaText.get_eula_text('GNU_V11')
        assert eula is not None
        assert len(eula) == 3

        eula = EulaText.get_eula_text('apache_v2_0')
        assert eula is not None
        assert len(eula) == 3

        eula = EulaText.get_eula_text('BSD_3clause')
        assert eula is not None
        assert len(eula) == 5

        eula = EulaText.get_eula_text('BSD_2clause')
        assert eula is not None
        assert len(eula) == 4

        eula = EulaText.get_eula_text('somethingelse')
        assert eula is None

    def test02_static_get_eula_name(self):
        """!
        @brief Test the static get EULA name method
        """
        eula_name = EulaText.get_eula_name('MIT_open')
        assert eula_name is not None
        assert eula_name == eula_data['MIT_open']['name']

        eula_name = EulaText.get_eula_name('MIT_no_atrtrib')
        assert eula_name is not None
        assert eula_name == eula_data['MIT_no_atrtrib']['name']

        eula_name = EulaText.get_eula_name('MIT_X11')
        assert eula_name is not None
        assert eula_name == eula_data['MIT_X11']['name']

        eula_name = EulaText.get_eula_name('GNU_V11')
        assert eula_name is not None
        assert eula_name == eula_data['GNU_V11']['name']

        eula_name = EulaText.get_eula_name('apache_v2_0')
        assert eula_name is not None
        assert eula_name == eula_data['apache_v2_0']['name']

        eula_name = EulaText.get_eula_name('BSD_3clause')
        assert eula_name is not None
        assert eula_name == eula_data['BSD_3clause']['name']

        eula_name = EulaText.get_eula_name('BSD_2clause')
        assert eula_name is not None
        assert eula_name == eula_data['BSD_2clause']['name']

        eula_name = EulaText.get_eula_name('somethingelse')
        assert eula_name is None

    def test11_constructor(self):
        """!
        @brief Test the EULA text constructor
        """
        eula = EulaText('MIT_open')
        assert eula.raw_eula_text is not None
        assert len(eula.raw_eula_text) == 3

        eula = EulaText('MIT_no_atrtrib')
        assert eula.raw_eula_text is not None
        assert len(eula.raw_eula_text) == 2

        eula = EulaText('MIT_X11')
        assert eula.raw_eula_text is not None
        assert len(eula.raw_eula_text) == 4

        eula = EulaText('GNU_V11')
        assert eula.raw_eula_text is not None
        assert len(eula.raw_eula_text) == 3

        eula = EulaText('apache_v2_0')
        assert eula.raw_eula_text is not None
        assert len(eula.raw_eula_text) == 3

        eula = EulaText('BSD_3clause')
        assert eula.raw_eula_text is not None
        assert len(eula.raw_eula_text) == 5

        eula = EulaText('BSD_2clause')
        assert eula.raw_eula_text is not None
        assert len(eula.raw_eula_text) == 4

        eula = EulaText(None, ["Custom EULA message","Test message"])
        assert eula.raw_eula_text is not None
        assert len(eula.raw_eula_text) == 2
        assert eula.raw_eula_text[0] == "Custom EULA message"

    def test12_constructor_error(self):
        """!
        @brief Test the EULA constructor error case
        """
        with pytest.raises(Exception) as context:
            eula = EulaText()
        assert "ERROR: Standard or custom EULA is required." in str(context.value)


    def test13_format_eula_text_default(self):
        """!
        @brief Test the EULA text format_eula_text method
        """
        eula = EulaText('MIT_open')
        formatedtext = eula.format_eula_text()
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

    def test14_format_eula_text_pad(self):
        """!
        @brief Test the EULA text format_eula_text method
        """
        eula = EulaText('MIT_open')
        formatedtext = eula.format_eula_text(pad=True)
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

    def test15_format_eula_text_length50(self):
        """!
        @brief Test the EULA text format_eula_text method
        """
        eula = EulaText('GNU_V11')
        formatedtext = eula.format_eula_text(50)
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

    def test16_format_eula_text_single_line(self):
        """!
        @brief Test the EULA text format_eula_text method with a single eula line
        """
        eula = EulaText(None, ['No real EULA text'])
        formatedtext = eula.format_eula_text(80)
        assert formatedtext is not None
        assert len(formatedtext) == 2
        assert formatedtext[0] == 'No real EULA text'

    def test17_format_eula_name(self):
        """!
        @brief Test the EULA format_eula_name method
        """
        eula = EulaText('GNU_V11')

        nametext = eula.format_eula_name()
        assert nametext == eula_data['GNU_V11']['name']

    def test18_format_eula_name_with_pad(self):
        """!
        @brief Test the EULA format_eula_name method
        """
        eula = EulaText('GNU_V11')
        nametext = eula.format_eula_name(80, True)
        assert nametext == eula_data['GNU_V11']['name'].ljust(80, ' ')

    def test19_format_eula_text_single_line_no_break(self):
        """!
        @brief Test the EULA text format_eula_text method with a single eula line
        """
        eula = EulaText(None, ['Longlinewithnobreakstoforceawkwardbreak'])
        formatedtext = eula.format_eula_text(22)
        assert formatedtext is not None
        assert len(formatedtext) == 3
        assert formatedtext[0] == 'Longlinewithnobreaksto'
        assert formatedtext[1] == 'forceawkwardbreak'
        assert formatedtext[2] == ''

#if __name__ == '__main__':
#    unittest.main()
