import os

pasta = "."   # pasta atual

arquivos = os.listdir(pasta)

contador = 1

for arquivo in arquivos:

    if os.path.isfile(arquivo) and arquivo != "change_name.py":

        extensao = os.path.splitext(arquivo)[1]

        novo_nome = f"foto{contador}{extensao}"

        os.rename(arquivo, novo_nome)

        print(f"{arquivo} -> {novo_nome}")

        contador += 1
