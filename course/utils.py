import base64
import io
import json
import uuid

from django.conf import settings
from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account

from . import constants


def save_audio_file(body) -> str:
    data = json.loads(body.decode('ascii'))
    audio = data['audio']
    file_name = f'record_{str(uuid.uuid4())[:8]}.mp3'
    path = f'{settings.MEDIA_ROOT}/audio_records/{file_name}'

    with open(path, 'wb') as f:
        decode_string = base64.b64decode(audio)
        f.write(decode_string)

    return 'audio_records/' + file_name


def speech_to_text(audio_file: str, language: str) -> str:
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


def levenshtein(source: str, target: str) -> int:
    len1, len2 = len(source), len(target)
    dp = [[0 for _ in range(len2 + 1)] for _ in range(len1 + 1)]

    for i in range(len1 + 1):
        dp[i][0] = i

    for j in range(len2 + 1):
        dp[0][j] = j

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if source[i - 1] == target[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[len1][len2]


def normalize(str1: str, str2: str, ignored_set=None, remove_whitespace=False) -> (str, str):
    if ignored_set is None:
        ignored_set = constants.IGNORED_SET

    for ignored in ignored_set:
        str1 = str1.replace(ignored, '')
        str2 = str2.replace(ignored, '')

    if remove_whitespace:
        str1 = str1.replace(' ', '')
        str2 = str2.replace(' ', '')

    str1 = str1.lower().strip()
    str2 = str2.lower().strip()
    return str1, str2


def calculate_accuracy(original: str, transcript: str) -> float:
    n_original, n_transcript = normalize(original, transcript)
    length = len(n_original)
    penalty = levenshtein(n_original, n_transcript)
    return (length - penalty) / length
