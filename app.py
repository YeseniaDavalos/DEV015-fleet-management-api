"""
Este es un ejemplo básico de una aplicación Flask que devuelve 'Hello, World!'.
"""
from app import create_app  # Esto ahora no generará conflicto

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

# Añadir una línea en blanco al final del archivo
