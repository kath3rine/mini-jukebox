import serial
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from secret import *

SCOPE = "user-modify-playback-state user-read-playback-state"
REDIRECT_URI = 'http://localhost:8888/callback'

# Arduino serial communication setup
ser = serial.Serial('/dev/cu.usbmodemF412FA7553042', 9600)  # Change to appropriate port
ser.flushInput()

# Spotify authentication
sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI,
                        scope=SCOPE)

# Get the access token
access_token = sp_oauth.get_access_token(as_dict=False)

# Spotify client initialization
sp = spotipy.Spotify(auth=access_token)

# Mapping between RFID tag IDs and Spotify song URIs
rfid_to_song = {
    "6C4C3750": "spotify:track:1fDFHXcykq4iw8Gg7s5hG9",
    "ECF82750": "spotify:track:0z1o5L7HJx562xZSATcIpY",
    "2CE92750": "spotify:track:5QLHGv0DfpeXLNFo7SFEy1",
    "ECCF2650": "spotify:track:4PTG3Z6ehGkBFwjybzWkR8"
}

# Main loop
while True:
#    print("hello world")
#    print(ser.in_waiting)
    if ser.in_waiting > 0:
        #rint(sp.devices())
        message = ser.readline().decode().strip()
        print("Message from Arduino:", message)
        if message.startswith("UID"):
            tagID = message.split(":")[1].strip()
            print(tagID)
            if tagID in rfid_to_song:
                song_uri = rfid_to_song[tagID]
                print(song_uri)
                # Play the selected song using Spotify API
                sp.start_playback(device_id = '7c346669666b42f24cc39728c1cfc2cc78f7b551', uris=[song_uri])
