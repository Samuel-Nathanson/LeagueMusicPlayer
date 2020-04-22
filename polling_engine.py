import requests
import time
import json

# Simple polling of web server to get back champion name when game starts

host_port = "https://127.0.0.1:2999/"
get_summoner_name_endpoint = "liveclientdata/activeplayername"
get_active_player_list_endpoint = "liveclientdata/playerlist"

def check_in_game():
    
    # Make request to webserver
    try:
        response = requests.get(host_port + get_summoner_name_endpoint, verify = False)
        if response.status_code == 200:
            summoner_name = response.json()
        elif response.status_code == 404:
            print("Response returned HTTP 404 - In loading screen") # TODO potentially try again sooner or see if other endpoints are available
            return
        else:
            print("Unexpected response!")
            print(json.dumps(response.json()))
            return
    except requests.exceptions.RequestException as e:
        print("RequestException - Likely out of game")
        return

    # Get champion name
    try:
        response = requests.get(host_port + get_active_player_list_endpoint, verify = False)
        if response.status_code != 200:
            print(json.dumps(response.json()))
        else:
            for player in response.json():
                if player["summonerName"] == summoner_name:
                    print(player["championName"])
    except requests.exceptions.RequestException as e:
        print(e) # This should probably never happen
        return

# Poll server on some interval
def polling_loop(interval):
    while True:
        check_in_game()
        time.sleep(interval)

# Supress SSL #TODO enable SSL
requests.packages.urllib3.disable_warnings()

polling_loop(5)


"""
 Findings:
 Connections will be refused while league client is closed
 In loading screen endpoints will return 404s
"""