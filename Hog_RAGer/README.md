# Question Answering System using TF-IDF and Pre-trained Transformer Model

This repository contains a simple question-answering system that uses TF-IDF for evidence retrieval from a corpus and a pre-trained transformer model (T5-small) for generating answers based on the retrieved evidence. The project is designed to match queries to documents in a corpus and generate a concise answer based on the top-matching evidence.

## Table of Contents

- [Introduction](#introduction)
- [Workflow](#workflow)
- [Installation](#installation)

## Introduction

This project combines two important techniques for building a question-answering system:
1. **TF-IDF (Term Frequency-Inverse Document Frequency)**: Used for retrieving relevant documents from a large corpus.
2. **Pre-trained Transformer Model (T5-small)**: Utilized for generating answers based on the context of the retrieved documents.

The system takes a query as input, retrieves relevant evidence from a pre-built corpus, and generates an answer using the pre-trained model. The corpus consists of multiple documents with their associated metadata.

## Workflow

### 1. Evidence Retrieval using TF-IDF
- The corpus is loaded from a `corpus.json` file, and we extract the textual content and metadata.
- A **TF-IDF vectorizer** is used to vectorize the text in the corpus.
- When a query is input, we compute the **cosine similarity** between the query and the corpus texts to identify the top 3 most relevant documents.
- These top documents serve as the evidence for answering the query.

### 2. Answer Generation using Pre-trained Model
- A pre-trained transformer model (**T5-small**) is loaded to generate answers.
- The top 3 relevant documents from the corpus are concatenated and provided as context to the model along with the query.
- The model then generates an answer based on the given query and the supporting evidence.

### 3. Output
- The system outputs the following:
  - The original query.
  - The generated answer.
  - The top 3 pieces of evidence (with their metadata) that were used to generate the answer.

## Installation

To run the project locally, follow these steps:

1. Clone this repository:
  ```bash
  git clone https://github.com/BhavikOstwal/AI-ML-Hackathon.git
  cd AI-ML-Hackathon/Hog_RAGer
  ```
  
   
2. Install the required Python packages:

- Ensure you have Python installed. This project was developed with Python `3.12.2`

- You can install the required dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```
3.  Run the script:
```
python complete_pipeline.py
```
### ENJOY 😎😎