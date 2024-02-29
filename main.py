import cv2
import numpy as np
import time

def perform_traffic_analysis(contours):
    return len(contours)

image_paths = [
    "images\\ht1.img",
    "images\\i1.webp",
    "images\\i2.jpg",
    "images\\new.jpg"
]
images = [cv2.resize(cv2.imread(image_path), (400, 200)) for image_path in image_paths]

current_image_index = 0
start_time = time.time()
signal_statuses = [False] * len(images)

while True:
    current_time = time.time()
    elapsed_time = current_time - start_time

    for i, image in enumerate(images):
        if i == current_image_index:
            contours =cv2.findContours(cv2.Canny(cv2.GaussianBlur(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), (5, 5), 0), 50, 150),
                             cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
            traffic_count = perform_traffic_analysis(contours)


            is_green_signal = i == current_image_index and elapsed_time < signal_duration
            signal_statuses[i] = is_green_signal
            print(signal_duration)

            signal_color = (0, 255, 0) if is_green_signal else (0, 0, 255)
            cv2.circle(image, (50, 50), 30, signal_color, -1)

        top_row = np.concatenate([images[0], images[1]], axis=1)
        bottom_row = np.concatenate([images[2], images[3]], axis=1)
        result_frame = np.concatenate([top_row, bottom_row], axis=0)

        cv2.imshow('Combined Images', result_frame)

    for i, image in enumerate(images):
        if i != current_image_index and signal_statuses[current_image_index]:
                
            cv2.circle(image, (50, 50), 30, (0, 0, 255), -1)

    if elapsed_time >= signal_duration:
        current_image_index = (current_image_index + 1) % len(images)
        start_time = current_time

    key = cv2.waitKey(10)
    if key == ord('q'):
        break

cv2.destroyAllWindows()