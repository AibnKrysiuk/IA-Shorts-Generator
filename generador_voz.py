import asyncio
import edge_tts
import os

ALONSO = 'es-US-AlonsoNeural'
JORGE =  'es-MX-JorgeNeural' 
VOZ_NARRADOR = JORGE 
OUTPUT_FOLDER = "audios"

async def generar_audio_async(texto, nombre_archivo):
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    
    archivo_final = os.path.join(OUTPUT_FOLDER, f"{nombre_archivo}.mp3")
    
    # Verificación de existencia para no gastar recursos
    if os.path.exists(archivo_final):
        print(f"⏩ Saltando audio {nombre_archivo}, ya existe.")
        return

    communicate = edge_tts.Communicate(texto, VOZ_NARRADOR, pitch="-5Hz", rate="+0%")
    await communicate.save(archivo_final)
    print(f"🎙️ Audio generado: {archivo_final}")

def procesar_lista_audios(lista_escenas):
    """
    Recibe la lista de diccionarios con 'text' y 'tipo'.
    """
    print(f"🔊 Iniciando procesamiento de {len(lista_escenas)} audios...")
    
    loop = asyncio.get_event_loop()
    
    # Creamos una tarea por cada escena
    tareas = []
    for escena in lista_escenas:
        # Usamos el campo 'text' para el contenido y 'tipo' para el nombre
        tareas.append(generar_audio_async(escena['text'], escena['tipo']))
    
    # Ejecutamos todas las tareas
    loop.run_until_complete(asyncio.gather(*tareas))