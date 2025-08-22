"""@package langstringautogen_example
Project example code
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

from code_tools_grocsoftware.base.json_string_class_description import StringClassDescription

def add_extra_mock_code(json_str:StringClassDescription):
    """!
    @brief Add extra mock base class select code
    """
    extra_mock = ["#if defined(CONSTRUCTOR_GET_HELP_STRING)\n"]
    extra_mock.append("    //Parent object constructor will call getHelpString, so setup the expected call\n")
    extra_mock.append("    //before returning the pointer\n")
    extra_mock.append("    stringMockptr stringMock = reinterpret_cast<stringMockptr> (retPtr.get());   // NOLINT\n")
    extra_mock.append("    EXPECT_CALL(*stringMock, getHelpString()).WillOnce(Return(\"mock getHelpString\"));\n")
    extra_mock.append("    #endif //defined(CONSTRUCTOR_GET_HELP_STRING)\n")
    json_str.set_extra_mock(extra_mock)
