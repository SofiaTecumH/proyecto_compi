from datetime import datetime
import re

class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = self.validate_columns(columns)
        self.data = []

    def validate_columns(self, columns):
        if not isinstance(columns, list) or not all(isinstance(col, tuple) and len(col) >= 2 for col in columns):
            raise ValueError(f"Error en la definición de columnas para '{self.name}'. Se esperaba lista de tuplas (nombre, tipo[, restricciones])")
        return columns

    def insert(self, values):
        if len(values) != len(self.columns):
            raise ValueError(f"Error: número de valores incorrecto para tabla '{self.name}'. Esperado {len(self.columns)}, recibido {len(values)}")

        cleaned_values = []
        for i, col in enumerate(self.columns):
            col_name = col[0]
            col_type = col[1]
            val = values[i]

            # Limpiar comillas si es string con comillas externas
            if isinstance(val, str):
                if (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
                    val = val[1:-1]

            if not self.validate_type(val, col_type):
                raise ValueError(f"Error: tipo de dato incorrecto para columna '{col_name}' en tabla '{self.name}'")

            cleaned_values.append(val)

        self.data.append(cleaned_values)

    def validate_type(self, val, col_type):
        if col_type.startswith('VARCHAR'):
            return isinstance(val, str)
        elif col_type in ('INT', 'NUMBER'):
            try:
                int(val)
                return True
            except:
                return False
        elif col_type == 'STRING':
            return isinstance(val, str)
        elif col_type == 'DATE':
            try:
                datetime.strptime(val, '%Y-%m-%d')
                return True
            except:
                return False
        else:
            return False

    def select(self, columns, condition=None):
        if columns == ['*']:
            cols = [col[0] for col in self.columns]
        else:
            cols = columns

        col_indices = [self.get_column_index(c) for c in cols]

        filtered_rows = [row for row in self.data if (condition is None or condition(row))]

        result_rows = [[row[i] for i in col_indices] for row in filtered_rows]
        return cols, result_rows

    def update(self, updates, condition=None):
        for i, row in enumerate(self.data):
            if condition is None or condition(row):
                new_row = list(row)
                for col_name, new_val in updates.items():
                    idx = self.get_column_index(col_name)
                    col_type = self.columns[idx][1]
                    if not self.validate_type(new_val, col_type):
                        raise ValueError(f"Error: tipo de dato incorrecto para columna '{col_name}' en tabla '{self.name}'")
                    new_row[idx] = new_val
                self.data[i] = new_row

    def delete(self, condition=None):
        self.data = [row for row in self.data if not (condition is None or condition(row))]

    def get_column_index(self, col_name):
        for i, col in enumerate(self.columns):
            if col[0] == col_name:
                return i
        raise ValueError(f"Columna '{col_name}' no existe en tabla '{self.name}'")

    def __repr__(self):
        return f"<Table {self.name} columnas={self.columns} filas={len(self.data)}>"

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
                self.tables[table_name] = Table(table_name, columns)

            elif tipo == 'INSERT':
                # Ahora desempacamos columnas y valores
                _, table_name, columns, values = instr
                if table_name not in self.tables:
                    raise ValueError(f"Tabla '{table_name}' no existe")

                # Si columns es None, asumimos orden según tabla
                if columns is None:
                    self.tables[table_name].insert(values)
                else:
                    # Insert con columnas específicas
                    # Crear fila con valores en el orden de las columnas de la tabla
                    row = [None] * len(self.tables[table_name].columns)
                    for col_name, val in zip(columns, values):
                        idx = self.tables[table_name].get_column_index(col_name)
                        row[idx] = val
                    # Rellenar valores faltantes con None o valor por defecto
                    for i in range(len(row)):
                        if row[i] is None:
                            row[i] = None  # O puedes definir otro valor por defecto
                    self.tables[table_name].insert(row)

            elif tipo == 'SELECT':
                _, columns, table_name, condition = instr
                if table_name not in self.tables:
                    raise ValueError(f"Tabla '{table_name}' no existe")

                # condition puede ser una tupla (left, op, right) o None
                condition_func = self.build_condition_func(table_name, condition)
                cols, rows = self.tables[table_name].select(columns, condition_func)
                resultados.append((cols, rows))

            elif tipo == 'UPDATE':
                _, table_name, updates, condition = instr
                if table_name not in self.tables:
                    raise ValueError(f"Tabla '{table_name}' no existe")
                condition_func = self.build_condition_func(table_name, condition)
                self.tables[table_name].update(updates, condition_func)

            elif tipo == 'DELETE':
                _, table_name, condition = instr
                if table_name not in self.tables:
                    raise ValueError(f"Tabla '{table_name}' no existe")
                condition_func = self.build_condition_func(table_name, condition)
                self.tables[table_name].delete(condition_func)

            else:
                raise ValueError(f"Instrucción desconocida '{tipo}'")
        return resultados

    def build_condition_func(self, table_name, condition):
        """
        Construye una función condicional para filtrar filas según la condición
        condition: tupla (columna, operador, valor) o None
        """
        if not condition:
            return None
        col, op, val = condition
        table = self.tables[table_name]
        col_idx = table.get_column_index(col)

        def cond_func(row):
            cell = row[col_idx]
            # Convertir tipos para comparación (si es número, convertir a int)
            try:
                if isinstance(cell, str) and cell.isdigit():
                    cell_val = int(cell)
                else:
                    cell_val = cell
            except:
                cell_val = cell

            try:
                if isinstance(val, str) and val.isdigit():
                    val_cmp = int(val)
                else:
                    val_cmp = val
            except:
                val_cmp = val

            if op == '=':
                return cell_val == val_cmp
            elif op == '!=':
                return cell_val != val_cmp
            elif op == '<':
                return cell_val < val_cmp
            elif op == '>':
                return cell_val > val_cmp
            elif op == '<=':
                return cell_val <= val_cmp
            elif op == '>=':
                return cell_val >= val_cmp
            else:
                raise ValueError(f"Operador desconocido '{op}' en condición")

        return cond_func
