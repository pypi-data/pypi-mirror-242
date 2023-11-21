import unittest
from vembed import string_to_embedding


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

    def test_various_inputs(self):
        for input_string, should_pass in self.test_cases:
            with self.subTest(input_string=input_string):
                if should_pass:
                    self.assertIsNotNone(string_to_embedding(input_string))
                else:
                    with self.assertRaises(ValueError):
                        string_to_embedding(input_string)


if __name__ == "__main__":
    unittest.main()
