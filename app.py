from flask import Flask, request, jsonify, render_template
import cv2
import shutil
import os

app = Flask(__name__)

base_names = ["12.jpg"]
multiplicative_ratio = [0]


def copy_images_to_static(image_paths):
    # Destination directory where images will be copied
    destination_dir = 'static/images/'

    # Create the destination directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)

    base_names_array = []

    # Copy each image to the destination directory
    for image_path in image_paths:
        # Extract the filename from the image path
        filename = os.path.basename(image_path)
        # Construct the destination path
        destination_path = os.path.join(destination_dir, filename)
        # Copy the image to the destination directory
        shutil.copy(image_path, destination_path)
        
        base_names_array.append(filename)
    
    return base_names_array


# function for /hello
def get_contour_count(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Resize the image if needed
    image = cv2.resize(image, (400, 200))

    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Detect edges using Canny
    edges = cv2.Canny(blurred, 50, 150)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Return number of contours
    return len(contours)

@app.route('/')
def index():
    return render_template('index.html', buffered_data=base_names, multiple_ratio=multiplicative_ratio)

@app.route('/hello', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        request_data = request.get_data(as_text=True)

        global base_names
        each_image = [i.strip('"') for i in request_data.split(", ")]

        base_names = copy_images_to_static(each_image)

        contour_count = [get_contour_count(i) for i in each_image]

        # Calculate total contour count
        total_contour_count = sum(contour_count)

        # Calculate ratio for each image
        ratios = [count / total_contour_count for count in contour_count]

        # Scale ratios to ensure their sum is 9000

        print(len(each_image))

        if len(each_image)>=4:
            total_mins = 90000
        elif len(each_image)==3:
            total_mins = 70000
        elif len(each_image)==2:
            total_mins = 50000

        scaled_ratios = [ratio * total_mins for ratio in ratios]
        global multiplicative_ratio

        multiplicative_ratio = [i / 2 for i in scaled_ratios]

        return multiplicative_ratio

    # If it's a GET request, simply render the template
    return render_template('index.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
