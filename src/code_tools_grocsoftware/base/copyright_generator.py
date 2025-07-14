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

class CopyrightGenerator():
    """!
    @brief Copyright message generator

    This class is used to generate new copyright message values based
    on a previously parsed copyright message and new dates or completely
    new copyright messages if a previously parsed message is unavailable.
    """

    @staticmethod
    def is_multi_year(create_year:int, last_modify_year:int)->bool:
        """!
        Determine if this is a multi or single year message

        @param create_year (integer): File creation date
        @param last_modify_year (integer): Last modification date of the file or None

        @return bool - True if last_modify_year is not None and last_modify_year != create_year
        """
        retval = False
        if last_modify_year is not None:
            if last_modify_year != create_year:
                retval = True
        return retval


    def create_new_copyright(self, owner:str, create_year:int,
                             last_modify_year:int = None)->str:
        """!
        @brief Create a new copyright message from scratch

        @param owner (string): Owner for the new message
        @param create_year (integer): File creation date
        @param last_modify_year (integer): Last modification date of the file

        @return string : New owner copyright message
        """
        # Get last modify if not supplied
        if CopyrightGenerator.is_multi_year(create_year, last_modify_year):
            copyright_str = "Copyright (c) "+str(create_year)+"-"+str(last_modify_year)+" "+owner
        else:
            copyright_str = "Copyright (c) "+str(create_year)+" "+owner

        return copyright_str
