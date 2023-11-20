import requests

def get_current_utc_time():
    url = "http://worldtimeapi.org/api/timezone/Etc/UTC"
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    data = response.json()
    return data['utc_datetime']
