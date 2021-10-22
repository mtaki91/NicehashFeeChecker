import json
import urllib.request
import playsound
import time

def get_fee():
    try:
        url = 'https://api2.nicehash.com/main/api/v2/public/service/fee/info'
        res = urllib.request.urlopen(url)
        data = json.loads(res.read().decode('utf-8'))

    except urllib.error.HTTPError as e:
        print('HTTPError: ', e)
        return None
    except json.JSONDecodeError as e:
        print('JSONDecodeError: ', e)
        return None

    data = data["withdrawal"]["BITGO"]["rules"]["BTC"]["intervals"][0]["element"]

    value = None
    sndValue = None
    
    if "value" in data:
        value = data["value"]

    if "sndValue" in data:
        sndValue = data["sndValue"]

    return value, sndValue


def main():
    while True:
        ret = get_fee()
        if ret is None:
            print("The fee data is not found.")
        else:
            value, sndValue = ret
            print("Current Fee: {0:.1f}% + {1:.8f} BTC".format(value*100, sndValue) , end = "\r")

            if sndValue < 0.00000101:
                print()
                playsound.playsound("Chime.mp3")
                print("Network fee is low!!")
        
        time.sleep(60)

if __name__ == "__main__":
    main()
