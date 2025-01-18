from .lexer import Token
from .nodes import *

toPython = {
    'true': 'True',
    'false': 'False',
    'std::printf': 'print',
    'std::cin()': 'input',
    '&&': 'and',
    '||': 'or',
}

MARGIN = '    '


class CodeGenerator:
    def __init__(self) -> None:
        self.output = ''
        self.variables = set()

    def genPythonNode(self, node: ExpressionNode, level=0, end='') -> str:
        if type(node) == BlockNode:
            if node.keyword.value == 'if':
                out = MARGIN * level + f'{node.keyword.value}'
                if node.condition is None:
                    out += ' (' + '):'
                else:
                    out += ' (' + self.genPythonNode(node.condition, 0, '):\n')
                for subnode in node.body:
                    out += self.genPythonNode(subnode, level + 1, '\n')
                if node.else_branch is not None:
                    out += self.genPythonNode(node.else_branch, level)
            elif node.keyword.value == 'while':
                out = f'{node.keyword.value} '
                if node.condition is None:
                    out += '()'
                else:
                    out += f'({self.genPythonNode(node.condition, 0)})'
                out += ':\n'
                for subnode in node.body:
                    out += self.genPythonNode(subnode, level + 1, '\n')
            elif node.keyword.value == 'for':
                out = ''
                out += self.genPythonNode(node.condition, level)
            else:
                out = ''
                out += self.genPythonNode(node.condition, level)
                for subnode in node.body:
                    out += self.genPythonNode(subnode, level + 1)
            return out + end

        if type(node) == StatementNode:
            out = ''
            for subnode in node.statements:
                if isinstance(subnode, list):
                    for subsubnode in subnode:
                        out += MARGIN * level + self.genPythonNode(subsubnode, level, '\n')
                elif isinstance(subnode, FuncNode):
                    out += f'{self.genPythonNode(subnode, level)}\n'
                else:
                    out += MARGIN * level + self.genPythonNode(subnode, level, '\n')
            return out + end

        elif type(node) == ElseNode:
            out = MARGIN * level + 'else:' + '\n'
            for subnode in node.body:
                out += self.genPythonNode(subnode, level + 1, '\n')
            return out + end


        elif type(node) == ElseIfNode:
            out = MARGIN * level + 'elif ('
            out += self.genPythonNode(node.condition, 0, ')') + '\n'
            for subnode in node.body:
                out += self.genPythonNode(subnode, level + 1, '\n')

            if isinstance(node.else_branch, ElseIfNode):
                out += self.genPythonNode(node.else_branch, level, '')
            elif isinstance(node.else_branch, ElseNode):
                out += MARGIN * level + 'else:\n'
                for subnode in node.else_branch.body:
                    out += self.genPythonNode(subnode, level + 1, '\n')

            return out + end

        elif type(node) == FunctionNode:
            if (node.name_token.value != 'main'):
                out = MARGIN * level + 'def ' + f'{node.name_token.value}('
                for args in node.parameters:
                    out += args.var_name.value + ', '
                out = out.rstrip(", ")
                out += '):\n'
                out += self.genPythonNode(node.body, level + 1, '')
                return out + end
            else:
                out = ''
                out += self.genPythonNode(node.body, 0, '\n')
                return out + end


        elif type(node) == UnarOperatorNode:
            p = self.genPythonNode(node.operand, 0)
            if node.operator.value == '--':
                out = MARGIN * level + f'{p} = {p} - 1'
            elif node.operator.value == '++':
                out = MARGIN * level + f'{p} = {p} + 1'
            else:
                out = MARGIN * level + \
                    f'{toPython[node.operator.value] if node.operator.value in toPython.keys() else node.operator.value}({self.genPythonNode(node.operand, 0, ")")}'
            return out + end

        elif type(node) == BinOperatorNode:
            out = MARGIN * level + \
                f'{self.genPythonNode(node.left, 0, " ")}{toPython[node.operator.value] if node.operator.value in toPython.keys() else node.operator.value} {self.genPythonNode(node.right, 0)}'
            return out + end

        elif type(node) == VariableDeclarationNode:
            if node.value is None:
                return ''
            out = f'{node.var_name.value} = '
            self.variables.add(node.var_name.value)
            out += self.genPythonNode(node.value, 0, '\n')
            return out + end

        elif type(node) == VariableUsageNode:
            out = MARGIN * level + \
                f'{node.var_name.value}'
            return out + end

        elif type(node) == ValueNode:
            out = MARGIN * level + \
                f'{toPython[node.value.value] if node.value.value in toPython.keys() else node.value.value}'
            return out + end

        elif type(node) == FuncNode:
            if node.func_token.value == 'std::printf':
                out = MARGIN * level + 'print' + '('
                for subnode in node.arguments:
                    out += self.genPythonNode(subnode, 0, ', ')
                out = out.rstrip(", ")
                out += ')'
            elif node.func_token.value == 'std::cin':
                out = MARGIN * level
                for subnode in node.arguments:
                    out += self.genPythonNode(subnode, 0, ', ')
                out = out.rstrip(", ")
                out += ' = input' + '()'
            elif node.func_token.value == 'std::cout':
                output = ''
                out =''
                for subnode in node.arguments:
                    if isinstance(subnode, StreamManipulatorNode):
                        output = output.rstrip(' + ')
                        out += MARGIN * level + f'print({output})\n'
                        output = ''
                    elif isinstance(subnode, BinOperatorNode):
                        output += f'str({self.genPythonNode(subnode, 0).strip()}) + '
                    elif isinstance(subnode, VariableUsageNode):
                        output += f'str({self.genPythonNode(subnode, 0).strip()}) + '
                    else:
                        output += self.genPythonNode(subnode, 0, ' + ')
                if output:
                    output = output.rstrip(' + ')
                    out += MARGIN * level + 'print' + '(' + output + ')' + '\n'
            return out + end

        elif type(node) == UseFuncNode:
            out = MARGIN * level
            out += f'{node.func_token.value}('
            for args in node.arguments:
                out += self.genPythonNode(args, 0, ', ')
            out = out.rstrip(", ")
            out += ')'
            return out + end

        elif type(node) == ReturnNode:
            if (level == 0):
                return ''
            elif type(node.keyword) == Token:
                out = 'return ' + f'{node.keyword.value}'
                return out + end
            else:
                out = 'return ' + f'{self.genPythonNode(node.keyword, 0)}'
                return out + end

        elif type(node) == ForNode:
            init_var = node.init.var_name.value
            start_value = self.genPythonNode(node.init.value, 0).strip()
            condition_right = self.genPythonNode(node.condition.right, 0).strip()
            if node.condition.operator.value == "<":
                stop_value = condition_right
            elif node.condition.operator.value == "<=":
                stop_value = int(condition_right) + 1
            else:
                stop_value = condition_right
            out = MARGIN * level + f'for {init_var} in range({start_value},{stop_value}):\n'
            for subnode in node.body:
                    out += self.genPythonNode(subnode, level + 1)
            return out + end

        elif type(node) == ArrayAccessNode:
            out = f'{node.array_name.value}[{self.genPythonNode(node.index_expression, 0)}]'
            return out + end

        elif type(node) == ArrayDeclarationNode:
            i = 0
            out = f'{node.var_name.value} = ['
            while (i < int(node.size.value)):
                out += f'{self.genPythonNode(node.elements[i], 0)}, '
                i = i+1
            out = out.rstrip(', ')
            out += ']'
            return out + end

        elif type(node) == DoWhileNode:
            out = MARGIN * level + f"while {self.genPythonNode(node.condition, 0)}:\n"
            for stmt in node.body:
                out += self.genPythonNode(stmt, level + 1)
            out += MARGIN * (level + 1) + "if not (" + self.genPythonNode(node.condition, 0) + "):\n"
            out += MARGIN * (level + 2) + "break\n"
            return out

        else:
            return '\n'

    def genPython(self, root: StatementNode) -> str:
        for node in root.statements:
            self.output += self.genPythonNode(node, 0)
        return self.output
