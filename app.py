import time
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from flask import Flask, request, jsonify
from caption_generation import generate_captions_and_prompts
from image_generation import generate_image
from posting_to_ig import post

app = Flask(__name__)

# Load environment variables from the .env file
load_dotenv()

# Get environment variables
CHAT_API_KEY = os.getenv("CHAT_API_KEY")
CHAT_ENDPOINT = os.getenv("CHAT_ENDPOINT")
IMAGE_API_KEY = os.getenv("IMAGE_API_KEY")
IMAGE_ENDPOINT = os.getenv("IMAGE_ENDPOINT")

# Initialize Azure OpenAI client for caption generation
chat_client = AzureOpenAI(
    azure_endpoint=CHAT_ENDPOINT,
    api_key=CHAT_API_KEY,
    api_version="2024-05-01-preview",
)

# Initialize Azure OpenAI client for image   generation
image_client = AzureOpenAI(
    api_version="2024-05-01-preview",
    azure_endpoint=IMAGE_ENDPOINT,
    api_key=IMAGE_API_KEY,
)

def schedule_post(image_caption_pairs, interval):
    """ Schedule posts at the specified interval. """
    for pair in image_caption_pairs:
        post(pair['image_url'], pair['caption'])  # Call the post function
        time.sleep(interval)  # Wait for the specified interval

@app.route('/schedule_post', methods=['POST'])
def schedule_post():
    print("Received request")
    data = request.json
    description = data.get('account_description')
    num_posts = int(data.get('num_posts'))
    time_interval = int(data.get('time_interval', 0))  # Default to 0 if not provided
    post_ideas = data.get('post_ideas', [])
    print("Received data")

    # Step 1: Generate captions and prompts
    caption_prompt_pairs = generate_captions_and_prompts(description, num_posts, post_ideas)
    print("Caption prompt pairs created successfully")

    # Step 2: Prepare image_url and caption pairs
    image_caption_pairs = []
    for key in caption_prompt_pairs.keys():
        caption = caption_prompt_pairs[key]['caption']
        prompt = caption_prompt_pairs[key]['prompt']
        image_data = generate_image(caption, prompt)
        image_caption_pairs.append(image_data)
        print("Image generated successfully")
    print("Image caption pairs generated successfully")

    # Step 3: Schedule posts
    for pair in image_caption_pairs:
        time.sleep(time_interval)  # Wait for the defined time interval before the next post
        media_url = pair['image_url']
        caption = pair['caption']
        post("IMAGE", media_url, caption)
        print("Image posted")

    return jsonify({"status": "success", "message": f"{num_posts} posts scheduled successfully."})

if __name__ == "__main__":
    app.run(debug=True)
