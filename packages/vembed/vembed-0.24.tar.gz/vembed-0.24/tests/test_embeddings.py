import unittest
import numpy as np
from vembed import (
    string_to_embedding,
    lists_to_embeddings,
    embeddings_to_proto_format,
    embeddings_to_json_format,
    json_to_embeddings,
)


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

    def test_lists_to_embeddings(self):
        converted_embeddings = lists_to_embeddings(self.list_strings_to_convert)
        self.assertIsNotNone(converted_embeddings)
        expected_number_of_embeddings = len(self.list_strings_to_convert)

        self.assertEqual(len(converted_embeddings), expected_number_of_embeddings)

        for embedding in converted_embeddings:
            self.assertTrue(isinstance(embedding, np.ndarray))

    def test_serialization_to_proto(self):
        embeddings = lists_to_embeddings(self.list_strings_to_convert)
        proto_format = embeddings_to_proto_format(embeddings)
        self.assertIsInstance(proto_format, list)
        self.assertIsNotNone(proto_format)
        # print("Proto Serialized Embedding", proto_format)

    def test_serialization_to_json(self):
        embeddings = lists_to_embeddings(self.list_strings_to_convert)
        json_format = embeddings_to_json_format(embeddings)
        self.assertIsInstance(json_format, str)
        self.assertIsNotNone(json_format)
        # print("JSON Serialized Embedding", json_format)

    def test_serialization_to_proto_and_json(self):
        embeddings = lists_to_embeddings(self.list_strings_to_convert)
        proto_format = embeddings_to_proto_format(embeddings)
        json_format = embeddings_to_json_format(embeddings)

        self.assertIsInstance(proto_format, list)
        self.assertIsInstance(json_format, str)

        # Deserialize and compare
        deserialized_json = json_to_embeddings(json_format)
        self.assertEqual(proto_format, deserialized_json)


if __name__ == "__main__":
    unittest.main()
