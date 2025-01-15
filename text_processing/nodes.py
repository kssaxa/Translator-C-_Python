from .lexer import Token
from typing import List


class ExpressionNode:
    """Базовый класс для всех узлов синтаксического дерева."""

    pass


class StatementNode(ExpressionNode):
    """Узел для последовательности операторов."""

    def __init__(self):
        super().__init__()
        self.statements:List = []

    def add_node(self, node: ExpressionNode):
        self.statements.append(node)


class ValueNode(ExpressionNode):
    """Узел для представления значения."""

    def __init__(self, value: Token):
        super().__init__()
        self.value = value


class BinOperatorNode(ExpressionNode):
    """Узел для бинарных операций."""

    def __init__(self, operator: Token, left: ExpressionNode, right: ExpressionNode):
        super().__init__()
        self.operator = operator
        self.left = left
        self.right = right


class UnarOperatorNode(ExpressionNode):
    """Узел для унарных операций."""

    def __init__(self, operator: Token, operand: ExpressionNode):
        super().__init__()
        self.operator = operator
        self.operand = operand


class BlockNode(ExpressionNode):
    """Узел для блоков (например, циклы или условные операторы)."""

    def __init__(self, keyword: Token):
        super().__init__()
        self.keyword = keyword
        self.condition = None  # поле для условия
        self.body = []
        self.else_branch = None  # Ветка else или else if

    def add_node(self, node: ExpressionNode):
        self.body.append(node)


class ElseNode(ExpressionNode):
    """Узел для блока else."""

    def __init__(self, keyword: Token):
        super().__init__()
        self.keyword = keyword
        self.body = []

    def add_node(self, node: ExpressionNode):
        self.body.append(node)


class ElseIfNode(ExpressionNode):
    """Узел для блока else if."""

    def __init__(self, keyword: Token, condition: ExpressionNode):
        super().__init__()
        self.keyword = keyword
        self.condition = condition
        self.body = []
        self.else_branch = None

    def add_node(self, node: ExpressionNode):
        self.body.append(node)


class FunctionNode(ExpressionNode):
    """Узел для объявления функции."""

    def __init__(self, return_type: Token, name_token: Token, parameters: list, body: ExpressionNode):
        super().__init__()
        self.return_type = return_type
        self.name_token = name_token
        self.parameters = parameters
        self.body = body


class ReturnNode(ExpressionNode):
    """Узел для ключевого слова return."""

    def __init__(self, keyword: Token):
        super().__init__()
        self.keyword = keyword


class VariableDeclarationNode(ExpressionNode):
    """Узел для объявления переменной."""

    def __init__(self, var_type: Token, var_name: Token, value: ExpressionNode = None):
        super().__init__()
        self.var_type = var_type
        self.var_name = var_name
        self.value = value


class VariableUsageNode(ExpressionNode):
    """Узел для использования переменной."""

    def __init__(self, var_name: Token):
        super().__init__()
        self.var_name = var_name

    def __repr__(self):
        return f"VariableUsageNode(var_name={self.var_name.value})"


class FuncNode:
    """Узел для функций ввода/вывода."""

    def __init__(self, func_token: Token, arguments: list):
        self.func_token = func_token  # Токен функции (например, cin)
        self.arguments = arguments  # Список аргументов функции
        self.operator = None

    def add_argument(self, argument):
        self.arguments.append(argument)


class UseFuncNode(ExpressionNode):
    """Узел для вызова функции."""

    def __init__(self, func_token: Token, arguments: list):
        super().__init__()
        self.name_variable = None
        self.return_type = None
        self.func_token = func_token
        self.arguments = arguments

class ForNode:
    """Вспомогательный узел для блока (для хранения condition для for)"""
    def __init__(self, init, condition, increment):
        self.init = init
        self.condition = condition
        self.increment = increment


class StreamManipulatorNode:
    """Для std::endl"""
    def __init__(self, token):
        self.token = token
