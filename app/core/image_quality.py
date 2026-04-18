import numpy as np
import cv2

def check_image_quality(image):
    try:
        img = np.array(image)

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # Blur detection (Laplacian variance)
        blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

        # Brightness check
        brightness = np.mean(gray)

        # Decision logic
        if blur_score < 50:
            return "Low"
        elif brightness < 50:
            return "Dark"
        else:
            return "Good"

    except Exception as e:
        print("Image quality error:", e)
        return "Unknown"