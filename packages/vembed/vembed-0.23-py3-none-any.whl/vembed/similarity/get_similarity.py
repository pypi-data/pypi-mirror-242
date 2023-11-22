from sentence_transformers import SentenceTransformer, util
import torch
import pandas as pd

from ..model.transformer_model import get_model


def calculate_similarities(
    queries, data, model=None, sorted=False, print_results=False
):
    """
    @Usage
    ```
    queries = ["What is the capital of France?", "How is the weather today?"]
        data = [
            "Paris is the capital of France.",
            "The weather is sunny.",
            "Berlin is the capital of Germany.",
            "It is raining in Berlin.",
        ]

        # Calculate similarities and Print Results
        cos_df, dot_df = calculate_similarities(
            queries, data, sorted=True, print_results=True
        )
    ```
    Calculates the cosine and dot product similarities between each query and each data point.

    Parameters:
    - queries (list of str): List of query strings.
    - data (list of str): List of data strings.
    - model (SentenceTransformer, optional): The SentenceTransformer model to use.
    - sorted (bool, optional): If True, sorts the results in descending order. Defaults to False.
    - print_results (bool, optional): If True, prints the resulting similarity data frames. Defaults to False.

    @Returns -> (cos_df , dot_df)
    @cos_df -> DataFrame of Cosine Similarities
    @dot_df -> DataFrame of Dot Product Similarities
    - tuple: A tuple containing two pandas DataFrames with cosine and dot product similarities.
    """
    if model is None:
        model = get_model()

    query_embeddings = model.encode(queries, convert_to_tensor=True)
    data_embeddings = model.encode(data, convert_to_tensor=True)

    cos_similarities = util.cos_sim(query_embeddings, data_embeddings).cpu().numpy()
    dot_similarities = util.dot_score(query_embeddings, data_embeddings).cpu().numpy()

    cos_df = pd.DataFrame(cos_similarities, index=queries, columns=data)
    dot_df = pd.DataFrame(dot_similarities, index=queries, columns=data)

    if print_results:
        print_formatted_results(cos_df, "Cosine Similarities", sorted=sorted)
        print_formatted_results(dot_df, "Dot Product Similarities", sorted=sorted)

    return cos_df, dot_df


def print_formatted_results(df, title, sorted=False):
    """
    - Using to print Results

    ```
    cos_df, dot_df = calculate_similarities(queries, data)
    print_formatted_results(cos_df, "Cosine Similarities")
    print_formatted_results(dot_df, "Dot Product Similarities")
    ```
    """
    print(f"\n{title}:")
    for query in df.index:
        print(f"\nQuery: '{query}'")
        sorted_scores = df.loc[query].sort_values(ascending=False)  # Sort scores
        for data_point, score in sorted_scores.items():
            print(f"  Data: '{data_point}' => Similarity Score: {score:.2f}")


# Function to plot the similarities (optional for users to use)
def plot_similarities(cos_df, dot_df, save_path: str = None):
    """
    Plotting function for visualizing the similarities. Requires matplotlib and seaborn.
    """
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Check if both dataframes are None
    if cos_df is None and dot_df is None:
        raise ValueError("At least one of cos_df or dot_df must be provided")

    num_plots = 0
    if cos_df is not None:
        num_plots += len(cos_df.index)
    if dot_df is not None:
        num_plots += len(dot_df.index)

    fig, ax = plt.subplots(num_plots, 1, figsize=(10, 5 * num_plots))
    ax = ax if num_plots > 1 else [ax]  # Ensure ax is always a list

    plot_idx = 0
    if cos_df is not None:
        for query in cos_df.index:
            sns.heatmap(
                data=cos_df.loc[[query]].T, annot=True, ax=ax[plot_idx], fmt=".2f"
            )
            ax[plot_idx].set_title(f"Cosine Sim - {query}")
            plot_idx += 1

    if dot_df is not None:
        for query in dot_df.index:
            sns.heatmap(
                data=dot_df.loc[[query]].T, annot=True, ax=ax[plot_idx], fmt=".2f"
            )
            ax[plot_idx].set_title(f"Dot Product Sim - {query}")
            plot_idx += 1

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.5, hspace=0.5)
    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()
