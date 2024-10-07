import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyHandler:
    def __init__(self, client_id, client_secret):
        # Authenticate with Spotify
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id,
                                                                        client_secret=client_secret))

    def get_top_drum_and_bass_tracks(self, limit=25):
        # Search for drum and bass tracks
        query = 'genre:"drum and bass"'
        results = self.sp.search(q=query, type='track', limit=limit)

        # Extract track details
        top_tracks = []
        for idx, item in enumerate(results['tracks']['items']):
            track_name = item['name']
            artist_name = item['artists'][0]['name']
            track_url = item['external_urls']['spotify']
            top_tracks.append(f"{idx + 1}. {track_name} by {artist_name} - {track_url}")

        return top_tracks


    def get_top_dubstep_tracks(self, limit=25):
        # Search for dubstep tracks
        query = 'genre:"dubstep"'
        results = self.sp.search(q=query, type='track', limit=limit)

        # Extract track details
        top_tracks = []
        for idx, item in enumerate(results['tracks']['items']):
            track_name = item['name']
            artist_name = item['artists'][0]['name']
            track_url = item['external_urls']['spotify']
            top_tracks.append(f"{idx + 1}. {track_name} by {artist_name} - {track_url}")

        return top_tracks


    def get_top_house_tracks(self, limit=25):
        # Search for house tracks
        query = 'genre:"house"'
        results = self.sp.search(q=query, type='track', limit=limit)

        # Extract track details
        top_tracks = []
        for idx, item in enumerate(results['tracks']['items']):
            track_name = item['name']
            artist_name = item['artists'][0]['name']
            track_url = item['external_urls']['spotify']
            top_tracks.append(f"{idx + 1}. {track_name} by {artist_name} - {track_url}")

        return top_tracks