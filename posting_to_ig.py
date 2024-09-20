import requests
import json
import time

def getCreds() :
    """ Get creds required for use in the applications
    
    Returns:
        dictionary: credentials needed globally
    """
    creds = dict()
    creds['access_token'] = 'EAAGx8UDBgFoBOZCZCe2rQuomJYXFwsLVCC7EHZAlVDhZBbd3K8jL54TmoxhfGhYB8NbQoufFSLkSGuHZB3ZAiu136MMGsPBRBSngzVH2AswJKilsuAbZBNNq64FXnaZB8th8T5crBd1E0yRvFk5eBGlCKivRIlZBkIw4VLx8st1ZBldviEZBiz5W5uCcpnEUTawXaoS'
    creds['graph_domain'] = 'https://graph.facebook.com/'
    creds['graph_version'] = 'v20.0'
    creds['endpoint_base'] = creds['graph_domain'] + creds['graph_version'] + '/'
    creds['instagram_account_id'] = '17841459117244865'
    return creds

def makeApiCall(url, endpointParams, type):
    """ Request data from endpoint with params
    
    Args:
        url: string of the url endpoint to make request from
        endpointParams: dictionary keyed by the names of the url parameters

    Returns:
        object: data from the endpoint
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
    """ Create media object
    
    Args:
        params: dictionary of params

    Returns:
        object: data from the endpoint
    """
    url = params['endpoint_base'] + params['instagram_account_id'] + '/media'
    endpointParams = dict()
    endpointParams['caption'] = params['caption']
    endpointParams['access_token'] = params['access_token']
    
    if params['media_type'] == 'IMAGE':
        endpointParams['image_url'] = params['media_url']
    else:
        endpointParams['media_type'] = params['media_type']
        endpointParams['video_url'] = params['media_url']
    
    return makeApiCall(url, endpointParams, 'POST')

def getMediaObjectStatus(mediaObjectId, params):
    """ Check the status of a media object
    
    Args:
        mediaObjectId: id of the media object
        params: dictionary of params

    Returns:
        object: data from the endpoint
    """
    url = params['endpoint_base'] + mediaObjectId
    endpointParams = dict()
    endpointParams['fields'] = 'status_code'
    endpointParams['access_token'] = params['access_token']
    
    return makeApiCall(url, endpointParams, 'GET')

def publishMedia(mediaObjectId, params):
    """ Publish content
    
    Args:
        mediaObjectId: id of the media object
        params: dictionary of params

    Returns:
        object: data from the endpoint
    """
    url = params['endpoint_base'] + params['instagram_account_id'] + '/media_publish'
    endpointParams = dict()
    endpointParams['creation_id'] = mediaObjectId
    endpointParams['access_token'] = params['access_token']
    
    return makeApiCall(url, endpointParams, 'POST')

def getContentPublishingLimit(params):
    """ Get the api limit for the user
    
    Args:
        params: dictionary of params

    Returns:
        object: data from the endpoint
    """
    url = params['endpoint_base'] + params['instagram_account_id'] + '/content_publishing_limit'
    endpointParams = dict()
    endpointParams['fields'] = 'config,quota_usage'
    endpointParams['access_token'] = params['access_token']
    
    return makeApiCall(url, endpointParams, 'GET')

def post(media_type, media_url, caption):
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

def job():
    post("IMAGE", 'https://dalleproduse.blob.core.windows.net/private/images/32fb9d08-daec-403f-8bda-ce70f4dd67d9/generated_00.png?se=2024-09-19T11%3A41%3A29Z&sig=bDmRUiPjUbZwIrYrtzl8td7ZD4KawumHXrJPwf3S8aw%3D&ske=2024-09-25T03%3A53%3A09Z&skoid=09ba021e-c417-441c-b203-c81e5dcd7b7f&sks=b&skt=2024-09-18T03%3A53%3A09Z&sktid=33e01921-4d64-4f8c-a055-5bdaffd5e33d&skv=2020-10-02&sp=r&spr=https&sr=b&sv=2020-10-02', "This is a test using the new post method")
