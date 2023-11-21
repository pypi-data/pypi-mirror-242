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


def strings_to_embeddings(strings, model=None):
    """
    Converts a list of strings to a list of vector embeddings using the specified model.
    """

    if not strings:
        raise ValueError("Input list cannot be empty.")

    if any(s.isspace() or not s for s in strings):
        raise ValueError(
            "Strings in the input list cannot be empty or whitespace only."
        )

    if model is None:
        model = get_model()

    # Encode and return list of embeddings
    embeddings = model.encode(strings, convert_to_tensor=True)
    return embeddings.cpu().numpy()  # Convert to numpy array if needed
