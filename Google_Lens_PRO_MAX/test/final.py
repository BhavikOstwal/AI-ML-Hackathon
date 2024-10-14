from transformers import BlipProcessor, BlipForConditionalGeneration, CLIPProcessor, CLIPModel
from PIL import Image
import torch

# Step 1: Load BLIP model for image captioning
blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Step 2: Load CLIP model for multimodal embeddings
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
    combined_query = f"{user_prompt}. Image shows: {image_caption}."
    return combined_query

# Step 5: Preprocess and encode the image using CLIP (for embeddings)
def generate_image_embedding(image_path):
    image = Image.open(image_path)
    inputs = clip_processor(images=image, return_tensors="pt")
    with torch.no_grad():
        image_embedding = clip_model.get_image_features(**inputs)
    image_embedding = torch.nn.functional.normalize(image_embedding, p=2, dim=-1)  # Normalize embedding
    return image_embedding

# Step 6: Convert combined query to a format suitable for search API
def prepare_query_for_search_api(combined_query):
    # You may need to URL-encode the query if using a web search API
    from urllib.parse import quote_plus
    formatted_query = quote_plus(combined_query)
    return formatted_query

# Step 7: Example search function (pseudo-code for API request)
def search_api(query):
    # Here, you would use the formatted query in a real API request
    # For example, Zenserp or any other free web search API
    # url = f"https://api.zenserp.com/search?q={query}&apikey=YOUR_API_KEY"
    # response = requests.get(url)
    # return response.json()
    return f"Search executed with query: {query}"

# Main function: Combine all steps
def main(image_path, user_prompt):
    # Step 1: Generate caption for the image using BLIP
    image_caption = generate_caption(image_path)
    print(f"Generated Image Caption: {image_caption}")

    # Step 2: Combine the image caption with the user's text prompt
    combined_query = combine_query(user_prompt, image_caption)
    print(f"Combined Query: {combined_query}")

    # Step 3: Prepare the combined query for web search
    formatted_query = prepare_query_for_search_api(combined_query)
    
    # Step 4: Call the search API with the formatted query
    search_results = search_api(formatted_query)
    print(search_results)

# Example usage
image_path = "path_to_your_image.jpg"  # Path to your input image
user_prompt = "brown cat"  # User-defined text query
main(image_path, user_prompt)
