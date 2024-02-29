from flask import Flask, request, jsonify
import cv2
import numpy as np

app = Flask(__name__)

def perform_traffic_analysis(contours):
    return len(contours)

@app.route('/upload', methods=['POST'])
def upload_images():
    images_data = request.files.getlist('images')
    signal_durations = []

    for image_data in images_data:
        nparr = np.frombuffer(image_data.read(), np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Perform image processing tasks
        contours = cv2.findContours(cv2.Canny(cv2.GaussianBlur(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (5, 5), 0), 50, 150),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        
        traffic_count = perform_traffic_analysis(contours)

        # Calculate signal duration based on traffic count
        signal_duration = max(1, traffic_count // 20)
        signal_durations.append(signal_duration)

    # Return signal durations as JSON response
    response = {'signal_durations': signal_durations}
    return jsonify(response)

@app.route('/hello', methods=['POST'])
def upload():
    # Return signal duration as JSON response
    response = {'signal_duration': 1}
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

