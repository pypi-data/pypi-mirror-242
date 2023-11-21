# from .model.transformer_model import get_model

from .string_to_vector.mpnet_paraphrase import string_to_embedding
from .similarity.get_similarity import (
    calculate_similarities,
    print_formatted_results,
    plot_similarities,
)
