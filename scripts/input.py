# input_processing.py

from transformers import BlipProcessor, BlipForConditionalGeneration, CLIPProcessor, CLIPModel
from PIL import Image
import torch
from urllib.parse import quote_plus

# Step 1: Load BLIP model for image captioning
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Step 2: Load CLIP model for multimodal embeddings (Optional, can be removed if not needed for embedding)
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
clip_model.eval()  # Set CLIP model to evaluation mode

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

# Step 5: (Optional) Generate image embedding using CLIP - in case you want to use embeddings
def generate_image_embedding(image_path):
    image = Image.open(image_path)
    inputs = clip_processor(images=image, return_tensors="pt")
    with torch.no_grad():
        image_embedding = clip_model.get_image_features(**inputs)
    image_embedding = torch.nn.functional.normalize(image_embedding, p=2, dim=-1)  # Normalize embedding
    return image_embedding

# Step 6: Prepare query for search API
def prepare_query_for_search_api(combined_query):
    formatted_query = quote_plus(combined_query)  # URL encode the query
    return formatted_query
