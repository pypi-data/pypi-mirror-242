import unittest
import numpy as np
from vembed import string_to_embedding, strings_to_embeddings


class TestStringToEmbedding(unittest.TestCase):
    """
    @TableTests

    input_string | should_pass  | expected_output
    ""           | False        | ValueError
    " "          | False        | ValueError
    "  "         | False        | ValueError
    "This is a test sentence." | True | Embedding
    "Another test string." | True | Embedding

    """

    test_cases = [
        ("This is a test sentence.", True),
        ("", False),
        ("Another test string.", True),
    ]

    list_strings_to_convert = [
        "This is a test sentence.",
        "Another test string.",
        "More Sentences",
        "John Daley is a Good Actor",
        "Bernie Sanders Politico Should Listen",
        "Michael Cera in SuperBad",
    ]

    def test_various_inputs(self):
        for input_string, should_pass in self.test_cases:
            with self.subTest(input_string=input_string):
                if should_pass:
                    self.assertIsNotNone(string_to_embedding(input_string))
                else:
                    with self.assertRaises(ValueError):
                        string_to_embedding(input_string)

    def test_list_strings_to_embeddings(self):
        converted_embeddings = strings_to_embeddings(self.list_strings_to_convert)
        # print(converted_embeddings)
        self.assertIsNotNone(converted_embeddings)
        expected_number_of_embeddings = len(self.list_strings_to_convert)

        # Check if the number of embeddings matches the number of input strings
        self.assertEqual(len(converted_embeddings), expected_number_of_embeddings)

        # Check if each item in embeddings is a NumPy array
        for embedding in converted_embeddings:
            self.assertTrue(isinstance(embedding, np.ndarray))


if __name__ == "__main__":
    unittest.main()
