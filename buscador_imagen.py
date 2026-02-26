import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("HF_TOKEN")
# URL del modelo FLUX
API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

# Añadimos "vertical mobile 9:16 aspect ratio" al final por si acaso
ESTETICA = "Gritty graphic novel noir style, heavy black ink outlines, hand-drawn sketchy texture, cel-shaded illustration, deep chiaroscuro shadows, moody desaturated color palette with sickly amber and charcoal tones, rough painterly brushstrokes, dark and ominous atmosphere, non-realistic comic book art, vertical mobile 9:16 aspect ratio"

def consultar_hf(prompt, reintentos=3):
    """Envía el prompt con parámetros de dimensiones para 9:16"""
    payload = {
        "inputs": prompt,
        "parameters": {
            "width": 576,   # Ancho para 9:16
            "height": 1024  # Alto para 9:16
        }
    }
    
    for i in range(reintentos):
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            return response.content
        elif response.status_code == 503:
            print(f"⏳ Modelo cargando... esperando 20s (intento {i+1}/{reintentos})")
            time.sleep(20)
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            break
    return None

def procesar_lista_escenas(lista_escenas):
    if not os.path.exists("imagenes"):
        os.makedirs("imagenes")

    print(f"🚀 Procesando {len(lista_escenas)} imágenes en formato 9:16...")

    for escena in lista_escenas:
        # Usamos el tipo como nombre de archivo
        nombre_archivo = f"imagenes/{escena['tipo']}.jpg"
        prompt_final = f"{ESTETICA}, {escena['imagenes']}"

        if os.path.exists(nombre_archivo):
            print(f"⏩ Saltando {escena['tipo']}, ya existe.")
            continue

        print(f"🎨 Generando {escena['tipo']}...")
        imagen_bytes = consultar_hf(prompt_final)
        
        if imagen_bytes:
            with open(nombre_archivo, "wb") as f:
                f.write(imagen_bytes)
            print(f"✅ Guardado: {nombre_archivo}")
        
        # Espera de cortesía para la API
        time.sleep(5)