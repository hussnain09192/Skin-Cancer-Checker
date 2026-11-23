import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

st.set_page_config(page_title="SkinGuard AI - Advanced Skin Cancer Detector", page_icon="🛡️", layout="centered")

# --- PREMIUM CSS - DIFFERENT FROM FRIEND ---
st.markdown("""
<style>
    .main { background-color: #F8F7FF; }
    .hero {
        background: linear-gradient(135deg, #1E1B4B 0%, #6D28D9 55%, #0EA5E9 100%);
        padding: 32px 22px;
        border-radius: 24px;
        color: white;
        text-align: center;
        box-shadow: 0 18px 35px rgba(109,40,217,0.35);
        margin-bottom: 18px;
    }
    .hero-logo {
        background: white;
        width: 88px; height: 88px;
        border-radius: 22px;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 12px auto;
        font-size: 48px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        transform: rotate(-3deg);
    }
    .hero h1 { color: white !important; font-size: 40px; margin: 0; letter-spacing: 0.5px; }
    .hero h1 span { color: #A5F3FC; }
    .hero p { color: #DDD6FE !important; font-size: 15px; margin-top: 8px; }
    .badge-green {
        background: #22C55E; color: white;
        padding: 7px 16px; border-radius: 20px;
        font-size: 12px; font-weight: 700;
    }
    .badge-white {
        background: rgba(255,255,255,0.18); color: white;
        padding: 7px 16px; border-radius: 20px;
        font-size: 12px; font-weight: 600;
        border: 1px solid rgba(255,255,255,0.3);
    }
    .feature-box {
        background: white;
        padding: 16px 8px;
        border-radius: 16px;
        text-align: center;
        border: 1px solid #EDE9FE;
        box-shadow: 0 4px 14px rgba(0,0,0,0.05);
    }
    .feature-box b { font-size: 14px; color: #1E1B4B; }
    .feature-box p { font-size: 11px; color: #64748B; margin: 2px 0 0 0; }
    .upload-title { font-size: 22px; font-weight: 800; color: #1E1B4B; margin-top: 18px; }
    .upload-sub { font-size: 13px; color: #64748B; margin-bottom: 10px; }
    .stButton > button {
        background: linear-gradient(135deg, #6D28D9, #0EA5E9) !important;
        color: white !important;
        font-size: 17px !important;
        font-weight: 700 !important;
        padding: 13px !important;
        border-radius: 50px !important;
        border: none !important;
        width: 100%;
        box-shadow: 0 10px 25px rgba(109,40,217,0.35);
    }
    .result-card {
        background: white;
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #EDE9FE;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.06);
    }
    .footer { text-align: center; color: #94A3B8; font-size: 12px; margin-top: 25px; }
</style>
""", unsafe_allow_html=True)

# --- HERO / HEADER ---
st.markdown("""
<div class="hero">
    <div class="hero-logo">🛡️</div>
    <h1>Skin<span>Guard</span> AI</h1>
    <p>Next-Gen Skin Cancer Screening • Benign vs Malignant • Deep Learning</p>
    <br>
    <span class="badge-green">● MODEL ACTIVE</span>
    &nbsp;
    <span class="badge-white">CNN • 128 x 128 • v2.0</span>
</div>
""", unsafe_allow_html=True)

# --- 4 FEATURE CARDS - DIFFERENT STYLE ---
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="feature-box"><div style="font-size:24px;">⚡</div><b>Instant</b><p>2 Sec Result</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="feature-box"><div style="font-size:24px;">🧠</div><b>Smart AI</b><p>Deep CNN Model</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="feature-box"><div style="font-size:24px;">🔒</div><b>100% Private</b><p>No Image Saved</p></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="feature-box"><div style="font-size:24px;">📊</div><b>Risk Meter</b><p>Confidence Score</p></div>', unsafe_allow_html=True)

# --- MODEL LOAD ---
@st.cache_resource
def load_my_model():
    return tf.keras.models.load_model('skin_cancer_cnn_model.keras')

try:
    model = load_my_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# --- UPLOAD ---
st.markdown('<div class="upload-title">📸 Upload Skin Lesion Image</div>', unsafe_allow_html=True)
st.markdown('<div class="upload-sub">Upload a clear, close-up image of the skin lesion for best accuracy.</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose Image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    col_img, col_res = st.columns([1, 1])
    with col_img:
        st.image(image, caption='Your Image', use_container_width=True)

    resized = image.resize((128, 128))
    img_array = np.array(resized) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    if st.button('🔬 Analyze With AI'):
        with st.spinner('AI is analyzing...'):
            prediction = model.predict(img_array)[0][0]

        with col_res:
            if prediction > 0.5:
                conf = prediction * 100
                st.markdown(f"""
                <div class="result-card" style="border-top: 5px solid #EF4444;">
                    <div style="font-size:40px;">⚠️</div>
                    <h3 style="color:#EF4444; margin:5px 0;">Malignant</h3>
                    <p style="font-size:13px; color:#64748B;">Confidence: <b>{conf:.2f}%</b></p>
                </div>
                """, unsafe_allow_html=True)
                st.progress(float(prediction))
                st.error("High Risk Detected. Please consult a Dermatologist immediately.")
            else:
                conf = (1 - prediction) * 100
                st.markdown(f"""
                <div class="result-card" style="border-top: 5px solid #22C55E;">
                    <div style="font-size:40px;">✅</div>
                    <h3 style="color:#22C55E; margin:5px 0;">Benign</h3>
                    <p style="font-size:13px; color:#64748B;">Confidence: <b>{conf:.2f}%</b></p>
                </div>
                """, unsafe_allow_html=True)
                st.progress(float(1 - prediction))
                st.success("Low Risk. It looks Benign. Still consult a doctor for confirmation.")

st.markdown("""
<div style="background:#FFFBEB; padding:12px; border-radius:12px; margin-top:20px; text-align:center; font-size:12px; color:#92400E;">
⚠️ <b>Disclaimer:</b> This tool is for educational purposes only. Please consult a Dermatologist for final diagnosis.
</div>
<div class="footer"><b>SkinGuard AI</b> | Final Year Project • Powered by CNN</div>
""", unsafe_allow_html=True)
