"""@package upcopyright_maintenancedate_copyright
@brief Scan source files and update copyright years
Scan the source files and update the copyright year in the header section of any modified files
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

import os
import io
import contextlib
from unittest.mock import patch, mock_open
import pytest

from code_tools_grocsoftware.base.insert_new_copyright_block import insert_new_copyright_block

from tests.dir_init import TESTFILEPATH
TEST_FILE_BASE_DIR = TESTFILEPATH

c_comment_parms =   {'blockStart': "/*", 'blockEnd': "*/", 'blockLineStart': "", 'singleLine': "//"}
pyCommentParms =  {'blockStart': "\"\"\"", 'blockEnd':"\"\"\"", 'blockLineStart': "", 'singleLine': "#"}
shCommentParms =  {'blockStart': None, 'blockEnd': None, 'blockLineStart': "#", 'singleLine': "#"}
batCommentParms = {'blockStart': None, 'blockEnd': None, 'blockLineStart': "REM ", 'singleLine': "REM ",}

class TestClass03InsertNewCopyrightBlock:
    """!
    @brief Test the insert_new_copyright_block function
    """
    @classmethod
    def setup_class(cls):
        """!
        @brief On test start open the input file
        """
        cls._input_file_name = os.path.join(TEST_FILE_BASE_DIR, "copyrighttest.h")
        cls._input_file = None
        # pylint: disable=consider-using-with
        cls._input_file = open(cls._input_file_name, mode='rt', encoding='utf-8')
        # pylint: enable=consider-using-with

    @classmethod
    def teardown_class(cls):
        """!
        @brief On test teardown close the file
        """
        cls._input_file.close()

    def test001_insert_new_copyright_block_write_fail(self):
        """!
        Test insert_new_copyright_block(), write file open failure
        """
        comment_blk_loc = {'blkStart': 0, 'blkEndEOL': 1082, 'blkEndSOL': 1079,
                           'copyrightMsgs': [
                               {'lineOffset': 3,
                                'text':" Copyright (c) 2022-2023 Randal Eike\n"}] }
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            with patch("builtins.open", mock_open()) as mock_wfile:
                mock_wfile.return_value = None
                mock_wfile.side_effect = Exception(OSError)
                with pytest.raises(Exception):
                    status = insert_new_copyright_block(self._input_file,
                                                        "test.c.out",
                                                        comment_blk_loc,
                                                        c_comment_parms,
                                                        "* Copyright (c) 2022-2023 Randal Eike\n",
                                                        ["test eula"])
                    assert not status
                    expected_err_str = "ERROR: Unable to open file \"test.c.out\" for writing " \
                                       "as text file.\n"
                    assert output.getvalue() == expected_err_str

    def test002_insert_new_copyright_block_replace_all(self):
        """!
        Test insert_new_copyright_block(), replace entire eula block
        """
        comment_blk_loc = {'blkStart': 0, 'blkEndEOL': 1082, 'blkEndSOL': 1079,
                           'copyrightMsgs': [
                               {'lineOffset': 3,
                                'text':" Copyright (c) 2022-2023 Randal Eike\n"}] }
        test_comment_markers = c_comment_parms
        test_comment_markers['blockLineStart'] = '*'
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            with patch("builtins.open", mock_open()) as mock_wfile:
                status = insert_new_copyright_block(self._input_file, "test.c.out",
                                                    comment_blk_loc, test_comment_markers,
                                                    "Copyright (c) 2022-2025 Randal Eike",
                                                    ["test eula"])
                assert status
                mock_wfile.assert_called_once_with('test.c.out', mode='wt', encoding='utf-8')
                handle = mock_wfile()
                # pylint: disable=line-too-long
                handle.write.assert_any_call('/*\n')
                handle.write.assert_any_call('* Copyright (c) 2022-2025 Randal Eike\n')
                handle.write.assert_any_call('*\n')
                handle.write.assert_any_call('* test eula\n')
                handle.write.assert_any_call('*/\n')
                handle.write.assert_any_call('\n')
                handle.write.assert_any_call('/**\n')
                handle.write.assert_any_call(' * @file copyrighttest.h\n')
                handle.write.assert_any_call(' * @ingroup test_copyright_msg_replacement\n')
                handle.write.assert_any_call(' * @{\n')
                handle.write.assert_any_call(' */\n')
                handle.write.assert_any_call('\n')
                handle.write.assert_any_call('// Single for test\n')
                handle.write.assert_any_call('\n')
                handle.write.assert_any_call('/**\n')
                handle.write.assert_any_call(' * @brief Useless dummy function to fill space in the file\n')
                handle.write.assert_any_call(' *\n')
                handle.write.assert_any_call(' * @param nothing - nothing at all\n')
                handle.write.assert_any_call(' */\n')
                handle.write.assert_any_call('void uselessFunction(int nothing);\n')
                handle.write.assert_any_call('\n')
                handle.write.assert_any_call('//==========================================================\n')
                handle.write.assert_any_call('// @brief Useless dummy function to fill space in the file\n')
                handle.write.assert_any_call('//\n')
                handle.write.assert_any_call('// @param nothing - nothing at all\n')
                handle.write.assert_any_call('//==========================================================\n')
                handle.write.assert_any_call('void uselessFunction2(int nothing);\n')
                handle.write.assert_any_call('/** @} */')
                # pylint: enable=line-too-long

    def test003_insert_new_copyright_block_replace_copyright_reformat(self):
        """!
        Test insert_new_copyright_block(), replace copyright, keep EULA, reformat comment block
        """
        comment_blk_loc = {'blkStart': 0, 'blkEndEOL': 1082, 'blkEndSOL': 1079,
                           'copyrightMsgs': [
                                {'lineOffset': 3,
                                 'text':" Copyright (c) 2022-2023 Randal Eike\n"}] }

        test_comment_markers = c_comment_parms
        test_comment_markers['blockLineStart'] = '*'
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            with patch("builtins.open", mock_open()) as mock_wfile:
                status = insert_new_copyright_block(self._input_file,
                                                    "test.c.out",
                                                    comment_blk_loc,
                                                    test_comment_markers,
                                                    "Copyright (c) 2022-2024 Randal Eike",
                                                    None)
                assert status
                mock_wfile.assert_called_once_with('test.c.out', mode='wt', encoding='utf-8')
                handle = mock_wfile()

                # pylint: disable=line-too-long
                handle.write.assert_any_call('/*\n')
                handle.write.assert_any_call('* Copyright (c) 2022-2024 Randal Eike\n')
                handle.write.assert_any_call('* \n')
                handle.write.assert_any_call('*  Permission is hereby granted, free of charge, to any person obtaining a\n')
                handle.write.assert_any_call('*  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n')
                handle.write.assert_any_call('*/\n')
                handle.write.assert_any_call('\n')
                handle.write.assert_any_call('/**\n')
                handle.write.assert_any_call(' * @file copyrighttest.h\n')
                handle.write.assert_any_call(' * @ingroup test_copyright_msg_replacement\n')
                handle.write.assert_any_call(' * @{\n')
                handle.write.assert_any_call(' */\n')
                handle.write.assert_any_call('\n')
                handle.write.assert_any_call('// Single for test\n')
                handle.write.assert_any_call('\n')
                handle.write.assert_any_call('/**\n')
                handle.write.assert_any_call(' * @brief Useless dummy function to fill space in the file\n')
                handle.write.assert_any_call(' *\n')
                handle.write.assert_any_call(' * @param nothing - nothing at all\n')
                handle.write.assert_any_call(' */\n')
                handle.write.assert_any_call('void uselessFunction(int nothing);\n')
                handle.write.assert_any_call('\n')
                handle.write.assert_any_call('//==========================================================\n')
                handle.write.assert_any_call('// @brief Useless dummy function to fill space in the file\n')
                handle.write.assert_any_call('//\n')
                handle.write.assert_any_call('// @param nothing - nothing at all\n')
                handle.write.assert_any_call('//==========================================================\n')
                handle.write.assert_any_call('void uselessFunction2(int nothing);\n')
                handle.write.assert_any_call('/** @} */')
                # pylint: enable=line-too-long

    def test004_insert_new_copyright_block_replace_all_not_start(self):
        """!
        Test insert_new_copyright_block(), replace entire eula block
        """
        comment_blk_loc = {'blkStart': 3, 'blkEndEOL': 1085, 'blkEndSOL': 1082,
                           'copyrightMsgs': [
                               {'lineOffset': 6, 'text':" Copyright (c) 2022-2023 Randal Eike\n"
                               }
                            ]
                          }
        test_comment_markers = c_comment_parms
        test_comment_markers['blockLineStart'] = '*'

        with patch("builtins.open", mock_open()) as mock_wfile:
            status = insert_new_copyright_block(self._input_file,
                                                "test.c.out",
                                                comment_blk_loc,
                                                test_comment_markers,
                                                "Copyright (c) 2022-2026 Randal Eike",
                                                ["test eula"])
            assert status
            mock_wfile.assert_called_once_with('test.c.out', mode='wt', encoding='utf-8')
            handle = mock_wfile()
            # pylint: disable=line-too-long
            handle.write.assert_any_call('//\n')
            handle.write.assert_any_call('/*\n')
            handle.write.assert_any_call('* Copyright (c) 2022-2026 Randal Eike\n')
            handle.write.assert_any_call('*\n')
            handle.write.assert_any_call('* test eula\n')
            handle.write.assert_any_call('*/\n')
            handle.write.assert_any_call('\n')
            handle.write.assert_any_call('/**\n')
            handle.write.assert_any_call(' * @file copyrighttest.h\n')
            handle.write.assert_any_call(' * @ingroup test_copyright_msg_replacement\n')
            handle.write.assert_any_call(' * @{\n')
            handle.write.assert_any_call(' */\n')
            handle.write.assert_any_call('\n')
            handle.write.assert_any_call('// Single for test\n')
            handle.write.assert_any_call('\n')
            handle.write.assert_any_call('/**\n')
            handle.write.assert_any_call(' * @brief Useless dummy function to fill space in the file\n')
            handle.write.assert_any_call(' *\n')
            handle.write.assert_any_call(' * @param nothing - nothing at all\n')
            handle.write.assert_any_call(' */\n')
            handle.write.assert_any_call('void uselessFunction(int nothing);\n')
            handle.write.assert_any_call('\n')
            handle.write.assert_any_call('//=========================================================\n')
            handle.write.assert_any_call('// @brief Useless dummy function to fill space in the file\n')
            handle.write.assert_any_call('//\n')
            handle.write.assert_any_call('// @param nothing - nothing at all\n')
            handle.write.assert_any_call('//==========================================================\n')
            handle.write.assert_any_call('void uselessFunction2(int nothing);\n')
            handle.write.assert_any_call('/** @} */')
            # pylint: enable=line-too-long
