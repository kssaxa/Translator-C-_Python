from .lexer import *
from .nodes import *
from .gen import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def parse(self):
        return self.parse_statements()

    # Создает узел StatementNode и добавляет в него операторы последовательно (до конца программы)
    def parse_statements(self):
        statement_node = StatementNode()
        while self.current_token_index < len(self.tokens):
            if self.current_token().type == 'NEWLINE':
                self.consume('NEWLINE')
            else:
                statement_node.add_node(self.parse_statement())
        return statement_node

    # Определяет тип оператора и вызывает соответствующий метод
    def parse_statement(self):
        current_token = self.current_token()
        if current_token.type == 'KEYWORD' and current_token.value in ('int', 'float', 'bool', 'void'):
            return self.parse_type_keyword()
        elif current_token.type == 'BLOCK':
            if current_token.value in ('if', 'while', 'for'):
                return self.parse_block()
            elif current_token.value == 'else':
                return self.parse_else()
            elif current_token.value == 'do':
                return self.parse_do_while()
            else:
                self.error(f"Unexpected keyword in block {current_token.value}")
        elif current_token.type == 'KEYWORD' and current_token.value == 'return':
            return self.parse_return_statement()
        elif current_token.type == 'IDENTIFIER':
            p_node = self.parse_expression()
            self.consume('SEPARATOR', ';')
            return p_node
        elif current_token.type == 'FUNC':
            return self.parse_func_statement()
        elif current_token.type == 'PREPROCESSOR':
            self.consume('PREPROCESSOR')
            self.consume('OPERATOR')
            self.consume('IDENTIFIER')
            self.consume('OPERATOR')
        elif current_token.type == 'KEYWORD' and current_token.value == 'const':
            self.consume('KEYWORD', 'const')
            is_const = True
            return self.parse_type_keyword(is_const)
        else:
            self.error(f"Unexpected token {current_token.type}")


    # Создает узел StatementNode и добавляет в него операторы последовательно
    # (Для функции, иначе в тело функции будет занесено всё до конца программы)
    def parse_statements_for_function(self):
        statement_node = StatementNode()
        while self.current_token().type != 'SEPARATOR' and self.current_token().value != '}':
            if self.current_token().type == 'NEWLINE':
                self.consume('NEWLINE')
            else:
                statement_node.add_node(self.parse_statement())
        return statement_node

    # Разделение keyword на переменную и функции
    def parse_type_keyword(self, is_const = False):
        type_token = self.consume('KEYWORD')
        next_token = self.current_token()

        if next_token.type == 'IDENTIFIER':
            name_token = self.consume('IDENTIFIER')
            declarations = []
            if self.current_token().type == 'SEPARATOR' and self.current_token().value == '(':
                return self.parse_function(type_token, name_token)
            elif self.current_token().type == 'OPERATOR' and self.current_token().value == '=':
                self.consume('OPERATOR', '=')
                value_expr = self.parse_expression()
                value_expr.return_type = type_token
                value_expr.name_variable = name_token
                declarations.append(VariableDeclarationNode(type_token, name_token, value_expr, is_const))
            elif self.current_token().type == 'SEPARATOR' and self.current_token().value == ';':
                declarations.append(VariableDeclarationNode(type_token, name_token, None, is_const))
            elif self.current_token().type == 'SEPARATOR' and self.current_token().value == '[':
                self.consume('SEPARATOR', '[')
                size_token = self.consume('NUMBER')
                self.consume('SEPARATOR', ']')
                if self.current_token().type == 'OPERATOR' and self.current_token().value == '=':
                    self.consume('OPERATOR', '=')
                    self.consume('SEPARATOR', '{')
                    elements = []
                    while self.current_token().type != 'SEPARATOR' or self.current_token().value != '}':
                        elements.append(self.parse_expression())
                        if self.current_token().type == 'SEPARATOR' and self.current_token().value == ',':
                            self.consume('SEPARATOR', ',')
                    self.consume('SEPARATOR', '}')
                    self.consume('SEPARATOR', ';')
                    return ArrayDeclarationNode(type_token, name_token, size_token, elements)
                else:
                    self.consume('SEPARATOR', ';')
                    return ArrayDeclarationNode(type_token, name_token, size_token, None)

            else:
                self.error("Unexpected token after variable name")

            while self.current_token().type == 'SEPARATOR' and self.current_token().value == ',':
                self.consume('SEPARATOR', ',')
                name_token = self.consume('IDENTIFIER')
                if self.current_token().type == 'OPERATOR' and self.current_token().value == '=':
                    self.consume('OPERATOR', '=')
                    value_expr = self.parse_expression()
                    value_expr.return_type = type_token
                    value_expr.name_variable = name_token
                    declarations.append(VariableDeclarationNode(type_token, name_token, value_expr))
                else:
                    declarations.append(VariableDeclarationNode(type_token, name_token, None))

            self.consume('SEPARATOR', ';')

            if len(declarations) == 1:
                return declarations[0]
            return declarations
        else:
            self.error("Expected identifier after type keyword")

    # Парсер функции
    def parse_function(self, return_type_token, name_token):
        self.consume('SEPARATOR', '(')
        parameters = self.parse_parameters()
        self.consume('SEPARATOR', ')')

        self.consume('SEPARATOR', '{')
        body = self.parse_statements_for_function()  # Тело функции (последовательность операторов)
        self.consume('SEPARATOR', '}')

        return FunctionNode(return_type_token,name_token, parameters, body)

    #Для параметров функции
    def parse_parameters(self):
        params = []
        while self.current_token().type != 'SEPARATOR' or self.current_token().value != ')':
            if self.current_token().type == 'KEYWORD' and self.current_token().value in ('int', 'float', 'bool'):
                param_type = self.consume('KEYWORD')
                param_name = self.consume('IDENTIFIER')
                params.append(VariableDeclarationNode(param_type, param_name))
                if self.current_token().type == 'SEPARATOR' and self.current_token().value == ',':
                    self.consume('SEPARATOR', ',')
            else:
                self.error(f"Unexpected token {self.current_token().type} in parameters")
        return params

    #RETURN
    def parse_return_statement(self):
            self.consume('KEYWORD', 'return')
            return_expr = self.parse_expression()
            self.consume('SEPARATOR', ';')
            return ReturnNode(return_expr)

    def parse_do_while(self):
        self.consume('BLOCK', 'do')
        self.consume('SEPARATOR', '{')
        body = []
        while not (self.current_token().type == 'SEPARATOR' and self.current_token().value == '}'):
            if self.current_token().type == 'NEWLINE':
                self.consume('NEWLINE')
            else:
                body.append(self.parse_statement())
        self.consume('SEPARATOR', '}')
        self.consume('BLOCK', 'while')
        self.consume('SEPARATOR', '(')
        condition = self.parse_expression()
        self.consume('SEPARATOR', ')')
        self.consume('SEPARATOR', ';')

        return DoWhileNode(body, condition)

    #Тело блоков if, else, while, for
    def parse_block(self):
        keyword = self.consume('BLOCK')
        keyword_value = keyword.value
        block_node = BlockNode(keyword)

        # Обработка условия в скобках
        self.consume('SEPARATOR', '(')
        condition = self.parse_expression(keyword=keyword_value)
        self.consume('SEPARATOR', ')')
        block_node.condition = condition

        self.consume('SEPARATOR', '{')
        while self.current_token().type != 'SEPARATOR' or self.current_token().value != '}':
            if self.current_token().type == 'NEWLINE':
                self.consume('NEWLINE')
            else:
                block_node.add_node(self.parse_statement())
        self.consume('SEPARATOR', '}')

        # Проверка на наличие else или else if
        if self.current_token().type == 'BLOCK' and self.current_token().value == 'else':
            self.consume('BLOCK', 'else')
            if self.current_token().type == 'BLOCK' and self.current_token().value == 'if':
                else_if = self.parse_else_if(block_node)
                block_node.else_branch = else_if
            elif self.current_token().type == 'SEPARATOR' and self.current_token().value == '{':
                block_node.else_branch = self.parse_else()

        condition.body = block_node.body
        return block_node

    # Обработка else if
    def parse_else_if(self, parent_block):
        keyword = self.consume('BLOCK', 'if')
        self.consume('SEPARATOR', '(')
        condition = self.parse_expression()
        self.consume('SEPARATOR', ')')

        else_if_node = ElseIfNode(keyword, condition)
        self.consume('SEPARATOR', '{')
        while self.current_token().type != 'SEPARATOR' or self.current_token().value != '}':
            if self.current_token().type == 'NEWLINE':
                self.consume('NEWLINE')
            else:
                else_if_node.add_node(self.parse_statement())
        self.consume('SEPARATOR', '}')

        if self.current_token().type == 'BLOCK' and self.current_token().value == 'else':
            self.consume('BLOCK', 'else')
            if self.current_token().type == 'BLOCK' and self.current_token().value == 'if':
                else_if_node.else_branch = self.parse_else_if(parent_block)
            elif self.current_token().type == 'SEPARATOR' and self.current_token().value == '{':
                else_if_node.else_branch = self.parse_else()

        return else_if_node

    # else
    def parse_else(self):
        else_node = ElseNode(self)

        self.consume('SEPARATOR', '{')
        while self.current_token().type != 'SEPARATOR' or self.current_token().value != '}':
            if self.current_token().type == 'NEWLINE':
                self.consume('NEWLINE')
            else:
                else_node.add_node(self.parse_statement())
        self.consume('SEPARATOR', '}')
        return else_node

    # Разветвление cin, cout и тд
    def parse_func_statement(self):
        func_token = self.consume('FUNC')

        if func_token.value in ('std::cin', 'std::cout', 'std::printf', 'std::scanf', 'std::getline'):
            if func_token.value in ('std::cin', 'std::cout'):
                return self.parse_cin_cout(func_token)
            elif func_token.value in ('std::printf', 'std::scanf', 'std::getline'):
                return self.parse_standard_func(func_token)


    def parse_cin_cout(self, func_token):
        # Ожидаем оператор << или >>
        output_node = FuncNode(func_token, [])

        while True:
            if self.current_token().type == 'OPERATOR' and self.current_token().value in ('<<', '>>'):
                self.consume('OPERATOR')
                if self.current_token().type in ('IDENTIFIER', 'NUMBER', 'STRING', 'NEWLINE'):
                    argument = self.parse_expression()
                    output_node.add_argument(argument)
                else:
                    self.error("Expected argument after operator")
            else:
                break

        self.consume('SEPARATOR', ';')
        return output_node

    #printf, getline и тд
    def parse_standard_func(self, func_token):
        arguments = []
        self.consume('SEPARATOR', '(')

        while self.current_token().type != 'SEPARATOR' or self.current_token().value != ')':
            if self.current_token().type == 'NEWLINE':
                    self.consume('NEWLINE')
            elif self.current_token().type in ('IDENTIFIER', 'NUMBER', 'STRING'):
                argument_node = self.parse_expression()
                arguments.append(argument_node)
                if self.current_token().type == 'SEPARATOR' and self.current_token().value == ',':
                    self.consume('SEPARATOR', ',')
            else:
                self.error(f"Unexpected token {self.current_token().type} in function arguments")

        self.consume('SEPARATOR', ')')
        self.consume('SEPARATOR', ';')
        return FuncNode(func_token, arguments)

    # Для выражений
    def parse_expression(self, precedence = 0, keyword = None):
        if keyword == 'for':
            init = self.parse_statement()

            condition = self.parse_expression()
            self.consume('SEPARATOR', ';')

            increment = self.parse_expression()
            return ForNode(init, condition, increment)
        else:
            left = self.parse_primary()
            if self.current_token().type == 'OPERATOR' and self.current_token().value in ('++','--'):
                operator = self.consume('OPERATOR')
                left = UnarOperatorNode(operator, left)
            else:
                while self.current_token().type == 'OPERATOR' and self.current_token().value not in ('<<', '>>') and self.get_precedence(self.current_token().value) >= precedence:
                    operator = self.consume('OPERATOR')
                    right = self.parse_expression(self.get_precedence(operator.value) + 1)  # увеличиваем приоритет для правой части
                    left = BinOperatorNode(operator, left, right)
            return left


    # Числа, идентификаторы, строки и тд
    def parse_primary(self):
        current_token = self.current_token()
        if current_token.type == 'NUMBER':
            return ValueNode(self.consume(current_token.type))
        elif current_token.type == 'IDENTIFIER':
            # Если идентификатор, проверяем, является ли это вызовом функции
            func_name = self.consume('IDENTIFIER')
            if self.current_token().type == 'SEPARATOR' and self.current_token().value == '(':
                self.consume('SEPARATOR', '(')
                arguments = []
                while self.current_token().type != 'SEPARATOR' or self.current_token().value != ')':
                    arguments.append(self.parse_expression())
                    if self.current_token().value == ',':
                        self.consume('SEPARATOR', ',')
                self.consume('SEPARATOR', ')')
                return UseFuncNode(func_name, arguments)
            elif self.current_token().type == 'SEPARATOR' and self.current_token().value == '[':
                self.consume('SEPARATOR', '[')
                index_expression = self.parse_expression()
                self.consume('SEPARATOR', ']')
                return ArrayAccessNode(func_name, index_expression)
            else:
                return VariableUsageNode(func_name)
        elif current_token.type == 'BOOL':
            return ValueNode(self.consume('BOOL'))
        elif current_token.type == 'SEPARATOR' and current_token.value == '(':
            self.consume('SEPARATOR', '(')
            expr = self.parse_expression()
            self.consume('SEPARATOR', ')')
            return expr
        elif current_token.type == 'STRING':
            return ValueNode(self.consume('STRING'))
        elif current_token.type == ('NEWLINE') and self.current_token().value in ('std::endl','\n'):
            newline_token = self.consume('NEWLINE')
            return StreamManipulatorNode(newline_token)
        else:
            self.error(f"Unexpected token {current_token.type}")

    # Приоритет операций (больше значение, выше приоритет)
    def get_precedence(self, operator: str) -> int:
        precedence = {
            '=': 1,      # Присваивание
            '==': 2,     # Сравнение
            '!=': 2,
            '<': 2,
            '>': 2,
            '<=': 2,
            '>=': 2,
            '+': 3,      # Арифметические операторы
            '-': 3,
            '*': 4,
            '/': 4,
            '%': 4
        }
        return precedence.get(operator, 0)  # если оператор не найден - 0


    def current_token(self):
        return self.tokens[self.current_token_index]

    # Проверяет и возвращает текущий токен, а затем переходит к следующему
    def consume(self, expected_type, expected_value=None):
        token = self.current_token()
        if token.type == expected_type and (expected_value is None or token.value == expected_value):
            self.current_token_index += 1
            return token
        else:
            self.error(f"Expected {expected_type} but got {token.type}")

    def error(self, message):
        raise SyntaxError(message)



def Sintaxize(tokens):
    parser_error = None
    ast_error = None
    gener_error = None

    parser = None
    ast = None
    gener = None


    try:
        parser = Parser(tokens)
    except Exception as e:
        parser_error = str(e)


    try:
        ast = parser.parse()
    except Exception as e:
        ast_error = str(e)

    gener_error = None

    try:
        gener = CodeGenerator()
        with open("test.py", "w") as file:
            file.write(gener.genPython(ast))
    except Exception as e:
        gener_error = str(e)





    def print_ast(node, level=0):
        indent = "  " * level
        result = []

        if isinstance(node, ValueNode):
            result.append(f"{indent}Value: {node.value.value}")
        elif isinstance(node, BinOperatorNode):
            result.append(f"{indent}Binary Operator: {node.operator.value}")
            result.extend(print_ast(node.left, level + 1))
            result.extend(print_ast(node.right, level + 1))
        elif isinstance(node, UnarOperatorNode):
            result.append(f"{indent}Unary Operator: {node.operator.value}")
            result.extend(print_ast(node.operand, level + 1))
        elif isinstance(node, BlockNode):
            result.append(f"{indent}Block: {node.keyword.value}")
            result.append(f"{indent}Condition:")
            result.extend(print_ast(node.condition, level + 1))
            result.append(f"{indent}Body:")
            for stmt in node.body:
                result.extend(print_ast(stmt, level + 1))
            if node.else_branch:
                result.append(f"{indent}Else:")
                result.extend(print_ast(node.else_branch, level + 1))
        elif isinstance(node, ElseNode):
            result.append(f"{indent}Else Block:")
            for stmt in node.body:
                result.extend(print_ast(stmt, level + 1))
        elif isinstance(node, ElseIfNode):
            result.append(f"{indent}Else If:")
            result.extend(print_ast(node.condition, level + 1))
            result.append(f"{indent}Body:")
            for stmt in node.body:
                result.extend(print_ast(stmt, level + 1))
            if node.else_branch:
                result.append(f"{indent}Else:")
                result.extend(print_ast(node.else_branch, level + 1))
        elif isinstance(node, StatementNode):
            result.append(f"{indent}Statements:")
            for stmt in node.statements:
                result.extend(print_ast(stmt, level + 1))
        elif isinstance(node, FunctionNode):
            result.append(f"{indent}Function: {node.return_type.value} {node.name_token.value}")
            result.append(f"{indent}Parameters:")
            for param in node.parameters:
                result.append(f"{indent}  {param.var_type.value} {param.var_name.value}")
            result.append(f"{indent}Body:")
            result.extend(print_ast(node.body, level + 1))
        elif isinstance(node, ReturnNode):
            result.append(f"{indent}Return:")
            result.extend(print_ast(node.keyword, level + 1))
        elif isinstance(node, VariableDeclarationNode):
            result.append(f"{indent}Variable Declaration: {node.var_type.value} {node.var_name.value}")
            if node.value:
                result.append(f"{indent}  Assigned value:")
                result.extend(print_ast(node.value, level + 1))
        elif isinstance(node, FuncNode):
            result.append(f"{indent}Function Call: {node.func_token.value}")
            for arg in node.arguments:
                result.append(f"{indent}  Argument:")
                result.extend(print_ast(arg, level + 1))
        else:
            result.append(f"{indent}Unknown node type: {type(node)}")

        return result

    return "\n".join(print_ast(ast)), ast, gener.output, parser_error, ast_error, gener_error


