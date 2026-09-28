import unittest

from cipher.caesar import shift_text
from cipher.vigenere import transform_text
from cipher.transposition import encrypt, decrypt


class CipherTests(unittest.TestCase):
    def test_caesar_round_trip_russian(self):
        text = "Привет, мир! 123"
        coded = shift_text(text, 3)
        self.assertEqual(shift_text(coded, 3, True), text)

    def test_caesar_round_trip_english(self):
        text = "Hello, World!"
        coded = shift_text(text, 5)
        self.assertEqual(shift_text(coded, 5, True), text)

    def test_caesar_negative_key(self):
        text = "ABC"
        self.assertEqual(shift_text(shift_text(text, -3), -3, True), text)

    def test_vigenere_russian(self):
        text = "ПРИВЕТ"
        coded = transform_text(text, "СЕКРЕТ")
        self.assertEqual(transform_text(coded, "СЕКРЕТ", True), text)

    def test_vigenere_english(self):
        text = "Hello World"
        coded = transform_text(text, "SECRET")
        self.assertEqual(transform_text(coded, "SECRET", True), text)

    def test_vigenere_mixed_text(self):
        text = "Привет, Hello! 123"
        coded = transform_text(text, "КЛЮЧ")
        self.assertEqual(transform_text(coded, "КЛЮЧ", True), text)

    def test_transposition_round_trip(self):
        text = "Привет, Hello! 123"
        for key in (1, 2, 3, 4, 7, 20):
            self.assertEqual(decrypt(encrypt(text, key), key), text)

    def test_transposition_keeps_symbols(self):
        text = "A-B C!"
        self.assertEqual(decrypt(encrypt(text, 3), 3), text)

    def test_empty_text(self):
        self.assertEqual(encrypt("", 4), "")
        self.assertEqual(decrypt("", 4), "")

    def test_invalid_keys(self):
        with self.assertRaises(ValueError):
            shift_text("ABC", "x")
        with self.assertRaises(ValueError):
            transform_text("ABC", "123")
        with self.assertRaises(ValueError):
            encrypt("ABC", 0)


if __name__ == "__main__":
    unittest.main()
