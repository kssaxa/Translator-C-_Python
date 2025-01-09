from lexer import Token
from nodes import *
from sintaxer import *

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
        self.variables[name] = var_type
        self.current_scope[-1].add(name)

    def check_variable(self, name: str):
        """Проверить использование переменной."""
        if name not in self.variables:
            raise NameError(f'Переменная {name!r} не определена')

    def declare_function(self, name: str, return_type: str, parameters: list):
        """Объявление функции."""
        if name in self.functions:
            raise NameError(f'Функция {name!r} уже объявлена')
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
            self.check_variable(node.var_name.value)    

        elif isinstance(node, FunctionNode):  # Функция (объявление)
            self.declare_function(
                node.name_token,
                node.return_type.value,
                [(param[0].value, param[1].value) for param in node.parameters]
            )
            self.enter_scope()
            # Проверяем, является ли тело функции одиночным StatementNode или списком
            if isinstance(node.body, StatementNode):
                for statement in node.body.statements:  # Проходим по операторам внутри StatementNode
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
if __name__ == "__main__":
    '''code = """
    int main() {
        int x;
        x = 5;
        return x;
    }
    """'''

    '''code = """
    int main() {
        int number;
        std::cin >> number;
        if (number % 2 == 0) {
            std::printf("The number is: ", number);
        } else {
            std::printf("The number is: ", 3);
        }
        return 0;
    }
    """'''

    # Ошибка: переменная y не была объявлена
    '''code = """
    int main() {
        int x;
        y = 10;
        return 0;
    }
    """'''

    '''code = """
    int sum(int a, int b) {
        return a + b;
    }

    int main() {
        int result = sum(5, 3);
        return 0;
    }
    """'''

    code = """
    int sum(int a, int b) {
        return a + b;
    }

    int main() {
        int result;
        result = sum(5, 3);
        return 0;
    }
    """




    tokens = tokenize(code)
    print(tokens)
    parser = Parser(tokens)
    ast = parser.parse()


    def print_ast(node, level=0):
        indent = "  " * level
        if isinstance(node, ValueNode):
            print(f"{indent}Value: {node.value.value}")
        elif isinstance(node, BinOperatorNode):
            print(f"{indent}Binary Operator: {node.operator.value}")
            print_ast(node.left, level + 1)
            print_ast(node.right, level + 1)
        elif isinstance(node, UnarOperatorNode):
            print(f"{indent}Unary Operator: {node.operator.value}")
            print_ast(node.operand, level + 1)
        elif isinstance(node, BlockNode):
            print(f"{indent}Block: {node.keyword.value}")
            print(f"{indent}Condition:")
            print_ast(node.condition, level + 1)
            print(f"{indent}Body:")
            for stmt in node.body:
                print_ast(stmt, level + 1)
            if node.else_branch:
                print(f"{indent}Else:")
                print_ast(node.else_branch, level + 1)
        elif isinstance(node, ElseNode):
            print(f"{indent}Else Block:")
            for stmt in node.body:
                print_ast(stmt, level + 1)
        elif isinstance(node, ElseIfNode):
            print(f"{indent}Else If:")
            print_ast(node.condition, level + 1)
            print(f"{indent}Body:")
            for stmt in node.body:
                print_ast(stmt, level + 1)
            if node.else_branch:
                print(f"{indent}Else:")
                print_ast(node.else_branch, level + 1)
        elif isinstance(node, StatementNode):
            print(f"{indent}Statements:")
            for stmt in node.statements:
                print_ast(stmt, level + 1)
        elif isinstance(node, FunctionNode):
            print(f"{indent}Function: {node.return_type.value} {node.name_token.value}")
            print(f"{indent}Parameters:")
            for param in node.parameters:
                print(f"{indent}  {param[0].value} {param[1].value}")
            print(f"{indent}Body:")
            print_ast(node.body, level + 1)
        elif isinstance(node, ReturnNode):
            print(f"{indent}Return:")
            print_ast(node.keyword, level + 1)
        elif isinstance(node, VariableDeclarationNode):
            print(f"{indent}Variable Declaration: {node.var_type.value} {node.var_name.value}")
            if node.value:
                print(f"{indent}  Assigned value:")
                print_ast(node.value, level + 1)
        elif isinstance(node, VariableUsageNode):
            print(f"{indent}Variable Usage: {node.var_name.value}")
        elif isinstance(node, FuncNode):
            print(f"{indent}Function Call: {node.func_token.value}")
            for arg in node.arguments:
                print(f"{indent}  Argument:")
                print_ast(arg, level + 1)
        elif isinstance(node, UseFuncNode):
            if node.name_variable != None:
                print(f"{indent}Variable Declaration: {node.return_type.value} {node.name_variable.value}")
                print(f"{indent}Operation: =")
            print(f"{indent}Function Call: {node.func_token.value}")
            print(f"{indent}Arguments:")
            for arg in node.arguments:
                print_ast(arg, level + 1)
        else:
            print(f"{indent}Unknown node type: {type(node)}")



    print_ast(ast)

    analyzer = SemanticAnalyzer()
    try:
        analyzer.check(ast)
        print("Семантический анализ прошел успешно!")
    except Exception as e:
        print(f"Семантическая ошибка: {e}")
