import re

KEYWORDS = {
    'CREATE', 'TABLE', 'INSERT', 'INTO', 'VALUES', 'SELECT', 'FROM', 'WHERE',
    'UPDATE', 'SET', 'DELETE', 'PRIMARY', 'KEY', 'NOT', 'NULL', 'UNIQUE'
}

TOKEN_TYPES = {
    'DATE': r'\d{4}-\d{2}-\d{2}',
    'KEYWORD': r'\b(?:CREATE|TABLE|INSERT|INTO|VALUES|SELECT|FROM|WHERE|PRIMARY|KEY|NOT|NULL|UNIQUE|UPDATE|SET|DELETE)\b',
    'IDENTIFIER': r'[a-zA-Z_][a-zA-Z0-9_]*',
    'STRING': r"'(?:[^'\\]|\\.)*'",
    'NUMBER': r'\d+',
    'OPERATOR': r'!=|<=|>=|=|<|>',
    'SYMBOL': r'[(),;*]',
    'WHITESPACE': r'\s+',
}

TOKEN_ORDER = ['DATE', 'KEYWORD', 'IDENTIFIER', 'STRING', 'NUMBER', 'OPERATOR', 'SYMBOL', 'WHITESPACE']

token_regex = [(name, re.compile(TOKEN_TYPES[name])) for name in TOKEN_ORDER]

def tokenize(line, line_num=1):
    pos = 0
    tokens = []
    while pos < len(line):
        match_found = False
        for token_name, pattern in token_regex:
            match = pattern.match(line, pos)
            if match:
                value = match.group()
                if token_name == 'WHITESPACE':
                    # Ignorar espacios en blanco
                    pass
                elif token_name == 'IDENTIFIER' and value.upper() in KEYWORDS:
                    tokens.append(('KEYWORD', value.upper(), line_num, pos))
                else:
                    tokens.append((token_name, value, line_num, pos))
                pos = match.end()
                match_found = True
                break
        if not match_found:
            print(f"Error léxico en línea {line_num}, posición {pos}: carácter no reconocido '{line[pos]}'")
            pos += 1
    return tokens

def tokenize_file(filename):
    tokens = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, start=1):
            tokens.extend(tokenize(line, line_num))
    return tokens

if __name__ == '__main__':
    ejemplo = "SELECT nombre, edad FROM empleados WHERE fecha_nac = '1990-05-20';"
    tokens = tokenize(ejemplo, 1)
    for t in tokens:
        print(t)


