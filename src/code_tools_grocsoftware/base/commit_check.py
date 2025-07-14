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

def get_commit_over_write_flag(entry_name:str, override:bool = False)->bool:
    """!
    @brief Determine if the user is ready to commit the new entry over the existing one
    @param entry_name {string} Name of the method that will be added
    @param override {boolean} True = force commit, False = ask user
    @return boolean - commit flag
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

def get_commit_new_flag(entry_name:str)->bool:
    """!
    @brief Determine if the user is ready to commit the new entry
    @param entry_name {string} Name of the method that will be added
    @return boolean - commit flag
    """
    commit = input("Add new "+entry_name+" entry? [Y/N]").upper()
    return bool(commit in ['Y', "YES"])

def get_commit_flag(entry_name:str, entry_keys:list, override:bool = False)->bool:
    """!
    @brief Determine if the user is ready to commit the new entry
    @param entry_name {string} Name of the method that will be added
    @param entry_keys {list of keys} List of the existing entry keys
    @param override {boolean} True = force commit, False = ask user
    @return boolean - commit flag
    """
    if entry_name in entry_keys:
        flag = get_commit_over_write_flag(entry_name, override)
    else:
        flag = get_commit_new_flag(entry_name)
    return flag

def new_entry_correct(new_entry)->bool:
    """!
    @brief Display the new entry and ask user if it is correct
    @param new_entry {object} New entry object to inspect
    @return boolean - correctness flag
    """
    # Print entry for user to inspect
    print("New Entry:")
    print(new_entry)
    commit = input("Is this correct? [Y/N]").upper()
    return bool(commit in ['Y', "YES"])
