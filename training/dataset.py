import os
import shutil
import cv2
from tqdm import tqdm

# ================================
# 📂 PATHS (Updated for your structure)
# ================================
# Ab hum 'raw_data' folder ko scan karenge jahan organizer ne data phenka hai
RAW_DATA_DIR = "raw_data" 
OUTPUT_DIR = "data/processed"
IMG_SIZE = 224

# Purana processed data saaf karo taaki fresh start ho
if os.path.exists(OUTPUT_DIR):
    print("🧹 Cleaning old processed data...")
    shutil.rmtree(OUTPUT_DIR)

os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"🚀 Processing images from: {RAW_DATA_DIR}")

count = 0
error_count = 0

# 1. Check karo folder exist karta hai ya nahi
if not os.path.exists(RAW_DATA_DIR):
    print(f"❌ Error: {RAW_DATA_DIR} folder nahi mila! Pehle organizer chalao.")
    exit()

# Har bimari ke folder ko loop mein lo (Acne, Melanoma, etc.)
classes = [d for d in os.listdir(RAW_DATA_DIR) if os.path.isdir(os.path.join(RAW_DATA_DIR, d))]

if not classes:
    print("❌ Error: raw_data ke andar koi folders nahi mile!")
    exit()

for class_name in classes:
    class_path = os.path.join(RAW_DATA_DIR, class_name)
    
    print(f"\n📁 Processing Class: {class_name}")
    
    # Processed folder ke andar class folder banao
    dst_dir = os.path.join(OUTPUT_DIR, class_name)
    os.makedirs(dst_dir, exist_ok=True)
    
    # Folder ki sari images loop mein lo
    files = os.listdir(class_path)
    for img_name in tqdm(files, desc=f"Resizing {class_name}"):
        # Sirf images ko process karo
        if not img_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            continue

        try:
            src_path = os.path.join(class_path, img_name)
            
            # Image ko read karo
            img = cv2.imread(src_path)
            if img is None:
                error_count += 1
                continue
                
            # Resize karo (224x224 standard hai Deep Learning ke liye)
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
            
            # Save karo
            dst_path = os.path.join(dst_dir, img_name)
            cv2.imwrite(dst_path, img)
            
            count += 1
        except Exception as e:
            error_count += 1
            continue

print(f"\n✅ All Set, Bhai!")
print(f"📊 Total images processed: {count}")
print(f"⚠️ Errors/Corrupt images: {error_count}")
print(f"📂 Final dataset ready in: {OUTPUT_DIR}")