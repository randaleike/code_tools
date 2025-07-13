"""@package langstringautogen
@brief Comment block find and generate tools
Scan source files to find comment block(s). Utility to generate new comment blocks
"""

#==========================================================================
# Copyright (c) 2024-2025 Randal Eike
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

class CommentGenerator:
    """!
    @brief Comment block generation helper class
    """
    def __init__(self, comment_markers:dict, line_length:int = None,
                 eoltext:str = None, use_single_line:bool = False):
        """!
        @brief Constructor

        @param comment_markers (CommentBlockDelim dictionary) - Comment deliminter markers for the
                                                                input file type.
        @param line_length (integer): Total length of the padded line including comment
                                     start and end of line text.  None if it's just the
                                     comment start
        @param eoltext (string): String to end the padded line with or None if no end
                                 of line is required.
        @param use_single_line (boolean): True use single line comment text even if comment
                                          blocking is available. False (default) use comment
                                          blocking if available
        """
        ## Comment block markers typical for the file type
        self.comment_data = comment_markers
        ## Maximum line length when generating comment line
        self.line_length = line_length
        ## End of line text to be appended to each comment line in a comment block
        self.eoltext = eoltext
        ## Length of the end of line text.  This length will shorten the max line length by the
        ## length amount
        self.eol_length = 0
        ## Force use of single line comment text even if block comment markers are available
        self.use_single_line = False

        if use_single_line or (comment_markers['blockStart'] is None):
            self.use_single_line = True

        if eoltext is not None:
            self.eol_length = len(eoltext)

    def _append_eoltext(self, new_line:str)->str:
        """!
        @brief Append end of line text if needed

        @param new_line (string): Comment line to add eol_text to

        @return string - Comment line with EOL text if needed
        """
        # Check for eoltext
        if self.eoltext is not None:
            new_line += self.eoltext

        return new_line

    def _pad_comment_line(self, new_line:str, fillchar:str, eol_length:int = 0)->str:
        """!
        @brief Pad comment line with fill character

        @param new_line (string): Comment line to pad
        @param fillchar (character): Character to pad the line with if line_length is
                                     not None
        @param eol_length (integer): Length og the eol text to allow for.

        @return string - Padded comment line
        """
        if self.line_length is not None:
            if self.line_length > (len(new_line) + eol_length):
                pad_len = self.line_length - eol_length
                if (eol_length > 0) or (fillchar != ' '):
                    new_line = new_line.ljust(pad_len, fillchar)
        return new_line

    def _pad_and_append_eol_comment_line(self, new_line:str, fillchar:str, eol_length:int = 0)->str:
        """!
        @brief Pad comment line with fill character and append EOL text if needed

        @param new_line (string): Comment line to pad
        @param fillchar (character): Character to pad the line with if line_length is
                                     not None
        @param eol_length (integer): Length og the eol text to allow for.

        @return string - Padded and EOL appended comment line
        """
        new_line = self._pad_comment_line(new_line, fillchar, eol_length)
        new_line = self._append_eoltext(new_line)
        return new_line

    def build_comment_block_header(self, lines:int = 1, fillchar:str = '-')->list:
        """!
        @brief Build a comment block header string list

        @param lines (integer): Number of header lines to build
        @param fillchar (character): Character to pad the line with if line_length is
                                     not None

        @return list of string(s) - Comment header as specified
        """

        # Initial setup
        header_text = []
        block_started = False

        # Start adding lines
        while lines > 0:
            if (self.comment_data['blockStart'] is None) or self.use_single_line:
                new_line = self.comment_data['singleLine']
            else:
                if block_started:
                    new_line = self.comment_data['blockLineStart']
                else:
                    new_line = self.comment_data['blockStart']
                    block_started = True

            # Check if we need to pad and append EOL text
            new_line = self._pad_and_append_eol_comment_line(new_line, fillchar, self.eol_length)

            # Add the new line to the list
            header_text.append(new_line)
            lines -= 1

        return header_text

    def build_comment_block_footer(self, lines:int = 1, fillchar:str = '-')->list:
        """!
        @brief Build a comment block footer string list

        @param lines (integer): Number of header lines to build
        @param fillchar (character): Character to pad the line with if line_length is
                                     not None
        @return list of string(s) - Comment header as specified
        """

        # Initial setup
        footer_text = []

        if (self.comment_data['blockEnd'] is None) or self.use_single_line:
            end_line = 0
            line_start = self.comment_data['singleLine']
        else:
            end_line = 1
            line_start = self.comment_data['blockLineStart']

        # Start adding fill lines
        while lines > end_line:
            new_line = line_start

            # Check if we need to pad and append EOL text
            new_line = self._pad_and_append_eol_comment_line(new_line, fillchar, self.eol_length)

            # Add the text to the list
            footer_text.append(new_line)
            lines -= 1

        # Add the last line if using blocking
        if lines > 0:
            new_line = self.comment_data['blockLineStart']
            eol_length = len(self.comment_data['blockEnd'])

            # Check if we need to pad
            new_line = self._pad_comment_line(new_line, fillchar, eol_length)
            new_line += self.comment_data['blockEnd']

            # Add the text to the list
            footer_text.append(new_line)

        return footer_text

    def wrap_comment_line(self, text:str, fillchar:str = ' ')->str:
        """!
        @brief Wrap and pad the input text line with the specified comment parameters

        @param text (string): Comment text line to wrap
        @param fillchar (character): Character to pad the line with if line_length is
                                     not None

        @return string - Comment line padded and wrapped in comment blocking text
        """

        # Determine the start data
        if self.use_single_line:
            new_line = self.comment_data['singleLine']+" "
        else:
            new_line = self.comment_data['blockLineStart']

        # Add the user text
        new_line += text

        # Check if we need to pad and append EOL text
        new_line = self._pad_and_append_eol_comment_line(new_line, fillchar, self.eol_length)

        return new_line

    def generate_single_line_comment(self, text:str)->str:
        """!
        @brief Convert input text into a single line comment string
        """
        return self.comment_data['singleLine']+" "+text


class CCommentGenerator(CommentGenerator):
    """!
    C,Cxx,H,Hxx comment generator
    """
    def __init__(self, line_length:int = None, eoltext:str = None, use_single_line:bool = False):
        """!
        @brief Constructor

        @param line_length (integer): Total length of the padded line including comment
                                     start and end of line text.  None if it's just the
                                     comment start
        @param eoltext (string): String to end the padded line with or None if no end
                                 of line is required.
        @param use_single_line (boolean): True use single line comment text even if comment
                                          blocking is available. False (default) use comment
                                          blocking if available
        """
        header_gen_comment_param = {'blockStart': "/*",
                                    'blockEnd': "*/",
                                    'blockLineStart': "* ",
                                    'singleLine': "//"}
        super().__init__(header_gen_comment_param, line_length, eoltext, use_single_line)

class PyCommentGenerator(CommentGenerator):
    """!
    Python comment generator
    """
    def __init__(self, line_length:int = None, eoltext:str = None, use_single_line:bool = False):
        """!
        @brief Constructor

        @param line_length (integer): Total length of the padded line including comment
                                     start and end of line text.  None if it's just the
                                     comment start
        @param eoltext (string): String to end the padded line with or None if no end
                                 of line is required.
        @param use_single_line (boolean): True use single line comment text even if comment
                                          blocking is available. False (default) use comment
                                          blocking if available
        """
        header_gen_comment_param = {'blockStart': '"""',
                                    'blockEnd': '"""',
                                    'blockLineStart': "",
                                    'singleLine': "#"}
        super().__init__(header_gen_comment_param, line_length, eoltext, use_single_line)

class TsCommentGenerator(CommentGenerator):
    """!
    Typescript comment generator
    """
    def __init__(self, line_length:int = None, eoltext:str = None, use_single_line:bool = False):
        """!
        @brief Constructor

        @param line_length (integer): Total length of the padded line including comment
                                     start and end of line text.  None if it's just the
                                     comment start
        @param eoltext (string): String to end the padded line with or None if no end
                                 of line is required.
        @param use_single_line (boolean): True use single line comment text even if comment
                                          blocking is available. False (default) use comment
                                          blocking if available
        """
        header_gen_comment_param = {'blockStart': "/*",
                                    'blockEnd': "*/", \
                                    'blockLineStart': "* ",
                                    'singleLine': "//"}
        super().__init__(header_gen_comment_param, line_length, eoltext, use_single_line)

class JsCommentGenerator(CommentGenerator):
    """!
    Javascript comment generator
    """
    def __init__(self, line_length:int = None, eoltext:str = None, use_single_line:bool = False):
        """!
        @brief Constructor

        @param line_length (integer): Total length of the padded line including comment
                                     start and end of line text.  None if it's just the
                                     comment start
        @param eoltext (string): String to end the padded line with or None if no end
                                 of line is required.
        @param use_single_line (boolean): True use single line comment text even if comment
                                          blocking is available. False (default) use comment
                                          blocking if available
        """
        header_gen_comment_param = {'blockStart': "/*",
                                    'blockEnd': "*/",
                                    'blockLineStart': "* ",
                                    'singleLine': "//"}
        super().__init__(header_gen_comment_param, line_length, eoltext, use_single_line)

class BashCommentGenerator(CommentGenerator):
    """!
    Bash comment generator
    """
    def __init__(self, line_length:int = None, eoltext:str = None, use_single_line:bool = True):
        """!
        @brief Constructor

        @param line_length (integer): Total length of the padded line including comment
                                     start and end of line text.  None if it's just the
                                     comment start
        @param eoltext (string): String to end the padded line with or None if no end
                                 of line is required.
        @param use_single_line (boolean): True use single line comment text even if comment
                                          blocking is available. False (default) use comment
                                          blocking if available
        """
        header_gen_comment_param = {'blockStart': None,
                                    'blockEnd': None,
                                    'blockLineStart': "#",
                                    'singleLine': "#"}
        super().__init__(header_gen_comment_param, line_length, eoltext, use_single_line)

class BatchCommentGenerator(CommentGenerator):
    """!
    Bash comment generator
    """
    def __init__(self, line_length:int = None, eoltext:str = None, use_single_line:bool = True):
        """!
        @brief Constructor

        @param line_length (integer): Total length of the padded line including comment
                                     start and end of line text.  None if it's just the
                                     comment start
        @param eoltext (string): String to end the padded line with or None if no end
                                 of line is required.
        @param use_single_line (boolean): True use single line comment text even if comment
                                          blocking is available. False (default) use comment
                                          blocking if available
        """
        header_gen_comment_param = {'blockStart': None,
                                    'blockEnd': None,
                                    'blockLineStart': "REM ",
                                    'singleLine': "REM ",}
        super().__init__(header_gen_comment_param, line_length, eoltext, use_single_line)
