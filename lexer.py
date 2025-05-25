import re

# Palabras clave válidas
KEYWORDS = {'CREATE', 'TABLE', 'INSERT', 'INTO', 'SELECT', 'FROM', 'WHERE', 'VALUES', 'UPDATE', 'SET', 'DELETE', 'PRIMARY'}

# Token types
TOKEN_TYPES = {
    'KEYWORD': r'\b(?:CREATE|TABLE|INSERT|INTO|SELECT|FROM|WHERE|VALUES|UPDATE|SET|DELETE|PRIMARY)\b',
    'IDENTIFIER': r'[a-zA-Z_][a-zA-Z0-9_]*',
    'STRING': r'\'[^\']*\'',
    'NUMBER': r'\d+(\.\d+)?',
    'DATE': r'\d{4}-\d{2}-\d{2}',
    'OPERATOR': r'!=|<=|>=|=|<|>',
    'SYMBOL': r'[\(\),;\*]',  # ✅ Aquí se incluye el *
    'WHITESPACE': r'\s+',
}

# Compilar expresiones regulares
token_regex = [(name, re.compile(pattern)) for name, pattern in TOKEN_TYPES.items()]

def tokenize_file(filename):
    tokens = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, start=1):
            tokens.extend(tokenize(line, line_num))
    return tokens

def tokenize(line, line_num):
    pos = 0
    tokens = []

    while pos < len(line):
        match_found = False

        for token_name, pattern in token_regex:
            match = pattern.match(line, pos)
            if match:
                value = match.group()
                if token_name == 'WHITESPACE':
                    pass  # ignorar espacios
                elif token_name == 'IDENTIFIER' and value.upper() in KEYWORDS:
                    tokens.append(('KEYWORD', value.upper(), line_num, pos))
                else:
                    tokens.append((token_name, value, line_num, pos))
                pos = match.end()
                match_found = True
                break

        if not match_found:
            print(f"Error léxico en línea {line_num}, posición {pos}: carácter no reconocido '{line[pos]}'")
            pos += 1  # saltar para seguir procesando

    return tokens

