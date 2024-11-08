import os
import requests
import json
import time
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


def getCreds():
    """ Get credentials required for use in the application.

    Loads credentials from environment variables, including access token, Instagram account ID, and API version information.

    Returns:
        dict: A dictionary containing the credentials needed globally.
    """
    creds = dict()
    creds['access_token'] = os.getenv("ACCESS_TOKEN")
    creds['graph_domain'] = 'https://graph.facebook.com/'
    creds['graph_version'] = 'v20.0'
    creds['endpoint_base'] = creds['graph_domain'] + creds['graph_version'] + '/'
    creds['instagram_account_id'] = os.getenv("INSTAGRAM_ACCOUNT_ID")
    return creds


def makeApiCall(url, endpointParams, type):
    """ Request data from an endpoint with provided parameters.

    Args:
        url (str): The endpoint URL to make a request from.
        endpointParams (dict): Dictionary containing the URL parameters.
        type (str): HTTP method type ('POST' or 'GET').

    Returns:
        dict: A dictionary containing the response data, including URL, endpoint parameters, and JSON response.
    """
    if type == 'POST':
        data = requests.post(url, endpointParams)
    else:
        data = requests.get(url, endpointParams)

    response = dict()
    response['url'] = url
    response['endpoint_params'] = endpointParams
    response['endpoint_params_pretty'] = json.dumps(endpointParams, indent=4)
    response['json_data'] = json.loads(data.content)
    response['json_data_pretty'] = json.dumps(response['json_data'], indent=4)

    return response


def createMediaObject(params):
    """ Create a media object on Instagram.

    Args:
        params (dict): Dictionary of required parameters like access token, media URL, and caption.

    Returns:
        dict: A dictionary containing the response data from the media creation request.
    """
    url = params['endpoint_base'] + params['instagram_account_id'] + '/media'
    endpointParams = dict()
    endpointParams['caption'] = params['caption']
    endpointParams['access_token'] = params['access_token']

    if params['media_type'] == 'IMAGE':
        endpointParams['image_url'] = params['media_url']

    return makeApiCall(url, endpointParams, 'POST')


def getMediaObjectStatus(mediaObjectId, params):
    """ Check the status of a media object on Instagram.

    Args:
        mediaObjectId (str): The ID of the media object to check status for.
        params (dict): Dictionary containing necessary credentials and parameters.

    Returns:
        dict: A dictionary containing the response data, including the media object status.
    """
    url = params['endpoint_base'] + mediaObjectId
    endpointParams = dict()
    endpointParams['fields'] = 'status_code'
    endpointParams['access_token'] = params['access_token']

    return makeApiCall(url, endpointParams, 'GET')


def publishMedia(mediaObjectId, params):
    """ Publish a media object to Instagram.

    Args:
        mediaObjectId (str): The ID of the media object to publish.
        params (dict): Dictionary containing necessary credentials and parameters.

    Returns:
        dict: A dictionary containing the response data after publishing the media.
    """
    url = params['endpoint_base'] + params['instagram_account_id'] + '/media_publish'
    endpointParams = dict()
    endpointParams['creation_id'] = mediaObjectId
    endpointParams['access_token'] = params['access_token']

    return makeApiCall(url, endpointParams, 'POST')


def getContentPublishingLimit(params):
    """ Get the API limit for the Instagram user.

    Args:
        params (dict): Dictionary containing necessary credentials and parameters.

    Returns:
        dict: A dictionary containing the response data for the content publishing limit.
    """
    url = params['endpoint_base'] + params['instagram_account_id'] + '/content_publishing_limit'
    endpointParams = dict()
    endpointParams['fields'] = 'config,quota_usage'
    endpointParams['access_token'] = params['access_token']

    return makeApiCall(url, endpointParams, 'GET')


def post(media_type, media_url, caption):
    """ Post media with a caption to Instagram.

        Args:
            media_type (str): The type of media ('IMAGE').
            media_url (str): The URL of the media.
            caption (str): The caption for the media post.

        Returns:
            None
    """
    params = getCreds()
    params['media_type'] = media_type
    params['media_url'] = media_url
    params['caption'] = caption

    mediaObjectResponse = createMediaObject(params)
    mediaObjectId = mediaObjectResponse['json_data']['id']
    mediaStatusCode = 'IN_PROGRESS'

    while mediaStatusCode != 'FINISHED':
        mediaObjectStatusResponse = getMediaObjectStatus(mediaObjectId, params)
        mediaStatusCode = mediaObjectStatusResponse['json_data']['status_code']
        print(f"\n---- {media_type} MEDIA OBJECT STATUS -----\n")
        print(f"\tStatus Code:\n\t{mediaStatusCode}")
        time.sleep(5)

    publishResponse = publishMedia(mediaObjectId, params)
    print(f"\n---- PUBLISHED {media_type} RESPONSE -----\n")
    print(f"\tResponse:\n{publishResponse['json_data_pretty']}")

    contentPublishingApiLimit = getContentPublishingLimit(params)
    print("\n---- CONTENT PUBLISHING USER API LIMIT -----\n")
    print(f"\tResponse:\n{contentPublishingApiLimit['json_data_pretty']}")


# Example usage:
if __name__ == "__main__":
    image_caption_pairs = [
        {
            "image_url": "https://dalleproduse.blob.core.windows.net/private/images/fa8e93d0-23a2-4a34-b3ae-653f786f2296/generated_00.png?se=2024-11-09T14%3A30%3A02Z&sig=QA3Pm7ANa0%2BlI5wNMWwTP8v8sGELXr8oL442EoGtPVU%3D&ske=2024-11-15T07%3A26%3A35Z&skoid=09ba021e-c417-441c-b203-c81e5dcd7b7f&sks=b&skt=2024-11-08T07%3A26%3A35Z&sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&skv=2020-10-02&sp=r&spr=https&sr=b&sv=2020-10-02",
            "caption": "Test caption:\n🗼 The Leaning Tower of Pisa, but with a neon glow! Bringing this historic monument into the pop art world with a bright and bold twist. 💡 #PisaGlow #NeonPopArt #TravelThroughArt"
        },
        {
            "image_url": "https://dalleproduse.blob.core.windows.net/private/images/fa8e93d0-23a2-4a34-b3ae-653f786f2296/generated_00.png?se=2024-11-09T14%3A30%3A02Z&sig=QA3Pm7ANa0%2BlI5wNMWwTP8v8sGELXr8oL442EoGtPVU%3D&ske=2024-11-15T07%3A26%3A35Z&skoid=09ba021e-c417-441c-b203-c81e5dcd7b7f&sks=b&skt=2024-11-08T07%3A26%3A35Z&sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&skv=2020-10-02&sp=r&spr=https&sr=b&sv=2020-10-02",
            "caption": "Test caption:\n🏛️ The timeless beauty of the Taj Mahal, reimagined with a neon glow. Flashy yet elegant, a pop art ode to one of the world's greatest wonders. 💫 #NeonTajMahal #PopArtJourney #ModernWonders"
        }
    ]

    for pair in image_caption_pairs:
        media_url = pair['image_url']
        caption = pair['caption']
        post("IMAGE", media_url, caption)
