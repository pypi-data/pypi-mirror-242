# python3 tests/test_converter.py

# python -m unittest discover -s tests -v


import unittest

from vembed import string_to_embedding


class TestConverter(unittest.TestCase):
    def test_string_to_embedding_non_empty(self):
        input_string = "This is a test sentence."
        embedding = string_to_embedding(input_string)
        self.assertIsNotNone(embedding)

    def test_string_to_embedding_empty(self):
        input_string = ""
        with self.assertRaisesRegex(ValueError, "Input string cannot be empty."):
            string_to_embedding(input_string)

    def test_string_to_embedding_whitespace(self):
        input_string = "   "
        with self.assertRaisesRegex(
            ValueError, "Empty whitespace is not allowed as input."
        ):
            string_to_embedding(input_string)


if __name__ == "__main__":
    unittest.main()
