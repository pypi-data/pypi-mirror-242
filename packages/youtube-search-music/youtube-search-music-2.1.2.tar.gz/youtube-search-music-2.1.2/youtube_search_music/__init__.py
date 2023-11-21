import requests

class YoutubeMusicSearch():
    """api key must be string from google cloud console https://console.cloud.google.com/ make sure to enable youtube api v3"""
    def __init__(self, api_key: str) -> None:        
        self.API_KEY = api_key
        self.BASE_URL = 'https://www.googleapis.com/youtube/v3/search'

    def search(self, query: str):
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'videoCategoryId': '10',  # 10 corresponds to the Music category
            'key': self.API_KEY,
        }

        response = requests.get(self.BASE_URL, params=params)
        return response.json()
