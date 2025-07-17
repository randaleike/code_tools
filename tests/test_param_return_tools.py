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

class Test01Buildmodification:
    """!
    @brief Unit test for the ParamRetDict class
    """
    def test01_build_mod(self):
        """!
        @brief Test build modification value function, default modification
        """
        test_mod = ParamRetDict.build_dict_mod_value()
        assert 0 == test_mod

    def test02_build_mod_list(self):
        """!
        @brief Test build modification value function, list modification
        """
        test_mod = ParamRetDict.build_dict_mod_value(is_list=True)
        assert ParamRetDict.type_mod_list == test_mod

    def test03_build_mod_ref(self):
        """!
        @brief Test build modification value function, reference modification
        """
        test_mod = ParamRetDict.build_dict_mod_value(is_reference=True)
        assert ParamRetDict.type_mod_ref == test_mod

    def test04_build_mod_ptr(self):
        """!
        @brief Test build modification value function, pointer modification
        """
        test_mod = ParamRetDict.build_dict_mod_value(is_ptr=True)
        assert ParamRetDict.type_mod_ptr == test_mod

    def test05_build_mod_undefined(self):
        """!
        @brief Test build modification value function, undefined modification
        """
        test_mod = ParamRetDict.build_dict_mod_value(or_undef=True)
        assert ParamRetDict.type_mod_undef == test_mod

    def test06_build_mod_multiple(self):
        """!
        @brief Test build modification value function, multiple modifications
        """
        test_mod = ParamRetDict.build_dict_mod_value(True, True, True, True)
        assert 0x0F == test_mod

    def test07_test_is_functions_true(self):
        """!
        @brief Test the mod check functions
        """
        test_mod = ParamRetDict.build_dict_mod_value(True, True, True, True)
        assert ParamRetDict.is_mod_list(test_mod)
        assert ParamRetDict.is_mod_pointer(test_mod)
        assert ParamRetDict.is_mod_reference(test_mod)
        assert ParamRetDict.is_or_undef_type(test_mod)

    def test08_test_is_functions_true(self):
        """!
        @brief Test the mod check functions
        """
        test_mod = ParamRetDict.build_dict_mod_value()
        assert not ParamRetDict.is_mod_list(test_mod)
        assert not ParamRetDict.is_mod_pointer(test_mod)
        assert not ParamRetDict.is_mod_reference(test_mod)
        assert not ParamRetDict.is_or_undef_type(test_mod)

    def test09_test_is_functions_false(self):
        """!
        @brief Test the mod check functions
        """
        test_mod = ParamRetDict.build_dict_mod_value()
        assert not ParamRetDict.is_mod_list(test_mod)
        assert not ParamRetDict.is_mod_pointer(test_mod)
        assert not ParamRetDict.is_mod_reference(test_mod)
        assert not ParamRetDict.is_or_undef_type(test_mod)

    def test10_test_set_type_mod_array_size(self):
        """!
        @brief Test the get array size value
        """
        test_list = [0,1,2,37,62,100,1000,10000]
        mask = ParamRetDict.type_mod_array_mask
        shift = ParamRetDict.type_mod_array_shift
        for test_value in test_list:
            expected_val = (test_value & mask) << shift
            assert expected_val == ParamRetDict.set_type_mod_array_size(0, test_value)

    def test11_test_set_type_mod_array_size_ptr_override(self):
        """!
        @brief Test the get array size value
        """
        test_list = [0,1,2,37,62,100,1000,10000]
        mask = ParamRetDict.type_mod_array_mask
        shift = ParamRetDict.type_mod_array_shift
        lstmod = ParamRetDict.type_mod_list
        for test_value in test_list:
            expected_val = (test_value & mask) << shift
            assert expected_val == ParamRetDict.set_type_mod_array_size(lstmod, test_value)

    def test12_test_get_array_size(self):
        """!
        @brief Test the get array size value
        """
        test_list = [0,1,2,37,62,100,1000,10000]
        for test_value in test_list:
            test_mod = ParamRetDict.set_type_mod_array_size(0, test_value)
            assert test_value == ParamRetDict.get_array_size(test_mod)

    def test13_test_set_array_size(self):
        """!
        @brief Test the get array size value
        """
        test_list = [0,1,2,37,62,100,1000,10000]
        test_dict = {'typeMod':0}

        for test_value in test_list:
            test_dict['typeMod'] = 0

            ParamRetDict.set_array_size(test_dict, test_value)
            assert test_value == ParamRetDict.get_array_size(test_dict['typeMod'])

class Test02ReturnDict:
    """!
    @brief Unit test for the ParamRetDict class
    """

    def test01_build_return_dict_default_mod(self):
        """!
        @brief Test build return dictionary function, default modification
        """
        test_dict = ParamRetDict.build_return_dict("string",
                                                   "Test return base description")
        key_list = list(test_dict.keys())
        assert 3 == len(key_list)
        assert 'type' in key_list
        assert 'desc' in key_list
        assert 'typeMod' in key_list

        assert "string" == test_dict['type']
        assert "Test return base description" == test_dict['desc']
        assert 0 == test_dict['typeMod']

    def test02_build_return_dict_list_mod(self):
        """!
        @brief Test build return dictionary function, list modification
        """
        test_dict = ParamRetDict.build_return_dict("string",
                                                   "Test return list modification",
                                                   True)
        key_list = list(test_dict.keys())
        assert 3 == len(key_list)
        assert 'type' in key_list
        assert 'desc' in key_list
        assert 'typeMod' in key_list

        assert "string" == test_dict['type']
        assert "Test return list modification" == test_dict['desc']
        assert ParamRetDict.type_mod_list == test_dict['typeMod']

    def test03_build_return_dict_ref_mod(self):
        """!
        @brief Test build return dictionary function, reference modification
        """
        test_dict = ParamRetDict.build_return_dict("integer",
                                                   "Test return reference modification",
                                                   is_reference=True)
        key_list = list(test_dict.keys())
        assert 3 == len(key_list)
        assert 'type' in key_list
        assert 'desc' in key_list
        assert 'typeMod' in key_list

        assert "integer" == test_dict['type']
        assert "Test return reference modification" == test_dict['desc']
        assert ParamRetDict.type_mod_ref == test_dict['typeMod']

    def test04_build_return_dict_ptr_mod(self):
        """!
        @brief Test build return dictionary function, pointer modification
        """
        test_dict = ParamRetDict.build_return_dict("integer",
                                                   "Test return pointer modification",
                                                   is_ptr=True)
        key_list = list(test_dict.keys())
        assert 3 == len(key_list)
        assert 'type' in key_list
        assert 'desc' in key_list
        assert 'typeMod' in key_list

        assert "integer" == test_dict['type']
        assert "Test return pointer modification" == test_dict['desc']
        assert ParamRetDict.type_mod_ptr == test_dict['typeMod']

    def test05_build_return_dict_undefined_mod(self):
        """!
        @brief Test build return dictionary function, undefined modification
        """
        test_dict = ParamRetDict.build_return_dict("unsigned",
                                                   "Test return undefined modification",
                                                   or_undef=True)
        key_list = list(test_dict.keys())
        assert 3 == len(key_list)
        assert 'type' in key_list
        assert 'desc' in key_list
        assert 'typeMod' in key_list

        assert "unsigned" == test_dict['type']
        assert "Test return undefined modification" == test_dict['desc']
        assert ParamRetDict.type_mod_undef == test_dict['typeMod']

    def test06_build_return_dict_multiple_mods(self):
        """!
        @brief Test build return dictionary function, multiple modifications
        """
        test_dict = ParamRetDict.build_return_dict("size",
                                                   "Test return multiple modifications",
                                                   is_list=True,
                                                   is_reference=True,
                                                   is_ptr=True,
                                                   or_undef=True)
        key_list = list(test_dict.keys())
        assert 3 == len(key_list)
        assert 'type' in key_list
        assert 'desc' in key_list
        assert 'typeMod' in key_list

        assert "size" == test_dict['type']
        assert "Test return multiple modifications" == test_dict['desc']
        expected_mod = ParamRetDict.type_mod_list
        expected_mod |= ParamRetDict.type_mod_ptr
        expected_mod |= ParamRetDict.type_mod_ref
        expected_mod |= ParamRetDict.type_mod_undef
        assert expected_mod == test_dict['typeMod']

    def test07_build_return_dict_default_plus_array(self):
        """!
        @brief Test build return dictionary function, add array set
        """
        test_dict = ParamRetDict.build_return_dict("float",
                                                   "Test return array post modification")
        ParamRetDict.set_array_size(test_dict, 7)

        key_list = list(test_dict.keys())
        assert 3 == len(key_list)
        assert 'type' in key_list
        assert 'desc' in key_list
        assert 'typeMod' in key_list

        assert "float" == test_dict['type']
        assert "Test return array post modification" == test_dict['desc']
        expected_mod = 7 << ParamRetDict.type_mod_array_shift
        assert expected_mod == test_dict['typeMod']

    def test08_build_return_dict_ptr_plus_array(self):
        """!
        @brief Test build return dictionary function, pointer modification plus array set
        """
        test_dict = ParamRetDict.build_return_dict("float",
                                                   "Test return ptr array post modification",
                                                   is_ptr=True)
        ParamRetDict.set_array_size(test_dict, 8)

        key_list = list(test_dict.keys())
        assert 3 == len(key_list)
        assert 'type' in key_list
        assert 'desc' in key_list
        assert 'typeMod' in key_list

        assert "float" == test_dict['type']
        assert "Test return ptr array post modification" == test_dict['desc']
        expected_mod = (8 << ParamRetDict.type_mod_array_shift) | ParamRetDict.type_mod_ptr
        assert expected_mod == test_dict['typeMod']

    def test09_build_return_dict_with_input_mod(self):
        """!
        @brief Test build return dictionary function, pointer modification plus array set
        """
        desc = "Test return dictionary with mode input"
        test_dict = ParamRetDict.build_return_dict_with_mod("struct",
                                                            desc,
                                                            55)

        key_list = list(test_dict.keys())
        assert 3 == len(key_list)
        assert 'type' in key_list
        assert 'desc' in key_list
        assert 'typeMod' in key_list

        assert "struct" == test_dict['type']
        assert "Test return dictionary with mode input" == test_dict['desc']
        assert 55 == test_dict['typeMod']

    def test10_get_return_data(self):
        """!
        @brief Test return dictionary get data function
        """
        desc = "Test return dictionary with mode input"
        test_dict = ParamRetDict.build_return_dict_with_mod("struct",
                                                            desc,
                                                            ParamRetDict.type_mod_list)
        assert "struct" == ParamRetDict.get_return_type(test_dict)
        assert "Test return dictionary with mode input" == ParamRetDict.get_return_desc(test_dict)
        assert ParamRetDict.type_mod_list == ParamRetDict.get_return_type_mod(test_dict)

    def test11_get_return_data_tuple(self):
        """!
        @brief Test return dictionary get data tuple function
        """
        desc = "Test return dictionary with mode input"
        test_dict = ParamRetDict.build_return_dict_with_mod("struct",
                                                            desc,
                                                            ParamRetDict.type_mod_ptr)

        ret_type, ret_desc, ret_mode = ParamRetDict.get_return_data(test_dict)
        assert "struct" == ret_type
        assert "Test return dictionary with mode input" == ret_desc
        assert ParamRetDict.type_mod_ptr == ret_mode


class Test03ParamDict:
    """!
    @brief Unit test for the ParamRetDict class
    """

    def test01_build_param_dict_default_mod(self):
        """!
        @brief Test build parameter dictionary function, default modification
        """
        test_dict = ParamRetDict.build_param_dict("foo",
                                                  "string",
                                                  "Test parameter base description")
        key_list = list(test_dict.keys())
        assert 4 == len(key_list)
        assert 'name' in key_list
        assert 'type' in key_list
        assert 'desc' in key_list
        assert 'typeMod' in key_list

        assert "foo" == test_dict['name']
        assert "string" == test_dict['type']
        assert "Test parameter base description" == test_dict['desc']
        assert 0 == test_dict['typeMod']

    def test02_build_param_dict_list_mod(self):
        """!
        @brief Test build parameter dictionary function, list modification
        """
        test_dict = ParamRetDict.build_param_dict("moo",
                                                  "string",
                                                  "Test parameter list modification",
                                                  True)
        key_list = list(test_dict.keys())
        assert 4 == len(key_list)
        assert 'name' in key_list
        assert 'type' in key_list
        assert 'desc' in key_list
        assert 'typeMod' in key_list

        assert "moo" == test_dict['name']
        assert "string" == test_dict['type']
        assert "Test parameter list modification" == test_dict['desc']
        assert ParamRetDict.type_mod_list == test_dict['typeMod']

    def test03_build_param_dict_ref_mod(self):
        """!
        @brief Test build parameter dictionary function, reference modification
        """
        test_dict = ParamRetDict.build_param_dict("goo",
                                                  "integer",
                                                  "Test parameter reference modification",
                                                  is_reference=True)
        key_list = list(test_dict.keys())
        assert 4 == len(key_list)
        assert 'name' in key_list
        assert 'type' in key_list
        assert 'desc' in key_list
        assert 'typeMod' in key_list

        assert "goo" == test_dict['name']
        assert "integer" == test_dict['type']
        assert "Test parameter reference modification" == test_dict['desc']
        assert ParamRetDict.type_mod_ref == test_dict['typeMod']

    def test04_build_param_dict_ptr_mod(self):
        """!
        @brief Test build parameter dictionary function, pointer modification
        """
        test_dict = ParamRetDict.build_param_dict("shoo",
                                                  "integer",
                                                  "Test parameter pointer modification",
                                                  is_ptr=True)
        key_list = list(test_dict.keys())
        assert 4 == len(key_list)
        assert 'name' in key_list
        assert 'type' in key_list
        assert 'desc' in key_list
        assert 'typeMod' in key_list

        assert "shoo" == test_dict['name']
        assert "integer" == test_dict['type']
        assert "Test parameter pointer modification" == test_dict['desc']
        assert ParamRetDict.type_mod_ptr == test_dict['typeMod']

    def test05_build_param_dict_undefined_mod(self):
        """!
        @brief Test build parameter dictionary function, undefined modification
        """
        test_dict = ParamRetDict.build_param_dict("too",
                                                  "unsigned",
                                                  "Test parameter undefined modification",
                                                  or_undef=True)
        key_list = list(test_dict.keys())
        assert 4 == len(key_list)
        assert 'name' in key_list
        assert 'type' in key_list
        assert 'desc' in key_list
        assert 'typeMod' in key_list

        assert "too" == test_dict['name']
        assert "unsigned" == test_dict['type']
        assert "Test parameter undefined modification" == test_dict['desc']
        assert ParamRetDict.type_mod_undef == test_dict['typeMod']

    def test06_build_param_dict_multiple_mods(self):
        """!
        @brief Test build parameter dictionary function, multiple modifications
        """
        test_dict = ParamRetDict.build_param_dict("yoo",
                                                  "size",
                                                  "Test parameter multiple modifications",
                                                   is_list=True,
                                                   is_reference=True,
                                                   is_ptr=True,
                                                   or_undef=True)
        key_list = list(test_dict.keys())
        assert 4 == len(key_list)
        assert 'name' in key_list
        assert 'type' in key_list
        assert 'desc' in key_list
        assert 'typeMod' in key_list

        assert "yoo" == test_dict['name']
        assert "size" == test_dict['type']
        assert "Test parameter multiple modifications" == test_dict['desc']
        expected_mod = ParamRetDict.type_mod_list
        expected_mod |= ParamRetDict.type_mod_ptr
        expected_mod |= ParamRetDict.type_mod_ref
        expected_mod |= ParamRetDict.type_mod_undef
        assert expected_mod == test_dict['typeMod']

    def test07_build_param_dict_default_plus_array(self):
        """!
        @brief Test build parameter dictionary function, add array set
        """
        test_dict = ParamRetDict.build_param_dict("pi",
                                                  "float",
                                                  "Test parameter array post modification")
        ParamRetDict.set_array_size(test_dict, 7)

        key_list = list(test_dict.keys())
        assert 4 == len(key_list)
        assert 'name' in key_list
        assert 'type' in key_list
        assert 'desc' in key_list
        assert 'typeMod' in key_list

        assert "pi" == test_dict['name']
        assert "float" == test_dict['type']
        assert "Test parameter array post modification" == test_dict['desc']
        expected_mod = 7 << ParamRetDict.type_mod_array_shift
        assert expected_mod == test_dict['typeMod']

    def test08_build_param_dict_ptr_plus_array(self):
        """!
        @brief Test build parameter dictionary function, pointer modification plus array set
        """
        desc = "Test parameter ptr array post modification"
        test_dict = ParamRetDict.build_param_dict("rugbyPlayers",
                                                  "string",
                                                  desc,
                                                  is_ptr=True)
        ParamRetDict.set_array_size(test_dict, 23)

        key_list = list(test_dict.keys())
        assert 4 == len(key_list)
        assert 'name' in key_list
        assert 'type' in key_list
        assert 'desc' in key_list
        assert 'typeMod' in key_list

        assert "rugbyPlayers" == test_dict['name']
        assert "string" == test_dict['type']
        assert "Test parameter ptr array post modification" == test_dict['desc']
        expected_mod = (23 << ParamRetDict.type_mod_array_shift) | ParamRetDict.type_mod_ptr
        assert expected_mod == test_dict['typeMod']

    def test09_build_param_dict_with_input_mod(self):
        """!
        @brief Test build parameter dictionary function, pointer modification plus array set
        """
        desc = "Test parameter dictionary with mode input"
        test_dict = ParamRetDict.build_param_dict_with_mod("employees",
                                                           "struct",
                                                           desc,
                                                           0x0440002)

        key_list = list(test_dict.keys())
        assert 4 == len(key_list)
        assert 'name' in key_list
        assert 'type' in key_list
        assert 'desc' in key_list
        assert 'typeMod' in key_list

        assert "employees" == test_dict['name']
        assert "struct" == test_dict['type']
        assert "Test parameter dictionary with mode input" == test_dict['desc']
        assert 0x0440002 == test_dict['typeMod']

    def test10_get_param_data(self):
        """!
        @brief Test parameter dictionary get data function
        """
        desc = "Test parameter dictionary with mode input"
        test_dict = ParamRetDict.build_param_dict_with_mod("employees",
                                                           "struct",
                                                           desc,
                                                           0x0440002)
        assert "employees" == ParamRetDict.get_param_name(test_dict)
        assert "struct" == ParamRetDict.get_param_type(test_dict)
        assert "Test parameter dictionary with mode input" == ParamRetDict.get_param_desc(test_dict)
        assert 0x0440002 == ParamRetDict.get_param_type_mod(test_dict)

    def test11_get_param_data_tuple(self):
        """!
        @brief Test parameter dictionary get data tuple function
        """
        desc = "Test parameter dictionary with mode input"
        test_dict = ParamRetDict.build_param_dict_with_mod("uid",
                                                           "integer",
                                                           desc,
                                                           ParamRetDict.type_mod_ptr)
        param_name, param_type, param_desc, param_mode = ParamRetDict.get_param_data(test_dict)

        assert "uid" == param_name
        assert "integer" == param_type
        assert "Test parameter dictionary with mode input" == param_desc
        assert ParamRetDict.type_mod_ptr == param_mode
