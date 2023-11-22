# vembed

<img src="assets/vecembed.jpg" alt="Alt text for the image" width="100%" height="auto" />

<br/>
<br/>


Library to Generate and Serialize Vector Embeddings, extract Semantic Similarity, and create Visualizations from data.

<br/>

```bash
pip install vembed
```


<br/>

<hr/>

### Strings to Embeddings 
<br/>

- Convert a String to a Vector Embedding

```py
from vembed import string_to_embedding

input_string = "This is a test sentence."

embedding = string_to_embedding(input_string)

#  [0.337, 0.143, 0.714 ...]
```
<br/>

- Use Batching to Convert Several Strings to their `Vector Float` Representation *Efficiently*.

```py
from vembed import lists_to_embeddings

embeddings = lists_to_embeddings(["Convert to a List[Float]", "Another String","More Strings!"])

# print(embeddings) [[0.123, 0.456, ...], [0.789, 0.012, ...]]
```
<br/>

### Serialization
<br/>

Functions for Embedding Serialization for Network Transfer.

<br/>

- **Protobuf** Serialization for usage with **gRPC** Services

- **JSON** Serialization for usage with **REST** API's

<br/>

```py
from vembed import lists_to_embeddings, embeddings_to_proto_format, embeddings_to_json_format

embeddings = lists_to_embeddings(["CSV,Row,1,with,some,data" , "CSV,Row,2,with,other,cols"])

# Convert to a Protobuf Serializable Format to send over a gRPC Service
proto_embedding = embeddings_to_proto_format(embeddings)

# Convert to a JSON String for usage with REST API's
json_embedding = embeddings_to_json_format(embeddings)
```

<hr/>

### Similarity 

<br/>


*Semantic Similarity Between Entities*

Extract Insights such as Patterns or Relevancy from your Data.

<br/>

- Calculating Similarity for Entities.

<br/>

```py
from vembed import calculate_similarities, plot_similarities

customer_feedback = ["Loved the recent update","The app is user-friendly",
                    "Facing issues after the update","The new interface is great"]

themes            = ["positive feedback","negative feedback","app interface","app functionality"]

cos_df, dot_df = calculate_similarities(customer_feedback, themes, print_results=True)

# Prints and Returns Results
```

<br/>

```bash
# Results

Cosine Similarities:

Query: 'Loved the recent update'
  Data: 'positive feedback' => Similarity Score: 0.45
  Data: 'app functionality' => Similarity Score: 0.22
  Data: 'app interface'     => Similarity Score: 0.19
  Data: 'negative feedback' => Similarity Score: 0.11

Query: 'Facing issues after the update'
  Data: 'negative feedback' => Similarity Score: 0.31
  Data: 'positive feedback' => Similarity Score: 0.27
  Data: 'app interface'     => Similarity Score: 0.24
  Data: 'app functionality' => Similarity Score: 0.21

Dot Product Similarities:

Query: 'Loved the recent update'
  Data: 'positive feedback' => Similarity Score: 4.51
  Data: 'app functionality' => Similarity Score: 2.06
  Data: 'negative feedback' => Similarity Score: 1.91
  Data: 'app interface'     => Similarity Score: 1.80

Query: 'Facing issues after the update'
  Data: 'negative feedback' => Similarity Score: 2.92
  Data: 'positive feedback' => Similarity Score: 2.51
  Data: 'app interface'     => Similarity Score: 2.07
  Data: 'app functionality' => Similarity Score: 1.82
```

<br/>

- Generating Clean, Beautiful Visualizations from Results.

<br/>


```py
from vembed import plot_similarities

# .... cos_df, dot_df = calculate_similarities(queries, data)

# Create HeapMap for Visualizing Relationships

plot_similarities(cos_df, dot_df, save_path="heatmaps/customer_feedback_similarity.png")

# View and access the Heatmap at /heatmaps/customer_feedback_similarity.png
```
<hr/>

### Cosine and Dot Product Vector Similarity Measures

```bash
@Coefficient Legend

Negative [ - ] - Low Similarity
Zero     [ 0 ] - Orthogonal , No Commonality
Positive [ + ] - Strong Similarity 
```

#### Cosine Similarity 
<br/>

  - Ranges between `-1` and `1`

  - Recommended when the Context and Similarity is important - and Frequency is not important (Magnitude)


- Use Case for Cosine Similarity 
  
  - Here, `Direction` - **thematic orienation** (*climate change, agriculture*) is relevant 

  - `Cosine Similarity` is useful here as we want to find the relevancy of documents discussing similar topics `(direction)` - irrespective of the length of frequency of specific words `(Magnitude)`

<br/>

```py
@Usage

queries = ["Climate change effects on agriculture"]

data =    [
           "Effects of climate change on wheat production",
           "Agriculture in developing countries",
           "Climate change and its impact on global food security",
           "Advances in agricultural technology"
          ]

# Calculate cosine similarities
cos_df, _ = calculate_similarities(queries, data, sorted=True, print_results=True)
```
<br/>

#### Dot Product Similarity 
<br/>

  - Ranges between any Real Number 

  - When both the **Magnitude** and **Direction** of the vectors are important, and we are dealing with vectors in a similar scale.

  - When the **Frequency** *(Magnitude)* as well as the **Direction** *(Relevancy)* is both important.

<br/>

- Use Case for Dot Product 
  
  - **Direction** *(Types of Articles)* and **Magnitude** *(Frequency of Reading Habits)* - both have relevancy.

<br/>

```py
@Usage

user_reading_profile = ["Read many articles on machine learning", "Occasionally reads about space exploration" ]
article_options      = [
                        "Latest trends in machine learning",
                        "Beginner's guide to space travel",
                        "In-depth analysis of neural networks",
                        "Recent discoveries in astronomy"
                       ]

# Calculate dot product similarities

_, dot_df = calculate_similarities(user_reading_profile, article_options, sorted=True, print_results=True)
```
<br/>


- Calculating Similarity

```py
@Usage

queries =  [ 
            "What is the capital of France?", 
            "How is the weather today?"
           ]

data    =  [
             "Paris is the capital of France.",
             "The weather is sunny.",
             "Berlin is the capital of Germany.",
             "It is raining in Berlin."
           ]

# Calculate similarities and Print Results

cos_df, dot_df = calculate_similarities(queries, data, sorted=True, print_results=True)


# Cosine Similarities:
# ...

# Dot Product Similarities:
# ...
```

<hr/>

<br/>

### Visualizations 

<br/>



*Generate Visualizations from Embeddings such as HeatMap Distributions*

<br/>

- Create a visualization to display the Simalirities using a Heatmap.

<br/>

```py
@Usage

customer_feedback = [
                      "Loved the recent update",
                      "The app is user-friendly",
                      "Facing issues after the update",
                      "The new interface is great"
                    ]

themes            = [
                      "positive feedback",
                      "negative feedback",
                      "app interface",
                      "app functionality"
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
<hr/>

<br/>


### Tests

[Latest](https://github.com/kuro337/vembed/tree/main/tests) Test Run

<hr/>

<br/>

#### Build and Run Locally from Source

<br/>


```bash
git clone git@github.com:kuro337/vembed.git

# Create Isolated Virtual Env
python3 -m venv venv
source venv/bin/activate

# Install Deps
pip install -e .

# Run Tests
chmod +x RUN_TESTS.sh
./RUN_TESTS.sh

# Create Dist 
pip3 install build && python3 -m build

# Use Built Dist in any project
pip3 install ./vembed/dist/vembed-0.24-py3-none-any.whl
```
<hr/>

Dependencies
- `sentence_transformers`
- `torch`
- `transformers`
- `pandas`
- `matplotlib`
- `seaborn`

<br/>

<hr/>

<br/>

*Note: vembed GPU Usage can be enabled from using `Nvidia Cuda` and `Torch` if a supported Nvidia Graphics Card is Available.*

<br/>



- Run [CUDA Tests](https://github.com/kuro337/vembed/blob/main/tests/test_cuda.py) from the [vembed Test Suite](https://github.com/kuro337/vembed/tree/main/tests) to check Nvidia System GPU availability

```bash
# Nvidia CUDA and PyTorch Test
python3 tests/test_cuda.py

# Run all Tests
python3 -m unittest discover -s tests -v
```
<br/>

*Checking Virtual or System Environment Deps and Cache Size*

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
