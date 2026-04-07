# Paquete Básico de Encriptación de Archivos

hellou este proyecto es una herramienta de línea de comandos (CLI) desarrollada en Python que permite cifrar y descifrar archivos de texto plano (menores a 1 KB) utilizando criptografía simétrica xd lol

## Justificación Criptográfica

* **Algoritmo seleccionado:** AES (Advanced Encryption Standard).
* **Tamaño de llave utilizado:** 256 bits (32 bytes). Se eligió este tamaño por ser el estándar más robusto actualmente en la industria, ofreciendo un nivel de seguridad óptimo contra ataques de fuerza bruta.
* **Modo de operación:** EAX (Encrypt-then-Authenticate-then-Translate). 
    * *Justificación:* A diferencia de modos más simples como ECB o CBC, EAX es un modo de cifrado autenticado (AEAD). Esto significa que no solo proporciona confidencialidad (cifra los datos), sino también integridad. Al cifrar, genera un "tag" (etiqueta) que se verifica al descifrar; si el archivo cifrado es modificado maliciosamente por un tercero, el programa lo detectará y se negará a descifrarlo. Además, no requiere la aplicación manual de algoritmos de padding (relleno).

## Instalación y Configuración

1. Asegúrate de tener Python 3.x instalado.
2. Clona este repositorio o descarga los archivos.
3. Abre una terminal en la carpeta del proyecto e instala las dependencias:
   ```bash
   pip install -r requirements.txt