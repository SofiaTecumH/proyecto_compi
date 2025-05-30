from lexer import tokenize_file
from parser import Parser
from executor import Executor


def main():
    tokens = tokenize_file("entrada.sql")  # Obtiene tokens y errores
    parser = Parser(tokens)

    try:
        instrucciones = parser.parse()
        executor = Executor()
        resultados = executor.execute(instrucciones)

        for cols, rows in resultados:
            print("Columnas:", cols)
            for r in rows:
                print(r)

    except SyntaxError as e:
        print(f" Error sintáctico detectado: {e}")
        print(" No se ejecutará el código ni se generará HTML.")

    except ValueError as e:
        print(f" Error de ejecución detectado: {e}")
        print(" No se generará el archivo HTML debido a errores en la ejecución.")


if __name__ == "__main__":
    main()
