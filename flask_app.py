import os
from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

app = Flask(__name__)

# Get sensitive information from enviroment variables
C_ID = os.getenv('C_ID')
C_SECRET = os.getenv('C_SECRET')

# Setting up spotipy client
client_credentials_manager = SpotifyClientCredentials(client_id=C_ID, client_secret=C_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def parse_url(url):
	""" Returns username from url """
	return url.split('/')[-1].split('?')[0]


def get_all_playlist_tracks(user):
	""" Returns tracks found in user's playlists.
		Limited to 50 playlists in spotipy user_playlists """
	#TODO: increase maximum playlists fetched from 50 to 100?
	usr_playlists = sp.user_playlists(user)

	tracks = []

	for pl in usr_playlists['items']:
		try:
			pl_tracks = sp.user_playlist_tracks(user, playlist_id=pl['id'])
			for track in pl_tracks['items']:
				tracks.append({ 'song_name' : track['track']['name'],
								'img' : track['track']['album']['images'][1]['url'],
								'artists' : [ dic['name'] for dic in track['track']['artists']] })
		#TODO: specific exception for no playlists found 
		# exception occurs when user has no playlists, if so,
		# we pass and an empty list is returned
		except:
			pass

	return tracks


def find_common_tracks(tracklist_one, tracklist_two):
	""" Returns intersection of track lists """		
	#TODO: add artist to track names or better identification
	#	   for a more accurate comparison between track lists.
	#	   Currently we are using only song name for comparison 
	#	   which can match songs by different artists with the 
	#	   same name. 
	
	# Finding the smaller list of the two for optimization
	smaller_list = sorted([tracklist_one, tracklist_two], key=len)
	# Create list of track names found in list
	sl_track_names = [item['song_name'] for item in smaller_list[0]]

	tracks = []

	for item in smaller_list[1]:
		if item['song_name'] in sl_track_names:
			tracks.append(item)
	
	# Return list of unique dictionaries 
	# see: https://stackoverflow.com/a/11092590
	return list({v['song_name']:v for v in tracks}.values())


@app.route('/', methods=['GET'])
def my_form_query():
	user_1 = request.args.get("usr1")
	user_2 = request.args.get("usr2")

	# Will only continue if two users are passed in
	if all((user_1, user_2)):
		# Not comparing two of the same username
		if user_1 == user_2:
			return render_template('index.html',
				msg="You should find someone to compare songs with.")
	

		# Parsing if url passed in
		#TODO: Clean this up
		if user_1.startswith('http'):
			user_1 = parse_url(user_1)
		if user_2.startswith('http'):
			user_2 = parse_url(user_2)

	
		# We try because a username may be incorrect
		# or we encounter an error that we do not yet know
		try:
			user_one_tracks = get_all_playlist_tracks(user_1)
			user_two_tracks = get_all_playlist_tracks(user_2)
		#TODO: add specific exception for invalid user
		except Exception as e:
			if "Invalid username" in str(e):
				return render_template('index.html',
						msg="Woops. Invalid Spotify username.")
			else:
				return render_template('index.html',
						msg="You broke it :(")

		# Songs in common between both users
		final_list = find_common_tracks(user_one_tracks, user_two_tracks)
		# Returning result page	
		return render_template("index.html", result=final_list, users=(user_1, user_2))

	# Returning main page	
	return render_template('index.html')


if __name__ == "__main__":
	app.run('127.0.0.1')
