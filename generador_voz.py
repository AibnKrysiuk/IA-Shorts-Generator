import asyncio
import edge_tts
import os

# Configuración: Aquí elegimos la voz
JORGE =  'es-MX-JorgeNeural' 
ALONSO = 'es-US-AlonsoNeural'
# 'es-ES-AlvaroNeural' es la versión de España, también muy seria.
VOZ_NARRADOR = JORGE
OUTPUT_FOLDER = "audios"

async def generar_audio(texto, nombre_archivo):
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    
    archivo_final = os.path.join(OUTPUT_FOLDER, nombre_archivo)
    communicate = edge_tts.Communicate(texto, VOZ_NARRADOR, pitch="-5Hz", rate="+0%")
    await communicate.save(archivo_final)
    print(f"🎙️ Audio generado con éxito: {archivo_final}")

def ejecutar_voz():
    if not os.path.exists("guion.txt"):
        print("❌ Error: Crea un archivo 'guion.txt' con el texto para el Short.")
        return

    with open("guion.txt", "r", encoding="utf-8") as f:
        contenido = f.read().strip()

    if contenido:
        print("🔊 Procesando voz de narrador...")
        asyncio.run(generar_audio(contenido, "narracion_final.mp3"))
    else:
        print("⚠️ El archivo guion.txt está vacío.")

if __name__ == "__main__":
    ejecutar_voz()