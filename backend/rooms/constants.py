from typing import Dict, List

MOOD_ANY = {
    'key': 'any',
    'name': 'No Mood'
}

MOOD_HAPPY = {
    'key': 'happy',
    'name': 'Happy'
}

MOOD_SAD = {
    'key': 'sad',
    'name': 'Sad'
}


def moods() -> List[Dict[str, str]]:
    return [MOOD_ANY, MOOD_HAPPY, MOOD_SAD]
