import os
from escenas import Escena
from editor import crear_video_short

def probar_escena_unica():
    # 1. Configuración de prueba
    # Asegúrate de tener al menos una imagen en /imagenes y un audio en /audios
    # Si no los tienes, renombra cualquier .jpg a 'contextominimo.jpg'
    tipo_test = "contextominimo"
    texto_test = "Bajo los arcos de la catedral de San Judas, donde la humedad devora la piedra."
    frase_test = "El tiempo se detuvo en 1890."
    
    print(f"🛠️ Iniciando prueba rápida para: {tipo_test}")

    # 2. Crear el objeto escena manualmente
    escena_test = Escena(
        texto=texto_test,
        prompt_img="prompt_de_prueba", 
        frase=frase_test,
        tipo=tipo_test
    )

    # 3. Forzar metadatos para la prueba
    # Si el archivo de audio existe, calculará la duración real.
    # Si no, puedes forzarla manualmente para la prueba:
    if os.path.exists(escena_test.audio):
        escena_test.calcular_metadatos()
    else:
        print(f"⚠️ No se encontró {escena_test.audio}, usando duración ficticia de 5s")
        escena_test.duracion = 5.0
        # Forzamos una imagen si la ruta no existe para que MoviePy no explote
        if not os.path.exists(escena_test.imagen):
            print("❌ Error: Necesitas al menos una imagen real en /imagenes para probar.")
            return

    # 4. Convertir al formato que espera el editor
    lista_prueba = [escena_test.to_dict()]

    # 5. Ejecutar solo el editor
    # Guardamos con un nombre distinto para no sobreescribir el final
    nombre_output = "TEST_PROCESAMIENTO.mp4"
    
    print("🎬 Renderizando clip de prueba...")
    crear_video_short(lista_prueba, nombre_output)
    
    print(f"\n✅ Prueba finalizada. Abre el archivo: {nombre_output}")

if __name__ == "__main__":
    probar_escena_unica()