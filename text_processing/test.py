from lexer import tokenize
from semanalizer import Semanalize
from sintaxer import Sintaxize


code = """int main(){
    int a = 4;
    int b = 5;
    int c = a + b;
    return 0;
}"""


tokens = tokenize(code)

tree, str_ast, code = Sintaxize(tokens)

semantalizer = Semanalize(str_ast)

print(code)
# print(semantalizer)

