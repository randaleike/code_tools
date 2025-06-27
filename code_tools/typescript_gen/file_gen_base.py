"""@package commonProgramFileTools
Utility classes for programming language file generation
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

from datetime import datetime

from code_tools.base.copyright_tools import CopyrightGenerator
from code_tools.base.eula import EulaText

from code_tools.base.comment_gen_tools import TsCommentGenerator
from code_tools.base.doxygen_gen_tools import TsDoxyCommentGenerator
from code_tools.base.param_return_tools import ParamRetDict

#============================================================================
#============================================================================
# File generation helper class
#============================================================================
#============================================================================
class GenerateTypeScriptFileHelper(object):
    """!
    @brief File generation helper class.

    This class implements boiler plate data and helper functions used by
    the parent file specific generation class to generate the file
    """
    def __init__(self, eulaName:str|None = None):
        """!
        @brief GenerateFileHelper constructor

        @param eulaName {string} Name of the EULA from EulaText class to use.
        """
        super().__init__()

        ## Copyright string generator for the file header generation
        self.copyrightGenerator = CopyrightGenerator()
        ## End User Licence Agreement (EULA) for the file header generation
        self.eula = None
        ## Standard indentation for code blocks
        self.levelTabSize = 4

        ## C/CPP Doxygen comment generator for generating doxygen comment blocks
        self.doxyCommentGen = TsDoxyCommentGenerator()
        ## C/CPP comment generator for single line and block comments
        self.headerCommentGen = TsCommentGenerator(80)

        ## Translation dictionary from generic data types to CPP specific data types
        self.typeXlationDict = {'string':"string",
                                'text':"string",
                                'size':"number",
                                'integer':"number",
                                'unsigned':"number",
                                'tuple':"tuple"}

        if eulaName is None:
            self.eula = EulaText("MIT_open")
        else:
            self.eula = EulaText(eulaName)

    def _declareType(self, baseType:str, typeMod:int=0)->str:
        """!
        @brief Generate the type text based on the input type name and type modification data
        @param baseType (str) Delclaration type
        @param typeMod (int) ParamRetDict type modification code
        @return string typescript type specification
        """
        typeReturn = baseType
        if baseType in list(self.typeXlationDict.keys()):
            typeReturn = self.typeXlationDict[baseType]

        arraySize = ParamRetDict.getArraySize(typeMod)
        if ParamRetDict.isModList(typeMod) or (arraySize > 0):
            typeReturn += "[]"
        if ParamRetDict.isOrUndefType(typeMod):
            typeReturn += "|undefined"
        return typeReturn

    def _xlateParams(self, paramDictList:list)->list:
        """!
        @brief Translate the generic parameter list type strings to the typescript specific parameter type strings
        @param paramDictList {list} List of ParamRetDict parameter dictionaries to translate
        @return list - List of ParamRetDict parameter dictionaries with the translated type
        """
        xlatedParams = []
        for param in paramDictList:
            xlatedType = self._declareType(ParamRetDict.getParamType(param), ParamRetDict.getParamTypeMod(param))
            xlatedParam = ParamRetDict.buildParamDictWithMod(ParamRetDict.getParamName(param),
                                                             xlatedType,
                                                             ParamRetDict.getParamDesc(param),
                                                             0)
            xlatedParams.append(xlatedParam)
        return xlatedParams

    def _xlateReturnDict(self, retDict:dict|None)->dict|None:
        """!
        @brief Translate the generic return dictionary to the typescript specific return dictionary
        @param retDict {dictionary} ParamRetDict return dictionary to translate
        @return dictionary|None - ParamRetDict return dictionary with the translated type or None if input is None
        """
        if retDict is not None:
            xlatedType = self._declareType(ParamRetDict.getReturnType(retDict), ParamRetDict.getReturnTypeMod(retDict))
            return ParamRetDict.buildReturnDictWithMod(xlatedType, ParamRetDict.getReturnDesc(retDict), 0)
        else:
            return None

    def _genFunctionRetType(self, retDict:dict|None = None)->str:
        """!
        @brief Generate the type text based on the variable input ParamRetDict dictionary
        @param retDict (dict|None) Variable ParamRetDict description dictionary
        @return string - : Type(s)
        """
        if retDict is not None:
            typeName = ParamRetDict.getReturnType(retDict)
            typeMod = ParamRetDict.getReturnTypeMod(retDict)
            returnText = ":"
            returnText += self._declareType(typeName, typeMod)
        else:
            returnText = ""
        return returnText

    def _genFunctionParams(self, paramDictList:list)->str:
        """!
        @brief Generate the parameter method string
        @param paramDictList (list) List of parameter dictionaries
        @return string - (typespec name, ...)
        """
        paramPrefix = ""
        paramText = "("
        for paramDict in paramDictList:
            typeName = ParamRetDict.getParamType(paramDict)
            typeMod = ParamRetDict.getParamTypeMod(paramDict)

            paramText += paramPrefix
            paramText += ParamRetDict.getParamName(paramDict)
            paramText += ":"
            paramText += self._declareType(typeName, typeMod)
            paramPrefix = ", "
        paramText += ")"
        return paramText

    def _declareFunctionWithDecorations(self, name:str, briefdesc:str, paramDictList:list, retDict:dict|None = None,
                                        indent:int = 0, noDoxygen:bool = False, prefixDecaration:str = "public",
                                        postfixDecaration:str|None = None, inlinecode:list = [],
                                        longDesc:str|None = None)->list:
        """!
        @brief Generate a function declatation text block with doxygen comment

        @param name {string} Function name
        @param briefdesc {string} Function description
        @param paramDictList {list of dictionaries} - Return parameter data
        @param retDict {dictionary or None} - Return parameter data or None
        @param indent {integer} Comment and function declaration indentation
        @param noDoxygen {boolean} True skip doxygen comment generation, False generate doxygen comment block
        @param prefixDecaration {string} Valid C/C++ declaration prefix decoration, i.e "virtual"
        @param postfixDecaration {string} Valid C/C++ declaration postfix decoration, i.e "const" | "override" ...
        @param inlinecode {sting list or None} Inline code for the declaration or None id there is no inline definition
        @param longDesc {string or None} Long description of the function

        @return string list - Function doxygen comment block and declaration
        """
        funcDeclareText = []

        # Add doxygen comment block
        if not noDoxygen:
            xlatedParamList = self._xlateParams(paramDictList)
            xlatedRet = self._xlateReturnDict(retDict)
            funcDeclareText.extend(self.doxyCommentGen.genDoxyMethodComment(briefdesc, xlatedParamList, xlatedRet, longDesc, indent))

        # Add function post fix decorations if defined
        if postfixDecaration is not None:
            funcDeclareText.append("".rjust(indent, ' ') + postfixDecaration+"\n")

        # Create function declaration line
        funcLine = "".rjust(indent, ' ')

        # Add function prefix definitions if defined
        funcLine += prefixDecaration
        funcLine += " "
        funcLine += name

        # Add the function parameters
        funcLine += self._genFunctionParams(paramDictList)

        # Construct main function declaration
        funcLine += self._genFunctionRetType(retDict)

        # Add inline code
        funcLine += "\n"
        funcDeclareText.append(funcLine)
        inlineIndent = "".rjust(indent, ' ')
        inlineStart = inlineIndent+"{"
        if len(inlinecode) == 1:
            funcDeclareText.append(inlineStart+inlinecode[0]+"}\n")
        else:
            funcDeclareText.append(inlineStart+"\n")
            inlineBodyIndent = "".rjust(indent+self.levelTabSize, ' ')
            for codeLine in inlinecode:
                funcDeclareText.append(inlineBodyIndent+codeLine+"\n")
            funcDeclareText.append(inlineIndent+"}\n")

        return funcDeclareText

    def _defineFunctionWithDecorations(self, name:str, briefdesc:str, paramDictList:list, retDict:dict,
                                       noDoxygen:bool = False, prefixDecaration:str|None = None,
                                       postfixDecaration:str|None = None, longDesc:list|None = None)->list:
        """!
        @brief Generate a function definition start with doxygen comment

        @param name {string} Function name
        @param briefdesc {string} Function description
        @param paramDictList {list of dictionaries} - Return parameter data
        @param retDict {dictionary} - Return parameter data
        @param noDoxygen {boolean} True skip doxygen comment generation, False generate doxygen comment block
        @param prefixDecaration {string or None} Valid C/C++ decldefineFunctionWithDecorationsaration prefix decoration, i.e "virtual"
        @param postfixDecaration {string or None} Valid C/C++ declaration postfix decoration, i.e "const" | "override" ...
        @param longDesc {string or None} Long description of the function

        @return string list - Function doxygen comment block and declaration start
        """
        funcDefineText = []

        # Add doxygen comment block
        if not noDoxygen:
            xlatedParamList = self._xlateParams(paramDictList)
            xlatedRet = self._xlateReturnDict(retDict)
            funcDefineText.extend(self.doxyCommentGen.genDoxyMethodComment(briefdesc, xlatedParamList, xlatedRet,
                                                                           longDesc))

        # Check for prefix
        funcLine = ""
        if prefixDecaration is not None:
            funcLine += prefixDecaration
            funcLine += " "

        # Create function declaration line
        funcLine += "function "

        # Construct main function declaration
        funcLine += name

        # Add the function parameters and return type
        funcLine += self._genFunctionParams(paramDictList)
        funcLine += self._genFunctionRetType(retDict)

        # Open the function
        funcDefineText.append(funcLine+"\n")
        funcDefineText.append("{\n")

        return funcDefineText

    def _endFunction(self, name:str)->str:
        """!
        @brief Get the function declaration string for the given name
        @param name (string) - Function name
        @return string - Function close with comment
        """
        return "} // end of function "+name+"\n"

    def _generateGenericFileHeader(self, autotoolname:str, startYear:int=2025, owner:str|None = None)->list:
        """!
        @brief Generate the boiler plate file header with copyright and eula

        @param autotoolname {string} Auto generation tool name for comments
        @param startYear {number} First copyright year
        @param owner {string or None} File owner for copyright message or None
        @return list of strings - Code to output
        """
        commentText = []
        copyrightEulaText = []
        if owner is not None:
            # Generate copyright and EULA text
            currentYear = datetime.now().year
            copyrightEulaText.append(self.copyrightGenerator.createNewCopyright(owner, startYear, currentYear))
            copyrightEulaText.append("") # white space for readability
            copyrightEulaText.append(self.eula.formatEulaName())
            copyrightEulaText.append("") # white space for readability
            copyrightEulaText.extend(self.eula.formatEulaText())
            copyrightEulaText.append("") # white space for readability

        copyrightEulaText.append("This file was autogenerated by "+autotoolname+" do not edit")
        copyrightEulaText.append("") # white space for readability

        # Generate comment header
        for line in self.headerCommentGen.buildCommentBlockHeader():
            commentText.append(line+"\n")

        # Wrap and output commentText lines
        for line in copyrightEulaText:
            commentText.append(self.headerCommentGen.wrapCommentLine(line)+"\n")

        # Generate comment footer
        for line in self.headerCommentGen.buildCommentBlockFooter():
            commentText.append(line+"\n")
        return commentText

    def _genImport(self, className:str, moduleName:str = None)->str:
        """!
        @brief Add Include line to the output file
        @param className {string} Name of the class to import
        @param moduleName {string} Name of the module to import from
        @return string - Import statement
        """
        if moduleName is not None:
            return "import {"+className+"} from "+moduleName+";\n"
        else:
            return "import '"+className+"';\n"

    def _genImportBlock(self, includeNames:list)->list:
        """!
        @brief Generate a series if include line(s) for each name in the list
        @param includeNames {list of tuples} Name(s) of class(es), Module name(s) of the class to import
        @return list of strings - Import code block to output
        """
        includeBlock = ["// Imports\n"]
        for className, moduleName in includeNames:
            includeBlock.append(self._genImport(className, moduleName))
        return includeBlock

    def _genNamespaceOpen(self, namespaceName:str)->list:
        """!
        @brief Generate namespace start code for include file
        @param namespaceName {string} Name of the namespace
        @return list of strings - Code to output
        """
        return ["namespace "+namespaceName+" {\n"]

    def _genNamespaceClose(self, namespaceName:str)->list:
        """!
        @brief Generate namespace start code for include file
        @param namespaceName {string} Name of the namespace
        @return list of strings - Code to output
        """
        return ["} // end of namespace "+namespaceName+"\n"]

    def _genClassOpen(self, className:str, classDesc:str|None = None, inheritence:str|None = None,
                      classDecoration:str|None = None, indent:int=0)->list:
        """!
        @brief Generate the class open code

        @param className {string} Name of the class
        @param classDesc {string} Description of the class object
        @param inheritence {sting} Parent class and visability or None
        @param classDecoration {sting} Class decoration or None
        @param indent {integer} Space indentation for the declaration and comments

        @return list of strings - Code to output
        """
        codeText = []
        declIndent = "".rjust(indent, ' ')

        # Generate Doxygen class description
        if classDesc is not None:
            codeText.extend(self.doxyCommentGen.genDoxyClassComment(classDesc, blockIndent=indent))

        # Generate class start
        if classDecoration is not None:
            classLine = declIndent+classDecoration+" class "+className
        else:
            classLine = declIndent+"class "+className

        if inheritence is not None:
            classLine += " extends "
            classLine += inheritence

        codeText.append(classLine+"\n")
        codeText.append(declIndent+"{\n")

        return codeText

    def _genClassClose(self, className:str, indent:int=0)->list:
        """!
        @brief Generate the class close code

        @param className {string} Name of the class
        @param indent {integer} Space indentation for the declaration and comments

        @return list of strings - Code to output
        """
        return ["".rjust(indent, ' ')+"} // end of "+className+" class\n"]

    def _genClassDefaultConstructor(self, className:str, indent:int = 8, paramList:list=[],
                                   constructorCode:list= [], noDoxyCommentConstructor:bool = False)->list:
        """!
        @brief Generate default constructor(s)/destructor declarations for a class

        @param className {string} Name of the class
        @param indent {number} Indentation space count for the declarations (default = 8)
        @param paramList {list} List of parameter dictionaries
        @param constructorCode {list} Constructor code
        @param noDoxyCommentConstructor {boolean} Doxygen comment disable. False = generate doxygen comments,
                                                  True = ommit comments
        @return list of strings - Code to output
        """
        # Declare default default constructor
        codeText = self._declareFunctionWithDecorations("constructor",
                                                       "Construct a new "+className+" object",
                                                       paramList,
                                                       None,
                                                       indent,
                                                       noDoxyCommentConstructor,
                                                       "public",
                                                       None,
                                                       constructorCode)
        codeText.append("\n")      #whitespace for readability
        return codeText

    def _declareStructure(self, name:str, varDistList:list, indent:int=0,
                          structDesc:str|None = None,
                          prefixDecoration:str|None = None,
                          postfixDecoration:str|None = None)->list:
        """!
        @brief Generate a structure declaration

        @param name {string} Name of the structure
        @param varDistList {list} List of ParamRetDict parameter dictionaries for the data elements
        @param indent {integer} Number of spaces to indent the code declarations, default = 0
        @param structDesc {string|None} Doxygen structure description
        @param prefixDecoration {str} Structure definition prefix decorations unused in python
        @param postfixDecoration {str} Structure definition end decorations unused in python

        @return list of strings - Code to output
        """
        codeText = []
        declIndent = "".rjust(indent, ' ')
        bodyIndent = "".rjust(indent+self.levelTabSize, ' ')

        # Generate the doxygen comment
        codeText.extend(self.doxyCommentGen.genDoxyClassComment(structDesc, None, indent))

        # Generate the structure
        if prefixDecoration is not None:
            codeText.append(declIndent+prefixDecoration+" interface "+name+" {\n")
        else:
            codeText.append(declIndent+"interface "+name+" {\n")

        # Generate the body code
        for varDict in varDistList:
            codeText.append(bodyIndent+self._declareVarStatment(varDict, 60-self.levelTabSize))

        # Close the struture
        if postfixDecoration is not None:
            codeText.append(declIndent+"} "+postfixDecoration+"\n")
        else:
            codeText.append(declIndent+"}\n")
        return codeText

    def _declareVarStatment(self, varDict:dict, doxyCommentIndent:int = -1)->str:
        """!
        @brief Declare a class/interface variable
        @param varDict {dict} ParamRetDict parameter dictionary describing the variable
        @param doxyCommentIndent {int} Column to begin the doxygen comment
        @return string Variable declatation code
        """
        # Declare the variable
        typeName = ParamRetDict.getParamType(varDict)
        typeMod = ParamRetDict.getParamTypeMod(varDict)

        varTypeDecl = self._declareType(typeName, typeMod)
        varDecl = ParamRetDict.getParamName(varDict)+":"+varTypeDecl+";"

        # Test for doxycomment skip
        if doxyCommentIndent != -1:
            if doxyCommentIndent > len(varDecl):
                varDecl = varDecl.ljust(doxyCommentIndent, ' ')
            else:
                varDecl+= " "
            varDecl += self.doxyCommentGen.genDoxyVarDocStr(ParamRetDict.getParamDesc(varDict))

        # Return the final data
        return varDecl+"\n"

    def _genAddListStatment(self, listName:str, valueName:str, isText:bool=False)->str:
        """!
        @brief Generate a list add code statement
        @param listName {string} Name of the list variable to add the valueName to
        @param valueName {string} Name of the value to add to the list object
        @param isText {boolean} False if valueName is a variable name or numeric value,
                                True if valueName is a text string
                                default = False
        @return string - Typescript code text
        """
        if isText:
            return listName+".push(\""+valueName+"\");"
        else:
            return listName+".push("+valueName+");"

    def _genReturnStatment(self, retValue:str, isText:bool=False)->str:
        """!
        @brief Generate a list add code statement
        @param retValue {string} Name of the return variable
        @param isText {boolean} False if retValue is a variable name or numeric value,
                                True if retValue is a text string
                                default = False
        @return string - Typescript code text
        """
        if isText:
            return "return \""+retValue+"\";"
        else:
            return "return "+retValue+";"
