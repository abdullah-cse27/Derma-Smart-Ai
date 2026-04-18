# FILE_NAME: app/utils/image.py

import cv2
import numpy as np
try:
    from config import IMAGE_SIZE
except ImportError:
    # Default fallback agar config load na ho sake
    IMAGE_SIZE = (224, 224)

def preprocess_image(image):
    """
    PURANA RELIABLE LOGIC:
    Isme koi 'Lighting Normalization' nahi hai jo accuracy bigade.
    Sirf Resize aur Simple Scaling hai.
    """
    try:
        # 1. PIL Image ko Numpy (RGB) mein convert karna
        img_array = np.array(image)

        # 2. Resize to (224, 224) - Jo tumhare model ki requirement hai
        img_resized = cv2.resize(img_array, IMAGE_SIZE)

        # 3. Normalization (0 se 1 ke beech pixels)
        # Note: Agar tune MobileNetV2 preprocess use kiya tha, 
        # toh isline ko badal kar: (img_resized.astype('float32') / 127.5 - 1.0) kar dena.
        img_final = img_resized.astype('float32') / 255.0

        # 4. Batch Dimension add karna (1, 224, 224, 3)
        img_final = np.expand_dims(img_final, axis=0)

        return img_final

    except Exception as e:
        print(f"❌ Error in Image Preprocessing: {e}")
        return None

def resize_for_display(image):
    """Sirf UI par dikhane ke liye bina kisi change ke"""
    img_array = np.array(image)
    return cv2.resize(img_array, IMAGE_SIZE)