from flask import Flask, request, Response
from flask_cors import CORS
import sys, os
import jsonpickle
import platform
import base64
import redis
import json
import io
import spotipy
import mysql.connector
from spotipy.oauth2 import SpotifyClientCredentials
import speech_recognition as sr

redisHost = os.getenv("REDIS_HOST") or "localhost"
redisPort = os.getenv("REDIS_PORT") or 6379
client_id = os.getenv('CLIENT_ID') or "01f4d3b546774e06a1ceb4713fed7664"
client_secret = os.getenv('CLIENT_SECRET') or "5ed9f86958e24976bef85a190f86a3a0"
sqlHost = os.getenv("MYSQL_HOST") or "mysql"

print(f"Connecting to redis({redisHost} : {redisPort})")
redisClient = redis.StrictRedis(host=redisHost,port=redisPort,db=0)
infoKey = "{}.rest.info".format(platform.node())
debugKey = "{}.rest.debug".format(platform.node())


spotifyQueue = 'toWorker'
def log_debug(message, key=debugKey):
    print("DEBUG:", message, file=sys.stdout)
    redisClient = redis.StrictRedis(host=redisHost, port=redisPort, db=0)
    redisClient.lpush('logging', f"{debugKey}:{message}")

def log_info(message, key=infoKey):
    print("INFO:", message, file=sys.stdout)
    redisClient = redis.StrictRedis(host=redisHost, port=redisPort, db=0)
    redisClient.lpush('logging', f"{infoKey}:{message}")   

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
log_debug('Creating REST frontend')

@app.route('/', methods=['GET'])
def hello():
    return '<h1> Welcome to Voice-based music search service</h1><p> Use a valid endpoint </p>'

@app.route('/spotify/voice', methods=['POST'])
def voice_based_search():
    try:
        data = request.get_json()
        decoded_file = base64.b64decode(data['wav'])
        rec = sr.Recognizer()
        audio_file = sr.AudioFile(io.BytesIO(decoded_file))
        with audio_file as source:
            audio = rec.record(source)
        sentence = rec.recognize_google(audio)
        print("The user's query turned into text:", sentence)
        response = {}
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id = client_id,client_secret = client_secret))
        results = sp.search(q=sentence, limit=10, type='track')
        print('results from the api end point',results)
        for idx, track in enumerate(results['tracks']['items']):
            print(idx, track['name'], track['artists'][0]['name'], track['album']['name'], track['external_urls']['spotify'])
            response[idx] = [track['name'], track['artists'][0]['name'], track['album']['name'], track['external_urls']['spotify']] 
        redisClient.lpush(spotifyQueue,json.dumps(response)) 
        return Response(response =  jsonpickle.encode(response), status = 200, mimetype = "application/json")
    except Exception as exp:
        log_info(f"error in getTrack => exception {exp}")
        print('printing the exception in expect block',exp)
        resp_pickled = jsonpickle.encode("Speech was not recognized, or no valid input was provided")  
        return Response(response = resp_pickled, status = 404, mimetype = "application/json")       

@app.route('/spotify/artist/<string:searchquery>',methods=['GET'])
def searchByArtist(searchquery):
    try:
        mydb = mysql.connector.connect(
                host=sqlHost,
                user="root",
                password="password"
        )
        mycursor = mydb.cursor()
        mycursor.execute("USE spotifydb")
        query = "SELECT * FROM tracks WHERE artist='{}'".format(searchquery)
        mycursor.execute(query)
        results = mycursor.fetchall()
        response_list = []
        for index in range(len(results)):
            new_dict = {}
            new_dict['track_name'] = results[index][1]
            new_dict['artist_name'] = results[index][2]
            new_dict['album_name'] = results[index][3]
            new_dict['spotify_url'] = results[index][4]
            response_list.append(new_dict)
        #info = "Songs found by " + searchquery + ": Track Name: " + results[0][1] + ", Artist Name: " + results[0][2] + ", Album Name: " + results[0][3] + ", Spotify URL: " + results[0][4]
        #print(info)
        response = {
            "tracks": response_list
        }   
        resp_pickled = jsonpickle.encode(response)
        return Response(response = resp_pickled, status = 200, mimetype = "application/json")       
    except Exception as exp:
        log_info(f"error while getting the artist or song {exp}")
        resp_pickled = jsonpickle.encode("error received while getting the search requested")  
        return Response(response = resp_pickled, status = 404, mimetype = "application/json") 
             
app.run(host="0.0.0.0", port=5000)