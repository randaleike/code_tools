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
from code_tools_grocsoftware.cpp_gen.file_gen_base import GenerateCppFileHelper


class Test01CppFilehelper:
    """!
    @brief Unit test for the GenerateCppFileHelper class
    """
    def test01_constructor(self):
        """!
        @brief Test the constructor
        """
        helper = GenerateCppFileHelper()

        assert helper.copyright_generator is not None
        assert helper.eula is not None
        assert helper.doxy_comment_gen is not None
        assert helper.header_comment_gen is not None
        assert helper.level_tab_size == 4

        assert len(list(helper.type_xlation_dict.keys())) == 6
        assert helper.type_xlation_dict['string'] == "std::string"
        assert helper.type_xlation_dict['text'] == "std::string"
        assert helper.type_xlation_dict['size'] == "size_t"
        assert helper.type_xlation_dict['integer'] == "int"
        assert helper.type_xlation_dict['unsigned'] == "unsigned"
        assert helper.type_xlation_dict['char'] == "char"

        helper = GenerateCppFileHelper("GNU_V11")

        assert helper.copyright_generator is not None
        assert helper.eula is not None
        assert helper.doxy_comment_gen is not None
        assert helper.header_comment_gen is not None
        assert helper.level_tab_size == 4

        assert len(list(helper.type_xlation_dict.keys())) == 6
        assert helper.type_xlation_dict['string'] == "std::string"
        assert helper.type_xlation_dict['text'] == "std::string"
        assert helper.type_xlation_dict['size'] == "size_t"
        assert helper.type_xlation_dict['integer'] == "int"
        assert helper.type_xlation_dict['unsigned'] == "unsigned"
        assert helper.type_xlation_dict['char'] == "char"

    def test02_declare_type_base(self):
        """!
        @brief Test the _declare_type method, no modification
        """
        helper = GenerateCppFileHelper()

        # Test the xlate path
        assert helper._declare_type('string') == "std::string"
        assert helper._declare_type('text') == "std::string"
        assert helper._declare_type('size') == "size_t"
        assert helper._declare_type('integer') == "int"
        assert helper._declare_type('unsigned') == "unsigned"

        # Test the non-xlate path
        assert helper._declare_type('MyClass') == "MyClass"

    def test03_declare_type_ptr(self):
        """!
        @brief Test the _declare_type method, pointer modification
        """
        helper = GenerateCppFileHelper()

        # Test the xlate path
        assert helper._declare_type('string', ParamRetDict.type_mod_ptr) == "std::string*"
        assert helper._declare_type('text', ParamRetDict.type_mod_ptr) == "std::string*"
        assert helper._declare_type('size', ParamRetDict.type_mod_ptr) == "size_t*"
        assert helper._declare_type('integer', ParamRetDict.type_mod_ptr) == "int*"
        assert helper._declare_type('unsigned', ParamRetDict.type_mod_ptr) == "unsigned*"

    def test04_declare_type_ref(self):
        """!
        @brief Test the _declare_type method, pointer modification
        """
        helper = GenerateCppFileHelper()

        # Test the xlate path
        assert helper._declare_type('string', ParamRetDict.type_mod_ref) == "std::string&"
        assert helper._declare_type('text', ParamRetDict.type_mod_ref) == "std::string&"
        assert helper._declare_type('size', ParamRetDict.type_mod_ref) == "size_t&"
        assert helper._declare_type('integer', ParamRetDict.type_mod_ref) == "int&"
        assert helper._declare_type('unsigned', ParamRetDict.type_mod_ref) == "unsigned&"

    def test05_declare_type_list(self):
        """!
        @brief Test the _declare_type method, list modification
        """
        helper = GenerateCppFileHelper()

        # Test the xlate path
        assert helper._declare_type('string', ParamRetDict.type_mod_list) == "std::list<std::string>"
        assert helper._declare_type('text', ParamRetDict.type_mod_list) == "std::list<std::string>"
        assert helper._declare_type('size', ParamRetDict.type_mod_list) == "std::list<size_t>"
        assert helper._declare_type('integer', ParamRetDict.type_mod_list) == "std::list<int>"
        assert helper._declare_type('unsigned', ParamRetDict.type_mod_list) == "std::list<unsigned>"

    def test06_declare_type_list_ptr(self):
        """!
        @brief Test the _declare_type method, list and pointer modification
        """
        helper = GenerateCppFileHelper()

        # Test the xlate path
        typemod = ParamRetDict.type_mod_list | ParamRetDict.type_mod_ptr
        assert helper._declare_type('string', typemod) == "std::list<std::string*>"
        assert helper._declare_type('text', typemod) == "std::list<std::string*>"
        assert helper._declare_type('size', typemod) == "std::list<size_t*>"
        assert helper._declare_type('integer', typemod) == "std::list<int*>"
        assert helper._declare_type('unsigned', typemod) == "std::list<unsigned*>"

    def test07_declare_type_list_ref(self):
        """!
        @brief Test the _declare_type method, list and reference modification
        """
        helper = GenerateCppFileHelper()

        # Test the xlate path
        typemod = ParamRetDict.type_mod_list | ParamRetDict.type_mod_ref
        assert helper._declare_type('string', typemod) == "std::list<std::string&>"
        assert helper._declare_type('text', typemod) == "std::list<std::string&>"
        assert helper._declare_type('size', typemod) == "std::list<size_t&>"
        assert helper._declare_type('integer', typemod) == "std::list<int&>"
        assert helper._declare_type('unsigned', typemod) == "std::list<unsigned&>"

    def test08_declare_type_array(self):
        """!
        @brief Test the _declare_type method, array modification
        """
        helper = GenerateCppFileHelper()

        # Test the xlate path
        assert helper._declare_type('string', 5 << ParamRetDict.type_mod_array_shift) == "std::array<std::string, 5>"
        assert helper._declare_type('text', 7 << ParamRetDict.type_mod_array_shift) == "std::array<std::string, 7>"
        assert helper._declare_type('size', 10 << ParamRetDict.type_mod_array_shift) == "std::array<size_t, 10>"
        assert helper._declare_type('integer', 20 << ParamRetDict.type_mod_array_shift) == "std::array<int, 20>"
        assert helper._declare_type('unsigned', 13 << ParamRetDict.type_mod_array_shift) == "std::array<unsigned, 13>"

    def test09_declare_type_array_ptr(self):
        """!
        @brief Test the _declare_type method, array and pointer modification
        """
        helper = GenerateCppFileHelper()

        # Test the xlate path
        typemod = (8 << ParamRetDict.type_mod_array_shift) | ParamRetDict.type_mod_ptr
        assert helper._declare_type('string', typemod) == "std::array<std::string*, 8>"
        assert helper._declare_type('text', typemod) == "std::array<std::string*, 8>"
        assert helper._declare_type('size', typemod) == "std::array<size_t*, 8>"
        assert helper._declare_type('integer', typemod) == "std::array<int*, 8>"
        assert helper._declare_type('unsigned', typemod) == "std::array<unsigned*, 8>"

    def test10_declare_type_array_ref(self):
        """!
        @brief Test the _declare_type method, array and reference modification
        """
        helper = GenerateCppFileHelper()

        # Test the xlate path
        typemod = (8 << ParamRetDict.type_mod_array_shift) | ParamRetDict.type_mod_ref
        assert helper._declare_type('string', typemod) == "std::array<std::string&, 8>"
        assert helper._declare_type('text', typemod) == "std::array<std::string&, 8>"
        assert helper._declare_type('size', typemod) == "std::array<size_t&, 8>"
        assert helper._declare_type('integer', typemod) == "std::array<int&, 8>"
        assert helper._declare_type('unsigned', typemod) == "std::array<unsigned&, 8>"

    def test11_declare_type_undef(self):
        """!
        @brief Test the _declare_type method, all with undef modification
        """
        helper = GenerateCppFileHelper()

        # Test the xlate path
        assert helper._declare_type('string', ParamRetDict.type_mod_undef) == "std::string"

        typemod = ParamRetDict.type_mod_undef | ParamRetDict.type_mod_ptr
        assert helper._declare_type('string', typemod) == "std::string*"

        typemod = ParamRetDict.type_mod_undef | ParamRetDict.type_mod_ref
        assert helper._declare_type('string', typemod) == "std::string&"

        typemod = (8 << ParamRetDict.type_mod_array_shift) | ParamRetDict.type_mod_undef
        assert helper._declare_type('string', typemod) == "std::array<std::string, 8>"

        typemod = ParamRetDict.type_mod_undef | ParamRetDict.type_mod_list
        assert helper._declare_type('string', typemod) == "std::list<std::string>"

        typemod = (25 << ParamRetDict.type_mod_array_shift) | ParamRetDict.type_mod_undef | ParamRetDict.type_mod_ptr
        assert helper._declare_type('string', typemod) == "std::array<std::string*, 25>"

        typemod = (7 << ParamRetDict.type_mod_array_shift) | ParamRetDict.type_mod_undef | ParamRetDict.type_mod_ref
        assert helper._declare_type('string', typemod) == "std::array<std::string&, 7>"

        typemod = ParamRetDict.type_mod_undef | ParamRetDict.type_mod_list
        assert helper._declare_type('string', typemod) == "std::list<std::string>"

        typemod = ParamRetDict.type_mod_undef | ParamRetDict.type_mod_list | ParamRetDict.type_mod_ptr
        assert helper._declare_type('string', typemod) == "std::list<std::string*>"

        typemod = ParamRetDict.type_mod_undef | ParamRetDict.type_mod_list | ParamRetDict.type_mod_ref
        assert helper._declare_type('string', typemod) == "std::list<std::string&>"

    def test12_xlate_param_list(self):
        """!
        @brief Test the _xlate_params method
        """
        helper = GenerateCppFileHelper()
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
        assert ParamRetDict.get_param_type(xlate_list[1]) == "size_t*"
        assert ParamRetDict.get_param_desc(xlate_list[1]) == ParamRetDict.get_param_desc(gen_param_list[1])
        assert ParamRetDict.get_param_type_mod(xlate_list[1]) == 0

        assert ParamRetDict.get_param_name(xlate_list[2]) == ParamRetDict.get_param_name(gen_param_list[2])
        assert ParamRetDict.get_param_type(xlate_list[2]) == "std::list<std::string>"
        assert ParamRetDict.get_param_desc(xlate_list[2]) == ParamRetDict.get_param_desc(gen_param_list[2])
        assert ParamRetDict.get_param_type_mod(xlate_list[2]) == 0

    def test13_xlate_param_empty_list(self):
        """!
        @brief Test the _xlate_params method, empty list input
        """
        helper = GenerateCppFileHelper()
        gen_param_list = []
        xlate_list = helper._xlate_params(gen_param_list)
        assert len(xlate_list) == 0

    def test14_xlate_ret_dict(self):
        """!
        @brief Test the _xlate_return_dict method
        """
        helper = GenerateCppFileHelper()
        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "myint", 0)

        xlated_ret = helper._xlate_return_dict(gen_ret_dict)
        assert ParamRetDict.get_return_type(xlated_ret) == "int"
        assert ParamRetDict.get_param_desc(xlated_ret) == ParamRetDict.get_param_desc(gen_ret_dict)
        assert ParamRetDict.get_param_type_mod(gen_ret_dict) == 0

    def test15_xlate_ret_dict_none(self):
        """!
        @brief Test the _xlate_return_dict method, with no input
        """
        helper = GenerateCppFileHelper()
        xlated_ret = helper._xlate_return_dict(None)
        assert xlated_ret is None

    def test16_gen_return_type(self):
        """!
        @brief Test the _gen_function_ret_type method
        """
        helper = GenerateCppFileHelper()

        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "myint", 0)
        return_text = helper._gen_function_ret_type(gen_ret_dict)
        assert return_text == "int "

        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "myint", ParamRetDict.type_mod_list)
        return_text = helper._gen_function_ret_type(gen_ret_dict)
        assert return_text == "std::list<int> "

    def test17_gen_return_type(self):
        """!
        @brief Test the _gen_function_ret_type method, with none input
        """
        helper = GenerateCppFileHelper()

        return_text = helper._gen_function_ret_type(None)
        assert return_text == ""

    def test18_gen_function_params(self):
        """!
        @brief Test the _gen_function_params method
        """
        helper = GenerateCppFileHelper()
        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo", "size", "mysize", ParamRetDict.type_mod_ptr))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("goo", "string", "mystr", ParamRetDict.type_mod_list))

        return_text = helper._gen_function_params(gen_param_list)
        assert return_text == "(int foo, size_t* moo, std::list<std::string> goo)"

    def test19_gen_function_params_empty(self):
        """!
        @brief Test the _gen_function_params method, empty list
        """
        helper = GenerateCppFileHelper()
        gen_param_list = []
        return_text = helper._gen_function_params(gen_param_list)
        assert return_text == "()"

    def test20_declare_function(self):
        """!
        @brief Test the _declare_function_with_decorations method, no decorations
        """
        helper = GenerateCppFileHelper()
        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return int", 0)

        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo", "size", "mysize", ParamRetDict.type_mod_ptr))

        function_text = helper._declare_function_with_decorations("my_test", "My test function", gen_param_list, gen_ret_dict)
        assert len(function_text) == 9
        assert function_text[0] == '/**\n'
        assert function_text[1] == ' * @brief My test function\n'
        assert function_text[2] == ' * \n'
        assert function_text[3] == ' * @param foo myint\n'
        assert function_text[4] == ' * @param moo mysize\n'
        assert function_text[5] == ' * \n'
        assert function_text[6] == ' * @return int - return int\n'
        assert function_text[7] == ' */\n'
        assert function_text[8] == 'int my_test(int foo, size_t* moo);\n'

    def test21_declare_function_with_prefix(self):
        """!
        @brief Test the _declare_function_with_decorations method, prefix decoration
        """
        helper = GenerateCppFileHelper()
        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return int", 0)

        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo", "size", "mysize", ParamRetDict.type_mod_ptr))

        function_text = helper._declare_function_with_decorations("my_test", "My test function", gen_param_list, gen_ret_dict, 8, prefix_decaration='virtual')
        assert len(function_text) == 9
        assert function_text[0] == '        /**\n'
        assert function_text[1] == '         * @brief My test function\n'
        assert function_text[2] == '         * \n'
        assert function_text[3] == '         * @param foo myint\n'
        assert function_text[4] == '         * @param moo mysize\n'
        assert function_text[5] == '         * \n'
        assert function_text[6] == '         * @return int - return int\n'
        assert function_text[7] == '         */\n'
        assert function_text[8] == '        virtual int my_test(int foo, size_t* moo);\n'

    def test22_declare_function_with_postfix(self):
        """!
        @brief Test the _declare_function_with_decorations method, postfix decoration
        """
        helper = GenerateCppFileHelper()
        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return int", 0)

        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo", "size", "mysize", ParamRetDict.type_mod_ptr))

        function_text = helper._declare_function_with_decorations("my_test", "My test function", gen_param_list, gen_ret_dict, 8, postfix_decaration='const override')
        assert len(function_text) == 9
        assert function_text[0] == '        /**\n'
        assert function_text[1] == '         * @brief My test function\n'
        assert function_text[2] == '         * \n'
        assert function_text[3] == '         * @param foo myint\n'
        assert function_text[4] == '         * @param moo mysize\n'
        assert function_text[5] == '         * \n'
        assert function_text[6] == '         * @return int - return int\n'
        assert function_text[7] == '         */\n'
        assert function_text[8] == '        int my_test(int foo, size_t* moo) const override;\n'

    def test23_declare_function_with_pre_and_postfix(self):
        """!
        @brief Test the _declare_function_with_decorations method, prefix, postfix decoration
        """
        helper = GenerateCppFileHelper()
        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return int", 0)

        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo", "size", "mysize", ParamRetDict.type_mod_ptr))

        function_text = helper._declare_function_with_decorations("my_test", "My test function", gen_param_list, gen_ret_dict,
                                                              8, prefix_decaration="[[nodiscard]]", postfix_decaration='const override')
        assert len(function_text) == 9
        assert function_text[0] == '        /**\n'
        assert function_text[1] == '         * @brief My test function\n'
        assert function_text[2] == '         * \n'
        assert function_text[3] == '         * @param foo myint\n'
        assert function_text[4] == '         * @param moo mysize\n'
        assert function_text[5] == '         * \n'
        assert function_text[6] == '         * @return int - return int\n'
        assert function_text[7] == '         */\n'
        assert function_text[8] == '        [[nodiscard]] int my_test(int foo, size_t* moo) const override;\n'

    def test24_declare_function_with_pre_and_postfix_no_comment(self):
        """!
        @brief Test the _declare_function_with_decorations method, prefix, postfix decoration, no comment
        """
        helper = GenerateCppFileHelper()
        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return int", 0)

        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo", "size", "mysize", ParamRetDict.type_mod_ptr))

        function_text = helper._declare_function_with_decorations("my_test", "My test function", gen_param_list, gen_ret_dict,
                                                              8, True, "[[nodiscard]]", 'const override')
        assert len(function_text) == 1
        assert function_text[0] == '        [[nodiscard]] int my_test(int foo, size_t* moo) const override;\n'

    def test25_declare_function_with_no_comment_inline_single_line(self):
        """!
        @brief Test the _declare_function_with_decorations method, no comment inline code
        """
        helper = GenerateCppFileHelper()
        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return int", 0)

        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo", "size", "mysize", ParamRetDict.type_mod_ptr))

        function_text = helper._declare_function_with_decorations("my_test", "My test function", gen_param_list, gen_ret_dict,
                                                              8, True, "[[nodiscard]]", 'const override', ["return 15;"])
        assert len(function_text) == 2
        assert function_text[0] == '        [[nodiscard]] int my_test(int foo, size_t* moo) const override\n'
        assert function_text[1] == '        {return 15;}\n'

    def test26_declare_function_with_no_comment_inline_multi_line(self):
        """!
        @brief Test the _declare_function_with_decorations method, no comment inline code
        """
        helper = GenerateCppFileHelper()
        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return list", ParamRetDict.type_mod_list)

        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo", "size", "mysize", ParamRetDict.type_mod_ptr))

        inline_code =["std::list<int> retvar;",
                     "retvar.push_back(15);",
                     "retvar.push_back(25);",
                     "return retvar;"]

        function_text = helper._declare_function_with_decorations("my_test", "My test function", gen_param_list, gen_ret_dict,
                                                              8, True, "[[nodiscard]]", 'const override', inline_code)
        assert len(function_text) == 7
        assert function_text[0] == '        [[nodiscard]] std::list<int> my_test(int foo, size_t* moo) const override\n'
        assert function_text[1] == '        {\n'
        assert function_text[2] == '            '+inline_code[0]+'\n'
        assert function_text[3] == '            '+inline_code[1]+'\n'
        assert function_text[4] == '            '+inline_code[2]+'\n'
        assert function_text[5] == '            '+inline_code[3]+'\n'
        assert function_text[6] == '        }\n'

    def test27_end_function(self):
        """!
        @brief Test the _end_function method
        """
        helper = GenerateCppFileHelper()
        function_text = helper._end_function("my_test")
        assert function_text == '} // end of my_test()\n'

    def test28_gen_file_header(self):
        """!
        @brief Test the _generate_generic_file_header method
        """
        helper = GenerateCppFileHelper()
        current_year = datetime.now().year
        header_text = helper._generate_generic_file_header("unittest", current_year, "Me")
        copyright_msg = "* Copyright (c) "+str(current_year)+" Me"
        assert len(header_text) == 27
        assert header_text[0] == "/*------------------------------------------------------------------------------\n"
        assert header_text[1] == copyright_msg+"\n"
        assert header_text[3] == "* MIT License\n"
        assert header_text[24] == "* This file was autogenerated by unittest do not edit\n"
        assert header_text[26] == "* ----------------------------------------------------------------------------*/\n"

        min_text = helper._generate_generic_file_header("unittest")
        assert len(min_text) == 4
        assert min_text[0] == "/*------------------------------------------------------------------------------\n"
        assert min_text[1] == "* This file was autogenerated by unittest do not edit\n"
        assert min_text[2] == "* \n"
        assert min_text[3] == "* ----------------------------------------------------------------------------*/\n"

    def test29_gen_include(self):
        """!
        @brief Test the _gen_include method
        """
        helper = GenerateCppFileHelper()

        include_text = helper._gen_include("test.h")
        assert include_text == "#include \"test.h\"\n"

        include_text = helper._gen_include("<test>")
        assert include_text == "#include <test>\n"

    def test30_gen_include_block(self):
        """!
        @brief Test the _gen_include_block method
        """
        helper = GenerateCppFileHelper()
        include_list = ["<stdlib>", "<test>", "test.h", "foo.h"]
        include_text = helper._gen_include_block(include_list)
        assert len(include_text) == len(include_list) + 1
        assert include_text[0] == "// Includes\n"
        assert include_text[1] == "#include <stdlib>\n"
        assert include_text[2] == "#include <test>\n"
        assert include_text[3] == "#include \"test.h\"\n"
        assert include_text[4] == "#include \"foo.h\"\n"

    def test31_gen_open_namespace(self):
        """!
        @brief Test the _gen_namespace_open method
        """
        helper = GenerateCppFileHelper()

        test_text = helper._gen_namespace_open("wonder")
        assert len(test_text) == 1
        assert test_text[0] == "namespace wonder {\n"

        test_text = helper._gen_namespace_open("boy")
        assert len(test_text) == 1
        assert test_text[0] == "namespace boy {\n"

    def test32_gen_close_namespace(self):
        """!
        @brief Test the _gen_namespace_close method
        """
        helper = GenerateCppFileHelper()

        test_text = helper._gen_namespace_close("wonder")
        assert len(test_text) == 1
        assert test_text[0] == "}; // end of namespace wonder\n"

        test_text = helper._gen_namespace_close("boy")
        assert len(test_text) == 1
        assert test_text[0] == "}; // end of namespace boy\n"

    def test33_gen_using_namespace(self):
        """!
        @brief Test the _gen_using_namespace method
        """
        helper = GenerateCppFileHelper()

        test_text = helper._gen_using_namespace("wonder")
        assert len(test_text) == 1
        assert test_text[0] == "using namespace wonder;\n"

        test_text = helper._gen_using_namespace("boy")
        assert len(test_text) == 1
        assert test_text[0] == "using namespace boy;\n"

    def test34_gen_class_open(self):
        """!
        @brief Test the _gen_class_open method, no decorations
        """
        helper = GenerateCppFileHelper()

        test_text = helper._gen_class_open("MyTestClassName", "My class description")
        assert len(test_text) == 5
        assert test_text[0] == "/**\n"
        assert test_text[1] == " * @brief My class description\n"
        assert test_text[2] == " */\n"
        assert test_text[3] == "class MyTestClassName\n"
        assert test_text[4] == "{\n"

    def test35_gen_class_open_with_inheritence(self):
        """!
        @brief Test the _gen_class_open method, with inheritence
        """
        helper = GenerateCppFileHelper()

        test_text = helper._gen_class_open("MyTestClassName", "My class description", "public MyBaseClass")
        assert len(test_text) == 5
        assert test_text[0] == "/**\n"
        assert test_text[1] == " * @brief My class description\n"
        assert test_text[2] == " */\n"
        assert test_text[3] == "class MyTestClassName : public MyBaseClass\n"
        assert test_text[4] == "{\n"

    def test36_gen_class_open_decoration(self):
        """!
        @brief Test the _gen_class_open method, with inheritence
        """
        helper = GenerateCppFileHelper()

        test_text = helper._gen_class_open("MyTestClassName", "My class description", "public MyBaseClass", "final", 2)
        assert len(test_text) == 5
        assert test_text[0] == "  /**\n"
        assert test_text[1] == "   * @brief My class description\n"
        assert test_text[2] == "   */\n"
        assert test_text[3] == "  class MyTestClassName final : public MyBaseClass\n"
        assert test_text[4] == "  {\n"

    def test37_gen_class_close(self):
        """!
        @brief Test the _gen_class_close method, with inheritence
        """
        helper = GenerateCppFileHelper()

        test_text = helper._gen_class_close("MyTestClassName")
        assert len(test_text) == 1
        assert test_text[0] == "}; // end of MyTestClassName class\n"

        test_text = helper._gen_class_close("MyTestClassName", 2)
        assert len(test_text) == 1
        assert test_text[0] == "  }; // end of MyTestClassName class\n"

    def test38_gen_class_default_con_destrutor(self):
        """!
        @brief Test the _gen_class_default_constructor_destructor method
        """
        helper = GenerateCppFileHelper()

        test_text = helper._gen_class_default_constructor_destructor("MyTestClassName")
        assert len(test_text) == 46
        assert test_text[0] == "        /**\n"
        assert test_text[1] == "         * @brief Construct a new MyTestClassName object\n"
        assert test_text[2] == "         * \n"
        assert test_text[3] == "         */\n"
        assert test_text[4] == "        MyTestClassName() = default;\n"
        assert test_text[5] == "\n"
        assert test_text[6] == "        /**\n"
        assert test_text[7] == "         * @brief Copy constructor for a new MyTestClassName object\n"
        assert test_text[8] == "         * \n"
        assert test_text[9] == "         * @param other Reference to object to copy\n"
        assert test_text[10] == "         * \n"
        assert test_text[11] == "         */\n"
        assert test_text[12] == "        MyTestClassName(const MyTestClassName& other) = default;\n"
        assert test_text[13] == "\n"
        assert test_text[14] == "        /**\n"
        assert test_text[15] == "         * @brief Move constructor for a new MyTestClassName object\n"
        assert test_text[16] == "         * \n"
        assert test_text[17] == "         * @param other Reference to object to move\n"
        assert test_text[18] == "         * \n"
        assert test_text[19] == "         */\n"
        assert test_text[20] == "        MyTestClassName(MyTestClassName&& other) = default;\n"
        assert test_text[21] == "\n"
        assert test_text[22] == "        /**\n"
        assert test_text[23] == "         * @brief Equate constructor for a new MyTestClassName object\n"
        assert test_text[24] == "         * \n"
        assert test_text[25] == "         * @param other Reference to object to copy\n"
        assert test_text[26] == "         * \n"
        assert test_text[27] == "         * @return MyTestClassName& - *this\n"
        assert test_text[28] == "         */\n"
        assert test_text[29] == "        MyTestClassName& operator=(const MyTestClassName& other) = default;\n"
        assert test_text[30] == "\n"
        assert test_text[31] == "        /**\n"
        assert test_text[32] == "         * @brief Equate move constructor for a new MyTestClassName object\n"
        assert test_text[33] == "         * \n"
        assert test_text[34] == "         * @param other Reference to object to move\n"
        assert test_text[35] == "         * \n"
        assert test_text[36] == "         * @return MyTestClassName& - *this\n"
        assert test_text[37] == "         */\n"
        assert test_text[38] == "        MyTestClassName& operator=(MyTestClassName&& other) = default;\n"
        assert test_text[39] == "\n"
        assert test_text[40] == "        /**\n"
        assert test_text[41] == "         * @brief Destructor for MyTestClassName object\n"
        assert test_text[42] == "         * \n"
        assert test_text[43] == "         */\n"
        assert test_text[44] == "        ~MyTestClassName() = default;\n"
        assert test_text[45] == "\n"

    def test39_gen_class_default_con_destrutor_no_doxy(self):
        """!
        @brief Test the _gen_class_default_constructor_destructor method, with no doxygen comments
        """
        helper = GenerateCppFileHelper()

        test_text = helper._gen_class_default_constructor_destructor("MyTestClassName", no_doxy_comment_constructor=True)
        assert len(test_text) == 7
        assert test_text[0] == "        MyTestClassName() = default;\n"
        assert test_text[1] == "        MyTestClassName(const MyTestClassName& other) = default;\n"
        assert test_text[2] == "        MyTestClassName(MyTestClassName&& other) = default;\n"
        assert test_text[3] == "        MyTestClassName& operator=(const MyTestClassName& other) = default;\n"
        assert test_text[4] == "        MyTestClassName& operator=(MyTestClassName&& other) = default;\n"
        assert test_text[5] == "        ~MyTestClassName() = default;\n"
        assert test_text[6] == "\n"

    def test40_gen_class_default_con_destrutor_no_doxy_virtual_destructor(self):
        """!
        @brief Test the _gen_class_default_constructor_destructor method, with no doxygen comments, virtual destructor
        """
        helper = GenerateCppFileHelper()

        test_text = helper._gen_class_default_constructor_destructor("MyTestClassName", virtual_destructor=True, no_doxy_comment_constructor=True)
        assert len(test_text) == 7
        assert test_text[0] == "        MyTestClassName() = default;\n"
        assert test_text[1] == "        MyTestClassName(const MyTestClassName& other) = default;\n"
        assert test_text[2] == "        MyTestClassName(MyTestClassName&& other) = default;\n"
        assert test_text[3] == "        MyTestClassName& operator=(const MyTestClassName& other) = default;\n"
        assert test_text[4] == "        MyTestClassName& operator=(MyTestClassName&& other) = default;\n"
        assert test_text[5] == "        virtual ~MyTestClassName() = default;\n"
        assert test_text[6] == "\n"

    def test41_gen_class_default_con_destrutor_no_doxy_no_copy(self):
        """!
        @brief Test the _gen_class_default_constructor_destructor method, with no doxycomment, no copy
        """
        helper = GenerateCppFileHelper()

        test_text = helper._gen_class_default_constructor_destructor("MyTestClassName", no_doxy_comment_constructor=True, no_copy=True)
        assert len(test_text) == 7
        assert test_text[0] == "        MyTestClassName() = default;\n"
        assert test_text[1] == "        MyTestClassName(const MyTestClassName& other) = delete;\n"
        assert test_text[2] == "        MyTestClassName(MyTestClassName&& other) = delete;\n"
        assert test_text[3] == "        MyTestClassName& operator=(const MyTestClassName& other) = delete;\n"
        assert test_text[4] == "        MyTestClassName& operator=(MyTestClassName&& other) = delete;\n"
        assert test_text[5] == "        ~MyTestClassName() = default;\n"
        assert test_text[6] == "\n"

    def test42_gen_class_default_con_destrutor_no_doxy_no_copy(self):
        """!
        @brief Test the _gen_class_default_constructor_destructor method, with virtual destructor, no doxycomment, no copy
        """
        helper = GenerateCppFileHelper()

        test_text = helper._gen_class_default_constructor_destructor("MyTestClassName", 6, True, True, True)
        assert len(test_text) == 7
        assert test_text[0] == "      MyTestClassName() = default;\n"
        assert test_text[1] == "      MyTestClassName(const MyTestClassName& other) = delete;\n"
        assert test_text[2] == "      MyTestClassName(MyTestClassName&& other) = delete;\n"
        assert test_text[3] == "      MyTestClassName& operator=(const MyTestClassName& other) = delete;\n"
        assert test_text[4] == "      MyTestClassName& operator=(MyTestClassName&& other) = delete;\n"
        assert test_text[5] == "      virtual ~MyTestClassName() = default;\n"
        assert test_text[6] == "\n"

    def test43_declare_struct_empty_list(self):
        """!
        @brief Test the _declare_structure method, No decorations, empty list
        """
        helper = GenerateCppFileHelper()

        var_list = []
        test_text = helper._declare_structure("MyTestStructName", var_list, 0, "Test structure")
        assert len(test_text) == 6
        assert test_text[0] == "/**\n"
        assert test_text[1] == " * @brief Test structure\n"
        assert test_text[2] == " */\n"
        assert test_text[3] == "structure MyTestStructName\n"
        assert test_text[4] == "{\n"
        assert test_text[5] == "};\n"

    def test44_declare_struct(self):
        """!
        @brief Test the _declare_structure method, No decorations
        """
        helper = GenerateCppFileHelper()

        member1 = ParamRetDict.build_param_dict_with_mod("foo", "integer", "Test integer", 0)
        member2 = ParamRetDict.build_param_dict_with_mod("moo", "unsigned", "Test unsigned", 0)
        var_list = [member1, member2]
        test_text = helper._declare_structure("MyTestStructName", var_list, 0, "Test structure")
        assert len(test_text) == 8
        assert test_text[0] == "/**\n"
        assert test_text[1] == " * @brief Test structure\n"
        assert test_text[2] == " */\n"
        assert test_text[3] == "structure MyTestStructName\n"
        assert test_text[4] == "{\n"
        assert test_text[5] == "    int foo;                                                //!< Test integer\n"
        assert test_text[6] == "    unsigned moo;                                           //!< Test unsigned\n"
        assert test_text[7] == "};\n"

    def test45_declare_struct_with_decorations(self):
        """!
        @brief Test the _declare_structure method, No decorations
        """
        helper = GenerateCppFileHelper()

        member1 = ParamRetDict.build_param_dict_with_mod("foo", "integer", "Test integer", 0)
        member2 = ParamRetDict.build_param_dict_with_mod("moo", "unsigned", "Test unsigned", 0)
        var_list = [member1, member2]
        test_text = helper._declare_structure("MyTestStructName", var_list, 0, "Test structure", "public", "const")
        assert len(test_text) == 8
        assert test_text[0] == "/**\n"
        assert test_text[1] == " * @brief Test structure\n"
        assert test_text[2] == " */\n"
        assert test_text[3] == "public structure MyTestStructName\n"
        assert test_text[4] == "{\n"
        assert test_text[5] == "    int foo;                                                //!< Test integer\n"
        assert test_text[6] == "    unsigned moo;                                           //!< Test unsigned\n"
        assert test_text[7] == "} const;\n"

    def test46_declare_variable(self):
        """!
        @brief Test the _declare_var_statment method
        """
        helper = GenerateCppFileHelper()
        member1 = ParamRetDict.build_param_dict_with_mod("foo", "integer", "Test integer", 0)
        member2 = ParamRetDict.build_param_dict_with_mod("moo", "unsigned", "Test unsigned", 0)
        member3 = ParamRetDict.build_param_dict_with_mod("goo", "string", "Test string", 0)

        test_text = helper._declare_var_statment(member1, 30)
        assert test_text == "int foo;                      //!< Test integer\n"

        test_text = helper._declare_var_statment(member2, 32)
        assert test_text == "unsigned moo;                   //!< Test unsigned\n"

        test_text = helper._declare_var_statment(member3, 10)
        assert test_text == "std::string goo; //!< Test string\n"

        test_text = helper._declare_var_statment(member2, -1)
        assert test_text == "unsigned moo;\n"

    def test47_add_list_entry(self):
        """!
        @brief Test the _gen_add_list_statment method
        """
        helper = GenerateCppFileHelper()
        test_text = helper._gen_add_list_statment("testList", "number", False)
        assert test_text == "testList.emplace_back(number);"
        test_text = helper._gen_add_list_statment("testList", "5", False)
        assert test_text == "testList.emplace_back(5);"

        test_text = helper._gen_add_list_statment("testList", "text", True)
        assert test_text == "testList.emplace_back(\"text\");"
        test_text = helper._gen_add_list_statment("testList", "AU", True)
        assert test_text == "testList.emplace_back(\"AU\");"

    def test48_generate_return(self):
        """!
        @brief Test the _gen_return_statment method
        """
        helper = GenerateCppFileHelper()
        test_text = helper._gen_return_statment("number", False)
        assert test_text == "return number;"
        test_text = helper._gen_return_statment("5", False)
        assert test_text == "return 5;"

        test_text = helper._gen_return_statment("text", True)
        assert test_text == "return \"text\";"
        test_text = helper._gen_return_statment("AU", True)
        assert test_text == "return \"AU\";"

    def test49_define_function(self):
        """!
        @brief Test the _define_function_with_decorations method, no decarations
        """
        helper = GenerateCppFileHelper()
        ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return value", 0)
        param_list = [ParamRetDict.build_param_dict_with_mod("foo", "unsigned", "Foo input", 0)]
        test_text = helper._define_function_with_decorations("MyDefineFunc", "Brief description", param_list, ret_dict)
        assert len(test_text) == 8
        assert test_text[0] == "/**\n"
        assert test_text[1] == " * @brief Brief description\n"
        assert test_text[2] == " * \n"
        assert test_text[3] == " * @param foo Foo input\n"
        assert test_text[4] == " * \n"
        assert test_text[5] == " * @return int - return value\n"
        assert test_text[6] == " */\n"
        assert test_text[7] == "int MyDefineFunc(unsigned foo)\n"

    def test50_define_function_with_pre_decoration(self):
        """!
        @brief Test the _define_function_with_decorations method, with prefix
        """
        helper = GenerateCppFileHelper()
        ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return value", 0)
        param_list = [ParamRetDict.build_param_dict_with_mod("foo", "unsigned", "Foo input", 0)]
        test_text = helper._define_function_with_decorations("MyDefineFunc", "Brief description", param_list, ret_dict, False, "static")
        assert len(test_text) == 8
        assert test_text[0] == "/**\n"
        assert test_text[1] == " * @brief Brief description\n"
        assert test_text[2] == " * \n"
        assert test_text[3] == " * @param foo Foo input\n"
        assert test_text[4] == " * \n"
        assert test_text[5] == " * @return int - return value\n"
        assert test_text[6] == " */\n"
        assert test_text[7] == "static int MyDefineFunc(unsigned foo)\n"

    def test51_define_function_with_post_decoration(self):
        """!
        @brief Test the _define_function_with_decorations method, with postfix
        """
        helper = GenerateCppFileHelper()
        ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return value", 0)
        param_list = [ParamRetDict.build_param_dict_with_mod("foo", "unsigned", "Foo input", 0)]
        test_text = helper._define_function_with_decorations("MyDefineFunc", "Brief description", param_list, ret_dict, postfix_decaration="const")
        assert len(test_text) == 8
        assert test_text[0] == "/**\n"
        assert test_text[1] == " * @brief Brief description\n"
        assert test_text[2] == " * \n"
        assert test_text[3] == " * @param foo Foo input\n"
        assert test_text[4] == " * \n"
        assert test_text[5] == " * @return int - return value\n"
        assert test_text[6] == " */\n"
        assert test_text[7] == "int MyDefineFunc(unsigned foo) const\n"

    def test52_define_function_with_pre_post_decoration(self):
        """!
        @brief Test the _define_function_with_decorations method, with prefix and postfix
        """
        helper = GenerateCppFileHelper()
        ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return value", 0)
        param_list = [ParamRetDict.build_param_dict_with_mod("foo", "unsigned", "Foo input", 0)]
        test_text = helper._define_function_with_decorations("MyDefineFunc", "Brief description", param_list, ret_dict,
                                                         prefix_decaration="static", postfix_decaration="const")
        assert len(test_text) == 8
        assert test_text[0] == "/**\n"
        assert test_text[1] == " * @brief Brief description\n"
        assert test_text[2] == " * \n"
        assert test_text[3] == " * @param foo Foo input\n"
        assert test_text[4] == " * \n"
        assert test_text[5] == " * @return int - return value\n"
        assert test_text[6] == " */\n"
        assert test_text[7] == "static int MyDefineFunc(unsigned foo) const\n"

    def test53_define_function_no_comment(self):
        """!
        @brief Test the _define_function_with_decorations method, with no comment
        """
        helper = GenerateCppFileHelper()
        ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return value", 0)
        param_list = [ParamRetDict.build_param_dict_with_mod("foo", "unsigned", "Foo input", 0)]
        test_text = helper._define_function_with_decorations("MyDefineFunc", "Brief description", param_list, ret_dict, True)
        assert len(test_text) == 1
        assert test_text[0] == "int MyDefineFunc(unsigned foo)\n"

    def test54_define_function_empty_param_list(self):
        """!
        @brief Test the _define_function_with_decorations method, with empty param list
        """
        helper = GenerateCppFileHelper()
        ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return value", 0)
        test_text = helper._define_function_with_decorations("MyDefineFunc", "Brief description", [], ret_dict, True)
        assert len(test_text) == 1
        assert test_text[0] == "int MyDefineFunc()\n"

    def test55_gen_class_open_no_descrtiption(self):
        """!
        @brief Test the _gen_class_open method, with no description
        """
        helper = GenerateCppFileHelper()

        test_text = helper._gen_class_open("MyTestClassName", None, "public MyBaseClass", "final", 2)
        assert len(test_text) == 2
        assert test_text[0] == "  class MyTestClassName final : public MyBaseClass\n"
        assert test_text[1] == "  {\n"
