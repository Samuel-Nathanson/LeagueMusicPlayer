import requests
import time
import json

# Simple polling of web server to get back champion name when game starts
class PollingEngine():

    def __init__(self, verify_ssl = True, interval = 5):
        self.host_port = "https://127.0.0.1:2999/"
        self.get_summoner_name_endpoint = "liveclientdata/activeplayername"
        self.get_active_player_list_endpoint = "liveclientdata/playerlist"

        self.interval = interval
        self.verify_ssl = verify_ssl

    def get_active_champion(self):

        summoner_name = self.get_summoner_name()
        if summoner_name == None:
            return None

        # Make request to webserver for champion name
        try:
            response = requests.get(self.host_port + self.get_active_player_list_endpoint, verify = self.verify_ssl)
            if response.status_code != 200:
                print(json.dumps(response.json()))
            else:
                for player in response.json():
                    if player["summonerName"] == summoner_name:
                        return player["championName"]
        except requests.exceptions.RequestException as e:
            print(e) # This should probably never happen
        
        return None

    # Make request to webserver for summoner name
    # Do not cache summoner_name to handle account switching
    def get_summoner_name(self):

        summoner_name = None
        
        try:
            response = requests.get(self.host_port + self.get_summoner_name_endpoint, verify = self.verify_ssl)
            if response.status_code == 200:
                summoner_name = response.json()
            elif response.status_code == 404:
                print("Response returned HTTP 404 - In loading screen") # TODO potentially try again sooner or see if other endpoints are available
            else:
                print("Unexpected response!")
                print(json.dumps(response.json()))
        except requests.exceptions.RequestException as e:
            print("RequestException - Likely out of game")

        return summoner_name

    # Poll server on some interval
    def poll_loop(self):
        while True:
            print(self.get_active_champion())
            time.sleep(self.interval)



if __name__ == "__main__":

    # Supress SSL #TODO enable SSL
    requests.packages.urllib3.disable_warnings()

    # init polling engine
    engine = PollingEngine(verify_ssl = False)
    engine.poll_loop()

"""
 Findings:
 Connections will be refused while league client is closed
 In loading screen endpoints will return 404s

 TODO
 Check sooner if user is in loading screen
 Implement async functions
 See if SSL works on windows machines
 Maybe implement logger
"""