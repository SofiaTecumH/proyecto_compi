from jinja2 import Environment, FileSystemLoader
# Datos de prueba
accion = "DELETE"
tabla = "usuarios"
mensaje = "Se ha insertado un nuevo registro correctamente."
resultados = [
    {"id": 1, "nombre": "Ana", "edad": 25},
    {"id": 2, "nombre": "Luis", "edad": 30},
]

# Cargar plantilla
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template("plantilla.html")

# Renderizar según la acción
html_generado = template.render(accion=accion, tabla=tabla, mensaje=mensaje, resultados=resultados)

# Guardar archivo HTML generado
with open("plantilla.html", "w", encoding="utf-8") as archivo:
    archivo.write(html_generado)

print("Archivo HTML generado correctamente.")