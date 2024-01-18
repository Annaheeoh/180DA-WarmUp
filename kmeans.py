import cv2
import numpy as np

# Function to find dominant color using K-Means
def find_dominant_color(frame, region_of_interest):
    # Extract the region of interest (ROI)
    roi = frame[region_of_interest[1]:region_of_interest[1]+region_of_interest[3],
                region_of_interest[0]:region_of_interest[0]+region_of_interest[2]]

    # Reshape ROI to a list of pixels
    pixels = roi.reshape((-1, 3))

    # Convert pixel values to float
    pixels = np.float32(pixels)

    # Define criteria for K-Means
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)

    # Apply K-Means clustering
    k = 3  # You can adjust the number of clusters
    _, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert the centers to integer values
    centers = np.uint8(centers)

    # Find the most dominant color
    dominant_color = centers[np.argmax(np.unique(labels, return_counts=True)[1])]

    return dominant_color

# Capture video from the default camera
cap = cv2.VideoCapture(0)

# Define the region of interest (central rectangle) [x, y, width, height]
roi = [200, 150, 100, 100]

while True:
    # Read a frame from the video stream
    ret, frame = cap.read()

    # Find the dominant color in the specified region
    dominant_color = find_dominant_color(frame, roi)

    # Draw a rectangle with the dominant color information
    cv2.rectangle(frame, (roi[0], roi[1]), (roi[0] + roi[2], roi[1] + roi[3]), dominant_color.tolist(), -1)

    # Display the frames
    cv2.imshow('Dominant Color', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close windows
cap.release()
cv2.destroyAllWindows()
