def get_result_from_midjourney():
    '''
        Get request for getting the result of post request
    '''
    get_url = "https://discord.com/api/v9/channels/121202**/messages?limit=50"
    get_payload = {}
    get_headers = {
        'Authorization': settings.midjourney_token,
        'Content-Type': 'application/json',
        'Cookie': <my cookie here>
    }
    get_response = requests.request(
        "GET", get_url, headers=get_headers, data=get_payload
    )
    return get_response