# 010101110110100001100101011011100010000001101100011010010110011001100101001000000110011101101001011101100110010101110011001000000111100101101111011101010010000001101100011001010110110101101111011011100111001100101100001000000110110101100001011010110110010100100000011011000110010101101101011011110110111001100001011001000110010100101110
import eel
from screeninfo import get_monitors
from valclient.client import Client
import os
import psutil

SCREEN_DIMENSIONS = (
    list(get_monitors())[0].width // 1.7,
    list(get_monitors())[0].height // 1.7,
) # get the screen dimensions of the primary monitor and divide them by 1.7 so the window is not too big

LOOP_DELAY = 4
LOCK_DELAY = 0
HOVER_DELAY = 0

AGENT = None
SEEN_MATCHES = []
RUNNING = False

AGENT_CODES = {
    "Jett": "add6443a-41bd-e414-f6ad-e58d267f4e95",
    "Reyna": "a3bfb853-43b2-7238-a4f1-ad90e9e46bcc",
    "Raze": "f94c3b30-42be-e959-889c-5aa313dba261",
    "Yoru": "7f94d92c-4234-0a36-9646-3a87eb8b5c89",
    "Phoenix": "eb93336a-449b-9c1b-0a54-a891f7921d69",
    "Neon": "bb2a4828-46eb-8cd1-e765-15848195d751",
    "Breach": "5f8d3a7f-467b-97f3-062c-13acf203c006",
    "Skye": "6f2a04ca-43e0-be17-7f36-b3908627744d",
    "Sova": "320b2a48-4d9b-a075-30f1-1f93a9b638fa",
    "Kayo": "601dbbe7-43ce-be57-2a40-4abd24953621",
    "Killjoy": "1e58de9c-4950-5125-93e9-a0aee9f98746",
    "Cypher": "117ed9e3-49f3-6512-3ccf-0cada7e3823b",
    "Sage": "569fdd95-4d10-43ab-ca70-79becc718b46",
    "Chamber": "22697a3d-45bf-8dd7-4fec-84a9e28c69d7",
    "Omen": "8e253930-4c05-31dd-1b6c-968525494517",
    "Brimstone": "9f0d8ba9-4140-b941-57d3-a7ad57c6b417",
    "Astra": "41fb69c1-4189-7b37-f117-bcaf1e96f1bf",
    "Viper": "707eab51-4836-f488-046a-cda6bf494859",
    "Fade": "dade69b4-4f5a-8528-247b-219e5a1facd6",
    "Harbor": "95b78ed7-4637-86d9-7e41-71ba8c293152",
    "Gekko": "e370fa57-4757-3604-3648-499e1f642d3f",
    "Deadlock": "cc8b64c8-4b25-4ff9-6e7f-37b4da43d235",
    "Iso": "0e38b510-41a8-5780-5e8f-568b2a4f2d6c",
} # aids but i was too lazy to write a function to get the agent codes from the api

def get_region():
    """ get the region code from the log file """
    with open(
        os.path.join(os.getenv("LOCALAPPDATA"), R"VALORANT\Saved\Logs\ShooterGame.log"),
        "rb",
    ) as f:
        lines = f.readlines()
    for line in lines:
        if b"regions" in line:
            region = line.split(b"regions/")[1].split(b"]")[0]
            return region.decode()


def errorAlert(line1, line2, time):
    """ show an error alert """
    eel.alertUser(line1, line2)
    eel.sleep(time)
    eel.askUserToChooseAgent()


@eel.expose
def stop_lock():
    """ stops the lock process """
    global RUNNING
    global AGENT
    RUNNING = False
    eel.hideStopButton()


@eel.expose
def try_lock(agent):
    """ try to lock the agent """
    global RUNNING
    global AGENT
    global SEEN_MATCHES

    # if val aint running then start crying
    if not "VALORANT.exe" in (p.name() for p in psutil.process_iter()):
        if RUNNING:
            stop_lock()
        return errorAlert("START VALORANT", "I THINK", 3)

    try:
        region_code = get_region()
    except:
        if RUNNING:
            stop_lock()
        return errorAlert("COULD NOT FIND REGION", "TRY LOGGING IN AGAIN", 5)

    if (
        RUNNING
    ):
        AGENT = AGENT_CODES[agent]
        return

    try:
        client = Client(region=region_code) # create a client object with the region code we got earlier from the log file
    except ValueError:
        return errorAlert("COULD NOT FIND REGION", "TRY LOGGING IN AGAIN", 5)

    client.activate() # activate the client

    RUNNING = True # set the running variable to true so we can stop the loop later

    while RUNNING: # loop until RUNNING is false
        eel.sleep(LOOP_DELAY) # sleep for the delay so we dont spam the api (gulp)

        if not RUNNING:
            return # sittim is the opposite of runnim aroum

        try:
            sessionState = client.fetch_presence(client.puuid)["sessionLoopState"] # get the session state of the client (pre-game, in-game, etc)
            matchID = client.pregame_fetch_match()["ID"] # get the match id of the current match the client is in

            if sessionState == "PREGAME" and matchID not in SEEN_MATCHES: # if the client is in pregame and the match id is not in the seen matches list
                SEEN_MATCHES.append(
                    matchID
                ) # add the match id to the seen matches list so we dont try to lock the agent again

                eel.changeStatus("LOCKING") # change the status to locking so the user knows we are locking the agent

                if not AGENT:
                    AGENT = AGENT_CODES[agent] # get the agent code from the agent name

                eel.sleep(HOVER_DELAY) # useless but some people wanted this so it doesnt look too obvious that we're intaloking
                client.pregame_select_character(AGENT) # select the agent (this is not the same as locking the agent)

                eel.sleep(LOCK_DELAY)
                client.pregame_lock_character(AGENT) # lock the agent

                stop_lock() # stop the lock process and change the status to locked

                eel.changeStatus("LOCKED")

                return True

        except Exception as e:
            if "pre-game" not in str(e):
                errorAlert("ERROR", e, 12)
                stop_lock()
                return

eel.init("web") # initialize eel with the web folder as the root folder
eel.start("index.html", size=(SCREEN_DIMENSIONS), port=0) # start the eel app with the index.html file as the main file and the screen dimensions as the window size
