import requests
import json, jsonpickle
import os
import sys
import base64
import glob

REST = os.getenv("REST") or "localhost"

def mkReq(reqmethod, endpoint, data, verbose=True):
    print(f"Response to http://{REST}/{endpoint} request is {type(data)}")
    jsonData = jsonpickle.encode(data)
    if verbose and data != None:
        print(f"Make request http://{REST}/{endpoint} with json {data.keys()}")
        print(f"wav is of type {type(data['wav'])} and length {len(data['wav'])} ")
    response = reqmethod(f"http://{REST}/{endpoint}", data=jsonData,
                         headers={'Content-type': 'application/json'})
    if response.status_code == 200:
        jsonResponse = json.dumps(response.json(), indent=4, sort_keys=True)
        print(jsonResponse)
        return
    else:
        print(
            f"response code is {response.status_code}, raw response is {response.text}")
        return response.text


for wav in glob.glob("data/*.wav"):
    #print(f"Separate data/{wav}")
    mkReq(requests.post, "spotify/voice",
        data={
            "wav": base64.b64encode( open(wav, "rb").read() ).decode('utf-8'),
            "callback": {
                "url": "http://localhost:5000",
                "data": {"wav": wav, 
                         "data": "to be returned"}
            }
        },
        verbose=True
        )
    print(f"Cache from server is")
    #mkReq(requests.get, "spotify/artist/Wallows", data=None)

sys.exit(0)