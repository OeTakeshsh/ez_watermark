import os
import re

carpeta = "."

# patrón: foto + números + extensión
patron = re.compile(r"^foto\d+\.(jpg|jpeg|png)$", re.IGNORECASE)

eliminados = 0

for archivo in os.listdir(carpeta):

    if patron.match(archivo):

        ruta = os.path.join(carpeta, archivo)

        os.remove(ruta)

        print(f"🗑 Eliminado: {archivo}")

        eliminados += 1

print(f"\n✅ Total eliminados: {eliminados}")
