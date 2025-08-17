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

import json
from datetime import date

from code_tools_grocsoftware.base.eula import EulaText
from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList
from code_tools_grocsoftware.base.json_string_class_description import StringClassDescription

class ProjectDescription():
    """!
    Language description list data
    """
    def __init__(self, project_data_file_name:str = None):
        """!
        @brief LanguageDescriptionList constructor

        @param project_data_file_name (string) - Name of the json file containing
                                           the project description data
        """
        ## Path/file name of the JSON language decription file
        self.filename = "jsonProjectDescription.json"

        ## JSON language description data from the file
        self.project_json_data = {}

        if project_data_file_name is not None:
            self.filename = project_data_file_name
            try:
                lang_json_file = open(self.filename, 'r', encoding='utf-8') # pylint: disable=consider-using-with
            except FileNotFoundError:
                self.clear()
            else:
                self.project_json_data = json.load(lang_json_file)
                lang_json_file.close()
        else:
            self.clear()


    def clear(self):
        """!
        @brief Reset all data to the default state
        """
        self.project_json_data = {'eula_name':"MIT_open", 'custom_text': [],
                                  'langDataFile':None, 'stringDataFile':None,
                                  'inc_subdir': "", 'src_subdir': "",
                                  'test_subdir': None, 'mock_subdir': None,
                                  'owner': "Unknown",
                                  'groupName': None, 'groupDesc': None,
                                  'inc_using':None,
                                  'base_src_using':None,
                                  'lang_src_using':None,
                                  'creationYear': int(date.today().year),
                                  'version':{'major':0,
                                             'minor':1,
                                             'patch':0}}

    def update(self):
        """!
        @brief Update the JSON file with the current contents of self.project_json_data
        """
        with open(self.filename, 'w', encoding='utf-8') as lang_json_file:
            json.dump(self.project_json_data, lang_json_file, indent=2)

    def get_eula(self)->EulaText:
        """!
        @brief Get the EULA object from the JSON data

        @return (string) - EULA name
        """
        if self.project_json_data['eula_name'] != 'custom':
            eula = EulaText(eula_type = self.project_json_data['eula_name'])
        else:
            eula = EulaText(custom_eula = self.project_json_data['custom_text'])
        return eula

    def set_eula_name(self, eula_name:str = "MIT_open"):
        """!
        @brief Set the EULA name in the JSON data

        @param eula_name (string) - EULA name to set
        """
        self.project_json_data['eula_name'] = eula_name

    def set_custom_eula_text(self, eula_text:list):
        """!
        @brief Set the EULA name in the JSON data

        @param eula_text (list) - Custom EULA text script
        """
        self.project_json_data['eula_name'] = 'custom'
        if not isinstance(eula_text, list):
            raise TypeError("EULA text must be a list of strings")
        self.project_json_data['custom_text'] = eula_text

    def get_lang_data(self)->LanguageDescriptionList:
        """!
        @brief Get the language data file name from the JSON data
        @return (LanguageDescriptionList) - Language data
        """
        return LanguageDescriptionList(self.project_json_data['langDataFile'])

    def set_lang_data_name(self, lang_data_name:str = None):
        """!
        @brief Set the language data file name in the JSON data

        @param lang_data_name (string) - Language data file name to set
        """
        self.project_json_data['langDataFile'] = lang_data_name

    def get_string_data(self)->StringClassDescription:
        """!
        @brief Get the string data file name from the JSON data
        @return (StringClassDescription) - String data
        """
        return StringClassDescription(self.project_json_data['stringDataFile'])

    def set_string_data_name(self, string_data_name:str = None):
        """!
        @brief Set the string data file name in the JSON data

        @param string_data_name (string) - String data file name to set
        """
        self.project_json_data['stringDataFile'] = string_data_name

    def get_custom_text(self)->list:
        """!
        @brief Get the custom text from the JSON data
        @return (list) - Custom text list
        """
        return self.project_json_data['custom_text']

    def get_owner(self)->str:
        """!
        @brief Get the owner name from the JSON data
        @return (string) - Owner name
        """
        return self.project_json_data['owner']

    def set_owner(self, owner:str):
        """!
        @brief Set the owner name in the JSON data

        @param owner (string) - Owner name to set
        """
        self.project_json_data['owner'] = owner

    def get_inc_subdir(self)->str:
        """!
        @brief Get the include subdirectory name from the JSON data
        @return (string) - Include subdirectory name
        """
        return self.project_json_data['inc_subdir']

    def set_inc_subdir(self, inc_subdir:str = "inc"):
        """!
        @brief Set the include subdirectory name in the JSON data

        @param inc_subdir (string) - Include subdirectory name to set
        """
        self.project_json_data['inc_subdir'] = inc_subdir

    def get_src_subdir(self)->str:
        """!
        @brief Get the source subdirectory name from the JSON data
        @return (string) - Source subdirectory name
        """
        return self.project_json_data['src_subdir']

    def set_src_subdir(self, src_subdir:str = "src"):
        """!
        @brief Set the source subdirectory name in the JSON data

        @param src_subdir (string) - Source subdirectory name to set
        """
        self.project_json_data['src_subdir'] = src_subdir

    def get_test_subdir(self)->str:
        """!
        @brief Get the test subdirectory name from the JSON data
        @return (string) - Test subdirectory name
        """
        return self.project_json_data['test_subdir']

    def set_test_subdir(self, test_subdir:str = "test"):
        """!
        @brief Set the test subdirectory name in the JSON data

        @param test_subdir (string) - Test subdirectory name to set
        """
        self.project_json_data['test_subdir'] = test_subdir

    def get_mock_subdir(self)->str:
        """!
        @brief Get the mock subdirectory name from the JSON data
        @return (string) - Mock subdirectory name
        """
        return self.project_json_data['mock_subdir']

    def set_mock_subdir(self, mock_subdir:str = "mock"):
        """!
        @brief Set the mock subdirectory name in the JSON data

        @param mock_subdir (string) - Mock subdirectory name to set
        """
        self.project_json_data['mock_subdir'] = mock_subdir

    def get_group_name(self):
        """!
        @brief Set the group name
        """
        return self.project_json_data['groupName']

    def set_group_name(self, name:str = None):
        """!
        @brief Set the mock subdirectory name in the JSON data

        @param name (string) - Group name name to set
        """
        self.project_json_data['groupName'] = name

    def get_group_desc(self):
        """!
        @brief Set the group description
        """
        return self.project_json_data['groupDesc']

    def set_group_desc(self, desc:str = None):
        """!
        @brief Set the mock subdirectory name in the JSON data

        @param desc (string) - Group description name to set
        """
        self.project_json_data['groupDesc'] = desc

    def _add_using(self, section:str, local_name:str, std_name:str, desc:str = None):
        """!
        @brief Add value to using list
        @param section {string} Using section name
        @param local_name {string} Local type name
        @param std_name {string} Standard C/C++ type name
        @param desc {string} Doxygen comment
        """
        new_entry = {'localName':local_name, 'stdName':std_name, 'desc':desc}
        if self.project_json_data[section] is None:
            self.project_json_data[section] = [new_entry]
        else:
            self.project_json_data[section].append(new_entry)

    def _get_using(self, section:str)->list:
        """!
        @brief Return the section using dictionary list
        @param section {string} Using section name
        @return list - list of using dictionary entries
        """
        return self.project_json_data[section]

    def add_include_using(self, local_name:str, std_name:str, desc:str = None):
        """!
        @brief Add value to include file using list
        @param local_name {string} Local type name
        @param std_name {string} Standard C/C++ type name
        @param desc {string} Doxygen comment
        @return string - Constructed using statement
        """
        self._add_using('inc_using', local_name, std_name, desc)

    def get_include_using(self)->list:
        """!
        @brief Return the include using dictionary list
        @return list - list of using dictionary entries
        """
        return self._get_using('inc_using')

    def add_base_src_using(self, local_name:str, std_name:str, desc:str = None):
        """!
        @brief Add value to base source file using list
        @param local_name {string} Local type name
        @param std_name {string} Standard C/C++ type name
        @param desc {string} Doxygen comment
        @return string - Constructed using statement
        """
        self._add_using('base_src_using', local_name, std_name, desc)

    def get_base_src_using(self)->list:
        """!
        @brief Return the base source using dictionary list
        @return list - list of using dictionary entries
        """
        return self._get_using('base_src_using')

    def add_lang_src_using(self, local_name:str, std_name:str, desc:str = None):
        """!
        @brief Add value to language specific source file using list
        @param local_name {string} Local type name
        @param std_name {string} Standard C/C++ type name
        @param desc {string} Doxygen comment
        @return string - Constructed using statement
        """
        self._add_using('lang_src_using', local_name, std_name, desc)

    def get_lang_src_using(self)->list:
        """!
        @brief Return the language specific source using dictionary list
        @return list - list of using dictionary entries
        """
        return self._get_using('lang_src_using')

    def set_version(self, major:int=0, minor:int=0, patch=0):
        """!
        @brief Set the version levels
        @param major {integer} Major version number, default = 0
        @param minor {integer} Major version number, default = 0
        @param patch {integer} Major version number, default = 0
        """
        self.project_json_data['version']={'major':major,
                                           'minor':minor,
                                           'patch':patch}

    def get_version_num(self)->str:
        """!
        @brief Get the version string
        @return string - Version numeric string
        """
        verstr = str(self.project_json_data['version']['major'])
        verstr += "."
        verstr += str(self.project_json_data['version']['minor'])
        verstr += "."
        verstr += str(self.project_json_data['version']['patch'])
        return verstr

    def get_version(self)->str:
        """!
        @brief Get the version string
        @return string - Version string
        """
        verstr = "v"+self.get_version_num()
        return verstr

    def set_creation_year(self, year:int):
        """!
        @brief Set the creation year
        @param year {integer} Project creation year
        """
        self.project_json_data['creationYear'] = year

    def get_creation_year(self):
        """!
        @brief Get the creation year
        """
        return self.project_json_data['creationYear']
