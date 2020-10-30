import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import webbrowser
import random

scope = "user-library-read"

# Create spotipy object
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# User
user = sp.current_user()

displayName = user['display_name']

while True:
    print()
    print(">>> Welcome to Spotify " + displayName + "!")
    print()
    print("0 - Search for an artist")
    print("1 - exit")
    print()
    choice = input("Your choice: ")

    # Search for the artist
    if choice == "0":
        print("0")
        searchQuery = input("Ok, what's their name?: ")
        print()

        # Get Search Results
        searchResults = sp.search(q=searchQuery, limit=1, offset=0, type="artist")

        # Artist details
        artist = searchResults['artists']['items'][0]
        print(artist['name'])
        print(str(artist['followers']['total']) + " followers")
        print("Genre: " + artist['genres'][0])
        print()

        # Top songs
        topTracks = sp.artist_top_tracks(artist_id=artist["id"], country="GB")["tracks"]

        trackIds = []
        trackPreviews = []
        z = 0
        print("Top tracks in UK: ")
        for item in topTracks:
            print(str(z) + ": " + item["name"])
            trackPreviews.append(item['preview_url'])
            trackIds.append(item['id'])
            z += 1

        print()
        songSelection = input("What song do you want to play?: ")
        print()

        audioFeature = sp.audio_features(tracks=[trackIds[int(songSelection)]])[0]

        acousticness = audioFeature["acousticness"]
        oppositeAcousticness = round(abs(acousticness - 1), 5)

        danceability = audioFeature["danceability"]
        oppositeDanceability = round(abs(danceability - 1), 5)

        energy = audioFeature["energy"]
        oppositeEnergy = round(abs(energy - 1), 5)

        valence = audioFeature["energy"]
        oppositeValence = round(abs(valence - 1), 5)

        print("Acousticness: " + str(acousticness))
        print("Opposite: " + str(oppositeAcousticness))
        print()
        print("Danceability: " + str(danceability))
        print("Opposite: " + str(oppositeDanceability))
        print()
        print("Energy: " + str(energy))
        print("Opposite: " + str(oppositeEnergy))
        print()
        print("Valence: " + str(valence))
        print("Opposite: " + str(oppositeValence))

        genres = ['pop', 'rap', 'jazz', 'rock', 'edm']

        recomendation = sp.recommendations(
            target_acousticness=oppositeAcousticness,
            target_danceability=oppositeDanceability,
            target_energy=oppositeEnergy,
            target_valence=oppositeValence,

            seed_genres=genres,
            limit=20
        )


        # print(json.dumps(recomendation['tracks'][0], sort_keys=True, indent=4))
        webbrowser.open(recomendation['tracks'][random.randint(0, 19)]["external_urls"]["spotify"])
        # webbrowser.open(trackPreviews[int(songSelection)])

        break
    # End the program
    if choice == "1":
        break
