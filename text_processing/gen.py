from lexer import Token
from nodes import *

toPython = {
    'true': 'True',
    'false': 'False',
    'std::printf': 'print',
    'std::cin()': 'input',
    '&&': 'and',
    '||': 'or',
}

MARGIN = '\t'


class CodeGenerator:
    def __init__(self) -> None:
        self.output = ''
        self.variables = set()

    def genPythonNode(self, node: ExpressionNode, level=0, end='') -> str:
        if type(node) == BlockNode:
            out = MARGIN * level + f'{node.keyword.value}'
            if node.condition is None:
                out += ' (' + '):'
            else:
                out += ' (' + self.genPythonNode(node.condition, 0, '):\n')
            for subnode in node.body:
                out += self.genPythonNode(subnode, level + 1, '\n')
            if node.else_branch is not None:
                out += self.genPythonNode(node.else_branch, level)
            return out + end
        
        if type(node) == StatementNode:
            out = ''
            for subnode in node.statements:
                out += MARGIN * level + self.genPythonNode(subnode, level, '\n')
            return out + end

        elif type(node) == ElseNode:
            out = MARGIN * level + 'else:' + '\n'
            for subnode in node.body:
                out += self.genPythonNode(subnode, level + 1, '\n')
            return out + end
        

        elif type(node) == ElseIfNode:
            out = MARGIN * level + 'elif ('
            out += self.genPythonNode(node.condition, 0, ')')
            for subnode in node.body:
                out += self.genPythonNode(subnode, level + 1, '\n')
            return out + end
        
        elif type(node) == FunctionNode:
            if (node.name_token.value != 'main'):
                out = MARGIN * level + 'def ' + f'{node.name_token.value} ('
                for args in node.parameters:
                    out += args[1].value + ', '
                out = out.rstrip(", ")
                out += '):\n'
                out += self.genPythonNode(node.body, level + 1, '')
                return out + end
            else:
                out = ''
                out += self.genPythonNode(node.body, 0, '\n')
                return out + end


        elif type(node) == UnarOperatorNode:
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
            out = MARGIN * level + f'{node.var_name.value} = '
            self.variables.add(node.var_name.value)
            out += self.genPythonNode(node.value, level)
            out += '\n'
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
            return out + end
        
        elif type(node) == UseFuncNode:
            out = MARGIN * level + f'{node.func_token.value} ('
            for args in node.arguments:
                out += self.genPythonNode(args, 0, ',')
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


        else:
            return '\n'

    def genPython(self, root: StatementNode) -> str:
        for node in root.statements:
            self.output += self.genPythonNode(node, 0)
        return self.output