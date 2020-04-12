import re
import sys
from tokenn import Token


class LexicalAnalyzer:

    def __init__(self):
        self.tokens = []
        self.table = {'!=': 'NOT_EQUAL', '==': 'EQUAL', '>=': 'GREAT_EQ', '<=': 'LESS_EQ',
                      '<': 'LESSTHAN', '>': 'GREATERTHAN', '%': 'MOD', '#': 'PREPROCESSOR',
                      '!': 'NOT', '.': 'DOT', ';': 'SEMICOLON', ',': 'COMMA', '(': 'RIGHT_ROUND_B',
                      ')': 'LEFT_ROUND_B', '[': 'RIGHT_SQUARE_B', ']': 'LEFT_SQUARE_B',
                      '{': 'RIGHT_CURLY_B', '}': 'LEFT_CURLY_B'}
        self.reserved = ['while', 'volatile', 'void', 'union', 'typedef', 'switch', 'struct', 'static', 'sizeof',
                         'return',
                         'register', 'if', 'goto', 'extern', 'enum', 'else', 'do', 'default', 'continue', 'const',
                         'case',
                         'break', 'false', 'true', 'new', 'auto']
        self.types = ["int", "float", "bool", "short", "double", "signed", "unsigned", "char", "long"]
        self.floatLiteralsRegex = r'[+-]?[0-9]+\.[0-9]+'
        self.intLiteralsRegex = r'(?<![\w.])[+-]?[0-9]+?(?![\w.])|(?<![\w.])[0-9]+[e]?[0-9]+?(?![\w.])'
        self.identifiersRegex = r'[a-zA-Z_]\w*'
        self.stringLiteralRegex = r'\".*\"'
        self.singleCommentRegex = r'//.*?[\n\r]'
        self.multiCommentRegex = r"/\*(.|[\r\n])*?\*/"
        self.equalOrRegex = r'(!=|==|\>\=|<=|<|>|%|#|!|\.|;|,|\(|\)|\[|\]|{|})'
        self.charRegex = r'\s[a-zA-Z]\s|\s[a-zA-Z]\='
        # self.assignmentOpRegex = r'(\w|\s)(\=)(\w|\s)'
        self.assignmentOpRegex = r'='

    # Private Methods
    def _postfix(self, word):
        reserved_postfix = r"\s?\b"
        return word + reserved_postfix + '|'

    def _createRegEx(self, words):
        s = '('
        for word in words:
            s = s + self._postfix(word)
        return s[0:len(s) - 1] + ')'

    def _tokenizeReserved(self, values):
        for value in values:
            self.tokens.append(Token(value.upper(), value))

    def _tokenize(self, values, tokenType):
        for value in values:
            self.tokens.append(Token(tokenType, value))

    def _removeFromSourceCode(self, values, sourceCode):
        for value in values:
            sourceCode = sourceCode.replace(value, '')
        return sourceCode

    def _tokenizeAndRmvFromSrcCode(self, values, tokenType, sourceCode):
        self._tokenize(values, tokenType)
        return self._removeFromSourceCode(values, sourceCode)

    # End of private methods

    def floatLiterals(self, line):
        floats = re.findall(self.floatLiteralsRegex, line)  # match float literal
        line = self._tokenizeAndRmvFromSrcCode(floats, 'FLOAT_LITERAL', line)
        return line

    def intLiterals(self, line):
        integers = re.findall(self.intLiteralsRegex,
                              line)  # match int literal #match int literal
        line = self._tokenizeAndRmvFromSrcCode(integers, 'INTEGRAL_LITERAL', line)
        return line

    def identifier(self, line):
        return re.findall(self.identifiersRegex, line)

    def stringLiteral(self, line):
        strings = re.findall(self.stringLiteralRegex, line)
        line = self._tokenizeAndRmvFromSrcCode(strings, 'STRING_LITERAL', line)
        return line

    def reservedWords(self, s):
        regex = self._createRegEx(self.reserved)
        values = re.findall(regex, s)
        self._tokenizeReserved(values)
        s = self._removeFromSourceCode(values, s)
        return s

    def dataTypes(self, s):
        regex = self._createRegEx(self.types)
        values = re.findall(regex, s)
        self._tokenizeReserved(values)
        s = self._removeFromSourceCode(values, s)
        return s

    def singleComment(self, s):
        singleComments = re.findall(self.singleCommentRegex, s)
        singleComments = [comment.replace('\n', '') for comment in singleComments]
        s = self._tokenizeAndRmvFromSrcCode(singleComments, 'SINGLE_COMMENT', s)
        return s

    def multiComment(self, s):
        return re.findall(self.multiCommentRegex, s)

    def bitwiseNot(self, s):
        return re.findall(r'~', s)

    def operators(self, s):  # << >>
        return re.findall(r'(<<|>>)', s)

    def andOperator(self, s):
        return re.findall(r'&', s)

    def bitwiseXor(self, s):
        return re.findall(r'\^', s)

    def bitwiseOr(self, s):
        return re.findall(r'[^\|]\|[^\|]', s)

    def OR(self, s):
        return re.findall(r'\|\|', s)

    def AND(self, s):
        return re.findall('&&', s)

    def equalOr(self, s):
        values = re.findall(self.equalOrRegex, s)
        for value in values:
            tokenType = self.table[value]
            self.tokens.append(Token(tokenType, value))
        s = self._removeFromSourceCode(values, s)
        return s

    def backSlash(self, s):
        return re.findall(r'[\\]', s)

    def assignmentOperator(self, s):
        equalSigns = re.findall(self.assignmentOpRegex, s)
        s = self._tokenizeAndRmvFromSrcCode(equalSigns, 'ASSIGN_OPERATOR', s)
        return s

    def char(self, s):
        return re.findall(self.charRegex, s)

    def main(self, sourceCode):
        # Pipeline
        sourceCode = self.singleComment(sourceCode)
        sourceCode = self.reservedWords(sourceCode)
        sourceCode = self.dataTypes(sourceCode)
        sourceCode = self.floatLiterals(sourceCode)
        sourceCode = self.equalOr(sourceCode)
        sourceCode = self.intLiterals(sourceCode)
        sourceCode = self.stringLiteral(sourceCode)
        sourceCode = self.assignmentOperator(sourceCode)
        return sourceCode

    def printTokens(self):
        for token in self.tokens:
            print('<' + token.type + ', ' + token.value + '>')

    def report(self, line_num, where, message):
        print("[line " + "] Error" + where + ": " + message)
        sys.exit(0)

    def error(self, line_num, message):
        self.report(line_num, "", message)
