import numpy as np

def detect_skin_tone(image):
    try:
        img = np.array(image)

        # brightness estimate
        mean_brightness = np.mean(img)

        if mean_brightness > 180:
            return "Light"
        elif mean_brightness > 120:
            return "Medium"
        else:
            return "Dark"

    except Exception as e:
        print("Skin tone error:", e)
        return "Unknown"