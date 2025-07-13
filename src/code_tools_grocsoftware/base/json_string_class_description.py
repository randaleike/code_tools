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

import re
import json

from code_tools_grocsoftware.base.param_return_tools import ParamRetDict
from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList
from code_tools_grocsoftware.base.translate_text_parser import TransTxtParser

class StringClassDescription():
    """!
    String object class definitions
    """

    def __init__(self, string_def_file_name:str = None):
        """!
        @brief StringClassDescription constructor

        @param lang_list_file_name (string) - Name of the json file containing
                                           the language description data
        """
        if string_def_file_name is None:
            self.filename = "jsonStringClassDescription.json"
        else:
            self.filename = string_def_file_name
        try:
            lang_json_file = open(self.filename, 'r', encoding='utf-8') # pylint: disable=consider-using-with
        except FileNotFoundError:
            self.string_jason_data = {'baseClassName': "baseclass",
                                      'namespace': "myNamespace",
                                      'dynamicCompileSwitch': "DYNAMIC_INTERNATIONALIZATION",
                                      'propertyMethods':{},
                                      'translateMethods':{}}
        else:
            self.string_jason_data = json.load(lang_json_file)
            lang_json_file.close()

        self.trans_client = None  # open it only if and when we need it

    def __set_transmethod_text(self, methodname:str, lang_code:str, text:list):
        """!
        @brief Set the language text for the input method name and language ISO code
        @param method_name {string} Translation method name dictionary id
        @param lang_iso_code {string} Translation method language iso code id
        @param text {list} Translated string data list
        """
        self.string_jason_data['translateMethods'][methodname]['translateDesc'][lang_code] = text

    def __get_transmethod_text(self, methodname:str, lang_code:str)->list:
        """!
        @brief Set the language text for the input method name and language ISO code
        @param method_name {string} Translation method name dictionary id
        @param lang_iso_code {string} Translation method language iso code id
        @return {list} Translated string data list
        """
        return self.string_jason_data['translateMethods'][methodname]['translateDesc'][lang_code]

    def __get_transmethod_text_list(self, methodname:str)->list:
        """!
        @brief Set the language text for the input method name and language ISO code
        @param method_name {string} Translation method name dictionary id
        @param lang_iso_code {string} Translation method language iso code id
        @return {list} Translated string data list
        """
        return list(self.string_jason_data['translateMethods'][methodname]['translateDesc'])

    def _get_commit_over_write_flag(self, entry_name:str, override:bool = False)->bool:
        """!
        @brief Determine if the user is ready to commit the new entry over the existing one
        @param entry_name {string} Name of the method that will be added
        @param override {boolean} True = force commit, False = ask user
        """
        commit_flag = False
        if override:
            commit_flag = True
        else:
            # Determine if we should overwrite existing
            commit = input("Overwrite existing "+entry_name+" entry? [Y/N]").upper()
            if commit in ['Y', "YES"]:
                commit_flag = True
        return commit_flag

    def _get_commit_new_flag(self, entry_name:str)->bool:
        """!
        @brief Determine if the user is ready to commit the new entry
        @param entry_name {string} Name of the method that will be added
        """
        commit = input("Add new "+entry_name+" entry? [Y/N]").upper()
        return bool(commit in ['Y', "YES"])

    def _get_commit_flag(self, entry_name:str, entry_keys:list, override:bool = False)->bool:
        """!
        @brief Determine if the user is ready to commit the new entry
        @param entry_name {string} Name of the method that will be added
        @param entry_keys {list of keys} List of the existing entry keys
        @param override {boolean} True = force commit, False = ask user
        """
        if entry_name in entry_keys:
            flag = self._get_commit_over_write_flag(entry_name, override)
        else:
            flag = self._get_commit_new_flag(entry_name)
        return flag

    def set_base_class_name(self, class_name:str):
        """!
        @brief Update the base class name
        @param class_name {string} Base class name for the methods
        """
        self.string_jason_data['baseClassName'] = class_name

    def get_base_class_name(self)->str:
        """!
        @brief Get the base class name value
        @return string - Base class name for the methods
        """
        return self.string_jason_data['baseClassName']

    def get_base_class_name_with_namespace(self, namespace_name:str,
                                           scope_operator:str = '::')->str:
        """!
        @brief Return the base class name
        @param namespace_name {string} Namespace name
        @param scope_operator {string} Programming language scope resolution operator
        @return string Base sting class name
        """
        return namespace_name+scope_operator+self.get_base_class_name()

    def get_language_class_name(self, language_name:str = None)->str:
        """!
        @brief Get the base class name value
        @param language_name {string} Language name to append to the base class name or None
        @return string - Generated class name for the methods
        """
        if language_name is None:
            ret_name = self.string_jason_data['baseClassName']
        else:
            ret_name = self.string_jason_data['baseClassName']+language_name.capitalize()
        return ret_name

    def get_language_class_name_with_namespace(self, namespace_name:str,
                                               scope_operator:str = '::',
                                               language_name:str = None)->str:
        """!
        @brief Return the base class name
        @param namespace_name {string} Namespace name
        @param scope_operator {string} Programming language scope resolution operator
        @param language_name {string} Language name to append to the base class name or None
        @return string Base sting class name
        """
        return namespace_name+scope_operator+self.get_language_class_name(language_name)

    def set_namespace_name(self, namespace:str):
        """!
        @brief Set the namespace name for code generation
        @param namespace {string} Namespace name string to add to the JSON file
        """
        self.string_jason_data['namespace'] = namespace

    def get_namespace_name(self)->str:
        """!
        @brief Get the namespace name for code generation
        @return string - Namespace name string from the JSON file
        """
        return self.string_jason_data['namespace']

    def set_dynamic_compile_switch(self, switch:str):
        """!
        @brief Set the dynamic language compile switch for code generation
        @param switch {string} Dynamic language compile switch string to add to the JSON file
        """
        self.string_jason_data['dynamicCompileSwitch'] = switch

    def get_dynamic_compile_switch(self)->str:
        """!
        @brief Get the dynamic language compile switch for code generation
        @return string - Dynamic language compile switch string from the JSON file
        """
        return self.string_jason_data['dynamicCompileSwitch']

    def _define_property_function_entry(self, property_name:str = "", brief_desc:str = "",
                                     ret_type:str = "", ret_desc:str = "",
                                     is_list:bool = False)->dict:
        """!
        @brief Define a property string return function dictionary and
               return the entry to the caller

        @param property_name {string} Name of the property
        @param brief_desc {string} Brief description of the function used in
                                  doxygen comment block generation
        @param ret_type {string} Return type string
        @param ret_desc {string} Description of the return parserstr value
        @param islist {boolean} True = data is a list, False = single value

        @return {'name':<string>, 'briefDesc':<string>, 'params':[],
                 'return':ParamRetDict.build_return_dict(ret_type, ret_desc, is_list),
                 'inline':<string>} property function dictionary
        """
        function_dict = {'name': property_name,
                         'briefDesc': brief_desc,
                         'params': [],
                         'return': ParamRetDict.build_return_dict(ret_type, ret_desc, is_list)
                        }
        return function_dict

    def get_property_method_list(self)->list:
        """!
        @brief Return a list of property method name strings
        @return list of strings - Names of the property methods
        """
        return list(self.string_jason_data['propertyMethods'].keys())

    def get_iso_property_method_name(self)->str:
        """!
        @brief Get the get ISO 639-1 code method name
        @return string - Get ISO code method name
        """
        property_method_list = self.get_property_method_list()
        for method_name in property_method_list:
            if self.string_jason_data['propertyMethods'][method_name]['name'] == 'isoCode':
                return method_name

        return None

    def get_property_method_data(self, method_name:str)->tuple:
        """!
        @brief Return the input method_name data
        @return (tuple) - {string} Language descption property name,
                          {string} Brief description of the property method for Doxygen comment,
                          {list of dictionaries} Parameter list (probably empty list),
                          {dictionary} Return data dictionary
        """
        entry = self.string_jason_data['propertyMethods'][method_name]
        return entry['name'], entry['briefDesc'], entry['params'], entry['return']

    def _define_translation_dict(self, translate_base_lang:str = "en",
                                 translate_text:list = None)->dict:
        """!
        @brief Create a translation dictionary
        @param translate_base_lang {string} ISO 639-1 language code for the input translate_text
                                            string
        @param translate_text {list} Parsed text of the message
        @return dictionary - {'base':<translate_base_lang>, 'text':<translate_text>} Translate
                             method translation string dictionary
        """
        return {translate_base_lang: translate_text}

    def add_manual_translation(self, method_name:str, base_lang:str = "en",
                               text_data:list = None)->bool:
        """!
        @brief Add language text to the function definition
        @param method_name {string} Translation method name to add the language text to
        @param base_lang {sting} ISO 639-1 language code for the input text_data string
        @param text_data {list} Parsed text of the message
        @return boolean - True if it was added, else false
        """
        status = False
        if method_name in self.string_jason_data['translateMethods']:
            if text_data is not None:
                self.__set_transmethod_text(method_name, base_lang, text_data)
                status = True
        return status

    def _translate_text(self, source_lang:str, target_lang:str, text:str)->str:
        """!
        @brief Translate the input text
        @param source_lang {string} ISO 639-1 language code of the input text
        @param target_lang {string} ISO 639-1 language code for the output text
        @param text {string} text to translate
        @return string - Translated text
        """
        from google.cloud import translate_v2   # pylint: disable=import-outside-toplevel
        if self.trans_client is None:
            self.trans_client = translate_v2.Client()

        if isinstance(text, bytes):
            text = text.decode("utf-8")

        transtext = self.trans_client.translate(text,
                                                target_language=target_lang,
                                                format_='text',
                                                source_language=source_lang,
                                                model='nmt')
        raw_translated_text = transtext['translatedText']
        return raw_translated_text

    def _translate_method_text(self, method_name:str,
                               json_lang_data:LanguageDescriptionList = None):
        """!
        @brief Add language text to the function definition
        @param method_name {string} Translation method name to add the language text to
        @param json_lang_data {LanguageDescriptionList} Language list data
        """
        if json_lang_data is not None:
            # Get the list of supported languages and the list of existing translations
            language_list = json_lang_data.get_language_list()
            existing_langages = self.__get_transmethod_text_list(method_name)

            # Determine if any language translations are missing
            for language in language_list:
                lang_iso_code = json_lang_data.get_language_iso_code_data(language)
                if lang_iso_code not in existing_langages:
                    # Use the first language
                    source_language = existing_langages[0]
                    base_text_data = self.__get_transmethod_text(method_name, source_language)
                    source_text = TransTxtParser.assemble_parsed_str_data(base_text_data)

                    # Translate and parse for storage
                    translated_text = self._translate_text(source_language,
                                                           lang_iso_code,
                                                           source_text)
                    text = TransTxtParser.parse_translate_string(translated_text)
                    self.__set_transmethod_text(method_name, lang_iso_code, text)
        else:
            pass


    def _define_translate_function_entry(self, brief_desc:str, params_list:list, ret_dict:dict,
                                         trans_base_lang:str = "en",
                                         trans_text:list = None)->dict:
        """!
        @brief Define a property string return function dictionary and
               return the entry to the caller

        @param brief_desc {string} Brief description of the function used in
                                  doxygen comment block generation
        @param params_list {list of dictionaries} List of the function parameter dictionary entrys
        @param ret_dict {dict} Return data dictionary
        @param translate_base_lang {string} ISO 639-1 language code for the input translate_text
                                            string
        @param translate_text {list} Parsed text of the message

        @return {'name':<string>, 'briefDesc':<string>, 'params':[],
                 'return':ParamRetDict.build_return_dict('text', ret_desc, False),
                 'translateDesc': {'base':<string> 'text':<string>}} Translate function dictionary
        """
        function_dict = {'briefDesc': brief_desc,
                         'params': params_list,
                         'return': ret_dict,
                         'translateDesc': self._define_translation_dict(trans_base_lang, trans_text)
                        }
        return function_dict

    def get_tranlate_method_list(self)->list:
        """!
        @brief Return a list of property method name strings
        @return list of strings - Names of the property methods
        """
        return list(self.string_jason_data['translateMethods'].keys())

    def get_tranlate_method_function_data(self, method_name:str)->tuple:
        """!
        @brief Return the input method_name data
        @return (tuple) - {string} Brief description of the property method for Doxygen comment,
                          {list of dictionaries} Parameter list (probably empty list),
                          {dictionary} Return data dictionary
        """
        entry = self.string_jason_data['translateMethods'][method_name]
        return entry['briefDesc'], entry['params'], entry['return']

    def get_tranlate_method_text_data(self, method_name:str, target_lang:str)->list:
        """!
        @brief Return the input method_name data
        @param method_name (string) Name of the method to retrive data from
        @param target_lang (string) Name of the target language to retrive
        @return (tuple list) - Parsed text list
        """
        return self.string_jason_data['translateMethods'][method_name]['translateDesc'][target_lang]

    def _input_iso_translate_code(self)->str:
        """!
        @brief Get the ISO 639-1 translate language code from user input and check for validity
        @return string - translate code
        """
        iso_translate_id = ""
        while iso_translate_id == "":
            prompt = "Enter original string ISO 639-1 translate language code " \
                     "(2 lower case characters): "
            trans_id = input(prompt).lower()

            # Check validity
            if re.match('^[a-z]{2}$', trans_id):
                # Valid name
                iso_translate_id = trans_id
            else:
                # invalid name
                print("Error: Only two characters a-z are allowed in the code, try again.")
        return iso_translate_id

    def _input_var_method_name(self, method_name:bool = False)->str:
        """!
        @brief Get the parameter or method name
        @param method_name {boolean} True if this is a method name call, else False (default)
        @return string - Validated name value
        """
        validated_name = ""
        while validated_name == "":
            if method_name:
                name = input("Enter method name: ")
            else:
                name = input("Enter parameter name: ")
            name.strip()

            # Check validity
            if re.match('^[a-zA-Z_][a-zA-Z0-9_]*$', name):
                # Valid name
                validated_name = name
            else:
                # invalid name
                print("Error: "+name+" is not a valid code name, try again.")
        return validated_name


    def _input_array_modifier(self, current_mod:int)->int:
        """!
        @brief Get the array size value from the user
        @param current_mod {int} Current type_mode value from ParamRetDict.build_dict_mod_value
        @return int - Modified type_mod value with array data added
        """
        retry = True
        final_mod = current_mod

        while retry:
            array_size = input("Size of the array in entries: ")
            try:
                int_array_size = int(array_size)
                if 0 < int_array_size < 65536:
                    final_mod = ParamRetDict.set_type_mod_array_size(current_mod, int_array_size)
                else:
                    print ("Error: must be a valid number between 1 and 65535")
            except TypeError:
                print ("Error: must be an integer value")

        return final_mod

    def _input_type_modifier(self)->int:
        """!
        @brief Get the parameter or method name
        @return int - ParamRetDict type_mod value,
        """
        # Check for list modification
        is_list_type = input("Is full type a list [y/n]:").lower()
        is_list = bool(is_list_type in ['y', 'yes'])

        # Check for pointer modification
        is_ptr_type = input("Is full type a pointer [y/n]:").lower()
        is_ptr = bool(is_ptr_type  in ['y', 'yes'])

        # Check for reference modification
        is_ref_type = input("Is full type a reference [y/n]:").lower()
        is_reference = bool(is_ref_type in ['y', 'yes'])

        # Check for undefined modification
        can_be_undef = input("Can value be undefined [y/n]:").lower()
        or_undef = bool(can_be_undef in ['y', 'yes'])

        # Generate basic modification
        type_mod = ParamRetDict.build_dict_mod_value(is_list, is_reference, is_ptr, or_undef)

        # Check for array modification
        is_array_type = input("Is full type an array [y/n]:").lower()
        if is_array_type in ['y', 'yes']:
            type_mod = self._input_array_modifier(type_mod)

        return type_mod

    def _input_param_return_type(self, return_type:bool = False)->tuple:
        """!
        @brief Get the parameter or method name
        @param return_type {boolean} True if this is a return type fetch, else False (default)
        @return tuple - String Validated name value,
                        Boolean is list,
                        Boolean is pointer type,
                        Boolean is reference type
        """
        var_type = ""
        while var_type == "":
            if return_type:
                prompt_str = "Enter return base type"
            else:
                prompt_str = "Enter parameter base type"
            ## @todo add float
            prompt_str += " [T(ext)|i(nteger)|u(nsigned)|s(ize)|c(ustom)]: "
            input_type = input(prompt_str).lower()

            # Check validity
            if input_type in ["s", "size"]:
                var_type = "size"
            elif input_type in ["t", "text", "string"]:
                var_type = "string"
            elif input_type in ["i", "integer", "int"]:
                var_type = "integer"
            elif input_type in ["u", "unsigned"]:
                var_type = "unsigned"
            elif input_type in ["f", "float"]:
                var_type = "float"
            elif input_type in ["c", "custom"]:
                # Note: Custom type class must have a stream operator method defined.
                custom_type = input("Enter custom type: ")
                if re.match('^[a-zA-Z_][a-zA-Z0-9_:]*$', custom_type):
                    # valid
                    var_type = custom_type
                else:
                    # invalid type
                    print (custom_type+" is not a valid code type name, try again.")
            else:
                # invalid name
                errstr = "Error: \""
                errstr += input_type
                errstr += "\" unknown. Please select one of the options from the menu."
                print(errstr)

        type_mod = self._input_type_modifier()
        return var_type, type_mod

    def _input_parameter_data(self)->dict:
        """!
        @brief Get input parameter data from user input
        @return dictionary - Param dictionary from  ParamRetDict.build_param_dict()
        """
        param_name = self._input_var_method_name()
        param_type, param_mod = self._input_param_return_type()
        param_desc = input("Enter brief parameter description for doxygen comment: ")
        return ParamRetDict.build_param_dict_with_mod(param_name, param_type, param_desc, param_mod)

    def _input_return_data(self)->dict:
        """!
        @brief Get the return data description from the user
        @return dictionary - Return dictionary from  ParamRetDict.build_return_dict()
        """
        return_type, return_mod = self._input_param_return_type(True)
        ret_desc = input("Enter brief description of the return value for doxygen comment: ")
        return ParamRetDict.build_return_dict_with_mod(return_type, ret_desc, return_mod)

    def update(self):
        """!
        @brief Update the JSON file with the current contents of self.lang_json_data
        """
        with open(self.filename, 'w', encoding='utf-8') as lang_json_file:
            json.dump(self.string_jason_data, lang_json_file, indent=2)

    def _validate_translate_string(self, param_list:list, test_string:str):
        """!
        @brief Get the translation string template for the new translate function

        @param param_list {list of dictionaries} List of parameter description dictionaries
                                                for this function
        @param test_string {string} String to check for validity

        @return boolean - True if string has all parameters correctly marked, else False
        @return number - Number of matched items
        @return number - Number of parameters found in the input string
        """
        # Construct the expected list
        expected_param_list = []
        for param in param_list:
            param_name = ParamRetDict.get_param_name(param)
            expected_param_list.append(param_name)

        # Break the string into it's component parts
        parsed_str_data = TransTxtParser.parse_translate_string(test_string)

        # Check the broken string counts
        mcount = 0
        pcount = 0
        for parsed_data in parsed_str_data:
            if TransTxtParser.is_parsed_param_type(parsed_data):
                pcount +=1
                if TransTxtParser.get_parsed_str_data(parsed_data) in expected_param_list:
                    mcount+=1

        status = bool((mcount == len(expected_param_list)) and (pcount == mcount))
        return status, mcount, pcount, parsed_str_data

    def _input_translate_string(self, param_list:list)->list:
        """!
        @brief Get the translation string template for the new translate function

        @param param_list {list of dictionaries} List of parameter description dictionaries
                                                for this function

        @return list - Validated TransTxtParser text/data list
        """
        # Build parameter list help string
        expected_param_help = ""
        prefix = ""
        for param in param_list:
            param_name = ParamRetDict.get_param_name(param)
            expected_param_help += prefix
            expected_param_help += '@'
            expected_param_help += param_name
            expected_param_help += '@'
            prefix = ", "

        # Get the translate string from the user
        strvalid = False
        translate_string = ""

        print("Enter translation template string. Use @paramName@ in the string to indicate")
        print("where the function parameters should be inserted.")
        print("Example with single input parameter name \"keyString\": ")
        print("  Found argument key @keyString@")

        while not strvalid:
            translate_string = input("String:")
            strvalid, mcount, pcount, parsestr = self._validate_translate_string(param_list,
                                                                                 translate_string)

            if not strvalid:
                if (len(param_list) > mcount) and (len(param_list) > pcount):
                    errstr = "Error: Template parameter missing, found "
                    errstr += str(mcount)
                    errstr += " of "
                    errstr += str(len(param_list))
                    errstr += " expected template parameters."
                    print (errstr)
                elif (len(param_list) > mcount) and (len(param_list) == pcount):
                    errstr = "Error: Template parameter(s) misspelled, spelling error count "
                    errstr += str(pcount-mcount)
                    print (errstr)
                elif (len(param_list) == mcount) and (len(param_list) < pcount):
                    errstr = "Error: Too many template parameters in input string, expected "
                    errstr += str(mcount)
                    errstr += " found "
                    errstr += str(pcount)
                    print (errstr)
                else:
                    print ("Error: Translation template parameter list does not match expected.")
                    fnd_str = "   Found "
                    fnd_str += str(pcount)
                    fnd_str += " parameters of expected "
                    fnd_str += str(len(param_list))
                    fnd_str += " parameters in string."
                    print (fnd_str)
                    matchstr = "   Matched "
                    matchstr += str(mcount)
                    matchstr += " parameters of expected "
                    matchstr += str(len(param_list))
                    matchstr += " parameters in string."
                    print (matchstr)

                print("User input template:")
                print("    "+translate_string)
                print("Expected parameter list:")
                print("    "+expected_param_help)

        return parsestr

    def new_translate_method_entry(self, language_list:LanguageDescriptionList = None,
                                   override:bool = False)->bool:
        """!
        @brief Define and add a new translate string return function dictionary
               to the list of translate functions
        @param language_list {LanguageDescriptionList | None} Supported language
                                                              description data or None
        @param override {boolean} True = Override existing without asking
        @return boolean True if new entry was written, else false
        """
        new_entry = {}
        entry_correct = False

        while not entry_correct:
            method_name = self._input_var_method_name(True)
            method_desc = input("Enter brief function description for doxygen comment: ")

            param_list = []
            pcount = int(input("Enter parameter count? [0-n]: "))
            while pcount > 0:
                param_list.append(self._input_parameter_data())
                pcount -= 1

            return_dict = self._input_return_data()

            language_base = self._input_iso_translate_code()
            translate_string = self._input_translate_string(param_list)
            new_entry = self._define_translate_function_entry(method_desc,
                                                              param_list,
                                                              return_dict,
                                                              language_base,
                                                              translate_string)

            # Print entry for user to inspect
            print("New Entry:")
            print(new_entry)
            commit = input("Is this correct? [Y/N]").upper()
            if commit in ['Y', "YES"]:
                entry_correct = True

        # Test existing for match
        commit_flag = self._get_commit_flag(method_name,
                                            self.string_jason_data['translateMethods'].keys(),
                                            override)
        if commit_flag:
            self.string_jason_data['translateMethods'][method_name] = new_entry
            self._translate_method_text(method_name, language_list)

        return commit_flag

    def add_translate_method_entry(self, method_name:str, method_desc:str, param_list:list,
                                   return_dict:dict, iso_lang_code:str, translate_string:str,
                                   override:bool = False,
                                   language_list:LanguageDescriptionList = None)->bool:
        """!
        @brief Add a new translate string return function dictionary
               to the list of translate functions
        @param method_name {string} Name of the function
        @param method_desc {string} Brief description of the function for doxygen comment
                                    generation
        @param param_list {list of dictionaries} List of the input parameter description
                                                 dictionaries
        @param return_dict {dict} Return dictionary definition
        @param iso_lang_code {string} ISO 639-1 language code of the input translate_string
        @param translate_string {string} String to generate translations for
        @param override {boolean} True = Override existing without asking
        @param language_list {LanguageDescriptionList | None} Supported language description
                                                              data or None
        @return boolean True if new entry was written, else false
        """
        status, mcount, pcount, parsed_str = self._validate_translate_string(param_list,
                                                                             translate_string)
        if not status:
            err_str = "Error: Invalid translation string: "
            err_str += translate_string
            err_str += ". pcount= "
            err_str += str(pcount)
            err_str += " mcount= "+str(mcount)
            print (err_str)
            return False

        new_entry = self._define_translate_function_entry(method_desc,
                                                          param_list,
                                                          return_dict,
                                                          iso_lang_code,
                                                          parsed_str)

        commit_flag = True
        if method_name in self.string_jason_data['translateMethods'].keys():
            # Determine if we should overwrite existing
            commit_flag = self._get_commit_over_write_flag(method_name, override)

        if commit_flag:
            self.string_jason_data['translateMethods'][method_name] = new_entry
            self._translate_method_text(method_name, language_list)

        return commit_flag

    def _get_property_return_data(self):
        """!
        @brief Get the property function return data and property name
        @return string, string, string, string - Language description property name,
                                                 Method name,
                                                 Method return type,
                                                 Return type description for Doxygen comment
                                                 True if return is a list, else False
        """
        property_options = LanguageDescriptionList.get_language_property_list()

        print ("Select language property, from options:")
        option_text = ""
        option_prefix = "    "
        max_index = 0
        for index, property_id in enumerate(property_options):
            option_text += option_prefix
            option_text += str(index)+": "
            option_text += property_id
            option_prefix = ", "
            max_index += 1
        print (option_text)

        propid = None
        while propid is None:
            property_index = int(input("Enter property [0 - "+str(max_index-1)+"]: "))
            if 0 <= property_index < max_index:
                propid = property_options[property_index]
            else:
                print ("Valid input values are 0 to "+str(max_index-1)+", try again")

        rtype, rdesc, is_list = LanguageDescriptionList.get_language_property_return_data(propid)
        method_name = LanguageDescriptionList.get_language_property_method_name(propid)
        return propid, method_name, rtype, rdesc, is_list

    def new_property_method_entry(self, override:bool = False)->bool:
        """!
        @brief Define and add a property string return function dictionary and
               add it to the list of translate functions
        @param override {boolean} True = Override existing without asking
        @return boolean True if new entry was written, else false
        """
        new_entry = {}
        entry_correct = False

        while not entry_correct:
            property_name, method_name, return_type, return_desc, is_list = self._get_property_return_data() # pylint: disable=line-too-long
            method_desc = "Get the "+return_desc+" for this object"

            new_entry = self._define_property_function_entry(property_name,
                                                             method_desc,
                                                             return_type,
                                                             return_desc,
                                                             is_list)

            # Print entry for user to inspect
            print(method_name+":")
            print(new_entry)
            commit = input("Is this correct? [Y/N]").upper()
            if commit in ['Y', "YES"]:
                entry_correct = True

        # Check for existing for match
        commit_flag = self._get_commit_flag(method_name,
                                            self.string_jason_data['propertyMethods'].keys(),
                                            override)
        if commit_flag:
            self.string_jason_data['propertyMethods'][method_name] = new_entry

        return commit_flag

    def add_property_method_entry(self, property_name:str, override:bool = False)->bool:
        """!
        @brief Add a new translate string return function dictionary
               to the list of translate functions
        @param property_name {string} LanguageDescriptionList.get_language_property_list()
                                      property key
        @param override {boolean} True = Override existing without asking
        @return boolean True if new entry was written, else false
        """
        # Make sure property exists in the language data
        property_list = LanguageDescriptionList.get_language_property_list()
        commit_flag = False

        # Property exists, generate the new entry
        if property_name in property_list:
            return_type, return_desc, is_list = LanguageDescriptionList.get_language_property_return_data(property_name) # pylint: disable=line-too-long
            method_desc = "Get the "+return_desc+" for this object"
            method_name = LanguageDescriptionList.get_language_property_method_name(property_name)

            new_entry = self._define_property_function_entry(property_name, method_desc,
                                                             return_type, return_desc, is_list)

            commit_flag = self._get_commit_flag(method_name,
                                                self.string_jason_data['propertyMethods'].keys(),
                                                override)
            if commit_flag:
                # Add the entry
                self.string_jason_data['propertyMethods'][method_name] = new_entry

        return commit_flag

    def update_tranlations(self, json_lang_data:LanguageDescriptionList = None):
        """!
        @brief Update the translation strings in the translation methods
        @param json_lang_data {LanguageDescriptionList} Updated language list defintions
        """
        method_list = self.get_tranlate_method_list()
        for method_name in method_list:
            self._translate_method_text(method_name, json_lang_data)
