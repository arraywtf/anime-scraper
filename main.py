import requests, ctypes

ctypes.windll.kernel32.SetConsoleTitleW("anime thumbnail scraper 3000")

# set up API access token
client_id = input("     Enter your AniList client ID: ")
client_secret = input("     Enter your AniList client secret: ")

print("[*] Starting scrape, this may take a few seconds")

auth_data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret
}

response = requests.post("https://anilist.co/api/v2/oauth/token", data=auth_data)
access_token = response.json()["access_token"]
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

query = '''
query ($perPage: Int, $page: Int) {
  Page (perPage: $perPage, page: $page) {
    media (type: ANIME) {
      id
      coverImage {
        extraLarge
      }
    }
  }
}
'''

perPage = 50
page = 1
all_images = []

while True:
    response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': {'perPage': perPage, 'page': page}}, headers=headers)
    data = response.json()
    
    if "errors" in data:
        print(data["errors"])
        break
    
    anime_list = data["data"]["Page"]["media"]
    for anime in anime_list:
        if anime["coverImage"] is not None:
            image_url = anime["coverImage"]["extraLarge"]
            all_images.append(image_url)
    
    if len(anime_list) < perPage:
        break
    else:
        page += 1

for i, image_url in enumerate(all_images):
    response = requests.get(image_url, stream=True)
    file_name = f"anime_image_{i}.jpg"
    with open(file_name, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    print(f"Downloaded {file_name}")