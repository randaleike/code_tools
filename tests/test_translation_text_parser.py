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

import pytest


import io
import contextlib

from dir_init import TESTFILEPATH
from dir_init import pathincsetup
pathincsetup()

from code_tools_grocsoftware.base.json_string_class_description import TranslationTextParser

class TestUnittest01TranslationTextParser:
    """!
    @brief Unit test for the TranslationTextParser class
    """
    def test01MakeTextEntry(self):
        """!
        @brief Test makeTextEntry()
        """
        transType, transStr = TranslationTextParser.makeTextEntry("test text")
        assert transType == TranslationTextParser.parsedTypeText
        assert transStr == "test text"

    def test02MakeSpecialCharEntry(self):
        """!
        @brief Test makeSpecialCharEntry()
        """
        transType, transStr = TranslationTextParser.makeSpecialCharEntry("'test'")
        assert transType == TranslationTextParser.parsedTypeSpecial
        assert transStr == "'"

    def test03MakeParamEntry(self):
        """!
        @brief Test makeParamEntry()
        """
        transType, transStr = TranslationTextParser.makeParamEntry("param1")
        assert transType == TranslationTextParser.parsedTypeParam
        assert transStr == "param1"

    def test04ParseTextBlock(self):
        """!
        @brief Test parseTextBlock()
        """
        outList = TranslationTextParser.parseTextBlock("This is a \"test\" string")
        assert len(outList) == 5
        assert outList[0][0] == TranslationTextParser.parsedTypeText
        assert outList[0][1] == "This is a "
        assert outList[1][0] == TranslationTextParser.parsedTypeSpecial
        assert outList[1][1] == '"'
        assert outList[2][0] == TranslationTextParser.parsedTypeText
        assert outList[2][1] == "test"
        assert outList[3][0] == TranslationTextParser.parsedTypeSpecial
        assert outList[3][1] == '"'
        assert outList[4][0] == TranslationTextParser.parsedTypeText
        assert outList[4][1] == " string"

    def test05ParseTextBlockSpecialEnd(self):
        """!
        @brief Test parseTextBlock(), end on special character
        """
        outList = TranslationTextParser.parseTextBlock("This is a \"test\"")
        assert len(outList) == 4
        assert outList[0][0] == TranslationTextParser.parsedTypeText
        assert outList[0][1] == "This is a "
        assert outList[1][0] == TranslationTextParser.parsedTypeSpecial
        assert outList[1][1] == '"'
        assert outList[2][0] == TranslationTextParser.parsedTypeText
        assert outList[2][1] == "test"
        assert outList[3][0] == TranslationTextParser.parsedTypeSpecial
        assert outList[3][1] == '"'

    def test06ParseTextBlockSpecialStart(self):
        """!
        @brief Test parseTextBlock(), start on special character
        """
        outList = TranslationTextParser.parseTextBlock("\"test\" string.")
        assert len(outList) == 4
        assert outList[0][0] == TranslationTextParser.parsedTypeSpecial
        assert outList[0][1] == '"'
        assert outList[1][0] == TranslationTextParser.parsedTypeText
        assert outList[1][1] == "test"
        assert outList[2][0] == TranslationTextParser.parsedTypeSpecial
        assert outList[2][1] == '"'
        assert outList[3][0] == TranslationTextParser.parsedTypeText
        assert outList[3][1] == " string."

    def test07ParseTextBlockSpecialBlock(self):
        """!
        @brief Test parseTextBlock(), start and end on special character
        """
        outList = TranslationTextParser.parseTextBlock("\"test string\"")
        assert len(outList) == 3
        assert outList[0][0] == TranslationTextParser.parsedTypeSpecial
        assert outList[0][1] == '"'
        assert outList[1][0] == TranslationTextParser.parsedTypeText
        assert outList[1][1] == "test string"
        assert outList[2][0] == TranslationTextParser.parsedTypeSpecial
        assert outList[2][1] == '"'

    def test08ParseTranslateStringSimple(self):
        """!
        @brief Test parseTranslateString(), single parameter, no quote
        """
        outList = TranslationTextParser.parseTranslateString("Simple with one @paramName@ in it")
        assert len(outList) == 3
        assert outList[0][0] == TranslationTextParser.parsedTypeText
        assert outList[0][1] == 'Simple with one '
        assert outList[1][0] == TranslationTextParser.parsedTypeParam
        assert outList[1][1] == "paramName"
        assert outList[2][0] == TranslationTextParser.parsedTypeText
        assert outList[2][1] == ' in it'

    def test09ParseTranslateStringQuotedParam(self):
        """!
        @brief Test parseTranslateString(), single quoted param
        """
        outList = TranslationTextParser.parseTranslateString("Quoted param single \"@paramName@\" in it")
        assert len(outList) == 5
        assert outList[0][0] == TranslationTextParser.parsedTypeText
        assert outList[0][1] == 'Quoted param single '
        assert outList[1][0] == TranslationTextParser.parsedTypeSpecial
        assert outList[1][1] == '"'
        assert outList[2][0] == TranslationTextParser.parsedTypeParam
        assert outList[2][1] == "paramName"
        assert outList[3][0] == TranslationTextParser.parsedTypeSpecial
        assert outList[3][1] == '"'
        assert outList[4][0] == TranslationTextParser.parsedTypeText
        assert outList[4][1] == ' in it'

    def test10ParseTranslateStringDoubleParam(self):
        """!
        @brief Test parseTranslateString(), double parameter, no quote
        """
        outList = TranslationTextParser.parseTranslateString("Simple with @paramName1@ and @paramName2@ in it")
        assert len(outList) == 5
        assert outList[0][0] == TranslationTextParser.parsedTypeText
        assert outList[0][1] == 'Simple with '
        assert outList[1][0] == TranslationTextParser.parsedTypeParam
        assert outList[1][1] == "paramName1"
        assert outList[2][0] == TranslationTextParser.parsedTypeText
        assert outList[2][1] == ' and '
        assert outList[3][0] == TranslationTextParser.parsedTypeParam
        assert outList[3][1] == "paramName2"
        assert outList[4][0] == TranslationTextParser.parsedTypeText
        assert outList[4][1] == ' in it'

    def test11ParseTranslateStringDoubleParamOneQuoted(self):
        """!
        @brief Test parseTranslateString(), double parameter, one quoted
        """
        outList = TranslationTextParser.parseTranslateString("Quoted with @paramName1@ and \"@paramName2@\" in it")
        assert len(outList) == 7
        assert outList[0][0] == TranslationTextParser.parsedTypeText
        assert outList[0][1] == 'Quoted with '
        assert outList[1][0] == TranslationTextParser.parsedTypeParam
        assert outList[1][1] == "paramName1"
        assert outList[2][0] == TranslationTextParser.parsedTypeText
        assert outList[2][1] == ' and '
        assert outList[3][0] == TranslationTextParser.parsedTypeSpecial
        assert outList[3][1] == '"'
        assert outList[4][0] == TranslationTextParser.parsedTypeParam
        assert outList[4][1] == "paramName2"
        assert outList[5][0] == TranslationTextParser.parsedTypeSpecial
        assert outList[5][1] == '"'
        assert outList[6][0] == TranslationTextParser.parsedTypeText
        assert outList[6][1] == ' in it'

    def test12AssembleParsedStrData(self):
        """!
        @brief Test assembleParsedStrData(), simple, one param, no quotes
        """
        paramList = [(TranslationTextParser.parsedTypeText, "Simple text with "),
                     (TranslationTextParser.parsedTypeParam, "paramName")]
        outStr = TranslationTextParser.assembleParsedStrData(paramList)
        assert outStr == "Simple text with @paramName@"

    def test13AssembleParsedStrDataQuotes(self):
        """!
        @brief Test assembleParsedStrData(), simple, one param, quotes
        """
        paramList = [(TranslationTextParser.parsedTypeText, "Simple text with "),
                     (TranslationTextParser.parsedTypeSpecial, "'"),
                     (TranslationTextParser.parsedTypeParam, "paramName"),
                     (TranslationTextParser.parsedTypeSpecial, "'")]
        outStr = TranslationTextParser.assembleParsedStrData(paramList)
        assert outStr == "Simple text with '@paramName@'"

    def test14AssembleParsedStrDataQuotesMultiple(self):
        """!
        @brief Test assembleParsedStrData(), Multiple, one param, quotes
        """
        paramList = [(TranslationTextParser.parsedTypeText, "Multiple text with "),
                     (TranslationTextParser.parsedTypeSpecial, "'"),
                     (TranslationTextParser.parsedTypeParam, "paramName1"),
                     (TranslationTextParser.parsedTypeSpecial, "'"),
                     (TranslationTextParser.parsedTypeText, " and "),
                     (TranslationTextParser.parsedTypeParam, "paramName2")]
        outStr = TranslationTextParser.assembleParsedStrData(paramList)
        assert outStr == "Multiple text with '@paramName1@' and @paramName2@"

    def test15AssembleParsedStrDataFailure(self):
        """!
        @brief Test assembleParsedStrData(), Multiple, one param, quotes
        """
        paramList = [(TranslationTextParser.parsedTypeText, "Simple text with "),
                     (TranslationTextParser.parsedTypeParam, "paramName"),
                     ('Unknown', "paramName")]

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            with pytest.raises(TypeError):
                outStr = TranslationTextParser.assembleParsedStrData(paramList)
                assert output == "Unknown string description tuple type: Unknown"

    def test16AssembleStream(self):
        """!
        @brief Test assembleParsedStrData(), simple, one param, no quotes
        """
        paramList = [(TranslationTextParser.parsedTypeText, "Simple text with "),
                     (TranslationTextParser.parsedTypeParam, "paramName")]
        outStr = TranslationTextParser.assembleStream(paramList)
        assert outStr == ' << "Simple text with " << paramName'

    def test17AssembleStreamQuotes(self):
        """!
        @brief Test assembleParsedStrData(), simple, one param, quotes
        """
        paramList = [(TranslationTextParser.parsedTypeText, "Simple text with "),
                     (TranslationTextParser.parsedTypeSpecial, "'"),
                     (TranslationTextParser.parsedTypeParam, "paramName"),
                     (TranslationTextParser.parsedTypeSpecial, "'")]
        outStr = TranslationTextParser.assembleStream(paramList)
        assert outStr == ' << "Simple text with \\\'" << paramName << "\\\'"'

    def test18AssembleStreamQuotesMultiple(self):
        """!
        @brief Test assembleParsedStrData(), simple, one param, quotes
        """
        paramList = [(TranslationTextParser.parsedTypeText, "Multiple text with "),
                     (TranslationTextParser.parsedTypeSpecial, "'"),
                     (TranslationTextParser.parsedTypeParam, "paramName1"),
                     (TranslationTextParser.parsedTypeSpecial, "'"),
                     (TranslationTextParser.parsedTypeText, " and "),
                     (TranslationTextParser.parsedTypeParam, "paramName2")]
        outStr = TranslationTextParser.assembleStream(paramList)
        assert outStr == ' << "Multiple text with \\\'" << paramName1 << "\\\' and " << paramName2'

    def test19AssembleStreamQuotesMultipleStreamSpec(self):
        """!
        @brief Test assembleParsedStrData(), simple, one param, quotes, non-default stream operator
        """
        paramList = [(TranslationTextParser.parsedTypeText, "Multiple text with "),
                     (TranslationTextParser.parsedTypeSpecial, "'"),
                     (TranslationTextParser.parsedTypeParam, "paramName1"),
                     (TranslationTextParser.parsedTypeSpecial, "'"),
                     (TranslationTextParser.parsedTypeText, " and "),
                     (TranslationTextParser.parsedTypeParam, "paramName2")]
        outStr = TranslationTextParser.assembleStream(paramList, "+")
        assert outStr == ' + "Multiple text with \\\'" + paramName1 + "\\\' and " + paramName2'

    def test20AssembleStreamFail(self):
        """!
        @brief Test assembleParsedStrData(), simple, one param, no quotes
        """
        paramList = [(TranslationTextParser.parsedTypeText, "Simple text with "),
                     (TranslationTextParser.parsedTypeParam, "paramName"),
                     ('Unknown', "paramName")]

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            with pytest.raises(TypeError):
                outStr = TranslationTextParser.assembleStream(paramList)
                assert output == "Unknown string description tuple type: Unknown"

    def test21IsParsedTextType(self):
        """!
        @brief Test isParsedTextType()
        """
        assert TranslationTextParser.isParsedTextType((TranslationTextParser.parsedTypeText, "text"))
        assert not TranslationTextParser.isParsedTextType((TranslationTextParser.parsedTypeParam, "paramName"))
        assert not TranslationTextParser.isParsedTextType((TranslationTextParser.parsedTypeSpecial, "'"))
        assert not TranslationTextParser.isParsedTextType(('notOne', ""))

    def test22IsParsedParamType(self):
        """!
        @brief Test isParsedParamType()
        """
        assert not TranslationTextParser.isParsedParamType((TranslationTextParser.parsedTypeText, "text"))
        assert TranslationTextParser.isParsedParamType((TranslationTextParser.parsedTypeParam, "paramName"))
        assert not TranslationTextParser.isParsedParamType((TranslationTextParser.parsedTypeSpecial, "'"))
        assert not TranslationTextParser.isParsedTextType(('notOne', ""))

    def test23IsParsedSpecialType(self):
        """!
        @brief Test isParsedSpecialType()
        """
        assert not TranslationTextParser.isParsedSpecialType((TranslationTextParser.parsedTypeText, "text"))
        assert not TranslationTextParser.isParsedSpecialType((TranslationTextParser.parsedTypeParam, "paramName"))
        assert TranslationTextParser.isParsedSpecialType((TranslationTextParser.parsedTypeSpecial, "'"))
        assert not TranslationTextParser.isParsedTextType(('notOne', ""))

    def test24GetParsedStrData(self):
        """!
        @brief Test getParsedStrData()
        """
        assert TranslationTextParser.getParsedStrData((TranslationTextParser.parsedTypeText, "text")) == "text"
        assert TranslationTextParser.getParsedStrData((TranslationTextParser.parsedTypeParam, "paramName")) == "paramName"
        assert TranslationTextParser.getParsedStrData((TranslationTextParser.parsedTypeSpecial, "'")) == "'"
        assert TranslationTextParser.getParsedStrData(('notOne', "55")) == "55"

    def test25AssembleTestReturnString(self):
        """!
        @brief Test assembleTestReturnString()
        """
        testTuple = [(TranslationTextParser.parsedTypeText, "Starting text "),
                     (TranslationTextParser.parsedTypeSpecial, '"'),
                     (TranslationTextParser.parsedTypeParam, 'paramName'),
                     (TranslationTextParser.parsedTypeSpecial, '"')]
        valueXlateDict = {'paramName': ("xlateName", False)}
        assert TranslationTextParser.assembleTestReturnString(testTuple, valueXlateDict) == "Starting text \\\"xlateName\\\""

    def test26AssembleTestReturnStringError(self):
        """!
        @brief Test assembleTestReturnString() error
        """
        testTuple = [(TranslationTextParser.parsedTypeText, "Starting text "),
                     ('unknown', ''),
                     (TranslationTextParser.parsedTypeSpecial, '"'),
                     (TranslationTextParser.parsedTypeParam, 'paramName'),
                     (TranslationTextParser.parsedTypeSpecial, '"')
                     ]
        valueXlateDict = {'paramName': ("xlateName", False)}
        with pytest.raises(TypeError):
            assert TranslationTextParser.assembleTestReturnString(testTuple, valueXlateDict) == "Starting text "
