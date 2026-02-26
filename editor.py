from moviepy import (ImageClip, VideoFileClip, AudioFileClip, CompositeAudioClip, 
                     concatenate_videoclips, CompositeVideoClip, ColorClip)
import moviepy.audio.fx as afx
import moviepy.video.fx as vfx
from subtitulador import crear_subtitulos
import os

def crear_video_short(lista_escenas_dicts, nombre_salida="video_final.mp4"):
    orden_vial = [
        "hook", "contextominimo", "hechoanomalo", 
        "escaladadetension","escaladadetension2", "puntoquiebre","puntoquiebre2", "cierreabierto", "cta"
    ]
    
    clips_de_video = []
    duracion_hook = 0
    duracion_total_acumulada = 0

    # 1. ENSAMBLAJE DE ESCENAS VISUALES Y VOCES
    for tipo_buscado in orden_vial:
        escena_data = next((e[tipo_buscado] for e in lista_escenas_dicts if tipo_buscado in e), None)
        if not escena_data: continue
        
        # --- LÓGICA VISUAL (Imagen con Zoom o Video CTA) ---
        if tipo_buscado == "cta":
            path_cta = os.path.join("assets", "cta.mp4")
            if os.path.exists(path_cta):
                # Cargamos el video animado del CTA
                visual_clip = (VideoFileClip(path_cta)
                               .resized(height=1920)
                               .with_duration(escena_data['duracion'])
                               .with_position('center'))
            else:
                visual_clip = ImageClip(escena_data['imagen']).resized(height=1920).with_duration(escena_data['duracion'])
        else:
            # Efecto Zoom Suave para imágenes estáticas
            def zoom_suave(t):
                return 1 + 0.05 * t 

            visual_clip = (ImageClip(escena_data['imagen'])
                .resized(height=1920)
                .with_duration(escena_data['duracion'])
                .with_effects([vfx.Resize(zoom_suave)])
                .with_position('center'))
        
        # Generar Subtítulos y Frase Clave
        sub_clip = crear_subtitulos(escena_data['text'], escena_data['frase'], escena_data['duracion'])
        
        # Combinar visual (Imagen/Video) con el Subtítulo
        escena_visual = CompositeVideoClip([visual_clip, sub_clip], size=(1080, 1920))

        # Audios de la escena (Voz + SFX)
        audio_voz = AudioFileClip(escena_data['audio'])
        lista_audios_escena = [audio_voz]
        
        if escena_data['sonido'] and os.path.exists(escena_data['sonido']):
            sfx = AudioFileClip(escena_data['sonido']).with_start(audio_voz.duration - 0.7)
            lista_audios_escena.append(sfx)

        clip_final_escena = escena_visual.with_audio(CompositeAudioClip(lista_audios_escena))
        clips_de_video.append(clip_final_escena)

        if tipo_buscado == "hook":
            duracion_hook = clip_final_escena.duration
        
        duracion_total_acumulada += clip_final_escena.duration

    # 2. CONCATENACIÓN DEL VIDEO BASE
    # El padding -0.3 crea una transición suave entre clips
    video_base = concatenate_videoclips(clips_de_video, method="compose", padding=-0.3)

    # 3. CAPA DE TEXTURA / VIÑETA (Cine Look)
    # Una capa negra muy tenue en los bordes para dar profundidad
    vignette = (ColorClip(size=(1080, 1920), color=(0,0,0))
                .with_duration(video_base.duration)
                .with_opacity(0.15))

    # 4. GESTIÓN DE LA MÚSICA DE FONDO
    path_bgm = os.path.join("assets", "background.mp3")
    audio_final_list = [video_base.audio]

    if os.path.exists(path_bgm):
        print(f"🎵 Añadiendo música de fondo...")
        duracion_musica = video_base.duration - duracion_hook
        bgm = (AudioFileClip(path_bgm)
                  .subclipped(0, duracion_musica)
                  .with_effects([afx.MultiplyVolume(0.65), afx.AudioFadeIn(1.0)]) 
                  .with_start(duracion_hook))
        audio_final_list.append(bgm)

    # 5. COMPOSICIÓN FINAL CON EFECTOS DE CIERRE
    video_final = CompositeVideoClip([video_base, vignette])
    video_final = video_final.with_audio(CompositeAudioClip(audio_final_list))

    # Efecto de fundido a negro al final de todo el video
    video_final = video_final.with_effects([
        vfx.FadeOut(1.5),
        afx.AudioFadeOut(1.5)
    ])

    # 6. RENDER FINAL
    video_final.write_videofile(nombre_salida, fps=24, codec="libx264", audio_codec="aac")