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

def aplicar_watermark(imagen_path, opacidad=50):
    print(f"🖼 Procesando: {imagen_path}")

    base = Image.open(imagen_path).convert("RGBA")
    w, h = base.size

    # 👇 obtener configuración según resolución
    config = common_res(w, h)

    escala = config["escala"]
    margen_x = config["margen_x"]
    margen_y = config["margen_y"]

    # redimensionar marca proporcional al ancho de la base
    marca = marca_original.copy()
    target_width = int(w * escala)
    ratio = target_width / marca.width
    new_size = (int(marca.width * ratio), int(marca.height * ratio))
    marca = marca.resize(new_size)

    # aplicar opacidad
    alpha = marca.split()[3]
    alpha = alpha.point(lambda p: int(p * (opacidad / 100)))
    marca.putalpha(alpha)

    # posición
    pos = (margen_x, margen_y)

    # pegar watermark
    base.paste(marca, pos, marca)

    # guardar
    nombre = os.path.basename(imagen_path)
    salida = os.path.join(output_dir, nombre)
    base.convert("RGB").save(salida)

    print(f"💾 Guardado: {salida}")

def common_res(w, h):

    """
    Devuelve escala y márgenes según resolución.
    """

    # imágenes grandes (horizontal o muy grandes)
    if w >= 1600 and h >= 1204:
        return {
            "escala": 0.12,
            "margen_x": 30,
            "margen_y": 30
        }

    # imágenes verticales grandes
    elif w <= 1204 and h >= 1600:
        return {
            "escala": 0.10,
            "margen_x": 25,
            "margen_y": 40
        }

    # resolución media tipo 1280x963 o similar
    elif w <= 1280 and h <= 963:
        return {
            "escala": 0.08,
            "margen_x": 25,
            "margen_y": 25
        }

    # fallback (caso general)
    else:
        return {
            "escala": 0.10,
            "margen_x": 20,
            "margen_y": 20
        }


def main():
    archivos = os.listdir(carpeta)
    print(f"📂 Archivos encontrados: {len(archivos)}")

    procesados = 0
    for archivo in archivos:
        if archivo.lower().endswith((".jpg", ".jpeg", ".png")) and archivo != os.path.basename(marca_path):
            ruta = os.path.join(carpeta, archivo)
            aplicar_watermark(ruta, opacidad=47)
            procesados += 1

    print(f"🏁 TERMINADO. Total procesados: {procesados}")


if __name__ == "__main__":
    main()
