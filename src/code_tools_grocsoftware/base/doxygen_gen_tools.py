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

from code_tools_grocsoftware.base.param_return_tools import ParamRetDict
from code_tools_grocsoftware.base.text_format import MultiLineFormat

#============================================================================
#============================================================================
# Doxygen comment block helper classes
#============================================================================
#============================================================================
class DoxyCommentGenerator():
    """!
    @brief Generic Doxygen comment generator class
    Generic Doxygen comment generator class. Use the constructor input to specify the appropriate comment
    markers for the specific programming language generation.
    """
    def __init__(self, block_start:str, block_end:str, block_line_start:str, single_line_start:str, add_param_type:bool=False):
        """!
        @brief DoxyCommentGenerator constructor
        @param block_start {string} Comment block start marker for the input file type.
        @param block_end {string} Comment block end marker for the input file type.
        @param block_line_start {string} Comment block line start marker for the input file type.
        @param single_line_start {string} Single line comment block start marker for the input file type.
        @param add_param_type {boolean} True add the parameter type to the doxygen param comment text
                                      False do not add parameter type to the doxygen param comment text
        """
        ## Multiline line block start comment marker or None
        self.block_start = block_start
        ## Multiline line block end comment marker or None
        self.block_end = block_end
        ## Multiline line block interior line comment marker or None
        self.block_line_start = block_line_start
        ## Single line comment marker
        self.single_line_start = single_line_start

        ## True if parameter comment should also include the parameter type in the description, else false
        self.add_param_type = add_param_type

        ## Maximum line length used to determine self.desc_format_max
        self.format_max_length = 120
        ## Maximum line length of a description string
        self.desc_format_max = self.format_max_length
        ## Current open group definition count
        self.group_counter = 0

        if self.block_start is not None:
            self.desc_format_max = self.format_max_length-len(self.block_start)
        elif self.single_line_start is not None:
            self.desc_format_max = self.format_max_length-len(self.single_line_start)


    def _gen_comment_block_prefix(self)->str:
        """!
        @brief Generate doxygen block prefix string
        @return string - Formatted block prefix
        """
        if self.block_line_start is not None:
            prefix = " "+self.block_line_start+" "
        elif self.single_line_start is not None:
            prefix = self.single_line_start+" "
        else:
            raise Exception("ERROR: Can't have a doxygen comment if there are no comment markers.")
        return prefix

    def _gen_block_start(self)->str:
        """!
        @brief Generate doxygen block start string
        @return string - Formatted block prefix
        """
        # Set the start
        if self.block_start is not None:
            block_start = self.block_start
        elif self.single_line_start is not None:
            block_start = self.single_line_start
        else:
            raise Exception("ERROR: Can't have a doxygen comment if there are no comment markers.")
        return block_start

    def _gen_block_end(self)->str:
        """!
        @brief Generate doxygen block start string
        @return string - Formatted block prefix
        """
        # Set the end
        if self.block_end is not None:
            if self.block_end == '"""':
                block_end = self.block_end
            else:
                block_end = " "+self.block_end
        else:
            block_end = ""
        return block_end

    def _gen_brief_desc(self, brief_desc:str, prefix:str)->list:
        """!
        @brief Generate the doxygen comment block

        @param brief_desc {string} @brief description for the comment block
        @param prefix {string} Current comment block indentation prefix
        @return list of strings - Long description comment as a list of formatted strings
        """
        brief_desc_list = []

        # Generate the brief description text
        brief_start = "@brief "
        formatted_brief_txt = MultiLineFormat(brief_desc, self.desc_format_max-len(brief_start))
        firstdesc = True
        for brief_line in formatted_brief_txt:
            brief_desc_list.append(prefix+brief_start+brief_line+"\n")

            if firstdesc:
                firstdesc = False
                brief_start = "       "

        return brief_desc_list

    def _gen_long_desc(self, prefix:str, long_desc:str|None = None)->list:
        """!
        @brief Generate the doxygen comment block

        @param prefix {string} Current comment block prefix string
        @param long_desc {string} Detailed description for the comment block or None if no detailed description

        @return list of strings - Long description comment as a list of formatted strings
        """
        long_descList = []

        # Generate the long description text
        if long_desc is not None:
            formatted_long_txt = MultiLineFormat(long_desc, self.desc_format_max)
            for long_descLine in formatted_long_txt:
                long_descList.append(prefix+long_descLine+"\n")
        return long_descList

    def _gen_comment_return_text(self, ret_dict:dict, prefix:str)->list:
        """!
        @brief Generate @return doxygen text

        @param ret_dict {dictionary} - Return parameter data
        @param prefix {string} Current comment block prefix string

        @return list of strings - Formatted string list for the comment block
        """
        # Construct first return line
        return_type, return_desc, type_mod = ParamRetDict.get_return_data(ret_dict)
        l1 = "@return "+return_type+" - "

        # Format the description into sized string(s)
        desc_list = MultiLineFormat(return_desc, self.desc_format_max-len(l1))

        # Construct the final block return text
        ret_list = []
        firstdesc = True
        desc_prefix = prefix+l1
        for desc_str in desc_list:
            ret_list.append(desc_prefix+desc_str+"\n")
            if firstdesc:
                firstdesc = False
                desc_prefix = prefix+"".rjust(len(l1), ' ')

        # return the final formated data string list
        return ret_list

    def _gen_comment_param_text(self, param_dict:dict, prefix:str)->list:
        """!
        @brief Generate parameter doxygen text

        @param param_dict {dictionary} - Return parameter data
        @param prefix {string} Current comment block prefix string

        @return list of strings - Formatted string list for the comment block
        """
        # Construct first param line
        param_name, param_type, param_desc, type_mod = ParamRetDict.get_param_data(param_dict)
        l1 = "@param "+param_name
        if self.add_param_type:
            l1 += " {"+param_type+"}"
        l1 += " "

        # Format the description into sized string(s)
        desc_list = MultiLineFormat(param_desc, self.desc_format_max-len(l1))

        # Add the description string(s)
        firstdesc = True
        ret_list = []
        param_prefix = prefix+l1
        for desc_str in desc_list:
            ret_list.append(param_prefix+desc_str+"\n")
            if firstdesc:
                firstdesc = False
                param_prefix = prefix+"".rjust(len(l1), ' ')

        # return the final formated data string list
        return ret_list

    def gen_doxy_method_comment(self, brief_desc:str, param_dict_list:list, ret_dict:dict|None = None,
                             long_desc:str|None = None, block_indent:int = 0)->list:
        """!
        @brief Generate the doxygen comment block

        @param brief_desc {string} @brief description for the comment block
        @param param_dict_list {list of dictionaries} - Return parameter data
        @param ret_dict {dictionary} - Return parameter data
        @param long_desc {string} Detailed description for the comment block or None if no detailed description
        @param block_indent Current comment block indentation

        @return list of strings - Comment block as a list of formatted strings
        """
        # Generate the block start
        pad_prefix = "".rjust(block_indent, ' ')
        block_str_list = [pad_prefix+self._gen_block_start()+"\n"]

        # Generate the block prefix text fot the rest
        prefix = pad_prefix+self._gen_comment_block_prefix()

        # Add the brief text
        block_str_list.extend(self._gen_brief_desc(brief_desc, prefix))
        block_str_list.append(prefix+"\n") # add empty line for readability

        # Add the long description
        if long_desc is not None:
            block_str_list.extend(self._gen_long_desc(prefix, long_desc))
            block_str_list.append(prefix+"\n") # add empty line for readability

        # Add Param data
        if (len(param_dict_list) > 0):
            for param_dict in param_dict_list:
                block_str_list.extend(self._gen_comment_param_text(param_dict, prefix))
            block_str_list.append(prefix+"\n") # add empty line for readability

        # Add return data
        if ret_dict is not None:
            block_str_list.extend(self._gen_comment_return_text(ret_dict, prefix))

        # Complete the block
        block_str_list.append(pad_prefix+self._gen_block_end()+"\n")
        return block_str_list

    def gen_doxy_class_comment(self, brief_desc:str|None, long_desc:str|None = None, block_indent:int = 0)->list:
        """!
        @brief Generate a doxygen cgen_doxy_class_commentlass/structure documentation block

        @param brief_desc {string} @brief description for the comment block
        @param long_desc {string} Detailed description for the comment block or None if no detailed description
        @param block_indent Current cmment block indentation

        @return list of strings - Comment block as a list of formatted strings
        """
        # Generate the block start
        pad_prefix = "".rjust(block_indent, ' ')
        block_str_list = [pad_prefix+self._gen_block_start()+"\n"]

        # Generate the block prefix text fot the rest
        prefix = pad_prefix+self._gen_comment_block_prefix()

        # Add the brief text
        if brief_desc is not None:
            block_str_list.extend(self._gen_brief_desc(brief_desc, prefix))

        # Add the long description
        if long_desc is not None:
            if brief_desc is not None:
                block_str_list.append(prefix+"\n") # add empty line for readability
            block_str_list.extend(self._gen_long_desc(prefix, long_desc))

        # Complete the block
        block_str_list.append(pad_prefix+self._gen_block_end()+"\n")
        return block_str_list

    def gen_doxy_defgroup(self, file_name:str, group:str|None = None, groupdef:str|None = None)->list:
        """!
        @brief Doxygen defgroup comment block
        @param file_name {string} File name and extention
        @param group {string} Name of the group to define
        @param groupdef {string} Description of the new group
        @return list of strings - Code to output
        """
        doxy_group_blk = [self._gen_block_start()+"\n"]

        # Generate the block prefix text fot the rest
        prefix = self._gen_comment_block_prefix()
        doxy_group_blk.append(prefix+"@file "+file_name+"\n")
        if group is not None:
            if groupdef is not None:
                doxy_group_blk.append(prefix+"@defgroup "+group+" "+groupdef+"\n")
            doxy_group_blk.append(prefix+"@ingroup "+group+"\n")
            doxy_group_blk.append(prefix+"@{\n")
            self.group_counter += 1
        doxy_group_blk.append(self._gen_block_end()+"\n")
        return doxy_group_blk

    def gen_doxy_group_end(self)->str|None:
        """!
        @brief Doxygen group comment block end marker
        @return string or None - Code to output
        """
        if self.group_counter > 0:
            doxy_end = self._gen_block_start()+"@}"+self._gen_block_end()+"\n"
            self.group_counter -= 1
            return doxy_end
        else:
            return None

    def gen_single_line_start(self)->str:
        """!
        @brief Generate doxygen single line comment start string
        @return string - Formatted block prefix
        """
        # Set the start
        return self.single_line_start

    def gen_doxy_var_doc_str(self, desc:str)->str:
        """!
        @brief Generate Doxygen variable comment
        @param desc {string} Variable description
        @return string Documentation string
        """
        return self.single_line_start+"< "+desc

class CDoxyCommentGenerator(DoxyCommentGenerator):
    """!
    C/C++ file Doxygen comment generator class
    """
    def __init__(self):
        """!
        CDoxyCommentGenerator constructor
        """
        super().__init__('/**', '*/', '*', '//!', False)

class PyDoxyCommentGenerator(DoxyCommentGenerator):
    """!
    Python file Doxygen comment generator class
    """
    def __init__(self):
        """!
        PyDoxyCommentGenerator constructor
        """
        super().__init__('"""!', '"""', '', '##', True)

    def gen_doxy_var_doc_str(self, desc:str)->str:
        """!
        @brief Generate Doxygen variable comment
        @param desc {string} Variable description
        @return string Documentation string
        """
        return self.single_line_start+" "+desc

class TsDoxyCommentGenerator(DoxyCommentGenerator):
    """!
    Typescript file Doxygen comment generator class
    """
    def __init__(self):
        """!
        TsDoxyCommentGenerator constructor
        """
        super().__init__('/**', '*/', '*', '//!', True)

class JsDoxyCommentGenerator(DoxyCommentGenerator):
    """!
    Javascript file Doxygen comment generator class
    """
    def __init__(self):
        """!
        JsDoxyCommentGenerator constructor
        """
        super().__init__('/**', '*/', '*', '//!', True)
