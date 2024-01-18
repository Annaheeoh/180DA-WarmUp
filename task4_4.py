import cv2
import numpy as np
from sklearn.cluster import KMeans

def find_dominant_color(image, k=3):
    
    # Reshape the image to a 2D array of pixels
    reshaped_image = image.reshape((-1, 3))

    # Appling K-Means clustering with explicit n_init to avoid warning
    clt = KMeans(n_clusters=k, n_init=10)
    clt.fit(reshaped_image)

    # get the cluster with the highest count
    cluster_count = np.bincount(clt.labels_)
    dominant_cluster = np.argmax(cluster_count)

    return clt.cluster_centers_[dominant_cluster]

def main():
    # Start video capture from the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Camera not accessible")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture video")
            break

        # Define the central rectangle dimensions
        h, w = frame.shape[:2]
        center_x, center_y = w // 2, h // 2
        rect_width, rect_height = 100, 100  
        x1, y1 = center_x - rect_width // 2, center_y - rect_height // 2
        x2, y2 = center_x + rect_width // 2, center_y + rect_height // 2

        # extract the central portion of the frame
        central_rect = frame[y1:y2, x1:x2]

        # Finding the dominant color
        dominant_color = find_dominant_color(central_rect, k = 3)
        dominant_color_bgr = tuple([int(val) for val in dominant_color])

        # draw the central rectangle and dominant color
        cv2.rectangle(frame, (x1, y1), (x2, y2), dominant_color_bgr, 5)
        cv2.imshow('Video Feed', frame)

        # break the loop with the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()