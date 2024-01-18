# reference: 
import cv2
import numpy as np
from sklearn.cluster import KMeans

def find_dominant_color(image, k=3):
    reshaped_image = image.reshape((-1, 3))
    clt = KMeans(n_clusters=k, n_init=10)
    clt.fit(reshaped_image)
    cluster_count = np.bincount(clt.labels_)
    dominant_cluster = np.argmax(cluster_count)
    return clt.cluster_centers_[dominant_cluster]

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Camera not accessible")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture video")
            break

        h, w = frame.shape[:2]

        # Define a larger central rectangle
        rect_width, rect_height = 220, 220
        x1, y1 = (w - rect_width) // 2, (h - rect_height) // 2
        x2, y2 = x1 + rect_width, y1 + rect_height

        central_rect = frame[y1:y2, x1:x2]

        dominant_color = find_dominant_color(central_rect, k=3)
        dominant_color_bgr = tuple([int(val) for val in dominant_color])

        cv2.rectangle(frame, (x1, y1), (x2, y2), dominant_color_bgr, 5)
        cv2.imshow('task4 - dominant color', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
