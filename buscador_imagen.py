import requests
import os
import time
from dotenv import load_dotenv

# Cargar configuración
load_dotenv()
API_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def consultar_hf(prompt, reintentos=3):
    """Envía el prompt a Hugging Face y maneja el tiempo de espera"""
    for i in range(reintentos):
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
        
        if response.status_code == 200:
            return response.content
        elif response.status_code == 503: # El modelo se está cargando
            print(f"⏳ El modelo está cargando... esperando 20s (intento {i+1}/{reintentos})")
            time.sleep(20)
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            break
    return None

def ejecutar_buscador():
    # 1. Crear carpeta si no existe
    if not os.path.exists("imagenes"):
        os.makedirs("imagenes")

    # 2. Leer prompts
    if not os.path.exists("prompts.txt"):
        print("❌ No se encontró el archivo prompts.txt")
        return

    with open("prompts.txt", "r", encoding="utf-8") as f:
        prompts = [line.strip() for line in f if line.strip()]

    print(f"🚀 Iniciando descarga de {len(prompts)} imágenes...")

    # 3. Procesar cada prompt
    for index, prompt in enumerate(prompts):
        nombre_archivo = f"imagenes/escena_{index + 1}.png"
        
        # 1. Verificamos si la imagen ya existe para no gastar cuota innecesariamente
        if os.path.exists(nombre_archivo):
            print(f"⏩ Saltando escena_{index + 1}, ya existe.")
            continue

        print(f"🎨 Generando ({index + 1}/{len(prompts)}): {prompt[:40]}...")
        
        imagen_bytes = consultar_hf(prompt)
        
        if imagen_bytes:
            with open(nombre_archivo, "wb") as f:
                f.write(imagen_bytes)
            print(f"✅ Guardado: {nombre_archivo}")
        
        # 2. EL PAUSA ESTRATÉGICA:
        # Esperamos 5 segundos entre imágenes. Esto mantiene tu "reputación" 
        # limpia ante el Router de Hugging Face.
        print("Waiting 5 seconds for next request...")
        time.sleep(5)

if __name__ == "__main__":
    ejecutar_buscador()