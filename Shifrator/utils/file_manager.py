from pathlib import Path


def read_text_file(path: str) -> str:
    """Читаем TXT только как UTF-8."""
    return Path(path).read_text(encoding="utf-8")


def write_text_file(path: str, text: str) -> None:
    """Сохраняем TXT в UTF-8."""
    Path(path).write_text(text, encoding="utf-8")
