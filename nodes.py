from lexer import Token


class ExpressionNode:
    """Базовый класс для всех узлов синтаксического дерева."""

    pass


class StatementNode(ExpressionNode):
    """Узел для последовательности операторов."""

    def __init__(self):
        super().__init__()
        self.statements = []

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

    def add_node(self, node: ExpressionNode):
        self.body.append(node)


class FunctionNode(ExpressionNode):
    """Узел для функции."""
    
    def __init__(self, return_type: Token, name_token: str, parameters: list, body: ExpressionNode):
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


class FuncNode:
    """Узел для функций ввода/вывода."""

    def __init__(self, func_token, arguments):
        self.func_token = func_token  # Токен функции (например, cin)
        self.arguments = arguments  # Список аргументов функции
        self.operator = None

    def add_argument(self, argument):
        self.arguments.append(argument)
