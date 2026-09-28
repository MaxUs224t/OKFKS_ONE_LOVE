RUSSIAN = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ENGLISH = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _key_shifts(key: str):
    shifts = []
    for char in key:
        upper = char.upper()
        if upper in RUSSIAN:
            shifts.append(RUSSIAN.index(upper))
        elif upper in ENGLISH:
            shifts.append(ENGLISH.index(upper))
    return shifts


def transform_text(text: str, key: str, decrypt: bool = False) -> str:
    """Шифр Виженера. Ключ содержит только буквы."""
    shifts = _key_shifts(key)
    if not shifts:
        raise ValueError("Ключ должен содержать хотя бы одну букву.")

    result = []
    key_index = 0

    for char in text:
        upper = char.upper()
        if upper not in RUSSIAN and upper not in ENGLISH:
            result.append(char)
            continue

        alphabet = RUSSIAN if upper in RUSSIAN else ENGLISH
        shift = shifts[key_index % len(shifts)]
        if decrypt:
            shift = -shift

        index = alphabet.index(upper)
        new_char = alphabet[(index + shift) % len(alphabet)]
        result.append(new_char if char.isupper() else new_char.lower())
        key_index += 1

    return "".join(result)
