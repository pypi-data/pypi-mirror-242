from typing import Optional, Union, Tuple, List
import numpy as np
import json

from sentence_transformers import SentenceTransformer
from ..model.transformer_model import get_model


def string_to_embedding(
    input_string: str,
    model: Optional[SentenceTransformer] = None,
    serialization_format: Optional[str] = None,
) -> Union[np.ndarray, List[float]]:
    """
    Uses a SentenceTransformer model to convert a string to a vector embedding.

    Args:
        `input_string` `(str)`: The string to convert into an embedding.
        `model` `(SentenceTransformer, optional)`: The SentenceTransformer model to use.
                                                Defaults to None, which loads the default model.
        `serialization_format` `(str, optional)`: The format for serialization
                                              ('proto' for gRPC, None for numpy array).
                                              Defaults to a numpy array.

    Returns:
        `Union[np.ndarray, List[float]]`: The embedding as a numpy array or a list of floats.

    @Usage
    ```
    embedding = string_to_embedding("Hello World")
    print(embedding)  # Output: [0.123, 0.456, ...]
    ```
    """

    if not input_string:
        raise ValueError("Input string cannot be empty.")
    if input_string.isspace():
        raise ValueError("Empty whitespace is not allowed as input.")

    if model is None:
        model = get_model()

    # Encode and return Embedding
    embedding = model.encode(input_string, convert_to_tensor=True)
    if serialization_format == "proto":
        return embeddings_to_proto_format(embedding)
    return embedding


def lists_to_embeddings(
    strings: List[str],
    model: Optional[SentenceTransformer] = None,
    serialization_format: Optional[str] = None,
) -> Union[np.ndarray, List[List[float]]]:
    """
    Batched Operation to Convert a List of Strings to a List of Embeddings.

    Args:
        `strings` `(List[str])`: A list of strings to convert into embeddings.
        `model` `(SentenceTransformer, optional)`: The SentenceTransformer model to use.
                                                Defaults to None, which loads the default model.
        `serialization_format` `(str, optional)`: The format for serialization
                                              ('proto' for gRPC, None for numpy array).
                                              Defaults to a numpy array

    Returns:
        `Union[np.ndarray, List[List[float]]]`: The embeddings as a numpy array or a list of lists of floats.

    @Usage
    ```
    embeddings = lists_to_embeddings(["Convert this Sentence", "And this Sentence","And More Sentences"])
    print(embeddings)  # Output: [[0.123, 0.456, ...], [0.789, 0.012, ...]]
    ```
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
    if serialization_format == "proto":
        return embeddings_to_proto_format(embeddings)
    return embeddings.cpu().numpy()


def embeddings_to_proto_format(embeddings: np.ndarray) -> List[List[float]]:
    """
    Converts numpy array embeddings to a list of lists format suitable for gRPC transmission.

    Args:
        embeddings (np.ndarray): The numpy array containing the embeddings.

    Returns:
        List[List[float]]: The embeddings in a list of lists format.

    Example:
    ```
    proto_format_embeddings = embeddings_to_proto_format(np.array([[1.0, 2.0], [3.0, 4.0]]))
    print(proto_format_embeddings)  # Output: [[1.0, 2.0], [3.0, 4.0]]
    ```
    """
    return embeddings.tolist()


def embeddings_to_json_format(embeddings: np.ndarray) -> str:
    """
    Converts numpy array embeddings to a JSON string format suitable for HTTP transmission or storage.

    Args:
        embeddings (np.ndarray): The numpy array containing the embeddings.

    Returns:
        str: The embeddings in JSON string format.

    Example:
    ```
    json_format_embeddings = embeddings_to_json_format(np.array([[1.0, 2.0], [3.0, 4.0]]))
    print(json_format_embeddings)  # Output: '[[1.0, 2.0], [3.0, 4.0]]'
    ```
    """
    # Convert numpy array to list of lists for JSON serialization
    list_of_lists = embeddings.tolist()

    # Serialize to JSON
    return json.dumps(list_of_lists)


def json_to_embeddings(json_string: str) -> List[List[float]]:
    """
    Converts a JSON string back into a list of lists of embeddings.

    Args:
        json_string (str): The JSON string containing the embeddings.

    Returns:
        List[List[float]]: The embeddings as a list of lists.

    Example:
    ```
    embeddings = json_to_embeddings('[[1.0, 2.0], [3.0, 4.0]]')
    print(embeddings)  # Output: [[1.0, 2.0], [3.0, 4.0]]
    ```
    """
    # Deserialize from JSON
    return json.loads(json_string)
