from .lexer import Token
from .nodes import *
from .sintaxer import *


class SemanticAnalyzer:
    def __init__(self) -> None:
        self.variables = {}  # Хранение переменных с их типами
        self.functions = {}  # Хранение функций с их параметрами и возвращаемыми типами
        self.current_scope = []  # Стек областей видимости

    def enter_scope(self):
        """Войти в новую область видимости."""
        self.current_scope.append(set())

    def leave_scope(self):
        """Выйти из текущей области видимости."""
        self.current_scope.pop()

    def declare_variable(self, name: str, var_type: str):
        """Объявление переменной в текущей области видимости."""
        if name in self.variables:
            raise NameError(f'Переменная {name!r} уже объявлена')
        last_scope = self.current_scope[-1] if self.current_scope else None
        if last_scope is not None:
            last_scope.add(name)

        self.variables[name] = var_type

    def check_variable(self, name: str):
        """Проверить использование переменной."""
        if name not in self.variables:
            raise NameError(f'Переменная {name!r} не определена')

    def declare_function(self, name: str, return_type: str, parameters: list):
        """Объявление функции."""
        if name in self.functions:
            raise NameError(f'Функция {name!r} уже объявлена')
        for param in parameters:
            self.declare_variable(param[1], param[0])
        self.functions[name] = {
            "return_type": return_type,
            "parameters": parameters,
        }

    def check_function(self, name: str, arguments: list):
        """Проверить вызов функции."""
        func = None
        for token, details in self.functions.items():
            if token.value == name:
                func = details
                break

        if func is None:
            raise NameError(f'Функция {name!r} не определена')
        if len(arguments) != len(func["parameters"]):
            raise TypeError(f'Ожидалось {len(func["parameters"])} аргументов, передано {len(arguments)}')

    def checkNode(self, node: ExpressionNode) -> None:
        """Проверка узлов."""
        if isinstance(node, VariableDeclarationNode):
            self.declare_variable(node.var_name.value, node.var_type.value)

        elif isinstance(node, ValueNode):
            pass

        elif isinstance(node, VariableUsageNode):
            if (node.var_name.value in ('break','continue')):
                pass
            else:
                self.check_variable(node.var_name.value)

        elif isinstance(node, FunctionNode):  # Функция (объявление)
            self.declare_function(
                node.name_token,
                node.return_type.value,
                [(param.var_type.value, param.var_name.value) for param in node.parameters]
            )
            self.enter_scope()
            # Проверяем, является ли тело функции одиночным StatementNode или списком
            if isinstance(node.body, StatementNode):
                for statement in node.body.statements:  # Проходим по операторам внутри StatementNode
                    if isinstance(statement, list):
                        for substatement in statement:
                            self.checkNode(substatement)
                    else:
                        self.checkNode(statement)
            else:
                self.checkNode(node.body)  # Если body не StatementNode, просто проверяем его
            self.leave_scope()

        elif isinstance(node, UseFuncNode):  # Вызовы функции
            self.check_function(
                node.func_token.value,
                [arg for arg in node.arguments]
            )
            for arg in node.arguments:
                self.checkNode(arg)

        elif isinstance(node, BinOperatorNode):
            self.checkNode(node.left)
            self.checkNode(node.right)

        elif isinstance(node, UnarOperatorNode):
            self.checkNode(node.operand)

        elif isinstance(node, BlockNode):
            self.enter_scope()
            for subnode in node.body:
                self.checkNode(subnode)
            self.leave_scope()

    def check(self, root: StatementNode) -> None:
        """Запуск проверки для корневого узла."""
        if isinstance(root, StatementNode):
            for node in root.statements:  # Теперь проверяем, что root является StatementNode
                self.checkNode(node)

# Пример
def Semanalize(ast):


    analyzer = SemanticAnalyzer()

    try:
        analyzer.check(ast)
        print("Семантический анализ прошел успешно!")
        # return analyzer
        return 1
    except Exception as e:
        print(f"Семантическая ошибка: {e}")
        return 0
