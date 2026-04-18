import streamlit as st
from PIL import Image


def upload_image():
    """
    Enhanced Image Uploader UI (Card-based + Preview + UX polish)
    """

    # =========================
    # 🎨 LOCAL STYLING
    # =========================
    st.markdown("""
    <style>
    .upload-card {
        padding: 15px;
        border-radius: 14px;
        background: rgba(255,255,255,0.06);
        backdrop-filter: blur(6px);
        border: 1px dashed rgba(255,255,255,0.2);
        text-align: center;
        margin-bottom: 10px;
    }

    .upload-text {
        font-size: 14px;
        opacity: 0.8;
    }

    .success-box {
        padding: 8px;
        border-radius: 10px;
        background: rgba(46, 204, 113, 0.2);
        margin-top: 10px;
        text-align: center;
    }

    </style>
    """, unsafe_allow_html=True)

    # =========================
    # 📤 HEADER
    # =========================
    st.markdown("### 📤 Upload Skin Image")

    # =========================
    # 📦 UPLOAD CARD
    # =========================
    st.markdown("""
    <div class="upload-card">
        <p class="upload-text">Drag & Drop Image or Click Below</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "",
        type=["jpg", "jpeg", "png"]
    )

    # =========================
    # 🖼️ IMAGE PREVIEW
    # =========================
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)

            st.image(image, use_container_width=True)

            # Success message
            st.markdown("""
            <div class="success-box">
                ✅ Image uploaded successfully
            </div>
            """, unsafe_allow_html=True)

            return image

        except Exception:
            st.error("❌ Invalid image file")
            return None

    # =========================
    # ℹ️ INFO STATE
    # =========================
    st.info("Supported formats: JPG, JPEG, PNG")

    return None