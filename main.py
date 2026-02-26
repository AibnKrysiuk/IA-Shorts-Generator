import re
from escenas import Escena
from buscador_imagen import procesar_lista_escenas
from generador_voz import procesar_lista_audios
from editor import crear_video_short

def extraer_objetos_escena(ruta_txt):
    try:
        with open(ruta_txt, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except FileNotFoundError:
        return []

    bloques = re.findall(r'escena \d+\s*\{(.*?)\}', contenido, re.DOTALL)
    lista_objetos = []

    for bloque in bloques:
        m_txt = re.search(r'text:\s*"(.*?)"', bloque)
        m_img = re.search(r'imagenes:\s*"(.*?)"', bloque)
        m_fra = re.search(r'frase:\s*"(.*?)"', bloque)
        m_tip = re.search(r'tipo:\s*([^.\}\n]+)', bloque)

        if all([m_txt, m_img, m_fra, m_tip]):
            # Creamos la instancia usando el constructor de escenas.py
            nueva_escena = Escena(
                texto=m_txt.group(1).strip(),
                prompt_img=m_img.group(1).strip(),
                frase=m_fra.group(1).strip(),
                tipo=m_tip.group(1).strip()
            )
            lista_objetos.append(nueva_escena)
    
    return lista_objetos

if __name__ == "__main__":
    # 1. Crear objetos desde el TXT
    escenas_obj = extraer_objetos_escena("escenas.txt")

    if escenas_obj:
        # Preparamos la data simple para los generadores (compatibilidad)
        data_simple = [{"tipo": e.tipo, "imagenes": e.prompt_temp, "text": e.text} for e in escenas_obj]

        # 2. Generar archivos físicos (si no existen)
        print("--- GENERANDO RECURSOS ---")
        procesar_lista_escenas(data_simple)
        procesar_lista_audios(data_simple)

        # 3. Calcular metadatos finales y mostrar resultados
        print("\n--- RESUMEN DE ESCENAS ---")
        lista_para_editor = []
        
        for e in escenas_obj:
            e.calcular_metadatos() # Ahora que existen los audios, mide su tiempo
            lista_para_editor.append(e.to_dict())
            
            # Print de control
            info = e.to_dict()[e.tipo]
            print(f"✅ {info['tipo'].upper()} | Duración: {info['duracion']}s | Sonido: {info['sonido']}")

        # 4. Aquí tienes tu lista de objetos/diccionarios lista para el editor de video
        print("\n--- INICIANDO EDICIÓN DE VIDEO ---")
        crear_video_short(lista_para_editor, "MiHistoriaVampiros.mp4")