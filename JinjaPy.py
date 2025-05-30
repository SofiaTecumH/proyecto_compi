from jinja2 import Environment, FileSystemLoader

class HtmlGenerator:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('.'))

    def generate_html(self, resultados, mensajes):
        """Genera un archivo HTML con los resultados de SQL y mensajes de éxito."""
        template_str = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Resultados SQL</title>
            <style>
                table { width: 100%; border-collapse: collapse; }
                th, td { border: 1px solid black; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                .mensaje { margin-bottom: 10px; font-weight: bold; }
            </style>
        </head>
        <body>
            <h2>Resultados SQL</h2>

            {% for mensaje in mensajes %}
                <p class="mensaje">{{ mensaje }}</p>
            {% endfor %}

            <table>
                <thead>
                    <tr>
                        {% for col in columnas %}
                            <th>{{ col }}</th>
                        {% endfor %}
                    </tr>
                </thead>
                <tbody>
                    {% for fila in datos %}
                    <tr>
                        {% for valor in fila %}
                            <td>{{ valor }}</td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </body>
        </html>
        """

        template = self.env.from_string(template_str)
        columnas, datos = resultados[0]

        html_generado = template.render(columnas=columnas, datos=datos, mensajes=mensajes)

        with open("salida.html", "w", encoding="utf-8") as archivo:
            archivo.write(html_generado)

        print("Archivo HTML generado correctamente como 'salida.html'.")
