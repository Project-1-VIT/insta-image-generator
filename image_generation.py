import os
import requests
import json
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get environment variables
IMAGE_API_KEY = os.getenv("IMAGE_API_KEY")
IMAGE_ENDPOINT = os.getenv("IMAGE_ENDPOINT")

image_client = AzureOpenAI(
    api_version="2024-05-01-preview",
    azure_endpoint=IMAGE_ENDPOINT,
    api_key=IMAGE_API_KEY,
)

# Function to generate image URL and return caption-image pairs
def generate_image(caption,prompt):
    """ Generate an image caption pair from a given prompt using DALL-E 3.

        Args:
            caption (str): Caption text for the Instagram post.
            prompt (str): Detailed image generation prompt for DALL-E 3.

        Returns:
            dict: A dictionary containing the caption and the generated image URL.
    """
    # Generate image from caption using DALL-E 3
    try:
        result = image_client.images.generate(
            model="iig-image",  # the name of our DALL-E 3 deployment
            prompt=prompt,
            n=1
        )
    except Exception as e:
        raise SystemExit(f"Failed to generate image. Error: {e}")

    # Parse the result and get the image URL
    try:
        json_response = json.loads(result.model_dump_json())
        image_url = json_response['data'][0]['url']  # Get image URL
    except KeyError:
        raise ValueError("Image generation failed or no URL was returned.")

    # Return the caption and corresponding image URL as a pair
    return {"caption": caption, "image_url": image_url}


# Example usage:
if __name__ == "__main__":
    # Sample caption prompt pairs to test
    caption = "🏛️ The timeless beauty of the Taj Mahal, reimagined with a neon glow. Flashy yet elegant, a pop art ode to one of the world's greatest wonders. 💫 #NeonTajMahal #PopArtJourney #ModernWonders"
    prompt = "Design a vibrant pop art version of the Taj Mahal, with neon colors outlining its iconic white marble domes and arches. The background should feature a glowing neon sky in shades of purple and pink, while the Taj Mahal itself is highlighted with bright neon blue, pink, and green accents to give it a modern, flashy aesthetic."

    result = generate_image(caption, prompt)
    print(result)  # Print or send result to another system