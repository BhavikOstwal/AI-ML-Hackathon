# search_api.py

import requests

# def my_web_scraper(query):
#     api_key = "670b6b9cd7afc43e3ad40f4e"
#     url = "https://api.scrapingdog.com/google_images/"
    
#     params = {
#         "api_key": api_key,
#         "query": f"{query}",
#         "results": 10,
#         "country": "in",
#         "page": 0
#     }
    
#     response = requests.get(url, params=params)
    
#     if response.status_code == 200:
#         data = response.json()
#         print(data)
#     else:
#         print(f"Request failed with status code: {response.status_code}")

def my_web_scraper(query):
    api_key = "670b6b9cd7afc43e3ad40f4e"
    # api_key = "670bdbdd1ad42cd59ea7b0c9"
    url = "https://api.scrapingdog.com/google_images/"
    
    params = {
        "api_key": api_key,
        "query": f"{query}",
        "results": 10,
        "country": "in",
        "page": 0
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json().get("images_results", [])
    else:
        print(f"Request failed with status code: {response.status_code}")
        return []