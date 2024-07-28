'''
 Class:        CS 4308 Section W01
 Term:         Summer 2024
 Name:         Kendal Elison
 Instructor:   Sharon Perry
 Project:      Deliverable P2 Parser
 '''

from Scanner import Scanner, Token, TokenType
from treelib import Node, Tree
from treelib import RenderTree

# Creates Parser Tree
class ParseTreeNode:

    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def __repr__(self):
        return f"{self.value} -> {self.children}"


class Parser:

    def __init__(self, scanner):
        self.scanner = scanner
        self.tokens = self.scanner.make_tokens()
        self.current_token_index = 0
        self.current_token = self.tokens[
            self.current_token_index] if self.current_token_index < len(
                self.tokens) else None
        self.errors = []
        self.parse_tree = ParseTreeNode("program")
        self.statement_count = 0  # Track the number of statements
        self.parse_program()

    # Handles error if incorrect Grammer
    def error(self, message):
        self.errors.append(
            f"Error: {message} at token {self.current_token.type if self.current_token else 'EOF' }"
        )
        raise Exception(message)

    #Takes in the current token the moves to next index
    def eat(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            self.current_token_index += 1
            self.current_token = self.tokens[
                self.current_token_index] if self.current_token_index < len(
                    self.tokens) else None
        else:
            self.error(f"Expected {token_type}")

    # Begining of grammer the start of the function
    def parse_program(self):
        self.eat(TokenType.FUNCTION)
        self.eat(TokenType.ID)
        self.eat(TokenType.PAREN_OPEN)
        self.eat(TokenType.PAREN_CLOSE)
        self.parse_block()
        self.eat(TokenType.END)
        print("program -> function id ( ) block end")

    def parse_block(self):
        if self.current_token:
            self.parse_statement()
            if self.current_token:
                print("block -> statement block")
                self.parse_block()
            else:
                print("block -> statement")
        else:
            print("block -> ")

    def parse_statement(self):
        if self.current_token.type == TokenType.IF:
            self.parse_if_statement()
            self.statement_count += 1
            print(f"statement -> if_statement")
        elif self.current_token.type == TokenType.WHILE:
            self.parse_while_statement()
            self.statement_count += 1
            print(f"statement -> while_statement")
        elif self.current_token.type == TokenType.PRINT:
            self.parse_print_statement()
            self.statement_count += 1
            print(f"statement -> print_statement")
        elif self.current_token.type == TokenType.ID:
            self.parse_assignment_statement()
            self.statement_count += 1
            print(f"statement -> assignment_statement")
        else:
            self.error("Invalid statement")

    def parse_if_statement(self):
        node = ParseTreeNode("if_statement")
        self.parse_tree.add_child(node)
        self.eat(TokenType.IF)
        node.add_child(self.parse_boolean_expression())
        self.eat(TokenType.THEN)
        node.add_child(self.parse_block())
        self.eat(TokenType.ELSE)
        node.add_child(self.parse_block())
        self.eat(TokenType.END)
        print(
            "if_statement -> if boolean_expression then block else block end")

    def parse_while_statement(self):
        node = ParseTreeNode("while_statement")
        self.parse_tree.add_child(node)
        self.eat(TokenType.WHILE)
        node.add_child(self.parse_boolean_expression())
        self.eat(TokenType.DO)
        node.add_child(self.parse_block())
        self.eat(TokenType.END)
        print("while_statement -> while boolean_expression do block end")

    def parse_assignment_statement(self):
        node = ParseTreeNode("assignment_statement")
        self.parse_tree.add_child(node)
        self.eat(TokenType.ID)
        self.eat(TokenType.ASSIGNMENT)
        node.add_child(self.parse_arithmetic_expression())
        print(
            "assignment_statement -> id assignment_operator arithmetic_expression"
        )

    def parse_print_statement(self):
        node = ParseTreeNode("print_statement")
        self.parse_tree.add_child(node)
        self.eat(TokenType.PRINT)
        self.eat(TokenType.PAREN_OPEN)
        node.add_child(self.parse_arithmetic_expression())
        self.eat(TokenType.PAREN_CLOSE)
        print("print_statement -> print ( arithmetic_expression )")

    def parse_boolean_expression(self):
        node = ParseTreeNode("boolean_expression")
        self.parse_tree.add_child(node)
        node.add_child(self.parse_relative_op())
        node.add_child(self.parse_arithmetic_expression())
        print("boolean_expression -> relative_op arithmetic_expression")
        return node

    # Dealing with relative operators
    def parse_relative_op(self):
        if self.current_token.type in {
                TokenType.LESSTHANEQUALTO, TokenType.LESSTHAN,
                TokenType.GREATEREQUALTO, TokenType.GREATERTHAN,
                TokenType.EQUAL, TokenType.NOTEQUAL
        }:
            node = ParseTreeNode(self.current_token.type)
            self.parse_tree.add_child(node)
            self.eat(self.current_token.type)
            return node
        else:
            self.error("Invalid relative operator")
            return None

    def parse_arithmetic_expression(self):
        node = ParseTreeNode("arithmetic_expression")
        self.parse_tree.add_child(node)
        if self.current_token.type in {TokenType.ID, TokenType.INT}:
            node.add_child(self.parse_eat_and_create_node(self.current_token.type))
            print("arithmetic_expression -> id | literal_integer")
        else:
            node.add_child(self.parse_arithmetic_op())
            node.add_child(self.parse_arithmetic_expression())
            node.add_child(self.parse_arithmetic_expression())
            print(
                "arithmetic_expression -> arithmetic_op arithmetic_expression arithmetic_expression"
            )
        return node

    def parse_arithmetic_op(self):
        if self.current_token.type in {
                TokenType.PLUS, TokenType.SUBTRACTION, TokenType.MULTIPLCATION,
                TokenType.DIVIDE
        }:
            node = ParseTreeNode(self.current_token.type)
            self.parse_tree.add_child(node)
            self.eat(self.current_token.type)
            return node
        else:
            self.error("Invalid arithmetic operator")
            return None
            
    # Adds token to parse tree
    def parse_eat_and_create_node(self, token_type):
        node = ParseTreeNode(token_type)
        self.parse_tree.add_child(node)
        self.eat(token_type)
        return node

def print_tree(parse_tree):
    for pre, fill, node in RenderTree(parse_tree):
        print("%s%s" % (pre, node.value))
