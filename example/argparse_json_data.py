"""@package autogenlang
Utility to automatically generate language strings using google translate api
for the argparse libraries
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

from code_tools_grocsoftware.base.param_return_tools import ParamRetDict
from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList
from code_tools_grocsoftware.base.json_string_class_description import StringClassDescription
from code_tools_grocsoftware.base.project_json import ProjectDescription

# pylint: disable=line-too-long

######################################
######################################
# Create default langauge list JSON file
######################################
######################################
def add_english(languages:LanguageDescriptionList):
    """!
    @brief Add the english language definition
           Example for add_language call

    @param languages (LanguageDescriptionList) - Object to add to
    """
    linux_env = "en"
    linux_region_lst = ["AU","BZ","CA","CB","GB","IE","JM","NZ","PH","TT","US","ZA","ZW"]
    win_lang_id = [0x09]
    win_lang_id_lst = [3081,10249,4105,9225,2057,16393,6153,8201,5129,13321,7177,11273,1033,12297]
    languages.add_language("english", linux_env, linux_region_lst, win_lang_id, win_lang_id_lst, "en", "ENGLISH_ERRORS")

def add_spanish(languages:LanguageDescriptionList):
    """!
    @brief Add the spanish language definition
           Example for add_language call

    @param languages (LanguageDescriptionList) - Object to add to
    """
    linux_env = "es"
    linux_region_lst = ["AR","BO","CL","CO","CR","DO","EC","ES","GT","HN",
                       "MX","NI","PA","PE","PR","PY","SV","UY","VE"]
    win_lang_id = [0x0A]
    win_lang_id_lst = [11274,16394,13322,9226,5130,7178,12298,17418,4106,18442,2058,19466,6154,15370,10250,20490,1034,14346,8202]
    languages.add_language("spanish", linux_env, linux_region_lst, win_lang_id, win_lang_id_lst, "es", "SPANISH_ERRORS")

def add_french(languages:LanguageDescriptionList):
    """!
    @brief Add the french language definition
           Example for add_language call

    @param languages (LanguageDescriptionList) - Object to add to
    """
    linux_env = "fr"
    linux_region_lst = ["BE","CA","CH","FR","LU","MC"]
    win_lang_id = [0x0C]
    win_lang_id_lst = [2060,11276,3084,9228,12300,1036,5132,13324,6156,14348,10252,4108,7180]
    languages.add_language("french", linux_env, linux_region_lst, win_lang_id, win_lang_id_lst, "fr", "FRENCH_ERRORS")

def add_simplified_chinese(languages:LanguageDescriptionList):
    """!
    @brief Add the simplified chinese language definition
           Example for add_language call

    @param languages (LanguageDescriptionList) - Object to add to
    """
    linux_env = "zh"
    linux_region_lst = ["CN","HK","MO","SG","TW"]
    win_lang_id = [0x04]
    win_lang_id_lst = [2052,3076,5124,4100,1028]
    languages.add_language("SimplifiedChinese", linux_env, linux_region_lst, win_lang_id, win_lang_id_lst, "zh", "CHINESE_ERRORS")

def create_argparse_language_file(languages:LanguageDescriptionList):
    """!
    @brief Create base default LanguageDescriptionList json file
    @param languages (LanguageDescriptionList) - Object to create
    """
    add_english(languages)
    add_spanish(languages)
    add_french(languages)
    add_simplified_chinese(languages)
    languages.set_default("english")
    languages.update()

######################################
######################################
# Create default strings json file
######################################
######################################
def create_argparse_string_file(language_list:LanguageDescriptionList,
                                class_strings:StringClassDescription,
                                force_update:bool = False):
    """!
    @brief Add a function to the self.langJsonData data
    @param language_list {LanguageDescriptionList} List of languages to translate
    @param class_strings {StringClassDescription} Object to create/update
    @param force_update {boolean} True force the update without user intervention,
                                 False request update confermation on all methods
    """
    # Set up the class description
    class_strings.set_base_class_name("ParserStringListInterface")
    class_strings.set_namespace_name("argparser")
    class_strings.set_dynamic_compile_switch("DYNAMIC_INTERNATIONALIZATION")
    class_strings.set_base_selection_name("getLocalParserStringListInterface")

    # Add any extra mock setup required for the unit test
    extra_mock = ["#if defined(CONSTRUCTOR_GET_HELP_STRING)\n"]
    extra_mock.append("    //Parent object constructor will call getHelpString, so setup the expected call\n")
    extra_mock.append("    //before returning the pointer\n")
    extra_mock.append("    stringMockptr stringMock = reinterpret_cast<stringMockptr> (retPtr.get());   // NOLINT\n")
    extra_mock.append("    EXPECT_CALL(*stringMock, getHelpString()).WillOnce(Return(\"mock getHelpString\"));\n")
    extra_mock.append("#endif //defined(CONSTRUCTOR_GET_HELP_STRING)\n")
    class_strings.set_extra_mock(extra_mock)

    # Add the property method to get the iso code
    class_strings.add_property_method_entry("isoCode", override = force_update)

    # General argument parsing messages
    class_strings.add_translate_method_entry("getNotListTypeMessage", "Return non-list varg error message",
                                            [ParamRetDict.build_param_dict_with_mod("nargs", "integer", "input nargs value")],
                                            ParamRetDict.build_return_dict_with_mod("string", "Non-list varg error message"),
                                            "en",
                                            "Only list type arguments can have an argument count of @nargs@",
                                            override = force_update,
                                            language_list = language_list)
    class_strings.add_test_param_value('nargs', "3", False)

    class_strings.add_translate_method_entry("getUnknownArgumentMessage", "Return unknown parser key error message",
                                            [ParamRetDict.build_param_dict_with_mod("keyString", "string", "Unknown key")],
                                            ParamRetDict.build_return_dict_with_mod("string", "Unknown parser key error message"),
                                            "en",
                                            "Unknown argument: @keyString@",
                                            override = force_update,
                                            language_list = language_list)
    class_strings.add_test_param_value('keyString', "--myKey", True)

    class_strings.add_translate_method_entry("getInvalidAssignmentMessage", "Return varg invalid assignment error message",
                                            [ParamRetDict.build_param_dict_with_mod("keyString", "string", "Error key")],
                                            ParamRetDict.build_return_dict_with_mod("string", "Varg key invalid assignment error message"),
                                            "en",
                                            "\"@keyString@\" invalid assignment",
                                            override = force_update,
                                            language_list = language_list)

    class_strings.add_translate_method_entry("getAssignmentFailedMessage", "Return varg assignment failed error message",
                                            [ParamRetDict.build_param_dict_with_mod("keyString", "string", "Error key"),
                                            ParamRetDict.build_param_dict_with_mod("valueString", "string", "Assignment value")],
                                            ParamRetDict.build_return_dict_with_mod("string", "Varg key assignment failed error message"),
                                            "en",
                                            "\"@keyString@\", \"@valueString@\" assignment failed",
                                            override = force_update,
                                            language_list = language_list)
    class_strings.add_test_param_value('valueString', "23", True)

    class_strings.add_translate_method_entry("getMissingAssignmentMessage", "Return varg missing assignment error message",
                                            [ParamRetDict.build_param_dict_with_mod("keyString", "string", "Error key")],
                                            ParamRetDict.build_return_dict_with_mod("string", "Varg key missing value assignment error message"),
                                            "en",
                                            "\"@keyString@\" missing assignment value",
                                            override = force_update,
                                            language_list = language_list)

    class_strings.add_translate_method_entry("getMissingListAssignmentMessage", "Return varg missing list value assignment error message",
                                            [ParamRetDict.build_param_dict_with_mod("keyString", "string", "Error key"),
                                            ParamRetDict.build_param_dict_with_mod("nargsExpected", "size", "Expected assignment list length"),
                                            ParamRetDict.build_param_dict_with_mod("nargsFound", "size", "Input assignment list length")],
                                            ParamRetDict.build_return_dict_with_mod("string", "Varg key input value list too short error message"),
                                            "en",
                                            "\"@keyString@\" missing assignment value(s). Expected: @nargsExpected@ found: @nargsFound@ arguments",
                                            override = force_update,
                                            language_list = language_list)
    class_strings.add_test_param_value('nargsExpected', "2", False)
    class_strings.add_test_param_value('nargsFound', "1", False)

    class_strings.add_translate_method_entry("getTooManyAssignmentMessage", "Return varg missing list value assignment error message",
                                            [ParamRetDict.build_param_dict_with_mod("keyString", "string", "Error key"),
                                            ParamRetDict.build_param_dict_with_mod("nargsExpected", "size", "Expected assignment list length"),
                                            ParamRetDict.build_param_dict_with_mod("nargsFound", "size", "Input assignment list length")],
                                            ParamRetDict.build_return_dict_with_mod("string", "Varg key input value list too long error message"),
                                            "en",
                                            "\"@keyString@\" too many assignment values. Expected: @nargsExpected@ found: @nargsFound@ arguments",
                                            override = force_update,
                                            language_list = language_list)

    class_strings.add_translate_method_entry("getMissingArgumentMessage", "Return required varg missing error message",
                                            [ParamRetDict.build_param_dict_with_mod("keyString", "string", "Error key")],
                                            ParamRetDict.build_return_dict_with_mod("string", "Required varg key missing error message"),
                                            "en",
                                            "\"@keyString@\" required argument missing",
                                            override = force_update,
                                            language_list = language_list)

    class_strings.add_translate_method_entry("getArgumentCreationError", "Return parser add varg failure error message",
                                            [ParamRetDict.build_param_dict_with_mod("keyString", "string", "Error key")],
                                            ParamRetDict.build_return_dict_with_mod("string", "Parser varg add failure message"),
                                            "en",
                                            "Argument add failed: @keyString@",
                                            override = force_update,
                                            language_list = language_list)

    # Command Line parser messages
    class_strings.add_translate_method_entry("getUsageMessage", "Return usage help message",
                                            [],
                                            ParamRetDict.build_return_dict_with_mod("string", "Usage help message"),
                                            "en",
                                            "Usage:",
                                            override = force_update,
                                            language_list = language_list)

    class_strings.add_translate_method_entry("getPositionalArgumentsMessage", "Return positional argument help message",
                                            [],
                                            ParamRetDict.build_return_dict_with_mod("string", "Positional argument help message"),
                                            "en",
                                            "Positional Arguments:",
                                            override = force_update,
                                            language_list = language_list)

    class_strings.add_translate_method_entry("getSwitchArgumentsMessage", "Return optional argument help message",
                                            [],
                                            ParamRetDict.build_return_dict_with_mod("string", "Optional argument help message"),
                                            "en",
                                            "Optional Arguments:",
                                            override = force_update,
                                            language_list = language_list)

    class_strings.add_translate_method_entry("getHelpString", "Return default help switch help message",
                                            [],
                                            ParamRetDict.build_return_dict_with_mod("string", "Default help argument help message"),
                                            "en",
                                            "show this help message and exit",
                                            override = force_update,
                                            language_list = language_list)

    # Environment parser messages
    class_strings.add_translate_method_entry("getEnvArgumentsMessage", "Return environment parser argument help header",
                                            [],
                                            ParamRetDict.build_return_dict_with_mod("string", "Environment parser argument help header message"),
                                            "en",
                                            "Defined Environment values:",
                                            override = force_update,
                                            language_list = language_list)

    class_strings.add_translate_method_entry("getEnvironmentNoFlags", "Return environment parser add flag varg failure error message",
                                            [ParamRetDict.build_param_dict_with_mod("envKeyString", "string", "Flag key")],
                                            ParamRetDict.build_return_dict_with_mod("string", "Environment parser add flag varg failure message"),
                                            "en",
                                            "Environment value @envKeyString@ narg must be > 0",
                                            override = force_update,
                                            language_list = language_list)
    class_strings.add_test_param_value('envKeyString', "MY_ENV_KEY", True)

    class_strings.add_translate_method_entry("getRequiredEnvironmentArgMissing", "Return environment parser required varg missing error message",
                                            [ParamRetDict.build_param_dict_with_mod("envKeyString", "string", "Flag key")],
                                            ParamRetDict.build_return_dict_with_mod("string", "Environment parser required varg missing error message"),
                                            "en",
                                            "Environment value @envKeyString@ must be defined",
                                            override = force_update,
                                            language_list = language_list)


    # JSON file parser messages
    class_strings.add_translate_method_entry("getJsonArgumentsMessage", "Return json parser argument help header",
                                            [],
                                            ParamRetDict.build_return_dict_with_mod("string", "JSON parser argument help header message"),
                                            "en",
                                            "Available JSON argument values:",
                                            override = force_update,
                                            language_list = language_list)

    # XML file parser messages
    class_strings.add_translate_method_entry("getXmlArgumentsMessage", "Return xml parser argument help header",
                                            [],
                                            ParamRetDict.build_return_dict_with_mod("string", "XML parser argument help header message"),
                                            "en",
                                            "Available XML argument values:",
                                            override = force_update,
                                            language_list = language_list)

    class_strings.add_test_param_value('jsonKeyString', "jsonkey:", True)
    class_strings.add_test_param_value('xmlKeyString', "<xmlkey>", True)
    class_strings.add_test_param_value('vargRange', "<-100:100>", True)
    class_strings.add_test_param_value('vargType', "integer", True)
    class_strings.update()

######################################
######################################
# Create default project json file
######################################
######################################
def create_argparse_project_file(project:ProjectDescription, proj_file_name:str):
    """!
    @brief Create the argparser project file
    @param project {ProjectDescription} Project object to create/update
    @param proj_file_name {string} Project file name to create
    """
    data_dir = os.path.dirname(proj_file_name)
    langfile_name = os.path.join(data_dir, "argparse_language_list.json")
    stringfile_name = os.path.join(data_dir, "argparse_strings.json")

    project.set_lang_data_name(langfile_name)
    project.set_string_data_name(stringfile_name)

    project.set_project_name("ParserStringListInterface")
    project.set_creation_year(2025)
    project.set_version(0,5,0)
    project.set_url("https://github.com/randaleike/argparse")
    project.set_description("C++ international language support dor the argparse library")
    project.set_owner("Randal Eike")
    project.set_eula_name("MIT_open")

    project.set_inc_subdir("inc")
    project.set_src_subdir("src")
    project.set_test_subdir("test")
    project.set_mock_subdir("mock")

    project.set_group_name("LocalLanguageSelection")
    project.set_group_desc("Local language detection and selection utility")

    project.add_include_using("parserstr", "std::string", "Standard parser string definition")
    project.add_include_using("parserchar", "char", "Standard parser character definition")

    project.add_lang_src_using("parser_str_stream", "std::stringstream", "Standard string stream definition")
    project.update()
