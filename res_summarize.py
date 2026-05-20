import os
from PIL import Image
from collections import Counter

carpeta = "."
output_txt = "resoluciones.txt"

resoluciones = []

# Recorrer todas las imágenes
for archivo in os.listdir(carpeta):
    if archivo.lower().endswith((".jpg", ".jpeg", ".png")):
        ruta = os.path.join(carpeta, archivo)
        try:
            with Image.open(ruta) as img:
                w, h = img.size
                resoluciones.append(((w, h), archivo))  # guardamos resolución + nombre
        except Exception as e:
            print(f"⚠️ No se pudo abrir {archivo}: {e}")

# Guardar todas las resoluciones en un txt
with open(output_txt, "w") as f:
    for (w, h), nombre in resoluciones:
        f.write(f"{nombre}: {w}x{h}\n")  # ahora cada línea tiene el nombre de la imagen

print(f"✅ Se guardaron {len(resoluciones)} resoluciones en {output_txt}")

# Contar las más frecuentes
counter = Counter([res for res, _ in resoluciones])
mas_comunes = counter.most_common(5)  # top 5 más repetidas

print("\n📊 Resoluciones más comunes:")
for res, cuenta in mas_comunes:
    print(f"{res[0]}x{res[1]} -> {cuenta} veces")

# Media de las más repetidas
if mas_comunes:
    total_w = sum(res[0] * cuenta for res, cuenta in mas_comunes)
    total_h = sum(res[1] * cuenta for res, cuenta in mas_comunes)
    total_cuenta = sum(cuenta for _, cuenta in mas_comunes)
    media_w = total_w / total_cuenta
    media_h = total_h / total_cuenta
    print(f"\n📏 Media ponderada de las más repetidas: {int(media_w)}x{int(media_h)}")
