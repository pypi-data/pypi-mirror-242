
# Anime Search

This Python program features a modular anime library leveraging the Jikan API. The `animeLibrary` class retrieves anime details such as title, score, episode count, and synopsis based on user input. 

## API 


```http
  https://api.jikan.moe/v4/anime
```





## Installation


```bash
  pip install animesearchinfo
```
    
## Usage/Examples

```javascript
from anime_library import animeLibrary

def main():
    jikan = animeLibrary()
    print(" ")
    query = input("Search an anime: ")
    print(" ")
    hasil_pencarian = jikan.cek_anime(query)

    if isinstance(hasil_pencarian, dict):
        for anime in hasil_pencarian.get('data', []):
            print(f"Title: {anime.get('title')}")
            print(f"Episodes: {anime.get('episodes')}")
            print(f"Score: {anime.get('scores')}")
            print(f"Synopsis: {anime.get('synopsis')}")
            
if __name__ == "__main__":
    main()

```

