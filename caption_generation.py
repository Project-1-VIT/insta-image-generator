import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get environment variables
CHAT_API_KEY = os.getenv("CHAT_API_KEY")
CHAT_ENDPOINT = os.getenv("CHAT_ENDPOINT")

# Initialize Azure OpenAI client for caption generation
chat_client = AzureOpenAI(
    azure_endpoint=CHAT_ENDPOINT,
    api_key=CHAT_API_KEY,
    api_version="2024-05-01-preview",
)

# Function to generate captions and prompts for Instagram posts
def generate_captions_and_prompts(page_description, num_posts, post_ideas=None):
    """ Generate captions and prompts for Instagram posts based on the page description and post ideas.

        Args:
            page_description (str): Description of the Instagram page.
            num_posts (int): Number of posts to generate captions and prompts for.
            post_ideas (list): List of post ideas.

        Returns:
            dict: A dictionary containing post codes with corresponding captions and prompts.
    """
    #Error handling for post_ideas
    if post_ideas == "":
        post_ideas = None

    # Prepare the prompt with user inputs
    if post_ideas is None:
        user_content = f"Page Description: {page_description}\nNo. of posts: {num_posts}" # Error handling so that model doesn't generate extra text
    else:
        user_content = f"Page Description: {page_description}\nNo. of posts: {num_posts}\nPost Ideas:\n" + "\n".join(post_ideas)
    print(user_content)

    # Generate the completion
    completion = chat_client.chat.completions.create(
        model=os.getenv("DEPLOYMENT_NAME", "gpt-4"),
        messages=[
            {
                "role": "system",
                "content": (
                    "Imagine you are a social media manager for a company. I will provide you with a description of "
                    "your client's Instagram page, number of posts, and ideas for those posts. You will provide me with "
                    "a caption for each Instagram post idea and a detailed prompt for image generation to feed to DALL-E 3."
                    "\n\nThe response should be a nested JSON. The first layer will be the post code (e.g., post_1, post_2), "
                    "and the second layer will contain 'caption' and 'prompt' fields.\n"
                )
            },
            {
                "role": "user",
                "content": user_content
            }
        ],
        max_tokens=800,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
    )

    # Parse the JSON response
    response = completion.to_json()
    response_dict = json.loads(response)

    # Extract the 'message' content which contains the captions and prompts
    message_content = response_dict['choices'][0]['message']['content']
    print("Message content:", message_content)

    # Convert the message content back to a dictionary
    posts_data = json.loads(message_content)

    # Initialize an empty dictionary to store the captions and prompts
    nested_dict = {}

    # Loop through the posts and save captions and prompts to the dictionary
    for post_key, post_data in posts_data.items():
        nested_dict[post_key] = {
            'caption': post_data['caption'],
            'prompt': post_data['prompt']
        }

    # Return the nested dictionary
    return nested_dict

# Example usage:
if __name__ == "__main__":
    page_description = "I am a graphic design page with nature-focused posts and abstract styles."
    num_posts = 2
    post_ideas = [
        "Post 1: Something to portray the bleak future if we continue to destroy nature.",
        "Post 2: Something to show the impact nature has on people."
    ]

    result = generate_captions_and_prompts(page_description, num_posts, post_ideas)
    print(result)  # Print the generated captions and prompts