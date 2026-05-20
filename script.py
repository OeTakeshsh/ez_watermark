import os
from PIL import Image

carpeta = "."
marca_path = "marca.png"
output_dir = "output"

os.makedirs(output_dir, exist_ok=True)

print("🚀 Iniciando script...")

# cargar marca UNA sola vez
marca_original = Image.open(marca_path).convert("RGBA")
print("✅ Marca cargada")

def aplicar_watermark(imagen_path, margen_x=20, margen_y=20, escala=0.10,opacidad=50):
    print(f"🖼 Procesando: {imagen_path}")

    base = Image.open(imagen_path).convert("RGBA")
    w, h = base.size

    # redimensionar marca proporcional al ancho de la base
    marca = marca_original.copy()
    target_width = int(w * escala)
    ratio = target_width / marca.width
    new_size = (int(marca.width * ratio), int(marca.height * ratio))
    marca = marca.resize(new_size)

    # aplicar opacidad correctamente
    alpha = marca.split()[3]
    alpha = alpha.point(lambda p: int(p * (opacidad / 100)))
    marca.putalpha(alpha)

    # posición con margen
    pos = (margen_x, margen_y)

    # pegar directamente respetando alpha
    base.paste(marca, pos, marca)

    # guardar
    nombre = os.path.basename(imagen_path)
    salida = os.path.join(output_dir, nombre)
    base.convert("RGB").save(salida)
    print(f"💾 Guardado: {salida}")


def main():
    archivos = os.listdir(carpeta)
    print(f"📂 Archivos encontrados: {len(archivos)}")

    procesados = 0
    for archivo in archivos:
        if archivo.lower().endswith((".jpg", ".jpeg", ".png")) and archivo != os.path.basename(marca_path):
            ruta = os.path.join(carpeta, archivo)
            aplicar_watermark(ruta, opacidad=70, margen_x=20, margen_y=20, escala=0.10)
            procesados += 1

    print(f"🏁 TERMINADO. Total procesados: {procesados}")


if __name__ == "__main__":
    main()
