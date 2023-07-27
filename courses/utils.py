import base64
import json
import uuid

from django.conf import settings


def save_audio_file(body) -> str:
    data = json.loads(body.decode('ascii'))
    audio = data['audio']
    file_name = f'record_{str(uuid.uuid4())[:8]}.mp3'
    path = f'{settings.MEDIA_ROOT}/audio_records/{file_name}'

    with open(path, 'wb') as f:
        decode_string = base64.b64decode(audio)
        f.write(decode_string)

    return 'audio_records/' + file_name
