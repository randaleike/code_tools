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

import os
from unittest.mock import patch

from code_tools_grocsoftware.base.json_string_class_description import TransTxtParser
from code_tools_grocsoftware.base.json_string_class_description import StringClassDescription
from code_tools_grocsoftware.base.param_return_tools import ParamRetDict

from tests.dir_init import TESTFILEPATH

# pylint: disable=protected-access

LIST_PROMPT = "[T(ext)|i(nteger)|u(nsigned)|s(ize)|c(ustom)]: "
RET_PROMPT = "Enter return base type "+LIST_PROMPT
PARAM_PROMPT = "Enter parameter base type "+LIST_PROMPT

class Test02StringClassDescription:
    """!
    @brief Unit test for the StringClassDescription class
    """
    @classmethod
    def setup_class(cls):
        """!
        @brief class setup function
        """
        cls.test_json = os.path.join(TESTFILEPATH, "teststrdesc.json")
        cls.testlanglist = os.path.join(TESTFILEPATH, "teststringlanglist.json")


    @classmethod
    def teardown_class(cls):
        """!
        @brief class teardown function
        """
        if os.path.exists("jsonStringClassDescription.json"):
            # Delete in case it was accidently created
            os.remove("jsonStringClassDescription.json")


    @staticmethod
    def mock_param_ret_input(prompt:str, input_str)->str:
        """!
        @brief input parameter user input simulation
        @param prompt {str} input call prompt
        @param input_str {iterator} Test specific input response strings
        @return string - simulater user response
        """
        modprompts = ["Is full type a list [y/n]:",
                      "Is full type a pointer [y/n]:",
                      "Is full type a reference [y/n]:",
                      "Can value be undefined [y/n]:",
                      "Is full type an array [y/n]:"]
        if prompt in modprompts:
            return "n"
        if prompt == 'Enter custom type: ':
            return "foobar"
        return next(input_str)

    def test01_input_iso_translate_code_good_input(self, capsys):
        """!
        @brief Test _input_iso_translate_code(), good input
        """
        with patch('builtins.input', return_value='fr'):
            testobj = StringClassDescription()
            assert testobj._input_iso_translate_code() == 'fr'
            assert capsys.readouterr().out == ""

    def test02_input_iso_translate_code_invalid_input(self, capsys):
        """!
        @brief Test _input_iso_translate_code(), invalid input
        """
        input_str = (text for text in ["", "de1", "d", "german", "de"])
        def test_mock_in(_:str)->str:
            return next(input_str)

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()
            assert testobj._input_iso_translate_code() == 'de'
            expected_str = "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected_str += "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected_str += "Error: Only two characters a-z are allowed in the code, try again.\n"
            expected_str += "Error: Only two characters a-z are allowed in the code, try again.\n"
            assert capsys.readouterr().out == expected_str

    def test03_input_var_method_name_good_input(self, capsys):
        """!
        @brief Test _input_var_method_name(), method_name=true, good input
        """
        input_str = (text for text in ["validMethodName",
                                       "validMethodName2",
                                       "valid_method_name",
                                       "valid_method3_name"])
        def test_mock_in(_:str)->str:
            return next(input_str)

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()
            assert testobj._input_var_method_name(True) == 'validMethodName'
            assert testobj._input_var_method_name(True) == 'validMethodName2'
            assert testobj._input_var_method_name(True) == 'valid_method_name'
            assert testobj._input_var_method_name(True) == 'valid_method3_name'
            assert capsys.readouterr().out == ""

    def test04_input_var_method_name_invalid_input(self, capsys):
        """!
        @brief Test _input_var_method_name(), method_name=true, invalid input
        """
        input_str = (text for text in ["",
                                       "2invalid_method_name",
                                       "invalid-method-name",
                                       "invalid;Name",
                                       "validMethodName"])
        def test_mock_in(_:str)->str:
            return next(input_str)

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()
            assert testobj._input_var_method_name(True) == 'validMethodName'
            expected_str = "Error:  is not a valid code name, try again.\n"
            expected_str += "Error: 2invalid_method_name is not a valid code name, try again.\n"
            expected_str += "Error: invalid-method-name is not a valid code name, try again.\n"
            expected_str += "Error: invalid;Name is not a valid code name, try again.\n"
            assert capsys.readouterr().out == expected_str

    def test05_input_var_method_name_good_input_method_false(self, capsys):
        """!
        @brief Test _input_var_method_name(), method_name=false, good input
        """
        input_str = (text for text in ["validParamName",
                                       "validParamName2",
                                       "valid_param_name",
                                       "valid_param3_name"])
        def test_mock_in(_:str)->str:
            return next(input_str)

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()
            assert testobj._input_var_method_name(False) == 'validParamName'
            assert testobj._input_var_method_name(False) == 'validParamName2'
            assert testobj._input_var_method_name(False) == 'valid_param_name'
            assert testobj._input_var_method_name(False) == 'valid_param3_name'
            assert capsys.readouterr().out == ""

    def test06_input_var_method_name_invalid_input_method_false(self, capsys):
        """!
        @brief Test _input_var_method_name(), method_name=false, invalid input
        """
        input_str = (text for text in ["",
                                       "2invalid_param_name",
                                       "invalid-param-name",
                                       "invalid#ParamName",
                                       "validParamName"])
        def test_mock_in(_:str)->str:
            return next(input_str)

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()
            assert testobj._input_var_method_name(False) == 'validParamName'
            expected_str = "Error:  is not a valid code name, try again.\n"
            expected_str += "Error: 2invalid_param_name is not a valid code name, try again.\n"
            expected_str += "Error: invalid-param-name is not a valid code name, try again.\n"
            expected_str += "Error: invalid#ParamName is not a valid code name, try again.\n"
            assert capsys.readouterr().out == expected_str

    def test07_input_array_modifier_valid_input(self, capsys):
        """!
        @brief Test _input_var_method_name(), Valid input
        """
        testobj = StringClassDescription()

        expected_mod = ParamRetDict.set_type_mod_array_size(0, 10)
        with patch('builtins.input', return_value='10'):
            assert testobj._input_array_modifier(0) == expected_mod
            assert capsys.readouterr().out == ""

        expected_mod2 = ParamRetDict.set_type_mod_array_size(0, 23)
        with patch('builtins.input', return_value='23'):
            assert testobj._input_array_modifier(0) == expected_mod2
            assert capsys.readouterr().out == ""

        expected_mod3 = ParamRetDict.set_type_mod_array_size(0, 1)
        with patch('builtins.input', return_value='1'):
            assert testobj._input_array_modifier(0) == expected_mod3
            assert capsys.readouterr().out == ""

        expected_mod4 = ParamRetDict.set_type_mod_array_size(0, 65535)
        with patch('builtins.input', return_value='65535'):
            assert testobj._input_array_modifier(0) == expected_mod4
            assert capsys.readouterr().out == ""

    def test08_input_array_modifier_invalid_input(self, capsys):
        """!
        @brief Test _input_var_method_name(), Invalid input
        """
        input_list = ["0", "65636", "100000", "-1", "ten", "one", "10"]
        input_str = (text for text in input_list)
        def test_mock_in(_:str)->str:
            return next(input_str)

        testobj = StringClassDescription()

        expected_mod = ParamRetDict.set_type_mod_array_size(0, 10)
        with patch('builtins.input', test_mock_in):
            assert testobj._input_array_modifier(0) == expected_mod
            expected_error_str = "Error: must be a valid number between 1 and 65535\n"
            expected_error_str += "Error: must be a valid number between 1 and 65535\n"
            expected_error_str += "Error: must be a valid number between 1 and 65535\n"
            expected_error_str += "Error: must be a valid number between 1 and 65535\n"
            expected_error_str += "Error: must be an integer value\n"
            expected_error_str += "Error: must be an integer value\n"
            assert capsys.readouterr().out == expected_error_str

    def test09_input_type_modifier_list_all_no(self):
        """!
        @brief Test _input_type_modifier(), Simple case, all no
        """
        def test_mock_in(_:str)->str:
            return 'n'

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()
            assert testobj._input_type_modifier() == 0

    # pylint: disable=too-many-return-statements
    def test10_input_type_modifier_list_one_yes(self):
        """!
        @brief Test _input_type_modifier(), Simple case, one yes
        """
        input_dict = {'listAns': "n",
                     'ptrAns': "n",
                     'refAns': "n",
                     'undefAns': "n",
                     'arrayAns': "n"}
        def test_mock_in(prompt:str)->str:
            if prompt == "Is full type a list [y/n]:":
                return input_dict['listAns']
            if prompt == "Is full type a pointer [y/n]:":
                return input_dict['ptrAns']
            if prompt == "Is full type a reference [y/n]:":
                return input_dict['refAns']
            if prompt == "Can value be undefined [y/n]:":
                return input_dict['undefAns']
            if prompt == "Is full type an array [y/n]:":
                return input_dict['arrayAns']
            if prompt == "Size of the array in entries: ":
                return "5"
            return 'n'

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()
            for answer in list(input_dict):
                input_dict[answer] = 'y'
                if answer == 'listAns':
                    expected_mod = ParamRetDict.type_mod_list
                elif answer == 'ptrAns':
                    expected_mod = ParamRetDict.type_mod_ptr
                elif answer == 'refAns':
                    expected_mod = ParamRetDict.type_mod_ref
                elif answer == 'undefAns':
                    expected_mod = ParamRetDict.type_mod_undef
                elif answer == 'arrayAns':
                    expected_mod = 5 << ParamRetDict.type_mod_array_shift
                else:
                    expected_mod = 0

                assert testobj._input_type_modifier() == expected_mod
                input_dict[answer] = 'n'
    # pylint: enable=too-many-return-statements

    # pylint: disable=too-many-statements
    # pylint: disable=too-many-return-statements
    def test11_input_type_modifier_list_two_yes(self):
        """!
        @brief Test _input_type_modifier(), two yes
        """
        input_dict = {'listAns': "n",
                     'ptrAns': "n",
                     'refAns': "n",
                     'undefAns': "n",
                     'arrayAns': "n"}
        def test_mock_in(prompt:str)->str:
            if prompt == "Is full type a list [y/n]:":
                return input_dict['listAns']
            if prompt == "Is full type a pointer [y/n]:":
                return input_dict['ptrAns']
            if prompt == "Is full type a reference [y/n]:":
                return input_dict['refAns']
            if prompt == "Can value be undefined [y/n]:":
                return input_dict['undefAns']
            if prompt == "Is full type an array [y/n]:":
                return input_dict['arrayAns']
            if prompt == "Size of the array in entries: ":
                return "6"
            return 'n'

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()
            for first_yes in list(input_dict):
                input_dict[first_yes] = 'y'
                first_mod = 0
                array_entry = False
                if first_yes == 'listAns':
                    first_mod = ParamRetDict.type_mod_list
                elif first_yes == 'ptrAns':
                    first_mod = ParamRetDict.type_mod_ptr
                elif first_yes == 'refAns':
                    first_mod = ParamRetDict.type_mod_ref
                elif first_yes == 'undefAns':
                    first_mod = ParamRetDict.type_mod_undef
                elif first_yes == 'arrayAns':
                    first_mod = 6 << ParamRetDict.type_mod_array_shift
                    array_entry = True
                else:
                    first_mod = 0

                for second_yes in list(input_dict):
                    expected_mod = 0
                    if second_yes != first_yes:
                        input_dict[second_yes] = 'y'
                        if second_yes == 'listAns':
                            if array_entry:
                                expected_mod = first_mod
                            else:
                                expected_mod = ParamRetDict.type_mod_list | first_mod
                        elif second_yes == 'ptrAns':
                            expected_mod = ParamRetDict.type_mod_ptr | first_mod
                        elif second_yes == 'refAns':
                            expected_mod = ParamRetDict.type_mod_ref | first_mod
                        elif second_yes == 'undefAns':
                            expected_mod = ParamRetDict.type_mod_undef | first_mod
                        elif second_yes == 'arrayAns':
                            if first_mod == ParamRetDict.type_mod_list:
                                expected_mod = 6 << ParamRetDict.type_mod_array_shift
                            else:
                                expected_mod = (6 << ParamRetDict.type_mod_array_shift) | first_mod
                        else:
                            expected_mod = 0

                        assert testobj._input_type_modifier() == expected_mod
                        input_dict[second_yes] = 'n'

                input_dict[first_yes] = 'n'

    # pylint: enable=too-many-return-statements
    # pylint: enable=too-many-statements

    def test12_input_type_modifier_list_all_yes_except_array(self):
        """!
        @brief Test _input_type_modifier(), all yes, except array
        """
        def test_mock_in(prompt:str)->str:
            if prompt == "Is full type an array [y/n]:":
                return 'n'
            if prompt == "Size of the array in entries: ":
                return "7"
            return 'y'

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()
            expected_mod = ParamRetDict.type_mod_list
            expected_mod |= ParamRetDict.type_mod_ptr
            expected_mod |= ParamRetDict.type_mod_ref
            expected_mod |= ParamRetDict.type_mod_undef
            assert testobj._input_type_modifier() == expected_mod

    def test13_input_type_modifier_list_all_yes(self):
        """!
        @brief Test _input_type_modifier(), all yes
        """
        def test_mock_in(prompt:str)->str:
            if prompt == "Size of the array in entries: ":
                return "7"
            return 'y'

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()
            expected_mod = ParamRetDict.type_mod_ptr
            expected_mod |= ParamRetDict.type_mod_ref
            expected_mod |= ParamRetDict.type_mod_undef
            expected_mod |= 7 << ParamRetDict.type_mod_array_shift
            assert testobj._input_type_modifier() == expected_mod

    def test14_input_param_return_type_good_input_text(self, capsys):
        """!
        @brief Test _input_param_return_type(), good input, text
        """
        type_list = ["t", "T", "text", "TEXT", "Text"]
        input_list = []
        for element in type_list:
            input_list.append(element)
            input_list.append(element)

        input_str = (text for text in input_list)
        def test_mock_in(prompt:str)->str:
            return Test02StringClassDescription.mock_param_ret_input(prompt, input_str)

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()
            for _ in range(0,len(type_list)):
                type_name, type_mod = testobj._input_param_return_type(True)
                assert type_name == 'string'
                assert type_mod == 0

                type_name, type_mod = testobj._input_param_return_type(False)
                assert type_name == 'string'
                assert type_mod == 0

            assert capsys.readouterr().out == ""

    def test15_input_param_return_type_good_input_integer(self, capsys):
        """!
        @brief Test _input_param_return_type(), good input, integer
        """
        type_list = ["i", "I", "integer", "INTEGER", "Integer", "int", "Int", "INT"]
        input_list = []
        for element in type_list:
            input_list.append(element)
            input_list.append(element)

        input_str = (text for text in input_list)
        def test_mock_in(prompt:str)->str:
            return Test02StringClassDescription.mock_param_ret_input(prompt, input_str)

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()
            for _ in range(0,len(type_list)):
                type_name, type_mod = testobj._input_param_return_type(True)
                assert type_name == 'integer'
                assert type_mod == 0

                type_name, type_mod = testobj._input_param_return_type(False)
                assert type_name == 'integer'
                assert type_mod == 0

            assert capsys.readouterr().out == ""

    def test16_input_param_return_type_good_input_unsigned(self, capsys):
        """!
        @brief Test _input_param_return_type(), good input, integer
        """
        type_list = ["u", "U", "unsigned", "UNSIGNED", "Unsigned"]
        input_list = []
        for element in type_list:
            input_list.append(element)
            input_list.append(element)

        input_str = (text for text in input_list)
        def test_mock_in(prompt:str)->str:
            return Test02StringClassDescription.mock_param_ret_input(prompt, input_str)

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()
            for _ in range(0,len(type_list)):
                type_name, type_mod = testobj._input_param_return_type(True)
                assert type_name == 'unsigned'
                assert type_mod == 0

                type_name, type_mod = testobj._input_param_return_type(False)
                assert type_name == 'unsigned'
                assert type_mod == 0

            assert capsys.readouterr().out == ""

    def test17_input_param_return_type_good_input_size(self, capsys):
        """!
        @brief Test _input_param_return_type(), good input, integer
        """
        type_list = ["s", "S", "size", "Size", "SIZE"]
        input_list = []
        for element in type_list:
            input_list.append(element)
            input_list.append(element)

        input_str = (text for text in input_list)
        def test_mock_in(prompt:str)->str:
            return Test02StringClassDescription.mock_param_ret_input(prompt, input_str)

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()
            for _ in range(0,len(type_list)):
                type_name, type_mod = testobj._input_param_return_type(True)
                assert type_name == 'size'
                assert type_mod == 0

                type_name, type_mod = testobj._input_param_return_type(False)
                assert type_name == 'size'
                assert type_mod == 0

            assert capsys.readouterr().out == ""

    def test18_input_param_return_type_good_input_custom_good_name(self, capsys):
        """!
        @brief Test _input_param_return_type(), good input, custom, good custom name
        """
        type_list = ["c", "C", "custom", "CUSTOM", "Custom"]
        input_list = []
        for element in type_list:
            input_list.append(element)
            input_list.append(element)

        input_str = (text for text in input_list)
        def test_mock_in(prompt:str)->str:
            return Test02StringClassDescription.mock_param_ret_input(prompt, input_str)

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()
            for _ in range(0,len(type_list)):
                type_name, type_mod = testobj._input_param_return_type(True)
                assert type_name == 'foobar'
                assert type_mod == 0

                type_name, type_mod = testobj._input_param_return_type(False)
                assert type_name == 'foobar'
                assert type_mod == 0

            assert capsys.readouterr().out == ""

    def test19_input_return_type_input_custom_good_custom_names(self, capsys):
        """!
        @brief Test _input_param_return_type(), return, custom, good names
        """
        custom_type_list = ["test",
                            "test1",
                            "test_underscore",
                            "namespace::test",
                            "test2__underscore"]
        custom_type_names = (text for text in custom_type_list)
        def test_mock_in(prompt:str)->str:
            if prompt == 'Enter custom type: ':
                return next(custom_type_names)
            if prompt == RET_PROMPT:
                return "c"
            if prompt == PARAM_PROMPT:
                return "c"
            return "n"

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()

            for name in custom_type_list:
                type_name, type_mod = testobj._input_param_return_type(True)
                assert type_name == name
                assert type_mod == 0

            assert capsys.readouterr().out == ""

    def test20_input_param_type_input_custom_good_custom_names(self, capsys):
        """!
        @brief Test _input_param_return_type(), return, custom, good names
        """
        custom_type_list = ["test",
                            "test1",
                            "test_underscore",
                            "namespace::test",
                            "test2__underscore"]
        custom_type_names = (text for text in custom_type_list)

        def test_mock_in(prompt:str)->str:
            if prompt == 'Enter custom type: ':
                return next(custom_type_names)
            if prompt == RET_PROMPT:
                return "c"
            if prompt == PARAM_PROMPT:
                return "c"
            return "n"

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()

            for name in custom_type_list:
                type_name, type_mod = testobj._input_param_return_type(False)
                assert type_name == name
                assert type_mod == 0

            assert capsys.readouterr().out == ""

    def test21_input_return_type_input_custom_bad_custom_names(self, capsys):
        """!
        @brief Test _input_param_return_type(), custom, bad names, return type
        """
        custom_type_list = ["1test", "test-dash", "test@", "namespace??test", "goodName"]
        custom_type_names = (text for text in custom_type_list)
        def test_mock_in(prompt:str)->str:
            if prompt == 'Enter custom type: ':
                return next(custom_type_names)
            if prompt == RET_PROMPT:
                return "c"
            if prompt == PARAM_PROMPT:
                return "c"
            return "n"

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()

            type_name, type_mod = testobj._input_param_return_type(True)
            assert type_name == 'goodName'
            assert type_mod == 0

            expected_str = ""
            for name in custom_type_list:
                if name != 'goodName':
                    expected_str += name+" is not a valid code type name, try again.\n"
            assert capsys.readouterr().out == expected_str

    def test22_input_param_type_input_custom_bad_custom_names(self, capsys):
        """!
        @brief Test _input_param_return_type(), custom, bad names, param type
        """
        custom_type_list = ["1test", "test-dash", "test@", "namespace??test", "goodName"]
        custom_type_names = (text for text in custom_type_list)
        def test_mock_in(prompt:str)->str:
            if prompt == 'Enter custom type: ':
                return next(custom_type_names)
            if prompt == RET_PROMPT:
                return "c"
            if prompt == PARAM_PROMPT:
                return "c"
            return "n"

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()

            type_name, type_mod = testobj._input_param_return_type(False)
            assert type_name == 'goodName'
            assert type_mod == 0

            expected_str = ""
            for name in custom_type_list:
                if name != 'goodName':
                    expected_str += name+" is not a valid code type name, try again.\n"
            assert capsys.readouterr().out == expected_str

    def test23_input_param_return_type_input_invalid_type(self, capsys):
        """!
        @brief Test _input_param_return_type(), invalid type selection
        """
        input_str = (text for text in ["x", "a", "dict", "i", "x", "z", "list", "i"])
        def test_mock_in(prompt:str)->str:
            return Test02StringClassDescription.mock_param_ret_input(prompt, input_str)

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()
            type_name, type_mod = testobj._input_param_return_type(True)
            assert type_name == 'integer'
            assert type_mod == 0

            type_name, type_mod = testobj._input_param_return_type(False)
            assert type_name == 'integer'
            assert type_mod == 0

            expected_str = "Error: \"x\" unknown. Please select one of the options from " \
                           "the menu.\n"
            expected_str += "Error: \"a\" unknown. Please select one of the options from " \
                            "the menu.\n"
            expected_str += "Error: \"dict\" unknown. Please select one of the options from " \
                            "the menu.\n"
            expected_str += "Error: \"x\" unknown. Please select one of the options from " \
                            "the menu.\n"
            expected_str += "Error: \"z\" unknown. Please select one of the options from " \
                            "the menu.\n"
            expected_str += "Error: \"list\" unknown. Please select one of the options " \
                            "from the menu.\n"
            assert capsys.readouterr().out == expected_str

    def test24_input_parameter_data(self):
        """!
        @brief Test _input_parameter_data(), simple as all the sub
               functions have already been tested
        """
        def test_mock_in(prompt:str)->str:
            if prompt == "Enter parameter name: ":
                return "paramName"
            if prompt == "Enter parameter base type [T(ext)|i(nteger)|" \
                           "u(nsigned)|s(ize)|c(ustom)]: ":
                return "i"
            if prompt == "Enter brief parameter description for doxygen comment: ":
                return "Brief parameter description"
            return "n"

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()
            param_dict = testobj._input_parameter_data()
            assert isinstance(param_dict, dict)
            assert len(param_dict) == 4
            assert ParamRetDict.get_param_type(param_dict) == "integer"
            assert ParamRetDict.get_param_name(param_dict) == "paramName"
            assert ParamRetDict.get_param_desc(param_dict) == "Brief parameter description"
            assert ParamRetDict.get_param_type_mod(param_dict) == 0

    def test25_input_return_data(self):
        """!
        @brief Test _input_return_data(), simple as all the sub functions have already been tested
        """
        def test_mock_in(prompt:str)->str:
            if prompt == "Enter return base type [T(ext)|i(nteger)|u(nsigned)|s(ize)|c(ustom)]: ":
                retstr = "t"
            elif prompt == "Enter brief description of the return value for doxygen comment: ":
                retstr = "Brief return data description"
            else:
                retstr = "n"
            return retstr

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()
            return_dict = testobj._input_return_data()
            assert isinstance(return_dict, dict)
            assert len(return_dict) == 3
            assert ParamRetDict.get_return_type(return_dict) == "string"
            assert ParamRetDict.get_return_desc(return_dict) == "Brief return data description"
            assert ParamRetDict.get_return_type_mod(return_dict) == 0

    def test26_validate_translate_string_pass(self):
        """!
        @brief Test _validate_translate_string method
        """
        testobj = StringClassDescription(self.test_json)
        param_list = [ParamRetDict.build_param_dict_with_mod("foo", "string", "Test param one")]
        tststr = 'Test string with input @foo@'
        valid, match_count, param_count, str_data = testobj._validate_translate_string(param_list,
                                                                                       tststr)
        assert valid
        assert match_count == 1
        assert param_count == 1
        assert isinstance(str_data, list)
        assert len(str_data) == 2
        assert str_data[0][0] == TransTxtParser.parsed_type_text
        assert str_data[0][1] == "Test string with input "
        assert str_data[1][0] == TransTxtParser.parsed_type_param
        assert str_data[1][1] == "foo"

    def test27_validate_translate_string_pass_two(self):
        """!
        @brief Test _validate_translate_string method
        """
        testobj = StringClassDescription(self.test_json)
        param_list = [ParamRetDict.build_param_dict_with_mod("foo", "string", "Test param one"),
                     ParamRetDict.build_param_dict_with_mod("moo", "string", "Test param two")]
        tststr = 'Test string with input @foo@ and @moo@'
        valid, mcount, pcount, str_data = testobj._validate_translate_string(param_list,
                                                                             tststr)
        assert valid
        assert mcount == 2
        assert pcount == 2
        assert isinstance(str_data, list)
        assert len(str_data) == 4
        assert str_data[0][0] == TransTxtParser.parsed_type_text
        assert str_data[0][1] == "Test string with input "
        assert str_data[1][0] == TransTxtParser.parsed_type_param
        assert str_data[1][1] == "foo"
        assert str_data[2][0] == TransTxtParser.parsed_type_text
        assert str_data[2][1] == " and "
        assert str_data[3][0] == TransTxtParser.parsed_type_param
        assert str_data[3][1] == "moo"

    def test28_validate_translate_string_fail(self):
        """!
        @brief Test _validate_translate_string method
        """
        testobj = StringClassDescription(self.test_json)
        param_list = [ParamRetDict.build_param_dict_with_mod("foo", "string", "Test param one"),
                     ParamRetDict.build_param_dict_with_mod("moo", "string", "Test param two")]
        tststr = 'Test string with input @foo@'
        valid, mcount, pcount, str_data = testobj._validate_translate_string(param_list,
                                                                             tststr)
        assert not valid
        assert mcount == 1
        assert pcount == 1
        assert isinstance(str_data, list)
        assert len(str_data) == 2
        assert str_data[0][0] == TransTxtParser.parsed_type_text
        assert str_data[0][1] == "Test string with input "
        assert str_data[1][0] == TransTxtParser.parsed_type_param
        assert str_data[1][1] == "foo"

    def test29_validate_translate_string_fail_too_many(self):
        """!
        @brief Test _validate_translate_string method
        """
        testobj = StringClassDescription(self.test_json)
        param_list = [ParamRetDict.build_param_dict_with_mod("foo", "string", "Test param one")]
        tststr = 'Test string with input @foo@ and @moo@'
        valid, mcount, pcount, str_data = testobj._validate_translate_string(param_list,
                                                                             tststr)
        assert not valid
        assert mcount == 1
        assert pcount == 2
        assert isinstance(str_data, list)
        assert len(str_data) == 4
        assert str_data[0][0] == TransTxtParser.parsed_type_text
        assert str_data[0][1] == "Test string with input "
        assert str_data[1][0] == TransTxtParser.parsed_type_param
        assert str_data[1][1] == "foo"
        assert str_data[2][0] == TransTxtParser.parsed_type_text
        assert str_data[2][1] == " and "
        assert str_data[3][0] == TransTxtParser.parsed_type_param
        assert str_data[3][1] == "moo"

    def test30_input_translate_string_good(self,capsys):
        """!
        @brief Test _input_translate_string method, proper message
        """
        with patch('builtins.input', return_value='Test string with input @foo@'):
            testobj = StringClassDescription(self.test_json)
            param_list = [ParamRetDict.build_param_dict_with_mod("foo",
                                                                 "string",
                                                                 "Test param one")]
            parsed_str_data = testobj._input_translate_string(param_list)
            assert isinstance(parsed_str_data, list)
            assert len(parsed_str_data) == 2
            assert parsed_str_data[0][0] == TransTxtParser.parsed_type_text
            assert parsed_str_data[0][1] == "Test string with input "
            assert parsed_str_data[1][0] == TransTxtParser.parsed_type_param
            assert parsed_str_data[1][1] == "foo"

            expected_str = "Enter translation template string. Use @paramName@ in the string " \
                           "to indicate\n"
            expected_str += "where the function parameters should be inserted.\n"
            expected_str += "Example with single input parameter name \"keyString\":\n"
            expected_str += "  Found argument key @keyString@\n"
            assert capsys.readouterr().out == expected_str

    def test31_input_translate_string_with_too_many_error(self, capsys):
        """!
        @brief Test _input_translate_string method, improper message, too many params
        """
        input_str = (text for text in ["Test string with input @foo@ and @moo@",
                                       "Test string with input @foo@"])
        def test_mock_in(_:str)->str:
            return next(input_str)

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription(self.test_json)
            param_list = [ParamRetDict.build_param_dict_with_mod("foo", "string", "Test param one")]
            parsed_str_data = testobj._input_translate_string(param_list)
            assert isinstance(parsed_str_data, list)
            assert len(parsed_str_data) == 2

            expected_str = "Enter translation template string. Use @paramName@ in the string" \
                           " to indicate\n"
            expected_str += "where the function parameters should be inserted.\n"
            expected_str += "Example with single input parameter name \"keyString\":\n"
            expected_str += "  Found argument key @keyString@\n"

            expected_str += "Error: Too many template parameters in input string, expected 1 " \
                            "found 2\n"
            expected_str += "User input template:\n"
            expected_str += "    Test string with input @foo@ and @moo@\n"
            expected_str += "Expected parameter list:\n"
            expected_str += "    @foo@\n"
            assert capsys.readouterr().out == expected_str


    def test32_input_translate_string_with_too_few_error(self, capsys):
        """!
        @brief Test _input_translate_string method, improper message
        """
        input_str = (text for text in ["Test string with input @foo@",
                                       "Test string with input @foo@ and @moo@"])
        def test_mock_in(_:str)->str:
            return next(input_str)

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription(self.test_json)
            param_list = [ParamRetDict.build_param_dict_with_mod("foo", "string", "Test param one"),
                         ParamRetDict.build_param_dict_with_mod("moo", "integer", "Test param two")]
            parsed_str_data = testobj._input_translate_string(param_list)
            assert isinstance(parsed_str_data, list)
            assert len(parsed_str_data) == 4

            expected_str = "Enter translation template string. Use @paramName@ in the string" \
                           " to indicate\n"
            expected_str += "where the function parameters should be inserted.\n"
            expected_str += "Example with single input parameter name \"keyString\":\n"
            expected_str += "  Found argument key @keyString@\n"

            expected_str += "Error: Template parameter missing, found 1 of 2 expected " \
                            "template parameters.\n"
            expected_str += "User input template:\n"
            expected_str += "    Test string with input @foo@\n"
            expected_str += "Expected parameter list:\n"
            expected_str += "    @foo@, @moo@\n"
            assert capsys.readouterr().out == expected_str

    def test33_input_translate_string_with_misspell_error(self, capsys):
        """!
        @brief Test _input_translate_string method, improper message
        """
        input_str = (text for text in ["Test string with input @goo@ and @moo@",
                                      "Test string with input @foo@ and @goo@",
                                      "Test string with input @doo@ and @goo@",
                                      "Test string with input @foo@ and @moo@"])
        def test_mock_in(_:str)->str:
            return next(input_str)

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription(self.test_json)
            param_list = [ParamRetDict.build_param_dict_with_mod("foo", "string", "Test param one"),
                         ParamRetDict.build_param_dict_with_mod("moo", "integer", "Test param two")]
            parsed_str_data = testobj._input_translate_string(param_list)
            assert isinstance(parsed_str_data, list)
            assert len(parsed_str_data) == 4

            expected_str = "Enter translation template string. Use @paramName@ in the string" \
                           " to indicate\n"
            expected_str += "where the function parameters should be inserted.\n"
            expected_str += "Example with single input parameter name \"keyString\":\n"
            expected_str += "  Found argument key @keyString@\n"

            expected_str += "Error: Template parameter(s) misspelled, spelling error count 1\n"
            expected_str += "User input template:\n"
            expected_str += "    Test string with input @goo@ and @moo@\n"
            expected_str += "Expected parameter list:\n"
            expected_str += "    @foo@, @moo@\n"
            expected_str += "Error: Template parameter(s) misspelled, spelling error count 1\n"
            expected_str += "User input template:\n"
            expected_str += "    Test string with input @foo@ and @goo@\n"
            expected_str += "Expected parameter list:\n"
            expected_str += "    @foo@, @moo@\n"
            expected_str += "Error: Template parameter(s) misspelled, spelling error count 2\n"
            expected_str += "User input template:\n"
            expected_str += "    Test string with input @doo@ and @goo@\n"
            expected_str += "Expected parameter list:\n"
            expected_str += "    @foo@, @moo@\n"
            assert capsys.readouterr().out == expected_str

    def test34_input_translate_string_with_double_param_error(self, capsys):
        """!
        @brief Test _input_translate_string method, improper message
        """
        input_str = (text for text in ["Test string with input @foo@, @foo@ and @moo@",
                                      "Test string with input @foo@ and @moo@"])
        def test_mock_in(_:str)->str:
            return next(input_str)

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription(self.test_json)
            param_list = [ParamRetDict.build_param_dict_with_mod("foo", "string", "Test param one"),
                         ParamRetDict.build_param_dict_with_mod("moo", "integer", "Test param two")]
            parsed_str_data = testobj._input_translate_string(param_list)
            assert isinstance(parsed_str_data, list)
            assert len(parsed_str_data) == 4

            expected_str = "Enter translation template string. Use @paramName@ in the string" \
                           " to indicate\n"
            expected_str += "where the function parameters should be inserted.\n"
            expected_str += "Example with single input parameter name \"keyString\":\n"
            expected_str += "  Found argument key @keyString@\n"

            expected_str += "Error: Translation template parameter list does not match " \
                            "expected.\n"
            expected_str += "   Found 3 parameters of expected 2 parameters in string.\n"
            expected_str += "   Matched 3 parameters of expected 2 parameters in string.\n"
            expected_str += "User input template:\n"
            expected_str += "    Test string with input @foo@, @foo@ and @moo@\n"
            expected_str += "Expected parameter list:\n"
            expected_str += "    @foo@, @moo@\n"
            assert capsys.readouterr().out == expected_str

    def test35_input_param_return_type_good_input_float(self, capsys):
        """!
        @brief Test _input_param_return_type(), good input, text
        """
        type_list = ["f", "F", "float", "FLOAT", "Float"]
        input_list = []
        for element in type_list:
            input_list.append(element)
            input_list.append(element)

        input_str = (text for text in input_list)
        def test_mock_in(prompt:str)->str:
            return Test02StringClassDescription.mock_param_ret_input(prompt, input_str)

        with patch('builtins.input', test_mock_in):
            testobj = StringClassDescription()
            for _ in range(0,len(type_list)):
                type_name, type_mod = testobj._input_param_return_type(True)
                assert type_name == 'float'
                assert type_mod == 0

                type_name, type_mod = testobj._input_param_return_type(False)
                assert type_name == 'float'
                assert type_mod == 0

            assert capsys.readouterr().out == ""

# pylint: enable=protected-access
