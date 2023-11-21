from setuptools import setup, find_packages

setup(
    name="vembed",
    version="0.2",
    author="kuro337",
    description="Package providing methods to create Vector Embeddings from Strings",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kuro337/vembed",
    packages=find_packages(),
    install_requires=[
        "sentence_transformers",
        "torch",
        "transformers",
        "pandas",
        "matplotlib",
        "seaborn",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

# pip3 install -e .
