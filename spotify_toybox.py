#!/usr/bin/env python
# coding: utf-8

# library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import warnings
warnings.simplefilter("ignore",FutureWarning)
import os
from dotenv import load_dotenv
from os.path import join, dirname

# .env
load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

client_id = os.environ.get("SPOTIFY_CLIENT_ID")
client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
redirect_uri = "http://127.0.0.1:8080/"
scope = "playlist-modify-public"
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))



# argument:song_id -> features
def get_features(song_id):
    features = spotify.audio_features(song_id)[0]
    return features, song_id

# argument:features -> recommendations
def get_recommendations(features,song_id):
    recommendations = spotify.recommendations(seed_tracks=[song_id], limit=15, target_energy=features['energy']+0.05, target_danceability=features['danceability'])
    return recommendations


# Create new playlist
def create_playlist(name, recommendations):
    playlist_name = name
    user_id = spotify.current_user()["id"]
    playlist = spotify.user_playlist_create(user_id,playlist_name)
    track_ids = [track['id'] for track in recommendations["tracks"]]
    spotify.playlist_add_items(playlist["id"],track_ids)
    print("New playlist created: ", playlist_name)

# Recommendations -> CSV
def recommendations_to_csv(recommendations):
    recommended_songs = pd.DataFrame(columns=['Song', 'Artist'])
    for track in recommendations['tracks']:
        recommended_songs = recommended_songs.append({'Song': track['name'], 'Artist': track['artists'][0]['name']}, ignore_index=True)
    recommended_songs.to_csv('recommended_songs.csv', index=False)

if __name__ == '__main__':
    song_id = input("Enter song id: ")
    playlist_name = input("Enter playlist name: ")
    features, song_id = get_features(song_id)
    recommendations = get_recommendations(features,song_id)
    create_playlist(playlist_name, recommendations)
    recommendations_to_csv(recommendations)



