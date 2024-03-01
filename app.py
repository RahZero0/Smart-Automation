from flask import Flask, request, jsonify
import cv2

app = Flask(__name__)

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

@app.route('/hello', methods=['POST'])
def upload():
    request_data = request.get_data(as_text=True)

    each_image = [i.split(": ")[1].strip('"') for i in request_data.split(",")]

    contour_count = [get_contour_count(i) for i in each_image]

    # Calculate total contour count
    total_contour_count = sum(contour_count)

    # Calculate ratio for each image
    ratios = [count / total_contour_count for count in contour_count]

    # Scale ratios to ensure their sum is 9000

    if len(contour_count)>=4:
        total_mins = 90000
    elif len(contour_count)==3:
        total_mins = 70000
    elif len(contour_count==2):
        total_mins = 50000

    scaled_ratios = [[ index+1, (ratio * total_mins)-7000, 7000] for index, ratio in enumerate(ratios)]

    return {'signal_duration': scaled_ratios}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

