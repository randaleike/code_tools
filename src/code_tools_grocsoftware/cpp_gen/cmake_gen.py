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
from code_tools_grocsoftware.cpp_gen.project_file_gen import ProjectFileGenerator

class GenerateCmakeFile():
    """!
    Class takes the GenerateLangFiles data and generates the CMakeLists.txt
    file.
    """
    def __init__(self, project_files:ProjectFileGenerator):
        """!
        @brief GenerateCmakeFile constructor

        @param project_files {ProjectFileGenerator} Generated files
        @param url {str} URL for the project
        @param description {str} Description of the project
        """
        ## Project file data
        self.file_gen = project_files
        self.proj_data:ProjectDescription = project_files.get_project_data()

    def _open_file(self, base_dir:str):
        """!
        @brief Open file
        @param base_dir {str} Base directory path
        @return file - open file or None
        """
        retfile = None
        open_name = os.path.join(base_dir, 'CMakeLists.txt')
        try: # pylint: disable=consider-using-with
            retfile = open(open_name, mode='wt', encoding="utf-8")
            return retfile
        except OSError:
            print (f"Failed to open cmake file '{base_dir}/CMakeLists.txt' for writing")
            return None

    def _gen_comment_block(self, comment:str)->list:
        """!
        @brief Generate comment block text
        @param comment {str} Block domment text
        """
        cmake_txt = []
        cmake_txt.append("####\n")
        cmake_txt.append("# "+comment+"\n")
        cmake_txt.append("####\n")
        return cmake_txt

    def gen_header(self, project_name:str, project_ver:str,
                   description:str=None, url:str=None)->list:
        """!
        @brief Generate the include directories cmake code
        @param project_name {str} Project name
        @param project_ver {str} Project version
        @param description {str} Project description
        @param url {str} Project url
        @return {list} cmake include directory list name
        """
        cmake_txt = []
        cmake_txt.append("cmake_minimum_required(VERSION 3.14)\n")
        project_line = f"project({project_name} VERSION {project_ver} LANGUAGES C CXX"
        if description is not None:
            project_line += f' DESCRIPTION "{description}"'
        if url is not None:
            project_line += f' HOMEPAGE_URL "{url}"'
        project_line += ")\n\n"

        cmake_txt.append(project_line)
        cmake_txt.append("set(CMAKE_CXX_STANDARD 17)\n")
        cmake_txt.append("set(CMAKE_CXX_STANDARD_REQUIRED True)\n")

        return cmake_txt

    def gen_include_dirs_list(self, project_name:str)->tuple:
        """!
        @brief Generate the include directories cmake code
        @param project_name {str} Project name
        @return {tuple} cmake include directory code list,
                        cmake include directory list name
        """
        cmake_txt = []
        inclst_name = None
        incdir_list = self.file_gen.get_include_dirs()

        if incdir_list:
            inclst_name = project_name+"Include"
            cmake_txt.extend(self._gen_comment_block(project_name+" include directories"))
            cmake_txt.append("set ("+inclst_name+"\n")
            for inc in incdir_list:
                line = "     ${CMAKE_CURRENT_LIST_DIR}/"+inc+"\n"
                cmake_txt.append(line)
            cmake_txt.append("    )\n")

        return cmake_txt, inclst_name

    def gen_source_file_list(self, project_name:str)->tuple:
        """!
        @brief Generate the include directories cmake code
        @param project_name {str} Project name
        @return {tuple} cmake include directory code list,
                        cmake include directory list name
        """
        cmake_txt = []
        srclst_name = None
        srclist = self.file_gen.get_source_fnames()

        if srclist:
            srclst_name = project_name+"Sources"
            cmake_txt.extend(self._gen_comment_block(project_name+" source files"))
            cmake_txt.append("set ("+srclst_name+"\n")
            for srcfile in srclist:
                line = "     ${CMAKE_CURRENT_LIST_DIR}/"+srcfile+"\n"
                cmake_txt.append(line)
            cmake_txt.append("    )\n")

        return cmake_txt, srclst_name

    def gen_lib_target(self, project_name:str,
                     srclst_name:str = None,
                     inclst_name:str = None)->list:
        """!
        @brief Generate the cmake build file
        @param project_name {str} Project name
        @param srclst_name {str} Source file list
        @param inclst_name {str} Include directory list
        @return {list} cmake library make code
        """
        cmake_txt = []
        if srclst_name is not None:
            # Add the library
            cmake_txt.extend(self._gen_comment_block(project_name+" library"))
            cmake_txt.append("add_library(${PROJECT_NAME} OBJECT ${"+srclst_name+"})\n")
            if inclst_name is not None:
                cmake_txt.append("target_include_directories(${PROJECT_NAME} PRIVATE ${"+inclst_name+"})\n")
            cmake_txt.append("set_target_properties(${PROJECT_NAME} " \
                            "PROPERTIES VERSION ${PROJECT_VERSION})\n")
        return cmake_txt

    def gen_enable_unittest(self, enable_googletest:bool = False)->list:
        """!
        @brief Generate unittest enable code
        @param enable_googletest {bool}: True to enable googletest, False otherwise.
                                         Defaults to False.
        @return {list} cmake unittest enable make code
        """
        cmake_txt = []

        # Enable testing
        cmake_txt.extend(self._gen_comment_block("Enable testing"))
        cmake_txt.append("enable_testing()\n")
        if enable_googletest:
            cmake_txt.append("include(GoogleTest)\n")
        return cmake_txt


    def gen_unittest_target(self, target_name:str,
                            srclst:list = None,
                            inclst_name:str = None,
                            enable_googletest:bool = False)->list:
        """!
        @brief Generate the cmake build file
        @param target_name {str} Project name
        @param srclst_name {str} Source file list
        @param inclst_name {str} Include directory list
        @param enable_googletest {bool} True to enable googletest, False otherwise
        @return {list} cmake unittest make code
        """
        if enable_googletest:
            if inclst_name is not None:
                test_inc = "${"+inclst_name+"} ${GTEST_INCLUDE_DIR}"
            else:
                test_inc = "${GTEST_INCLUDE_DIR}"

            test_lib = "${GTEST_LIBRARIES}"
            extra_link = "-DGTEST_LINKED_AS_SHARED_LIBRARY=1"
        else:
            if inclst_name is not None:
                test_inc = "${"+inclst_name+"}"
            else:
                test_inc = None
            test_lib = None
            extra_link = None

        cmake_txt = []
        if srclst is not None:
            # Add the library
            cmake_txt.extend(self._gen_comment_block(target_name+" unit test build"))
            exe_line = "add_executable("+target_name
            for srcfile in srclst:
                exe_line += " "+srcfile
            exe_line += ")\n"
            cmake_txt.append(exe_line)
            if test_inc is not None:
                cmake_txt.append("target_include_directories("+target_name+" PUBLIC "+test_inc+")\n")
            if test_lib is not None:
                # If we have a test library, link it
                cmake_txt.append("target_link_libraries("+target_name+" PRIVATE "+test_lib+")\n")
            if extra_link is not None:
                # If we have extra link options, add them
                cmake_txt.append("target_compile_options("+target_name+" PUBLIC "+extra_link+")\n")

            cmake_txt.append("if((${CMAKE_SYSTEM_NAME} MATCHES \"Linux\") AND " \
                                "(CMAKE_BUILD_TYPE MATCHES \"^[Dd]ebug\"))\n")
            cmake_txt.append("    target_compile_options("+target_name+" PRIVATE --coverage)\n")
            cmake_txt.append("    target_link_options("+target_name+" PRIVATE --coverage)\n")
            cmake_txt.append("endif()\n\n")

            cmake_txt.append("gtest_add_tests (TARGET "+target_name+" TEST_LIST "+target_name+"AllTests)\n\n")

            cmake_txt.append("if(\"${CMAKE_SYSTEM_NAME}\" == \"Windows\")\n")
            cmake_txt.append("    set_tests_properties("+target_name+"AllTests " \
                                "PROPERTIES ENVIRONMENT \"PATH=$<SHELL_PATH:$<TARGET_FILE_DIR" \
                                ":gtest>>$<SEMICOLON>$ENV{PATH}\")\n")
            cmake_txt.append("endif()\n")

        return cmake_txt

    def generate_cmake(self, base_dir:str, enable_googletest:bool = False)->bool:
        """!
        @brief Generate the cmake build file
        @param base_dir {str} Base directory name to create the file in
        @param enable_googletest {bool} True to enable googletest, False otherwise
        @return {bool} True if successful, False if not
        """
        cmake_file = self._open_file(base_dir)
        if not cmake_file:
            return False

        project_name = self.proj_data.get_project_name()
        project_ver = self.proj_data.get_version_num()
        description = self.proj_data.get_description()
        url = self.proj_data.get_url()

        # Generate the header
        cmake_txt = self.gen_header(project_name, project_ver, description, url)
        cmake_file.writelines(cmake_txt)
        cmake_file.write("\n")  # whitespace for readability

        # Include the base include
        cmake_txt, inclst_name = self.gen_include_dirs_list(project_name)
        cmake_file.writelines(cmake_txt)
        cmake_file.write("\n")  # whitespace for readability

        # Include the base source files
        cmake_txt, srclst_name = self.gen_source_file_list(project_name)
        cmake_file.writelines(cmake_txt)
        cmake_file.write("\n")  # whitespace for readability

        # Add the library
        cmake_txt = self.gen_lib_target(project_name,
                                        srclst_name=srclst_name,
                                        inclst_name=inclst_name)
        cmake_file.writelines(cmake_txt)
        cmake_file.write("\n")  # whitespace for readability

        # Enable testing
        cmake_txt = self.gen_enable_unittest(enable_googletest)
        cmake_file.writelines(cmake_txt)
        cmake_file.write("\n")  # whitespace for readability

        # Add the language unit tests
        unttest_list = self.file_gen.get_lang_unittest_set_names()
        for srcfile, tstfile, target in unttest_list:
            cmake_txt = self.gen_unittest_target(target,
                                                 srclst=[srcfile, tstfile],
                                                 inclst_name=inclst_name,
                                                 enable_googletest=enable_googletest)

            cmake_file.writelines(cmake_txt)
            cmake_file.write("\n")  # whitespace for readability

        # Add the OS selection unit tests
        unttest_list = self.file_gen.get_select_unittest_set_names()
        for tstfile, target in unttest_list:
            cmake_txt = self.gen_unittest_target(target,
                                                 srclst=["${"+srclst_name+"}", tstfile],
                                                 inclst_name=inclst_name,
                                                 enable_googletest=enable_googletest)

            cmake_file.writelines(cmake_txt)
            cmake_file.write("\n")  # whitespace for readability

        # Add the base file unit tests
        tstfile, target = self.file_gen.get_base_unittest_set_names()
        cmake_txt = self.gen_unittest_target(target,
                                            srclst=["${"+srclst_name+"}", tstfile],
                                            inclst_name=inclst_name,
                                            enable_googletest=enable_googletest)

        cmake_file.writelines(cmake_txt)
        cmake_file.write("\n")  # whitespace for readability

        return True
