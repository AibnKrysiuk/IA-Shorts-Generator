# AI Shorts Generator 🎥 (Horror & Mystery Edition)

Sistema automatizado para la creación de YouTube Shorts con estética de misterio, horror cósmico y "found footage". Este motor orquesta la generación de imágenes por IA, narrativa, música atmosférica y post-producción avanzada de video.



## ✨ Características Premium

* **Edición Multi-Escena:** Soporte nativo para estructuras de hasta 9 escenas (Hook -> Tensión -> Punto de Quiebre -> CTA).
* **Cinematografía Dinámica:** * **Efecto Ken Burns:** Zoom suave automático en todas las imágenes para eliminar el estatismo.
    * **Vignette Look:** Capa de viñeta oscura para enfocar la atención y dar profundidad.
    * **Transiciones:** Fundidos a negro y solapamientos de audio de -0.7s para mayor fluidez narrativa.
* **Subtítulos de Impacto:** * Generación de texto dinámico con bordes resaltados (*stroke*).
    * **Frases Clave:** Resaltado en amarillo con efectos de entrada/salida (*Zoom-In* y *Fade-Out*).
* **Audio Atmosférico:**
    * Gestión de música de fondo con **Audio Ducking** (la música entra después del Hook).
    * Mezcla de voz (TTS) y efectos de sonido (SFX).
* **Cierre de Canal:** Integración automática de video animado (`cta.mp4`) en la escena final.

## 🛠️ Tecnologías Usadas

* **Python 3.10+**
* **MoviePy 2.0+** (Motor de video de última generación)
* **Hugging Face API** (Generación de imágenes con modelos SDXL/Flux)
* **Git LFS** (Opcional, para manejo de assets pesados)

## 🚀 Instalación y Uso

1. **Clonar el repositorio:**
   git clone [https://github.com/tu-usuario/IA-Shorts-Generator.git](https://github.com/tu-usuario/IA-Shorts-Generator.git)
   cd IA-Shorts-Generator
   
2. **Preparar el entorno:
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
3. **Configuración de Assets:

Asegúrate de tener una carpeta assets/ con:

background.mp3 (música de fondo).

cta.mp4 (video final de suscripción).

arialbd.ttf (fuente para subtítulos).

4. **Ejecución:
Define tu historia en un archivo .txt y corre el script principal:

python main.py


📝 Formato del Guion (Input)
El sistema procesa bloques estructurados como el siguiente:

Plaintext
escena 1{
    text: "Murió tres veces esa noche, pero seguía pidiendo un cigarrillo."
    imagenes: "Close-up of a pale man, bloody collar, noir high contrast."
    frase: "La inmortalidad es una condena."
    tipo: hook
}


📂 Estructura del Proyecto
main.py: Punto de entrada y orquestador.

editor.py: Lógica de montaje, capas y efectos cinematográficos.

subtitulador.py: Renderizado de fuentes, colores y VFX de texto.

assets/: Recursos estáticos (música, videos CTA, tipografías).

Desarrollado para creadores de contenido que buscan automatizar la calidad, no solo la cantidad. 🌑
