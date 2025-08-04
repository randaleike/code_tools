"""@package test_programmer_tools
Unittest for programmer base tools utility
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


from code_tools_grocsoftware.base.copyright_generator import CopyrightGenerator

def test001_constructor():
    """!
    Test the CopyrightGenerator constructor
    """
    # Create an instance of the CopyrightGenerator
    testobj = CopyrightGenerator()

    # Check that the instance is created successfully
    assert testobj is not None, "CopyrightGenerator instance should be created successfully"

def test002_is_multi_year():
    """!
    Test the is_multi_year method
    """
    testobj = CopyrightGenerator()

    # Test with same year
    assert not testobj.is_multi_year(2025, 2025), "Should return False for same year"

    # Test with different years
    assert testobj.is_multi_year(2025, 2026), "Should return True for different years"
    assert testobj.is_multi_year(2025, None) is False, "Should return False if last_modify_year is None"

def test003_create_new_copyright():
    """!
    Test the create_new_copyright method
    """
    testobj = CopyrightGenerator()

    # Test with same year
    result = testobj.create_new_copyright("Test Owner", 2025, 2025)
    expected = "Copyright (c) 2025 Test Owner"
    assert result == expected, f"Expected '{expected}', got '{result}'"

    # Test with different years
    result = testobj.create_new_copyright("Test Owner", 2025, 2026)
    expected = "Copyright (c) 2025-2026 Test Owner"
    assert result == expected, f"Expected '{expected}', got '{result}'"

    # Test with None as last_modify_year
    result = testobj.create_new_copyright("Test Owner", 2025)
    expected = "Copyright (c) 2025 Test Owner"
    assert result == expected, f"Expected '{expected}', got '{result}'"

    # Test with only create_year
    result = testobj.create_new_copyright("Test Owner", 2025, None)
    expected = "Copyright (c) 2025 Test Owner"
    assert result == expected, f"Expected '{expected}', got '{result}'"
