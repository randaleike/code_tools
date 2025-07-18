"""@package test_programmer_tools
Unittest for programmer base tools utility
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

import pytest
from code_tools_grocsoftware.base.param_return_tools import ParamRetDict
from code_tools_grocsoftware.base.doxygen_gen_tools import DoxyCommentGenerator

from code_tools_grocsoftware.base.doxygen_gen_tools import CDoxyCommentGenerator
from code_tools_grocsoftware.base.doxygen_gen_tools import PyDoxyCommentGenerator
from code_tools_grocsoftware.base.doxygen_gen_tools import TsDoxyCommentGenerator
from code_tools_grocsoftware.base.doxygen_gen_tools import JsDoxyCommentGenerator

# pylint: disable=protected-access
# pylint: disable=attribute-defined-outside-init

class UnittestDoxygenCommentBlock:
    """!
    Doxygen comment block test cases
    """
    def set_up_params(self, block_start:str, block_end:str,
                      block_line:str, single_line:str, add_param:bool):
        """!
        @brief Common test set_up routine

        @param block_start {string} Doxygen comment block start for the programming language
        @param block_end {string} Doxygen comment block end for the programming language
        @param block_line {string} Doxygen comment block line prefix for the programming language
        @param single_line {string} Doxygen comment single line start for the programming language
        @param add_param {boolean} True, add parameter type to documentation comment,
                                   False, do not add type to comment
        """
        self.block_start = block_start
        self.block_end = block_end
        self.block_line = block_line
        self.single_line = single_line
        self.add_param = add_param

        self.tst_gen = DoxyCommentGenerator(block_start,
                                            block_end,
                                            block_line,
                                            single_line,
                                            add_param)
        if block_start is not None:
            self.desc_format_adjust = len(block_start)
            self.expected_block_start = block_start
            if block_end == '"""':
                self.expected_block_end = block_end
            else:
                self.expected_block_end = " "+block_end
            self.expected_block_prefix = " "+block_line+" "
        elif single_line is not None:
            self.desc_format_adjust = len(single_line)
            self.expected_block_start = single_line
            self.expected_block_end = ""
            self.expected_block_prefix = single_line+" "

    def test01_doxy_gen_constructor(self):
        """!
        @brief Test the constructor
        """
        assert self.tst_gen.block_start == self.block_start
        assert self.tst_gen.block_end == self.block_end
        assert self.tst_gen.block_line_start == self.block_line
        assert self.tst_gen.single_line_start == self.single_line

        assert self.tst_gen.format_max_length == 120
        assert self.tst_gen.desc_format_max == 120-self.desc_format_adjust

        assert self.tst_gen.add_param_type == self.add_param
        assert self.tst_gen.group_counter == 0

    def test02_gen_block_prefix(self):
        """!
        @brief Test the block line prefix generation
        """
        tst_str = self.tst_gen._gen_comment_block_prefix()
        assert tst_str == self.expected_block_prefix

    def test03_gen_block_start(self):
        """!
        @brief Test the block start generation
        """
        tst_str = self.tst_gen._gen_block_start()
        assert tst_str == self.expected_block_start

    def test04_gen_block_end(self):
        """!
        @brief Test the block end generation
        """
        tst_str = self.tst_gen._gen_block_end()
        assert tst_str == self.expected_block_end

    def test05_gen_brief_desc_short(self):
        """!
        @brief Test the brief description block with short description
        """
        prefix = "  "+self.expected_block_prefix
        self.tst_gen.desc_format_max = 80
        tst_str_lst = self.tst_gen._gen_brief_desc("Brief description short", prefix)
        assert len(tst_str_lst) == 1
        assert tst_str_lst[0] == prefix+"@brief Brief description short\n"

    def test06_gen_brief_desc_long(self):
        """!
        @brief Test the brief description block with long description
        """
        prefix = "  "+self.expected_block_prefix
        self.tst_gen.desc_format_max = 79+len(prefix)
        tst_str_lst = self.tst_gen._gen_brief_desc("Brief description long. Long meandering " \
                                                    "description to make sure that the text " \
                                                    "wraps at least one line.  Just to make sure.",
                                                   prefix)
        assert len(tst_str_lst) == 2
        assert tst_str_lst[0] == prefix+"@brief Brief description long. Long meandering " \
                                        "description to make sure that the\n"
        assert tst_str_lst[1] == prefix+"       text wraps at least one line.  Just to make sure.\n"

    def test07_gen_long_desc_short(self):
        """!
        @brief Test the long description block with short description
        """
        prefix = "  "+self.expected_block_prefix
        self.tst_gen.desc_format_max = 80+len(prefix)
        tst_str_lst = self.tst_gen._gen_long_desc(prefix, "Short description line")
        assert len(tst_str_lst) == 1
        assert tst_str_lst[0] == prefix+"Short description line\n"

    def test08_gen_long_desc_short_long(self):
        """!
        @brief Test the long description block with long description
        """
        prefix = "  "+self.expected_block_prefix
        self.tst_gen.desc_format_max = 80+len(prefix)
        tst_str_lst = self.tst_gen._gen_long_desc(prefix,
                                                  "Long description line. Long meandering " \
                                                    "description to make sure that the text " \
                                                    "wraps at least one line.  Just to make sure.")
        assert len(tst_str_lst) == 2
        assert tst_str_lst[0] == prefix+"Long description line. Long meandering description to " \
                                        "make sure that the text wraps\n"
        assert tst_str_lst[1] == prefix+"at least one line.  Just to make sure.\n"

    def test09_gen_ret_doc_short_desc(self):
        """!
        @brief Test the generate return documentation with short description
        """
        prefix = "  "+self.expected_block_prefix
        self.tst_gen.desc_format_max = 80+len(prefix)
        ret_dict = ParamRetDict.build_return_dict("string", "Short desciption")
        tst_str_lst = self.tst_gen._gen_comment_return_text(ret_dict, prefix)
        assert len(tst_str_lst) == 1
        expected_str  = prefix
        expected_str += "@return "
        expected_str += ParamRetDict.get_return_type(ret_dict)
        expected_str += " - "
        expected_str += ParamRetDict.get_return_desc(ret_dict)
        expected_str += "\n"
        assert tst_str_lst[0] == expected_str

    def test10_gen_ret_doc_long_desc(self):
        """!
        @brief Test the generate return documentation with long description
        """
        prefix = "  "+self.expected_block_prefix
        self.tst_gen.desc_format_max = 78+len(prefix)
        ret_dict = ParamRetDict.build_return_dict("string",
                                                  "Long meandering desciption of the return " \
                                                   "data designed to make sure that the line " \
                                                   "wraps")
        tst_str_lst = self.tst_gen._gen_comment_return_text(ret_dict, prefix)
        assert len(tst_str_lst) == 2

        expected_str  = prefix
        expected_str += "@return "
        expected_str += ParamRetDict.get_return_type(ret_dict)
        expected_str += " - Long meandering desciption of the return data designed to make\n"
        assert tst_str_lst[0] == expected_str

        expected_str1  = prefix
        expected_str1 += "                 sure that the line wraps\n"
        assert tst_str_lst[1] == expected_str1

    def test11_gen_param_doc_short_desc(self):
        """!
        @brief Test the generate parameter documentation with short description
        """
        prefix = "  "+self.expected_block_prefix
        self.tst_gen.desc_format_max = 80+len(prefix)
        param_dict = ParamRetDict.build_param_dict_with_mod("foo", "string", "Short desciption", 0)
        tst_str_lst = self.tst_gen._gen_comment_param_text(param_dict, prefix)

        expected_str  = prefix
        expected_str += "@param "
        expected_str += ParamRetDict.get_param_name(param_dict)
        expected_str += " "

        if self.add_param:
            expected_str += "{"
            expected_str += ParamRetDict.get_param_type(param_dict)
            expected_str += "} "

        expected_str += ParamRetDict.get_param_desc(param_dict)
        expected_str += "\n"

        assert len(tst_str_lst) == 1
        assert tst_str_lst[0] == expected_str

    def test12_gen_param_doc_long_desc(self):
        """!
        @brief Test the generate parameter documentation with long description
        """
        prefix = "  "+self.expected_block_prefix
        self.tst_gen.desc_format_max = 76+len(prefix)
        param_dict = ParamRetDict.build_param_dict_with_mod("moo",
                                                            "string",
                                                            "Long meandering desciption of " \
                                                             "the return data designed to make " \
                                                             "sure that the line wraps")

        tst_str_lst = self.tst_gen._gen_comment_param_text(param_dict, prefix)

        expected_str  = prefix
        expected_str += "@param "
        expected_str += ParamRetDict.get_param_name(param_dict)
        expected_str += " "

        if self.add_param:
            expected_str += "{"
            expected_str += ParamRetDict.get_param_type(param_dict)
            expected_str += "} Long meandering desciption of the return data designed to\n"
        else:
            expected_str += "Long meandering desciption of the return data designed to make sure\n"


        expected_str1  = prefix
        if self.add_param:
            expected_str1 += "                    make sure that the line wraps\n"
        else:
            expected_str1 += "           that the line wraps\n"

        assert len(tst_str_lst) == 2
        assert tst_str_lst[0] == expected_str
        assert tst_str_lst[1] == expected_str1

    def test13_gen_method_doc_brief_only(self):
        """!
        @brief Test the generate method documentation
        """
        prefix = "".rjust(4, ' ')
        blockprefix = prefix+self.expected_block_prefix
        ret_dict = ParamRetDict.build_return_dict("string", "Short return desciption")
        param_dict_list = [ParamRetDict.build_param_dict_with_mod("moo",
                                                                  "string",
                                                                  "Short str param desciption"),
                           ParamRetDict.build_param_dict_with_mod("foo",
                                                                  "int",
                                                                  "Short int param desciption")]

        tst_str_lst = self.tst_gen.gen_doxy_method_comment("Brief method description",
                                                           param_dict_list,
                                                           ret_dict, block_indent=4)

        assert len(tst_str_lst) == 8
        assert tst_str_lst[0] == prefix+self.expected_block_start+"\n"
        assert tst_str_lst[1] == blockprefix+"@brief Brief method description\n"
        assert tst_str_lst[2] == blockprefix+"\n"

        param_prefix = blockprefix+"@param "
        param1_exp = param_prefix+ParamRetDict.get_param_name(param_dict_list[0])+" "
        if self.add_param:
            param1_exp += "{"
            param1_exp += ParamRetDict.get_param_type(param_dict_list[0])
            param1_exp += "} "

        param1_exp += "Short str param desciption\n"

        param2_exp = param_prefix+ParamRetDict.get_param_name(param_dict_list[1])+" "
        if self.add_param:
            param2_exp += "{"
            param2_exp += ParamRetDict.get_param_type(param_dict_list[1])
            param2_exp += "} "

        param2_exp += "Short int param desciption\n"

        assert tst_str_lst[3] == param1_exp
        assert tst_str_lst[4] == param2_exp
        assert tst_str_lst[5] == blockprefix+"\n"

        return_expected  = blockprefix+"@return "
        return_expected += ParamRetDict.get_return_type(ret_dict)
        return_expected += " - Short return desciption\n"
        assert tst_str_lst[6] == return_expected

        assert tst_str_lst[7] == prefix+self.expected_block_end+"\n"

    def test14_gen_method_doc_brief_and_long(self):
        """!
        @brief Test the generate method documentation, with long description
        """
        prefix = "".rjust(4, ' ')
        blockprefix = prefix+self.expected_block_prefix
        self.tst_gen.desc_format_max = 77+len(blockprefix)
        ret_dict = ParamRetDict.build_return_dict("string", "Short return desciption")
        param_dict_list = [ParamRetDict.build_param_dict_with_mod("moo",
                                                                  "string",
                                                                  "Short str param desciption"),
                           ParamRetDict.build_param_dict_with_mod("foo",
                                                                  "int",
                                                                  "Short int param desciption")]

        long_method_desc = "Long meandering method description. Not sure what there is to " \
                           "say, just going on until I can make sure it will wrap"
        tst_str_lst = self.tst_gen.gen_doxy_method_comment("Brief method description",
                                                           param_dict_list,
                                                           ret_dict,
                                                           long_method_desc,
                                                           4)

        assert len(tst_str_lst) == 11
        assert tst_str_lst[0] == prefix+self.expected_block_start+"\n"
        assert tst_str_lst[1] == blockprefix+"@brief Brief method description\n"
        assert tst_str_lst[2] == blockprefix+"\n"
        assert tst_str_lst[3] == blockprefix+"Long meandering method description. Not " \
                                             "sure what there is to say, just going on\n"
        assert tst_str_lst[4] == blockprefix+"until I can make sure it will wrap\n"
        assert tst_str_lst[5] == blockprefix+"\n"

        param_prefix = blockprefix+"@param "
        param1_exp = param_prefix+ParamRetDict.get_param_name(param_dict_list[0])+" "
        if self.add_param:
            param1_exp += "{"
            param1_exp += ParamRetDict.get_param_type(param_dict_list[0])
            param1_exp += "} "

        param1_exp += "Short str param desciption\n"

        param2_exp = param_prefix+ParamRetDict.get_param_name(param_dict_list[1])+" "
        if self.add_param:
            param2_exp += "{"
            param2_exp += ParamRetDict.get_param_type(param_dict_list[1])
            param2_exp += "} "

        param2_exp += "Short int param desciption\n"

        assert tst_str_lst[6] == param1_exp
        assert tst_str_lst[7] == param2_exp
        assert tst_str_lst[8] == blockprefix+"\n"

        return_expected  = blockprefix+"@return "
        return_expected += ParamRetDict.get_return_type(ret_dict)
        return_expected += " - Short return desciption\n"
        assert tst_str_lst[9] == return_expected

        assert tst_str_lst[10] == prefix+self.expected_block_end+"\n"

    def test15_gen_class_doc_brief_only(self):
        """!
        @brief Test the generate class documentation
        """
        prefix = "".rjust(4, ' ')
        blockprefix = prefix+self.expected_block_prefix
        self.tst_gen.desc_format_max = 78+len(prefix)
        tst_str_lst = self.tst_gen.gen_doxy_class_comment("Brief class description", block_indent=4)

        assert len(tst_str_lst) == 3
        assert tst_str_lst[0] == prefix+self.expected_block_start+"\n"
        assert tst_str_lst[1] == blockprefix+"@brief Brief class description\n"
        assert tst_str_lst[2] == prefix+self.expected_block_end+"\n"

    def test16_gen_class_doc_brief_and_long(self):
        """!
        @brief Test the generate class documentation
        """
        prefix = "".rjust(4, ' ')
        blockprefix = prefix+self.expected_block_prefix
        self.tst_gen.desc_format_max = 78+len(prefix)
        long_class_desc = "Long meandering class description. Not sure what there is to say, " \
                          "just going on until I can make sure it will wrap"
        tst_str_lst = self.tst_gen.gen_doxy_class_comment("Brief class description",
                                                          long_class_desc,
                                                          4)

        assert len(tst_str_lst) == 6
        assert tst_str_lst[0] == prefix+self.expected_block_start+"\n"
        assert tst_str_lst[1] == blockprefix+"@brief Brief class description\n"
        assert tst_str_lst[2] == blockprefix+"\n"
        assert tst_str_lst[3] == blockprefix+"Long meandering class description. Not sure what " \
                                             "there is to say, just going on\n"
        assert tst_str_lst[4] == blockprefix+"until I can make sure it will wrap\n"
        assert tst_str_lst[5] == prefix+self.expected_block_end+"\n"

    def test17_gen_def_group_full(self):
        """!
        @brief Test the generate group definition documentation, full definition
        """
        tst_str_lst = self.tst_gen.gen_doxy_defgroup("test.x", "Fred", "Test Fred group")
        assert len(tst_str_lst) == 6
        assert tst_str_lst[0] == self.expected_block_start+"\n"
        assert tst_str_lst[1] == self.expected_block_prefix+"@file test.x\n"
        assert tst_str_lst[2] == self.expected_block_prefix+"@defgroup Fred Test Fred group\n"
        assert tst_str_lst[3] == self.expected_block_prefix+"@ingroup Fred\n"
        assert tst_str_lst[4] == self.expected_block_prefix+"@{\n"
        assert tst_str_lst[5] == self.expected_block_end+"\n"

    def test18_gen_def_group_only(self):
        """!
        @brief Test the generate group definition documentation, group only
        """
        tst_str_lst = self.tst_gen.gen_doxy_defgroup("test.x", "Fred")
        assert len(tst_str_lst) == 5
        assert tst_str_lst[0] == self.expected_block_start+"\n"
        assert tst_str_lst[1] == self.expected_block_prefix+"@file test.x\n"
        assert tst_str_lst[2] == self.expected_block_prefix+"@ingroup Fred\n"
        assert tst_str_lst[3] == self.expected_block_prefix+"@{\n"
        assert tst_str_lst[4] == self.expected_block_end+"\n"

    def test18_gen_def_end_group_with_no_open(self):
        """!
        @brief Test the generate end group documentation if no group was opened
        """
        assert self.tst_gen.gen_doxy_group_end() is None

    def test19_gen_def_end_group_with_one_open(self):
        """!
        @brief Test the generate end group documentation where one group was opened
        """
        self.tst_gen.gen_doxy_defgroup("test.x", "Fred")
        tst_str = self.tst_gen.gen_doxy_group_end()
        assert tst_str is not None
        assert tst_str == self.expected_block_start+"@}"+self.expected_block_end+"\n"

        # Verify the group counter is 0
        assert self.tst_gen.gen_doxy_group_end() is None

    def test20_gen_def_end_group_with_two_open(self):
        """!
        @brief Test the generate end group documentation where two groups were opened
        """
        self.tst_gen.gen_doxy_defgroup("test.x", "Fred")
        self.tst_gen.gen_doxy_defgroup("test.x", "Barney")
        tst_str = self.tst_gen.gen_doxy_group_end()
        assert tst_str is not None
        assert tst_str == self.expected_block_start+"@}"+self.expected_block_end+"\n"

        tst_str1 = self.tst_gen.gen_doxy_group_end()
        assert tst_str1 is not None
        assert tst_str1 == self.expected_block_start+"@}"+self.expected_block_end+"\n"

        # Verify the group counter is 0
        assert self.tst_gen.gen_doxy_group_end() is None

    def test21_gen_single_line_comment(self):
        """!
        @brief Test the generate single line comment
        """
        assert self.tst_gen.gen_single_line_start() == self.single_line

    def test21_gen_var_doc(self):
        """!
        @brief Test the generate single line comment
        """
        exp_sls = self.single_line+"< Short description"
        exp_slf = self.single_line+"< Foo description"
        assert self.tst_gen.gen_doxy_var_doc_str("Short description") == exp_sls
        assert self.tst_gen.gen_doxy_var_doc_str("Foo description") == exp_slf

    def test22_gen_method_doc_no_return(self):
        """!
        @brief Test the generate method documentation
        """
        prefix = "".rjust(4, ' ')
        blockprefix = prefix+self.expected_block_prefix
        param_dict_list = [ParamRetDict.build_param_dict_with_mod("moo",
                                                                  "string",
                                                                  "Short str param desciption"),
                           ParamRetDict.build_param_dict_with_mod("foo",
                                                                  "int",
                                                                  "Short int param desciption")]

        tst_str_lst = self.tst_gen.gen_doxy_method_comment("Brief method description",
                                                           param_dict_list,
                                                           None,
                                                           block_indent=4)

        assert len(tst_str_lst) == 7
        assert tst_str_lst[0] == prefix+self.expected_block_start+"\n"
        assert tst_str_lst[1] == blockprefix+"@brief Brief method description\n"
        assert tst_str_lst[2] == blockprefix+"\n"

        param_prefix = blockprefix+"@param "
        param1_exp = param_prefix+ParamRetDict.get_param_name(param_dict_list[0])+" "
        if self.add_param:
            param1_exp += "{"
            param1_exp += ParamRetDict.get_param_type(param_dict_list[0])
            param1_exp += "} "

        param1_exp += "Short str param desciption\n"

        param2_exp = param_prefix+ParamRetDict.get_param_name(param_dict_list[1])+" "
        if self.add_param:
            param2_exp += "{"
            param2_exp += ParamRetDict.get_param_type(param_dict_list[1])
            param2_exp += "} "

        param2_exp += "Short int param desciption\n"

        assert tst_str_lst[3] == param1_exp
        assert tst_str_lst[4] == param2_exp
        assert tst_str_lst[5] == blockprefix+"\n"
        assert tst_str_lst[6] == prefix+self.expected_block_end+"\n"

    def test23_gen_method_doc_empty_param_list(self):
        """!
        @brief Test the generate method documentation
        """
        prefix = "".rjust(4, ' ')
        blockprefix = prefix+self.expected_block_prefix
        ret_dict = ParamRetDict.build_return_dict("string", "Short return desciption")
        tst_str_lst = self.tst_gen.gen_doxy_method_comment("Brief method description",
                                                           [],
                                                           ret_dict,
                                                           block_indent=4)

        assert len(tst_str_lst) == 5
        assert tst_str_lst[0] == prefix+self.expected_block_start+"\n"
        assert tst_str_lst[1] == blockprefix+"@brief Brief method description\n"
        assert tst_str_lst[2] == blockprefix+"\n"
        return_expected  = blockprefix+"@return "
        return_expected += ParamRetDict.get_return_type(ret_dict)
        return_expected += " - Short return desciption\n"
        assert tst_str_lst[3] == return_expected

        assert tst_str_lst[4] == prefix+self.expected_block_end+"\n"

    def test24_gen_method_doc_empty_param_list_no_return(self):
        """!
        @brief Test the generate method documentation
        """
        prefix = "".rjust(4, ' ')
        blockprefix = prefix+self.expected_block_prefix
        tst_str_lst = self.tst_gen.gen_doxy_method_comment("Brief method description",
                                                           [],
                                                           None,
                                                           block_indent=4)

        assert len(tst_str_lst) == 4
        assert tst_str_lst[0] == prefix+self.expected_block_start+"\n"
        assert tst_str_lst[1] == blockprefix+"@brief Brief method description\n"
        assert tst_str_lst[2] == blockprefix+"\n"
        assert tst_str_lst[3] == prefix+self.expected_block_end+"\n"

    def test25_gen_long_none(self):
        """!
        @brief Test the long description block with None long description
        """
        prefix = "  "+self.expected_block_prefix
        self.tst_gen.desc_format_max = 80+len(prefix)
        tst_str_lst = self.tst_gen._gen_long_desc(prefix)
        assert len(tst_str_lst) == 0

    def test26_gen_class_doc_brief_none(self):
        """!
        @brief Test the generate class documentation
        """
        prefix = "".rjust(4, ' ')
        blockprefix = prefix+self.expected_block_prefix
        self.tst_gen.desc_format_max = 78+len(prefix)
        tst_str_lst = self.tst_gen.gen_doxy_class_comment(None,
                                                          "Long class description",
                                                          block_indent=4)

        assert len(tst_str_lst) == 3
        assert tst_str_lst[0] == prefix+self.expected_block_start+"\n"
        assert tst_str_lst[1] == blockprefix+"Long class description\n"
        assert tst_str_lst[2] == prefix+self.expected_block_end+"\n"

    def test27_gen_def_group_none(self):
        """!
        @brief Test the generate group definition documentation, None group
        """
        tst_str_lst = self.tst_gen.gen_doxy_defgroup("test.x")
        assert len(tst_str_lst) == 3
        assert tst_str_lst[0] == self.expected_block_start+"\n"
        assert tst_str_lst[1] == self.expected_block_prefix+"@file test.x\n"
        assert tst_str_lst[2] == self.expected_block_end+"\n"

class TestUnittestDoxygenCCommentBlock(UnittestDoxygenCommentBlock):
    """!
    Doxygen comment block test cases
    """
    def setup_method(self):
        """!
        Test setup method
        """
        self.set_up_params('/**', '*/', '*', '//!', False)

class TestUnittestDoxygenPyCommentBlock(UnittestDoxygenCommentBlock):
    """!
    Doxygen comment block test cases
    """
    def setup_method(self):
        """!
        Test setup method
        """
        self.set_up_params('"""!', '"""', '', '##!', True)

class TestUnittestDoxygenJsTsCommentBlock(UnittestDoxygenCommentBlock):
    """!
    Doxygen comment block test cases
    """
    def setup_method(self):
        """!
        Test setup method
        """
        self.set_up_params('/**', '*/', '*', '//!', True)

class TestUnittestDoxygenSinglLineCommentBlock(UnittestDoxygenCommentBlock):
    """!
    Doxygen comment block test cases
    """
    def setup_method(self):
        """!
        Test setup method
        """
        self.set_up_params(None, None, None, '##!', True)

class TestUnittestDoxygenProgCommentBlock:
    """!
    Doxygen comment block test cases
    """
    def test01_c_generator_constructor(self):
        """!
        @brief Test c doxygen comment generator class constructor,
               default
        """
        tst_gen = CDoxyCommentGenerator()
        assert tst_gen.block_start == "/**"
        assert tst_gen.block_end == "*/"
        assert tst_gen.block_line_start == "*"
        assert tst_gen.single_line_start == "//!"
        assert not tst_gen.add_param_type

    def test02_ts_generator_constructor(self):
        """!
        @brief Test typescript doxygen comment generator class constructor,
               default
        """
        tst_gen = TsDoxyCommentGenerator()
        assert tst_gen.block_start == "/**"
        assert tst_gen.block_end == "*/"
        assert tst_gen.block_line_start == "*"
        assert tst_gen.single_line_start == "//!"
        assert tst_gen.add_param_type

    def test03_js_generator_constructor(self):
        """!
        @brief Test java script doxygen comment generator class constructor,
               default
        """
        tst_gen = JsDoxyCommentGenerator()
        assert tst_gen.block_start == "/**"
        assert tst_gen.block_end == "*/"
        assert tst_gen.block_line_start == "*"
        assert tst_gen.single_line_start == "//!"
        assert tst_gen.add_param_type

    def test04_py_generator_constructor(self):
        """!
        @brief Test python doxygen comment generator class constructor,
               default
        """
        tst_gen = PyDoxyCommentGenerator()
        assert tst_gen.block_start == '"""!'
        assert tst_gen.block_end == '"""'
        assert tst_gen.block_line_start == ""
        assert tst_gen.single_line_start == "##"
        assert tst_gen.add_param_type

    def test05_null_generator_constructor(self):
        """!
        @brief Test generic doxygen comment generator class constructor
        """
        tst_gen = DoxyCommentGenerator(None, None, None, None)
        assert tst_gen.block_start is None
        assert tst_gen.block_end is None
        assert tst_gen.block_line_start is None
        assert tst_gen.single_line_start is None
        assert not tst_gen.add_param_type

        exp_err_str = "ERROR: Can't have a doxygen comment if there are no comment markers."

        with pytest.raises(Exception) as context:
            tst_gen._gen_comment_block_prefix()
        assert exp_err_str in str(context.value)

        with pytest.raises(Exception) as context:
            tst_gen._gen_block_start()
        assert exp_err_str in str(context.value)

# pylint: enable=protected-access
# pylint: enable=attribute-defined-outside-init
