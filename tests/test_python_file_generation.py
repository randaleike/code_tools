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


from datetime import datetime

from code_tools_grocsoftware.base.param_return_tools import ParamRetDict
from code_tools_grocsoftware.python_gen.file_gen_base import GeneratePythonFileHelper

class Test01CppFilehelper:
    """!
    @brief Unit test for the GeneratePythonFileHelper class
    """
    def test01_constructor(self):
        """!
        @brief Test the constructor
        """
        helper = GeneratePythonFileHelper()

        assert helper.copyright_generator is not None
        assert helper.eula is not None
        assert helper.doxy_comment_gen is not None
        assert helper.header_comment_gen is not None
        assert helper.level_tab_size == 4

        assert len(list(helper.type_xlation_dict.keys())) == 7
        assert helper.type_xlation_dict['string'] == "str"
        assert helper.type_xlation_dict['text'] == "str"
        assert helper.type_xlation_dict['size'] == "int"
        assert helper.type_xlation_dict['integer'] == "int"
        assert helper.type_xlation_dict['unsigned'] == "int"
        assert helper.type_xlation_dict['structure'] == "dict"
        assert helper.type_xlation_dict['tuple'] == "tuple"

        helper = GeneratePythonFileHelper("GNU_V11")

        assert helper.copyright_generator is not None
        assert helper.eula is not None
        assert helper.doxy_comment_gen is not None
        assert helper.header_comment_gen is not None
        assert helper.level_tab_size == 4

        assert len(list(helper.type_xlation_dict.keys())) == 7
        assert helper.type_xlation_dict['string'] == "str"
        assert helper.type_xlation_dict['text'] == "str"
        assert helper.type_xlation_dict['size'] == "int"
        assert helper.type_xlation_dict['integer'] == "int"
        assert helper.type_xlation_dict['unsigned'] == "int"
        assert helper.type_xlation_dict['structure'] == "dict"
        assert helper.type_xlation_dict['tuple'] == "tuple"

    def test02_declare_type_base(self):
        """!
        @brief Test the _declare_type method, no modification
        """
        helper = GeneratePythonFileHelper()

        # Test the xlate path
        assert helper._declare_type('string') == "str"
        assert helper._declare_type('text') == "str"
        assert helper._declare_type('size') == "int"
        assert helper._declare_type('integer') == "int"
        assert helper._declare_type('unsigned') == "int"
        assert helper._declare_type('structure') == "dict"
        assert helper._declare_type('tuple') == "tuple"

        # Test the non-xlate pathGN
        assert helper._declare_type('MyClass') == "MyClass"

    def test03_declare_type_ptr(self):
        """!
        @brief Test the _declare_type method, pointer modification
        """
        helper = GeneratePythonFileHelper()

        # Test the xlate path
        assert helper._declare_type('string', ParamRetDict.type_mod_ptr) == "str"
        assert helper._declare_type('text', ParamRetDict.type_mod_ptr) == "str"
        assert helper._declare_type('size', ParamRetDict.type_mod_ptr) == "int"
        assert helper._declare_type('integer', ParamRetDict.type_mod_ptr) == "int"
        assert helper._declare_type('unsigned', ParamRetDict.type_mod_ptr) == "int"
        assert helper._declare_type('structure', ParamRetDict.type_mod_ptr) == "dict"
        assert helper._declare_type('tuple', ParamRetDict.type_mod_ptr) == "tuple"

    def test04_declare_type_ref(self):
        """!
        @brief Test the _declare_type method, pointer modification
        """
        helper = GeneratePythonFileHelper()

        # Test the xlate path
        assert helper._declare_type('string', ParamRetDict.type_mod_ref) == "str"
        assert helper._declare_type('text', ParamRetDict.type_mod_ref) == "str"
        assert helper._declare_type('size', ParamRetDict.type_mod_ref) == "int"
        assert helper._declare_type('integer', ParamRetDict.type_mod_ref) == "int"
        assert helper._declare_type('unsigned', ParamRetDict.type_mod_ref) == "int"
        assert helper._declare_type('structure', ParamRetDict.type_mod_ref) == "dict"
        assert helper._declare_type('tuple', ParamRetDict.type_mod_ref) == "tuple"

    def test05_declare_type_list(self):
        """!
        @brief Test the _declare_type method, list modification
        """
        helper = GeneratePythonFileHelper()

        # Test the xlate path
        assert helper._declare_type('string', ParamRetDict.type_mod_list) == "list"
        assert helper._declare_type('text', ParamRetDict.type_mod_list) == "list"
        assert helper._declare_type('size', ParamRetDict.type_mod_list) == "list"
        assert helper._declare_type('integer', ParamRetDict.type_mod_list) == "list"
        assert helper._declare_type('unsigned', ParamRetDict.type_mod_list) == "list"
        assert helper._declare_type('structure', ParamRetDict.type_mod_list) == "list"
        assert helper._declare_type('tuple', ParamRetDict.type_mod_list) == "list"

    def test06_declare_type_list_ptr(self):
        """!
        @brief Test the _declare_type method, list and pointer modification
        """
        helper = GeneratePythonFileHelper()

        # Test the xlate path
        typemod = ParamRetDict.type_mod_list | ParamRetDict.type_mod_ptr
        assert helper._declare_type('string', typemod) == "list"
        assert helper._declare_type('text', typemod) == "list"
        assert helper._declare_type('size', typemod) == "list"
        assert helper._declare_type('integer', typemod) == "list"
        assert helper._declare_type('unsigned', typemod) == "list"
        assert helper._declare_type('structure', typemod) == "list"
        assert helper._declare_type('tuple', typemod) == "list"

    def test07_declare_type_list_ref(self):
        """!
        @brief Test the _declare_type method, list and reference modification
        """
        helper = GeneratePythonFileHelper()

        # Test the xlate path
        typemod = ParamRetDict.type_mod_list | ParamRetDict.type_mod_ref
        assert helper._declare_type('string', typemod) == "list"
        assert helper._declare_type('text', typemod) == "list"
        assert helper._declare_type('size', typemod) == "list"
        assert helper._declare_type('integer', typemod) == "list"
        assert helper._declare_type('unsigned', typemod) == "list"
        assert helper._declare_type('structure', typemod) == "list"
        assert helper._declare_type('tuple', typemod) == "list"

    def test08_declare_type_array(self):
        """!
        @brief Test the _declare_type method, array modification
        """
        helper = GeneratePythonFileHelper()

        # Test the xlate path
        assert helper._declare_type('string', 5 << ParamRetDict.type_mod_array_shift) == "list"
        assert helper._declare_type('text', 7 << ParamRetDict.type_mod_array_shift) == "list"
        assert helper._declare_type('size', 10 << ParamRetDict.type_mod_array_shift) == "list"
        assert helper._declare_type('integer', 20 << ParamRetDict.type_mod_array_shift) == "list"
        assert helper._declare_type('unsigned', 13 << ParamRetDict.type_mod_array_shift) == "list"
        assert helper._declare_type('structure', 12 << ParamRetDict.type_mod_array_shift) == "list"
        assert helper._declare_type('tuple', 14 << ParamRetDict.type_mod_array_shift) == "list"

    def test09_declare_type_array_ptr(self):
        """!
        @brief Test the _declare_type method, array and pointer modification
        """
        helper = GeneratePythonFileHelper()

        # Test the xlate path
        typemod = (8 << ParamRetDict.type_mod_array_shift) | ParamRetDict.type_mod_ptr
        assert helper._declare_type('string', typemod) == "list"
        assert helper._declare_type('text', typemod) == "list"
        assert helper._declare_type('size', typemod) == "list"
        assert helper._declare_type('integer', typemod) == "list"
        assert helper._declare_type('unsigned', typemod) == "list"
        assert helper._declare_type('structure', typemod) == "list"
        assert helper._declare_type('tuple', typemod) == "list"

    def test10_declare_type_array_ref(self):
        """!
        @brief Test the _declare_type method, array and reference modification
        """
        helper = GeneratePythonFileHelper()

        # Test the xlate path
        typemod = (8 << ParamRetDict.type_mod_array_shift) | ParamRetDict.type_mod_ref
        assert helper._declare_type('string', typemod) == "list"
        assert helper._declare_type('text', typemod) == "list"
        assert helper._declare_type('size', typemod) == "list"
        assert helper._declare_type('integer', typemod) == "list"
        assert helper._declare_type('unsigned', typemod) == "list"
        assert helper._declare_type('structure', typemod) == "list"
        assert helper._declare_type('tuple', typemod) == "list"

    def test11_declare_type_undef(self):
        """!
        @brief Test the _declare_type method, all with undef modification
        """
        helper = GeneratePythonFileHelper()

        # Test the xlate path
        assert helper._declare_type('string', ParamRetDict.type_mod_undef) == "str|None"

        typemod = ParamRetDict.type_mod_undef | ParamRetDict.type_mod_ptr
        assert helper._declare_type('string', typemod) == "str|None"

        typemod = ParamRetDict.type_mod_undef | ParamRetDict.type_mod_ref
        assert helper._declare_type('string', typemod) == "str|None"

        typemod = (8 << ParamRetDict.type_mod_array_shift) | ParamRetDict.type_mod_undef
        assert helper._declare_type('string', typemod) == "list|None"

        typemod = ParamRetDict.type_mod_undef | ParamRetDict.type_mod_list
        assert helper._declare_type('string', typemod) == "list|None"

        typemod = (25 << ParamRetDict.type_mod_array_shift) | ParamRetDict.type_mod_undef | ParamRetDict.type_mod_ptr
        assert helper._declare_type('string', typemod) == "list|None"

        typemod = (7 << ParamRetDict.type_mod_array_shift) | ParamRetDict.type_mod_undef | ParamRetDict.type_mod_ref
        assert helper._declare_type('string', typemod) == "list|None"

        typemod = ParamRetDict.type_mod_undef | ParamRetDict.type_mod_list
        assert helper._declare_type('string', typemod) == "list|None"

        typemod = ParamRetDict.type_mod_undef | ParamRetDict.type_mod_list | ParamRetDict.type_mod_ptr
        assert helper._declare_type('string', typemod) == "list|None"

        typemod = ParamRetDict.type_mod_undef | ParamRetDict.type_mod_list | ParamRetDict.type_mod_ref
        assert helper._declare_type('string', typemod) == "list|None"

    def test12_xlate_param_list(self):
        """!
        @brief Test the _xlate_params method
        """
        helper = GeneratePythonFileHelper()
        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo", "size", "mysize", ParamRetDict.type_mod_ptr))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("goo", "string", "mystr", ParamRetDict.type_mod_list))

        xlate_list = helper._xlate_params(gen_param_list)
        assert len(xlate_list) == len(gen_param_list)
        assert ParamRetDict.get_param_name(xlate_list[0]) == ParamRetDict.get_param_name(gen_param_list[0])
        assert ParamRetDict.get_param_type(xlate_list[0]) == "int"
        assert ParamRetDict.get_param_desc(xlate_list[0]) == ParamRetDict.get_param_desc(gen_param_list[0])
        assert ParamRetDict.get_param_type_mod(xlate_list[0]) == 0

        assert ParamRetDict.get_param_name(xlate_list[1]) == ParamRetDict.get_param_name(gen_param_list[1])
        assert ParamRetDict.get_param_type(xlate_list[1]) == "int"
        assert ParamRetDict.get_param_desc(xlate_list[1]) == ParamRetDict.get_param_desc(gen_param_list[1])
        assert ParamRetDict.get_param_type_mod(xlate_list[1]) == 0

        assert ParamRetDict.get_param_name(xlate_list[2]) == ParamRetDict.get_param_name(gen_param_list[2])
        assert ParamRetDict.get_param_type(xlate_list[2]) == "list"
        assert ParamRetDict.get_param_desc(xlate_list[2]) == ParamRetDict.get_param_desc(gen_param_list[2])
        assert ParamRetDict.get_param_type_mod(xlate_list[2]) == 0

    def test13_xlate_param_empty_list(self):
        """!
        @brief Test the _xlate_params method, empty list input
        """
        helper = GeneratePythonFileHelper()
        gen_param_list = []
        xlate_list = helper._xlate_params(gen_param_list)
        assert len(xlate_list) == 0

    def test14_xlate_ret_dict(self):
        """!
        @brief Test the _xlate_return_dict method
        """
        helper = GeneratePythonFileHelper()
        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "myint", 0)

        xlated_ret = helper._xlate_return_dict(gen_ret_dict)
        assert ParamRetDict.get_return_type(xlated_ret) == "int"
        assert ParamRetDict.get_param_desc(xlated_ret) == ParamRetDict.get_param_desc(gen_ret_dict)
        assert ParamRetDict.get_param_type_mod(gen_ret_dict) == 0

    def test15_xlate_ret_dict_none(self):
        """!
        @brief Test the _xlate_return_dict method, with no input
        """
        helper = GeneratePythonFileHelper()
        xlated_ret = helper._xlate_return_dict(None)
        assert xlated_ret is None

    def test16_gen_return_type(self):
        """!
        @brief Test the _gen_function_ret_type method
        """
        helper = GeneratePythonFileHelper()

        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "myint", 0)
        return_text = helper._gen_function_ret_type(gen_ret_dict)
        assert return_text == " -> int:"

        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "myint", ParamRetDict.type_mod_list)
        return_text = helper._gen_function_ret_type(gen_ret_dict)
        assert return_text == " -> list:"

    def test17_gen_return_type(self):
        """!
        @brief Test the _gen_function_ret_type method, with none input
        """
        helper = GeneratePythonFileHelper()

        return_text = helper._gen_function_ret_type(None)
        assert return_text == ":"

    def test18_gen_function_params(self):
        """!
        @brief Test the _gen_function_params method
        """
        helper = GeneratePythonFileHelper()
        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo", "size", "mysize", ParamRetDict.type_mod_ptr))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("goo", "string", "mystr", ParamRetDict.type_mod_list))

        return_text = helper._gen_function_params(gen_param_list)
        assert return_text == "(foo:int, moo:int, goo:list)"

    def test19_gen_function_params_empty(self):
        """!
        @brief Test the _gen_function_params method, empty list
        """
        helper = GeneratePythonFileHelper()
        gen_param_list = []
        return_text = helper._gen_function_params(gen_param_list)
        assert return_text == "()"

    def test20_declare_function(self):
        """!
        @brief Test the _declare_function_with_decorations method, no decorations
        """
        helper = GeneratePythonFileHelper()
        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return int", 0)

        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo", "size", "mysize", ParamRetDict.type_mod_ptr))

        function_text = helper._declare_function_with_decorations("my_test", "My test function", gen_param_list, gen_ret_dict)
        assert len(function_text) == 10
        assert function_text[0] == '    def my_test(foo:int, moo:int) -> int:\n'
        assert function_text[1] == '        """!\n'
        assert function_text[2] == '          @brief My test function\n'
        assert function_text[3] == '          \n'
        assert function_text[4] == '          @param foo {int} myint\n'
        assert function_text[5] == '          @param moo {int} mysize\n'
        assert function_text[6] == '          \n'
        assert function_text[7] == '          @return int - return int\n'
        assert function_text[8] == '        """\n'
        assert function_text[9] == '        ## @todo Implement code\n'

    def test21_declare_function_with_prefix(self):
        """!
        @brief Test the _declare_function_with_decorations method, prefix decoration
        """
        helper = GeneratePythonFileHelper()
        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return int", 0)

        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo", "size", "mysize", ParamRetDict.type_mod_ptr))

        function_text = helper._declare_function_with_decorations("my_test", "My test function", gen_param_list, gen_ret_dict, 8, prefix_decaration='@staticmethod')
        assert len(function_text) == 11
        assert function_text[0] == '        @staticmethod\n'
        assert function_text[1] == '        def my_test(foo:int, moo:int) -> int:\n'
        assert function_text[2] == '            """!\n'
        assert function_text[3] == '              @brief My test function\n'
        assert function_text[4] == '              \n'
        assert function_text[5] == '              @param foo {int} myint\n'
        assert function_text[6] == '              @param moo {int} mysize\n'
        assert function_text[7] == '              \n'
        assert function_text[8] == '              @return int - return int\n'
        assert function_text[9] == '            """\n'
        assert function_text[10] == '            ## @todo Implement code\n'

    def test22_declare_function_with_postfix(self):
        """!
        @brief Test the _declare_function_with_decorations method, postfix decoration
        """
        helper = GeneratePythonFileHelper()
        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return int", 0)

        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo", "size", "mysize", ParamRetDict.type_mod_ptr))

        function_text = helper._declare_function_with_decorations("my_test", "My test function", gen_param_list, gen_ret_dict, 8, postfix_decaration='const override')
        assert len(function_text) == 10
        assert function_text[0] == '        def my_test(foo:int, moo:int) -> int:\n'
        assert function_text[1] == '            """!\n'
        assert function_text[2] == '              @brief My test function\n'
        assert function_text[3] == '              \n'
        assert function_text[4] == '              @param foo {int} myint\n'
        assert function_text[5] == '              @param moo {int} mysize\n'
        assert function_text[6] == '              \n'
        assert function_text[7] == '              @return int - return int\n'
        assert function_text[8] == '            """\n'
        assert function_text[9] == '            ## @todo Implement code\n'


    def test23_declare_function_with_pre_and_postfix(self):
        """!
        @brief Test the _declare_function_with_decorations method, prefix, postfix decoration
        """
        helper = GeneratePythonFileHelper()
        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return int", 0)

        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo", "size", "mysize", ParamRetDict.type_mod_ptr))

        function_text = helper._declare_function_with_decorations("my_test", "My test function", gen_param_list, gen_ret_dict,
                                                              8, prefix_decaration="@staticmethod", postfix_decaration='const override')
        assert len(function_text) == 11
        assert function_text[0] == '        @staticmethod\n'
        assert function_text[1] == '        def my_test(foo:int, moo:int) -> int:\n'
        assert function_text[2] == '            """!\n'
        assert function_text[3] == '              @brief My test function\n'
        assert function_text[4] == '              \n'
        assert function_text[5] == '              @param foo {int} myint\n'
        assert function_text[6] == '              @param moo {int} mysize\n'
        assert function_text[7] == '              \n'
        assert function_text[8] == '              @return int - return int\n'
        assert function_text[9] == '            """\n'
        assert function_text[10] == '            ## @todo Implement code\n'

    def test24_declare_function_with_pre_and_postfix_no_comment(self):
        """!
        @brief Test the _declare_function_with_decorations method, prefix, postfix decoration, no comment
        """
        helper = GeneratePythonFileHelper()
        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return int", 0)

        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo", "size", "mysize", ParamRetDict.type_mod_ptr))

        function_text = helper._declare_function_with_decorations("my_test", "My test function", gen_param_list, gen_ret_dict,
                                                              8, True, "@staticmethod", 'const override')
        assert len(function_text) == 3
        assert function_text[0] == '        @staticmethod\n'
        assert function_text[1] == '        def my_test(foo:int, moo:int) -> int:\n'
        assert function_text[2] == '            ## @todo Implement code\n'

    def test25_declare_function_with_no_comment_inline_single_line(self):
        """!
        @brief Test the _declare_function_with_decorations method, no comment inline code
        """
        helper = GeneratePythonFileHelper()
        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return int", 0)

        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo", "size", "mysize", ParamRetDict.type_mod_ptr))

        function_text = helper._declare_function_with_decorations("my_test", "My test function", gen_param_list, gen_ret_dict,
                                                              8, True, "@staticmethod", 'const override', ["return 15"])
        assert len(function_text) == 3
        assert function_text[0] == '        @staticmethod\n'
        assert function_text[1] == '        def my_test(foo:int, moo:int) -> int:\n'
        assert function_text[2] == '            return 15\n'

    def test26_declare_function_with_no_comment_inline_multi_line(self):
        """!
        @brief Test the _declare_function_with_decorations method, no comment inline code
        """
        helper = GeneratePythonFileHelper()
        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return list", ParamRetDict.type_mod_list)

        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo", "size", "mysize", ParamRetDict.type_mod_ptr))

        inline_code =["retvar = []",
                     "retvar.append(15)",
                     "retvar.append(25)",
                     "return retvar"]

        function_text = helper._declare_function_with_decorations("my_test", "My test function", gen_param_list, gen_ret_dict,
                                                              8, True, inlinecode = inline_code)
        assert len(function_text) == 5
        assert function_text[0] == '        def my_test(foo:int, moo:int) -> list:\n'
        assert function_text[1] == '            '+inline_code[0]+'\n'
        assert function_text[2] == '            '+inline_code[1]+'\n'
        assert function_text[3] == '            '+inline_code[2]+'\n'
        assert function_text[4] == '            '+inline_code[3]+'\n'

    def test27_end_function(self):
        """!
        @brief Test the _end_function method
        """
        helper = GeneratePythonFileHelper()
        function_text = helper._end_function("my_test")
        assert function_text == '# end of function my_test\n'

    def test28_gen_file_header(self):
        """!
        @brief Test the _generate_generic_file_header method
        """
        helper = GeneratePythonFileHelper()
        current_year = datetime.now().year
        header_text = helper._generate_generic_file_header("unittest", current_year, "Me")
        copyright_msg = "# Copyright (c) "+str(current_year)+" Me"
        assert len(header_text) == 27
        assert header_text[0] == "#-------------------------------------------------------------------------------\n"
        assert header_text[1] == copyright_msg+"\n"
        assert header_text[3] == "# MIT License\n"
        assert header_text[24] == "# This file was autogenerated by unittest do not edit\n"
        assert header_text[26] == "#-------------------------------------------------------------------------------\n"

        min_text = helper._generate_generic_file_header("unittest")
        assert len(min_text) == 4
        assert min_text[0] == "#-------------------------------------------------------------------------------\n"
        assert min_text[1] == "# This file was autogenerated by unittest do not edit\n"
        assert min_text[2] == "# \n"
        assert min_text[3] == "#-------------------------------------------------------------------------------\n"

    def test29_gen_include(self):
        """!
        @brief Test the _gen_import method
        """
        helper = GeneratePythonFileHelper()

        include_text = helper._gen_import("MyImportClass", "import_module_name")
        assert include_text == "from import_module_name import MyImportClass\n"

        include_text = helper._gen_import("os")
        assert include_text == "import os\n"

    def test30_gen_include_block(self):
        """!
        @brief Test the _gen_importBlock method
        """
        helper = GeneratePythonFileHelper()
        include_list = [("re", None), ("datetime", "datetime"), ("MyImportClass", "import_module_name")]
        include_text = helper._gen_importBlock(include_list)
        assert len(include_text) == len(include_list) + 1
        assert include_text[0] == "// Imports\n"
        assert include_text[1] == "import re\n"
        assert include_text[2] == "from datetime import datetime\n"
        assert include_text[3] == "from import_module_name import MyImportClass\n"

    def test31_gen_open_namespace(self):
        """!
        @brief Test the _gen_namespace_open method
        """
        helper = GeneratePythonFileHelper()

        test_text = helper._gen_namespace_open("wonder")
        assert len(test_text) == 0

        test_text = helper._gen_namespace_open("boy")
        assert len(test_text) == 0

    def test32_gen_close_namespace(self):
        """!
        @brief Test the _gen_namespace_close method
        """
        helper = GeneratePythonFileHelper()

        test_text = helper._gen_namespace_close("wonder")
        assert len(test_text) == 0

        test_text = helper._gen_namespace_close("boy")
        assert len(test_text) == 0

    def test33_gen_using_namespace(self):
        """!
        @brief Test the _gen_using_namespace method
        """
        helper = GeneratePythonFileHelper()

        test_text = helper._gen_using_namespace("wonder")
        assert len(test_text) == 0

        test_text = helper._gen_using_namespace("boy")
        assert len(test_text) == 0

    def test34_gen_class_open(self):
        """!
        @brief Test the _gen_class_open method, no decorations
        """
        helper = GeneratePythonFileHelper()

        test_text = helper._gen_class_open("MyTestClassName", "My class description")
        assert len(test_text) == 4
        assert test_text[0] == "class MyTestClassName(object):\n"
        assert test_text[1] == '    """!\n'
        assert test_text[2] == "      @brief My class description\n"
        assert test_text[3] == '    """\n'

    def test35_gen_class_open_with_inheritence(self):
        """!
        @brief Test the _gen_class_open method, with inheritence
        """
        helper = GeneratePythonFileHelper()

        test_text = helper._gen_class_open("MyTestClassName", "My class description", "MyBaseClass")
        assert len(test_text) == 4
        assert test_text[0] == "class MyTestClassName(MyBaseClass):\n"
        assert test_text[1] == '    """!\n'
        assert test_text[2] == "      @brief My class description\n"
        assert test_text[3] == '    """\n'

    def test36_gen_class_open_decoration(self):
        """!
        @brief Test the _gen_class_open method, with decoration
        """
        helper = GeneratePythonFileHelper()

        test_text = helper._gen_class_open("MyTestClassName", "My class description", "MyBaseClass", "final", 2)
        assert len(test_text) == 4
        assert test_text[0] == "  class MyTestClassName(MyBaseClass):\n"
        assert test_text[1] == '      """!\n'
        assert test_text[2] == "        @brief My class description\n"
        assert test_text[3] == '      """\n'

    def test37_gen_class_close(self):
        """!
        @brief Test the _gen_class_close method, with inheritence
        """
        helper = GeneratePythonFileHelper()

        test_text = helper._gen_class_close("MyTestClassName")
        assert len(test_text) == 1
        assert test_text[0] == "# end of MyTestClassName class\n"

        test_text = helper._gen_class_close("MyTestClassName", 2)
        assert len(test_text) == 1
        assert test_text[0] == "  # end of MyTestClassName class\n"

    def test38_gen_class_default_construtor(self):
        """!
        @brief Test the _gen_class_default_constructor method
        """
        helper = GeneratePythonFileHelper()

        test_text = helper._gen_class_default_constructor("MyTestClassName")
        assert len(test_text) == 6
        assert test_text[0] == "    def __init__():\n"
        assert test_text[1] == '        """!\n'
        assert test_text[2] == "          @brief Construct a new MyTestClassName object\n"
        assert test_text[3] == '          \n'
        assert test_text[4] == '        """\n'
        assert test_text[5] == '    \n'

    def test39_gen_class_default_con_destrutor_no_doxy(self):
        """!
        @brief Test the _gen_class_default_constructor method, with no doxygen comments
        """
        helper = GeneratePythonFileHelper()

        test_text = helper._gen_class_default_constructor("MyTestClassName", no_doxy_comment_constructor=True)
        assert len(test_text) == 2
        assert test_text[0] == "    def __init__():\n"
        assert test_text[1] == '    \n'

    def test40_declare_struct_empty_list(self):
        """!
        @brief Test the _declare_structure method, No decorations, empty list
        """
        helper = GeneratePythonFileHelper()

        var_list = []
        test_text = helper._declare_structure("MyTestStructName", var_list, 0, "Test structure")
        assert len(test_text) == 5
        assert test_text[0] == "class MyTestStructName(object):\n"
        assert test_text[1] == '    """!\n'
        assert test_text[2] == "      @brief Test structure\n"
        assert test_text[3] == '    """\n'
        assert test_text[4] == '# end of MyTestStructName class\n'

    def test41_declare_struct(self):
        """!
        @brief Test the _declare_structure method, No decorations
        """
        helper = GeneratePythonFileHelper()

        member1 = ParamRetDict.build_param_dict_with_mod("foo", "integer", "Test integer", 0)
        member2 = ParamRetDict.build_param_dict_with_mod("moo", "unsigned", "Test unsigned", 0)
        var_list = [member1, member2]
        test_text = helper._declare_structure("MyTestStructName", var_list, 0, "Test structure")
        assert len(test_text) == 7
        assert test_text[0] == "class MyTestStructName(object):\n"
        assert test_text[1] == '    """!\n'
        assert test_text[2] == "      @brief Test structure\n"
        assert test_text[3] == '    """\n'
        assert test_text[4] == "    ## Test integer\n    foo:int\n"
        assert test_text[5] == "    ## Test unsigned\n    moo:int\n"
        assert test_text[6] == '# end of MyTestStructName class\n'

    def test42_declare_variable(self):
        """!
        @brief Test the _declare_var_statment method
        """
        helper = GeneratePythonFileHelper()
        member1 = ParamRetDict.build_param_dict_with_mod("foo", "integer", "Test integer", 0)
        member2 = ParamRetDict.build_param_dict_with_mod("moo", "unsigned", "Test unsigned", 0)
        member3 = ParamRetDict.build_param_dict_with_mod("goo", "string", "Test string", 0)

        test_text = helper._declare_var_statment(member1, 4)
        assert test_text == "    ## Test integer\n    foo:int\n"

        test_text = helper._declare_var_statment(member2, 8)
        assert test_text == "        ## Test unsigned\n        moo:int\n"

        test_text = helper._declare_var_statment(member3)
        assert test_text == "## Test string\ngoo:str\n"

    def test43_add_list_entry(self):
        """!
        @brief Test the _gen_add_list_statment method
        """
        helper = GeneratePythonFileHelper()
        test_text = helper._gen_add_list_statment("testList", "number", False)
        assert test_text == "testList.append(number)"
        test_text = helper._gen_add_list_statment("testList", "5", False)
        assert test_text == "testList.append(5)"

        test_text = helper._gen_add_list_statment("testList", "text", True)
        assert test_text == "testList.append(\"text\")"
        test_text = helper._gen_add_list_statment("testList", "AU", True)
        assert test_text == "testList.append(\"AU\")"

    def test44_generate_return(self):
        """!
        @brief Test the _gen_return_statment method
        """
        helper = GeneratePythonFileHelper()
        test_text = helper._gen_return_statment("number", False)
        assert test_text == "return number"
        test_text = helper._gen_return_statment("5", False)
        assert test_text == "return 5"

        test_text = helper._gen_return_statment("text", True)
        assert test_text == "return \"text\""
        test_text = helper._gen_return_statment("AU", True)
        assert test_text == "return \"AU\""

    def test49_define_function(self):
        """!
        @brief Test the _define_function_with_decorations method, no decarations
        """
        helper = GeneratePythonFileHelper()
        ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return value", 0)
        param_list = [ParamRetDict.build_param_dict_with_mod("foo", "unsigned", "Foo input", 0)]
        test_text = helper._define_function_with_decorations("MyDefineFunc", "Brief description", param_list, ret_dict)
        assert len(test_text) == 8
        assert test_text[0] == 'def MyDefineFunc(foo:int) -> int:\n'
        assert test_text[1] == '    """!\n'
        assert test_text[2] == '      @brief Brief description\n'
        assert test_text[3] == '      \n'
        assert test_text[4] == '      @param foo {int} Foo input\n'
        assert test_text[5] == '      \n'
        assert test_text[6] == '      @return int - return value\n'
        assert test_text[7] == '    """\n'

    def test50_define_function_with_pre_decoration(self):
        """!
        @brief Test the _define_function_with_decorations method, with prefix
        """
        helper = GeneratePythonFileHelper()
        ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return value", 0)
        param_list = [ParamRetDict.build_param_dict_with_mod("foo", "unsigned", "Foo input", 0)]
        test_text = helper._define_function_with_decorations("MyDefineFunc", "Brief description", param_list, ret_dict, False, "@static")
        assert len(test_text) == 9
        assert test_text[0] == '@static\n'
        assert test_text[1] == 'def MyDefineFunc(foo:int) -> int:\n'
        assert test_text[2] == '    """!\n'
        assert test_text[3] == '      @brief Brief description\n'
        assert test_text[4] == '      \n'
        assert test_text[5] == '      @param foo {int} Foo input\n'
        assert test_text[6] == '      \n'
        assert test_text[7] == '      @return int - return value\n'
        assert test_text[8] == '    """\n'

    def test51_define_function_with_post_decoration(self):
        """!
        @brief Test the _define_function_with_decorations method, with postfix
        """
        helper = GeneratePythonFileHelper()
        ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return value", 0)
        param_list = [ParamRetDict.build_param_dict_with_mod("foo", "unsigned", "Foo input", 0)]
        test_text = helper._define_function_with_decorations("MyDefineFunc", "Brief description", param_list, ret_dict, postfix_decaration="const")
        assert len(test_text) == 8
        assert test_text[0] == 'def MyDefineFunc(foo:int) -> int:\n'
        assert test_text[1] == '    """!\n'
        assert test_text[2] == '      @brief Brief description\n'
        assert test_text[3] == '      \n'
        assert test_text[4] == '      @param foo {int} Foo input\n'
        assert test_text[5] == '      \n'
        assert test_text[6] == '      @return int - return value\n'
        assert test_text[7] == '    """\n'

    def test52_define_function_with_pre_post_decoration(self):
        """!
        @brief Test the _define_function_with_decorations method, with prefix and postfix
        """
        helper = GeneratePythonFileHelper()
        ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return value", 0)
        param_list = [ParamRetDict.build_param_dict_with_mod("foo", "unsigned", "Foo input", 0)]
        test_text = helper._define_function_with_decorations("MyDefineFunc", "Brief description", param_list, ret_dict,
                                                         prefix_decaration="@static", postfix_decaration="const")
        assert len(test_text) == 9
        assert test_text[0] == '@static\n'
        assert test_text[1] == 'def MyDefineFunc(foo:int) -> int:\n'
        assert test_text[2] == '    """!\n'
        assert test_text[3] == '      @brief Brief description\n'
        assert test_text[4] == '      \n'
        assert test_text[5] == '      @param foo {int} Foo input\n'
        assert test_text[6] == '      \n'
        assert test_text[7] == '      @return int - return value\n'
        assert test_text[8] == '    """\n'

    def test53_define_function_no_comment(self):
        """!
        @brief Test the _define_function_with_decorations method, with no comment
        """
        helper = GeneratePythonFileHelper()
        ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return value", 0)
        param_list = [ParamRetDict.build_param_dict_with_mod("foo", "unsigned", "Foo input", 0)]
        test_text = helper._define_function_with_decorations("MyDefineFunc", "Brief description", param_list, ret_dict, True)
        assert len(test_text) == 1
        assert test_text[0] == 'def MyDefineFunc(foo:int) -> int:\n'

    def test54_define_function_empty_param_list(self):
        """!
        @brief Test the _define_function_with_decorations method, with empty param list
        """
        helper = GeneratePythonFileHelper()
        ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return value", 0)
        test_text = helper._define_function_with_decorations("MyDefineFunc", "Brief description", [], ret_dict, True)
        assert len(test_text) == 1
        assert test_text[0] == 'def MyDefineFunc() -> int:\n'

    def test55_gen_class_open_no_description(self):
        """!
        @brief Test the _gen_class_open method, with no description
        """
        helper = GeneratePythonFileHelper()

        test_text = helper._gen_class_open("MyTestClassName", None, "MyBaseClass", "final", 2)
        assert len(test_text) == 1
        assert test_text[0] == "  class MyTestClassName(MyBaseClass):\n"
