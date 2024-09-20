### Turn this into a function that will take multiple inputs, the social media description along with the
### art style, the no of posts, the type of posts(optional) and return the caption and the image prompt.
### Put the keys in a .env file



import os
import requests

# Configuration
API_KEY = "5e0c5e35b933413d83f4a981576da9cf"
headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}

# Payload for the request
payload = {
  "messages": [
    {
      "role": "system",
      "content": [
        {
          "type": "text",
          "text": "Imagine you are a social media manager for a company, I will provide you with a description of your clients Instagram page, number of posts and ideas for those posts. You will provide me with a caption for each Instagram post idea and a detailed prompt for image generation to feed to dalle 3.\n\nThe response is to be formatted in a python dictionary with each post having its own key. The value for each key should be a list with the first element as the caption and the second element as the prompt"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Page Description: I am a graphic designing page with nature focused posts. I have abstract style posts."
        },

      ]
    },
    {
      "role": "assistant",
      "content": [
        {
          "type": "text",
          "text": "```python\ninstagram_posts = {\n    \"post_1\": [\n        \"🌍 A glimpse into a bleak future. Our choices today shape the world of tomorrow. Let's protect nature before it's too late. #SaveThePlanet #Nature #AbstractArt\",\n        \"An abstract representation of a desolate landscape, showcasing cracked earth, dying trees, and a polluted sky. Use muted colors like grays and browns to evoke a sense of despair.\"\n    ],\n    \"post_2\": [\n        \"🌿 Nature's embrace heals the soul. Here's a reminder of how the great outdoors can uplift our spirits and connect us to what truly matters. #NatureLovers #Wellbeing #ArtInNature\",\n        \"A vibrant abstract artwork illustrating the positive impact of nature on people. Include figures joyfully interacting with trees, flowers, and water, surrounded by bright greens and blues to evoke feelings of tranquility and happiness.\"\n    ]\n}\n```"
        }
      ]
    }
  ],
  "temperature": 0.7,
  "top_p": 0.95,
  "max_tokens": 800
}

ENDPOINT = "https://iig-openai.openai.azure.com/openai/deployments/iig-caption/chat/completions?api-version=2024-02-15-preview"

# Send request
try:
    response = requests.post(ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
except requests.RequestException as e:
    raise SystemExit(f"Failed to make the request. Error: {e}")

# Handle the response as needed (e.g., print or process)
print(response.json())
