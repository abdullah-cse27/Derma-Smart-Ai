import numpy as np
import tensorflow as tf
import cv2

from models.loader import load_model
from utils.image import preprocess_image

model = None

def generate_heatmap(image):
    global model
    if model is None:
        model = load_model()

    try:
        # =========================
        # 🧠 STEP 1: PREPROCESS
        # =========================
        img = preprocess_image(image)

        if img is None:
            return None

        # =========================
        # 🔥 STEP 2: GRAD-CAM MODEL
        # =========================
        # 🔥 Automatically find last Conv layer
        last_conv_layer = None

        for layer in reversed(model.layers):
            if isinstance(layer, tf.keras.layers.Conv2D):
                last_conv_layer = layer.name
                break

        if last_conv_layer is None:
            print("No Conv layer found")
            return None

        last_conv_layer_name = last_conv_layer

        grad_model = tf.keras.models.Model(
            inputs=model.inputs,
            outputs=[
                model.get_layer(last_conv_layer_name).output,
                model.output
            ]
        )

        # =========================
        # 📊 STEP 3: GRADIENTS
        # =========================
        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img)
            pred_index = int(tf.argmax(predictions[0]))
            loss = predictions[:, pred_index]

        grads = tape.gradient(loss, conv_outputs)

        if grads is None:
            print("Gradients are None")
            return None

        # =========================
        # 🎯 STEP 4: WEIGHTED MAP
        # =========================
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        conv_outputs = conv_outputs[0]

        heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)

        # =========================
        # 🧼 STEP 5: NORMALIZATION
        # =========================
        heatmap = np.maximum(heatmap, 0)

        if hasattr(heatmap, "numpy"):
            heatmap = heatmap.numpy()

        # Normalize to 0–1
        heatmap = heatmap / (np.max(heatmap) + 1e-8)

        # =========================
        # 🎨 STEP 6: SMOOTHING
        # =========================
        heatmap = cv2.resize(heatmap, (224, 224))

        # 🔥 Smooth edges (IMPORTANT)
        heatmap = cv2.GaussianBlur(heatmap, (15, 15), 0)

        # Convert to 0–255
        heatmap = np.uint8(255 * heatmap)

        # =========================
        # 🖼️ STEP 7: ORIGINAL IMAGE
        # =========================
        original = np.array(image.resize((224, 224))).astype("uint8")

        # =========================
        # 🌈 STEP 8: COLOR MAP
        # =========================
        heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

        # 🔥 Extra smoothing for better visual
        heatmap_color = cv2.GaussianBlur(heatmap_color, (15, 15), 0)

        # =========================
        # 🎯 STEP 9: BALANCED OVERLAY
        # =========================
        superimposed = cv2.addWeighted(original, 0.6, heatmap_color, 0.4, 0)

        return superimposed

    except Exception as e:
        print("Heatmap error:", e)
        return None