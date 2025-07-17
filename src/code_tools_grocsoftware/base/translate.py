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

class Translator:
    """!
    String object class definitions
    """
    trans_client = None  # open it only if and when we need it

    def translate_text(self, source_lang:str, target_lang:str, text:str)->str:
        """!
        @brief Translate the input text
        @param source_lang {string} ISO 639-1 language code of the input text
        @param target_lang {string} ISO 639-1 language code for the output text
        @param text {string} text to translate
        @return string - Translated text
        """
        from google.cloud import translate_v2   # pylint: disable=import-outside-toplevel
        if self.trans_client is None:
            self.trans_client = translate_v2.Client()

        if isinstance(text, bytes):
            text = text.decode("utf-8")

        transtext = self.trans_client.translate(text,
                                                target_language=target_lang,
                                                format_='text',
                                                source_language=source_lang,
                                                model='nmt')
        raw_translated_text = transtext['translatedText']
        return raw_translated_text
