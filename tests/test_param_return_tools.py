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



from dir_init import pathincsetup
pathincsetup()

from code_tools_grocsoftware.base.param_return_tools import ParamRetDict

class TestUnittest01Buildmodification:
    """!
    @brief Unit test for the ParamRetDict class
    """
    def test01BuildMod(self):
        """!
        @brief Test build modification value function, default modification
        """
        testMod = ParamRetDict.buildDictModValue()
        assert 0 == testMod

    def test02BuildModList(self):
        """!
        @brief Test build modification value function, list modification
        """
        testMod = ParamRetDict.buildDictModValue(isList=True)
        assert ParamRetDict.typeModList == testMod

    def test03BuildModRef(self):
        """!
        @brief Test build modification value function, reference modification
        """
        testMod = ParamRetDict.buildDictModValue(isReference=True)
        assert ParamRetDict.typeModRef == testMod

    def test04BuildModPtr(self):
        """!
        @brief Test build modification value function, pointer modification
        """
        testMod = ParamRetDict.buildDictModValue(isPtr=True)
        assert ParamRetDict.typeModPtr == testMod

    def test05BuildModUndefined(self):
        """!
        @brief Test build modification value function, undefined modification
        """
        testMod = ParamRetDict.buildDictModValue(orUndef=True)
        assert ParamRetDict.typeModUndef == testMod

    def test06BuildModMultiple(self):
        """!
        @brief Test build modification value function, multiple modifications
        """
        testMod = ParamRetDict.buildDictModValue(True, True, True, True)
        assert 0x0F == testMod

    def test07TestIsFunctionsTrue(self):
        """!
        @brief Test the mod check functions
        """
        testMod = ParamRetDict.buildDictModValue(True, True, True, True)
        assert ParamRetDict.isModList(testMod)
        assert ParamRetDict.isModPointer(testMod)
        assert ParamRetDict.isModReference(testMod)
        assert ParamRetDict.isOrUndefType(testMod)

    def test08TestIsFunctionsTrue(self):
        """!
        @brief Test the mod check functions
        """
        testMod = ParamRetDict.buildDictModValue()
        assert not ParamRetDict.isModList(testMod)
        assert not ParamRetDict.isModPointer(testMod)
        assert not ParamRetDict.isModReference(testMod)
        assert not ParamRetDict.isOrUndefType(testMod)

    def test09TestIsFunctionsFalse(self):
        """!
        @brief Test the mod check functions
        """
        testMod = ParamRetDict.buildDictModValue()
        assert not ParamRetDict.isModList(testMod)
        assert not ParamRetDict.isModPointer(testMod)
        assert not ParamRetDict.isModReference(testMod)
        assert not ParamRetDict.isOrUndefType(testMod)

    def test10TestSetTypeModArraySize(self):
        """!
        @brief Test the get array size value
        """
        testList = [0,1,2,37,62,100,1000,10000]
        for testValue in testList:
            expectedVal = (testValue & ParamRetDict.typeModArrayMask) << ParamRetDict.typeModArrayShift
            assert expectedVal == ParamRetDict.setTypeModArraySize(0, testValue)

    def test11TestSetTypeModArraySizePtrOverride(self):
        """!
        @brief Test the get array size value
        """
        testList = [0,1,2,37,62,100,1000,10000]
        for testValue in testList:
            expectedVal = (testValue & ParamRetDict.typeModArrayMask) << ParamRetDict.typeModArrayShift
            assert expectedVal == ParamRetDict.setTypeModArraySize(ParamRetDict.typeModList, testValue)

    def test12TestGetArraySize(self):
        """!
        @brief Test the get array size value
        """
        testList = [0,1,2,37,62,100,1000,10000]
        for testValue in testList:
            testMod = ParamRetDict.setTypeModArraySize(0, testValue)
            assert testValue == ParamRetDict.getArraySize(testMod)

    def test13TestSetArraySize(self):
        """!
        @brief Test the get array size value
        """
        testList = [0,1,2,37,62,100,1000,10000]
        testDict = {'typeMod':0}

        for testValue in testList:
            testDict['typeMod'] = 0

            ParamRetDict.setArraySize(testDict, testValue)
            assert testValue == ParamRetDict.getArraySize(testDict['typeMod'])

class TestUnittest02ReturnDict:
    """!
    @brief Unit test for the ParamRetDict class
    """

    def test01BuildReturnDictDefaultMod(self):
        """!
        @brief Test build return dictionary function, default modification
        """
        testDict = ParamRetDict.buildReturnDict("string", "Test return base description")
        keyList = list(testDict.keys())
        assert 3 == len(keyList)
        assert 'type' in keyList
        assert 'desc' in keyList
        assert 'typeMod' in keyList

        assert "string" == testDict['type']
        assert "Test return base description" == testDict['desc']
        assert 0 == testDict['typeMod']

    def test02BuildReturnDictListMod(self):
        """!
        @brief Test build return dictionary function, list modification
        """
        testDict = ParamRetDict.buildReturnDict("string", "Test return list modification", True)
        keyList = list(testDict.keys())
        assert 3 == len(keyList)
        assert 'type' in keyList
        assert 'desc' in keyList
        assert 'typeMod' in keyList

        assert "string" == testDict['type']
        assert "Test return list modification" == testDict['desc']
        assert ParamRetDict.typeModList == testDict['typeMod']

    def test03BuildReturnDictRefMod(self):
        """!
        @brief Test build return dictionary function, reference modification
        """
        testDict = ParamRetDict.buildReturnDict("integer", "Test return reference modification", isReference=True)
        keyList = list(testDict.keys())
        assert 3 == len(keyList)
        assert 'type' in keyList
        assert 'desc' in keyList
        assert 'typeMod' in keyList

        assert "integer" == testDict['type']
        assert "Test return reference modification" == testDict['desc']
        assert ParamRetDict.typeModRef == testDict['typeMod']

    def test04BuildReturnDictPtrMod(self):
        """!
        @brief Test build return dictionary function, pointer modification
        """
        testDict = ParamRetDict.buildReturnDict("integer", "Test return pointer modification", isPtr=True)
        keyList = list(testDict.keys())
        assert 3 == len(keyList)
        assert 'type' in keyList
        assert 'desc' in keyList
        assert 'typeMod' in keyList

        assert "integer" == testDict['type']
        assert "Test return pointer modification" == testDict['desc']
        assert ParamRetDict.typeModPtr == testDict['typeMod']

    def test05BuildReturnDictUndefinedMod(self):
        """!
        @brief Test build return dictionary function, undefined modification
        """
        testDict = ParamRetDict.buildReturnDict("unsigned", "Test return undefined modification", orUndef=True)
        keyList = list(testDict.keys())
        assert 3 == len(keyList)
        assert 'type' in keyList
        assert 'desc' in keyList
        assert 'typeMod' in keyList

        assert "unsigned" == testDict['type']
        assert "Test return undefined modification" == testDict['desc']
        assert ParamRetDict.typeModUndef == testDict['typeMod']

    def test06BuildReturnDictMultipleMods(self):
        """!
        @brief Test build return dictionary function, multiple modifications
        """
        testDict = ParamRetDict.buildReturnDict("size", "Test return multiple modifications",
                                                isList=True, isReference=True, isPtr=True, orUndef=True)
        keyList = list(testDict.keys())
        assert 3 == len(keyList)
        assert 'type' in keyList
        assert 'desc' in keyList
        assert 'typeMod' in keyList

        assert "size" == testDict['type']
        assert "Test return multiple modifications" == testDict['desc']
        expectedMod = ParamRetDict.typeModList|ParamRetDict.typeModPtr|ParamRetDict.typeModRef|ParamRetDict.typeModUndef
        assert expectedMod == testDict['typeMod']

    def test07BuildReturnDictDefaultPlusArray(self):
        """!
        @brief Test build return dictionary function, add array set
        """
        testDict = ParamRetDict.buildReturnDict("float", "Test return array post modification")
        ParamRetDict.setArraySize(testDict, 7)

        keyList = list(testDict.keys())
        assert 3 == len(keyList)
        assert 'type' in keyList
        assert 'desc' in keyList
        assert 'typeMod' in keyList

        assert "float" == testDict['type']
        assert "Test return array post modification" == testDict['desc']
        expectedMod = 7 << ParamRetDict.typeModArrayShift
        assert expectedMod == testDict['typeMod']

    def test08BuildReturnDictPtrPlusArray(self):
        """!
        @brief Test build return dictionary function, pointer modification plus array set
        """
        testDict = ParamRetDict.buildReturnDict("float", "Test return ptr array post modification", isPtr=True)
        ParamRetDict.setArraySize(testDict, 8)

        keyList = list(testDict.keys())
        assert 3 == len(keyList)
        assert 'type' in keyList
        assert 'desc' in keyList
        assert 'typeMod' in keyList

        assert "float" == testDict['type']
        assert "Test return ptr array post modification" == testDict['desc']
        expectedMod = (8 << ParamRetDict.typeModArrayShift) | ParamRetDict.typeModPtr
        assert expectedMod == testDict['typeMod']

    def test09BuildReturnDictWithInputMod(self):
        """!
        @brief Test build return dictionary function, pointer modification plus array set
        """
        testDict = ParamRetDict.buildReturnDictWithMod("struct", "Test return dictionary with mode input", 55)

        keyList = list(testDict.keys())
        assert 3 == len(keyList)
        assert 'type' in keyList
        assert 'desc' in keyList
        assert 'typeMod' in keyList

        assert "struct" == testDict['type']
        assert "Test return dictionary with mode input" == testDict['desc']
        assert 55 == testDict['typeMod']

    def test10GetReturnData(self):
        """!
        @brief Test return dictionary get data function
        """
        testDict = ParamRetDict.buildReturnDictWithMod("struct", "Test return dictionary with mode input", ParamRetDict.typeModList)
        assert "struct" == ParamRetDict.getReturnType(testDict)
        assert "Test return dictionary with mode input" == ParamRetDict.getReturnDesc(testDict)
        assert ParamRetDict.typeModList == ParamRetDict.getReturnTypeMod(testDict)

    def test11GetReturnDataTuple(self):
        """!
        @brief Test return dictionary get data tuple function
        """
        testDict = ParamRetDict.buildReturnDictWithMod("struct", "Test return dictionary with mode input", ParamRetDict.typeModPtr)

        retType, retDesc, retMode = ParamRetDict.getReturnData(testDict)
        assert "struct" == retType
        assert "Test return dictionary with mode input" == retDesc
        assert ParamRetDict.typeModPtr == retMode


class TestUnittest03ParamDict:
    """!
    @brief Unit test for the ParamRetDict class
    """

    def test01BuildParamDictDefaultMod(self):
        """!
        @brief Test build parameter dictionary function, default modification
        """
        testDict = ParamRetDict.buildParamDict("foo", "string", "Test parameter base description")
        keyList = list(testDict.keys())
        assert 4 == len(keyList)
        assert 'name' in keyList
        assert 'type' in keyList
        assert 'desc' in keyList
        assert 'typeMod' in keyList

        assert "foo" == testDict['name']
        assert "string" == testDict['type']
        assert "Test parameter base description" == testDict['desc']
        assert 0 == testDict['typeMod']

    def test02BuildParamDictListMod(self):
        """!
        @brief Test build parameter dictionary function, list modification
        """
        testDict = ParamRetDict.buildParamDict("moo", "string", "Test parameter list modification", True)
        keyList = list(testDict.keys())
        assert 4 == len(keyList)
        assert 'name' in keyList
        assert 'type' in keyList
        assert 'desc' in keyList
        assert 'typeMod' in keyList

        assert "moo" == testDict['name']
        assert "string" == testDict['type']
        assert "Test parameter list modification" == testDict['desc']
        assert ParamRetDict.typeModList == testDict['typeMod']

    def test03BuildParamDictRefMod(self):
        """!
        @brief Test build parameter dictionary function, reference modification
        """
        testDict = ParamRetDict.buildParamDict("goo", "integer", "Test parameter reference modification", isReference=True)
        keyList = list(testDict.keys())
        assert 4 == len(keyList)
        assert 'name' in keyList
        assert 'type' in keyList
        assert 'desc' in keyList
        assert 'typeMod' in keyList

        assert "goo" == testDict['name']
        assert "integer" == testDict['type']
        assert "Test parameter reference modification" == testDict['desc']
        assert ParamRetDict.typeModRef == testDict['typeMod']

    def test04BuildParamDictPtrMod(self):
        """!
        @brief Test build parameter dictionary function, pointer modification
        """
        testDict = ParamRetDict.buildParamDict("shoo", "integer", "Test parameter pointer modification", isPtr=True)
        keyList = list(testDict.keys())
        assert 4 == len(keyList)
        assert 'name' in keyList
        assert 'type' in keyList
        assert 'desc' in keyList
        assert 'typeMod' in keyList

        assert "shoo" == testDict['name']
        assert "integer" == testDict['type']
        assert "Test parameter pointer modification" == testDict['desc']
        assert ParamRetDict.typeModPtr == testDict['typeMod']

    def test05BuildParamDictUndefinedMod(self):
        """!
        @brief Test build parameter dictionary function, undefined modification
        """
        testDict = ParamRetDict.buildParamDict("too", "unsigned", "Test parameter undefined modification", orUndef=True)
        keyList = list(testDict.keys())
        assert 4 == len(keyList)
        assert 'name' in keyList
        assert 'type' in keyList
        assert 'desc' in keyList
        assert 'typeMod' in keyList

        assert "too" == testDict['name']
        assert "unsigned" == testDict['type']
        assert "Test parameter undefined modification" == testDict['desc']
        assert ParamRetDict.typeModUndef == testDict['typeMod']

    def test06BuildParamDictMultipleMods(self):
        """!
        @brief Test build parameter dictionary function, multiple modifications
        """
        testDict = ParamRetDict.buildParamDict("yoo", "size", "Test parameter multiple modifications",
                                                isList=True, isReference=True, isPtr=True, orUndef=True)
        keyList = list(testDict.keys())
        assert 4 == len(keyList)
        assert 'name' in keyList
        assert 'type' in keyList
        assert 'desc' in keyList
        assert 'typeMod' in keyList

        assert "yoo" == testDict['name']
        assert "size" == testDict['type']
        assert "Test parameter multiple modifications" == testDict['desc']
        expectedMod = ParamRetDict.typeModList|ParamRetDict.typeModPtr|ParamRetDict.typeModRef|ParamRetDict.typeModUndef
        assert expectedMod == testDict['typeMod']

    def test07BuildParamDictDefaultPlusArray(self):
        """!
        @brief Test build parameter dictionary function, add array set
        """
        testDict = ParamRetDict.buildParamDict("pi", "float", "Test parameter array post modification")
        ParamRetDict.setArraySize(testDict, 7)

        keyList = list(testDict.keys())
        assert 4 == len(keyList)
        assert 'name' in keyList
        assert 'type' in keyList
        assert 'desc' in keyList
        assert 'typeMod' in keyList

        assert "pi" == testDict['name']
        assert "float" == testDict['type']
        assert "Test parameter array post modification" == testDict['desc']
        expectedMod = 7 << ParamRetDict.typeModArrayShift
        assert expectedMod == testDict['typeMod']

    def test08BuildParamDictPtrPlusArray(self):
        """!
        @brief Test build parameter dictionary function, pointer modification plus array set
        """
        testDict = ParamRetDict.buildParamDict("rugbyPlayers", "string", "Test parameter ptr array post modification", isPtr=True)
        ParamRetDict.setArraySize(testDict, 23)

        keyList = list(testDict.keys())
        assert 4 == len(keyList)
        assert 'name' in keyList
        assert 'type' in keyList
        assert 'desc' in keyList
        assert 'typeMod' in keyList

        assert "rugbyPlayers" == testDict['name']
        assert "string" == testDict['type']
        assert "Test parameter ptr array post modification" == testDict['desc']
        expectedMod = (23 << ParamRetDict.typeModArrayShift) | ParamRetDict.typeModPtr
        assert expectedMod == testDict['typeMod']

    def test09BuildParamDictWithInputMod(self):
        """!
        @brief Test build parameter dictionary function, pointer modification plus array set
        """
        testDict = ParamRetDict.buildParamDictWithMod("employees", "struct", "Test parameter dictionary with mode input", 0x0440002)

        keyList = list(testDict.keys())
        assert 4 == len(keyList)
        assert 'name' in keyList
        assert 'type' in keyList
        assert 'desc' in keyList
        assert 'typeMod' in keyList

        assert "employees" == testDict['name']
        assert "struct" == testDict['type']
        assert "Test parameter dictionary with mode input" == testDict['desc']
        assert 0x0440002 == testDict['typeMod']

    def test10GetParamData(self):
        """!
        @brief Test parameter dictionary get data function
        """
        testDict = ParamRetDict.buildParamDictWithMod("employees", "struct", "Test parameter dictionary with mode input", 0x0440002)
        assert "employees" == ParamRetDict.getParamName(testDict)
        assert "struct" == ParamRetDict.getParamType(testDict)
        assert "Test parameter dictionary with mode input" == ParamRetDict.getParamDesc(testDict)
        assert 0x0440002 == ParamRetDict.getParamTypeMod(testDict)

    def test11GetParamDataTuple(self):
        """!
        @brief Test parameter dictionary get data tuple function
        """
        testDict = ParamRetDict.buildParamDictWithMod("uid", "integer", "Test parameter dictionary with mode input", ParamRetDict.typeModPtr)
        paramName, paramType, paramDesc, paramMode = ParamRetDict.getParamData(testDict)

        assert "uid" == paramName
        assert "integer" == paramType
        assert "Test parameter dictionary with mode input" == paramDesc
        assert ParamRetDict.typeModPtr == paramMode
