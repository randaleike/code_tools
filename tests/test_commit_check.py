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

from unittest.mock import patch

from code_tools_grocsoftware.base.commit_check import get_commit_over_write_flag
from code_tools_grocsoftware.base.commit_check import get_commit_new_flag
from code_tools_grocsoftware.base.commit_check import get_commit_flag
from code_tools_grocsoftware.base.commit_check import new_entry_correct

def test01_get_commit_overwrite_flag_no():
    """!
    @brief Test get_commit_over_write_flag method, no answer
    """
    with patch('builtins.input', side_effect='n') as in_mock:
        assert not get_commit_over_write_flag("test_entry")
        in_mock.assert_called_once_with("Overwrite existing test_entry entry? [Y/N]")

    with patch('builtins.input', side_effect='N') as in_mock:
        assert not get_commit_over_write_flag("test_entry")
        in_mock.assert_called_once_with("Overwrite existing test_entry entry? [Y/N]")

    with patch('builtins.input', side_effect='No') as in_mock:
        assert not get_commit_over_write_flag("test_entry")
        in_mock.assert_called_once_with("Overwrite existing test_entry entry? [Y/N]")

def test02_get_commit_overwrite_flag_yes():
    """!
    @brief Test get_commit_over_write_flag method, Yes answer
    """
    with patch('builtins.input', side_effect='y') as in_mock:
        assert get_commit_over_write_flag("test_entry")
        in_mock.assert_called_once_with("Overwrite existing test_entry entry? [Y/N]")

    with patch('builtins.input', side_effect='Y') as in_mock:
        assert get_commit_over_write_flag("test_entry")
        in_mock.assert_called_once_with("Overwrite existing test_entry entry? [Y/N]")

    with patch('builtins.input', side_effect='yes') as in_mock:
        assert get_commit_over_write_flag("test_entry")
        in_mock.assert_called_once_with("Overwrite existing test_entry entry? [Y/N]")

    with patch('builtins.input', side_effect='YES') as in_mock:
        assert get_commit_over_write_flag("test_entry")
        in_mock.assert_called_once_with("Overwrite existing test_entry entry? [Y/N]")

    with patch('builtins.input', side_effect='Yes') as in_mock:
        assert get_commit_over_write_flag("test_entry")
        in_mock.assert_called_once_with("Overwrite existing test_entry entry? [Y/N]")

def test03_get_commit_overwrite_flag_override(capsys):
    """!
    @brief Test get_commit_over_write_flag method, override=True
    """
    assert get_commit_over_write_flag("test_entry", True)
    assert capsys.readouterr().out == ""

def test04_get_commit_new_flag_no():
    """!
    @brief Test get_commit_new_flag method, no answer
    """
    with patch('builtins.input', side_effect='n') as in_mock:
        assert not get_commit_new_flag("test_entry")
        in_mock.assert_called_once_with("Add new test_entry entry? [Y/N]")

    with patch('builtins.input', side_effect='N') as in_mock:
        assert not get_commit_new_flag("test_entry")
        in_mock.assert_called_once_with("Add new test_entry entry? [Y/N]")

    with patch('builtins.input', side_effect='no') as in_mock:
        assert not get_commit_new_flag("test_entry")
        in_mock.assert_called_once_with("Add new test_entry entry? [Y/N]")

    with patch('builtins.input', side_effect='NO') as in_mock:
        assert not get_commit_new_flag("test_entry")
        in_mock.assert_called_once_with("Add new test_entry entry? [Y/N]")

    with patch('builtins.input', side_effect='No') as in_mock:
        assert not get_commit_new_flag("test_entry")
        in_mock.assert_called_once_with("Add new test_entry entry? [Y/N]")

def test05_get_commit_new_flag_yes():
    """!
    @brief Test get_commit_new_flag method, Yes answer
    """
    with patch('builtins.input', side_effect='y') as in_mock:
        assert get_commit_new_flag("test_entry")
        in_mock.assert_called_once_with("Add new test_entry entry? [Y/N]")

    with patch('builtins.input', side_effect='Y') as in_mock:
        assert get_commit_new_flag("test_entry")
        in_mock.assert_called_once_with("Add new test_entry entry? [Y/N]")

    with patch('builtins.input', side_effect='yes') as in_mock:
        assert get_commit_new_flag("test_entry")
        in_mock.assert_called_once_with("Add new test_entry entry? [Y/N]")

    with patch('builtins.input', side_effect='YES') as in_mock:
        assert get_commit_new_flag("test_entry")
        in_mock.assert_called_once_with("Add new test_entry entry? [Y/N]")

    with patch('builtins.input', side_effect='Yes') as in_mock:
        assert get_commit_new_flag("test_entry")
        in_mock.assert_called_once_with("Add new test_entry entry? [Y/N]")

def test06_get_commit_flag():
    """!
    @brief Test get_commit_flag method
    """
    with patch('builtins.input', side_effect='y') as in_mock:
        assert get_commit_flag("test_entry",['test_entry'])
        in_mock.assert_called_once_with("Overwrite existing test_entry entry? [Y/N]")
    with patch('builtins.input', side_effect='n') as in_mock:
        assert not get_commit_flag("test_entry",['test_entry'])
        in_mock.assert_called_once_with("Overwrite existing test_entry entry? [Y/N]")

    with patch('builtins.input', side_effect='y') as in_mock:
        assert get_commit_flag("test33",['test_entry'])
        in_mock.assert_called_once_with("Add new test33 entry? [Y/N]")
    with patch('builtins.input', side_effect='n') as in_mock:
        assert not get_commit_flag("test33",['test_entry'])
        in_mock.assert_called_once_with("Add new test33 entry? [Y/N]")

    assert get_commit_flag("test_entry",['test_entry'], True)

    with patch('builtins.input', side_effect='y') as in_mock:
        assert get_commit_flag("test33",['test_entry'], True)
        in_mock.assert_called_once_with("Add new test33 entry? [Y/N]")
    with patch('builtins.input', side_effect='n') as in_mock:
        assert not get_commit_flag("test33",['test_entry'], True)
        in_mock.assert_called_once_with("Add new test33 entry? [Y/N]")

def test07_new_entry_correct(capsys):
    """!
    @brief Test new_entry_correct method
    """
    with patch('builtins.input', side_effect='y') as in_mock:
        assert new_entry_correct("test_entry")
        in_mock.assert_called_once_with("Is this correct? [Y/N]")
        expected = "New Entry:\n"
        expected += "test_entry\n"
        assert capsys.readouterr().out == expected
    with patch('builtins.input', side_effect='n') as in_mock:
        assert not new_entry_correct("test_entry")
        in_mock.assert_called_once_with("Is this correct? [Y/N]")
        expected = "New Entry:\n"
        expected += "test_entry\n"
        assert capsys.readouterr().out == expected
