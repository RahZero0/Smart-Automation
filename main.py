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

while True:
    images = [cv2.resize(image, (400, 200)) for image in images]

    top_row = np.concatenate([images[0], images[1]], axis=1)
    bottom_row = np.concatenate([images[2], images[3]], axis=1)
    result_frame = np.concatenate([top_row, bottom_row], axis=0)

    gray_images = [cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) for image in images]

    blurred_images = [cv2.GaussianBlur(gray_image, (5, 5), 0) for gray_image in gray_images]

    edges_images = [cv2.Canny(blurred_image, 50, 150) for blurred_image in blurred_images]

    contours_images = [cv2.findContours(edges_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] for edges_image in edges_images]

    traffic_counts = [perform_traffic_analysis(contours) for contours in contours_images]

    for i, count in enumerate(traffic_counts):
        print(f'Traffic on Image {i + 1}: {count}')

    cv2.imshow('Combined Images', result_frame)

    time.sleep(10)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()