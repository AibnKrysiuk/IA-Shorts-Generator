import os
import textwrap
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
from moviepy import TextClip, CompositeVideoClip
import moviepy.video.fx as vfx

RUTA_FUENTE = r"C:\Windows\Fonts\arialbd.ttf"
ancho_maximo = 950
def crear_subtitulos(texto,frase_clave, duracion_escena):
    # 1. Forzamos el salto de línea manual a los 35 caracteres
    # wrap() crea una lista de líneas, join() las une con saltos de línea \n
    texto_formateado = "\n".join(textwrap.wrap(texto, width=35)) + "\n"
    
    # 2. Ahora que el texto ya tiene los saltos de línea correctos, 
    # podemos usar TextClip.
    subtitulo = TextClip(
        text=texto_formateado,
        font_size=55,
        color='white',
        font=RUTA_FUENTE,
        stroke_color='red',
        stroke_width=3,
        # Usamos 'caption' con un ancho mayor para que respete nuestros \n 
        # y no añada saltos extra inesperados.
        method='label', 
        text_align='center'
    ).with_duration(duracion_escena)
    # --- 2. CONFIGURACIÓN DE LA FRASE CLAVE (Centro) ---
    # La frase clave suele ser corta, pero por seguridad también le damos wrap
    texto_frase = "\n".join(textwrap.wrap(frase_clave.upper(), width=25)) + "\n" # En MAYÚSCULAS para impacto
    sub_frase_central = TextClip(
        text=texto_frase,
        font_size=70,          # Más grande que la narración
        color='yellow',        # Color diferente (ej. amarillo o dorado) para resaltar
        font=RUTA_FUENTE,
        stroke_color='black',
        stroke_width=3,
        method='label',
        text_align='center'
    ).with_duration(3)

    def efecto_zoom(t):
        if t < 0.5:
            return 0.8 + (0.4 * t) # Crece rápido al principio
        return 1.0

    sub_frase_central = sub_frase_central.with_effects([
        vfx.Resize(efecto_zoom), # Efecto de escala dinámica
        vfx.FadeIn(0.3),         # Aparece suavemente
        vfx.FadeOut(0.5)         # Desaparece suavemente
    ])

    capa_textos = CompositeVideoClip(
        [
            sub_frase_central.with_position('center'),           # Centro absoluto
            subtitulo.with_position(('center', 1500))        # Forzado a la zona inferior
        ],
        size=(1080, 1920)
    ).with_duration(duracion_escena)

    return capa_textos