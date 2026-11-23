import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np

st.set_page_config(page_title="SkinSense AI - Skin Cancer Detector", page_icon="👁️", layout="centered")

st.markdown("""
<style>
    .main { background-color: #F8FAFC; }
    .header-box {
        background: linear-gradient(135deg, #020617 0%, #0F766E 60%, #14B8A6 100%);
        padding: 32px 25px 26px 25px;
        border-radius: 22px;
        color: white;
        text-align: center;
        box-shadow: 0 15px 30px rgba(0,0,0,0.22);
        margin-bottom: 18px;
    }
    .logo-circle {
        background: white;
        width: 82px; height: 82px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto 12px auto;
        font-size: 42px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.25);
    }
    .header-box h1 { color: white !important; font-size: 40px; margin: 0; }
    .header-box h1 span { color: #5EEAD4; }
    .header-box p { color: #CCFBF1 !important; font-size: 15px; margin-top: 6px; }
    .badge-green {
        background: #22C55E; color: white;
        padding: 7px 16px; border-radius: 20px;
        font-size: 12px; font-weight: 700;
    }
    .badge-white {
        background: rgba(255,255,255,0.16); color: white;
        padding: 7px 16px; border-radius: 20px;
        font-size: 12px; font-weight: 600;
        border: 1px solid rgba(255,255,255,0.3);
    }
    .feature-box {
        background: white;
        padding: 18px 6px;
        border-radius: 16px;
        text-align: center;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .feature-box b { font-size: 14px; color: #0F172A; }
    .feature-box p { font-size: 11px; color: #64748B; margin: 3px 0 0 0; }

    /* --- SINGLE UPLOAD BOX - YEHI MAIN FIX HAI --- */
    [data-testid="stFileUploader"] {
        background: white;
        border: 2.5px dashed #14B8A6 !important;
        border-radius: 18px !important;
        padding: 28px 20px 22px 20px !important;
        text-align: center;
        margin-top: 18px;
    }
    [data-testid="stFileUploader"] section {
        border: none !important;
        padding: 0 !important;
    }
    [data-testid="stFileUploader"] button {
        background: #0F766E !important;
        color: white !important;
        border-radius: 50px !important;
        padding: 10px 28px !important;
        font-weight: 700 !important;
        border: none !important;
        font-size: 15px !important;
    }
    [data-testid="stFileUploader"] small {
        font-size: 13px !important;
        color: #64748B !important;
    }

    .stButton > button {
        border-radius: 50px !important;
        font-weight: 700 !important;
        padding: 14px 20px !important;
        font-size: 16px !important;
        border: none !important;
        box-shadow: 0 8px 18px rgba(0,0,0,0.15) !important;
    }
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(135deg, #0F766E, #14B8A6) !important;
        color: white !important;
        font-size: 19px !important;
        padding: 16px !important;
        width: 100%;
    }
    .footer { text-align: center; color: #94A3B8; font-size: 12px; margin-top: 22px; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="header-box">
    <div class="logo-circle">👁️</div>
    <h1>Skin<span>Sense</span> AI</h1>
    <p>Early Skin Cancer Detection • Benign vs Malignant • Powered by Deep Learning</p>
    <br>
    <span class="badge-green">● AI MODEL ACTIVE</span>
    &nbsp;
    <span class="badge-white">CNN • 128 x 128 • High Accuracy</span>
</div>
""", unsafe_allow_html=True)

# --- 4 CARDS ---
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="feature-box"><div style="font-size:26px;">⚡</div><b>Fast</b><p>Result in 2 Sec</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="feature-box"><div style="font-size:26px;">🎯</div><b>Accurate</b><p>Deep CNN Model</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="feature-box"><div style="font-size:26px;">🔒</div><b>Private</b><p>Image Not Saved</p></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="feature-box"><div style="font-size:26px;">📋</div><b>Report</b><p>Downloadable Report</p></div>', unsafe_allow_html=True)

# --- MODEL ---
@st.cache_resource
def load_my_model():
    return tf.keras.models.load_model('skin_cancer_cnn_model.keras')

try:
    model = load_my_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# --- SINGLE UPLOAD BOX - AB SIRF YEHI HAI, UPAR WALA ALAG BOX KHATAM ---
uploaded_file = st.file_uploader("📸 Upload Skin Lesion Image", type=["jpg", "jpeg", "png"], help="Upload a clear, close-up image for best accuracy")

# --- EXTRA BUTTONS ---
eb1, eb2, eb3 = st.columns(3)
with eb1:
    sample_btn = st.button("🖼️ Try Sample Image", use_container_width=True)
with eb2:
    clear_btn = st.button("🗑️ Clear Image", use_container_width=True)
with eb3:
    info_btn = st.button("ℹ️ How It Works", use_container_width=True)

if clear_btn:
    st.rerun()
if info_btn:
    st.info("1. Upload Image -> 2. Click Analyze -> 3. Get Result + Download Report")
if sample_btn:
    st.info("Please upload your own image to test.")

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption='Your Uploaded Image', use_container_width=True)

    resized = image.resize((128, 128))
    img_array = np.array(resized) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    if st.button('🔬 Analyze Now', type="primary", use_container_width=True):
        with st.spinner('SkinSense AI is analyzing...'):
            prediction = model.predict(img_array)[0][0]

        st.markdown("---")
        if prediction > 0.5:
            conf = prediction * 100
            st.error(f"### ⚠️ Prediction: Malignant")
            st.progress(float(prediction))
            st.write(f"**Confidence:** {conf:.2f}%  |  **Risk:** High")
            st.warning("Please consult a Dermatologist immediately.")
            report = f"SkinSense AI Report\nResult: Malignant\nConfidence: {conf:.2f}%\nAdvice: Consult Dermatologist Immediately"
        else:
            conf = (1 - prediction) * 100
            st.success(f"### ✅ Prediction: Benign")
            st.progress(float(1 - prediction))
            st.write(f"**Confidence:** {conf:.2f}%  |  **Risk:** Low")
            st.info("Good news! It looks Benign. Please still consult a doctor for confirmation.")
            report = f"SkinSense AI Report\nResult: Benign\nConfidence: {conf:.2f}%\nAdvice: Routine Checkup"

        st.download_button("⬇️ Download Full Report", data=report, file_name="SkinSense_Report.txt", mime="text/plain", use_container_width=True)

st.markdown("""
<div style="background:#FFFBEB; padding:12px; border-radius:12px; margin-top:20px; text-align:center; font-size:12px; color:#92400E;">
⚠️ <b>Disclaimer:</b> This tool is for educational purposes only. It is not a final medical diagnosis.
</div>
<div class="footer"><b>SkinSense AI</b> | Early Detection Saves Lives • Final Year Project</div>
""", unsafe_allow_html=True)
