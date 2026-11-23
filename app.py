import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# --- PAGE SETTING ---
st.set_page_config(page_title="SkinGuard AI - Skin Cancer Detector", page_icon="🛡️", layout="centered")

# --- PREMIUM MODERN CSS ---
st.markdown("""
<style>
    .main { background-color: #F1F5F9; }
    .header-box {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 55%, #2563EB 100%);
        padding: 35px 25px 28px 25px;
        border-radius: 22px;
        color: white;
        text-align: center;
        box-shadow: 0 15px 30px rgba(0,0,0,0.20);
        margin-bottom: 22px;
    }
    .logo-circle {
        background: white;
        width: 85px; height: 85px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 12px auto;
        font-size: 45px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.25);
    }
    .header-box h1 { color: white !important; font-size: 42px; margin: 0; letter-spacing: 1px; }
    .header-box h1 span { color: #60A5FA; }
    .header-box p { color: #CBD5E1 !important; font-size: 16px; margin-top: 8px; }
    .badge {
        background: rgba(255,255,255,0.15);
        padding: 6px 16px; border-radius: 20px;
        font-size: 13px; color: white;
        border: 1px solid rgba(255,255,255,0.25);
    }
    .steps-card {
        background: white;
        padding: 18px 10px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        text-align: center;
    }
    .step { display: inline-block; margin: 0 10px; font-size: 14px; color: #334155; font-weight: 600; }
    .stButton > button {
        background: linear-gradient(135deg, #1E3A8A, #2563EB) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        padding: 13px 40px !important;
        border-radius: 50px !important;
        border: none !important;
        width: 100%;
        box-shadow: 0 10px 22px rgba(37,99,235,0.35);
    }
    .footer {
        text-align: center; color: #64748B; font-size: 13px; margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER / LOGO ---
st.markdown("""
<div class="header-box">
    <div class="logo-circle">🛡️</div>
    <h1>Skin<span>Guard</span> AI</h1>
    <p>Early Detection Saves Lives | AI Skin Cancer Screening</p>
    <br>
    <span class="badge">✦ AI-Powered &nbsp; • &nbsp; Fast &nbsp; • &nbsp; Secure &nbsp; • &nbsp; Accurate</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="steps-card">
    <span class="step">① Upload Image</span>
    <span style="color:#94A3B8;">→</span>
    <span class="step">② Click Predict</span>
    <span style="color:#94A3B8;">→</span>
    <span class="step">③ Get Instant Result</span>
</div>
""", unsafe_allow_html=True)

# --- MODEL ---
@st.cache_resource
def load_my_model():
    return tf.keras.models.load_model('skin_cancer_cnn_model.keras')

try:
    model = load_my_model()
    st.success("✅ Model Loaded Successfully!")
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# --- UPLOAD ---
uploaded_file = st.file_uploader("📸 Upload Your Skin Lesion Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption='Uploaded Image', use_container_width=True)

    resized_image = image.resize((128, 128))
    img_array = np.array(resized_image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    if st.button('🔬 Analyze Now'):
        with st.spinner('AI is analyzing your image...'):
            prediction = model.predict(img_array)[0][0]

        st.markdown("---")
        if prediction > 0.5:
            confidence = prediction * 100
            st.error(f"### ⚠️ Prediction: Malignant\n**Confidence: {confidence:.2f}%**")
            st.warning("Please consult a dermatologist immediately. This is an AI prediction, not a final medical diagnosis.")
        else:
            confidence = (1 - prediction) * 100
            st.success(f"### ✅ Prediction: Benign\n**Confidence: {confidence:.2f}%**")
            st.info("Good news! It looks Benign. Still, please consult a doctor for confirmation.")

st.markdown("""
<div class="footer">
    <b>SkinGuard AI</b> | Developed for Early Skin Cancer Detection<br>
    Disclaimer: This tool is for educational purposes only. It is not a medical diagnosis.
</div>
""", unsafe_allow_html=True)
