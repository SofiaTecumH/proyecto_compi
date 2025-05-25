class Table:
    def __init__(self, name, columns):
        self.name = name
        # columns: lista de tuplas (nombre_col, tipo)
        self.columns = self.validate_columns(columns)  # Validar estructura
        self.data = []  # lista de registros, cada uno es lista de valores

    def validate_columns(self, columns):
        if not isinstance(columns, list) or not all(isinstance(col, tuple) and len(col) == 2 for col in columns):
            raise ValueError(f"Error en la definición de columnas para '{self.name}'. Se esperaba lista de tuplas (nombre, tipo).")
        return columns

    def insert(self, values):
        if len(values) != len(self.columns):
            raise ValueError(f"Error: número de valores incorrecto para tabla '{self.name}'. Esperado {len(self.columns)}, recibido {len(values)}")

        for i, (col_name, col_type) in enumerate(self.columns):
            val = values[i]
            if not self.validate_type(val, col_type):
                raise ValueError(f"Error: tipo de dato incorrecto para columna '{col_name}' en tabla '{self.name}'")

        self.data.append(values)

    def validate_type(self, val, col_type):
        if col_type in ('INT', 'NUMBER'):
            try:
                int(val)
                return True
            except ValueError:
                return False
        elif col_type == 'STRING':
            return isinstance(val, str)
        elif col_type == 'DATE':
            import re
            return bool(re.match(r'\d{4}-\d{2}-\d{2}', val))
        else:
            return False

class Executor:
    def __init__(self):
        self.tables = {}

    def execute(self, instrucciones):
        resultados = []
        for instr in instrucciones:
            tipo = instr[0]
            if tipo == 'CREATE_TABLE':
                _, table_name, columns = instr
                if table_name in self.tables:
                    raise ValueError(f"Tabla '{table_name}' ya existe")
                self.tables[table_name] = Table(table_name, columns)  # Ahora maneja correctamente la regla

            elif tipo == 'INSERT':
                _, table_name, values = instr
                if table_name not in self.tables:
                    raise ValueError(f"Tabla '{table_name}' no existe")
                self.tables[table_name].insert(values)

            elif tipo == 'SELECT':
                _, columns, table_name, condition = instr
                if table_name not in self.tables:
                    raise ValueError(f"Tabla '{table_name}' no existe")
                cols, rows = self.tables[table_name].select(columns, condition)
                resultados.append((cols, rows))

            else:
                raise ValueError(f"Instrucción desconocida '{tipo}'")
        return resultados