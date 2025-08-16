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

import os

from code_tools_grocsoftware.base.project_json import ProjectDescription

from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList
from code_tools_grocsoftware.cpp_gen.class_file_gen import GenerateLangFiles

from code_tools_grocsoftware.cpp_gen.master_lang_select import MasterSelectFunctionGenerator
from code_tools_grocsoftware.cpp_gen.linux_lang_select import LinuxLangSelectFunctionGenerator
from code_tools_grocsoftware.cpp_gen.windows_lang_select import WindowsLangSelectFunctionGenerator
# Add additional OS lang select classes here

class ProjectFileGenerator():
    """!
    Class takes the LanguageDescriptionList JSON data and StringClassDescription JSON
    data and generates the base and language specific source, include, mock and unittest
    files.
    """
    def __init__(self, project_data:ProjectDescription):
        """!
        @brief GenerateBaseLangFile constructor

        @param project_data {ProjectDescription} JSON project data object
        """
        ## Json project data object
        self.project_data = project_data

        ## Class generator
        self.class_gen = GenerateLangFiles(project_data)

        ## Json language data list object
        self.json_lang_data:LanguageDescriptionList = project_data.get_lang_data()

        ## File name dictionary
        #  {language_name: {'include': include_fname,
        #                   'source': source_fname,
        #                   'mockInclude': mock_include_fname,
        #                   'mockSource': mock_source_fname,
        #                   'unittest': unittest_fname}}
        self.fnames = {}
        ## Include subdirectory list
        self.inc_subdirs = []

    def add_inculde_dir(self, subdir_name:str):
        """!
        @brief Add subdir name to the include dir list
        @param subdir_name {string} Subdirectory name
        """
        self.inc_subdirs.append(subdir_name)

    def get_include_dirs(self)->list:
        """!
        @brief Get the include subdirectory list
        @return list - List of include subdirectory strings that were added
                       using the add_inculde_dir method
        """
        return self.inc_subdirs

    def _add_file(self, file_type:str, file_name:str, language_name:str=None):
        """!
        @brief Add File to the list of files
        @param file_type {string} Type 'include' | 'source' | 'mockInclude'
                                       | 'mockSource | 'unittest'
        @param file_name {string} File name to add
        @param language_name {string} Language name or None for base files
        @note If language_name is None, then the file is a base file
        @note If language_name is not None, then the file is a language specific file
        """
        if language_name is None:
            language_name = 'base'

        if language_name in self.fnames:
            self.fnames[language_name][file_type] = file_name
        else:
            self.fnames[language_name] = {}
            self.fnames[language_name][file_type] = file_name

    def get_include_fnames(self)->list:
        """!
        @brief Generate a list of include file names
        @return list - list of generated include file names
        """
        file_list = []
        for _, lang_files in self.fnames.items():
            if 'include' in lang_files:
                file_list.append(lang_files['include'])
        return file_list

    def get_mock_include_fnames(self)->list:
        """!
        @brief Generate a list of include file names
        @return list - list of generated mockInclude file names
        """
        file_list = []
        for _, lang_files in self.fnames.items():
            if 'mockInclude' in lang_files:
                file_list.append(lang_files['mockInclude'])
        return file_list

    def get_source_fnames(self)->list:
        """!
        @brief Generate a list of source file names
        @return list - list of generated source file names
        """
        file_list = []
        for _, lang_files in self.fnames.items():
            if 'source' in lang_files:
                file_list.append(lang_files['source'])
        return file_list

    def get_unittest_set_names(self)->list:
        """!
        @brief Generate a list of source file names
        @return list - list of unittest source, unittest file names
        """
        unittest_sets = []
        language_list = self.json_lang_data.get_language_list()
        for language_name in language_list:
            if ((language_name not in self.fnames) or
                 ('source' not in self.fnames[language_name]) or
                 ('unittest' not in self.fnames[language_name])):
                continue

            # Generate the unittest target name and add data to the list
            unittest_target = self.class_gen.gen_unittest_target_name(language_name)
            unittest_sets.append((language_name,
                                  self.fnames[language_name]['source'],
                                  self.fnames[language_name]['unittest'],
                                  unittest_target))

        return unittest_sets


    def _make_subdir(self, subdir:str)->bool:
        """!
        @brief Make the subdirectory
        @return bool - True, directory created, False if an error occurred
        """
        return_val = True
        if not os.path.exists(subdir):
            try:
                os.mkdir(subdir)
            except PermissionError:
                return_val = False
                print(f"Permission denied: Unable to create '{subdir}'.")
            except OSError:
                return_val = False
                print(f"OS Error occurred creating: {subdir}.")
        return return_val

    def make_dirs(self)->bool:
        """!
        @brief Make the subdirectories
        @return bool - True, all directories created, False id an error occurred
        """
        return_val = True
        base_dir = self.project_data.get_base_dir_name()

        if not os.path.exists(base_dir):
            return_val = False
            raise NameError(f"ERROR: base directory '{base_dir}' does not exist")
        else:
            incdir = os.path.join(base_dir, self.project_data.get_inc_subdir())
            srcdir = os.path.join(base_dir, self.project_data.get_src_subdir())
            testdir = os.path.join(base_dir, self.project_data.get_test_subdir())
            mockdir = os.path.join(base_dir, self.project_data.get_mock_subdir())

            subdir_list = [incdir, srcdir, testdir, mockdir]
            for subdir in subdir_list:
                return_val &= self._make_subdir(subdir)

        return return_val

    def generate_files(self):
        """!
        @brief Generate the output files
        """
        base_dir = self.project_data.get_base_dir_name()
        incdir = os.path.join(base_dir, self.project_data.get_inc_subdir())
        self.add_inculde_dir(incdir)

        srcdir = os.path.join(base_dir, self.project_data.get_src_subdir())
        testdir = os.path.join(base_dir, self.project_data.get_test_subdir())
        mockdir = os.path.join(base_dir, self.project_data.get_mock_subdir())

        incname = os.path.join(incdir, self.class_gen.gen_h_fname())
        srcname = os.path.join(srcdir, self.class_gen.gen_cpp_fname())
        tstname = os.path.join(testdir, self.class_gen.gen_unittest_fname())
        mockhname = os.path.join(mockdir, self.class_gen.gen_mock_h_fname())
        mocksrcname = os.path.join(mockdir, self.class_gen.gen_mock_cpp_fname())

        with open(incname, mode='wt', encoding="utf-8") as baseinc:
            self._add_file('include', incname)
            self.class_gen.write_inc_file(baseinc)

        with open(srcname, mode='wt', encoding="utf-8") as basesrc:
            self.class_gen.write_base_src_file(basesrc)

        with open(tstname, mode='wt', encoding="utf-8") as utsrc:
            self.class_gen.write_base_unittest_file(utsrc)

        with open(mockhname, mode='wt', encoding="utf-8") as mock_h:
            self.class_gen.write_mock_inc_file(mock_h)

        with open(mocksrcname, mode='wt', encoding="utf-8") as mock_cpp:
            self.class_gen.write_mock_src_file(mock_cpp)

        for os_sel in self.class_gen.get_os_lang_sel_list():
            fname = os.path.join(testdir, os_sel.get_unittest_file_name())
            with open(fname, mode='wt', encoding="utf-8") as utos_cpp:
                self.class_gen.write_selection_unittest_file(utos_cpp, os_sel)

        lang_list = self.json_lang_data.get_language_list()
        for lang in lang_list:
            incname = os.path.join(incdir, self.class_gen.gen_h_fname(lang))
            srcname = os.path.join(testdir, self.class_gen.gen_cpp_fname(lang))
            tstname = os.path.join(mockdir, self.class_gen.gen_unittest_fname(lang))
            with open(incname, mode='wt', encoding="utf-8") as langinc:
                self.class_gen.write_inc_file(langinc, lang)

            with open(srcname, mode='wt', encoding="utf-8") as langsrc:
                self.class_gen.write_lang_src_file(langsrc, lang)

            with open(tstname, mode='wt', encoding="utf-8") as utsrc:
                self.class_gen.write_lang_unittest_file(utsrc, lang)
