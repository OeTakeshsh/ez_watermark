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

    # configuración
    config = common_res(w, h)

    escala = config["escala"]
    margen_x = config["margen_x"]
    margen_y = config["margen_y"]

    # copiar marca
    marca = marca_original.copy()

    # tamaño proporcional
    target_width = int(w * escala)

    # 👇 límites para equilibrar tamaños
    target_width = max(140, min(target_width, 240))

    ratio = target_width / marca.width

    new_size = (
        int(marca.width * ratio),
        int(marca.height * ratio)
    )

    marca = marca.resize(new_size)

    # opacidad
    alpha = marca.split()[3]
    alpha = alpha.point(lambda p: int(p * (opacidad / 100)))
    marca.putalpha(alpha)

    # posición (arriba izquierda)
    pos = (margen_x, margen_y)

    # pegar
    base.paste(marca, pos, marca)

    # guardar
    nombre = os.path.basename(imagen_path)
    salida = os.path.join(output_dir, nombre)

    base.convert("RGB").save(salida)

    print(f"💾 Guardado: {salida}")


def common_res(w, h):

    """
    Configuración según resolución
    """

    # imágenes grandes
    if w >= 1600 and h >= 1204:
        return {
            "escala": 0.085,
            "margen_x": 70,
            "margen_y": 50,
        }

    # verticales grandes
    elif w <= 1204 and h >= 1600:
        return {
            "escala": 0.09,
            "margen_x": 60,
            "margen_y": 70
        }

    # medianas
    elif w <= 1280 and h <= 963:
        return {
            "escala": 0.11,
            "margen_x": 55,
            "margen_y": 45
        }

    # fallback
    else:
        return {
            "escala": 0.10,
            "margen_x": 50,
            "margen_y": 40
        }


def main():

    archivos = os.listdir(carpeta)

    print(f"📂 Archivos encontrados: {len(archivos)}")

    procesados = 0

    for archivo in archivos:

        if (
            archivo.lower().endswith((".jpg", ".jpeg", ".png"))
            and archivo != os.path.basename(marca_path)
        ):

            ruta = os.path.join(carpeta, archivo)

            aplicar_watermark(ruta, opacidad=47)

            procesados += 1

    print(f"🏁 TERMINADO. Total procesados: {procesados}")


if __name__ == "__main__":
    main()
