from sentence_transformers import SentenceTransformer

_model = None  # This will hold the singleton instance of the model


def get_model(model_name="paraphrase-multilingual-mpnet-base-v2"):
    """
    Loads and returns a SentenceTransformer model.
    Uses a singleton pattern to ensure the model is loaded only once.
    """
    global _model
    if _model is None:
        _model = SentenceTransformer(model_name)
    return _model
