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

import os
import unittest
from unittest.mock import patch, MagicMock

import io
import contextlib

from dir_init import TESTFILEPATH
from dir_init import pathincsetup
pathincsetup()

from code_tools.base.json_string_class_description import TranslationTextParser
from code_tools.base.json_string_class_description import StringClassDescription
from code_tools.base.param_return_tools import ParamRetDict

class Unittest02StringClassDescription(unittest.TestCase):
    """!
    @brief Unit test for the StringClassDescription class
    """
    @classmethod
    def setUpClass(cls):
        cls.testJson = os.path.join(TESTFILEPATH, "teststrdesc.json")
        cls.testlanglist = os.path.join(TESTFILEPATH, "teststringlanglist.json")
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        if os.path.exists("jsonStringClassDescription.json"):
            os.remove("jsonStringClassDescription.json")   # Delete in case it was accidently created
        return super().tearDownClass()

    @staticmethod
    def mockParamRetInput(prompt, inputStr):
        if prompt == "Is full type a list [y/n]:":
            return "n"
        elif prompt == "Is full type a pointer [y/n]:":
            return "n"
        elif prompt == "Is full type a reference [y/n]:":
            return "n"
        elif prompt == "Can value be undefined [y/n]:":
            return "n"
        elif prompt == "Is full type an array [y/n]:":
            return "n"
        elif prompt == 'Enter custom type: ':
            return "foobar"
        else:
            return next(inputStr)

    def test01InputIsoTranslateCodeGoodInput(self):
        """!
        @brief Test _inputIsoTranslateCode(), good input
        """
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', return_value='fr'):
            testobj = StringClassDescription()
            self.assertEqual(testobj._inputIsoTranslateCode(), 'fr')
            self.assertEqual(output.getvalue(), "")

    def test02InputIsoTranslateCodeInvalidInput(self):
        """!
        @brief Test _inputIsoTranslateCode(), invalid input
        """
        inputStr = (text for text in ["", "de1", "d", "german", "de"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription()
            self.assertEqual(testobj._inputIsoTranslateCode(), 'de')
            expectedStr = "Error: Only two characters a-z are allowed in the code, try again.\n"
            expectedStr += "Error: Only two characters a-z are allowed in the code, try again.\n"
            expectedStr += "Error: Only two characters a-z are allowed in the code, try again.\n"
            expectedStr += "Error: Only two characters a-z are allowed in the code, try again.\n"
            self.assertEqual(output.getvalue(), expectedStr)

    def test03InputVarMethodNameGoodInput(self):
        """!
        @brief Test _inputVarMethodName(), methodName=true, good input
        """
        inputStr = (text for text in ["validMethodName", "validMethodName2", "valid_method_name", "valid_method3_name"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription()
            self.assertEqual(testobj._inputVarMethodName(True), 'validMethodName')
            self.assertEqual(testobj._inputVarMethodName(True), 'validMethodName2')
            self.assertEqual(testobj._inputVarMethodName(True), 'valid_method_name')
            self.assertEqual(testobj._inputVarMethodName(True), 'valid_method3_name')
            self.assertEqual(output.getvalue(), "")

    def test04InputVarMethodNameInvalidInput(self):
        """!
        @brief Test _inputVarMethodName(), methodName=true, invalid input
        """
        inputStr = (text for text in ["", "2invalidMethodName", "invalid-method-name", "invalid;Name", "validMethodName"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription()
            self.assertEqual(testobj._inputVarMethodName(True), 'validMethodName')
            expectedStr = "Error:  is not a valid code name, try again.\n"
            expectedStr += "Error: 2invalidMethodName is not a valid code name, try again.\n"
            expectedStr += "Error: invalid-method-name is not a valid code name, try again.\n"
            expectedStr += "Error: invalid;Name is not a valid code name, try again.\n"
            self.assertEqual(output.getvalue(), expectedStr)

    def test05InputVarMethodNameGoodInputMethodFalse(self):
        """!
        @brief Test _inputVarMethodName(), methodName=false, good input
        """
        inputStr = (text for text in ["validParamName", "validParamName2", "valid_param_name", "valid_param3_name"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription()
            self.assertEqual(testobj._inputVarMethodName(False), 'validParamName')
            self.assertEqual(testobj._inputVarMethodName(False), 'validParamName2')
            self.assertEqual(testobj._inputVarMethodName(False), 'valid_param_name')
            self.assertEqual(testobj._inputVarMethodName(False), 'valid_param3_name')
            self.assertEqual(output.getvalue(), "")

    def test06InputVarMethodNameInvalidInputMethodFalse(self):
        """!
        @brief Test _inputVarMethodName(), methodName=false, invalid input
        """
        inputStr = (text for text in ["", "2invalidParamName", "invalid-param-name", "invalid#ParamName",  "validParamName"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription()
            self.assertEqual(testobj._inputVarMethodName(False), 'validParamName')
            expectedStr = "Error:  is not a valid code name, try again.\n"
            expectedStr += "Error: 2invalidParamName is not a valid code name, try again.\n"
            expectedStr += "Error: invalid-param-name is not a valid code name, try again.\n"
            expectedStr += "Error: invalid#ParamName is not a valid code name, try again.\n"
            self.assertEqual(output.getvalue(), expectedStr)

    def test07InputArrayModifierValidInput(self):
        """!
        @brief Test _inputVarMethodName(), Valid input
        """
        testobj = StringClassDescription()

        expectedMod = ParamRetDict.setTypeModArraySize(0, 10)
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', return_value='10'):
            self.assertEqual(testobj._inputArrayModifier(0), expectedMod)
            self.assertEqual(output.getvalue(), "")

        expectedMod2 = ParamRetDict.setTypeModArraySize(0, 23)
        with contextlib.redirect_stdout(output), patch('builtins.input', return_value='23'):
            self.assertEqual(testobj._inputArrayModifier(0), expectedMod2)
            self.assertEqual(output.getvalue(), "")

        expectedMod3 = ParamRetDict.setTypeModArraySize(0, 1)
        with contextlib.redirect_stdout(output), patch('builtins.input', return_value='1'):
            self.assertEqual(testobj._inputArrayModifier(0), expectedMod3)
            self.assertEqual(output.getvalue(), "")

        expectedMod4 = ParamRetDict.setTypeModArraySize(0, 65535)
        with contextlib.redirect_stdout(output), patch('builtins.input', return_value='65535'):
            self.assertEqual(testobj._inputArrayModifier(0), expectedMod4)
            self.assertEqual(output.getvalue(), "")

    def test08InputArrayModifierInvalidInput(self):
        """!
        @brief Test _inputVarMethodName(), Invalid input
        """
        inputList = ["0", "65636", "100000", "-1", "ten", "one", "10"]
        inputStr = (text for text in inputList)
        def testMockIn(prompt):
            return next(inputStr)

        testobj = StringClassDescription()

        expectedMod = ParamRetDict.setTypeModArraySize(0, 10)
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            self.assertEqual(testobj._inputArrayModifier(0), expectedMod)
            expectedErrorStr = "Error: must be a valid number between 1 and 65535\n"
            expectedErrorStr += "Error: must be a valid number between 1 and 65535\n"
            expectedErrorStr += "Error: must be a valid number between 1 and 65535\n"
            expectedErrorStr += "Error: must be a valid number between 1 and 65535\n"
            expectedErrorStr += "Error: must be an integer value\n"
            expectedErrorStr += "Error: must be an integer value\n"
            self.assertEqual(output.getvalue(), expectedErrorStr)

    def test09InputTypeModifierListAllNo(self):
        """!
        @brief Test _inputTypeModifier(), Simple case, all no
        """
        def testMockIn(prompt):
            return 'n'

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription()
            self.assertEqual(testobj._inputTypeModifier(), 0)

    def test10InputTypeModifierListOneYes(self):
        """!
        @brief Test _inputTypeModifier(), Simple case, one yes
        """
        inputDict = {'listAns': "n",
                     'ptrAns': "n",
                     'refAns': "n",
                     'undefAns': "n",
                     'arrayAns': "n"}
        def testMockIn(prompt):
            if prompt == "Is full type a list [y/n]:":
                return inputDict['listAns']
            elif prompt == "Is full type a pointer [y/n]:":
                return inputDict['ptrAns']
            elif prompt == "Is full type a reference [y/n]:":
                return inputDict['refAns']
            elif prompt == "Can value be undefined [y/n]:":
                return inputDict['undefAns']
            elif prompt == "Is full type an array [y/n]:":
                return inputDict['arrayAns']
            elif prompt == "Size of the array in entries: ":
                return "5"
            else:
                return 'n'

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription()
            for answer in list(inputDict):
                inputDict[answer] = 'y'
                if answer == 'listAns':
                    expectedMod = ParamRetDict.typeModList
                elif answer == 'ptrAns':
                    expectedMod = ParamRetDict.typeModPtr
                elif answer == 'refAns':
                    expectedMod = ParamRetDict.typeModRef
                elif answer == 'undefAns':
                    expectedMod = ParamRetDict.typeModUndef
                elif answer == 'arrayAns':
                    expectedMod = 5 << ParamRetDict.typeModArrayShift
                else:
                    expectedMod = 0

                self.assertEqual(testobj._inputTypeModifier(), expectedMod)
                inputDict[answer] = 'n'

    def test11InputTypeModifierListTwoYes(self):
        """!
        @brief Test _inputTypeModifier(), two yes
        """
        inputDict = {'listAns': "n",
                     'ptrAns': "n",
                     'refAns': "n",
                     'undefAns': "n",
                     'arrayAns': "n"}
        def testMockIn(prompt):
            if prompt == "Is full type a list [y/n]:":
                return inputDict['listAns']
            elif prompt == "Is full type a pointer [y/n]:":
                return inputDict['ptrAns']
            elif prompt == "Is full type a reference [y/n]:":
                return inputDict['refAns']
            elif prompt == "Can value be undefined [y/n]:":
                return inputDict['undefAns']
            elif prompt == "Is full type an array [y/n]:":
                return inputDict['arrayAns']
            elif prompt == "Size of the array in entries: ":
                return "6"
            else:
                return 'n'

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription()
            for firstYes in list(inputDict):
                inputDict[firstYes] = 'y'
                firstMod = 0
                arrayEntry = False
                if firstYes == 'listAns':
                    firstMod = ParamRetDict.typeModList
                elif firstYes == 'ptrAns':
                    firstMod = ParamRetDict.typeModPtr
                elif firstYes == 'refAns':
                    firstMod = ParamRetDict.typeModRef
                elif firstYes == 'undefAns':
                    firstMod = ParamRetDict.typeModUndef
                elif firstYes == 'arrayAns':
                    firstMod = 6 << ParamRetDict.typeModArrayShift
                    arrayEntry = True
                else:
                    firstMod = 0

                for secondYes in list(inputDict):
                    expectedMod = 0
                    if secondYes != firstYes:
                        inputDict[secondYes] = 'y'
                        if secondYes == 'listAns':
                            if arrayEntry:
                                expectedMod = firstMod
                            else:
                                expectedMod = ParamRetDict.typeModList | firstMod
                        elif secondYes == 'ptrAns':
                            expectedMod = ParamRetDict.typeModPtr | firstMod
                        elif secondYes == 'refAns':
                            expectedMod = ParamRetDict.typeModRef | firstMod
                        elif secondYes == 'undefAns':
                            expectedMod = ParamRetDict.typeModUndef | firstMod
                        elif secondYes == 'arrayAns':
                            if firstMod == ParamRetDict.typeModList:
                                expectedMod = (6 << ParamRetDict.typeModArrayShift)
                            else:
                                expectedMod = (6 << ParamRetDict.typeModArrayShift) | firstMod
                        else:
                            expectedMod = 0

                        self.assertEqual(testobj._inputTypeModifier(), expectedMod)
                        inputDict[secondYes] = 'n'

                inputDict[firstYes] = 'n'

    def test12InputTypeModifierListAllYesExceptArray(self):
        """!
        @brief Test _inputTypeModifier(), all yes, except array
        """
        def testMockIn(prompt):
            if prompt == "Is full type an array [y/n]:":
                return 'n'
            elif prompt == "Size of the array in entries: ":
                return "7"
            else:
                return 'y'

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription()
            expectedMod = ParamRetDict.typeModList | ParamRetDict.typeModPtr | ParamRetDict.typeModRef | ParamRetDict.typeModUndef
            self.assertEqual(testobj._inputTypeModifier(), expectedMod)

    def test13InputTypeModifierListAllYes(self):
        """!
        @brief Test _inputTypeModifier(), all yes
        """
        def testMockIn(prompt):
            if prompt == "Size of the array in entries: ":
                return "7"
            else:
                return 'y'

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription()
            expectedMod = ParamRetDict.typeModPtr | ParamRetDict.typeModRef | ParamRetDict.typeModUndef
            expectedMod |= 7 << ParamRetDict.typeModArrayShift
            self.assertEqual(testobj._inputTypeModifier(), expectedMod)

    def test14InputParamReturnTypeGoodInputText(self):
        """!
        @brief Test _inputParamReturnType(), good input, text
        """
        typeList = ["t", "T", "text", "TEXT", "Text"]
        inputList = []
        for element in typeList:
            inputList.append(element)
            inputList.append(element)

        inputStr = (text for text in inputList)
        def testMockIn(prompt):
            return Unittest02StringClassDescription.mockParamRetInput(prompt, inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription()
            for i in range(0,len(typeList)):
                typeName, typeMod = testobj._inputParamReturnType(True)
                self.assertEqual(typeName, 'string')
                self.assertEqual(typeMod, 0)

                typeName, typeMod = testobj._inputParamReturnType(False)
                self.assertEqual(typeName, 'string')
                self.assertEqual(typeMod, 0)

            self.assertEqual(output.getvalue(), "")

    def test15InputParamReturnTypeGoodInputInteger(self):
        """!
        @brief Test _inputParamReturnType(), good input, integer
        """
        typeList = ["i", "I", "integer", "INTEGER", "Integer", "int", "Int", "INT"]
        inputList = []
        for element in typeList:
            inputList.append(element)
            inputList.append(element)

        inputStr = (text for text in inputList)
        def testMockIn(prompt):
            return Unittest02StringClassDescription.mockParamRetInput(prompt, inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription()
            for i in range(0,len(typeList)):
                typeName, typeMod = testobj._inputParamReturnType(True)
                self.assertEqual(typeName, 'integer')
                self.assertEqual(typeMod, 0)

                typeName, typeMod = testobj._inputParamReturnType(False)
                self.assertEqual(typeName, 'integer')
                self.assertEqual(typeMod, 0)

            self.assertEqual(output.getvalue(), "")

    def test16InputParamReturnTypeGoodInputUnsigned(self):
        """!
        @brief Test _inputParamReturnType(), good input, integer
        """
        typeList = ["u", "U", "unsigned", "UNSIGNED", "Unsigned"]
        inputList = []
        for element in typeList:
            inputList.append(element)
            inputList.append(element)

        inputStr = (text for text in inputList)
        def testMockIn(prompt):
            return Unittest02StringClassDescription.mockParamRetInput(prompt, inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription()
            for i in range(0,len(typeList)):
                typeName, typeMod = testobj._inputParamReturnType(True)
                self.assertEqual(typeName, 'unsigned')
                self.assertEqual(typeMod, 0)

                typeName, typeMod = testobj._inputParamReturnType(False)
                self.assertEqual(typeName, 'unsigned')
                self.assertEqual(typeMod, 0)

            self.assertEqual(output.getvalue(), "")

    def test17InputParamReturnTypeGoodInputSize(self):
        """!
        @brief Test _inputParamReturnType(), good input, integer
        """
        typeList = ["s", "S", "size", "Size", "SIZE"]
        inputList = []
        for element in typeList:
            inputList.append(element)
            inputList.append(element)

        inputStr = (text for text in inputList)
        def testMockIn(prompt):
            return Unittest02StringClassDescription.mockParamRetInput(prompt, inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription()
            for i in range(0,len(typeList)):
                typeName, typeMod = testobj._inputParamReturnType(True)
                self.assertEqual(typeName, 'size')
                self.assertEqual(typeMod, 0)

                typeName, typeMod = testobj._inputParamReturnType(False)
                self.assertEqual(typeName, 'size')
                self.assertEqual(typeMod, 0)

            self.assertEqual(output.getvalue(), "")

    def test18InputParamReturnTypeGoodInputCustomGoodName(self):
        """!
        @brief Test _inputParamReturnType(), good input, custom, good custom name
        """
        typeList = ["c", "C", "custom", "CUSTOM", "Custom"]
        inputList = []
        for element in typeList:
            inputList.append(element)
            inputList.append(element)

        inputStr = (text for text in inputList)
        def testMockIn(prompt):
            return Unittest02StringClassDescription.mockParamRetInput(prompt, inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription()
            for i in range(0,len(typeList)):
                typeName, typeMod = testobj._inputParamReturnType(True)
                self.assertEqual(typeName, 'foobar')
                self.assertEqual(typeMod, 0)

                typeName, typeMod = testobj._inputParamReturnType(False)
                self.assertEqual(typeName, 'foobar')
                self.assertEqual(typeMod, 0)

            self.assertEqual(output.getvalue(), "")

    def test19InputReturnTypeInputCustomGoodCustomNames(self):
        """!
        @brief Test _inputParamReturnType(), return, custom, good names
        """
        customTypeList = ["test", "test1", "test_underscore", "namespace::test", "test2__underscore"]
        customTypeNames = (text for text in customTypeList)
        def testMockIn(prompt):
            if prompt == 'Enter custom type: ':
                return next(customTypeNames)
            elif prompt == 'Enter return base type [T(ext)|i(nteger)|u(nsigned)|s(ize)|c(ustom)]: ':
                return "c"
            elif prompt == 'Enter parameter base type [T(ext)|i(nteger)|u(nsigned)|s(ize)|c(ustom)]: ':
                return "c"
            else:
                return "n"

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription()

            for name in customTypeList:
                typeName, typeMod = testobj._inputParamReturnType(True)
                self.assertEqual(typeName, name)
                self.assertEqual(typeMod, 0)

            self.assertEqual(output.getvalue(), "")

    def test20InputParamTypeInputCustomGoodCustomNames(self):
        """!
        @brief Test _inputParamReturnType(), return, custom, good names
        """
        customTypeList = ["test", "test1", "test_underscore", "namespace::test", "test2__underscore"]
        customTypeNames = (text for text in customTypeList)
        def testMockIn(prompt):
            if prompt == 'Enter custom type: ':
                return next(customTypeNames)
            elif prompt == 'Enter return base type [T(ext)|i(nteger)|u(nsigned)|s(ize)|c(ustom)]: ':
                return "c"
            elif prompt == 'Enter parameter base type [T(ext)|i(nteger)|u(nsigned)|s(ize)|c(ustom)]: ':
                return "c"
            else:
                return "n"

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription()

            for name in customTypeList:
                typeName, typeMod = testobj._inputParamReturnType(False)
                self.assertEqual(typeName, name)
                self.assertEqual(typeMod, 0)

            self.assertEqual(output.getvalue(), "")

    def test21InputReturnTypeInputCustomBadCustomNames(self):
        """!
        @brief Test _inputParamReturnType(), custom, bad names, return type
        """
        customTypeList = ["1test", "test-dash", "test@", "namespace??test", "goodName"]
        customTypeNames = (text for text in customTypeList)
        def testMockIn(prompt):
            if prompt == 'Enter custom type: ':
                return next(customTypeNames)
            elif prompt == 'Enter return base type [T(ext)|i(nteger)|u(nsigned)|s(ize)|c(ustom)]: ':
                return "c"
            elif prompt == 'Enter parameter base type [T(ext)|i(nteger)|u(nsigned)|s(ize)|c(ustom)]: ':
                return "c"
            else:
                return "n"

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription()

            typeName, typeMod = testobj._inputParamReturnType(True)
            self.assertEqual(typeName, 'goodName')
            self.assertEqual(typeMod, 0)

            expectedStr = ""
            for name in customTypeList:
                if name != 'goodName':
                    expectedStr += name+" is not a valid code type name, try again.\n"
            self.assertEqual(output.getvalue(), expectedStr)

    def test22InputParamTypeInputCustomBadCustomNames(self):
        """!
        @brief Test _inputParamReturnType(), custom, bad names, param type
        """
        customTypeList = ["1test", "test-dash", "test@", "namespace??test", "goodName"]
        customTypeNames = (text for text in customTypeList)
        def testMockIn(prompt):
            if prompt == 'Enter custom type: ':
                return next(customTypeNames)
            elif prompt == 'Enter return base type [T(ext)|i(nteger)|u(nsigned)|s(ize)|c(ustom)]: ':
                return "c"
            elif prompt == 'Enter parameter base type [T(ext)|i(nteger)|u(nsigned)|s(ize)|c(ustom)]: ':
                return "c"
            else:
                return "n"

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription()

            typeName, typeMod = testobj._inputParamReturnType(False)
            self.assertEqual(typeName, 'goodName')
            self.assertEqual(typeMod, 0)

            expectedStr = ""
            for name in customTypeList:
                if name != 'goodName':
                    expectedStr += name+" is not a valid code type name, try again.\n"
            self.assertEqual(output.getvalue(), expectedStr)

    def test23InputParamReturnTypeInputInvalidType(self):
        """!
        @brief Test _inputParamReturnType(), invalid type selection
        """
        inputStr = (text for text in ["x", "a", "dict", "i", "x", "z", "list", "i"])
        def testMockIn(prompt):
            return Unittest02StringClassDescription.mockParamRetInput(prompt, inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription()
            typeName, typeMod = testobj._inputParamReturnType(True)
            self.assertEqual(typeName, 'integer')
            self.assertEqual(typeMod, 0)

            typeName, typeMod = testobj._inputParamReturnType(False)
            self.assertEqual(typeName, 'integer')
            self.assertEqual(typeMod, 0)

            expectedStr = "Error: \"x\" unknown. Please select one of the options from the menu.\n"
            expectedStr += "Error: \"a\" unknown. Please select one of the options from the menu.\n"
            expectedStr += "Error: \"dict\" unknown. Please select one of the options from the menu.\n"
            expectedStr += "Error: \"x\" unknown. Please select one of the options from the menu.\n"
            expectedStr += "Error: \"z\" unknown. Please select one of the options from the menu.\n"
            expectedStr += "Error: \"list\" unknown. Please select one of the options from the menu.\n"
            self.assertEqual(output.getvalue(), expectedStr)

    def test24InputParameterData(self):
        """!
        @brief Test _inputParameterData(), simple as all the sub functions have already been tested
        """
        def testMockIn(prompt):
            if ((prompt == "Is full type a list [y/n]:") or
                (prompt == "Is full type a pointer [y/n]:") or
                (prompt == "Is full type a reference [y/n]:") or
                (prompt == "Can value be undefined [y/n]:") or
                (prompt == "Is full type an array [y/n]:")):
                return 'n'
            elif prompt == "Enter parameter name: ":
                return "paramName"
            elif prompt == "Enter parameter base type [T(ext)|i(nteger)|u(nsigned)|s(ize)|c(ustom)]: ":
                return "i"
            elif prompt == "Enter brief parameter description for doxygen comment: ":
                return "Brief parameter description"
            else:
                return "n"

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription()
            paramDict = testobj._inputParameterData()
            self.assertIsInstance(paramDict, dict)
            self.assertEqual(len(paramDict), 4)
            self.assertEqual(ParamRetDict.getParamType(paramDict), "integer")
            self.assertEqual(ParamRetDict.getParamName(paramDict), "paramName")
            self.assertEqual(ParamRetDict.getParamDesc(paramDict), "Brief parameter description")
            self.assertEqual(ParamRetDict.getParamTypeMod(paramDict), 0)

    def test25InputReturnData(self):
        """!
        @brief Test _inputReturnData(), simple as all the sub functions have already been tested
        """
        def testMockIn(prompt):
            if ((prompt == "Is full type a list [y/n]:") or
                (prompt == "Is full type a pointer [y/n]:") or
                (prompt == "Is full type a reference [y/n]:") or
                (prompt == "Can value be undefined [y/n]:") or
                (prompt == "Is full type an array [y/n]:")):
                return 'n'
            elif prompt == "Enter return base type [T(ext)|i(nteger)|u(nsigned)|s(ize)|c(ustom)]: ":
                return "t"
            elif prompt == "Enter brief description of the return value for doxygen comment: ":
                return "Brief return data description"
            else:
                return "n"

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription()
            returnDict = testobj._inputReturnData()
            self.assertIsInstance(returnDict, dict)
            self.assertEqual(len(returnDict), 3)
            self.assertEqual(ParamRetDict.getReturnType(returnDict), "string")
            self.assertEqual(ParamRetDict.getReturnDesc(returnDict), "Brief return data description")
            self.assertEqual(ParamRetDict.getReturnTypeMod(returnDict), 0)

    def test26ValidateTranslateStringPass(self):
        """!
        @brief Test _validateTranslateString method
        """
        testobj = StringClassDescription(self.testJson)
        paramList = [ParamRetDict.buildParamDictWithMod("foo", "string", "Test param one")]
        valid, matchCount, paramCount, parsedStrData = testobj._validateTranslateString(paramList, 'Test string with input @foo@')
        self.assertTrue(valid)
        self.assertEqual(matchCount, 1)
        self.assertEqual(paramCount, 1)
        self.assertIsInstance(parsedStrData, list)
        self.assertEqual(len(parsedStrData), 2)
        self.assertEqual(parsedStrData[0][0], TranslationTextParser.parsedTypeText)
        self.assertEqual(parsedStrData[0][1], "Test string with input ")
        self.assertEqual(parsedStrData[1][0], TranslationTextParser.parsedTypeParam)
        self.assertEqual(parsedStrData[1][1], "foo")

    def test27ValidateTranslateStringPassTwo(self):
        """!
        @brief Test _validateTranslateString method
        """
        testobj = StringClassDescription(self.testJson)
        paramList = [ParamRetDict.buildParamDictWithMod("foo", "string", "Test param one"),
                     ParamRetDict.buildParamDictWithMod("moo", "string", "Test param two")]
        valid, matchCount, paramCount, parsedStrData = testobj._validateTranslateString(paramList, 'Test string with input @foo@ and @moo@')
        self.assertTrue(valid)
        self.assertEqual(matchCount, 2)
        self.assertEqual(paramCount, 2)
        self.assertIsInstance(parsedStrData, list)
        self.assertEqual(len(parsedStrData), 4)
        self.assertEqual(parsedStrData[0][0], TranslationTextParser.parsedTypeText)
        self.assertEqual(parsedStrData[0][1], "Test string with input ")
        self.assertEqual(parsedStrData[1][0], TranslationTextParser.parsedTypeParam)
        self.assertEqual(parsedStrData[1][1], "foo")
        self.assertEqual(parsedStrData[2][0], TranslationTextParser.parsedTypeText)
        self.assertEqual(parsedStrData[2][1], " and ")
        self.assertEqual(parsedStrData[3][0], TranslationTextParser.parsedTypeParam)
        self.assertEqual(parsedStrData[3][1], "moo")

    def test28ValidateTranslateStringFail(self):
        """!
        @brief Test _validateTranslateString method
        """
        testobj = StringClassDescription(self.testJson)
        paramList = [ParamRetDict.buildParamDictWithMod("foo", "string", "Test param one"),
                     ParamRetDict.buildParamDictWithMod("moo", "string", "Test param two")]
        valid, matchCount, paramCount, parsedStrData = testobj._validateTranslateString(paramList, 'Test string with input @foo@')
        self.assertFalse(valid)
        self.assertEqual(matchCount, 1)
        self.assertEqual(paramCount, 1)
        self.assertIsInstance(parsedStrData, list)
        self.assertEqual(len(parsedStrData), 2)
        self.assertEqual(parsedStrData[0][0], TranslationTextParser.parsedTypeText)
        self.assertEqual(parsedStrData[0][1], "Test string with input ")
        self.assertEqual(parsedStrData[1][0], TranslationTextParser.parsedTypeParam)
        self.assertEqual(parsedStrData[1][1], "foo")

    def test29ValidateTranslateStringFailTooMany(self):
        """!
        @brief Test _validateTranslateString method
        """
        testobj = StringClassDescription(self.testJson)
        paramList = [ParamRetDict.buildParamDictWithMod("foo", "string", "Test param one")]
        valid, matchCount, paramCount, parsedStrData = testobj._validateTranslateString(paramList, 'Test string with input @foo@ and @moo@')
        self.assertFalse(valid)
        self.assertEqual(matchCount, 1)
        self.assertEqual(paramCount, 2)
        self.assertIsInstance(parsedStrData, list)
        self.assertEqual(len(parsedStrData), 4)
        self.assertEqual(parsedStrData[0][0], TranslationTextParser.parsedTypeText)
        self.assertEqual(parsedStrData[0][1], "Test string with input ")
        self.assertEqual(parsedStrData[1][0], TranslationTextParser.parsedTypeParam)
        self.assertEqual(parsedStrData[1][1], "foo")
        self.assertEqual(parsedStrData[2][0], TranslationTextParser.parsedTypeText)
        self.assertEqual(parsedStrData[2][1], " and ")
        self.assertEqual(parsedStrData[3][0], TranslationTextParser.parsedTypeParam)
        self.assertEqual(parsedStrData[3][1], "moo")

    def test30InputTranslateStringGood(self):
        """!
        @brief Test _inputTranslateString method, proper message
        """
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', return_value='Test string with input @foo@'):
            testobj = StringClassDescription(self.testJson)
            paramList = [ParamRetDict.buildParamDictWithMod("foo", "string", "Test param one")]
            parsedStrData = testobj._inputTranslateString(paramList)
            self.assertIsInstance(parsedStrData, list)
            self.assertEqual(len(parsedStrData), 2)
            self.assertEqual(parsedStrData[0][0], TranslationTextParser.parsedTypeText)
            self.assertEqual(parsedStrData[0][1], "Test string with input ")
            self.assertEqual(parsedStrData[1][0], TranslationTextParser.parsedTypeParam)
            self.assertEqual(parsedStrData[1][1], "foo")

            expectedStr = "Enter translation template string. Use @paramName@ in the string to indicate where the \n"
            expectedStr += "function parameters should be inserted.\n"
            expectedStr += "Example with single input parameter name \"keyString\": Found argument key @keyString@\n"
            self.assertEqual(output.getvalue(), expectedStr)

    def test31InputTranslateStringWithTooManyError(self):
        """!
        @brief Test _inputTranslateString method, improper message, too many params
        """
        inputStr = (text for text in ["Test string with input @foo@ and @moo@", "Test string with input @foo@"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription(self.testJson)
            paramList = [ParamRetDict.buildParamDictWithMod("foo", "string", "Test param one")]
            parsedStrData = testobj._inputTranslateString(paramList)
            self.assertIsInstance(parsedStrData, list)
            self.assertEqual(len(parsedStrData), 2)

            expectedStr = "Enter translation template string. Use @paramName@ in the string to indicate where the \n"
            expectedStr += "function parameters should be inserted.\n"
            expectedStr += "Example with single input parameter name \"keyString\": Found argument key @keyString@\n"
            expectedStr += "Error: Too many template parameters in input string, expected 1 found 2\n"
            expectedStr += "User input template:\n"
            expectedStr += "    Test string with input @foo@ and @moo@\n"
            expectedStr += "Expected parameter list:\n"
            expectedStr += "    @foo@\n"
            self.assertEqual(output.getvalue(), expectedStr)

    def test32InputTranslateStringWithTooFewError(self):
        """!
        @brief Test _inputTranslateString method, improper message
        """
        inputStr = (text for text in ["Test string with input @foo@", "Test string with input @foo@ and @moo@"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription(self.testJson)
            paramList = [ParamRetDict.buildParamDictWithMod("foo", "string", "Test param one"),
                         ParamRetDict.buildParamDictWithMod("moo", "integer", "Test param two")]
            parsedStrData = testobj._inputTranslateString(paramList)
            self.assertIsInstance(parsedStrData, list)
            self.assertEqual(len(parsedStrData), 4)

            expectedStr = "Enter translation template string. Use @paramName@ in the string to indicate where the \n"
            expectedStr += "function parameters should be inserted.\n"
            expectedStr += "Example with single input parameter name \"keyString\": Found argument key @keyString@\n"
            expectedStr += "Error: Template parameter missing, found 1 of 2 expected template parameters.\n"
            expectedStr += "User input template:\n"
            expectedStr += "    Test string with input @foo@\n"
            expectedStr += "Expected parameter list:\n"
            expectedStr += "    @foo@, @moo@\n"
            self.assertEqual(output.getvalue(), expectedStr)

    def test33InputTranslateStringWithMisspellError(self):
        """!
        @brief Test _inputTranslateString method, improper message
        """
        inputStr = (text for text in ["Test string with input @goo@ and @moo@",
                                      "Test string with input @foo@ and @goo@",
                                      "Test string with input @doo@ and @goo@",
                                      "Test string with input @foo@ and @moo@"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription(self.testJson)
            paramList = [ParamRetDict.buildParamDictWithMod("foo", "string", "Test param one"),
                         ParamRetDict.buildParamDictWithMod("moo", "integer", "Test param two")]
            parsedStrData = testobj._inputTranslateString(paramList)
            self.assertIsInstance(parsedStrData, list)
            self.assertEqual(len(parsedStrData), 4)

            expectedStr = "Enter translation template string. Use @paramName@ in the string to indicate where the \n"
            expectedStr += "function parameters should be inserted.\n"
            expectedStr += "Example with single input parameter name \"keyString\": Found argument key @keyString@\n"
            expectedStr += "Error: Template parameter(s) misspelled, spelling error count 1\n"
            expectedStr += "User input template:\n"
            expectedStr += "    Test string with input @goo@ and @moo@\n"
            expectedStr += "Expected parameter list:\n"
            expectedStr += "    @foo@, @moo@\n"
            expectedStr += "Error: Template parameter(s) misspelled, spelling error count 1\n"
            expectedStr += "User input template:\n"
            expectedStr += "    Test string with input @foo@ and @goo@\n"
            expectedStr += "Expected parameter list:\n"
            expectedStr += "    @foo@, @moo@\n"
            expectedStr += "Error: Template parameter(s) misspelled, spelling error count 2\n"
            expectedStr += "User input template:\n"
            expectedStr += "    Test string with input @doo@ and @goo@\n"
            expectedStr += "Expected parameter list:\n"
            expectedStr += "    @foo@, @moo@\n"
            self.assertEqual(output.getvalue(), expectedStr)

    def test34InputTranslateStringWithDoubleParamError(self):
        """!
        @brief Test _inputTranslateString method, improper message
        """
        inputStr = (text for text in ["Test string with input @foo@, @foo@ and @moo@",
                                      "Test string with input @foo@ and @moo@"])
        def testMockIn(prompt):
            return next(inputStr)

        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch('builtins.input', testMockIn):
            testobj = StringClassDescription(self.testJson)
            paramList = [ParamRetDict.buildParamDictWithMod("foo", "string", "Test param one"),
                         ParamRetDict.buildParamDictWithMod("moo", "integer", "Test param two")]
            parsedStrData = testobj._inputTranslateString(paramList)
            self.assertIsInstance(parsedStrData, list)
            self.assertEqual(len(parsedStrData), 4)

            expectedStr = "Enter translation template string. Use @paramName@ in the string to indicate where the \n"
            expectedStr += "function parameters should be inserted.\n"
            expectedStr += "Example with single input parameter name \"keyString\": Found argument key @keyString@\n"
            expectedStr += "Error: Translation template parameter list does not match expected.\n"
            expectedStr += "   Found 3 parameters of expected 2 parameters in string.\n"
            expectedStr += "   Matched 3 parameters of expected 2 parameters in string.\n"
            expectedStr += "User input template:\n"
            expectedStr += "    Test string with input @foo@, @foo@ and @moo@\n"
            expectedStr += "Expected parameter list:\n"
            expectedStr += "    @foo@, @moo@\n"
            self.assertEqual(output.getvalue(), expectedStr)

if __name__ == '__main__':
    unittest.main()
