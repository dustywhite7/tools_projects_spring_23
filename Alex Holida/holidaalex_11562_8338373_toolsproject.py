import os

import face_recognition
import requests
import json
from datetime import datetime


def main():
    # Set up a Bing image search query using my Bing API
    subscription_key = "f9962b455f0f4ba08c98e0f21c7dedd9"
    search_url = "https://api.bing.microsoft.com/v7.0/images/search"
    search_query = "Captain Ibrahim Traore"

    # Define headers with subscription key
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}

    # Define the start and end dates for the time frame - this is optional,
    # but I wanted to narrow down the search parameters to when Capt Traore took power.
    end_date = datetime.now()
    start_date = datetime(2022, 12, 1)

    # Format the dates as strings in the correct format for the API
    start_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_date_str = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Make an HTTP GET request to the search endpoint with the freshness parameter
    response = requests.get(search_url, headers=headers, params={
        "q": search_query,
        "freshness": "Month",
        "dateRestriction": f"{start_date_str}..{end_date_str}"
    })

    # Extract the image URLs from the search results if the response is not empty
    results = json.loads(response.content)
    if "value" in results:
        image_urls = [result["contentUrl"] for result in results["value"]]
        # Process the image URLs
    else:
        print("No images found for the search query.")
        exit(0)

    # Loop through the image URLs, load each image, encode the faces, and compare to the known encoding
    known_image_url = "https://static.dw.com/image/64358257_804.jpg"

    image_dir = "images"
    if not os.path.exists(image_dir):
        os.mkdir(image_dir)


    # Download the file locally
    known_file_name = download_image_locally(image_dir, known_image_url)
    known_image = face_recognition.load_image_file(known_file_name)
    known_encoding = face_recognition.face_encodings(known_image)[0]

    for image_url in image_urls:
        try:
            # Load the image from the URL and encode the faces in it
            img_name = download_image_locally(image_dir, image_url)
            unknown_image = face_recognition.load_image_file(img_name)
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

            # Compare the face encodings and print the result
            results = face_recognition.compare_faces([known_encoding], unknown_encoding, 0.1)
            if results:
                print(f"Match found {image_url}!")
            else:
                print(f"No match found {image_url}.")
        except Exception as e:
            print(f"Error processing image {image_url}: {e}")


def download_image_locally(directory: str, url: str) -> str:
    img_data = requests.get(url).content
    image_name = url.split("/")[-1]
    full_path = f'{directory}/{image_name}'
    with open(full_path, 'wb') as handler:
        handler.write(img_data)
    return full_path


# Go download a bunch of pictures of Vlad and loop over each one
# getting the encoding for it.
def get_known_image_encoding(image_dir: str, image_path: str):
    known_image = face_recognition.load_image_file(f'{image_dir}/{image_path}')
    return face_recognition.face_encodings(known_image)[0]


def encode_all_known_images():
    # something like this...
    known_image_dir = "known_images"

    known_image_encodings = []
    for known_image in os.listdir(known_image_dir):
        encoding = get_known_image_encoding(known_image_dir, known_image)
        if len(encoding):
            known_image_encodings.append(encoding)
    return known_image_encodings


if __name__ == '__main__':
    main()
