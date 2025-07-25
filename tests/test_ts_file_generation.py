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
from code_tools_grocsoftware.typescript_gen.file_gen_base import GenerateTypeScriptFileHelper

# pylint: disable=too-many-lines
# pylint: disable=protected-access

class Test01CppFilehelper:
    """!
    @brief Unit test for the GenerateTypeScriptFileHelper class
    """
    def test01_constructor(self):
        """!
        @brief Test the constructor
        """
        helper = GenerateTypeScriptFileHelper()

        assert helper.copyright_generator is not None
        assert helper.eula is not None
        assert helper.doxy_comment_gen is not None
        assert helper.header_comment_gen is not None
        assert helper.level_tab_size == 4

        assert len(list(helper.type_xlation_dict.keys())) == 6
        assert helper.type_xlation_dict['string'] == "string"
        assert helper.type_xlation_dict['text'] == "string"
        assert helper.type_xlation_dict['size'] == "number"
        assert helper.type_xlation_dict['integer'] == "number"
        assert helper.type_xlation_dict['unsigned'] == "number"
        assert helper.type_xlation_dict['tuple'] == "tuple"

        helper = GenerateTypeScriptFileHelper("GNU_V11")

        assert helper.copyright_generator is not None
        assert helper.eula is not None
        assert helper.doxy_comment_gen is not None
        assert helper.header_comment_gen is not None
        assert helper.level_tab_size == 4

        assert len(list(helper.type_xlation_dict.keys())) == 6
        assert helper.type_xlation_dict['string'] == "string"
        assert helper.type_xlation_dict['text'] == "string"
        assert helper.type_xlation_dict['size'] == "number"
        assert helper.type_xlation_dict['integer'] == "number"
        assert helper.type_xlation_dict['unsigned'] == "number"
        assert helper.type_xlation_dict['tuple'] == "tuple"

    def test02declare_type_base(self):
        """!
        @brief Test the declare_type method, no modification
        """
        helper = GenerateTypeScriptFileHelper()

        # Test the xlate path
        assert helper.declare_type('string') == "string"
        assert helper.declare_type('text') == "string"
        assert helper.declare_type('size') == "number"
        assert helper.declare_type('integer') == "number"
        assert helper.declare_type('unsigned') == "number"
        assert helper.declare_type('tuple') == "tuple"

        # Test the non-xlate path
        assert helper.declare_type('MyClass') == "MyClass"

    def test03declare_type_ptr(self):
        """!
        @brief Test the declare_type method, pointer modification
        """
        helper = GenerateTypeScriptFileHelper()

        # Test the xlate path
        assert helper.declare_type('string', ParamRetDict.type_mod_ptr) == "string"
        assert helper.declare_type('text', ParamRetDict.type_mod_ptr) == "string"
        assert helper.declare_type('size', ParamRetDict.type_mod_ptr) == "number"
        assert helper.declare_type('integer', ParamRetDict.type_mod_ptr) == "number"
        assert helper.declare_type('unsigned', ParamRetDict.type_mod_ptr) == "number"
        assert helper.declare_type('tuple', ParamRetDict.type_mod_ptr) == "tuple"

    def test04declare_type_ref(self):
        """!
        @brief Test the declare_type method, pointer modification
        """
        helper = GenerateTypeScriptFileHelper()

        # Test the xlate path
        assert helper.declare_type('string', ParamRetDict.type_mod_ref) == "string"
        assert helper.declare_type('text', ParamRetDict.type_mod_ref) == "string"
        assert helper.declare_type('size', ParamRetDict.type_mod_ref) == "number"
        assert helper.declare_type('integer', ParamRetDict.type_mod_ref) == "number"
        assert helper.declare_type('unsigned', ParamRetDict.type_mod_ref) == "number"
        assert helper.declare_type('tuple', ParamRetDict.type_mod_ref) == "tuple"

    def test05declare_type_list(self):
        """!
        @brief Test the declare_type method, list modification
        """
        helper = GenerateTypeScriptFileHelper()

        # Test the xlate path
        assert helper.declare_type('string', ParamRetDict.type_mod_list) == "string[]"
        assert helper.declare_type('text', ParamRetDict.type_mod_list) == "string[]"
        assert helper.declare_type('size', ParamRetDict.type_mod_list) == "number[]"
        assert helper.declare_type('integer', ParamRetDict.type_mod_list) == "number[]"
        assert helper.declare_type('unsigned', ParamRetDict.type_mod_list) == "number[]"
        assert helper.declare_type('tuple', ParamRetDict.type_mod_list) == "tuple[]"

    def test06declare_type_list_ptr(self):
        """!
        @brief Test the declare_type method, list and pointer modification
        """
        helper = GenerateTypeScriptFileHelper()

        # Test the xlate path
        typemod = ParamRetDict.type_mod_list | ParamRetDict.type_mod_ptr
        assert helper.declare_type('string', typemod) == "string[]"
        assert helper.declare_type('text', typemod) == "string[]"
        assert helper.declare_type('size', typemod) == "number[]"
        assert helper.declare_type('integer', typemod) == "number[]"
        assert helper.declare_type('unsigned', typemod) == "number[]"
        assert helper.declare_type('tuple', typemod) == "tuple[]"

    def test07declare_type_list_ref(self):
        """!
        @brief Test the declare_type method, list and reference modification
        """
        helper = GenerateTypeScriptFileHelper()

        # Test the xlate path
        typemod = ParamRetDict.type_mod_list | ParamRetDict.type_mod_ref
        assert helper.declare_type('string', typemod) == "string[]"
        assert helper.declare_type('text', typemod) == "string[]"
        assert helper.declare_type('size', typemod) == "number[]"
        assert helper.declare_type('integer', typemod) == "number[]"
        assert helper.declare_type('unsigned', typemod) == "number[]"
        assert helper.declare_type('tuple', typemod) == "tuple[]"

    def test08declare_type_array(self):
        """!
        @brief Test the declare_type method, array modification
        """
        helper = GenerateTypeScriptFileHelper()

        # Test the xlate path
        assert helper.declare_type('string', 5 << ParamRetDict.type_mod_array_shift) == "string[]"
        assert helper.declare_type('text', 7 << ParamRetDict.type_mod_array_shift) == "string[]"
        assert helper.declare_type('size', 10 << ParamRetDict.type_mod_array_shift) == "number[]"
        assert helper.declare_type('integer', 20 << ParamRetDict.type_mod_array_shift) == "number[]"
        assert helper.declare_type('unsigned', 13 << ParamRetDict.type_mod_array_shift)=="number[]"
        assert helper.declare_type('tuple', 14 << ParamRetDict.type_mod_array_shift) == "tuple[]"

    def test09declare_type_array_ptr(self):
        """!
        @brief Test the declare_type method, array and pointer modification
        """
        helper = GenerateTypeScriptFileHelper()

        # Test the xlate path
        typemod = (8 << ParamRetDict.type_mod_array_shift) | ParamRetDict.type_mod_ptr
        assert helper.declare_type('string', typemod) == "string[]"
        assert helper.declare_type('text', typemod) == "string[]"
        assert helper.declare_type('size', typemod) == "number[]"
        assert helper.declare_type('integer', typemod) == "number[]"
        assert helper.declare_type('unsigned', typemod) == "number[]"
        assert helper.declare_type('tuple', typemod) == "tuple[]"

    def test10declare_type_array_ref(self):
        """!
        @brief Test the declare_type method, array and reference modification
        """
        helper = GenerateTypeScriptFileHelper()

        # Test the xlate path
        typemod = (8 << ParamRetDict.type_mod_array_shift) | ParamRetDict.type_mod_ref
        assert helper.declare_type('string', typemod) == "string[]"
        assert helper.declare_type('text', typemod) == "string[]"
        assert helper.declare_type('size', typemod) == "number[]"
        assert helper.declare_type('integer', typemod) == "number[]"
        assert helper.declare_type('unsigned', typemod) == "number[]"

    def test11declare_type_undef(self):
        """!
        @brief Test the declare_type method, all with undef modification
        """
        helper = GenerateTypeScriptFileHelper()

        # Test the xlate path
        assert helper.declare_type('string', ParamRetDict.type_mod_undef) == "string|undefined"

        typemod = ParamRetDict.type_mod_undef | ParamRetDict.type_mod_ptr
        assert helper.declare_type('string', typemod) == "string|undefined"

        typemod = ParamRetDict.type_mod_undef | ParamRetDict.type_mod_ref
        assert helper.declare_type('string', typemod) == "string|undefined"

        typemod = (8 << ParamRetDict.type_mod_array_shift) | ParamRetDict.type_mod_undef
        assert helper.declare_type('string', typemod) == "string[]|undefined"

        typemod = ParamRetDict.type_mod_undef | ParamRetDict.type_mod_list
        assert helper.declare_type('string', typemod) == "string[]|undefined"

        typemod = 25 << ParamRetDict.type_mod_array_shift
        typemod |= ParamRetDict.type_mod_undef
        typemod |= ParamRetDict.type_mod_ptr
        assert helper.declare_type('string', typemod) == "string[]|undefined"

        typemod = 7 << ParamRetDict.type_mod_array_shift
        typemod |= ParamRetDict.type_mod_undef | ParamRetDict.type_mod_ref
        assert helper.declare_type('string', typemod) == "string[]|undefined"

        typemod = ParamRetDict.type_mod_undef | ParamRetDict.type_mod_list
        assert helper.declare_type('string', typemod) == "string[]|undefined"

        typemod = ParamRetDict.type_mod_undef
        typemod |= ParamRetDict.type_mod_list
        typemod |= ParamRetDict.type_mod_ptr
        assert helper.declare_type('string', typemod) == "string[]|undefined"

        typemod = ParamRetDict.type_mod_undef
        typemod |= ParamRetDict.type_mod_list
        typemod |= ParamRetDict.type_mod_ref
        assert helper.declare_type('string', typemod) == "string[]|undefined"

    def test12_xlate_param_list(self):
        """!
        @brief Test the xlate_params method
        """
        helper = GenerateTypeScriptFileHelper()
        params = []
        params.append(ParamRetDict.build_param_dict_with_mod("foo",
                                                             "integer",
                                                             "myint",
                                                             0))
        params.append(ParamRetDict.build_param_dict_with_mod("moo",
                                                             "size",
                                                             "mysize",
                                                             ParamRetDict.type_mod_ptr))
        params.append(ParamRetDict.build_param_dict_with_mod("goo",
                                                             "string",
                                                             "mystr",
                                                             ParamRetDict.type_mod_list))

        xlate_list = helper.xlate_params(params)
        assert len(xlate_list) == len(params)
        assert ParamRetDict.get_param_name(xlate_list[0]) == ParamRetDict.get_param_name(params[0])
        assert ParamRetDict.get_param_type(xlate_list[0]) == "number"
        assert ParamRetDict.get_param_desc(xlate_list[0]) == ParamRetDict.get_param_desc(params[0])
        assert ParamRetDict.get_param_type_mod(xlate_list[0]) == 0

        assert ParamRetDict.get_param_name(xlate_list[1]) == ParamRetDict.get_param_name(params[1])
        assert ParamRetDict.get_param_type(xlate_list[1]) == "number"
        assert ParamRetDict.get_param_desc(xlate_list[1]) == ParamRetDict.get_param_desc(params[1])
        assert ParamRetDict.get_param_type_mod(xlate_list[1]) == 0

        assert ParamRetDict.get_param_name(xlate_list[2]) == ParamRetDict.get_param_name(params[2])
        assert ParamRetDict.get_param_type(xlate_list[2]) == "string[]"
        assert ParamRetDict.get_param_desc(xlate_list[2]) == ParamRetDict.get_param_desc(params[2])
        assert ParamRetDict.get_param_type_mod(xlate_list[2]) == 0

    def test13_xlate_param_empty_list(self):
        """!
        @brief Test the xlate_params method, empty list input
        """
        helper = GenerateTypeScriptFileHelper()
        gen_param_list = []
        xlate_list = helper.xlate_params(gen_param_list)
        assert len(xlate_list) == 0

    def test14_xlate_ret_dict(self):
        """!
        @brief Test the xlate_return_dict method
        """
        helper = GenerateTypeScriptFileHelper()
        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "myint", 0)

        xlated_ret = helper.xlate_return_dict(gen_ret_dict)
        assert ParamRetDict.get_return_type(xlated_ret) == "number"
        assert ParamRetDict.get_param_desc(xlated_ret) == ParamRetDict.get_param_desc(gen_ret_dict)
        assert ParamRetDict.get_param_type_mod(gen_ret_dict) == 0

    def test15_xlate_ret_dict_none(self):
        """!
        @brief Test the xlate_return_dict method, with no input
        """
        helper = GenerateTypeScriptFileHelper()
        xlated_ret = helper.xlate_return_dict(None)
        assert xlated_ret is None

    def test16_gen_return_type(self):
        """!
        @brief Test the gen_function_ret_type method
        """
        helper = GenerateTypeScriptFileHelper()

        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "myint", 0)
        return_text = helper.gen_function_ret_type(gen_ret_dict)
        assert return_text == ":number"

        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer",
                                                               "myint",
                                                               ParamRetDict.type_mod_list)
        return_text = helper.gen_function_ret_type(gen_ret_dict)
        assert return_text == ":number[]"

    def test17_gen_return_type(self):
        """!
        @brief Test the gen_function_ret_type method, with none input
        """
        helper = GenerateTypeScriptFileHelper()

        return_text = helper.gen_function_ret_type(None)
        assert return_text == ""

    def test18gen_function_params(self):
        """!
        @brief Test the gen_function_params method
        """
        helper = GenerateTypeScriptFileHelper()
        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo",
                                                                     "size",
                                                                     "mysize",
                                                                     ParamRetDict.type_mod_ptr))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("goo",
                                                                     "string",
                                                                     "mystr",
                                                                     ParamRetDict.type_mod_list))

        return_text = helper.gen_function_params(gen_param_list)
        assert return_text == "(foo:number, moo:number, goo:string[])"

    def test19gen_function_params_empty(self):
        """!
        @brief Test the gen_function_params method, empty list
        """
        helper = GenerateTypeScriptFileHelper()
        gen_param_list = []
        return_text = helper.gen_function_params(gen_param_list)
        assert return_text == "()"

    def test20_declare_function(self):
        """!
        @brief Test the declare_function_with_decorations method, no decorations
        """
        helper = GenerateTypeScriptFileHelper()
        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return int", 0)

        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo",
                                                                     "size",
                                                                     "mysize",
                                                                     ParamRetDict.type_mod_ptr))

        function_text = helper.declare_function_with_decorations("my_test", "My test function",
                                                                 gen_param_list, gen_ret_dict)
        assert len(function_text) == 10
        assert function_text[0] == '/**\n'
        assert function_text[1] == ' * @brief My test function\n'
        assert function_text[2] == ' * \n'
        assert function_text[3] == ' * @param foo {number} myint\n'
        assert function_text[4] == ' * @param moo {number} mysize\n'
        assert function_text[5] == ' * \n'
        assert function_text[6] == ' * @return number - return int\n'
        assert function_text[7] == ' */\n'
        assert function_text[8] == 'public my_test(foo:number, moo:number):number\n'
        assert function_text[9] == '{//! @todo Implement code }\n'

    def test21_declare_function_with_prefix(self):
        """!
        @brief Test the declare_function_with_decorations method, prefix decoration
        """
        helper = GenerateTypeScriptFileHelper()
        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return int", 0)

        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo",
                                                                     "size",
                                                                     "mysize",
                                                                     ParamRetDict.type_mod_ptr))

        function_text = helper.declare_function_with_decorations("my_test",
                                                                 "My test function",
                                                                 gen_param_list,
                                                                 gen_ret_dict,
                                                                 8,
                                                                 prefix_decaration='public')
        assert len(function_text) == 10
        assert function_text[0] == '        /**\n'
        assert function_text[1] == '         * @brief My test function\n'
        assert function_text[2] == '         * \n'
        assert function_text[3] == '         * @param foo {number} myint\n'
        assert function_text[4] == '         * @param moo {number} mysize\n'
        assert function_text[5] == '         * \n'
        assert function_text[6] == '         * @return number - return int\n'
        assert function_text[7] == '         */\n'
        assert function_text[8] == '        public my_test(foo:number, moo:number):number\n'
        assert function_text[9] == '        {//! @todo Implement code }\n'

    def test22_declare_function_with_postfix(self):
        """!
        @brief Test the declare_function_with_decorations method, postfix decoration
        """
        helper = GenerateTypeScriptFileHelper()
        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return int", 0)

        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo",
                                                                     "size",
                                                                     "mysize",
                                                                     ParamRetDict.type_mod_ptr))

        pf_decaration = '@configurable(false)'
        function_text = helper.declare_function_with_decorations("my_test",
                                                                 "My test function",
                                                                 gen_param_list,
                                                                 gen_ret_dict,
                                                                 8,
                                                                 postfix_decaration=pf_decaration)
        assert len(function_text) == 11
        assert function_text[0] == '        /**\n'
        assert function_text[1] == '         * @brief My test function\n'
        assert function_text[2] == '         * \n'
        assert function_text[3] == '         * @param foo {number} myint\n'
        assert function_text[4] == '         * @param moo {number} mysize\n'
        assert function_text[5] == '         * \n'
        assert function_text[6] == '         * @return number - return int\n'
        assert function_text[7] == '         */\n'
        assert function_text[8] == '        @configurable(false)\n'
        assert function_text[9] == '        public my_test(foo:number, moo:number):number\n'
        assert function_text[10] == '        {//! @todo Implement code }\n'

    def test23_declare_function_with_pre_and_postfix(self):
        """!
        @brief Test the declare_function_with_decorations method, prefix, postfix decoration
        """
        helper = GenerateTypeScriptFileHelper()
        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return int", 0)

        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo",
                                                                     "size",
                                                                     "mysize",
                                                                     ParamRetDict.type_mod_ptr))

        pf_decaration = '@configurable(false)'
        function_text = helper.declare_function_with_decorations("my_test",
                                                                 "My test function",
                                                                 gen_param_list,
                                                                 gen_ret_dict,
                                                                 8,
                                                                 prefix_decaration="private",
                                                                 postfix_decaration=pf_decaration)
        assert len(function_text) == 11
        assert function_text[0] == '        /**\n'
        assert function_text[1] == '         * @brief My test function\n'
        assert function_text[2] == '         * \n'
        assert function_text[3] == '         * @param foo {number} myint\n'
        assert function_text[4] == '         * @param moo {number} mysize\n'
        assert function_text[5] == '         * \n'
        assert function_text[6] == '         * @return number - return int\n'
        assert function_text[7] == '         */\n'
        assert function_text[8] == '        @configurable(false)\n'
        assert function_text[9] == '        private my_test(foo:number, moo:number):number\n'
        assert function_text[10] == '        {//! @todo Implement code }\n'

    def test24_declare_function_with_pre_and_postfix_no_comment(self):
        """!
        @brief Test the declare_function_with_decorations method,
               prefix, postfix decoration, no comment
        """
        helper = GenerateTypeScriptFileHelper()
        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return int", 0)

        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo",
                                                                     "size",
                                                                     "mysize",
                                                                     ParamRetDict.type_mod_ptr))

        function_text = helper.declare_function_with_decorations("my_test",
                                                                 "My test function",
                                                                 gen_param_list,
                                                                 gen_ret_dict,
                                                                 8,
                                                                 True,
                                                                 "public",
                                                                 '@enumerable(false)')
        assert len(function_text) == 3
        assert function_text[0] == '        @enumerable(false)\n'
        assert function_text[1] == '        public my_test(foo:number, moo:number):number\n'
        assert function_text[2] == '        {//! @todo Implement code }\n'

    def test25_declare_function_with_no_comment_inline_single_line(self):
        """!
        @brief Test the declare_function_with_decorations method, no comment inline code
        """
        helper = GenerateTypeScriptFileHelper()
        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return int", 0)

        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo",
                                                                     "size",
                                                                     "mysize",
                                                                     ParamRetDict.type_mod_ptr))

        function_text = helper.declare_function_with_decorations("my_test",
                                                                 "My test function",
                                                                 gen_param_list,
                                                                 gen_ret_dict,
                                                                 8,
                                                                 True,
                                                                 "public",
                                                                 '@enumerable(false)',
                                                                 ["return 15;"])
        assert len(function_text) == 3
        assert function_text[0] == '        @enumerable(false)\n'
        assert function_text[1] == '        public my_test(foo:number, moo:number):number\n'
        assert function_text[2] == '        {return 15;}\n'

    def test26_declare_function_with_no_comment_inline_multi_line(self):
        """!
        @brief Test the declare_function_with_decorations method, no comment inline code
        """
        helper = GenerateTypeScriptFileHelper()
        gen_ret_dict = ParamRetDict.build_return_dict_with_mod("integer",
                                                               "return list",
                                                               ParamRetDict.type_mod_list)

        gen_param_list = []
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("foo", "integer", "myint", 0))
        gen_param_list.append(ParamRetDict.build_param_dict_with_mod("moo",
                                                                     "size",
                                                                     "mysize",
                                                                     ParamRetDict.type_mod_ptr))

        inline_code =["number retvar[];",
                     "retvar.push_back(15);",
                     "retvar.push_back(25);",
                     "return retvar;"]

        function_text = helper.declare_function_with_decorations("my_test",
                                                                 "My test function",
                                                                 gen_param_list,
                                                                 gen_ret_dict,
                                                                 8,
                                                                 True,
                                                                 "public",
                                                                 '@enumerable(false)',
                                                                 inline_code)
        assert len(function_text) == 8
        assert function_text[0] == '        @enumerable(false)\n'
        assert function_text[1] == '        public my_test(foo:number, moo:number):number[]\n'
        assert function_text[2] == '        {\n'
        assert function_text[3] == '            '+inline_code[0]+'\n'
        assert function_text[4] == '            '+inline_code[1]+'\n'
        assert function_text[5] == '            '+inline_code[2]+'\n'
        assert function_text[6] == '            '+inline_code[3]+'\n'
        assert function_text[7] == '        }\n'

    def test27end_function(self):
        """!
        @brief Test the end_function method
        """
        helper = GenerateTypeScriptFileHelper()
        function_text = helper.end_function("my_test")
        assert function_text == '} // end of function my_test\n'

    def test28_gen_file_header(self):
        """!
        @brief Test the generate_generic_file_header method
        """
        helper = GenerateTypeScriptFileHelper()
        current_year = datetime.now().year
        header_text = helper.generate_generic_file_header("unittest", current_year, "Me")
        copyright_msg = "* Copyright (c) "+str(current_year)+" Me"
        assert len(header_text) == 27
        assert header_text[0] == "/*--------------------------------------------------------" \
                                 "----------------------\n"
        assert header_text[1] == copyright_msg+"\n"
        assert header_text[3] == "* MIT License\n"
        assert header_text[24] == "* This file was autogenerated by unittest do not edit\n"
        assert header_text[26] == "* ------------------------------------------------------" \
                                  "----------------------*/\n"

    def test29_gen_import(self):
        """!
        @brief Test the gen_import method
        """
        helper = GenerateTypeScriptFileHelper()

        include_text = helper.gen_import("testclass", "testmodule")
        assert include_text == "import {testclass} from testmodule;\n"

        include_text = helper.gen_import("testclass")
        assert include_text == "import 'testclass';\n"

    def test30_gen_import_block(self):
        """!
        @brief Test the gen_import_block method
        """
        helper = GenerateTypeScriptFileHelper()
        include_list = [("class1", "module1"),
                        ("class2", "module2"),
                        ("class3", "module3"),
                        ("class4", None)]
        include_text = helper.gen_import_block(include_list)
        assert len(include_text) == len(include_list) + 1
        assert include_text[0] == "// Imports\n"
        assert include_text[1] == "import {class1} from module1;\n"
        assert include_text[2] == "import {class2} from module2;\n"
        assert include_text[3] == "import {class3} from module3;\n"
        assert include_text[4] == "import 'class4';\n"

    def test31_gen_open_namespace(self):
        """!
        @brief Test the gen_namespace_open method
        """
        helper = GenerateTypeScriptFileHelper()

        test_text = helper.gen_namespace_open("wonder")
        assert len(test_text) == 1
        assert test_text[0] == "namespace wonder {\n"

        test_text = helper.gen_namespace_open("boy")
        assert len(test_text) == 1
        assert test_text[0] == "namespace boy {\n"

    def test32_gen_close_namespace(self):
        """!
        @brief Test the gen_namespace_close method
        """
        helper = GenerateTypeScriptFileHelper()

        test_text = helper.gen_namespace_close("wonder")
        assert len(test_text) == 1
        assert test_text[0] == "} // end of namespace wonder\n"

        test_text = helper.gen_namespace_close("boy")
        assert len(test_text) == 1
        assert test_text[0] == "} // end of namespace boy\n"

    def test34gen_class_open(self):
        """!
        @brief Test the gen_class_open method, no decorations
        """
        helper = GenerateTypeScriptFileHelper()

        test_text = helper.gen_class_open("MyTestClassName", "My class description")
        assert len(test_text) == 5
        assert test_text[0] == "/**\n"
        assert test_text[1] == " * @brief My class description\n"
        assert test_text[2] == " */\n"
        assert test_text[3] == "class MyTestClassName\n"
        assert test_text[4] == "{\n"

    def test35gen_class_open_with_inheritence(self):
        """!
        @brief Test the gen_class_open method, with inheritence
        """
        helper = GenerateTypeScriptFileHelper()

        test_text = helper.gen_class_open("MyTestClassName", "My class description", "MyBaseClass")
        assert len(test_text) == 5
        assert test_text[0] == "/**\n"
        assert test_text[1] == " * @brief My class description\n"
        assert test_text[2] == " */\n"
        assert test_text[3] == "class MyTestClassName extends MyBaseClass\n"
        assert test_text[4] == "{\n"

    def test36gen_class_open_decoration(self):
        """!
        @brief Test the gen_class_open method, with inheritence
        """
        helper = GenerateTypeScriptFileHelper()

        test_text = helper.gen_class_open("MyTestClassName",
                                          "My class description",
                                          "MyBaseClass",
                                          "export",
                                          2)
        assert len(test_text) == 5
        assert test_text[0] == "  /**\n"
        assert test_text[1] == "   * @brief My class description\n"
        assert test_text[2] == "   */\n"
        assert test_text[3] == "  export class MyTestClassName extends MyBaseClass\n"
        assert test_text[4] == "  {\n"

    def test37gen_class_close(self):
        """!
        @brief Test the gen_class_close method, with inheritence
        """
        helper = GenerateTypeScriptFileHelper()

        test_text = helper.gen_class_close("MyTestClassName")
        assert len(test_text) == 1
        assert test_text[0] == "} // end of MyTestClassName class\n"

        test_text = helper.gen_class_close("MyTestClassName", 2)
        assert len(test_text) == 1
        assert test_text[0] == "  } // end of MyTestClassName class\n"

    def test38_gen_class_default_construtor(self):
        """!
        @brief Test the gen_class_default_constructor method
        """
        helper = GenerateTypeScriptFileHelper()

        test_text = helper.gen_class_default_constructor("MyTestClassName")
        assert len(test_text) == 7
        assert test_text[0] == "        /**\n"
        assert test_text[1] == "         * @brief Construct a new MyTestClassName object\n"
        assert test_text[2] == "         * \n"
        assert test_text[3] == "         */\n"
        assert test_text[4] == "        public constructor()\n"
        assert test_text[5] == "        {//! @todo Implement code }\n"
        assert test_text[6] == "\n"

    def test39_gen_class_default_contrutor_no_doxy(self):
        """!
        @brief Test the gen_class_default_constructor method, with no doxygen comments
        """
        helper = GenerateTypeScriptFileHelper()

        test_text = helper.gen_class_default_constructor("MyTestClassName",
                                                         no_doxy_comment_constructor=True)
        assert len(test_text) == 3
        assert test_text[0] == "        public constructor()\n"
        assert test_text[1] == "        {//! @todo Implement code }\n"
        assert test_text[2] == "\n"

    def test40_gen_class_default_construtor_with_input_params(self):
        """!
        @brief Test the gen_class_default_constructor method, with doxygen
               comments, and parameter list
        """
        helper = GenerateTypeScriptFileHelper()
        params = [ParamRetDict.build_param_dict_with_mod("one", "string", "Parameter one", 0),
                  ParamRetDict.build_param_dict_with_mod("two", "integer", "Parameter two", 0)]
        test_text = helper.gen_class_default_constructor("MyTestClassName", param_list=params)
        assert len(test_text) == 10
        assert test_text[0] == "        /**\n"
        assert test_text[1] == "         * @brief Construct a new MyTestClassName object\n"
        assert test_text[2] == "         * \n"
        assert test_text[3] == "         * @param one {string} Parameter one\n"
        assert test_text[4] == "         * @param two {number} Parameter two\n"
        assert test_text[5] == "         * \n"
        assert test_text[6] == "         */\n"
        assert test_text[7] == "        public constructor(one:string, two:number)\n"
        assert test_text[8] == "        {//! @todo Implement code }\n"
        assert test_text[9] == "\n"

    def test41_gen_class_default_construtor_no_doxy_input_params(self):
        """!
        @brief Test the gen_class_default_constructor method,
               with no doxygen comments, and parameter list
        """
        helper = GenerateTypeScriptFileHelper()
        params = [ParamRetDict.build_param_dict_with_mod("one", "string", "Parameter one", 0),
                  ParamRetDict.build_param_dict_with_mod("two", "integer", "Parameter two", 0)]
        test_text = helper.gen_class_default_constructor("MyTestClassName",
                                                         param_list=params,
                                                         no_doxy_comment_constructor=True)
        assert len(test_text) == 3
        assert test_text[0] == "        public constructor(one:string, two:number)\n"
        assert test_text[1] == "        {//! @todo Implement code }\n"
        assert test_text[2] == "\n"

    def test42_gen_class_default_construtor_no_doxy_with_inline(self):
        """!
        @brief Test the gen_class_default_constructor method, with virtual destructor,
               no doxycomment, no copy
        """
        helper = GenerateTypeScriptFileHelper()

        helper = GenerateTypeScriptFileHelper()
        params = [ParamRetDict.build_param_dict_with_mod("one", "string", "Parameter one", 0),
                  ParamRetDict.build_param_dict_with_mod("two", "integer", "Parameter two", 0)]
        inline_code = ["this.one = one;", "this.two = two;"]
        test_text = helper.gen_class_default_constructor("MyTestClassName",
                                                         4,
                                                         params,
                                                         inline_code,
                                                         True)
        assert len(test_text) == 6
        assert test_text[0] == "    public constructor(one:string, two:number)\n"
        assert test_text[1] == "    {\n"
        assert test_text[2] == "        this.one = one;\n"
        assert test_text[3] == "        this.two = two;\n"
        assert test_text[4] == "    }\n"
        assert test_text[5] == "\n"

    def test43_declare_struct_empty_list(self):
        """!
        @brief Test the declare_structure method, No decorations, empty list
        """
        helper = GenerateTypeScriptFileHelper()

        var_list = []
        test_text = helper.declare_structure("MyTestStructName", var_list, 0, "Test structure")
        assert len(test_text) == 5
        assert test_text[0] == "/**\n"
        assert test_text[1] == " * @brief Test structure\n"
        assert test_text[2] == " */\n"
        assert test_text[3] == "interface MyTestStructName {\n"
        assert test_text[4] == "}\n"

    def test44_declare_struct(self):
        """!
        @brief Test the declare_structure method, No decorations
        """
        helper = GenerateTypeScriptFileHelper()

        member1 = ParamRetDict.build_param_dict_with_mod("foo", "integer", "Test integer", 0)
        member2 = ParamRetDict.build_param_dict_with_mod("moo", "unsigned", "Test unsigned", 0)
        var_list = [member1, member2]
        test_text = helper.declare_structure("MyTestStructName", var_list, 0, "Test structure")
        assert len(test_text) == 7
        assert test_text[0] == "/**\n"
        assert test_text[1] == " * @brief Test structure\n"
        assert test_text[2] == " */\n"
        assert test_text[3] == "interface MyTestStructName {\n"
        assert test_text[4] == "    foo:number;                    " \
                               "                         //!< Test integer\n"
        assert test_text[5] == "    moo:number;                    " \
                               "                         //!< Test unsigned\n"
        assert test_text[6] == "}\n"

    def test45_declare_struct_with_decorations(self):
        """!
        @brief Test the declare_structure method, No decorations
        """
        helper = GenerateTypeScriptFileHelper()

        member1 = ParamRetDict.build_param_dict_with_mod("foo", "integer", "Test integer", 0)
        member2 = ParamRetDict.build_param_dict_with_mod("moo", "unsigned", "Test unsigned", 0)
        var_list = [member1, member2]
        test_text = helper.declare_structure("MyTestStructName",
                                             var_list,
                                             0,
                                             "Test structure",
                                             "export",
                                             "const")
        assert len(test_text) == 7
        assert test_text[0] == "/**\n"
        assert test_text[1] == " * @brief Test structure\n"
        assert test_text[2] == " */\n"
        assert test_text[3] == "export interface MyTestStructName {\n"
        assert test_text[4] == "    foo:number;                        " \
                               "                     //!< Test integer\n"
        assert test_text[5] == "    moo:number;                        " \
                               "                     //!< Test unsigned\n"
        assert test_text[6] == "} const\n"

    def test46_declare_variable(self):
        """!
        @brief Test the declare_var_statment method
        """
        helper = GenerateTypeScriptFileHelper()
        member1 = ParamRetDict.build_param_dict_with_mod("foo", "integer", "Test integer", 0)
        member2 = ParamRetDict.build_param_dict_with_mod("moo", "unsigned", "Test unsigned", 0)
        member3 = ParamRetDict.build_param_dict_with_mod("goo", "string", "Test string", 0)

        test_text = helper.declare_var_statment(member1, 30)
        assert test_text == "foo:number;                   //!< Test integer\n"

        test_text = helper.declare_var_statment(member2, 32)
        assert test_text == "moo:number;                     //!< Test unsigned\n"

        test_text = helper.declare_var_statment(member3, 10)
        assert test_text == "goo:string; //!< Test string\n"

    def test47_add_list_entry(self):
        """!
        @brief Test the gen_add_list_statment method
        """
        helper = GenerateTypeScriptFileHelper()
        test_text = helper.gen_add_list_statment("testList", "number", False)
        assert test_text == "testList.push(number);"
        test_text = helper.gen_add_list_statment("testList", "5", False)
        assert test_text == "testList.push(5);"

        test_text = helper.gen_add_list_statment("testList", "text", True)
        assert test_text == "testList.push(\"text\");"
        test_text = helper.gen_add_list_statment("testList", "AU", True)
        assert test_text == "testList.push(\"AU\");"

    def test48_generate_return(self):
        """!
        @brief Test the gen_return_statment method
        """
        helper = GenerateTypeScriptFileHelper()
        test_text = helper.gen_return_statment("number", False)
        assert test_text == "return number;"
        test_text = helper.gen_return_statment("5", False)
        assert test_text == "return 5;"

        test_text = helper.gen_return_statment("text", True)
        assert test_text == "return \"text\";"
        test_text = helper.gen_return_statment("AU", True)
        assert test_text == "return \"AU\";"

    def test49_define_function(self):
        """!
        @brief Test the define_function_with_decorations method, no decarations
        """
        helper = GenerateTypeScriptFileHelper()
        ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return value", 0)
        param_list = [ParamRetDict.build_param_dict_with_mod("foo", "unsigned", "Foo input", 0)]
        test_text = helper.define_function_with_decorations("MyDefineFunc",
                                                            "Brief description",
                                                            param_list,
                                                            ret_dict)
        assert len(test_text) == 9
        assert test_text[0] == "/**\n"
        assert test_text[1] == " * @brief Brief description\n"
        assert test_text[2] == " * \n"
        assert test_text[3] == " * @param foo {number} Foo input\n"
        assert test_text[4] == " * \n"
        assert test_text[5] == " * @return number - return value\n"
        assert test_text[6] == " */\n"
        assert test_text[7] == "function MyDefineFunc(foo:number):number\n"
        assert test_text[8] == "{\n"


    def test50_define_function_with_pre_decoration(self):
        """!
        @brief Test the define_function_with_decorations method, with prefix
        """
        helper = GenerateTypeScriptFileHelper()
        ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return value", 0)
        param_list = [ParamRetDict.build_param_dict_with_mod("foo", "unsigned", "Foo input", 0)]
        test_text = helper.define_function_with_decorations("MyDefineFunc",
                                                            "Brief description",
                                                            param_list,
                                                            ret_dict,
                                                            False,
                                                            "export")
        assert len(test_text) == 9
        assert test_text[0] == "/**\n"
        assert test_text[1] == " * @brief Brief description\n"
        assert test_text[2] == " * \n"
        assert test_text[3] == " * @param foo {number} Foo input\n"
        assert test_text[4] == " * \n"
        assert test_text[5] == " * @return number - return value\n"
        assert test_text[6] == " */\n"
        assert test_text[7] == "export function MyDefineFunc(foo:number):number\n"
        assert test_text[8] == "{\n"

    def test51_define_function_with_post_decoration(self):
        """!
        @brief Test the define_function_with_decorations method, with postfix
        """
        helper = GenerateTypeScriptFileHelper()
        ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return value", 0)
        param_list = [ParamRetDict.build_param_dict_with_mod("foo", "unsigned", "Foo input", 0)]
        test_text = helper.define_function_with_decorations("MyDefineFunc",
                                                            "Brief description",
                                                            param_list, ret_dict)
        assert len(test_text) == 9
        assert test_text[0] == "/**\n"
        assert test_text[1] == " * @brief Brief description\n"
        assert test_text[2] == " * \n"
        assert test_text[3] == " * @param foo {number} Foo input\n"
        assert test_text[4] == " * \n"
        assert test_text[5] == " * @return number - return value\n"
        assert test_text[6] == " */\n"
        assert test_text[7] == "function MyDefineFunc(foo:number):number\n"
        assert test_text[8] == "{\n"

    def test52_define_function_with_pre_post_decoration(self):
        """!
        @brief Test the define_function_with_decorations method, with prefix and postfix
        """
        helper = GenerateTypeScriptFileHelper()
        ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return value", 0)
        param_list = [ParamRetDict.build_param_dict_with_mod("foo", "unsigned", "Foo input", 0)]
        test_text = helper.define_function_with_decorations("MyDefineFunc",
                                                            "Brief description",
                                                            param_list, ret_dict,
                                                            prefix_decaration="export")
        assert len(test_text) == 9
        assert test_text[0] == "/**\n"
        assert test_text[1] == " * @brief Brief description\n"
        assert test_text[2] == " * \n"
        assert test_text[3] == " * @param foo {number} Foo input\n"
        assert test_text[4] == " * \n"
        assert test_text[5] == " * @return number - return value\n"
        assert test_text[6] == " */\n"
        assert test_text[7] == "export function MyDefineFunc(foo:number):number\n"
        assert test_text[8] == "{\n"

    def test53_define_function_no_comment(self):
        """!
        @brief Test the define_function_with_decorations method, with no comment
        """
        helper = GenerateTypeScriptFileHelper()
        ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return value", 0)
        param_list = [ParamRetDict.build_param_dict_with_mod("foo", "unsigned", "Foo input", 0)]
        test_text = helper.define_function_with_decorations("MyDefineFunc",
                                                            "Brief description",
                                                            param_list,
                                                            ret_dict,
                                                            True)
        assert len(test_text) == 2
        assert test_text[0] == "function MyDefineFunc(foo:number):number\n"
        assert test_text[1] == "{\n"

    def test54_define_function_empty_param_list(self):
        """!
        @brief Test the define_function_with_decorations method, with empty param list
        """
        helper = GenerateTypeScriptFileHelper()
        ret_dict = ParamRetDict.build_return_dict_with_mod("integer", "return value", 0)
        test_text = helper.define_function_with_decorations("MyDefineFunc",
                                                            "Brief description",
                                                            [],
                                                            ret_dict,
                                                            True)
        assert len(test_text) == 2
        assert test_text[0] == "function MyDefineFunc():number\n"
        assert test_text[1] == "{\n"

# pylint: enable=too-many-public-methods
# pylint: enable=protected-access
