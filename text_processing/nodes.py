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
        self.body = []

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
