# embedding_converter/converter.py

from sentence_transformers import SentenceTransformer
from ..model.transformer_model import get_model

# # Initialize the SentenceTransformer model
# model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")


def string_to_embedding(input_string, model=None):
    """
    Uses paraphrase-multilingual-mpnet-base-v2 to convert a string to a vector embedding.
    """

    if not input_string:
        raise ValueError("Input string cannot be empty.")
    if input_string.isspace():
        raise ValueError("Empty whitespace is not allowed as input.")

    if model is None:
        model = get_model()

    # Encode and return Embedding
    embedding = model.encode(input_string, convert_to_tensor=True)
    return embedding
