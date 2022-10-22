from random import randint
import requests

#https://xkcd.com/2688/ last address
def getImageXKCD():
    """Return a random image from xkcd"""
    num = randint(1,2688)
    response = requests.get(f"https://xkcd.com/{num}/info.0.json")
    data = response.json()
    try:
        image = data["img"]
        return image
    except:
        return f"https://xkcd.com/{num}/"


if __name__ == "__main__":
    getImageXKCD()