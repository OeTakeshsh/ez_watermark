from PIL import Image

base = Image.open("foto1.jpeg").convert("RGBA")
marca = Image.open("marca.jpeg").convert("RGBA")

w, h = base.size

# 🔥 tamaño pequeño (10% del ancho)
target_width = int(w * 0.20)

ratio = target_width / marca.width
new_size = (int(marca.width * ratio), int(marca.height * ratio))

marca = marca.resize(new_size)

# superior, lateral
pos = (100, 50)

base.paste(marca, pos, marca)

base.convert("RGB").save("test.jpeg")

print("OK")
