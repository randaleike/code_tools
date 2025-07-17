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

from code_tools_grocsoftware.base.param_return_tools import ParamRetDict

def get_expected_extern(param_dict_list:list, intf_ret_ptr_type:str, select_function_name:str)->str:
    """!
    @brief construct the expected external declaration string
    @param param_dict_list {list} List of parameter dictionaries for parameter list declaration
    @param intf_ret_ptr_type {str} Return type for extern declaration
    @param select_function_name {str} Function name for extern declaration
    @return string - external function declaration string
    """
    param_prefix = ""
    param_str = ""
    for param_dict in param_dict_list:
        param_type = ParamRetDict.get_param_type(param_dict)
        param_name = ParamRetDict.get_param_name(param_dict)
        param_str += param_prefix
        param_str += param_type
        param_str += " "
        param_str += param_name
        param_prefix = ", "

    expected_str = "extern "+intf_ret_ptr_type+" "+select_function_name+"("+param_str+");\n"
    return expected_str
