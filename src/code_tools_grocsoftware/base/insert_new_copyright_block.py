"""@package langstringautogen
@brief Scan source files and update copyright years
Scan the source files and update the copyright year in the header section of any modified files
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

def insert_new_copyright_block(input_file, output_filename:str, comment_block_data:dict,
                               comment_marker:dict, new_copyright_msg:str,
                               new_eula:list = None)->bool: # pylint: disable=too-many-arguments
    """!
    @brief Write a new file with the updated copyright message

    @param input_file (file): Existing text file
    @param output_filename (filename string): Name of the file to output updated text to
    @param comment_block_data (dictionary): Comment block locations to update
    @param comment_marker (dictionary): comment_block_delim object to use for comment block
                                        replacement
    @param new_copyright_msg (string): New copyright message to write to the new file
    @param new_eula (list of strings): New license text to add to the copyright comment block

    @return Bool - True if new file was written, False if an error occured.
    """
    try: # pylint: disable=consider-using-with
        output_file = open(output_filename, mode='wt', encoding="utf-8")

        # Copy the first chunk of the file
        input_file.seek(0)
        if comment_block_data['blkStart'] != 0:
            header = input_file.read(comment_block_data['blkStart'])
            output_file.write(header)

        # Output start of the comment block
        new_line = comment_marker['blockStart']+"\n"
        output_file.write(new_line)

        # Insert the new copyright and licence text
        new_line = comment_marker['blockLineStart']+" "+new_copyright_msg+"\n"
        output_file.write(new_line)

        # Determine if we should update EULA
        if new_eula is not None:
            new_line = comment_marker['blockLineStart']+"\n"
            output_file.write(new_line)

            # Insert new EULA
            for licence_line in new_eula:
                new_line = comment_marker['blockLineStart']+" "+licence_line+"\n"
                output_file.write(new_line)
        else:
            # Copy old EULA
            copyright_location = comment_block_data['copyrightMsgs'][0]
            copyright_end = copyright_location['lineOffset'] + len(copyright_location['text'])
            input_file.seek(copyright_end)
            current_line_offset = copyright_end
            while current_line_offset < comment_block_data['blkEndSOL']:
                new_line = comment_marker['blockLineStart']+" "+input_file.readline()
                output_file.write(new_line)
                current_line_offset = input_file.tell()

        # Output the comment block end
        new_line = comment_marker['blockEnd']+"\n"
        output_file.write(new_line)

        # Copy the remainder of the file
        input_file.seek(comment_block_data['blkEndEOL'])
        while new_line:
            new_line = input_file.readline()
            output_file.write(new_line)

        output_file.close()
        return True

    except OSError:
        print("ERROR: Unable to open file \""+output_filename+"\" for writing as text file.")
        return False
