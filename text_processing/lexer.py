from typing import NamedTuple
import re


class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int


# Спецификация токенов для C++
TOKEN_SPECIFICATION = [
    ("PREPROCESSOR", r"#\s*\w+"),  # Директивы препроцессора
    ("NUMBER", r"\d+(\.\d*)?"),  # Числа
    ("KEYWORD", r"int|float|return|void|bool"),  # Ключевые слова C++
    ("BLOCK", r"if|else|while|for"),  # Блоки управления
    ("BOOL", r"true|false"),  # Логические значения
    ("FUNC", r"std::cin|std::cout|std::printf|std::scanf|std::getline"),  # Функции ввода/вывода
    ("IDENTIFIER", r"[a-zA-Z_][a-zA-Z0-9_]*"),  # Идентификаторы (имена переменных, функций)
    ("OPERATOR", r"\+\+|\-\-|==|!=|<=|>=|<<|>>|=|\+|\-|\*|/|<|>|%|\?|:"),  # Операторы
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
