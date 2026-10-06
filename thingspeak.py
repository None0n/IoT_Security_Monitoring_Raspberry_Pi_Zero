import requests

from config import (
    THINGSPEAK_URL,
    THINGSPEAK_WRITE_API_KEY
)


def send_to_thingspeak(stats, security_alert):

    data = {

        "api_key": THINGSPEAK_WRITE_API_KEY,

        "field1": stats["download"],

        "field2": stats["upload"],

        "field3": stats["connections"],

        "field4": stats["tcp"],

        "field5": stats["udp"],

        "field6": stats["interfaces"],

        "field7": security_alert,

        "field8": stats["packets"]
    }

    try:

        response = requests.post(
            THINGSPEAK_URL,
            data=data,
            timeout=10
        )

        if response.status_code == 200:

            print(f"ThingSpeak update: {response.text}")

            return True

        else:

            print(f"ThingSpeak error: {response.status_code}")

            return False

    except requests.RequestException as e:

        print(f"Connection error: {e}")

        return False

def send_tel_message(msg):
    data = {
        "user": "just_nobody8",
        "text": msg
    }
    res = requests.post("https://api.callmebot.com/text.php", params=data)
    if res.status_code == 200:
        print(f"Ok callmebot")
    else:
        print("Connection error to callmebot")

