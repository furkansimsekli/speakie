import math
import uuid

import requests
from django.conf import settings


def calculate_level(score: int) -> int:
    return math.ceil(math.log(1 + 0.005 * score, 1.5))


def save_image_from_google(image_url: str):
    res = requests.get(image_url)
    file_name = f'googlepic_{str(uuid.uuid4())[:8]}.jpg'

    with open(f'{settings.MEDIA_ROOT}/profile_pictures/{file_name}', 'wb') as f:
        f.write(res.content)

    return 'profile_pictures/' + file_name
