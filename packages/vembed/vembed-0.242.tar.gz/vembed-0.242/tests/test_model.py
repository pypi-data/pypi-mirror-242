from doctest import debug
import unittest
from sentence_transformers import SentenceTransformer
from vembed import get_model_embedding_dimensionality, get_model_info


class TestModelEmbeddingDimensionality(unittest.TestCase):
    def test_embedding_dimensionality(self):
        model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
        dimensionality = get_model_embedding_dimensionality(model, debug=False)
        self.assertEqual(dimensionality, 768)
        self.assertIsInstance(dimensionality, int)
        self.assertTrue(dimensionality > 0)

    def test_get_model_info(self):
        model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
        model_info = get_model_info(model, debug=False)
        self.assertIsInstance(model_info, dict)
        self.assertTrue(len(model_info) > 0)
        self.assertTrue("model_name" in model_info)
        self.assertTrue("embedding_dimensionality" in model_info)
        self.assertEqual(model_info["model_name"], "SentenceTransformer")
        self.assertIsInstance(model_info["embedding_dimensionality"], int)
        self.assertTrue(model_info["embedding_dimensionality"] > 0)

    def test_default_model_info(self):
        model_info = get_model_info(debug=False)
        self.assertIsInstance(model_info, dict)
        self.assertTrue(len(model_info) > 0)
        self.assertTrue("model_name" in model_info)
        self.assertTrue("embedding_dimensionality" in model_info)
        self.assertEqual(model_info["model_name"], "SentenceTransformer")
        self.assertIsInstance(model_info["embedding_dimensionality"], int)
        self.assertTrue(model_info["embedding_dimensionality"] > 0)


if __name__ == "__main__":
    unittest.main()
