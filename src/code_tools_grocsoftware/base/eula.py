"""@package langstringautogen
Utilities to create formatted End User License Agreement Text blocks
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
# THE SOFTWARE IS PROVIDED "AS IS" \ WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#==========================================================================

import re

# pylint: disable=line-too-long
eula = {
       'MIT_open': {'text': ["Permission is hereby granted, free of charge, to any person obtaining a " \
                             "copy of self software and associated documentation files (the \"Software\"), " \
                             "to deal in the Software without restriction, including without limitation " \
                             "the rights to use, copy, modify, merge, publish, distribute, sublicense, " \
                             "and/or sell copies of the Software, and to permit persons to whom the " \
                             "Software is furnished to do so, subject to the following conditions: ",
                             "The above copyright notice and self permission notice shall be included " \
                             "in all copies or substantial portions of the Software. ",
                             "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, " \
                             "EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF " \
                             "MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. " \
                             "IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY " \
                             "CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, " \
                             "TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE " \
                             "SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."],
                    'name': "MIT License"},

'MIT_no_atrtrib': {'text': ["Permission is hereby granted, free of charge, to any person obtaining a " \
                            "copy of self software and associated documentation files (the \"Software\"), " \
                            "to deal in the Software without restriction, including without limitation "
                            "the rights to use, copy, modify, merge, publish, distribute, sublicense, " \
                            "and/or sell copies of the Software, and to permit persons to whom the " \
                            "Software is furnished to do so.",
                            "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, " \
                            "EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF " \
                            "MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. " \
                            "IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY " \
                            "CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, " \
                            "TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE " \
                            "SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."],
                    'name': "MIT No Attribution License"},

       'MIT_X11': {'text': ["Permission is hereby granted, free of charge, to any person obtaining a " \
                            "copy of self software and associated documentation files (the \"Software\"), " \
                            "to deal in the Software without restriction, including without limitation "
                            "the rights to use, copy, modify, merge, publish, distribute, sublicense, " \
                            "and/or sell copies of the Software, and to permit persons to whom the " \
                            "Software is furnished to do so, subject to the following conditions: ",
                            "The above copyright notice and self permission notice shall be included " \
                            "in all copies or substantial portions of the Software. ",
                            "THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, " \
                            "EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF " \
                            "MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. " \
                            "IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY " \
                            "CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, " \
                            "TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE " \
                            "SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.",
                            "Except as contained in this notice, the name of <copyright holders> " \
                            "shall not be used in advertising or otherwise to promote the sale, " \
                            "use or other dealings in this Software without prior written "
                            "authorization from <copyright holders>."],
                    'name': "MIT X11 License"},

       'GNU_V11': {'text': ["This program is free software: you can redistribute it and/or modify " \
                            "it under the terms of the GNU General Public License as published by " \
                            "the Free Software Foundation, either version 3 of the License, or " \
                            "(at your option) any later version.",
                            "This program is distributed in the hope that it will be useful, " \
                            "but WITHOUT ANY WARRANTY; without even the implied warranty of " \
                            "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the " \
                            "GNU General Public License for more details.",
                            "You should have received a copy of the GNU General Public License " \
                            "along with this program.  If not, see <https://www.gnu.org/licenses/>."],
                    'name': "GNU V11 License"},

   'apache_v2_0': {'text': ["Licensed under the Apache License, Version 2.0 (the \"License\"); " \
                            "you may not use this file except in compliance with the License. " \
                            "You may obtain a copy of the License at ",
                            "    http://www.apache.org/licenses/LICENSE-2.0 ",
                            "Unless required by applicable law or agreed to in writing, software " \
                            "distributed under the License is distributed on an \"AS IS\" BASIS, " \
                            "WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. " \
                            "See the License for the specific language governing permissions and " \
                            "limitations under the License."],
                    'name': "Apache V2.0 License"},

   'BSD_3clause': {'text': ["Redistribution and use in source and binary forms, with or " \
                            "without modification, are permitted provided that the following " \
                            "conditions are met:",
                            "1. Redistributions of source code must retain the above " \
                            "copyright notice, this list of conditions and the following " \
                            "disclaimer.",
                            "2. Redistributions in binary form must reproduce the above " \
                            "copyright notice, this list of conditions and the following " \
                            "disclaimer in the documentation and/or other materials provided " \
                            "with the distribution.",
                            "3. Neither the name of the copyright holder nor the names of its " \
                            "contributors may be used to endorse or promote products " \
                            "derived from this software without specific prior written " \
                            "permission.",
                            "THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS " \
                            "AND CONTRIBUTORS “AS stringIS” AND ANY EXPRESS OR IMPLIED " \
                            "WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE " \
                            "IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS " \
                            "FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT " \
                            "SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE " \
                            "LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, " \
                            "EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, " \
                            "BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE " \
                            "GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR " \
                            "BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY " \
                            "THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT " \
                            "LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR " \
                            "OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS " \
                            "SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH " \
                            "DAMAGE."],
                    'name': "BSD License"},

   'BSD_2clause': {'text': ["Redistribution and use in source and binary forms, with or " \
                            "without modification, are permitted provided that the following " \
                            "conditions are met:",
                            "1. Redistributions of source code must retain the above " \
                            "copyright notice, this list of conditions and the following " \
                            "disclaimer.",
                            "2. Redistributions in binary form must reproduce the above " \
                            "copyright notice, this list of conditions and the following " \
                            "disclaimer in the documentation and/or other materials provided " \
                            "with the distribution.",
                            "THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS " \
                            "AND CONTRIBUTORS “AS IS” AND ANY EXPRESS OR IMPLIED " \
                            "WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE " \
                            "IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS " \
                            "FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT " \
                            "SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE " \
                            "LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, " \
                            "EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, " \
                            "BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE " \
                            "GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR " \
                            "BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY " \
                            "THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT " \
                            "LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR " \
                            "OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS " \
                            "SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH " \
                            "DAMAGE."],
                    'name': "BSD License"},
             }
# pylint: enable=line-too-long

class EulaText():
    """!
    EULA text helper class
    """
    def __init__(self, eula_type:str|None = None, custom_eula:list|None = None):
        """!
        @brief Constuctor

        @param eula_type (string): MIT_open, MIT_no_atrtrib, MIT_X11,
                                    GNU_V11, apache_v2_0, BSD_3clause
                                    or BSD_2clause
        @param custom_eula (list of strings): custom EULA string list
        """
        ## List of End User Licence Agreement (EULA) text strings
        self.raw_eula_text = []
        ## End User Licence Agreement (EULA) name
        self.eula_name = ""

        if eula_type is None:
            if custom_eula is not None:
                self.raw_eula_text = custom_eula
                self.eula_name = ""
            else:
                raise TypeError("ERROR: Standard or custom EULA is required.")
        else:
            self.raw_eula_text = self.get_eula_text(eula_type)
            self.eula_name = self.get_eula_name(eula_type)

    @staticmethod
    def get_eula_text(eula_type:str)->list|None:
        """!
        @brief Get the eula string list for the input EULA type.

        @param eula_type (string): MIT_open, MIT_no_atrtrib, MIT_X11,
                                    GNU_V11, apache_v2_0, BSD_3clause
                                    or BSD_2clause
        @return list or None: list of strings for the requested EULA or
                                None if the input eula_type is unknown.
        """
        ret_text = None
        if eula_type in eula:
            ret_text = eula[eula_type]['text']
        return ret_text

    @staticmethod
    def get_eula_name(eula_type:str)->str|None:
        """!
        @brief Get the eula string list for the input EULA type.

        @param eula_type (string): MIT_open, MIT_no_atrtrib, MIT_X11,
                                    GNU_V11, apache_v2_0, BSD_3clause
                                    or BSD_2clause

        @return string or None: Name strings for the requested EULA or
                                None if the input eula_type is unknown.
        """
        ret_name = None
        if eula_type in eula:
            ret_name = eula[eula_type]['name']
        return ret_name

    @staticmethod
    def _output_line(line_text:str, max_length:int = 80, pad:bool = False)->str:
        """!
        @brief Format the raw EULA text to the appropriate line length

        @param line_text (string) - EULA line text
        @param max_length (integer) - Maximum line length for the EULA text, default = 80
        @param pad (boolean) - False: no padding to max_length,
                            True: pad line with spaces out to max_length

        @return Formated line of text
        """
        if pad:
            ret_text = line_text.ljust(max_length, ' ')
        else:
            ret_text = line_text
        return ret_text

    @staticmethod
    def _output_multi_line(raw_text:str, max_length:int = 80, pad:bool = False)->list:
        """!
        @brief Break the long EULA text string into a list of strings that do not
               exceed the max_length input parameter

        @param raw_text (string) - Long EULA line text
        @param max_length (integer) - Maximum line length for the EULA text, default = 80
        @param pad (boolean) - False: no padding to max_length,
                               True: pad line with spaces out to max_length

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
                if pad:
                    formatted_text.append(new_line.ljust(max_length, ' '))
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
            if pad:
                formatted_text.append(new_line.ljust(max_length, ' '))
            else:
                formatted_text.append(new_line)

        return formatted_text

    def format_eula_name(self, max_length:int = 80, pad:bool = False)->str:
        """!
        @brief Format the raw EULA name to the appropriate line length

        @param max_length (integer) - Maximum line length for the EULA text, default = 80
        @param pad (boolean) - False: no padding to max_length,
                            True: pad line with spaces out to max_length

        @return string - formatted name text
        """
        if pad:
            ret_text = self.eula_name.ljust(max_length, ' ')
        else:
            ret_text = self.eula_name
        return ret_text


    def format_eula_text(self, max_length:int = 80, pad:bool = False)->list:
        """!
        @brief Format the raw EULA text to the appropriate line length

        @param max_length (integer) - Maximum line length for the EULA text, default = 80
        @param pad (boolean) - False: no padding to max_length,
                            True: pad line with spaces out to max_length

        @return list of formated eula strings or None if there was a failure
        """
        # Read each line and format it
        formated_eula_text = []
        for raw_text in self.raw_eula_text:
            if len(raw_text) <= max_length:
                # Single line processing
                formated_eula_text.append(self._output_line(raw_text, max_length, pad))
            else:
                # Multi line processing
                formated_eula_text.extend(self._output_multi_line(raw_text, max_length, pad))

            # Append empty line between the EULA text blocks
            formated_eula_text.append(self._output_line("", max_length, pad))

        return formated_eula_text
