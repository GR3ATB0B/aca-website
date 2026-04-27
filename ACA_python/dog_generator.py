import requests
import time
from PIL import Image
from io import BytesIO


def get_random_dog():
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    data = response.json()
    return data["message"]


def main():
    print("=== Random Dog Image Generator ===")
    print("A new dog will appear every second. Press Ctrl+C to stop.\n")
    try:
        while True:
            url = get_random_dog()
            breed = url.split("/")[4].replace("-", " ").title()
            print(f"Breed: {breed}")
            img_data = requests.get(url)
            img = Image.open(BytesIO(img_data.content))
            img.show()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nGoodbye!")


if __name__ == "__main__":
    main()
