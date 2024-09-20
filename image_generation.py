### Turn this into a function that takes the caption from the caption_generation.py file and returns
### image url and caption pairs which can be used for pipelining. No need to display the image.
### Also put all endpoints and keys into .env files



from openai import AzureOpenAI
import os
import requests
from PIL import Image
import json

client = AzureOpenAI(
    api_version="2024-05-01-preview",
    azure_endpoint="https://iig-openai.openai.azure.com/",
    api_key="5e0c5e35b933413d83f4a981576da9cf",
)

result = client.images.generate(
    model="iig-image", # the name of our DALL-E 3 deployment
    prompt="Design a vibrant and uplifting abstract image that illustrates the positive impact of nature on childhood. The scene should feature elements like playful children interacting with nature, lush green landscapes, and colorful, whimsical elements that evoke a sense of joy and imagination. Use bright, cheerful colors and fluid, organic shapes to convey a sense of wonder and positivity. The style should be abstract yet joyful, highlighting the harmony between children and the natural world.",
    n=1
)

json_response = json.loads(result.model_dump_json())
print(json_response['data'][0]['url']) # can directly send to the instagram graph api

# Set the directory for the stored image
image_dir = os.path.join(os.curdir, 'images')

# If the directory doesn't exist, create it
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)

# Initialize the image path (note the filetype should be png)
image_path = os.path.join(image_dir, 'generated_image.png')

# Retrieve the generated image
image_url = json_response["data"][0]["url"]  # extract image URL from response
generated_image = requests.get(image_url).content  # download the image
with open(image_path, "wb") as image_file:
    image_file.write(generated_image)

# Display the image in the default image viewer
image = Image.open(image_path)
image.show()
