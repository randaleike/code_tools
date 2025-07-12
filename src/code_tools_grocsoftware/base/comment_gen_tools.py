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
    def __init__(self, commentMarkers:dict, lineLength:int|None = None, eoltext:str|None = None, useSingleLine:bool = False):
        """!
        @brief Constructor

        @param commentMarkers (CommentBlockDelim dictionary) - Comment deliminter markers for the input file type.
        @param lineLength (integer): Total length of the padded line including comment
                                     start and end of line text.  None if it's just the
                                     comment start
        @param eoltext (string): String to end the padded line with or None if no end
                                 of line is required.
        @param useSingleLine (boolean): True use single line comment text even if comment blocking
                                        is available. False (default) use comment blocking if available
        """
        ## Comment block markers typical for the file type
        self.commentData = commentMarkers
        ## Maximum line length when generating comment line
        self.lineLength = lineLength
        ## End of line text to be appended to each comment line in a comment block
        self.eoltext = eoltext
        ## Length of the end of line text.  This length will shorten the max line length by the length amount
        self.eolLength = 0
        ## Force use of single line comment text even if block comment markers are available
        self.useSingleLine = False

        if useSingleLine or (commentMarkers['blockStart'] is None):
            self.useSingleLine = True

        if eoltext is not None:
            self.eolLength = len(eoltext)

    def _appendEoltext(self, newLine:str)->str:
        """!
        @brief Append end of line text if needed

        @param newLine (string): Comment line to add eolText to

        @return string - Comment line with EOL text if needed
        """
        # Check for eoltext
        if self.eoltext is not None:
            newLine += self.eoltext

        return newLine

    def _padCommentLine(self, newLine:str, fillchar:str, eolLength:int = 0)->str:
        """!
        @brief Pad comment line with fill character

        @param newLine (string): Comment line to pad
        @param fillchar (character): Character to pad the line with if lineLength is
                                     not None
        @param eolLength (integer): Length og the eol text to allow for.

        @return string - Padded comment line
        """
        if self.lineLength is not None:
            if self.lineLength > (len(newLine) + eolLength):
                padLen = self.lineLength - eolLength
                if (eolLength > 0) or (fillchar != ' '):
                    newLine = newLine.ljust(padLen, fillchar)
        return newLine

    def _padAndAppendEolCommentLine(self, newLine:str, fillchar:str, eolLength:int = 0)->str:
        """!
        @brief Pad comment line with fill character and append EOL text if needed

        @param newLine (string): Comment line to pad
        @param fillchar (character): Character to pad the line with if lineLength is
                                     not None
        @param eolLength (integer): Length og the eol text to allow for.

        @return string - Padded and EOL appended comment line
        """
        newLine = self._padCommentLine(newLine, fillchar, eolLength)
        newLine = self._appendEoltext(newLine)
        return newLine

    def buildCommentBlockHeader(self, lines:int = 1, fillchar:str = '-')->list:
        """!
        @brief Build a comment block header string list

        @param lines (integer): Number of header lines to build
        @param fillchar (character): Character to pad the line with if lineLength is
                                     not None

        @return list of string(s) - Comment header as specified
        """

        # Initial setup
        headerText = []
        blockStarted = False

        # Start adding lines
        while lines > 0:
            if (self.commentData['blockStart'] is None) or self.useSingleLine:
                newLine = self.commentData['singleLine']
            else:
                if blockStarted:
                    newLine = self.commentData['blockLineStart']
                else:
                    newLine = self.commentData['blockStart']
                    blockStarted = True

            # Check if we need to pad and append EOL text
            newLine = self._padAndAppendEolCommentLine(newLine, fillchar, self.eolLength)

            # Add the new line to the list
            headerText.append(newLine)
            lines -= 1

        return headerText

    def buildCommentBlockFooter(self, lines:int = 1, fillchar:str = '-')->list:
        """!
        @brief Build a comment block footer string list

        @param lines (integer): Number of header lines to build
        @param fillchar (character): Character to pad the line with if lineLength is
                                     not None
        @return list of string(s) - Comment header as specified
        """

        # Initial setup
        footerText = []

        if (self.commentData['blockEnd'] is None) or self.useSingleLine:
            endLine = 0
            lineStart = self.commentData['singleLine']
        else:
            endLine = 1
            lineStart = self.commentData['blockLineStart']

        # Start adding fill lines
        while lines > endLine:
            newLine = lineStart

            # Check if we need to pad and append EOL text
            newLine = self._padAndAppendEolCommentLine(newLine, fillchar, self.eolLength)

            # Add the text to the list
            footerText.append(newLine)
            lines -= 1

        # Add the last line if using blocking
        if lines > 0:
            newLine = self.commentData['blockLineStart']
            eolLength = len(self.commentData['blockEnd'])

            # Check if we need to pad
            newLine = self._padCommentLine(newLine, fillchar, eolLength)
            newLine += self.commentData['blockEnd']

            # Add the text to the list
            footerText.append(newLine)

        return footerText

    def wrapCommentLine(self, text:str, fillchar:str = ' ')->str:
        """!
        @brief Wrap and pad the input text line with the specified comment parameters

        @param text (string): Comment text line to wrap
        @param fillchar (character): Character to pad the line with if lineLength is
                                     not None

        @return string - Comment line padded and wrapped in comment blocking text
        """

        # Determine the start data
        if self.useSingleLine:
            newLine = self.commentData['singleLine']+" "
        else:
            newLine = self.commentData['blockLineStart']

        # Add the user text
        newLine += text

        # Check if we need to pad and append EOL text
        newLine = self._padAndAppendEolCommentLine(newLine, fillchar, self.eolLength)

        return newLine

    def generateSingleLineComment(self, text:str)->str:
        """!
        @brief Convert input text into a single line comment string
        """
        return self.commentData['singleLine']+" "+text


class CCommentGenerator(CommentGenerator):
    """!
    C,Cxx,H,Hxx comment generator
    """
    def __init__(self, lineLength:int|None = None, eoltext:str|None = None, useSingleLine:bool = False):
        """!
        @brief Constructor

        @param lineLength (integer): Total length of the padded line including comment
                                     start and end of line text.  None if it's just the
                                     comment start
        @param eoltext (string): String to end the padded line with or None if no end
                                 of line is required.
        @param useSingleLine (boolean): True use single line comment text even if comment blocking
                                        is available. False (default) use comment blocking if available
        """
        headerGenCommentParam = {'blockStart': "/*", 'blockEnd': "*/", 'blockLineStart': "* ", 'singleLine': "//"}
        super().__init__(headerGenCommentParam, lineLength, eoltext, useSingleLine)

class PyCommentGenerator(CommentGenerator):
    """!
    Python comment generator
    """
    def __init__(self, lineLength:int|None = None, eoltext:str|None = None, useSingleLine:bool = False):
        """!
        @brief Constructor

        @param lineLength (integer): Total length of the padded line including comment
                                     start and end of line text.  None if it's just the
                                     comment start
        @param eoltext (string): String to end the padded line with or None if no end
                                 of line is required.
        @param useSingleLine (boolean): True use single line comment text even if comment blocking
                                        is available. False (default) use comment blocking if available
        """
        headerGenCommentParam = {'blockStart': '"""', 'blockEnd': '"""', 'blockLineStart': "", 'singleLine': "#"}
        super().__init__(headerGenCommentParam, lineLength, eoltext, useSingleLine)

class TsCommentGenerator(CommentGenerator):
    """!
    Typescript comment generator
    """
    def __init__(self, lineLength:int|None = None, eoltext:str|None = None, useSingleLine:bool = False):
        """!
        @brief Constructor

        @param lineLength (integer): Total length of the padded line including comment
                                     start and end of line text.  None if it's just the
                                     comment start
        @param eoltext (string): String to end the padded line with or None if no end
                                 of line is required.
        @param useSingleLine (boolean): True use single line comment text even if comment blocking
                                        is available. False (default) use comment blocking if available
        """
        headerGenCommentParam = {'blockStart': "/*", 'blockEnd': "*/", 'blockLineStart': "* ", 'singleLine': "//"}
        super().__init__(headerGenCommentParam, lineLength, eoltext, useSingleLine)

class JsCommentGenerator(CommentGenerator):
    """!
    Javascript comment generator
    """
    def __init__(self, lineLength:int|None = None, eoltext:str|None = None, useSingleLine:bool = False):
        """!
        @brief Constructor

        @param lineLength (integer): Total length of the padded line including comment
                                     start and end of line text.  None if it's just the
                                     comment start
        @param eoltext (string): String to end the padded line with or None if no end
                                 of line is required.
        @param useSingleLine (boolean): True use single line comment text even if comment blocking
                                        is available. False (default) use comment blocking if available
        """
        headerGenCommentParam = {'blockStart': "/*", 'blockEnd': "*/", 'blockLineStart': "* ", 'singleLine': "//"}
        super().__init__(headerGenCommentParam, lineLength, eoltext, useSingleLine)

class BashCommentGenerator(CommentGenerator):
    """!
    Bash comment generator
    """
    def __init__(self, lineLength:int|None = None, eoltext:str|None = None, useSingleLine:bool = True):
        """!
        @brief Constructor

        @param lineLength (integer): Total length of the padded line including comment
                                     start and end of line text.  None if it's just the
                                     comment start
        @param eoltext (string): String to end the padded line with or None if no end
                                 of line is required.
        @param useSingleLine (boolean): True use single line comment text even if comment blocking
                                        is available. False (default) use comment blocking if available
        """
        headerGenCommentParam = {'blockStart': None, 'blockEnd': None, 'blockLineStart': "#", 'singleLine': "#"}
        super().__init__(headerGenCommentParam, lineLength, eoltext, useSingleLine)

class BatchCommentGenerator(CommentGenerator):
    """!
    Bash comment generator
    """
    def __init__(self, lineLength:int|None = None, eoltext:str|None = None, useSingleLine:bool = True):
        """!
        @brief Constructor

        @param lineLength (integer): Total length of the padded line including comment
                                     start and end of line text.  None if it's just the
                                     comment start
        @param eoltext (string): String to end the padded line with or None if no end
                                 of line is required.
        @param useSingleLine (boolean): True use single line comment text even if comment blocking
                                        is available. False (default) use comment blocking if available
        """
        headerGenCommentParam = {'blockStart': None, 'blockEnd': None, 'blockLineStart': "REM ", 'singleLine': "REM ",}
        super().__init__(headerGenCommentParam, lineLength, eoltext, useSingleLine)
