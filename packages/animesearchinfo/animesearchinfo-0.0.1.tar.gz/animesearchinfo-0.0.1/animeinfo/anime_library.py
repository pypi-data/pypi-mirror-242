import requests

class animeLibrary:
    def __init__(self):
        self.base_url = "https://api.jikan.moe/v4/anime"

    def cek_anime(self, query):
        params = {'q': query}
        response = requests.get(self.base_url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code}"