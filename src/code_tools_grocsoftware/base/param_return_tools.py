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

class ParamRetDict():
    """!
    Parameter/Return value dictionary utility functions
    """
    ## List return/parameter bit flag value, type_mod value & type_mod_list = 0
    ## return/parameter is not a list, = 1 return/parameter is not a list
    type_mod_list:int  = 1<<0
    ## Pointer return/parameter bit flag value, type_mod value & type_mod_list = 0
    ## return/parameter is not a pointer, = 1 return/parameter is not a pointer
    type_mod_ptr:int   = 1<<1
    ## Reference return/parameter bit flag value, type_mod value & type_mod_list = 0
    ## return/parameter is not a reference, = 1 return/parameter is not a reference
    type_mod_ref:int   = 1<<2
    ## Undefined return/parameter bit flag value, type_mod value & type_mod_list = 0
    ## return/parameter cannot be unknown, = 1 return/parameter can be unknown
    type_mod_undef:int = 1<<3

    ## Return/parameter type_mod array size value bit shift
    type_mod_array_shift:int = 16
    ## Return/parameter type_mod array post shift size mask
    type_mod_array_mask:int  = 0xFFFF

    @staticmethod
    def build_dict_mod_value(is_list:bool = False, is_reference:bool = False,
                             is_ptr:bool = False, or_undef:bool = False) -> int:
        """!
        @brief Build a return data dictionary
        @param is_list {boolean} True if return is list, false if not
        @param is_reference {boolean} True if item needs a pointer decoration, false if not
        @param is_ptr {boolean} True if item needs a reference decoration, false if not
        @param or_undef {boolean} True if item can also be language undefined type, false if not
        @return {int} Mod value
        """
        entry_type_mod = 0
        if is_list:
            entry_type_mod |= ParamRetDict.type_mod_list
        if is_reference:
            entry_type_mod |= ParamRetDict.type_mod_ref
        if is_ptr:
            entry_type_mod |= ParamRetDict.type_mod_ptr
        if or_undef:
            entry_type_mod |= ParamRetDict.type_mod_undef
        return entry_type_mod

    @staticmethod
    def build_return_dict_with_mod(ret_type:str, ret_desc:str = "", entry_type_mod:int = 0) -> dict:
        """!
        @brief Build a return data dictionary
        @param ret_type {string} Code type definition
        @param ret_desc {string} Brief description of the return value for
                                 @return doxygen generation
        @param entry_type_mod {integer} Type modification flags
        @return {dictionary} Return dictionary
        """
        return {'type':ret_type, 'desc':ret_desc, 'typeMod': entry_type_mod}

    @staticmethod
    def build_return_dict(ret_type:str, ret_desc:str = "", is_list:bool = False,
                        is_reference:bool = False, is_ptr:bool = False,
                        or_undef:bool = False) -> dict:
        """!
        @brief Build a return data dictionary
        @param ret_type {string} Code type definition
        @param ret_desc {string} Brief description of the return value for @return
                                 doxygen generation
        @param is_list {boolean} True if return is list, false if not
        @param is_reference {boolean} True if parameter needs a pointer decoration, false if not
        @param is_ptr {boolean} True if parameter needs a reference decoration, false if not
        @param or_undef {boolean} True if item can also be language undefined type, false if not
        @return {dictionary} Return dictionary
        """
        entry_type_mod = ParamRetDict.build_dict_mod_value(is_list, is_reference, is_ptr, or_undef)
        return ParamRetDict.build_return_dict_with_mod(ret_type, ret_desc, entry_type_mod)

    @staticmethod
    def get_return_data(return_dict:dict) -> tuple:
        """!
        @brief Build a return data dictionary
        @param return_dict {dictionary} Return dictionary entry
        @return tuple - Return type string
                        Return description string,
                        Return type modifier bit flags
        """
        return return_dict['type'], return_dict['desc'], return_dict['typeMod']

    @staticmethod
    def get_return_type(return_dict:dict) -> str:
        """!
        @brief Build a return data dictionary
        @param return_dict {dictionary} Return dictionary entry
        @return string - Return type string
        """
        return return_dict['type']

    @staticmethod
    def get_return_desc(return_dict:dict) -> str:
        """!
        @brief Build a return data dictionary
        @param return_dict {dictionary} Return dictionary entry
        @return string - Return type brief description
        """
        return return_dict['desc']

    @staticmethod
    def get_return_type_mod(return_dict:dict) -> int:
        """!
        @brief Build a return data dictionary
        @param return_dict {dictionary} Return dictionary entry
        @return int - Return type modification flags
        """
        return return_dict['typeMod']

    @staticmethod
    def build_param_dict_with_mod(param_name:str, param_type:str,
                                  param_desc:str = "", entry_type_mod:int = 0) -> dict:
        """!
        @brief Build a return data dictionary
        @param param_name {string} Code param name
        @param param_type {string} Code param type
        @param param_desc {string} Brief description of the param value for param doxygen generation
        @param entry_type_mod {int} Type modification flags
        @return {dictionary} Parameter dictionary
        """
        return {'name':param_name, 'type':param_type, 'desc':param_desc, 'typeMod':entry_type_mod}

    @staticmethod
    def build_param_dict(param_name:str, param_type:str, param_desc:str = "",
                         is_list:bool = False, is_reference:bool = False,
                         is_ptr:bool = False, or_undef:bool = False) -> dict:
        """!
        @brief Build a return data dictionary
        @param param_name {string} Code param name
        @param param_type {string} Code param type
        @param param_desc {string} Brief description of the param value for param doxygen generation
        @param is_list {boolean} True if parameter is list, false if not
        @param is_reference {boolean} True if parameter needs a pointer decoration, false if not
        @param is_ptr {boolean} True if parameter needs a reference decoration, false if not
        @param or_undef {boolean} True if item can also be language undefined type, false if not
        @return {dictionary} Parameter dictionary
        """
        mod = ParamRetDict.build_dict_mod_value(is_list, is_reference, is_ptr, or_undef)
        return ParamRetDict.build_param_dict_with_mod(param_name, param_type, param_desc, mod)

    @staticmethod
    def get_param_data(param_dict:dict) -> tuple:
        """!
        @brief Build a return data dictionary
        @param param_dict {dictionary} Parameter dictionary entry
        @return tuple - Parameter name string,
                        Parameter type string (text|number),
                        Parameter description string
                        Parameter type modifier bit flags
        """
        return param_dict['name'], param_dict['type'], param_dict['desc'], param_dict['typeMod']

    @staticmethod
    def get_param_type(param_dict:dict) -> str:
        """!
        @brief Build a return data dictionary
        @param param_dict {dictionary} Parameter dictionary entry
        @return string - Parameter type string
        """
        return param_dict['type']

    @staticmethod
    def get_param_name(param_dict:dict) -> str:
        """!
        @brief Build a return data dictionary
        @param param_dict {dictionary} Parameter dictionary entry
        @return string - Parameter name string
        """
        return param_dict['name']

    @staticmethod
    def get_param_desc(param_dict:dict) -> str:
        """!
        @brief Build a return data dictionary
        @param param_dict {dictionary} Parameter dictionary entry
        @return string - Parameter description string
        """
        return param_dict['desc']

    @staticmethod
    def get_param_type_mod(param_dict:dict) -> int:
        """!
        @brief Build a return data dictionary
        @param param_dict {dictionary} Parameter dictionary entry
        @return int - Parameter type modification flags
        """
        return param_dict['typeMod']

    @staticmethod
    def is_mod_list(type_mod:int) -> bool:
        """!
        @brief Check if the input type_mode has the list modifier set
        @param type_mod {integer} Dictionary TypeMod entry
        @return bool - True if object needs to be a list type, else false
        """
        return bool((type_mod & ParamRetDict.type_mod_list) != 0)

    @staticmethod
    def is_mod_pointer(type_mod:int) -> bool:
        """!
        @brief Check if the input type_mode has the pointer modifier set
        @param type_mod {integer} Dictionary TypeMod entry
        @return bool - True if object needs a pointer decoration, else false
        """
        return bool((type_mod & ParamRetDict.type_mod_ptr) != 0)

    @staticmethod
    def is_mod_reference(type_mod:int) -> bool:
        """!
        @brief Check if the input type_mode has the reference modifier set
        @param type_mod {integer} Dictionary TypeMod entry
        @return bool - True if object needs a reference decoration, else false
        """
        return bool((type_mod & ParamRetDict.type_mod_ref) != 0)

    @staticmethod
    def is_or_undef_type(type_mod:int) -> bool:
        """!
        @brief Check if the input type_mode has the Or undefined modifier set
        @param type_mod {integer} Dictionary TypeMod entry
        @return bool - True if object can be undefined, else false
        """
        return bool((type_mod & ParamRetDict.type_mod_undef) != 0)

    @staticmethod
    def get_array_size(type_mod:int) -> int:
        """!
        @brief Get the array size in the type modifier value
        @param type_mod {integer} Dictionary TypeMod entry
        @return int - Array size
        """
        mask = ParamRetDict.type_mod_array_mask
        shift = ParamRetDict.type_mod_array_shift
        size = (type_mod >> shift) & mask
        return size

    @staticmethod
    def set_type_mod_array_size(type_mod_input:int, array_size:int)->int:
        """!
        @brief Get the array size in the type modifier value
        @param type_mod_input {int} Current type_mod value
        @param array_size {integer} Size of the array
        @return type_mod value with array set
        """
        mask = ParamRetDict.type_mod_array_mask
        shift = ParamRetDict.type_mod_array_shift
        type_mod = type_mod_input | ((array_size & mask) << shift)
        type_mod &= (~ParamRetDict.type_mod_list)  # Cannot be array and list
        return type_mod

    @staticmethod
    def set_array_size(var_dict:dict, array_size:int):
        """!
        @brief Get the array size in the type modifier value
        @param var_dict {dict} Dictionary object to modify
        @param array_size {integer} Size of the array
        """
        var_dict['typeMod'] = ParamRetDict.set_type_mod_array_size(var_dict['typeMod'], array_size)
