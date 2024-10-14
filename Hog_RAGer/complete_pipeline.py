import json
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the corpus and train datasets
with open("data/corpus.json", "r") as corpus_file:
    corpus = json.load(corpus_file)

with open("data/train.json", "r") as train_file:
    train_data = json.load(train_file)

# Extract text and metadata from corpus for TF-IDF
corpus_texts = [doc['body'] for doc in corpus]
corpus_metadata = [{key: doc[key] for key in ['title', 'author', 'url', 'source', 'category', 'published_at']} for doc in corpus]

# Tokenize and fit TF-IDF on the corpus
vectorizer = TfidfVectorizer(stop_words='english')
corpus_tfidf = vectorizer.fit_transform(corpus_texts)

# Load pre-trained model and tokenizer for answer generation (e.g., t5-small or similar open-source model)
tokenizer = AutoTokenizer.from_pretrained("t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")

# Function to match query to corpus and retrieve evidence
def retrieve_evidence(query):
    query_tfidf = vectorizer.transform([query])
    cosine_similarities = cosine_similarity(query_tfidf, corpus_tfidf).flatten()
    
    # Get indices of top matches
    top_indices = cosine_similarities.argsort()[-3:][::-1]
    
    evidence_list = []
    for idx in top_indices:
        evidence = {
            "title": corpus[idx]['title'],
            "author": corpus[idx]['author'],
            "url": corpus[idx]['url'],
            "source": corpus[idx]['source'],
            "category": corpus[idx]['category'],
            "published_at": corpus[idx]['published_at'],
            "fact": corpus[idx]['body'][:150]  # Just taking first 150 chars as a sample fact
        }
        evidence_list.append(evidence)
    
    return evidence_list, [corpus_texts[idx] for idx in top_indices]

# Function to generate answer from top evidence using a pre-trained model
def generate_answer(query, evidence_texts):
    # Concatenate the relevant documents as context
    context = " ".join(evidence_texts)
    
    # Prepare input for the model by combining query and context
    input_text = f"question: {query} context: {context}"
    
    # Tokenize and generate the answer using the model
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True)
    outputs = model.generate(inputs["input_ids"], max_length=50, num_beams=5, early_stopping=True)
    
    # Decode the output tokens to get the final answer
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer

# Example function to process a query
def process_query(query):
    # Retrieve evidence from the corpus
    evidence_list, evidence_texts = retrieve_evidence(query)
    
    # Generate answer using the model
    answer = generate_answer(query, evidence_texts)
    
    # Structure the result
    result = {
        "query": query,
        "answer": answer,  # The generated answer from the model
        "question_type": "inference_query",  # Assuming all questions are inference queries
        "evidence_list": evidence_list  # Evidence used for generating the answer
    }
    return result