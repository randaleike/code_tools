"""@package langstringautogen
Utility to create a json language description list
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

class LanguageDescriptionList(object):
    """!
    Language description list data
    """
    def __init__(self, langListFileName = None):
        """!
        @brief LanguageDescriptionList constructor

        @param langListFileName (string) - Name of the json file containing
                                           the language description data
        """
        ## Path/file name of the JSON language decription file
        self.filename = "jsonLanguageDescriptionList.json"
        ## JSON language description data from the file
        self.langJsonData = {'default':{'name':"english", 'isoCode':"en"}, 'languages':{}}

        if langListFileName is not None:
            self.filename = langListFileName

        try:
            langJsonFile = open(self.filename, 'r', encoding='utf-8')
        except FileNotFoundError:
            self.langJsonData =  {'default':{'name':"english", 'isoCode':"en"}, 'languages':{}}
        else:
            self.langJsonData = json.load(langJsonFile)
            langJsonFile.close()

    def clear(self):
        """!
        @brief Reset all data to the default state
        """
        self.langJsonData = {'default':{'name':"english", 'isoCode':"en"}, 'languages':{}}

    def _printError(self, errorStr:str):
        """!
        @brief Output the error text to the console
        @param errorStr {string} Error text message
        """
        print ("Error: "+errorStr)

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

    def update(self):
        """!
        @brief Update the JSON file with the current contents of self.langJsonData
        """
        with open(self.filename, 'w', encoding='utf-8') as langJsonFile:
            json.dump(self.langJsonData, langJsonFile, indent=2)

    def setDefault(self, langName:str):
        """!
        @brief Set the default language
        @param langName (string) - Language name to use default if detection fails
        """
        if langName.lower() in self.langJsonData['languages'].keys():
            defaultDict = {'name':langName, 'isoCode':self.langJsonData['languages'][langName]['isoCode']}
            self.langJsonData['default'] = defaultDict
        else:
            self._printError("You must select a current language as the default.")
            print("Available languages:")
            for langName in list(self.langJsonData['languages']):
                print("  "+langName)

    def getDefaultData(self)->tuple:
        """!
        @brief Get the default language data
        @return tuple (string, string) - Default lauguage (entry name, ISO 639 set 3 language code)
        """
        defaultLang = self.langJsonData['default']['name']
        defaultIsoCode = self.langJsonData['default']['isoCode']
        return defaultLang, defaultIsoCode

    @staticmethod
    def _createLanguageEntry(linuxEnvCode:str = "", linuxRegionList:list = [],
                             windowsLangId:list = [], windowsRegionList:list = [],
                             iso639Code:str = "", compileSwitch:str = "")->dict:
        """!
        @brief Create a language dictionart entry

        @param linuxEnvCode (string) - linux LANG environment value for this language
        @param linuxRegionList (list of strings) - Linux LANG region codes for this language
        @param windowsLangId (list of numbers) - Windows LANGID & 0xFF value(s) for this language
        @param windowsRegionList (list of numbers) - Windows LANGID value(s) for this language
        @param iso639Code (string) - ISO 639 set 3 language code
        @param compileSwitch (string) - Language compile switch

        @return language dictionary object
        """
        langData = [('LANG', linuxEnvCode),
                    ('LANG_regions', linuxRegionList),
                    ('LANGID', windowsLangId),
                    ('LANGID_regions', windowsRegionList),
                    ('isoCode', iso639Code),
                    ('compileSwitch', compileSwitch)]
        langEntry = dict(langData)
        return langEntry

    def getLanguageList(self)->list:
        """!
        @brief Get a list of the current defined languages
        @return list of strings - Current ['languages'] keys
        """
        return list(self.langJsonData['languages'].keys())

    def getLanguagePropertyData(self, languageName:str, propertyName:str):
        """!
        @brief Get a list of the current defined languages
        @param languageName {string} Language entry key to fetch the ptoperty value from
        @param propertyName {string} Name of the property to get the value of
        @return any - property value
        """
        return self.langJsonData['languages'][languageName][propertyName]

    def getLanguageIsoCodeData(self, languageName:str)->str:
        """!
        @brief Get the ISO 639 code data for the given entryName language
        @param languageName {string} Language entry key to fetch the ptoperty value from
        @return string - Current ['languages'][entryName]['isoCode'] data
        """
        return self.langJsonData['languages'][languageName]['isoCode']

    def getLanguageLANGData(self, languageName:str)->tuple:
        """!
        @brief Get the LANG and LANG_regions data for the given entryName language
        @param languageName {string} Language entry key to fetch the ptoperty value from
        @return tuple (string, list of strings) - Current ['languages'][entryName]['LANG'] data,
                                                  and ['languages'][entryName]['LANGID_regions'] data
        """
        langCode = self.langJsonData['languages'][languageName]['LANG']
        regionList = self.langJsonData['languages'][languageName]['LANG_regions']
        return langCode, regionList

    def getLanguageLANGIDData(self, languageName:str)->tuple:
        """!
        @brief Get the LANGID and LANGID_regions data for the given entryName language
        @param languageName {string} Language entry key to fetch the ptoperty value from
        @return tuple (list of numbers, list of numbers) -
                Current ['languages'][entryName]['LANGID'] data,
                and ['languages'][entryName]['LANGID_regions'] data
        """
        langCode = self.langJsonData['languages'][languageName]['LANGID']
        regionList = self.langJsonData['languages'][languageName]['LANGID_regions']
        return langCode, regionList

    def getLanguageCompileSwitchData(self, languageName:str)->str:
        """!
        @brief Get the compileSwitch data for the given entryName language
        @param languageName {string} Language entry key to fetch the ptoperty value from
        @return string - Current ['languages'][entryName][compileSwitch] data
        """
        return self.langJsonData['languages'][languageName]['compileSwitch']

    @staticmethod
    def getLanguagePropertyList()->list:
        """!
        @brief Return a tuple list of the usable language dictionary entries
        @return list of language entry property names
        """
        entryTemplate = LanguageDescriptionList._createLanguageEntry()
        return list(entryTemplate.keys())

    @staticmethod
    def getLanguagePropertyReturnData(propertyName:str)->tuple:
        """!
        @brief Get the property description
        @param propertyName (string) Name of the property from getLanguagePropertyList()
        @return tuple - Data type (text|number) or None if the propertyName is unknown
                        Description or None if the propertyName is unknown
                        True if data is a list else False
        """
        if propertyName == 'LANG':
            return "string", "Linux environment language code", False
        elif propertyName == 'LANG_regions':
            return "string", "Linux environment region codes for this language code", True
        elif propertyName == 'LANGID':
            return "LANGID", "Windows LANGID & 0xFF language code(s)", True
        elif propertyName == 'LANGID_regions':
            return "LANGID", "Windows full LANGID language code(s)", True
        elif propertyName == 'isoCode':
            return "string", "ISO 639 set 1 language code", False
        elif propertyName == 'compileSwitch':
            return "string", "Compile switch definition for the language", False
        else:
            return None, None, False

    @staticmethod
    def isLanguagePropertyText(propertyName:str)->bool:
        """!
        @brief Return true if the data is stored as text or false if the data is stored as a number
        @param propertyName (string) Name of the property from getLanguagePropertyList()
        @return boolean - True if the data is stored as text or
                          False if the data is stored as a number
        """
        if propertyName == 'LANG':
            return True
        elif propertyName == 'LANG_regions':
            return True
        elif propertyName == 'LANGID':
            return False
        elif propertyName == 'LANGID_regions':
            return False
        elif propertyName == 'isoCode':
            return True
        elif propertyName == 'compileSwitch':
            return True
        else:
            return False

    @staticmethod
    def getLanguagePropertyMethodName(propertyName:str)->str:
        """!
        @brief Get the property method name
        @param propertyName (string) Name of the property from getLanguagePropertyList()
        @return string CPP description or None if the propertyName is unknown
        """
        if propertyName == 'LANG':
            return "getLANGLanguage"
        elif propertyName == 'LANG_regions':
            return "getLANGRegionList"
        elif propertyName == 'LANGID':
            return "getLANGIDCode"
        elif propertyName == 'LANGID_regions':
            return "getLANGIDList"
        elif propertyName == 'isoCode':
            return "getLangIsoCode"
        elif propertyName == 'compileSwitch':
            return "getLanguageCompileSwitch"
        else:
            return None

    @staticmethod
    def getLanguageIsoPropertyMethodName()->str:
        """!
        @brief Get the property method name
        @return string CPP description or None if the propertyName is unknown
        """
        return LanguageDescriptionList.getLanguagePropertyMethodName('isoCode')

    def addLanguage(self, langName:str, linuxEnvCode:str, linuxRegionList:list,
                    windowsLangId:list, windowsRegionList:list,
                    iso639Code:str, compileSwitch:str):
        """!
        @brief Add a language to the self.langJsonData data

        @param langName (string) - Language name to use for file/class name generation
        @param linuxEnvCode (string) - linux LANG environment value for this language
        @param linuxRegionList (list of strings) - Linux LANG region codes for this language
        @param windowsLangId (list of numbers) - Windows LANGID & 0xFF value(s) for this language
        @param windowsRegionList (list of numbers) - Windows LANGID value(s) for this language
        @param iso639Code (string) - ISO 639 set 3 language code
        @param compileSwitch (string) - Language compile switch
        """
        langEntry = self._createLanguageEntry(linuxEnvCode, linuxRegionList,
                                              windowsLangId, windowsRegionList,
                                              iso639Code, compileSwitch)
        self.langJsonData['languages'][langName] = langEntry

    def _inputLanguageName(self)->str:
        """!
        @brief Get the language from user input and check for validity
        @return string - language name
        """
        languageName = ""
        while(languageName == ""):
            name = input("Enter language name value to be used for class<lang> generation: ").lower()

            # Check validity
            if re.match('^[a-z]+$', name):
                # Valid name
                languageName = name
            else:
                # invalid name
                self._printError("Only characters a-z are allowed in the <lang> name, try again.")
        return languageName

    def _inputIsoTranslateCode(self)->str:
        """!
        @brief Get the ISO 639-1 translate language code from user input and check for validity
        @return string - translate code
        """
        isoTranslateId = ""
        while(isoTranslateId == ""):
            transId = input("Enter ISO 639-1 translate language code (2 lower case characters): ").lower()

            # Check validity
            if re.match('^[a-z]{2}$', transId):
                # Valid name
                isoTranslateId = transId
            else:
                # invalid name
                self._printError("Only two characters a-z are allowed in the code, try again.")
        return isoTranslateId

    def _inputLinuxLangCode(self)->str:
        """!
        @brief Get the linux language code from user input and check for validity
        @return string - linux language code
        """
        linuxLangId = ""
        while(linuxLangId == ""):
            linuxEnvCode = input("Enter linux language code (first 2 chars of 'LANG' environment value): ").lower()

            # Check validity
            if re.match('^[a-z]{2}$', linuxEnvCode):
                # Valid name
                linuxLangId = linuxEnvCode
            else:
                # invalid name
                self._printError("Only two characters a-z are allowed in the code, try again.")
        return linuxLangId

    def _inputLinuxLangRegions(self)->list:
        """!
        @brief Get the linux language region code(s) from user input and check for validity
        @return list of strings - linux region codes
        """
        linuxRegionList = []
        print ("Enter linux region code(s) (2 chars following the _ in the 'LANG' environment value).")
        print ("Enter empty string to exit.")

        while (True):
            region = input("Region value: ").upper()

            # Check validity
            if region == "":
                # End of list
                break
            elif re.match('^[A-Z]{2}$', region):
                # Valid region
                linuxRegionList.append(region)
            else:
                # invalid name
                self._printError("Only two characters A-Z are allowed in the code, try again.")
        return linuxRegionList

    def _inputWindowsLangIds(self)->tuple:
        """!
        @brief Get the windows language code(s) from user input
        @return tuple ([numbers], [numbers]) - windows LANGID codes.  First list is
                unique user LANGID codees & 0x0FF. Second list is all LANGID codes from user)
        """
        windowsIdCodeList = []
        windowsIdCodes = []
        print ("Enter Windows LANGID values. A value of 0 will exit.")
        while (True):
            region = int(input("LANGID value: "))
            if region == 0:
                break
            else:
                if region not in windowsIdCodeList:
                    windowsIdCodeList.append(region)

                    winId = region & 0x0FF
                    if winId not in windowsIdCodes:
                        windowsIdCodes.append(winId)

        return windowsIdCodes, windowsIdCodeList

    def newLanguage(self, override:bool = False)->bool:
        """!
        @brief Add a new language to the self.langJsonData data
        @param override {boolean} If true, override existing and force commit
        @return boolean - True if user selected to overwrite or commit
        """
        newEntry = {}
        entryCorrect = False

        while not entryCorrect:
            name = self._inputLanguageName()
            compileSwitch = name.upper()+"_ERRORS"
            isoCode = self._inputIsoTranslateCode()
            linuxLangCode = self._inputLinuxLangCode()
            linuxLangRegions = self._inputLinuxLangRegions()
            winCaseIds, winLangIds = self._inputWindowsLangIds()

            newEntry = self._createLanguageEntry(linuxLangCode, linuxLangRegions,
                                                 winCaseIds, winLangIds, isoCode, compileSwitch)

            # Print entry for user to inspect
            print("New Entry:")
            print(newEntry)
            commit = input("Is this correct? [Y/N]").upper()
            if ((commit == 'Y') or (commit == "YES")):
                entryCorrect = True


        # Determine if it's an overwrite or addition
        commitFlag = self._getCommitFlag(name, self.langJsonData['languages'].keys(), override)
        if commitFlag:
            self.langJsonData['languages'][name] = newEntry

        return commitFlag

    def __str__(self):
        """!
        @brief Convert JSON data to string
        """
        retStr = ""
        jsonLangData = self.langJsonData
        for langName, langData in jsonLangData['languages'].items():
            retStr += langName
            retStr += ": {\n"
            retStr += str(langData)
            retStr += "} end "
            retStr += langName
            retStr +="\n"

        retStr+= "Default = "
        retStr += str(jsonLangData['default']['name'])
        return retStr
