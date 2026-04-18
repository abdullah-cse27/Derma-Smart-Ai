import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models, callbacks
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import os
import json
import numpy as np
from sklearn.utils import class_weight

# ================================
# ⚙️ CONFIGURATION
# ================================
DATA_DIR = "data/processed"
MODEL_DIR = "model"
IMG_SIZE = (224, 224)
BATCH_SIZE = 64 # 🚀 Batch size badha diya taaki training fast ho (Agar GPU memory allow kare)

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# ================================
# 📸 DATA GENERATORS (Optimized for Speed)
# ================================
datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    validation_split=0.2,
    rotation_range=20,     # Thoda kam kiya taaki training fast ho
    horizontal_flip=True,
    fill_mode='nearest'
)

train_data = datagen.flow_from_directory(
    DATA_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE,
    class_mode='categorical', subset='training'
)

val_data = datagen.flow_from_directory(
    DATA_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE,
    class_mode='categorical', subset='validation'
)

# 🔥 SAVE CLASS MAPPING (Always do this first)
class_indices = train_data.class_indices
labels = {v: k for k, v in class_indices.items()}
with open(os.path.join(MODEL_DIR, "classes.json"), "w") as f:
    json.dump(labels, f, indent=4)

# ================================
# 🧠 MODEL ARCHITECTURE
# ================================
base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
base_model.trainable = False 

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(256, activation='relu'), # Optimized size
    layers.BatchNormalization(),
    layers.Dropout(0.4),
    layers.Dense(train_data.num_classes, activation='softmax')
])

# ================================
# 🏗️ PHASE 1: QUICK WARM UP (3-5 Epochs)
# ================================
print("🏗️ Phase 1: Quick Warm up...")
model.compile(optimizer=tf.keras.optimizers.Adam(2e-3), # High learning rate for speed
              loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(train_data, validation_data=val_data, epochs=4) 

# ================================
# 🚀 PHASE 2: AGGRESSIVE FINE-TUNING
# ================================
print("🚀 Phase 2: Fine-Tuning...")
base_model.trainable = True

# Sirf top 30-40 layers unfreeze karo, MobileNet ke liye kafi hai
for layer in base_model.layers[:-30]:
    layer.trainable = False

# Bahut zaroori: ReduceLROnPlateau taaki agar accuracy na badhe toh ye LR kam kar de
reduce_lr = callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6)
early_stop = callbacks.EarlyStopping(monitor='val_accuracy', patience=8, restore_best_weights=True)
checkpoint = callbacks.ModelCheckpoint(os.path.join(MODEL_DIR, "skin_model_best.h5"), 
                                     monitor='val_accuracy', save_best_only=True)

model.compile(optimizer=tf.keras.optimizers.Adam(1e-4), 
              loss='categorical_crossentropy', metrics=['accuracy'])

print("🔥 Starting Deep Training (Fast Mode)...")
try:
    model.fit(
        train_data,
        validation_data=val_data,
        epochs=30, # 50 ki zaroorat nahi padegi, EarlyStop rok dega
        callbacks=[checkpoint, early_stop, reduce_lr]
    )
    model.save(os.path.join(MODEL_DIR, "skin_model_final.h5"))
    print("\n✅ Training Complete! Ab parson aag laga dena!")
except Exception as e:
    print(f"❌ Error: {e}")