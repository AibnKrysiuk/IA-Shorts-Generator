import os
from mutagen.mp3 import MP3

class Escena:
    def __init__(self, texto, prompt_img, frase, tipo):
        self.tipo = tipo.lower().replace(" ", "")
        self.text = texto
        self.prompt_temp = prompt_img  # Usado para la generación
        self.frase = frase
        self.audio = f"audios/{self.tipo}.mp3"
        self.imagen = f"imagenes/{self.tipo}.jpg"
        self.sonido = None
        self.duracion = 0

    def calcular_metadatos(self):
        """Calcula la duración real basada en el archivo de audio generado."""
        duracion_voz = 0
        if os.path.exists(self.audio):
            try:
                audio_info = MP3(self.audio)
                duracion_voz = audio_info.info.length
            except Exception as e:
                print(f"Error leyendo audio {self.audio}: {e}")
        
        # Lógica de sonidos y duraciones según el tipo
        self._aplicar_reglas_especificas(duracion_voz)

    def _aplicar_reglas_especificas(self, d_voz):
        # Configuración por defecto
        self.duracion = d_voz
        
        if self.tipo == "hook":
            self.sonido = "assets/BoomInicial.mp3"
            self.duracion = d_voz 
            
        elif self.tipo in ["contextominimo", "cierreabierto"]:
            if d_voz < 7:
                self.duracion = d_voz + 0.5
                
        elif self.tipo in ["hechoanomalo", "escaladadetension", "puntodequiebre"]:
            if d_voz < 9:
                self.duracion = d_voz + 0.5
            
            if self.tipo == "escaladadetension":
                self.sonido = "Assets/Tension.mp3"
            elif self.tipo == "puntodequiebre":
                self.sonido = "Assets/BoomMenor.mp3"
                
        elif self.tipo == "cta":
            self.duracion = d_voz + 0.5
            self.sonido = "Assets/cierre.mp3"

    def to_dict(self):
        """Devuelve la representación que pediste."""
        return {
            self.tipo: {
                "text": self.text,
                "audio": self.audio,
                "imagen": self.imagen,
                "frase": self.frase,
                "tipo": self.tipo,
                "duracion": self.duracion,
                "sonido": self.sonido
            }
        }