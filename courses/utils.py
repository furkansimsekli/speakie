import base64
import io
import json
import uuid

from django.conf import settings
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account


def save_audio_file(body) -> str:
    data = json.loads(body.decode('ascii'))
    audio = data['audio']
    file_name = f'record_{str(uuid.uuid4())[:8]}.mp3'
    path = f'{settings.MEDIA_ROOT}/audio_records/{file_name}'

    with open(path, 'wb') as f:
        decode_string = base64.b64decode(audio)
        f.write(decode_string)

    return 'audio_records/' + file_name


def speech_to_text(audio_file: str, language: str):
    client_file = 'sa_speakie.json'
    credentials = service_account.Credentials.from_service_account_file(client_file)
    client = speech.SpeechClient(credentials=credentials)

    with io.open(audio_file, 'rb') as f:
        content = f.read()
        audio = speech.RecognitionAudio({'content': content})

    config = speech.RecognitionConfig({
        'encoding': speech.RecognitionConfig.AudioEncoding.MP3,
        'sample_rate_hertz': 24000,
        'language_code': language,
        'audio_channel_count': 1
    })

    response = client.recognize(config=config, audio=audio)
    transcription_paragraph = ''

    for result in response.results:
        transcription_paragraph += result.alternatives[0].transcript.strip() + ' '

    return transcription_paragraph
