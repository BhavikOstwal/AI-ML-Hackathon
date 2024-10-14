import streamlit as st
from PIL import Image
import requests
from io import BytesIO
from scripts import input, search_api 

st.title("Google Lens Pro MAX")

uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

user_text = st.text_input("Enter a search query:")

if st.button("Search"):
    if uploaded_image and user_text:
        with st.spinner("Generating caption..."):
            caption = input.generate_caption(uploaded_image)
            print(caption)
            st.write(f"Generated Image Caption: {caption}")
        
        combined_query = input.combine_query(user_text, caption)
        # blended_query = input.blend_query_spacy(user_text,combined_query)
        st.write(f"Combined Query: {combined_query}")
        # print(blended_query)
        # formatted_query = prepare_query_for_search_api(combined_query)
        
        with st.spinner("Fetching image results..."):
            image_results = search_api.my_web_scraper(combined_query)
            # print(image_results)

            if image_results:
                cols = st.columns(3)
                
                for id, image in enumerate(image_results):
                    col = cols[id%3]  # so that 3-3 ke grid mein images dikhe
                    col.image(image["original"], caption=image["title"], use_column_width=True)
                    # col.image("https://d2j6dbq0eux0bg.cloudfront.net/images/18729129/1470047725.jpg",use_column_width=True)
                    # col.write(f"[Link to product]({image['link']})")
            else:
                st.write("No images found for the query.")
