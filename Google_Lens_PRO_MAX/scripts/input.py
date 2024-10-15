from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
from urllib.parse import quote_plus
import spacy

# Step 1: Load BLIP model for image captioning
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Step 3: Function to generate image caption using BLIP
def generate_caption(image_path):
    image = Image.open(image_path)
    inputs = blip_processor(images=image, return_tensors="pt")
    out = blip_model.generate(**inputs)
    caption = blip_processor.decode(out[0], skip_special_tokens=True)
    return caption

# Step 4: Combine user text prompt and image caption
def combine_query(user_prompt, image_caption):
    combined_query = f"{user_prompt}. The image shows {image_caption}."
    return combined_query

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")
def blend_query_spacy(user_query, blip_caption):
    vague_words = ['similar', 'this', 'type', 'kind', 'like']
    
    # Parse the user query and BLIP caption
    user_query_doc = nlp(user_query)
    
    # Replace vague words in the user query with BLIP details
    new_query_tokens = []
    for token in user_query_doc:
        if token.text in vague_words:
            new_query_tokens.append(blip_caption)
        else:
            new_query_tokens.append(token.text)
    
    # Combine the tokens back into a sentence
    blended_query = " ".join(new_query_tokens)
    return blended_query


# Step 6: Prepare query for search API
def prepare_query_for_search_api(combined_query):
    formatted_query = quote_plus(combined_query)  # URL encode the query
    return formatted_query
