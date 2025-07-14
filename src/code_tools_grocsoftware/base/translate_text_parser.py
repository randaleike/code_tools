"""@package langstringautogen
Utility to automatically generate language strings using google translate api
for a language string generation library
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

import re

class TransTxtParser():
    """!
    Translation text helper functions
    """
    ## Text string marker
    parsed_type_text    = 'text'
    ## Parameter name marker
    parsed_type_param   = 'param'
    ## Special character marker
    parsed_type_special = 'special'

    @staticmethod
    def make_text_entry(text_block:str)->tuple:
        """!
        @brief Make a parsed text tuple object
        @param text_block {string} Text string for the tuple
        @return tuple - (TransTxtParser.parsed_type_text, text_block)
        """
        return (TransTxtParser.parsed_type_text, text_block)

    @staticmethod
    def make_special_char_entry(text_block:str)->tuple:
        """!
        @brief Make a special character tuple object
        @param text_block {string} Special character for the tuple
        @return tuple - (TransTxtParser.parsed_type_special, text_block)
        """
        return (TransTxtParser.parsed_type_special, text_block[0])

    @staticmethod
    def make_param_entry(param_name:str)->tuple:
        """!
        @brief Make a parameter name tuple object
        @param param_name {string} Special character for the tuple
        @return tuple - (TransTxtParser.parsed_type_param, param_name)
        """
        return (TransTxtParser.parsed_type_param, param_name)

    #pylint: disable=consider-using-f-string
    @staticmethod
    def parse_text_block(text_block:str)->list:
        """!
        @brief Convert the input string to an output string stream
        @param text_block {string} String to convert
        @return list of dictionaries - List of dictionary entries descibing the parsed string
        """
        match_list = re.finditer(r'\\|\"', text_block)

        string_list = []
        previous_end = 0
        for match_data in match_list:
            # Add text data prior to first match if any
            if match_data.start() > previous_end:
                raw_text = r'{}'.format(text_block[previous_end:match_data.start()])
                string_list.append(TransTxtParser.make_text_entry(raw_text))

            # Add the matched parameter
            string_list.append(TransTxtParser.make_special_char_entry(match_data.group()))
            previous_end = match_data.end()

        # Add the trailing string
        if previous_end < len(text_block):
            raw_text = r'{}'.format(text_block[previous_end:])
            string_list.append(TransTxtParser.make_text_entry(raw_text))

        return string_list
    #pylint: enable=consider-using-f-string

    @staticmethod
    def parse_translate_string(base_string:str)->list:
        """!
        @brief Convert the input string to an output string stream
        @param base_string {string} String to convert
        @return list of tuples - List of tuples descibing the parsed string
                                 tuple[0] = type, TransTxtParser.parsed_type_text or
                                                  TransTxtParser.parsed_type_param
                                 tuple[1] = data, if TransTxtParser.parsed_type_text = text string
                                                  if TransTxtParser.parsed_type_param = param name
        """
        match_list = re.finditer(r'@[a-zA-Z_][a-zA-Z0-9_]*@', base_string)

        # pylint: disable=consider-using-f-string
        string_list = []
        previous_end = 0
        for match_data in match_list:
            # Add text data prior to first match if any
            if match_data.start() > previous_end:
                raw_text = r'{}'.format(base_string[previous_end:match_data.start()])
                string_list.extend(TransTxtParser.parse_text_block(raw_text))

            # Add the matched parameter
            string_list.append(TransTxtParser.make_param_entry(match_data.group()[1:-1]))
            previous_end = match_data.end()

        # Add the trailing string
        if previous_end < len(base_string):
            raw_text = r'{}'.format(base_string[previous_end:])
            string_list.extend(TransTxtParser.parse_text_block(raw_text))

        # pylint: enable=consider-using-f-string

        return string_list

    @staticmethod
    def assemble_parsed_str_data(string_tuple_list:list)->str:
        """!
        @brief Assemble the input string description tuple list into a translation string
        @param string_tuple_list (list) List of string description tuples
        @return string - Assempled text string ready for input into a language translation engine
        """
        return_text = ""
        for desc_type, desc_data in string_tuple_list:
            if TransTxtParser.parsed_type_text == desc_type:
                return_text += desc_data
            elif TransTxtParser.parsed_type_param == desc_type:
                return_text += '@'
                return_text += desc_data
                return_text += '@'
            elif TransTxtParser.parsed_type_special == desc_type:
                return_text += desc_data
            else:
                raise TypeError("Unknown string description tuple type: "+desc_type)

        return return_text

    @staticmethod
    def assemble_stream(string_tuple_list:list, stream_operator:str = "<<")->str:
        """!
        @brief Assemble the input string description tuple list into a translation string
        @param string_tuple_list (list) List of string description tuples
        @param stream_operator (string) Language specific stream operator
        @return string - Assempled text string ready for input into a language translation engine
        """
        return_text = ""
        string_open = False

        for desc_type, desc_data in string_tuple_list:
            if TransTxtParser.parsed_type_text == desc_type:
                if not string_open:
                    return_text += " "
                    return_text += stream_operator
                    return_text += " \""
                    string_open = True
                return_text += desc_data
            elif TransTxtParser.parsed_type_param == desc_type:
                if string_open:
                    return_text += "\" "
                    return_text += stream_operator
                    return_text += " "
                    string_open = False
                return_text += desc_data
            elif TransTxtParser.parsed_type_special == desc_type:
                if not string_open:
                    return_text += " "
                    return_text += stream_operator
                    return_text += " \""
                    string_open = True
                return_text += "\\"+desc_data
            else:
                raise TypeError("Unknown string description tuple type: "+desc_type)

        # Close the open string if present
        if string_open:
            return_text += "\""
            string_open = False
        return return_text

    @staticmethod
    def assemble_test_return_string(string_tuple_list:list, value_xlate_dict:dict)->str:
        """!
        @brief Assemble the input string description tuple list into a translation string
        @param string_tuple_list (list) List of string description tuples
        @param value_xlate_dict (dict) Dictionary of param names and expected values
        @return string - Assempled text string ready for input into a language translation
                         expected string
        """
        return_text = ""
        for desc_type, desc_data in string_tuple_list:
            if TransTxtParser.parsed_type_text == desc_type:
                return_text += desc_data
            elif TransTxtParser.parsed_type_param == desc_type:
                value, _ = value_xlate_dict[desc_data]
                return_text += value
            elif TransTxtParser.parsed_type_special == desc_type:
                return_text += "\\"+desc_data
            else:
                raise TypeError("Unknown string description tuple type: "+desc_type)
        return return_text

    @staticmethod
    def is_parsed_text_type(parsed_tuple:tuple)->bool:
        """!
        @brief Check if the input pget_parsed_str_dataarsed translation tuple is a text type
        @return boolean - True if tuple[0] == TransTxtParser.parsed_type_text
                          else False
        """
        return bool(parsed_tuple[0] == TransTxtParser.parsed_type_text)

    @staticmethod
    def is_parsed_param_type(parsed_tuple:tuple)->bool:
        """!
        @brief Check if the input parsed translation tuple is a parameter type
        @return boolean - True if tuple[0] == TransTxtParser.parsed_type_param
                          else False
        """
        return bool(parsed_tuple[0] == TransTxtParser.parsed_type_param)

    @staticmethod
    def is_parsed_special_type(parsed_tuple:tuple)->bool:
        """!
        @brief Check if the input parsed translation tuple is a special character type
        @return boolean - True if tuple[0] == TransTxtParser.parsed_type_param
                          else False
        """
        return bool(parsed_tuple[0] == TransTxtParser.parsed_type_special)

    @staticmethod
    def get_parsed_str_data(parsed_tuple:tuple)->bool:
        """!
        @brief Get the tuple string data field
        @return string - pared_tuple data field
        """
        return parsed_tuple[1]
