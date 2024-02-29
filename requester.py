import requests

# List of image paths
image_paths = [
    "images\\ht1.img",
    "images\\i1.webp",
    "images\\i2.jpg",
    "images\\new.jpg"
]

# Prepare data for the POST request
files = [('images', open(image_path, 'rb')) for image_path in image_paths]

# Make the POST request to the Flask route
response = requests.post('http://localhost:5000/upload', files=files)

# Print the response
if response.status_code == 200:
    print("Signal durations:", response.json()['signal_durations'])
else:
    print("Error:", response.status_code)
