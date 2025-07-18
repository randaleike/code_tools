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

import io
import contextlib
import pytest

from code_tools_grocsoftware.base.json_string_class_description import TransTxtParser

class Test01TranslationTextParser:
    """!
    @brief Unit test for the TransTxtParser class
    """
    def test01_make_text_entry(self):
        """!
        @brief Test make_text_entry()
        """
        trans_type, trans_str = TransTxtParser.make_text_entry("test text")
        assert trans_type == TransTxtParser.parsed_type_text
        assert trans_str == "test text"

    def test02_make_special_char_entry(self):
        """!
        @brief Test make_special_char_entry()
        """
        trans_type, trans_str = TransTxtParser.make_special_char_entry("'test'")
        assert trans_type == TransTxtParser.parsed_type_special
        assert trans_str == "'"

    def test03_make_param_entry(self):
        """!
        @brief Test make_param_entry()
        """
        trans_type, trans_str = TransTxtParser.make_param_entry("param1")
        assert trans_type == TransTxtParser.parsed_type_param
        assert trans_str == "param1"

    def test04_parse_text_block(self):
        """!
        @brief Test parse_text_block()
        """
        out_list = TransTxtParser.parse_text_block("This is a \"test\" string")
        assert len(out_list) == 5
        assert out_list[0][0] == TransTxtParser.parsed_type_text
        assert out_list[0][1] == "This is a "
        assert out_list[1][0] == TransTxtParser.parsed_type_special
        assert out_list[1][1] == '"'
        assert out_list[2][0] == TransTxtParser.parsed_type_text
        assert out_list[2][1] == "test"
        assert out_list[3][0] == TransTxtParser.parsed_type_special
        assert out_list[3][1] == '"'
        assert out_list[4][0] == TransTxtParser.parsed_type_text
        assert out_list[4][1] == " string"

    def test05_parse_text_block_special_end(self):
        """!
        @brief Test parse_text_block(), end on special character
        """
        out_list = TransTxtParser.parse_text_block("This is a \"test\"")
        assert len(out_list) == 4
        assert out_list[0][0] == TransTxtParser.parsed_type_text
        assert out_list[0][1] == "This is a "
        assert out_list[1][0] == TransTxtParser.parsed_type_special
        assert out_list[1][1] == '"'
        assert out_list[2][0] == TransTxtParser.parsed_type_text
        assert out_list[2][1] == "test"
        assert out_list[3][0] == TransTxtParser.parsed_type_special
        assert out_list[3][1] == '"'

    def test06_parse_text_block_special_start(self):
        """!
        @brief Test parse_text_block(), start on special character
        """
        out_list = TransTxtParser.parse_text_block("\"test\" string.")
        assert len(out_list) == 4
        assert out_list[0][0] == TransTxtParser.parsed_type_special
        assert out_list[0][1] == '"'
        assert out_list[1][0] == TransTxtParser.parsed_type_text
        assert out_list[1][1] == "test"
        assert out_list[2][0] == TransTxtParser.parsed_type_special
        assert out_list[2][1] == '"'
        assert out_list[3][0] == TransTxtParser.parsed_type_text
        assert out_list[3][1] == " string."

    def test07_parse_text_block_special_block(self):
        """!
        @brief Test parse_text_block(), start and end on special character
        """
        out_list = TransTxtParser.parse_text_block("\"test string\"")
        assert len(out_list) == 3
        assert out_list[0][0] == TransTxtParser.parsed_type_special
        assert out_list[0][1] == '"'
        assert out_list[1][0] == TransTxtParser.parsed_type_text
        assert out_list[1][1] == "test string"
        assert out_list[2][0] == TransTxtParser.parsed_type_special
        assert out_list[2][1] == '"'

    def test08_parse_translate_string_simple(self):
        """!
        @brief Test parse_translate_string(), single parameter, no quote
        """
        out_list = TransTxtParser.parse_translate_string("Simple with one @paramName@ in it")
        assert len(out_list) == 3
        assert out_list[0][0] == TransTxtParser.parsed_type_text
        assert out_list[0][1] == 'Simple with one '
        assert out_list[1][0] == TransTxtParser.parsed_type_param
        assert out_list[1][1] == "paramName"
        assert out_list[2][0] == TransTxtParser.parsed_type_text
        assert out_list[2][1] == ' in it'

    def test09_parse_translate_string_quoted_param(self):
        """!
        @brief Test parse_translate_string(), single quoted param
        """
        txt = "Quoted param single \"@paramName@\" in it"
        out_list = TransTxtParser.parse_translate_string(txt)
        assert len(out_list) == 5
        assert out_list[0][0] == TransTxtParser.parsed_type_text
        assert out_list[0][1] == 'Quoted param single '
        assert out_list[1][0] == TransTxtParser.parsed_type_special
        assert out_list[1][1] == '"'
        assert out_list[2][0] == TransTxtParser.parsed_type_param
        assert out_list[2][1] == "paramName"
        assert out_list[3][0] == TransTxtParser.parsed_type_special
        assert out_list[3][1] == '"'
        assert out_list[4][0] == TransTxtParser.parsed_type_text
        assert out_list[4][1] == ' in it'

    def test10_parse_translate_string_double_param(self):
        """!
        @brief Test parse_translate_string(), double parameter, no quote
        """
        txt = "Simple with @param_name1@ and @param_name2@ in it"
        out_list = TransTxtParser.parse_translate_string(txt)

        assert len(out_list) == 5
        assert out_list[0][0] == TransTxtParser.parsed_type_text
        assert out_list[0][1] == 'Simple with '
        assert out_list[1][0] == TransTxtParser.parsed_type_param
        assert out_list[1][1] == "param_name1"
        assert out_list[2][0] == TransTxtParser.parsed_type_text
        assert out_list[2][1] == ' and '
        assert out_list[3][0] == TransTxtParser.parsed_type_param
        assert out_list[3][1] == "param_name2"
        assert out_list[4][0] == TransTxtParser.parsed_type_text
        assert out_list[4][1] == ' in it'

    def test11_parse_translate_string_double_param_one_quoted(self):
        """!
        @brief Test parse_translate_string(), double parameter, one quoted
        """
        txt = "Quoted with @param_name1@ and \"@param_name2@\" in it"
        out_list = TransTxtParser.parse_translate_string(txt)

        assert len(out_list) == 7
        assert out_list[0][0] == TransTxtParser.parsed_type_text
        assert out_list[0][1] == 'Quoted with '
        assert out_list[1][0] == TransTxtParser.parsed_type_param
        assert out_list[1][1] == "param_name1"
        assert out_list[2][0] == TransTxtParser.parsed_type_text
        assert out_list[2][1] == ' and '
        assert out_list[3][0] == TransTxtParser.parsed_type_special
        assert out_list[3][1] == '"'
        assert out_list[4][0] == TransTxtParser.parsed_type_param
        assert out_list[4][1] == "param_name2"
        assert out_list[5][0] == TransTxtParser.parsed_type_special
        assert out_list[5][1] == '"'
        assert out_list[6][0] == TransTxtParser.parsed_type_text
        assert out_list[6][1] == ' in it'

    def test12_assemble_parsed_str_data(self):
        """!
        @brief Test assemble_parsed_str_data(), simple, one param, no quotes
        """
        param_list = [(TransTxtParser.parsed_type_text, "Simple text with "),
                     (TransTxtParser.parsed_type_param, "paramName")]
        out_str = TransTxtParser.assemble_parsed_str_data(param_list)
        assert out_str == "Simple text with @paramName@"

    def test13_assemble_parsed_str_data_quotes(self):
        """!
        @brief Test assemble_parsed_str_data(), simple, one param, quotes
        """
        param_list = [(TransTxtParser.parsed_type_text, "Simple text with "),
                     (TransTxtParser.parsed_type_special, "'"),
                     (TransTxtParser.parsed_type_param, "paramName"),
                     (TransTxtParser.parsed_type_special, "'")]
        out_str = TransTxtParser.assemble_parsed_str_data(param_list)
        assert out_str == "Simple text with '@paramName@'"

    def test14_assemble_parsed_str_data_quotes_multiple(self):
        """!
        @brief Test assemble_parsed_str_data(), Multiple, one param, quotes
        """
        param_list = [(TransTxtParser.parsed_type_text, "Multiple text with "),
                     (TransTxtParser.parsed_type_special, "'"),
                     (TransTxtParser.parsed_type_param, "paramName1"),
                     (TransTxtParser.parsed_type_special, "'"),
                     (TransTxtParser.parsed_type_text, " and "),
                     (TransTxtParser.parsed_type_param, "paramName2")]
        out_str = TransTxtParser.assemble_parsed_str_data(param_list)
        assert out_str == "Multiple text with '@paramName1@' and @paramName2@"

    def test15_assemble_parsed_str_data_failure(self):
        """!
        @brief Test assemble_parsed_str_data(), Multiple, one param, quotes
        """
        param_list = [(TransTxtParser.parsed_type_text, "Simple text with "),
                     (TransTxtParser.parsed_type_param, "paramName"),
                     ('Unknown', "paramName")]

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            with pytest.raises(TypeError):
                TransTxtParser.assemble_parsed_str_data(param_list)
                assert output == "Unknown string description tuple type: Unknown"

    def test16_assemble_stream(self):
        """!
        @brief Test assemble_parsed_str_data(), simple, one param, no quotes
        """
        param_list = [(TransTxtParser.parsed_type_text, "Simple text with "),
                     (TransTxtParser.parsed_type_param, "paramName")]
        out_str = TransTxtParser.assemble_stream(param_list)
        assert out_str == ' << "Simple text with " << paramName'

    def test17_assemble_stream_quotes(self):
        """!
        @brief Test assemble_parsed_str_data(), simple, one param, quotes
        """
        param_list = [(TransTxtParser.parsed_type_text, "Simple text with "),
                     (TransTxtParser.parsed_type_special, "'"),
                     (TransTxtParser.parsed_type_param, "paramName"),
                     (TransTxtParser.parsed_type_special, "'")]
        out_str = TransTxtParser.assemble_stream(param_list)
        assert out_str == ' << "Simple text with \\\'" << paramName << "\\\'"'

    def test18_assemble_stream_quotes_multiple(self):
        """!
        @brief Test assemble_parsed_str_data(), simple, one param, quotes
        """
        param_list = [(TransTxtParser.parsed_type_text, "Multiple text with "),
                     (TransTxtParser.parsed_type_special, "'"),
                     (TransTxtParser.parsed_type_param, "param_name1"),
                     (TransTxtParser.parsed_type_special, "'"),
                     (TransTxtParser.parsed_type_text, " and "),
                     (TransTxtParser.parsed_type_param, "param_name2")]
        out_str = TransTxtParser.assemble_stream(param_list)
        expstr = ' << "Multiple text with \\\''
        expstr += '" << param_name1 << "\\\' and " << param_name2'
        assert out_str == expstr

    def test19_assemble_stream_quotes_multiple_stream_spec(self):
        """!
        @brief Test assemble_parsed_str_data(), simple, one param, quotes,
               non-default stream operator
        """
        param_list = [(TransTxtParser.parsed_type_text, "Multiple text with "),
                     (TransTxtParser.parsed_type_special, "'"),
                     (TransTxtParser.parsed_type_param, "param_name1"),
                     (TransTxtParser.parsed_type_special, "'"),
                     (TransTxtParser.parsed_type_text, " and "),
                     (TransTxtParser.parsed_type_param, "param_name2")]
        out_str = TransTxtParser.assemble_stream(param_list, "+")
        assert out_str == ' + "Multiple text with \\\'" + param_name1 + "\\\' and " + param_name2'

    def test20_assemble_stream_fail(self):
        """!
        @brief Test assemble_parsed_str_data(), simple, one param, no quotes
        """
        param_list = [(TransTxtParser.parsed_type_text, "Simple text with "),
                     (TransTxtParser.parsed_type_param, "paramName"),
                     ('Unknown', "paramName")]

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            with pytest.raises(TypeError):
                TransTxtParser.assemble_stream(param_list)
                assert output == "Unknown string description tuple type: Unknown"

    def test21_is_parsed_text_type(self):
        """!
        @brief Test is_parsed_text_type()
        """
        assert TransTxtParser.is_parsed_text_type((TransTxtParser.parsed_type_text, "text"))
        assert not TransTxtParser.is_parsed_text_type((TransTxtParser.parsed_type_param,
                                                       "paramName"))
        assert not TransTxtParser.is_parsed_text_type((TransTxtParser.parsed_type_special, "'"))
        assert not TransTxtParser.is_parsed_text_type(('notOne', ""))

    def test22_is_parsed_param_type(self):
        """!
        @brief Test is_parsed_param_type()
        """
        assert not TransTxtParser.is_parsed_param_type((TransTxtParser.parsed_type_text, "text"))
        assert TransTxtParser.is_parsed_param_type((TransTxtParser.parsed_type_param, "paramName"))
        assert not TransTxtParser.is_parsed_param_type((TransTxtParser.parsed_type_special, "'"))
        assert not TransTxtParser.is_parsed_text_type(('notOne', ""))

    def test23_is_parsed_special_type(self):
        """!
        @brief Test is_parsed_special_type()
        """
        assert not TransTxtParser.is_parsed_special_type((TransTxtParser.parsed_type_text, "text"))
        assert not TransTxtParser.is_parsed_special_type((TransTxtParser.parsed_type_param,
                                                          "paramName"))
        assert TransTxtParser.is_parsed_special_type((TransTxtParser.parsed_type_special, "'"))
        assert not TransTxtParser.is_parsed_text_type(('notOne', ""))

    def test24_get_parsed_str_data(self):
        """!
        @brief Test get_parsed_str_data()
        """
        txt_entry = TransTxtParser.get_parsed_str_data((TransTxtParser.parsed_type_text, "text"))
        assert txt_entry == "text"

        parm_entry = TransTxtParser.get_parsed_str_data((TransTxtParser.parsed_type_param,
                                                        "paramName"))
        assert parm_entry == "paramName"

        spcl_entry = TransTxtParser.get_parsed_str_data((TransTxtParser.parsed_type_special, "'"))
        assert spcl_entry == "'"

        assert TransTxtParser.get_parsed_str_data(('notOne', "55")) == "55"

    def test25_assemble_test_return_string(self):
        """!
        @brief Test assemble_test_return_string()
        """
        test_tuple = [(TransTxtParser.parsed_type_text, "Starting text "),
                     (TransTxtParser.parsed_type_special, '"'),
                     (TransTxtParser.parsed_type_param, 'paramName'),
                     (TransTxtParser.parsed_type_special, '"')]
        value_xlate_dict = {'paramName': ("xlateName", False)}
        retstr = TransTxtParser.assemble_test_return_string(test_tuple, value_xlate_dict)
        assert retstr == "Starting text \\\"xlateName\\\""

    def test26_assemble_test_return_string_error(self):
        """!
        @brief Test assemble_test_return_string() error
        """
        test_tuple = [(TransTxtParser.parsed_type_text, "Starting text "),
                     ('unknown', ''),
                     (TransTxtParser.parsed_type_special, '"'),
                     (TransTxtParser.parsed_type_param, 'paramName'),
                     (TransTxtParser.parsed_type_special, '"')
                     ]
        value_xlate_dict = {'paramName': ("xlateName", False)}
        with pytest.raises(TypeError):
            retstr = TransTxtParser.assemble_test_return_string(test_tuple, value_xlate_dict)
            assert retstr == "Starting text "
