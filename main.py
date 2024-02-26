import cv2
import numpy as np
def perform_traffic_analysis(images):
    import random
    return random.randint(0, 100)

image_paths = [
    "C:\\Users\\arunb\\OneDrive\\Desktop\\Hackathon\\ht1.img",
    "C:\\Users\\arunb\\OneDrive\\Desktop\\Hackathon\\i1.webp",
    "C:\\Users\\arunb\\OneDrive\\Desktop\\Hackathon\\i2.jpg",
    "C:\\Users\\arunb\\OneDrive\\Desktop\\Hackathon\\i3",
]

images = [cv2.resize(cv2.imread(image_path), (400, 200)) for image_path in image_paths]

while True:
    images = [cv2.resize(image, (400, 200)) for image in images]

    top_row = np.concatenate([images[0], images[1]], axis=1)
    bottom_row = np.concatenate([images[2], images[3]], axis=1)
    result_frame = np.concatenate([top_row, bottom_row], axis=0)

    cv2.imshow('Combined Images', result_frame)

    traffic_count = perform_traffic_analysis(images)

    print(f'Traffic Count: {traffic_count}')

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()