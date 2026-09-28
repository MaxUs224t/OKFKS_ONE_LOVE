RUSSIAN = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ENGLISH = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def shift_text(text: str, key: int, decrypt: bool = False) -> str:
    """Шифр Цезаря для русского и английского текста."""
    if not isinstance(key, int):
        raise ValueError("Ключ Цезаря должен быть целым числом.")
    if decrypt:
        key = -key

    result = []
    for char in text:
        alphabet = None
        if char.upper() in RUSSIAN:
            alphabet = RUSSIAN
        elif char.upper() in ENGLISH:
            alphabet = ENGLISH

        if alphabet is None:
            result.append(char)
            continue

        index = alphabet.index(char.upper())
        new_char = alphabet[(index + key) % len(alphabet)]
        result.append(new_char if char.isupper() else new_char.lower())

    return "".join(result)
