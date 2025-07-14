"""@package langstringautogen
Utility to automatically generate language strings using google translate api
for a language string generation library
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

def mult_line_format(raw_text:str, max_length:int = 80, padchar:str = None)->list:
    """!
    @brief Break the long text string into a list of strings that do not
           exceed the max_length input parameter

    @param raw_text (string) - Long EULA line text
    @param max_length (integer) - Maximum line length for the EULA text, default = 80
    @param pad (char) - Character to pad the end of the line with or
                        None if no padding is required

    @return list of strings, List of strings broken at the appropriate length
    """

    formatted_text = []

    while len(raw_text) > max_length:
        # Find a good breaking point
        current_index = max_length-1
        while (re.match(r'[\s,\.-]',raw_text[current_index]) is None) and (current_index > 0):
            current_index -= 1

        if current_index == 0:
            # No good break found, just truncate and max length
            formatted_text.append(raw_text[:max_length])
            raw_text = raw_text[max_length:]
        else:
            # Good break found, truncate to the good location
            # Get the partial text and strip the trailing space if present
            new_line = raw_text[:current_index]
            new_line.strip()

            # Add the new line to the list
            if padchar is not None:
                formatted_text.append(new_line.ljust(max_length, padchar))
            else:
                formatted_text.append(new_line)

            # Strip the preceeding space if present
            while raw_text[current_index] == ' ':
                current_index += 1

            # Get the remaining string
            raw_text = raw_text[current_index:]

    # Strip leading and trailing spaces for the last line
    new_line = raw_text.strip()
    if new_line != '':
        # Add the last line to the list
        if padchar is not None:
            formatted_text.append(new_line.ljust(max_length, padchar))
        else:
            formatted_text.append(new_line)

    return formatted_text
