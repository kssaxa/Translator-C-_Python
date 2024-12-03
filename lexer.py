from typing import NamedTuple
import re


class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int


# Спецификация токенов для C++
TOKEN_SPECIFICATION = [
    ("NUMBER", r"\d+(\.\d*)?"),  # Числа
    ("KEYWORD", r"int|float|if|else|while|for|return"),  # Ключевые слова C++
    (
        "IDENTIFIER",
        r"[a-zA-Z_][a-zA-Z0-9_]*",
    ),  # Идентификаторы (имена переменных, функций)
    ("OPERATOR", r"[+\-*/]|==|!=|<=|>=|<|>|="),  # Операторы
    ("STRING", r"\".*?\"|\'.*?\'"),  # Строки
    ("SEPARATOR", r"[(){},;]"),  # Разделители
    ("COMMENT", r"//.*?$|/\*.*?\*/"),  # Комментарии (однострочные и многострочные)
    ("NEWLINE", r"\n"),  # Перенос строки
    ("SKIP", r"[ \t\r]+"),  # Пропуск пробелов
    ("MISMATCH", r"."),  # Неопределённые токены
]


def tokenize(code: str):
    """
    Функция для разбора исходного кода на токены.
    :param code: Исходный код C++
    :return: Список токенов
    """
    tokens = []
    tok_regex = "|".join("(?P<%s>%s)" % pair for pair in TOKEN_SPECIFICATION)
    line_num = 1
    line_start = 0
    for match in re.finditer(tok_regex, code):
        kind = match.lastgroup
        value = match.group()
        column = match.start() - line_start + 1

        if kind == "NEWLINE":
            line_num += 1
            line_start = match.end()
        elif kind == "SKIP":
            continue
        elif kind == "COMMENT":
            continue
        elif kind == "MISMATCH":
            raise SyntaxError(
                f"Unexpected token {value!r} at line {line_num}, column {column}"
            )
        tokens.append(Token(kind, value, line_num, column))

    return tokens


if __name__ == "__main__":
    
    cpp_code = 'int main() { int a = 5; float b = 10.0;if (a < b) { return a; } else { return b;} }'
    try:
        tokens = tokenize(cpp_code)
        for token in tokens:
            print(token)
    except SyntaxError as e:
        print(f"Ошибка: {e}")
