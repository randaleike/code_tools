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

import argparse
import pathlib
import os

# Command line default function import
from argparse_json_data import create_argparse_language_file
from argparse_json_data import create_argparse_string_file
from argparse_json_data import create_argparse_project_file

# Json tools import
from code_tools_grocsoftware.base.project_json import ProjectDescription

# File generator tools import
from code_tools_grocsoftware.cpp_gen.project_file_gen import ProjectFileGenerator
from code_tools_grocsoftware.cpp_gen.cmake_gen import GenerateCmakeFile

##################################
##################################
# Generate the cmake files
##################################
##################################
def generate_cmake(file_gen:ProjectFileGenerator, base_dir:str)->bool:
    """!
    @brief Generate the subdir makefile
    @param file_gen {ProjectFileGenerator} Object used to generate the interface files
    @param base_dir {string} Base directory name
    @return boolean- True for pass else False for failure
    """
    cmake_generator = GenerateCmakeFile(file_gen)
    return_status = cmake_generator.generate_cmake(base_dir, True)
    return return_status

##################################
##################################
# Generate the source files
##################################
##################################
def generate_source(file_gen:ProjectFileGenerator, base_dir:str)->bool:
    """!
    @brief Generate the string files

    @param file_gen {ProjectFileGenerator} Object used to generate the interface files
    @param base_dir {string} Base directory name
    @return boolean- True for pass else False for failure
    """
    # Generate the directories
    ret_status = file_gen.make_dirs(base_dir)
    if ret_status:
        # Generate the files
        ret_status = file_gen.generate_files(base_dir)

    return ret_status

def command_main():
    """!
    Utility command interface
    @param subcommand {string} JSON string file command
    """
    parser = argparse.ArgumentParser(prog="autogenlang subcommand",
                                     description="Update argpaser library language " \
                                                 "h/cpp/unittest file generation")
    parser.add_argument('-j','--json', dest='json_proj_name', required=False,
                        type=pathlib.Path, default='../data/argparse_project.json',
                        help='Project json file name, default = ../data/argparse_project.json')

    subcommands= parser.add_subparsers(title='subcommand', dest='subcommand',
                                       help='Options: build, langjson, classjson, projjson')

    build_parser = subcommands.add_parser('build', help='Build Help')
    build_parser.add_argument('-o','--outpath', dest='gen_file_path',
                              required=True, type=pathlib.Path,
                              default='../output',
                              help='Existing destination directory for source and data files')

    lang_json_parser = subcommands.add_parser('langjson', help='Language JSON File Commands Help')
    lang_json_parser.add_argument('langcommand', choices=['createdefault', 'add'])

    class_json_parser = subcommands.add_parser('classjson', help='Strings Class JSON File Commands Help')
    class_json_parser.add_argument('stringscommand',
                                   choices=['createdefault',
                                            'addtranslate',
                                            'addproperty',
                                            'languageupdate'])

    proj_json_parser = subcommands.add_parser('projjson', help='Project JSON File Commands Help')
    proj_json_parser.add_argument('projcommand', choices=['createdefault'])

    args = parser.parse_args()

    # Open the data files
    data_file = os.path.abspath(args.json_proj_name)
    proj_json_data = ProjectDescription(data_file)

    # Process the subcommand
    if args.subcommand == 'build':
        # Open the project description file
        proj_gen = ProjectFileGenerator(proj_json_data)

        # Generate the source and cmake files
        print ("Building directory structure")
        output_base = os.path.abspath(args.gen_file_path)
        build_status = proj_gen.make_dirs(output_base)
        if build_status:
            print ("Building source and cmake files")
            build_status = proj_gen.generate_files(output_base)

        if build_status:
            cmake_generator = GenerateCmakeFile(proj_gen)
            build_status = cmake_generator.generate_cmake(output_base, True)

    elif args.subcommand == 'classjson':
        class_data = proj_json_data.get_string_data()
        lang_data = proj_json_data.get_lang_data()

        if args.stringscommand == 'createdefault':
            # Build the default methods definitions file
            print ("Updating Class Strings JSON file")
            create_argparse_string_file(lang_data, class_data, True)

        elif args.stringscommand == 'addtranslate':
            # Add a translation method to the strings file
            class_data = proj_json_data.get_string_data()
            commit = class_data.new_translate_method_entry(lang_data)
            if commit:
                print ("Updating Class Strings JSON file")
                class_data.update()
        elif args.stringscommand == 'addproperty':
            # Add a translation method to the strings file
            class_data = proj_json_data.get_string_data()
            commit = class_data.new_property_method_entry()
            if commit:
                print ("Updating Class Strings JSON file")
                class_data.update()
        elif args.stringscommand == 'languageupdate':
            # Build the default language list definitions file
            print ("Updating Class Strings JSON file")
            class_data.update_tranlations(lang_data)
            class_data.update()
        else:
            raise ValueError("Error: Unknown JSON string file command: "+args.stringscommand)

    elif args.subcommand == 'langjson':
        lang_data = proj_json_data.get_lang_data()
        if args.langcommand == 'createdefault':
            # Build the default language list definitions file
            print ("Updating Language JSON file")
            create_argparse_language_file(lang_data)
        elif args.langcommand == 'add':
            # Add a new language and update the class strings with the new language
            commit = lang_data.new_language()
            if commit:
                print ("Updating Language JSON file")
                lang_data.update()
                class_data = proj_json_data.get_string_data()

                class_data.update_tranlations(lang_data)
                class_data.update()
        else:
            raise ValueError("Error: Unknown JSON language file command: "+args.langcommand)
    elif args.subcommand == 'projjson':
        if args.projcommand == 'createdefault':
            # Build the default language list definitions file
            print ("Updating project JSON file")
            create_argparse_project_file(proj_json_data, data_file)
        else:
            raise ValueError("Error: Unknown JSON project file command: "+args.projcommand)
    else:
        raise ValueError("Error: Unknown subcommand: "+args.subcommand)


if __name__ == '__main__':
    command_main()
