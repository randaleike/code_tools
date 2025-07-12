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

import re
import json

from code_tools_grocsoftware.base.param_return_tools import ParamRetDict
from code_tools_grocsoftware.base.json_language_list import LanguageDescriptionList

class TranslationTextParser(object):
    """!
    Translation text helper functions
    """
    ## Text string marker
    parsedTypeText    = 'text'
    ## Parameter name marker
    parsedTypeParam   = 'param'
    ## Special character marker
    parsedTypeSpecial = 'special'

    def __init__(self):
        """!
        @brief TranslationTextParser constructor
        """
        pass

    @staticmethod
    def makeTextEntry(textBlock:str)->tuple:
        """!
        @brief Make a parsed text tuple object
        @param textBlock {string} Text string for the tuple
        @return tuple - (TranslationTextParser.parsedTypeText, textBlock)
        """
        return (TranslationTextParser.parsedTypeText, textBlock)

    @staticmethod
    def makeSpecialCharEntry(textBlock:str)->tuple:
        """!
        @brief Make a special character tuple object
        @param textBlock {string} Special character for the tuple
        @return tuple - (TranslationTextParser.parsedTypeSpecial, textBlock)
        """
        return (TranslationTextParser.parsedTypeSpecial, textBlock[0])

    @staticmethod
    def makeParamEntry(paramName:str)->tuple:
        """!
        @brief Make a parameter name tuple object
        @param paramName {string} Special character for the tuple
        @return tuple - (TranslationTextParser.parsedTypeParam, paramName)
        """
        return (TranslationTextParser.parsedTypeParam, paramName)

    @staticmethod
    def parseTextBlock(textBlock:str)->list:
        """!
        @brief Convert the input string to an output string stream
        @param textBlock {string} String to convert
        @return list of dictionaries - List of dictionary entries descibing the parsed string
        """
        matchList = re.finditer(r'\\|\"', textBlock)

        stringList = []
        previousEnd = 0
        for matchData in matchList:
            # Add text data prior to first match if any
            if matchData.start() > previousEnd:
                rawText = r'{}'.format(textBlock[previousEnd:matchData.start()])
                stringList.append(TranslationTextParser.makeTextEntry(rawText))

            # Add the matched parameter
            stringList.append(TranslationTextParser.makeSpecialCharEntry(matchData.group()))
            previousEnd = matchData.end()

        # Add the trailing string
        if previousEnd < len(textBlock):
            rawText = r'{}'.format(textBlock[previousEnd:])
            stringList.append(TranslationTextParser.makeTextEntry(rawText))

        return stringList

    @staticmethod
    def parseTranslateString(baseString:str)->list:
        """!
        @brief Convert the input string to an output string stream
        @param baseString {string} String to convert
        @return list of tuples - List of tuples descibing the parsed string
                                 tuple[0] = type, TranslationTextParser.parsedTypeText or TranslationTextParser.parsedTypeParam
                                 tuple[1] = data, if TranslationTextParser.parsedTypeText = text string
                                                  if TranslationTextParser.parsedTypeParam = parameter name
        """
        matchList = re.finditer(r'@[a-zA-Z_][a-zA-Z0-9_]*@', baseString)

        stringList = []
        previousEnd = 0
        for matchData in matchList:
            # Add text data prior to first match if any
            if matchData.start() > previousEnd:
                rawText = r'{}'.format(baseString[previousEnd:matchData.start()])
                stringList.extend(TranslationTextParser.parseTextBlock(rawText))

            # Add the matched parameter
            stringList.append(TranslationTextParser.makeParamEntry(matchData.group()[1:-1]))
            previousEnd = matchData.end()

        # Add the trailing string
        if previousEnd < len(baseString):
            rawText = r'{}'.format(baseString[previousEnd:])
            stringList.extend(TranslationTextParser.parseTextBlock(rawText))

        return stringList

    @staticmethod
    def assembleParsedStrData(stringTupleList:list)->str:
        """!
        @brief Assemble the input string description tuple list into a translation string
        @param stringTupleList (list) List of string description tuples
        @return string - Assempled text string ready for input into a language translation engine
        """
        returnText = ""
        for descType, descData in stringTupleList:
            if TranslationTextParser.parsedTypeText == descType:
                returnText += descData
            elif TranslationTextParser.parsedTypeParam == descType:
                returnText += '@'
                returnText += descData
                returnText += '@'
            elif TranslationTextParser.parsedTypeSpecial == descType:
                returnText += descData
            else:
                raise TypeError("Unknown string description tuple type: "+descType)

        return returnText

    @staticmethod
    def assembleStream(stringTupleList:list, streamOperator:str = "<<")->str:
        """!
        @brief Assemble the input string description tuple list into a translation string
        @param stringTupleList (list) List of string description tuples
        @param streamOperator (string) Language specific stream operator
        @return string - Assempled text string ready for input into a language translation engine
        """
        returnText = ""
        stringOpen = False

        for descType, descData in stringTupleList:
            if TranslationTextParser.parsedTypeText == descType:
                if not stringOpen:
                    returnText += " "
                    returnText += streamOperator
                    returnText += " \""
                    stringOpen = True
                returnText += descData
            elif TranslationTextParser.parsedTypeParam == descType:
                if stringOpen:
                    returnText += "\" "
                    returnText += streamOperator
                    returnText += " "
                    stringOpen = False
                returnText += descData
            elif TranslationTextParser.parsedTypeSpecial == descType:
                if not stringOpen:
                    returnText += " "
                    returnText += streamOperator
                    returnText += " \""
                    stringOpen = True
                returnText += "\\"+descData
            else:
                raise TypeError("Unknown string description tuple type: "+descType)

        # Close the open string if present
        if stringOpen:
            returnText += "\""
            stringOpen = False
        return returnText

    @staticmethod
    def assembleTestReturnString(stringTupleList:list, valueXlateDict:dict)->str:
        """!
        @brief Assemble the input string description tuple list into a translation string
        @param stringTupleList (list) List of string description tuples
        @param valueXlateDict (dict) Dictionary of param names and expected values
        @return string - Assempled text string ready for input into a language translation
                         expected string
        """
        returnText = ""
        for descType, descData in stringTupleList:
            if TranslationTextParser.parsedTypeText == descType:
                returnText += descData
            elif TranslationTextParser.parsedTypeParam == descType:
                value, isText = valueXlateDict[descData]
                returnText += value
            elif TranslationTextParser.parsedTypeSpecial == descType:
                returnText += "\\"+descData
            else:
                raise TypeError("Unknown string description tuple type: "+descType)
        return returnText

    @staticmethod
    def isParsedTextType(parsedTuple:tuple)->bool:
        """!
        @brief Check if the input pgetParsedStrDataarsed translation tuple is a text type
        @return boolean - True if tuple[0] == TranslationTextParser.parsedTypeText
                          else False
        """
        if parsedTuple[0] == TranslationTextParser.parsedTypeText:
            return True
        else:
            return False

    @staticmethod
    def isParsedParamType(parsedTuple:tuple)->bool:
        """!
        @brief Check if the input parsed translation tuple is a parameter type
        @return boolean - True if tuple[0] == TranslationTextParser.parsedTypeParam
                          else False
        """
        if parsedTuple[0] == TranslationTextParser.parsedTypeParam:
            return True
        else:
            return False

    @staticmethod
    def isParsedSpecialType(parsedTuple:tuple)->bool:
        """!
        @brief Check if the input parsed translation tuple is a special character type
        @return boolean - True if tuple[0] == TranslationTextParser.parsedTypeParam
                          else False
        """
        if parsedTuple[0] == TranslationTextParser.parsedTypeSpecial:
            return True
        else:
            return False

    @staticmethod
    def getParsedStrData(parsedTuple:tuple)->bool:
        """!
        @brief Get the tuple string data field
        @return string - paredTuple data field
        """
        return parsedTuple[1]


class StringClassDescription(object):
    """!
    String object class definitions
    """

    def __init__(self, stringDefFileName:str = None):
        """!
        @brief StringClassDescription constructor

        @param langListFileName (string) - Name of the json file containing
                                           the language description data
        """
        if stringDefFileName is None:
            self.filename = "jsonStringClassDescription.json"
        else:
            self.filename = stringDefFileName
        try:
            langJsonFile = open(self.filename, 'r', encoding='utf-8')
        except FileNotFoundError:
            self.stringJasonData = {'baseClassName': "baseclass",
                                    'namespace': "myNamespace",
                                    'dynamicCompileSwitch': "DYNAMIC_INTERNATIONALIZATION",
                                    'propertyMethods':{},
                                    'translateMethods':{}}
        else:
            self.stringJasonData = json.load(langJsonFile)
            langJsonFile.close()

        self.transClient = None  # open it only if and when we need it

    def _getCommitOverWriteFlag(self, entryName:str, override:bool = False)->bool:
        """!
        @brief Determine if the user is ready to commit the new entry over the existing one
        @param entryName {string} Name of the method that will be added
        @param override {boolean} True = force commit, False = ask user
        """
        commitFlag = False
        if override:
            commitFlag = True
        else:
            # Determine if we should overwrite existing
            commit = input("Overwrite existing "+entryName+" entry? [Y/N]").upper()
            if ((commit == 'Y') or (commit == "YES")):
                commitFlag = True
        return commitFlag

    def _getCommitNewFlag(self, entryName:str)->bool:
        """!
        @brief Determine if the user is ready to commit the new entry
        @param entryName {string} Name of the method that will be added
        """
        commit = input("Add new "+entryName+" entry? [Y/N]").upper()
        if ((commit == 'Y') or (commit == "YES")):
            return True
        else:
            return False

    def _getCommitFlag(self, entryName:str, entryKeys:list, override:bool = False)->bool:
        """!
        @brief Determine if the user is ready to commit the new entry
        @param entryName {string} Name of the method that will be added
        @param entryKeys {list of keys} List of the existing entry keys
        @param override {boolean} True = force commit, False = ask user
        """
        if entryName in entryKeys:
            return self._getCommitOverWriteFlag(entryName, override)
        else:
            return self._getCommitNewFlag(entryName)

    def setBaseClassName(self, className:str):
        """!
        @brief Update the base class name
        @param className {string} Base class name for the methods
        """
        self.stringJasonData['baseClassName'] = className

    def getBaseClassName(self)->str:
        """!
        @brief Get the base class name value
        @return string - Base class name for the methods
        """
        return self.stringJasonData['baseClassName']

    def getBaseClassNameWithNamespace(self, namespaceName:str, scopeOperator:str = '::')->str:
        """!
        @brief Return the base class name
        @param namespaceName {string} Namespace name
        @param scopeOperator {string} Programming language scope resolution operator
        @return string Base sting class name
        """
        return namespaceName+scopeOperator+self.getBaseClassName()

    def getLanguageClassName(self, languageName:str = None)->str:
        """!
        @brief Get the base class name value
        @param languageName {string} Language name to append to the base class name or None
        @return string - Generated class name for the methods
        """
        if languageName is None:
            return self.stringJasonData['baseClassName']
        else:
            return self.stringJasonData['baseClassName']+languageName.capitalize()

    def getLanguageClassNameWithNamespace(self, namespaceName:str, scopeOperator:str = '::', languageName:str = None)->str:
        """!
        @brief Return the base class name
        @param namespaceName {string} Namespace name
        @param scopeOperator {string} Programming language scope resolution operator
        @param languageName {string} Language name to append to the base class name or None
        @return string Base sting class name
        """
        return namespaceName+scopeOperator+self.getLanguageClassName(languageName)

    def setNamespaceName(self, namespace:str):
        self.stringJasonData['namespace'] = namespace

    def getNamespaceName(self):
        return self.stringJasonData['namespace']

    def setDynamicCompileSwitch(self, switch:str):
        self.stringJasonData['dynamicCompileSwitch'] = switch

    def getDynamicCompileSwitch(self):
        return self.stringJasonData['dynamicCompileSwitch']

    def _definePropertyFunctionEntry(self, propertyName:str = "", briefDesc:str = "",
                                     retType:str = "", retDesc:str = "", isList:bool = False)->dict:
        """!
        @brief Define a property string return function dictionary and
               return the entry to the caller

        @param propertyName {string} Name of the property
        @param briefDesc {string} Brief description of the function used in
                                  doxygen comment block generation
        @param retType {string} Return type string
        @param retDesc {string} Description of the return parserstr value
        @param islist {boolean} True = data is a list, False = single value

        @return {'name':<string>, 'briefDesc':<string>, 'params':[],
                 'return':ParamRetDict.buildReturnDict(retType, retDesc, isList),
                 'inline':<string>} property function dictionary
        """
        functionDict = {'name': propertyName,
                        'briefDesc': briefDesc,
                        'params': [],
                        'return': ParamRetDict.buildReturnDict(retType, retDesc, isList)
                        }
        return functionDict

    def getPropertyMethodList(self)->list:
        """!
        @brief Return a list of property method name strings
        @return list of strings - Names of the property methods
        """
        return list(self.stringJasonData['propertyMethods'].keys())

    def getIsoPropertyMethodName(self)->str:
        """!
        @brief Get the get ISO 639-1 code method name
        @return string - Get ISO code method name
        """
        propertyMethodList = self.getPropertyMethodList()
        for methodName in propertyMethodList:
            if self.stringJasonData['propertyMethods'][methodName]['name'] == 'isoCode':
                return methodName

        return None

    def getPropertyMethodData(self, methodName:str)->tuple:
        """!
        @brief Return the input methodName data
        @return (tuple) - {string} Language descption property name,
                          {string} Brief description of the property method for Doxygen comment,
                          {list of dictionaries} Parameter list (probably empty list),
                          {dictionary} Return data dictionary
        """
        entry = self.stringJasonData['propertyMethods'][methodName]
        return entry['name'], entry['briefDesc'], entry['params'], entry['return']

    def _defineTranslationDict(self, translateBaseLang:str = "en", translateText:list = None)->dict:
        """!
        @brief Create a translation dictionary
        @param translateBaseLang {string} ISO 639-1 language code for the input translateText string
        @param translateText {list} Parsed text of the message
        @return dictionary - {'base':<translateBaseLang>, 'text':<translateText>} Translate method translation string dictionary
        """
        return {translateBaseLang: translateText}

    def addManualTranslation(self, methodName:str, baseLang:str = "en", textData:list = None)->bool:
        """!
        @brief Add language text to the function definition
        @param methodName {string} Translation method name to add the language text to
        @param baseLang {sting} ISO 639-1 language code for the input textData string
        @param textData {list} Parsed text of the message
        @return boolean - True if it was added, else false
        """
        if methodName in self.stringJasonData['translateMethods']:
            if textData is not None:
                self.stringJasonData['translateMethods'][methodName]['translateDesc'][baseLang] = textData
                return True
            else:
                return False
        else:
            return False

    def _translateText(self, sourceLang:str, targetLang:str, text:str)->str:
        """!
        @brief Translate the input text
        @param sourceLang {string} ISO 639-1 language code of the input text
        @param targetLang {string} ISO 639-1 language code for the output text
        @param text {string} text to translate
        @return string - Translated text
        """
        from google.cloud import translate_v2
        if self.transClient is None:
            self.transClient = translate_v2.Client()

        if isinstance(text, bytes):
            text = text.decode("utf-8")

        translatedTextData = self.transClient.translate(text,
                                                        target_language=targetLang,
                                                        format_='text',
                                                        source_language=sourceLang,
                                                        model='nmt')
        rawTranslatedText = translatedTextData['translatedText']
        return rawTranslatedText

    def _translateMethodText(self, methodName:str, jsonLangData:LanguageDescriptionList = None):
        """!
        @brief Add language text to the function definition
        @param methodName {string} Translation method name to add the language text to
        @param jsonLangData {LanguageDescriptionList} Language list data
        """
        if jsonLangData is not None:
            # Get the list of supported languages and the list of existing translations
            languageList = jsonLangData.getLanguageList()
            existingLangages = list(self.stringJasonData['translateMethods'][methodName]['translateDesc'])

            # Determine if any language translations are missing
            for language in languageList:
                langIsoCode = jsonLangData.getLanguageIsoCodeData(language)
                if langIsoCode not in existingLangages:
                    # Use the first language
                    sourceLanguage = existingLangages[0]
                    baseTextData = self.stringJasonData['translateMethods'][methodName]['translateDesc'][sourceLanguage]
                    sourceText = TranslationTextParser.assembleParsedStrData(baseTextData)

                    # Translate and parse for storage
                    translatedText = self._translateText(sourceLanguage, langIsoCode, sourceText)
                    translatedTextData = TranslationTextParser.parseTranslateString(translatedText)
                    self.stringJasonData['translateMethods'][methodName]['translateDesc'][langIsoCode] = translatedTextData
        else:
            pass


    def _defineTranslateFunctionEntry(self, briefDesc:str = "", paramsList:list = [], retDict:dict = {},
                                      translateBaseLang:str = "en", translateText:list = None)->dict:
        """!
        @brief Define a property string return function dictionary and
               return the entry to the caller

        @param briefDesc {string} Brief description of the function used in
                                  doxygen comment block generation
        @param paramsList {list of dictionaries} List of the function parameter dictionary entrys
        @param retDict {dict} Return data dictionary
        @param translateBaseLang {string} ISO 639-1 language code for the input translateText string
        @param translateText {list} Parsed text of the message

        @return {'name':<string>, 'briefDesc':<string>, 'params':[],
                 'return':ParamRetDict.buildReturnDict('text', retDesc, False),
                 'translateDesc': {'base':<string> 'text':<string>}} Translate function dictionary
        """
        functionDict = {'briefDesc': briefDesc,
                        'params': paramsList,
                        'return': retDict,
                        'translateDesc': self._defineTranslationDict(translateBaseLang, translateText)
                        }
        return functionDict

    def getTranlateMethodList(self)->list:
        """!
        @brief Return a list of property method name strings
        @return list of strings - Names of the property methods
        """
        return list(self.stringJasonData['translateMethods'].keys())

    def getTranlateMethodFunctionData(self, methodName:str)->tuple:
        """!
        @brief Return the input methodName data
        @return (tuple) - {string} Brief description of the property method for Doxygen comment,
                          {list of dictionaries} Parameter list (probably empty list),
                          {dictionary} Return data dictionary
        """
        entry = self.stringJasonData['translateMethods'][methodName]
        return entry['briefDesc'], entry['params'], entry['return']

    def getTranlateMethodTextData(self, methodName:str, targetLanguage:str)->list:
        """!
        @brief Return the input methodName data
        @param methodName (string) Name of the method to retrive data from
        @param targetLanguage (string) Name of the target language to retrive
        @return (tuple list) - Parsed text list
        """
        return self.stringJasonData['translateMethods'][methodName]['translateDesc'][targetLanguage]

    def _inputIsoTranslateCode(self)->str:
        """!
        @brief Get the ISO 639-1 translate language code from user input and check for validity
        @return string - translate code
        """
        isoTranslateId = ""
        while(isoTranslateId == ""):
            transId = input("Enter original string ISO 639-1 translate language code (2 lower case characters): ").lower()

            # Check validity
            if re.match('^[a-z]{2}$', transId):
                # Valid name
                isoTranslateId = transId
            else:
                # invalid name
                print("Error: Only two characters a-z are allowed in the code, try again.")
        return isoTranslateId

    def _inputVarMethodName(self, methodName:bool = False)->str:
        """!
        @brief Get the parameter or method name
        @param methodName {boolean} True if this is a method name call, else False (default)
        @return string - Validated name value
        """
        validatedName = ""
        while(validatedName == ""):
            if methodName:
                name = input("Enter method name: ")
            else:
                name = input("Enter parameter name: ")
            name.strip()

            # Check validity
            if re.match('^[a-zA-Z_][a-zA-Z0-9_]*$', name):
                # Valid name
                validatedName = name
            else:
                # invalid name
                print("Error: "+name+" is not a valid code name, try again.")
        return validatedName


    def _inputArrayModifier(self, currentMod:int)->int:
        """!
        @brief Get the array size value from the user
        @param currentMod {int} Current typeMode value from ParamRetDict.buildDictModValue
        @return int - Modified typeMod value with array data added
        """
        while True:
            arraySize = input("Size of the array in entries: ")
            try:
                intArraySize = int(arraySize)
                if (intArraySize > 0) and (intArraySize < 65536):
                    return ParamRetDict.setTypeModArraySize(currentMod, intArraySize)
                else:
                    print ("Error: must be a valid number between 1 and 65535")
            except:
                print ("Error: must be an integer value")

    def _inputTypeModifier(self)->int:
        """!
        @brief Get the parameter or method name
        @return int - ParamRetDict typeMod value,
        """
        # Check for list modification
        isListType = input("Is full type a list [y/n]:").lower()
        if (isListType == 'y') or (isListType == 'yes'):
            isList = True
        else:
            isList = False

        # Check for pointer modification
        isPtrType = input("Is full type a pointer [y/n]:").lower()
        if (isPtrType == 'y') or (isPtrType == 'yes'):
            isPtr = True
        else:
            isPtr = False

        # Check for reference modification
        isRefType = input("Is full type a reference [y/n]:").lower()
        if (isRefType == 'y') or (isRefType == 'yes'):
            isReference = True
        else:
            isReference = False

        # Check for undefined modification
        canBeUndef = input("Can value be undefined [y/n]:").lower()
        if (canBeUndef == 'y') or (canBeUndef == 'yes'):
            orUndef = True
        else:
            orUndef = False

        # Generate basic modification
        typeMod = ParamRetDict.buildDictModValue(isList, isReference, isPtr, orUndef)

        # Check for array modification
        isArrayType = input("Is full type an array [y/n]:").lower()
        if (isArrayType == 'y') or (isArrayType == 'yes'):
            typeMod = self._inputArrayModifier(typeMod)

        return typeMod

    def _inputParamReturnType(self, returnType:bool = False)->tuple:
        """!
        @brief Get the parameter or method name
        @param returnType {boolean} True if this is a return type fetch, else False (default)
        @return tuple - String Validated name value,
                        Boolean is list,
                        Boolean is pointer type,
                        Boolean is reference type
        """
        varType = ""
        while(varType == ""):
            if returnType:
                promptStr = "Enter return base type"
            else:
                promptStr = "Enter parameter base type"

            inputType = input(promptStr+" [T(ext)|i(nteger)|u(nsigned)|s(ize)|c(ustom)]: ").lower()

            # Check validity
            if (inputType == "s") or (inputType=="size"):
                varType = "size"
            elif (inputType == "t") or (inputType=="text") or (inputType=="string"):
                varType = "string"
            elif (inputType == "i") or (inputType=="integer") or (inputType=="int"):
                varType = "integer"
            elif (inputType == "u") or (inputType=="unsigned"):
                varType = "unsigned"
            elif (inputType == "c") or (inputType=="custom"):
                # Note: Custom type class must have a stream operator method defined.
                customType = input("Enter custom type: ")
                if re.match('^[a-zA-Z_][a-zA-Z0-9_:]*$', customType):
                    # valid
                    varType = customType
                else:
                    # invalid type
                    print (customType+" is not a valid code type name, try again.")
            else:
                # invalid name
                print("Error: \""+inputType+"\" unknown. Please select one of the options from the menu.")

        typeMod = self._inputTypeModifier()
        return varType, typeMod

    def _inputParameterData(self)->dict:
        """!
        @brief Get input parameter data from user input
        @return dictionary - Param dictionary from  ParamRetDict.buildParamDict()
        """
        paramName = self._inputVarMethodName()
        paramType, paramMod = self._inputParamReturnType()
        paramDesc = input("Enter brief parameter description for doxygen comment: ")
        return ParamRetDict.buildParamDictWithMod(paramName, paramType, paramDesc, paramMod)

    def _inputReturnData(self)->dict:
        """!
        @brief Get the return data description from the user
        @return dictionary - Return dictionary from  ParamRetDict.buildReturnDict()
        """
        returnType, returnMod = self._inputParamReturnType(True)
        retDesc = input("Enter brief description of the return value for doxygen comment: ")
        return ParamRetDict.buildReturnDictWithMod(returnType, retDesc, returnMod)

    def update(self):
        """!
        @brief Update the JSON file with the current contents of self.langJsonData
        """
        with open(self.filename, 'w', encoding='utf-8') as langJsonFile:
            json.dump(self.stringJasonData, langJsonFile, indent=2)

    def _validateTranslateString(self, paramList:list, testString:str):
        """!
        @brief Get the translation string template for the new translate function

        @param paramList {list of dictionaries} List of parameter description dictionaries
                                                for this function
        @param testString {string} String to check for validity

        @return boolean - True if string has all parameters correctly marked, else False
        @return number - Number of matched items
        @return number - Number of parameters found in the input string
        """
        # Construct the expected list
        expectedParamList = []
        for param in paramList:
            paramName = ParamRetDict.getParamName(param)
            expectedParamList.append(paramName)

        # Break the string into it's component parts
        parsedStrData = TranslationTextParser.parseTranslateString(testString)

        # Check the broken string counts
        matchCount = 0
        paramCount = 0
        for parsedData in parsedStrData:
            if TranslationTextParser.isParsedParamType(parsedData):
                paramCount +=1
                if TranslationTextParser.getParsedStrData(parsedData) in expectedParamList:
                    matchCount+=1

        if (matchCount == len(expectedParamList)) and (paramCount == matchCount):
            # Return success
            return True, matchCount, paramCount, parsedStrData
        else:
            # Return failure
            return False, matchCount, paramCount, parsedStrData

    def _inputTranslateString(self, paramList:list)->list:
        """!
        @brief Get the translation string template for the new translate function

        @param paramList {list of dictionaries} List of parameter description dictionaries
                                                for this function

        @return list - Validated TranslationTextParser text/data list
        """
        # Build parameter list help string
        expectedParamHelp = ""
        prefix = ""
        for param in paramList:
            paramName = ParamRetDict.getParamName(param)
            expectedParamHelp += prefix
            expectedParamHelp += '@'
            expectedParamHelp += paramName
            expectedParamHelp += '@'
            prefix = ", "

        # Get the translate string from the user
        stringValid = False
        translateString = ""

        print("Enter translation template string. Use @paramName@ in the string to indicate where the ")
        print("function parameters should be inserted.")
        print("Example with single input parameter name \"keyString\": Found argument key @keyString@")

        while not stringValid:
            translateString = input("String:")
            stringValid, matchCount, paramCount, parsedString = self._validateTranslateString(paramList, translateString)

            if not stringValid:
                if (len(paramList) > matchCount) and (len(paramList) > paramCount):
                    print ("Error: Template parameter missing, found "+str(matchCount)+" of "+str(len(paramList))+" expected template parameters.")
                elif (len(paramList) > matchCount) and (len(paramList) == paramCount):
                    print ("Error: Template parameter(s) misspelled, spelling error count "+str(paramCount-matchCount))
                elif (len(paramList) == matchCount) and (len(paramList) < paramCount):
                    print ("Error: Too many template parameters in input string, expected "+str(matchCount)+" found "+str(paramCount))
                else:
                    print ("Error: Translation template parameter list does not match expected.")
                    print ("   Found "+str(paramCount)+" parameters of expected "+str(len(paramList))+" parameters in string.")
                    print ("   Matched "+str(matchCount)+" parameters of expected "+str(len(paramList))+" parameters in string.")
                print("User input template:")
                print("    "+translateString)
                print("Expected parameter list:")
                print("    "+expectedParamHelp)

        return parsedString

    def newTranslateMethodEntry(self, languageList:LanguageDescriptionList = None, override:bool = False)->bool:
        """!
        @brief Define and add a new translate string return function dictionary
               to the list of translate functions
        @param languageList {LanguageDescriptionList | None} Supported language description data or None
        @param override {boolean} True = Override existing without asking
        @return boolean True if new entry was written, else false
        """
        newEntry = {}
        entryCorrect = False

        while not entryCorrect:
            methodName = self._inputVarMethodName(True)
            methodDesc = input("Enter brief function description for doxygen comment: ")

            paramList = []
            paramCount = int(input("Enter parameter count? [0-n]: "))
            while(paramCount > 0):
                paramList.append(self._inputParameterData())
                paramCount -= 1

            returnDict = self._inputReturnData()

            languageBase = self._inputIsoTranslateCode()
            translateString = self._inputTranslateString(paramList)
            newEntry = self._defineTranslateFunctionEntry(methodDesc, paramList, returnDict, languageBase, translateString)

            # Print entry for user to inspect
            print("New Entry:")
            print(newEntry)
            commit = input("Is this correct? [Y/N]").upper()
            if ((commit == 'Y') or (commit == "YES")):
                entryCorrect = True

        # Test existing for match
        commitFlag = self._getCommitFlag(methodName, self.stringJasonData['translateMethods'].keys(), override)
        if commitFlag:
            self.stringJasonData['translateMethods'][methodName] = newEntry
            self._translateMethodText(methodName, languageList)

        return commitFlag

    def addTranslateMethodEntry(self, methodName:str, methodDesc:str, paramList:list,
                                returnDict:dict, isoLangCode:str, translateString:str,
                                override:bool = False, languageList:LanguageDescriptionList = None)->bool:
        """!
        @brief Add a new translate string return function dictionary
               to the list of translate functions
        @param methodName {string} Name of the function
        @param methodDesc {string} Brief description of the function for doxygen comment generation
        @param paramList {list of dictionaries} List of the input parameter description dictionaries
        @param returnDict {dict} Return dictionary definition
        @param isoLangCode {string} ISO 639-1 language code of the input translateString
        @param translateString {string} String to generate translations for        @return boolean True if new entry was written, else false

        @param override {boolean} True = Override existing without asking
        @param languageList {LanguageDescriptionList | None} Supported language description data or None
        @return boolean True if new entry was written, else false
        """
        status, matchCount, paramCount, parsedStrData = self._validateTranslateString(paramList, translateString)
        if not status:
            print ("Error: Invalid translation string: "+translateString+". paramCount= "+str(paramCount)+" matchCount= "+str(matchCount))
            return False

        newEntry = self._defineTranslateFunctionEntry(methodDesc, paramList, returnDict, isoLangCode, parsedStrData)

        commitFlag = True
        if methodName in self.stringJasonData['translateMethods'].keys():
            # Determine if we should overwrite existing
            commitFlag = self._getCommitOverWriteFlag(methodName, override)

        if commitFlag:
            self.stringJasonData['translateMethods'][methodName] = newEntry
            self._translateMethodText(methodName, languageList)

        return commitFlag

    def _getPropertyReturnData(self):
        """!
        @brief Get the property function return data and property name
        @return string, string, string, string - Language description property name,
                                                 Method name,
                                                 Method return type,
                                                 Return type description for Doxygen comment
                                                 True if return is a list, else False
        """
        propertyOptions = LanguageDescriptionList.getLanguagePropertyList()

        print ("Select language property, from options:")
        optionText = ""
        optionPrefix = "    "
        maxIndex = 0
        for index, propertyId in enumerate(propertyOptions):
            optionText += optionPrefix
            optionText += str(index)+": "
            optionText += propertyId
            optionPrefix = ", "
            maxIndex += 1
        print (optionText)

        propertyId = None
        while propertyId is None:
            propertyIndex = int(input("Enter property [0 - "+str(maxIndex-1)+"]: "))
            if (propertyIndex >= 0) and (propertyIndex < maxIndex):
                propertyId = propertyOptions[propertyIndex]
            else:
                print ("Valid input values are 0 to "+str(maxIndex-1)+", try again")

        returnType, returnDesc, isList = LanguageDescriptionList.getLanguagePropertyReturnData(propertyId)
        methodName = LanguageDescriptionList.getLanguagePropertyMethodName(propertyId)
        return propertyId, methodName, returnType, returnDesc, isList

    def newPropertyMethodEntry(self, override:bool = False)->bool:
        """!
        @brief Define and add a property string return function dictionary and
               add it to the list of translate functions
        @param override {boolean} True = Override existing without asking
        @return boolean True if new entry was written, else false
        """
        newEntry = {}
        entryCorrect = False

        while not entryCorrect:
            propertyName, methodName, returnType, returnDesc, isList = self._getPropertyReturnData()
            methodDesc = "Get the "+returnDesc+" for this object"

            newEntry = self._definePropertyFunctionEntry(propertyName, methodDesc, returnType, returnDesc, isList)

            # Print entry for user to inspect
            print(methodName+":")
            print(newEntry)
            commit = input("Is this correct? [Y/N]").upper()
            if ((commit == 'Y') or (commit == "YES")):
                entryCorrect = True

        # Check for existing for match
        commitFlag = self._getCommitFlag(methodName, self.stringJasonData['propertyMethods'].keys(), override)
        if commitFlag:
            self.stringJasonData['propertyMethods'][methodName] = newEntry

        return commitFlag

    def addPropertyMethodEntry(self, propertyName:str, override:bool = False)->bool:
        """!
        @brief Add a new translate string return function dictionary
               to the list of translate functions
        @param propertyName {string} LanguageDescriptionList.getLanguagePropertyList() property key
        @param override {boolean} True = Override existing without asking
        @return boolean True if new entry was written, else false
        """
        # Make sure property exists in the language data
        propertyList = LanguageDescriptionList.getLanguagePropertyList()
        commitFlag = False

        # Property exists, generate the new entry
        if propertyName in propertyList:
            returnType, returnDesc, isList = LanguageDescriptionList.getLanguagePropertyReturnData(propertyName)
            methodDesc = "Get the "+returnDesc+" for this object"
            methodName = LanguageDescriptionList.getLanguagePropertyMethodName(propertyName)

            newEntry = self._definePropertyFunctionEntry(propertyName, methodDesc, returnType, returnDesc, isList)

            commitFlag = self._getCommitFlag(methodName, self.stringJasonData['propertyMethods'].keys(), override)
            if commitFlag:
                # Add the entry
                self.stringJasonData['propertyMethods'][methodName] = newEntry

        return commitFlag

    def updateTranlations(self, jsonLangData:LanguageDescriptionList = None):
        """!
        @brief Update the translation strings in the translation methods
        @param jsonLangData {LanguageDescriptionList} Updated language list defintions
        """
        methodList = self.getTranlateMethodList()
        for methodName in methodList:
            self._translateMethodText(methodName, jsonLangData)
