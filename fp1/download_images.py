import requests
import os
from urllib.parse import urlparse, unquote

def search_unsplash_images(query, client_id, folder='unsplash_downloads', per_page=3):
    endpoint = "https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "client_id": client_id,
        "per_page": per_page
    }
    response = requests.get(endpoint, params=params)
    if response.status_code != 200:
        print("Failed to fetch images:", response.content)
        return []
    
    if not os.path.exists(folder):
        os.makedirs(folder)
        
    i = 1
    for image in response.json()['results']:
        image_url = image['urls']['regular']  # You can choose different sizes ['small', 'thumb', 'raw', etc.]
        image_response = requests.get(image_url, stream=True)
        
        
        if image_response.status_code == 200:
            
            file_name = os.path.basename(query) + str(i) + ".jpg"
            i+=1
            
            # Ensure file name is valid and decode any URL encoding
            file_name = unquote(file_name).replace("?", "_").replace("&", "_")

            file_path = os.path.join(folder, file_name)
            with open(file_path, 'wb') as f:
                for chunk in image_response.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded {image_url.split('/')[-1]}")
        else:
            print(f"Failed to download {image_url}")

def download_image(image_url, folder='unsplash_downloads'):
    if not os.path.exists(folder):
        os.makedirs(folder)
    response = requests.get(image_url, stream=True)
    
    
    if response.status_code == 200:
        parsed_url = urlparse(image_url)
        file_name = os.path.basename(parsed_url.path) + ".jpg"
        
        # Ensure file name is valid and decode any URL encoding
        file_name = unquote(file_name).replace("?", "_").replace("&", "_")

        file_path = os.path.join(folder, file_name)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded {image_url.split('/')[-1]}")
    else:
        print(f"Failed to download {image_url}")

# Usage Example
client_id = "SfIJjEbmk8kstjFNxaccV1Tb_dnDOvzf0ddmIt6qDRg"  # Replace with your Unsplash Access Key
images = search_unsplash_images("chole bhature", client_id)

