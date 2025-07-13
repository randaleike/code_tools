"""@package langstringautogen
Utility to create a json language description list
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

class LanguageDescriptionList():
    """!
    Language description list data
    """
    def __init__(self, lang_list_file_name = None):
        """!
        @brief LanguageDescriptionList constructor

        @param lang_list_file_name (string) - Name of the json file containing
                                           the language description data
        """
        ## Path/file name of the JSON language decription file
        self.filename = "jsonLanguageDescriptionList.json"
        ## JSON language description data from the file
        self.lang_json_data = {'default':{'name':"english", 'isoCode':"en"}, 'languages':{}}

        if lang_list_file_name is not None:
            self.filename = lang_list_file_name

        try:
            lang_json_file = open(self.filename, 'r', encoding='utf-8') # pylint: disable=consider-using-with
        except FileNotFoundError:
            self.lang_json_data =  {'default':{'name':"english", 'isoCode':"en"}, 'languages':{}}
        else:
            self.lang_json_data = json.load(lang_json_file)
            lang_json_file.close()

    def clear(self):
        """!
        @brief Reset all data to the default state
        """
        self.lang_json_data = {'default':{'name':"english", 'isoCode':"en"}, 'languages':{}}

    def _print_error(self, error_str:str):
        """!
        @brief Output the error text to the console
        @param error_str {string} Error text message
        """
        print ("Error: "+error_str)

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

    def update(self):
        """!
        @brief Update the JSON file with the current contents of self.lang_json_data
        """
        with open(self.filename, 'w', encoding='utf-8') as lang_json_file:
            json.dump(self.lang_json_data, lang_json_file, indent=2)

    def set_default(self, lang_name:str):
        """!
        @brief Set the default language
        @param lang_name (string) - Language name to use default if detection fails
        """
        if lang_name.lower() in self.lang_json_data['languages'].keys():
            default_dict = {'name':lang_name,
                            'isoCode':self.lang_json_data['languages'][lang_name]['isoCode']}
            self.lang_json_data['default'] = default_dict
        else:
            self._print_error("You must select a current language as the default.")
            print("Available languages:")
            for available_name in list(self.lang_json_data['languages']):
                print("  "+available_name)

    def get_default_data(self)->tuple:
        """!
        @brief Get the default language data
        @return tuple (string, string) - Default lauguage (entry name, ISO 639 set 3 language code)
        """
        default_lang = self.lang_json_data['default']['name']
        default_iso_code = self.lang_json_data['default']['isoCode']
        return default_lang, default_iso_code

    @staticmethod
    def _create_language_entry(linux_env_code:str, linux_region_list:list,
                               windows_lang_id:list, windows_region_list:list,
                               iso_639_code:str, compile_switch:str)->dict:
        """!
        @brief Create a language dictionart entry

        @param linux_env_code (string) - linux LANG environment value for this language
        @param linux_region_list (list of strings) - Linux LANG region codes for this language
        @param windows_lang_id (list of numbers) - Windows LANGID & 0xFF value(s) for this language
        @param windows_region_list (list of numbers) - Windows LANGID value(s) for this language
        @param iso_639_code (string) - ISO 639 set 3 language code
        @param compile_switch (string) - Language compile switch

        @return language dictionary object
        """
        lang_data = [('LANG', linux_env_code),
                    ('LANG_regions', linux_region_list),
                    ('LANGID', windows_lang_id),
                    ('LANGID_regions', windows_region_list),
                    ('isoCode', iso_639_code),
                    ('compileSwitch', compile_switch)]
        lang_entry = dict(lang_data)
        return lang_entry

    def get_language_list(self)->list:
        """!
        @brief Get a list of the current defined languages
        @return list of strings - Current ['languages'] keys
        """
        return list(self.lang_json_data['languages'].keys())

    def get_language_property_data(self, language_name:str, property_name:str):
        """!
        @brief Get a list of the current defined languages
        @param language_name {string} Language entry key to fetch the ptoperty value from
        @param property_name {string} Name of the property to get the value of
        @return any - property value
        """
        return self.lang_json_data['languages'][language_name][property_name]

    def get_language_iso_code_data(self, language_name:str)->str:
        """!
        @brief Get the ISO 639 code data for the given entry_name language
        @param language_name {string} Language entry key to fetch the ptoperty value from
        @return string - Current ['languages'][entry_name]['isoCode'] data
        """
        return self.lang_json_data['languages'][language_name]['isoCode']

    def get_language_lang_data(self, language_name:str)->tuple:
        """!
        @brief Get the LANG and LANG_regions data for the given entry_name language
        @param language_name {string} Language entry key to fetch the ptoperty value from
        @return tuple (string, list of strings) - Current ['languages'][entry_name]['LANG'] data,
                                                  and ['languages'][entry_name]['LANGID_regions']
                                                  data
        """
        lang_code = self.lang_json_data['languages'][language_name]['LANG']
        region_list = self.lang_json_data['languages'][language_name]['LANG_regions']
        return lang_code, region_list

    def get_language_langid_data(self, language_name:str)->tuple:
        """!
        @brief Get the LANGID and LANGID_regions data for the given entry_name language
        @param language_name {string} Language entry key to fetch the ptoperty value from
        @return tuple (list of numbers, list of numbers) -
                Current ['languages'][entry_name]['LANGID'] data,
                and ['languages'][entry_name]['LANGID_regions'] data
        """
        lang_code = self.lang_json_data['languages'][language_name]['LANGID']
        region_list = self.lang_json_data['languages'][language_name]['LANGID_regions']
        return lang_code, region_list

    def get_language_compile_switch_data(self, language_name:str)->str:
        """!
        @brief Get the compile_switch data for the given entry_name language
        @param language_name {string} Language entry key to fetch the ptoperty value from
        @return string - Current ['languages'][entry_name][compile_switch] data
        """
        return self.lang_json_data['languages'][language_name]['compileSwitch']

    @staticmethod
    def get_language_property_list()->list:
        """!
        @brief Return a tuple list of the usable language dictionary entries
        @return list of language entry property names
        """
        # create empty dictionary just for the keys
        entry_template = LanguageDescriptionList._create_language_entry("", [], [], [], "", "")
        return list(entry_template.keys())

    @staticmethod
    def get_language_property_return_data(property_name:str)->tuple:
        """!
        @brief Get the property description
        @param property_name (string) Name of the property from get_language_property_list()
        @return tuple - Data type (text|number) or None if the property_name is unknown
                        Description or None if the property_name is unknown
                        True if data is a list else False
        """
        prop_type = None
        prop_desc = None
        is_list = False
        if property_name == 'LANG':
            prop_type = "string"
            prop_desc = "Linux environment language code"
        elif property_name == 'LANG_regions':
            prop_type = "string"
            prop_desc = "Linux environment region codes for this language code"
            is_list = True
        elif property_name == 'LANGID':
            prop_type = "LANGID"
            prop_desc = "Windows LANGID & 0xFF language code(s)"
            is_list = True
        elif property_name == 'LANGID_regions':
            prop_type = "LANGID"
            prop_desc = "Windows full LANGID language code(s)"
            is_list = True
        elif property_name == 'isoCode':
            prop_type = "string"
            prop_desc = "ISO 639 set 1 language code"
        elif property_name == 'compileSwitch':
            prop_type = "string"
            prop_desc = "Compile switch definition for the language"

        return prop_type, prop_desc, is_list

    @staticmethod
    def is_language_property_text(property_name:str)->bool:
        """!
        @brief Return true if the data is stored as text or false if the data is stored as a number
        @param property_name (string) Name of the property from get_language_property_list()
        @return boolean - True if the data is stored as text or
                          False if the data is stored as a number
        """
        return bool(property_name in ['LANG', 'LANG_regions', 'isoCode', 'compileSwitch'])

    @staticmethod
    def get_language_property_method_name(property_name:str)->str:
        """!
        @brief Get the property method name
        @param property_name (string) Name of the property from get_language_property_list()
        @return string CPP description or None if the property_name is unknown
        """
        if property_name == 'LANG':
            retname = "getLANGLanguage"
        elif property_name == 'LANG_regions':
            retname = "getLANGRegionList"
        elif property_name == 'LANGID':
            retname = "getLANGIDCode"
        elif property_name == 'LANGID_regions':
            retname = "getLANGIDList"
        elif property_name == 'isoCode':
            retname = "getLangIsoCode"
        elif property_name == 'compileSwitch':
            retname = "getLanguageCompileSwitch"
        else:
            retname = None
        return retname

    @staticmethod
    def get_language_iso_property_method_name()->str:
        """!
        @brief Get the property method name
        @return string CPP description or None if the property_name is unknown
        """
        return LanguageDescriptionList.get_language_property_method_name('isoCode')

    def add_language(self, lang_name:str, linux_env_code:str, linux_region_list:list,
                    windows_lang_id:list, windows_region_list:list,
                    iso_639_code:str, compile_switch:str):
        """!
        @brief Add a language to the self.lang_json_data data

        @param lang_name (string) - Language name to use for file/class name generation
        @param linux_env_code (string) - linux LANG environment value for this language
        @param linux_region_list (list of strings) - Linux LANG region codes for this language
        @param windows_lang_id (list of numbers) - Windows LANGID & 0xFF value(s) for this language
        @param windows_region_list (list of numbers) - Windows LANGID value(s) for this language
        @param iso_639_code (string) - ISO 639 set 3 language code
        @param compile_switch (string) - Language compile switch
        """
        lang_entry = self._create_language_entry(linux_env_code, linux_region_list,
                                                 windows_lang_id, windows_region_list,
                                                 iso_639_code, compile_switch)
        self.lang_json_data['languages'][lang_name] = lang_entry

    def _input_language_name(self)->str:
        """!
        @brief Get the language from user input and check for validity
        @return string - language name
        """
        language_name = ""
        while language_name == "":
            prompt = "Enter language name value to be used for class<lang> generation: "
            name = input(prompt).lower()

            # Check validity
            if re.match('^[a-z]+$', name):
                # Valid name
                language_name = name
            else:
                # invalid name
                self._print_error("Only characters a-z are allowed in the <lang> name, try again.")
        return language_name

    def _input_iso_translate_code(self)->str:
        """!
        @brief Get the ISO 639-1 translate language code from user input and check for validity
        @return string - translate code
        """
        iso_translate_id = ""
        while iso_translate_id == "":
            prompt = "Enter ISO 639-1 translate language code (2 lower case characters): "
            trans_id = input(prompt).lower()

            # Check validity
            if re.match('^[a-z]{2}$', trans_id):
                # Valid name
                iso_translate_id = trans_id
            else:
                # invalid name
                self._print_error("Only two characters a-z are allowed in the code, try again.")
        return iso_translate_id

    def _input_linux_lang_code(self)->str:
        """!
        @brief Get the linux language code from user input and check for validity
        @return string - linux language code
        """
        linux_lang_id = ""
        while linux_lang_id == "":
            desc = "(2 chars of the 'LANG' environment value)"
            linux_env_code = input("Enter linux language code "+desc+": ").lower()

            # Check validity
            if re.match('^[a-z]{2}$', linux_env_code):
                # Valid name
                linux_lang_id = linux_env_code
            else:
                # invalid name
                self._print_error("Only two characters a-z are allowed in the code, try again.")
        return linux_lang_id

    def _input_linux_lang_regions(self)->list:
        """!
        @brief Get the linux language region code(s) from user input and check for validity
        @return list of strings - linux region codes
        """
        linux_region_list = []
        desc = "(2 chars following the _ in the 'LANG' environment value)"
        print ("Enter linux region code(s) "+desc+".")
        print ("Enter empty string to exit.")

        more_data = True
        while more_data:
            region = input("Region value: ").upper()

            # Check validity
            if region == "":
                # End of list
                more_data = False
            elif re.match('^[A-Z]{2}$', region):
                # Valid region
                linux_region_list.append(region)
            else:
                # invalid name
                self._print_error("Only two characters A-Z are allowed in the code, try again.")
        return linux_region_list

    def _input_windows_lang_ids(self)->tuple:
        """!
        @brief Get the windows language code(s) from user input
        @return tuple ([numbers], [numbers]) - windows LANGID codes.  First list is
                unique user LANGID codees & 0x0FF. Second list is all LANGID codes from user)
        """
        windows_id_code_list = []
        windows_id_match_codes = []
        print ("Enter Windows LANGID values. A value of 0 will exit.")

        more_data = True
        while more_data:
            region = int(input("LANGID value: "))
            if region == 0:
                more_data = False
            else:
                if region not in windows_id_code_list:
                    windows_id_code_list.append(region)

                    win_id = region & 0x0FF
                    if win_id not in windows_id_match_codes:
                        windows_id_match_codes.append(win_id)

        return windows_id_match_codes, windows_id_code_list

    def new_language(self, override:bool = False)->bool:
        """!
        @brief Add a new language to the self.lang_json_data data
        @param override {boolean} If true, override existing and force commit
        @return boolean - True if user selected to overwrite or commit
        """
        new_entry = {}
        entry_correct = False

        while not entry_correct:
            name = self._input_language_name()
            compile_switch = name.upper()+"_ERRORS"
            iso_code = self._input_iso_translate_code()
            linux_lang_code = self._input_linux_lang_code()
            linux_lang_regions = self._input_linux_lang_regions()
            win_case_ids, win_lang_ids = self._input_windows_lang_ids()

            new_entry = self._create_language_entry(linux_lang_code, linux_lang_regions,
                                                    win_case_ids, win_lang_ids, iso_code,
                                                    compile_switch)

            # Print entry for user to inspect
            print("New Entry:")
            print(new_entry)
            commit = input("Is this correct? [Y/N]").upper()
            if commit in ['Y', "YES"]:
                entry_correct = True


        # Determine if it's an overwrite or addition
        commit_flag = self._get_commit_flag(name, self.lang_json_data['languages'].keys(), override)
        if commit_flag:
            self.lang_json_data['languages'][name] = new_entry

        return commit_flag

    def __str__(self):
        """!
        @brief Convert JSON data to string
        """
        ret_str = ""
        json_lang_data = self.lang_json_data
        for lang_name, lang_data in json_lang_data['languages'].items():
            ret_str += lang_name
            ret_str += ": {\n"
            ret_str += str(lang_data)
            ret_str += "} end "
            ret_str += lang_name
            ret_str +="\n"

        ret_str+= "Default = "
        ret_str += str(json_lang_data['default']['name'])
        return ret_str
