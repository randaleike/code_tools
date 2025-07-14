"""@package langstringautogen
Utilities to get the creation and last modification years of a file
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

__version__ = '0.8.3'

__all__ = ["commit_check", "text_format", "copyright_generator", "eula",
           "comment_gen_tools", "doxygen_gen_tools", "param_return_tools",
           "json_language_list", "json_string_class_description",
           "insert_new_copyright_block"]

from . import commit_check
from . import text_format

from . import copyright_generator
from . import eula

from . import comment_gen_tools
from . import doxygen_gen_tools

from . import param_return_tools

from . import json_language_list
from . import json_string_class_description
from . import insert_new_copyright_block
