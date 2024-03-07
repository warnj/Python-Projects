import os
import pytesseract
from PIL import Image
import re


def extract_text_from_image(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Use pytesseract to extract text from the image
        text = pytesseract.image_to_string(img)
    return text


def extract_gps_coordinates_from_text(text):
    # Regular expression pattern to match GPS coordinates
    pattern = r"(\d{1,2}\.\d+), (\d{1,3}\.\d+)"
    matches = re.findall(pattern, text)
    coordinates = []
    for match in matches:
        latitude = float(match[0])
        longitude = float(match[1])
        coordinates.append((latitude, longitude))
    return coordinates


def main(directory):
    # Iterate through each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            image_path = os.path.join(directory, filename)
            text = extract_text_from_image(image_path)
            gps_coordinates = extract_gps_coordinates_from_text(text)

            print(f"Image: {image_path}")
            print(f"Text extracted: {text}")
            if gps_coordinates:
                print(f"GPS Coordinates: {gps_coordinates}\n")
            else:
                print('no gps coords found')


if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    directory = 'D:\\Pictures\\All\\Underwater\\Books\\Northwest'
    main(directory)
