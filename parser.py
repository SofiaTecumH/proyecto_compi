class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def match(self, expected_type, expected_value=None):
        token = self.current_token()
        if token and token[0] == expected_type:
            if expected_value is None or token[1].upper() == expected_value.upper():
                self.pos += 1
                return token
        return None

    def expect(self, expected_type, expected_value=None):
        token = self.match(expected_type, expected_value)
        if not token:
            expected = expected_value if expected_value else expected_type
            actual = self.current_token()
            line = actual[2] if actual else "EOF"
            pos = actual[3] if actual else ""
            raise SyntaxError(f"Error sintáctico: se esperaba '{expected}' en línea {line} posición {pos}")
        return token

    def parse(self):
        instrucciones = []
        while self.pos < len(self.tokens):
            instr = self.parse_instruction()
            if instr:
                instrucciones.append(instr)
            else:
                token = self.current_token()
                if token:
                    line, col = token[2], token[3]
                    raise SyntaxError(f"Error sintáctico en línea {line} posición {col}: token inesperado {token}")
                else:
                    break
        return instrucciones

    def parse_instruction(self):
        token = self.current_token()
        if not token:
            return None

        if token[0] == 'KEYWORD':
            if token[1].upper() == 'CREATE':
                return self.parse_create()
            elif token[1].upper() == 'INSERT':
                return self.parse_insert()
            elif token[1].upper() == 'SELECT':
                return self.parse_select()
        return None

    def parse_create(self):
        # CREATE TABLE <table_name> ( <column_name> <type>, ... );
        self.expect('KEYWORD', 'CREATE')
        self.expect('KEYWORD', 'TABLE')
        table_name = self.expect('IDENTIFIER')[1]

        self.expect('SYMBOL', '(')
        columns = []

        while True:
            col_name = self.expect('IDENTIFIER')[1]
            col_type = self.expect('IDENTIFIER')[1].upper()

            # Validar tipos SQL aceptados
            if col_type not in ('INT', 'NUMBER', 'STRING', 'DATE'):
                raise SyntaxError(f"Tipo de dato inválido '{col_type}' en tabla '{table_name}'")

            columns.append((col_name, col_type))

            # Verificar si hay más columnas o si se debe cerrar el paréntesis
            token = self.current_token()
            if token and token[0] == 'SYMBOL':
                if token[1] == ',':
                    self.pos += 1  # Consumir ',' para seguir con otra columna
                elif token[1] == ')':
                    break  # Fin de la lista de columnas
                else:
                    raise SyntaxError(f"Token inesperado '{token[1]}' en definición de columnas.")
            else:
                raise SyntaxError("Se esperaba ',' o ')' después de la columna")

        self.expect('SYMBOL', ')')
        self.expect('SYMBOL', ';')

        return ('CREATE_TABLE', table_name, columns)

    def parse_insert(self):
        # INSERT INTO <table_name> VALUES ( val1, val2, ... );
        self.expect('KEYWORD', 'INSERT')
        self.expect('KEYWORD', 'INTO')
        table_name = self.expect('IDENTIFIER')[1]

        self.expect('KEYWORD', 'VALUES')
        self.expect('SYMBOL', '(')

        values = []
        while True:
            token = self.current_token()
            if token[0] in ('NUMBER', 'STRING', 'DATE'):
                values.append(token[1])
                self.pos += 1
            else:
                raise SyntaxError(f"Valor inválido en INSERT en línea {token[2]} posición {token[3]}")

            token = self.current_token()
            if token and token[0] == 'SYMBOL' and token[1] == ',':
                self.pos += 1  # consumir ','
            else:
                break

        self.expect('SYMBOL', ')')
        self.expect('SYMBOL', ';')

        return ('INSERT', table_name, values)

    def parse_select(self):
        # SELECT <columns> FROM <table> [WHERE <condition>] ;
        self.expect('KEYWORD', 'SELECT')

        # para simplificar, aceptar * o lista simple de columnas
        token = self.current_token()
        columns = []
        if token[0] == 'SYMBOL' and token[1] == '*':
            columns = ['*']
            self.pos += 1
        else:
            while True:
                col = self.expect('IDENTIFIER')[1]
                columns.append(col)
                token = self.current_token()
                if token and token[0] == 'SYMBOL' and token[1] == ',':
                    self.pos += 1
                else:
                    break

        self.expect('KEYWORD', 'FROM')
        table_name = self.expect('IDENTIFIER')[1]

        # WHERE opcional
        condition = None
        token = self.current_token()
        if token and token[0] == 'KEYWORD' and token[1] == 'WHERE':
            self.pos += 1
            condition = self.parse_condition()

        self.expect('SYMBOL', ';')
        return ('SELECT', columns, table_name, condition)

    def parse_condition(self):
        # condición simple: <identificador> <operador> <valor>
        left = self.expect('IDENTIFIER')[1]
        op = self.expect('OPERATOR')[1]
        token = self.current_token()
        if token[0] in ('NUMBER', 'STRING', 'DATE'):
            right = token[1]
            self.pos += 1
        else:
            raise SyntaxError(f"Valor inválido en condición en línea {token[2]} posición {token[3]}")

        return (left, op, right)
