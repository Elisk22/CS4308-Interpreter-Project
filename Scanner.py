'''
 Class:        CS 4308 Section W01
 Term:         Summer 2024
 Name:         Kendal Elison
 Instructor:   Sharon Perry
 Project:      Deliverable P1 Scanner
 '''


# Token class to initalize tokens
class Token:

    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.checked = False

    def __str__(self):
        return f'Token({self.type}, {self.value})'


# List of the diffrent types of tokens
class TokenType:

    INT = 'LITERAL_INT'
    IF = 'IF'
    ELSE = 'ELSE'
    PRINT = 'PRINT'
    END = 'END'
    THEN = 'THEN'
    DO = 'DO'
    WHILE = 'WHILE'
    FUNCTION = 'FUNCTION'
    KEYWORD = 'KEYWORD'
    ID = 'ID'
    EQUAL = 'EQUAL'
    ASSIGNMENT = 'ASSIGNMENT_OPERATOR'
    LESSTHAN = 'LT_OPERATOR'
    GREATERTHAN = 'GT_OPERATOR'
    GREATEREQUALTO = 'GE_OPERATOR'
    LESSTHANEQUALTO = 'LE_OPERATOR'
    PAREN_OPEN = 'PAREN_OPEN'
    PAREN_CLOSE = 'PAREN_CLOSE'
    SEMICOLON = 'SEMICOLON'
    NOTEQUAL = 'NE_OPERATOR'
    PLUS = 'ADD_OPERATOR'
    SUBTRACTION = 'SUB_OPERATOR'
    MULTIPLCATION = 'MUL_OPERATOR'
    DIVIDE = 'DIV_OPERATOR'


class Scanner:
    # Initalizes starting character
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.pos < len(
            self.text) else None
        self.keywords = {
            'if': 'IF',
            'else': 'ELSE',
            'end': 'END',
            'function': 'FUNCTION',
            'print': 'PRINT',
            'then': 'THEN',
            'while': 'WHILE',
            'do': 'DO'
        }

    # Moves index to next char
    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(
            self.text) else None

    # Peek function take a look at the next char without advancing the pointer
    def peek(self):
        peek_pos = self.pos + 1
        return self.text[peek_pos] if peek_pos < len(self.text) else None

    # Checks if current char is a certain token.
    def make_tokens(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
            elif self.current_char.isalpha():
                tokens.append(self.make_identifier_or_keyword())
            elif self.current_char.isdigit():
                tokens.append(self.make_number())
            elif self.current_char == '=':
                tokens.append(Token(TokenType.ASSIGNMENT, '='))
                self.advance()
            elif self.current_char == '<':
                tokens.append(Token(TokenType.LESSTHAN, '<'))
                self.advance()
            elif self.current_char == '>':
                tokens.append(Token(TokenType.GREATERTHAN, '>'))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TokenType.PAREN_OPEN, '('))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TokenType.PAREN_CLOSE, ')'))
                self.advance()
            elif self.current_char == ';':
                tokens.append(Token(TokenType.SEMICOLON, ';'))
                self.advance()
            elif self.current_char == "~":
                tokens.append(Token(TokenType.NOTEQUAL, "~"))
                self.advance()
            elif self.current_char == "+":
                tokens.append(Token(TokenType.PLUS, "+"))
                self.advance()
            elif self.current_char == "-":
                tokens.append(Token(TokenType.SUBTRACTION, "-"))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(TokenType.MULTIPLCATION, "*"))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(TokenType.DIVIDE, "/"))
                self.advance()
            else:
                print(f'Illegal character: {self.current_char}')
                self.advance()
        return tokens

    # Checks if current char IS keyword if not then assigned ID
    def make_identifier_or_keyword(self):
        id_str = ''
        while self.current_char is not None and (self.current_char.isalnum()
                                                 or self.current_char == '_'):
            id_str += self.current_char
            self.advance()
        if id_str in self.keywords:
            token_type = getattr(TokenType, self.keywords[id_str])
            # Specific TokenType constant--- not just show Keyword
            return Token(token_type, id_str)
        else:
            return Token(TokenType.ID, id_str)

    # MAKES AN INT
    def make_number(self):
        num_str = ''
        while self.current_char is not None and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()
        return Token(TokenType.INT, int(num_str))

    # Still not entirly complete but its supoes to take a peek at next postion
    # Then if next postion is some character that makes == or ~= and so on it assigns the right token.
    def make_relational_operator(self):
        op_str = self.current_char
        self.advance()
        if self.current_char == '=':
            op_str += self.current_char
            self.advance()
        return Token(TokenType.EQUAL, op_str)
