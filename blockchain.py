import os
import argparse
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# ==========================================
# Funciones Criptográficas
# ==========================================

def generar_llave(ruta_llave="secret.key"):
    """
    Genera una llave AES de 256 bits (32 bytes) y la guarda en un archivo.
    """
    key = get_random_bytes(32)
    with open(ruta_llave, "wb") as f:
        f.write(key)
    print(f"[+] Llave criptográfica generada y guardada en: {ruta_llave}")

def cifrar_archivo(ruta_entrada, ruta_llave="secret.key"):
    """
    Cifra un archivo de texto plano utilizando AES en modo EAX.
    """
    # RF-01: Validar tamaño máximo de 1 KB (1024 bytes)
    if os.path.getsize(ruta_entrada) > 1024:
        print("[-] Error: El archivo supera el tamaño máximo permitido de 1 KB.")
        return

    # Leer la llave y el archivo
    with open(ruta_llave, "rb") as f:
        key = f.read()
    with open(ruta_entrada, "rb") as f:
        data = f.read()

    # RF-03: Cifrar contenido
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    # Guardar archivo cifrado (Guardamos nonce, tag y el texto cifrado)
    ruta_salida = ruta_entrada + ".enc"
    with open(ruta_salida, "wb") as f:
        [f.write(x) for x in (cipher.nonce, tag, ciphertext)]
    
    print(f"[+] Archivo cifrado exitosamente: {ruta_salida}")

def descifrar_archivo(ruta_entrada, ruta_llave="secret.key"):
    """
    Descifra un archivo encriptado y recupera el texto original.
    """
    # Leer la llave
    with open(ruta_llave, "rb") as f:
        key = f.read()
    
    # Leer el archivo cifrado
    with open(ruta_entrada, "rb") as f:
        nonce = f.read(16)
        tag = f.read(16)
        ciphertext = f.read()

    # RF-04: Descifrar contenido
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    try:
        data = cipher.decrypt_and_verify(ciphertext, tag)
        ruta_salida = ruta_entrada.replace(".enc", ".dec")
        with open(ruta_salida, "wb") as f:
            f.write(data)
        
        print(f"[+] Archivo descifrado exitosamente: {ruta_salida}")
        print("-" * 40)
        print("Contenido recuperado:")
        print(data.decode('utf-8'))
        print("-" * 40)
    except ValueError:
        print("[-] Error: La llave es incorrecta o el archivo está corrupto.")

# ==========================================
# Interfaz de Línea de Comandos (CLI) - RF-05
# ==========================================

def main():
    parser = argparse.ArgumentParser(description="Herramienta básica de cifrado de archivos de texto plano.")
    subparsers = parser.add_subparsers(dest="comando", help="Comandos disponibles")

    # Comando: generar
    subparsers.add_parser("generar", help="Genera una nueva llave criptográfica AES")

    # Comando: cifrar
    parser_cifrar = subparsers.add_parser("cifrar", help="Cifra un archivo de texto")
    parser_cifrar.add_argument("archivo", help="Ruta del archivo a cifrar")

    # Comando: descifrar
    parser_descifrar = subparsers.add_parser("descifrar", help="Descifra un archivo de texto")
    parser_descifrar.add_argument("archivo", help="Ruta del archivo a descifrar (.enc)")

    args = parser.parse_args()

    if args.comando == "generar":
        generar_llave()
    elif args.comando == "cifrar":
        if os.path.exists(args.archivo):
            cifrar_archivo(args.archivo)
        else:
            print("[-] El archivo especificado no existe.")
    elif args.comando == "descifrar":
        if os.path.exists(args.archivo):
            descifrar_archivo(args.archivo)
        else:
            print("[-] El archivo cifrado especificado no existe.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()