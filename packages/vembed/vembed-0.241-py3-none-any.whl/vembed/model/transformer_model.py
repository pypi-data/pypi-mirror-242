from typing import Optional, Dict
from xmlrpc.client import Boolean

from sentence_transformers import SentenceTransformer

_model = None


def get_model(model_name: str = "paraphrase-multilingual-mpnet-base-v2"):
    """
    Loads and returns a SentenceTransformer model.
    Uses a singleton pattern to ensure the model is loaded only once.
    """
    global _model
    if _model is None:
        _model = SentenceTransformer(model_name)
    return _model


def get_model_embedding_dimensionality(
    model: Optional[SentenceTransformer] = None, debug: Boolean = True
) -> int:
    """
    Returns the dimensionality of the embeddings produced by the model.
    """
    if model is None:
        model = get_model()

    dimensionality = model.get_sentence_embedding_dimension()
    if debug:
        print("Dimensionality of the model's embeddings:", dimensionality)
    return dimensionality


def get_model_info(
    model: Optional[SentenceTransformer] = None, debug: Boolean = True
) -> Dict[str, any]:
    """
    Returns information about the SentenceTransformer model, including its name,
    dimensionality, and any other relevant attributes.
    """
    if model is None:
        model = get_model()

    model_info = {
        "model_name": model.__class__.__name__,
        "embedding_dimensionality": model.get_sentence_embedding_dimension(),
    }

    if debug:
        for key, value in model_info.items():
            print(f"{key}: {value}")

    return model_info
