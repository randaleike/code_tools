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
        ## Select unit test file list
        self.select_files = []

    def get_project_data(self)->ProjectDescription:
        """!
        @brief Get the project data
        @return {ProjectDescription} Project data object
        """
        return self.project_data

    def add_include_dir(self, subdir_name:str):
        """!
        @brief Add subdir name to the include dir list
        @param subdir_name {string} Subdirectory name
        """
        self.inc_subdirs.append(subdir_name)

    def get_include_dirs(self)->list:
        """!
        @brief Get the include subdirectory list
        @return list - List of include subdirectory strings that were added
                       using the add_include_dir method
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

    def _add_select_file(self, file_name:str, target_name:str):
        """!
        @brief Add file name and target name to the select unit test list
        @param file_name {str} Subdirectory/File name sof the select unittest
        @param target_name {str} Target name for the unittest
        """
        self.select_files.append((file_name, target_name))

    def get_select_unittest_set_names(self):
        """!
        @brief Get the OS select target file list
        @return tuple list - List of OS select unit test data
        """
        return self.select_files

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

    def get_lang_unittest_set_names(self)->list:
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
            unittest_sets.append((self.fnames[language_name]['source'],
                                  self.fnames[language_name]['unittest'],
                                  unittest_target))

        return unittest_sets

    def get_base_unittest_set_names(self)->tuple:
        """!
        @brief Generate a list of source file names
        @return tuple - unittest source file, unittest target name
        """
        # Generate the unittest target name and add data to the list
        return (self.fnames['base']['unittest'], self.class_gen.gen_unittest_target_name())

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

    def make_dirs(self, base_dir:str)->bool:
        """!
        @brief Make the subdirectories
        @param base_dir {str} Base directory name
        @return bool - True, all directories created, False id an error occurred
        """
        return_val = True

        if not os.path.exists(base_dir):
            return_val = False
            raise NameError(f"ERROR: base directory '{base_dir}' does not exist")

        incdir = os.path.join(base_dir, self.project_data.get_inc_subdir())
        srcdir = os.path.join(base_dir, self.project_data.get_src_subdir())
        testdir = os.path.join(base_dir, self.project_data.get_test_subdir())
        mockdir = os.path.join(base_dir, self.project_data.get_mock_subdir())

        subdir_list = [incdir, srcdir, testdir, mockdir]
        for subdir in subdir_list:
            return_val &= self._make_subdir(subdir)

        return return_val

    def open_file(self, base_dir:str, fname:str):
        """!
        @brief Open file
        @param base_dir {str} Base directory path
        @param fname {str} subdirectory/file name to open
        @return file - open file or None
        """
        retfile = None
        open_name = os.path.join(base_dir, fname)
        try: # pylint: disable=consider-using-with
            retfile = open(open_name, mode='wt', encoding="utf-8")
            return retfile
        except OSError:
            print (f"Failed to open '{open_name}' for writing")
            return None

    def generate_lang_files(self, base_dir:str, lang:str = None):
        """!
        @brief Generate the inc, source and unittest files
        @param base_dir {str} Base directory name
        @param lang {str or None} Language name or None for base files
        """
        incname = os.path.join(self.project_data.get_inc_subdir(),
                               self.class_gen.gen_h_fname(lang))
        baseinc = self.open_file(base_dir, incname)
        if baseinc is not None:
            self._add_file('include', incname, lang)
            self.class_gen.write_inc_file(baseinc, lang)

        srcname = os.path.join(self.project_data.get_src_subdir(),
                               self.class_gen.gen_cpp_fname(lang))
        basesrc = self.open_file(base_dir, srcname)
        if basesrc is not None:
            self._add_file('source', srcname, lang)
            if lang is None:
                self.class_gen.write_base_src_file(basesrc)
            else:
                self.class_gen.write_lang_src_file(basesrc, lang)

        tstname = os.path.join(self.project_data.get_test_subdir(),
                               self.class_gen.gen_unittest_fname(lang))
        utsrc = self.open_file(base_dir, tstname)
        if utsrc is not None:
            self._add_file('unittest', tstname, lang)
            if lang is None:
                self.class_gen.write_base_unittest_file(utsrc)
            else:
                self.class_gen.write_lang_unittest_file(utsrc, lang)

    def generate_mock_files(self, base_dir:str):
        """!
        @brief Generate the mock files
        @param base_dir {str} Base directory name
        """
        mockhname = os.path.join(self.project_data.get_mock_subdir(),
                                 self.class_gen.gen_mock_h_fname())
        mock_h = self.open_file(base_dir, mockhname)
        if mock_h is not None:
            self._add_file('mockInclude', mockhname)
            self.class_gen.write_mock_inc_file(mock_h)

        mocksrcname = os.path.join(self.project_data.get_mock_subdir(),
                                   self.class_gen.gen_mock_cpp_fname())
        mock_cpp = self.open_file(base_dir, mocksrcname)
        if mock_cpp is not None:
            self._add_file('mockSource', mocksrcname)
            self.class_gen.write_mock_src_file(mock_cpp)

    def generate_select_files(self, base_dir:str):
        """!
        @brief Generate the output files
        @param base_dir {str} Base directory name
        """
        for os_sel in self.class_gen.get_os_lang_sel_list():
            fname, target_name = os_sel.get_unittest_file_name()
            selname = os.path.join(self.project_data.get_test_subdir(), fname)
            select_ut = self.open_file(base_dir, selname)
            if select_ut is not None:
                self._add_select_file(selname, target_name)
                self.class_gen.write_selection_unittest_file(select_ut, os_sel)

    def generate_files(self, base_dir:str):
        """!
        @brief Generate the output files
        @param base_dir {str} Base directory name
        """
        incdir = os.path.join(base_dir, self.project_data.get_inc_subdir())
        self.add_include_dir(incdir)

        # Generate the base files
        self.generate_lang_files(base_dir)

        # Generate the language specific files
        lang_list = self.json_lang_data.get_language_list()
        for lang in lang_list:
            self.generate_lang_files(base_dir, lang)

        # Generate the mock files
        self.generate_mock_files(base_dir)

        # Generate the select unit tests
        self.generate_select_files(base_dir)
