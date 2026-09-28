def _validate_key(key: int) -> None:
    if key <= 0:
        raise ValueError("Ключ должен быть положительным целым числом.")


def encrypt(text: str, key: int) -> str:
    """Столбцовая транспозиция: запись по строкам, чтение по столбцам."""
    _validate_key(key)
    if not text:
        return ""

    columns = key
    rows = (len(text) + columns - 1) // columns
    result = []

    for column in range(columns):
        for row in range(rows):
            index = row * columns + column
            if index < len(text):
                result.append(text[index])

    return "".join(result)


def decrypt(text: str, key: int) -> str:
    """Восстанавливает исходный порядок символов."""
    _validate_key(key)
    if not text:
        return ""

    columns = key
    rows = (len(text) + columns - 1) // columns
    short_columns = columns * rows - len(text)
    column_lengths = [rows] * columns

    for column in range(columns - short_columns, columns):
        if column >= 0:
            column_lengths[column] -= 1

    table = [""] * columns
    position = 0
    for column in range(columns):
        length = column_lengths[column]
        table[column] = text[position:position + length]
        position += length

    result = []
    for row in range(rows):
        for column in range(columns):
            if row < len(table[column]):
                result.append(table[column][row])

    return "".join(result)
