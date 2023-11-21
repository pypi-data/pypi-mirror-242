# vembed

![Alt text for the image](assets/vembed.jpg)


Library to generate Embeddings and Extract Semantic Similarity from Data.

<hr/>

#### String to Embeddings 

- Convert Strings to Vector Embeddings



```py
@Usage

from embedder import string_to_embedding

input_string = "This is a test sentence."
embedding = string_to_embedding(input_string)
print(embedding)
```
<hr/>

### Similarity 

Extracting Similarity Between Entities

```bash
Negative - Low Similarity
Zero     - Orthogonal - no commonality
Positive - Strong Similarity 
```

#### Cosine Similarity 

  - Ranges between `-1` and `1`

  - Recommended when the Context and Similarity is important - and Frequency is not important (Magnitude)


- Use Case for Cosine Similarity 
  
  - Here, `Direction` - **thematic orienation** (*climate change, agriculture*) is relevant 

  - `Cosine Similarity` is useful here as we want to find the relevancy of documents discussing similar topics `(direction)` - irrespective of the length of frequency of specific words `(Magnitude)`


```py
@Usage

queries = ["Climate change effects on agriculture"]
data = [
    "Effects of climate change on wheat production",
    "Agriculture in developing countries",
    "Climate change and its impact on global food security",
    "Advances in agricultural technology"
]

# Calculate cosine similarities
cos_df, _ = calculate_similarities(queries, data, sorted=True, print_results=True)
```

#### Dot Product Similarity 

  - Ranges between any Real Number 

  - When both the `magnitude` and `direction` of the vectors are important, and you are dealing with vectors in a similar scale.

  - When the `Frequency` (Magnitude) as well as the `Direction` (Relevancy) is both important.

- Use Case for Dot Product 
  
  - `Direction` (Types of Articles) and `Magnitude` (Frequency of Reading Habits) are both important.

```py
@Usage

user_reading_profile = ["Read many articles on machine learning", "Occasionally reads about space exploration"]
article_options = [
    "Latest trends in machine learning",
    "Beginner's guide to space travel",
    "In-depth analysis of neural networks",
    "Recent discoveries in astronomy"
]

# Calculate dot product similarities
_, dot_df = calculate_similarities(user_reading_profile, article_options, sorted=True, print_results=True)


```


- Calculating Similarity

```py
@Usage

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

### Visualization for Relevance 

<hr/>

- Create a visualization to display the Simalirities using a Heatmap.

```py
@Usage

customer_feedback = [
    "Loved the recent update",
    "The app is user-friendly",
    "Facing issues after the update",
    "The new interface is great",
]
themes = [
    "positive feedback",
    "negative feedback",
    "app interface",
    "app functionality",
]

# Heatmap of Both Cosine and Dot Product
cos_df, dot_df = calculate_similarities(customer_feedback, themes, sorted=True)
plot_similarities(cos_df, dot_df, save_path="customer_feedback_similarity.png")

# Heatmap of Only Cosine Similarity
cos_df, _ = calculate_similarities(customer_feedback, themes, sorted=True)
plot_similarities(cos_df, None, save_path="customer_feedback_similarity.png")

# Heatmap of Only Dot Product Similarity
_, dot_df = calculate_similarities(customer_feedback, themes, sorted=True)
plot_similarities(None, dot_df, save_path="customer_feedback_similarity.png")

# View customer_feedback_similarity.png to see the Heatmap
```

<hr/>

Dependencies
- `sentence_transformers`
- `torch`
- `transformers`
- `pandas`
- `matplotlib`
- `seaborn`

*Note: This package uses `Nvidia Cuda` and `Torch`.*

```bash
# Check Disk Allocation for Packages 
du -h venv | sort -hr | head -n 10

2.8G    venv/lib/python3.11/site-packages/nvidia
1.4G    venv/lib/python3.11/site-packages/torch
1.3G    venv/lib/python3.11/site-packages/torch/lib
1.2G    venv/lib/python3.11/site-packages/nvidia/cudnn/lib
1.2G    venv/lib/python3.11/site-packages/nvidia/cudnn
596M    venv/lib/python3.11/site-packages/nvidia/cublas

# Checking System Cache

# Show pip cache location
pip cache dir # /home/user/.cache/pip

# Getting Top Folders from Cache by Size
du -h /home/user/.cache/pip | sort -hr | head -n 10

# Remove Cached Files
pip cache purge 

# Cached Files
pip cache list

# Installing Packages without Cache
pip install --no-cache-dir <package_name>
```
<hr/>

Author: [kuro337](https://github.com/kuro337)
