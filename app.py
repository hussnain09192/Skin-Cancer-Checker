import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

# --- PAGE SETTING ---
st.set_page_config(page_title="DermAI - Skin Cancer Detector", page_icon="🧬", layout="centered")

# --- MODERN CSS ---
st.markdown("""
<style>
    .main { background-color: #F8FAFC; }
    .header-box {
        background: linear-gradient(135deg, #0F766E 0%, #14B8A6 50%, #06B6D4 100%);
        padding: 30px 25px;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        margin-bottom: 25px;
    }
    .header-box h1 { color: white !important; font-size: 38px; margin: 0; }
    .header-box p { color: #E0F2FE !important; font-size: 16px; margin-top: 8px; }
    .info-card {
        background: white;
        padding: 18px;
        border-radius: 15px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        text-align: center;
    }
    .stButton > button {
        background: linear-gradient(135deg, #0F766E, #06B6D4) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        padding: 12px 40px !important;
        border-radius: 50px !important;
        border: none !important;
        width: 100%;
        box-shadow: 0 8px 20px rgba(20,184,166,0.3);
    }
    .stButton > button:hover {
        transform: scale(1.02);
    }
    .footer {
        text-align: center;
        color: #64748B;
        font-size: 13px;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER / LOGO AREA ---
st.markdown("""
<div class="header-box">
    <div style="font-size:55px;">🧬</div>
    <h1>DermAI</h1>
    <p>Smart Skin Cancer Detection | Benign vs Malignant</p>
    <p style="font-size:13px; background: rgba(255,255,255,0.2); display:inline-block; padding:5px 15px; border-radius:20px;">AI-Powered • Fast • Accurate</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
    <b>🔍 کیسے استعمال کریں؟</b><br>
    1. اپنی سکن کی تصویر اپلوڈ کریں &nbsp; | &nbsp; 2. Predict بٹن دبائیں &nbsp; | &nbsp; 3. رزلٹ دیکھیں
</div>
""", unsafe_allow_html=True)

# --- MODEL LOAD ---
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
uploaded_file = st.file_uploader("📸 اپنی سکن کی تصویر یہاں اپلوڈ کریں", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption='Uploaded Image', use_container_width=True)

    resized_image = image.resize((128, 128))
    img_array = np.array(resized_image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    if st.button('🔬 Predict Now'):
        with st.spinner('AI تصویر کا تجزیہ کر رہا ہے...'):
            prediction = model.predict(img_array)[0][0]

        st.markdown("---")
        if prediction > 0.5:
            confidence = prediction * 100
            st.error(f"### ⚠️ Prediction: Malignant\n**Confidence: {confidence:.2f}%**")
            st.warning("براہ کرم جلد کسی ماہر ڈاکٹر سے رابطہ کریں۔ یہ صرف AI کا اندازہ ہے۔")
        else:
            confidence = (1 - prediction) * 100
            st.success(f"### ✅ Prediction: Benign\n**Confidence: {confidence:.2f}%**")
            st.info("اچھی خبر ہے! یہ Benign لگ رہا ہے، پھر بھی احتیاط کے لیے ڈاکٹر سے چیک کروا لیں۔")

# --- FOOTER ---
st.markdown("""
<div class="footer">
    Made with ❤️ by DermAI Team | This tool is for educational purpose only, not a medical diagnosis.
</div>
""", unsafe_allow_html=True)
