from lexer import tokenize
from lexer import tokenize_file
from parser import Parser
from executor import Executor

def main():
    tokens = tokenize_file("entrada.sql")
    parser = Parser(tokens)

    try:
        instrucciones = parser.parse()
        executor = Executor()
        resultados = executor.execute(instrucciones)

        for cols, rows in resultados:
            print("Columnas:", cols)
            for r in rows:
                print(r)

        # Aquí puedes agregar el código para generar el HTML con los resultados.

    except (SyntaxError, ValueError) as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
