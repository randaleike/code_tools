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

class TranslationTextParser(object):
    """!
    Translation text helper functions
    """
    ## Text string marker
    parsed_type_text    = 'text'
    ## Parameter name marker
    parsed_type_param   = 'param'
    ## Special character marker
    parsed_type_special = 'special'

    def __init__(self):
        """!
        @brief TranslationTextParser constructor
        """
        pass

    @staticmethod
    def make_text_entry(text_block:str)->tuple:
        """!
        @brief Make a parsed text tuple object
        @param text_block {string} Text string for the tuple
        @return tuple - (TranslationTextParser.parsed_type_text, text_block)
        """
        return (TranslationTextParser.parsed_type_text, text_block)

    @staticmethod
    def make_special_char_entry(text_block:str)->tuple:
        """!
        @brief Make a special character tuple object
        @param text_block {string} Special character for the tuple
        @return tuple - (TranslationTextParser.parsed_type_special, text_block)
        """
        return (TranslationTextParser.parsed_type_special, text_block[0])

    @staticmethod
    def make_param_entry(param_name:str)->tuple:
        """!
        @brief Make a parameter name tuple object
        @param param_name {string} Special character for the tuple
        @return tuple - (TranslationTextParser.parsed_type_param, param_name)
        """
        return (TranslationTextParser.parsed_type_param, param_name)

    @staticmethod
    def parse_text_block(text_block:str)->list:
        """!
        @brief Convert the input string to an output string stream
        @param text_block {string} String to convert
        @return list of dictionaries - List of dictionary entries descibing the parsed string
        """
        match_list = re.finditer(r'\\|\"', text_block)

        string_list = []
        previous_end = 0
        for match_data in match_list:
            # Add text data prior to first match if any
            if match_data.start() > previous_end:
                raw_text = r'{}'.format(text_block[previous_end:match_data.start()])
                string_list.append(TranslationTextParser.make_text_entry(raw_text))

            # Add the matched parameter
            string_list.append(TranslationTextParser.make_special_char_entry(match_data.group()))
            previous_end = match_data.end()

        # Add the trailing string
        if previous_end < len(text_block):
            raw_text = r'{}'.format(text_block[previous_end:])
            string_list.append(TranslationTextParser.make_text_entry(raw_text))

        return string_list

    @staticmethod
    def parse_translate_string(base_string:str)->list:
        """!
        @brief Convert the input string to an output string stream
        @param base_string {string} String to convert
        @return list of tuples - List of tuples descibing the parsed string
                                 tuple[0] = type, TranslationTextParser.parsed_type_text or TranslationTextParser.parsed_type_param
                                 tuple[1] = data, if TranslationTextParser.parsed_type_text = text string
                                                  if TranslationTextParser.parsed_type_param = parameter name
        """
        match_list = re.finditer(r'@[a-zA-Z_][a-zA-Z0-9_]*@', base_string)

        string_list = []
        previous_end = 0
        for match_data in match_list:
            # Add text data prior to first match if any
            if match_data.start() > previous_end:
                raw_text = r'{}'.format(base_string[previous_end:match_data.start()])
                string_list.extend(TranslationTextParser.parse_text_block(raw_text))

            # Add the matched parameter
            string_list.append(TranslationTextParser.make_param_entry(match_data.group()[1:-1]))
            previous_end = match_data.end()

        # Add the trailing string
        if previous_end < len(base_string):
            raw_text = r'{}'.format(base_string[previous_end:])
            string_list.extend(TranslationTextParser.parse_text_block(raw_text))

        return string_list

    @staticmethod
    def assemble_parsed_str_data(string_tuple_list:list)->str:
        """!
        @brief Assemble the input string description tuple list into a translation string
        @param string_tuple_list (list) List of string description tuples
        @return string - Assempled text string ready for input into a language translation engine
        """
        return_text = ""
        for desc_type, desc_data in string_tuple_list:
            if TranslationTextParser.parsed_type_text == desc_type:
                return_text += desc_data
            elif TranslationTextParser.parsed_type_param == desc_type:
                return_text += '@'
                return_text += desc_data
                return_text += '@'
            elif TranslationTextParser.parsed_type_special == desc_type:
                return_text += desc_data
            else:
                raise TypeError("Unknown string description tuple type: "+desc_type)

        return return_text

    @staticmethod
    def assemble_stream(string_tuple_list:list, stream_operator:str = "<<")->str:
        """!
        @brief Assemble the input string description tuple list into a translation string
        @param string_tuple_list (list) List of string description tuples
        @param stream_operator (string) Language specific stream operator
        @return string - Assempled text string ready for input into a language translation engine
        """
        return_text = ""
        string_open = False

        for desc_type, desc_data in string_tuple_list:
            if TranslationTextParser.parsed_type_text == desc_type:
                if not string_open:
                    return_text += " "
                    return_text += stream_operator
                    return_text += " \""
                    string_open = True
                return_text += desc_data
            elif TranslationTextParser.parsed_type_param == desc_type:
                if string_open:
                    return_text += "\" "
                    return_text += stream_operator
                    return_text += " "
                    string_open = False
                return_text += desc_data
            elif TranslationTextParser.parsed_type_special == desc_type:
                if not string_open:
                    return_text += " "
                    return_text += stream_operator
                    return_text += " \""
                    string_open = True
                return_text += "\\"+desc_data
            else:
                raise TypeError("Unknown string description tuple type: "+desc_type)

        # Close the open string if present
        if string_open:
            return_text += "\""
            string_open = False
        return return_text

    @staticmethod
    def assemble_test_return_string(string_tuple_list:list, value_xlate_dict:dict)->str:
        """!
        @brief Assemble the input string description tuple list into a translation string
        @param string_tuple_list (list) List of string description tuples
        @param value_xlate_dict (dict) Dictionary of param names and expected values
        @return string - Assempled text string ready for input into a language translation
                         expected string
        """
        return_text = ""
        for desc_type, desc_data in string_tuple_list:
            if TranslationTextParser.parsed_type_text == desc_type:
                return_text += desc_data
            elif TranslationTextParser.parsed_type_param == desc_type:
                value, is_text = value_xlate_dict[desc_data]
                return_text += value
            elif TranslationTextParser.parsed_type_special == desc_type:
                return_text += "\\"+desc_data
            else:
                raise TypeError("Unknown string description tuple type: "+desc_type)
        return return_text

    @staticmethod
    def is_parsed_text_type(parsed_tuple:tuple)->bool:
        """!
        @brief Check if the input pget_parsed_str_dataarsed translation tuple is a text type
        @return boolean - True if tuple[0] == TranslationTextParser.parsed_type_text
                          else False
        """
        if parsed_tuple[0] == TranslationTextParser.parsed_type_text:
            return True
        else:
            return False

    @staticmethod
    def is_parsed_param_type(parsed_tuple:tuple)->bool:
        """!
        @brief Check if the input parsed translation tuple is a parameter type
        @return boolean - True if tuple[0] == TranslationTextParser.parsed_type_param
                          else False
        """
        if parsed_tuple[0] == TranslationTextParser.parsed_type_param:
            return True
        else:
            return False

    @staticmethod
    def is_parsed_special_type(parsed_tuple:tuple)->bool:
        """!
        @brief Check if the input parsed translation tuple is a special character type
        @return boolean - True if tuple[0] == TranslationTextParser.parsed_type_param
                          else False
        """
        if parsed_tuple[0] == TranslationTextParser.parsed_type_special:
            return True
        else:
            return False

    @staticmethod
    def get_parsed_str_data(parsed_tuple:tuple)->bool:
        """!
        @brief Get the tuple string data field
        @return string - pared_tuple data field
        """
        return parsed_tuple[1]


class StringClassDescription(object):
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
            lang_json_file = open(self.filename, 'r', encoding='utf-8')
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
            if ((commit == 'Y') or (commit == "YES")):
                commit_flag = True
        return commit_flag

    def _get_commit_new_flag(self, entry_name:str)->bool:
        """!
        @brief Determine if the user is ready to commit the new entry
        @param entry_name {string} Name of the method that will be added
        """
        commit = input("Add new "+entry_name+" entry? [Y/N]").upper()
        if ((commit == 'Y') or (commit == "YES")):
            return True
        else:
            return False

    def _get_commit_flag(self, entry_name:str, entry_keys:list, override:bool = False)->bool:
        """!
        @brief Determine if the user is ready to commit the new entry
        @param entry_name {string} Name of the method that will be added
        @param entry_keys {list of keys} List of the existing entry keys
        @param override {boolean} True = force commit, False = ask user
        """
        if entry_name in entry_keys:
            return self._get_commit_over_write_flag(entry_name, override)
        else:
            return self._get_commit_new_flag(entry_name)

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

    def get_base_class_name_with_namespace(self, namespace_name:str, scope_operator:str = '::')->str:
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
            return self.string_jason_data['baseClassName']
        else:
            return self.string_jason_data['baseClassName']+language_name.capitalize()

    def get_language_class_name_with_namespace(self, namespace_name:str, scope_operator:str = '::', language_name:str = None)->str:
        """!
        @brief Return the base class name
        @param namespace_name {string} Namespace name
        @param scope_operator {string} Programming language scope resolution operator
        @param language_name {string} Language name to append to the base class name or None
        @return string Base sting class name
        """
        return namespace_name+scope_operator+self.get_language_class_name(language_name)

    def set_namespace_name(self, namespace:str):
        self.string_jason_data['namespace'] = namespace

    def get_namespace_name(self):
        return self.string_jason_data['namespace']

    def set_dynamic_compile_switch(self, switch:str):
        self.string_jason_data['dynamicCompileSwitch'] = switch

    def get_dynamic_compile_switch(self):
        return self.string_jason_data['dynamicCompileSwitch']

    def _define_property_function_entry(self, property_name:str = "", brief_desc:str = "",
                                     ret_type:str = "", ret_desc:str = "", is_list:bool = False)->dict:
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

    def _define_translation_dict(self, translate_base_lang:str = "en", translate_text:list = None)->dict:
        """!
        @brief Create a translation dictionary
        @param translate_base_lang {string} ISO 639-1 language code for the input translate_text string
        @param translate_text {list} Parsed text of the message
        @return dictionary - {'base':<translate_base_lang>, 'text':<translate_text>} Translate method translation string dictionary
        """
        return {translate_base_lang: translate_text}

    def add_manual_translation(self, method_name:str, base_lang:str = "en", text_data:list = None)->bool:
        """!
        @brief Add language text to the function definition
        @param method_name {string} Translation method name to add the language text to
        @param base_lang {sting} ISO 639-1 language code for the input text_data string
        @param text_data {list} Parsed text of the message
        @return boolean - True if it was added, else false
        """
        if method_name in self.string_jason_data['translateMethods']:
            if text_data is not None:
                self.string_jason_data['translateMethods'][method_name]['translateDesc'][base_lang] = text_data
                return True
            else:
                return False
        else:
            return False

    def _translate_text(self, source_lang:str, target_lang:str, text:str)->str:
        """!
        @brief Translate the input text
        @param source_lang {string} ISO 639-1 language code of the input text
        @param target_lang {string} ISO 639-1 language code for the output text
        @param text {string} text to translate
        @return string - Translated text
        """
        from google.cloud import translate_v2
        if self.trans_client is None:
            self.trans_client = translate_v2.Client()

        if isinstance(text, bytes):
            text = text.decode("utf-8")

        translated_textData = self.trans_client.translate(text,
                                                          target_language=target_lang,
                                                          format_='text',
                                                          source_language=source_lang,
                                                          model='nmt')
        raw_translated_text = translated_textData['translatedText']
        return raw_translated_text

    def _translate_method_text(self, method_name:str, json_lang_data:LanguageDescriptionList = None):
        """!
        @brief Add language text to the function definition
        @param method_name {string} Translation method name to add the language text to
        @param json_lang_data {LanguageDescriptionList} Language list data
        """
        if json_lang_data is not None:
            # Get the list of supported languages and the list of existing translations
            language_list = json_lang_data.get_language_list()
            existing_langages = list(self.string_jason_data['translateMethods'][method_name]['translateDesc'])

            # Determine if any language translations are missing
            for language in language_list:
                lang_iso_code = json_lang_data.get_language_iso_code_data(language)
                if lang_iso_code not in existing_langages:
                    # Use the first language
                    source_language = existing_langages[0]
                    base_text_data = self.string_jason_data['translateMethods'][method_name]['translateDesc'][source_language]
                    source_text = TranslationTextParser.assemble_parsed_str_data(base_text_data)

                    # Translate and parse for storage
                    translated_text = self._translate_text(source_language, lang_iso_code, source_text)
                    translated_textData = TranslationTextParser.parse_translate_string(translated_text)
                    self.string_jason_data['translateMethods'][method_name]['translateDesc'][lang_iso_code] = translated_textData
        else:
            pass


    def _define_translate_function_entry(self, brief_desc:str = "", params_list:list = [], ret_dict:dict = {},
                                      translate_base_lang:str = "en", translate_text:list = None)->dict:
        """!
        @brief Define a property string return function dictionary and
               return the entry to the caller

        @param brief_desc {string} Brief description of the function used in
                                  doxygen comment block generation
        @param params_list {list of dictionaries} List of the function parameter dictionary entrys
        @param ret_dict {dict} Return data dictionary
        @param translate_base_lang {string} ISO 639-1 language code for the input translate_text string
        @param translate_text {list} Parsed text of the message

        @return {'name':<string>, 'briefDesc':<string>, 'params':[],
                 'return':ParamRetDict.build_return_dict('text', ret_desc, False),
                 'translateDesc': {'base':<string> 'text':<string>}} Translate function dictionary
        """
        function_dict = {'briefDesc': brief_desc,
                         'params': params_list,
                         'return': ret_dict,
                         'translateDesc': self._define_translation_dict(translate_base_lang, translate_text)
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

    def get_tranlate_method_text_data(self, method_name:str, target_language:str)->list:
        """!
        @brief Return the input method_name data
        @param method_name (string) Name of the method to retrive data from
        @param target_language (string) Name of the target language to retrive
        @return (tuple list) - Parsed text list
        """
        return self.string_jason_data['translateMethods'][method_name]['translateDesc'][target_language]

    def _input_iso_translate_code(self)->str:
        """!
        @brief Get the ISO 639-1 translate language code from user input and check for validity
        @return string - translate code
        """
        iso_translate_id = ""
        while(iso_translate_id == ""):
            trans_id = input("Enter original string ISO 639-1 translate language code (2 lower case characters): ").lower()

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
        while(validated_name == ""):
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
        while True:
            array_size = input("Size of the array in entries: ")
            try:
                int_array_size = int(array_size)
                if (int_array_size > 0) and (int_array_size < 65536):
                    return ParamRetDict.set_type_mod_array_size(current_mod, int_array_size)
                else:
                    print ("Error: must be a valid number between 1 and 65535")
            except:
                print ("Error: must be an integer value")

    def _input_type_modifier(self)->int:
        """!
        @brief Get the parameter or method name
        @return int - ParamRetDict type_mod value,
        """
        # Check for list modification
        is_listType = input("Is full type a list [y/n]:").lower()
        if (is_listType == 'y') or (is_listType == 'yes'):
            is_list = True
        else:
            is_list = False

        # Check for pointer modification
        is_ptrType = input("Is full type a pointer [y/n]:").lower()
        if (is_ptrType == 'y') or (is_ptrType == 'yes'):
            is_ptr = True
        else:
            is_ptr = False

        # Check for reference modification
        is_ref_type = input("Is full type a reference [y/n]:").lower()
        if (is_ref_type == 'y') or (is_ref_type == 'yes'):
            is_reference = True
        else:
            is_reference = False

        # Check for undefined modification
        can_beUndef = input("Can value be undefined [y/n]:").lower()
        if (can_beUndef == 'y') or (can_beUndef == 'yes'):
            or_undef = True
        else:
            or_undef = False

        # Generate basic modification
        type_mod = ParamRetDict.build_dict_mod_value(is_list, is_reference, is_ptr, or_undef)

        # Check for array modification
        is_array_type = input("Is full type an array [y/n]:").lower()
        if (is_array_type == 'y') or (is_array_type == 'yes'):
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
        while(var_type == ""):
            if return_type:
                prompt_str = "Enter return base type"
            else:
                prompt_str = "Enter parameter base type"

            input_type = input(prompt_str+" [T(ext)|i(nteger)|u(nsigned)|s(ize)|c(ustom)]: ").lower()

            # Check validity
            if (input_type == "s") or (input_type=="size"):
                var_type = "size"
            elif (input_type == "t") or (input_type=="text") or (input_type=="string"):
                var_type = "string"
            elif (input_type == "i") or (input_type=="integer") or (input_type=="int"):
                var_type = "integer"
            elif (input_type == "u") or (input_type=="unsigned"):
                var_type = "unsigned"
            elif (input_type == "c") or (input_type=="custom"):
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
                print("Error: \""+input_type+"\" unknown. Please select one of the options from the menu.")

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
        parsed_str_data = TranslationTextParser.parse_translate_string(test_string)

        # Check the broken string counts
        match_count = 0
        param_count = 0
        for parsed_data in parsed_str_data:
            if TranslationTextParser.is_parsed_param_type(parsed_data):
                param_count +=1
                if TranslationTextParser.get_parsed_str_data(parsed_data) in expected_param_list:
                    match_count+=1

        if (match_count == len(expected_param_list)) and (param_count == match_count):
            # Return success
            return True, match_count, param_count, parsed_str_data
        else:
            # Return failure
            return False, match_count, param_count, parsed_str_data

    def _input_translate_string(self, param_list:list)->list:
        """!
        @brief Get the translation string template for the new translate function

        @param param_list {list of dictionaries} List of parameter description dictionaries
                                                for this function

        @return list - Validated TranslationTextParser text/data list
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
        string_valid = False
        translate_string = ""

        print("Enter translation template string. Use @paramName@ in the string to indicate where the ")
        print("function parameters should be inserted.")
        print("Example with single input parameter name \"keyString\": Found argument key @keyString@")

        while not string_valid:
            translate_string = input("String:")
            string_valid, match_count, param_count, parsed_string = self._validate_translate_string(param_list, translate_string)

            if not string_valid:
                if (len(param_list) > match_count) and (len(param_list) > param_count):
                    print ("Error: Template parameter missing, found "+str(match_count)+" of "+str(len(param_list))+" expected template parameters.")
                elif (len(param_list) > match_count) and (len(param_list) == param_count):
                    print ("Error: Template parameter(s) misspelled, spelling error count "+str(param_count-match_count))
                elif (len(param_list) == match_count) and (len(param_list) < param_count):
                    print ("Error: Too many template parameters in input string, expected "+str(match_count)+" found "+str(param_count))
                else:
                    print ("Error: Translation template parameter list does not match expected.")
                    print ("   Found "+str(param_count)+" parameters of expected "+str(len(param_list))+" parameters in string.")
                    print ("   Matched "+str(match_count)+" parameters of expected "+str(len(param_list))+" parameters in string.")
                print("User input template:")
                print("    "+translate_string)
                print("Expected parameter list:")
                print("    "+expected_param_help)

        return parsed_string

    def new_translate_method_entry(self, language_list:LanguageDescriptionList = None, override:bool = False)->bool:
        """!
        @brief Define and add a new translate string return function dictionary
               to the list of translate functions
        @param language_list {LanguageDescriptionList | None} Supported language description data or None
        @param override {boolean} True = Override existing without asking
        @return boolean True if new entry was written, else false
        """
        new_entry = {}
        entry_correct = False

        while not entry_correct:
            method_name = self._input_var_method_name(True)
            method_desc = input("Enter brief function description for doxygen comment: ")

            param_list = []
            param_count = int(input("Enter parameter count? [0-n]: "))
            while(param_count > 0):
                param_list.append(self._input_parameter_data())
                param_count -= 1

            return_dict = self._input_return_data()

            language_base = self._input_iso_translate_code()
            translate_string = self._input_translate_string(param_list)
            new_entry = self._define_translate_function_entry(method_desc, param_list, return_dict, language_base, translate_string)

            # Print entry for user to inspect
            print("New Entry:")
            print(new_entry)
            commit = input("Is this correct? [Y/N]").upper()
            if ((commit == 'Y') or (commit == "YES")):
                entry_correct = True

        # Test existing for match
        commit_flag = self._get_commit_flag(method_name, self.string_jason_data['translateMethods'].keys(), override)
        if commit_flag:
            self.string_jason_data['translateMethods'][method_name] = new_entry
            self._translate_method_text(method_name, language_list)

        return commit_flag

    def add_translate_method_entry(self, method_name:str, method_desc:str, param_list:list,
                                return_dict:dict, iso_lang_code:str, translate_string:str,
                                override:bool = False, language_list:LanguageDescriptionList = None)->bool:
        """!
        @brief Add a new translate string return function dictionary
               to the list of translate functions
        @param method_name {string} Name of the function
        @param method_desc {string} Brief description of the function for doxygen comment generation
        @param param_list {list of dictionaries} List of the input parameter description dictionaries
        @param return_dict {dict} Return dictionary definition
        @param iso_lang_code {string} ISO 639-1 language code of the input translate_string
        @param translate_string {string} String to generate translations for        @return boolean True if new entry was written, else false

        @param override {boolean} True = Override existing without asking
        @param language_list {LanguageDescriptionList | None} Supported language description data or None
        @return boolean True if new entry was written, else false
        """
        status, match_count, param_count, parsed_str_data = self._validate_translate_string(param_list, translate_string)
        if not status:
            print ("Error: Invalid translation string: "+translate_string+". param_count= "+str(param_count)+" match_count= "+str(match_count))
            return False

        new_entry = self._define_translate_function_entry(method_desc, param_list, return_dict, iso_lang_code, parsed_str_data)

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

        property_id = None
        while property_id is None:
            property_index = int(input("Enter property [0 - "+str(max_index-1)+"]: "))
            if (property_index >= 0) and (property_index < max_index):
                property_id = property_options[property_index]
            else:
                print ("Valid input values are 0 to "+str(max_index-1)+", try again")

        return_type, return_desc, is_list = LanguageDescriptionList.get_language_property_return_data(property_id)
        method_name = LanguageDescriptionList.get_language_property_method_name(property_id)
        return property_id, method_name, return_type, return_desc, is_list

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
            property_name, method_name, return_type, return_desc, is_list = self._get_property_return_data()
            method_desc = "Get the "+return_desc+" for this object"

            new_entry = self._define_property_function_entry(property_name, method_desc, return_type, return_desc, is_list)

            # Print entry for user to inspect
            print(method_name+":")
            print(new_entry)
            commit = input("Is this correct? [Y/N]").upper()
            if ((commit == 'Y') or (commit == "YES")):
                entry_correct = True

        # Check for existing for match
        commit_flag = self._get_commit_flag(method_name, self.string_jason_data['propertyMethods'].keys(), override)
        if commit_flag:
            self.string_jason_data['propertyMethods'][method_name] = new_entry

        return commit_flag

    def add_property_method_entry(self, property_name:str, override:bool = False)->bool:
        """!
        @brief Add a new translate string return function dictionary
               to the list of translate functions
        @param property_name {string} LanguageDescriptionList.get_language_property_list() property key
        @param override {boolean} True = Override existing without asking
        @return boolean True if new entry was written, else false
        """
        # Make sure property exists in the language data
        property_list = LanguageDescriptionList.get_language_property_list()
        commit_flag = False

        # Property exists, generate the new entry
        if property_name in property_list:
            return_type, return_desc, is_list = LanguageDescriptionList.get_language_property_return_data(property_name)
            method_desc = "Get the "+return_desc+" for this object"
            method_name = LanguageDescriptionList.get_language_property_method_name(property_name)

            new_entry = self._define_property_function_entry(property_name, method_desc, return_type, return_desc, is_list)

            commit_flag = self._get_commit_flag(method_name, self.string_jason_data['propertyMethods'].keys(), override)
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
