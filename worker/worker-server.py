import jsonpickle, pickle
import io, os, sys
import platform
import redis
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import mysql.connector


redisHost = os.getenv("REDIS_HOST") or "localhost"
redisPort = os.getenv("REDIS_PORT") or 6379
sqlHost = os.getenv("MYSQL_HOST") or "mysql"
sqlPort = os.getenv("MYSQL_PORT") or 3306


redisClient = redis.StrictRedis(host=redisHost,port=redisPort,db=0)

infoKey = "{}.rest.info".format(platform.node())
debugKey = "{}.rest.debug".format(platform.node())


def log_debug(message, key=debugKey):
    print("DEBUG:", message, file=sys.stdout)
    redisClient = redis.StrictRedis(host=redisHost, port=redisPort, db=0)
    redisClient.lpush('logging', f"{debugKey}:{message}")

def log_info(message, key=infoKey):
    print("INFO:", message, file=sys.stdout)
    redisClient = redis.StrictRedis(host=redisHost, port=redisPort, db=0)
    redisClient.lpush('logging', f"{infoKey}:{message}")

log_debug(f"Connecting to redis({redisHost} : {redisPort})")      

def callback(response_dict):
    try:
        log_debug("Inside the callback method")
        mydb = mysql.connector.connect(host=sqlHost,
        user="root",
        password="password")
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS spotifydb")
        mycursor.execute("USE spotifydb")
        mycursor.execute("CREATE TABLE IF NOT EXISTS tracks (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), artist VARCHAR(255), album_name VARCHAR(255), url VARCHAR(255))")
        sql = "INSERT INTO tracks (name, artist, album_name, url) VALUES (%s, %s, %s, %s)"
        log_debug('saving the reponse',response_dict)
        response = json.loads(response_dict)
        print(response)
        list_values = []
        for index in range(len(response)):
            dict_key = str(index)
            list_values.append((response[dict_key][0],response[dict_key][1],response[dict_key][2],response[dict_key][3]))
        mycursor.executemany(sql, list_values)
        mydb.commit()  
    except Exception as exp:
        print(f"Exception occurred => {exp}")
        log_info(f"Exception raised in log loop: {str(exp)}")

while True:
    try:
        log_debug("consumption by the redis started")
        work = redisClient.blpop("toWorker", timeout=0)
        log_debug(f"contents worker {work}")
        string_key = work[0].decode('utf-8')
        response_dict = work[1].decode('utf-8')
        log_debug('string key :',string_key)
        log_debug('response_dict :', response_dict)
        if string_key == 'toWorker':
            callback(response_dict)
    except Exception as exp:
        log_info("Exception raised in log loop: {str(exp)}")
        print(f"Exception raised in log loop: {str(exp)}")
    sys.stdout.flush()
    sys.stderr.flush()