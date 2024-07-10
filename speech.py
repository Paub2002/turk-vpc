import os
from pydub import AudioSegment
from pydub.playback import play
from google.cloud import texttospeech

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "turk-vpc/text-to-speech.json"
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "text-to-speech.json"

client = texttospeech.TextToSpeechClient()

voice = texttospeech.VoiceSelectionParams(
        language_code = "es-ES",
        name = "es-ES-Neural2-F"
    )

audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

def text_to_speech(text):
    # Eliminar los asteriscos
    texto_sin_asteriscos = text.replace("*", "")
    text_block = texto_sin_asteriscos
    synthesis_input = texttospeech.SynthesisInput(text = text_block)

    response = client.synthesize_speech(
        input = synthesis_input, voice=voice, audio_config=audio_config
    )

    with open("output.mp3", "wb") as output:
        output.write(response.audio_content)
        print('Audio content written  to file "output.mp3"')

    # Carga el archivo MP3
    audio = AudioSegment.from_mp3('output.mp3')

    # Reproduce el archivo MP3
    play(audio)

