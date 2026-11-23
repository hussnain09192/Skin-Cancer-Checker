import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import io

st.set_page_config(page_title="DermaLens AI", page_icon="🔬", layout="wide")

# --- COMPLETELY DIFFERENT STYLE - MINT + BLACK ---
st.markdown("""
<style>
    .main { background-color: #FFFFFF; }
    .topbar {
        background: #0F0F0F;
        padding: 14px 20px;
        border-radius: 14px;
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 20px;
    }
    .topbar b { color: white; font-size: 20px; }
    .topbar b span { color: #00E5A0; }
    .topbar p { color: #A1A1AA; font-size: 12px; margin: 0; }
    .left-card {
        background: #F0FDF4;
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #BBF7D0;
    }
    .left-card h2 { color: #14532D; font-size: 34px; line-height: 1.1; margin: 0; }
    .left-card p { color: #4B5563; font-size: 14px; }
    .pill { background: white; border: 1px solid #E5E7EB; padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; margin: 3px; }
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 12px !important;
        border: none !important;
    }
    /* Main Analyze Button - Green */
    div[data-testid="stButton"] button[kind="primary"] {
        background: #00C389 !important; color: white !important; font-size: 17px !important;
    }
    .footer { text-align: center; color: #9CA3AF; font-size: 12px; margin-top: 20px; }
</style>
""", unsafe_allow_html=True)

# --- TOP BAR - NOT HERO ---
st.markdown("""
<div class="topbar">
    <div><b>🔬 Derma<span>Lens</span> AI</b><p>Advanced Dermatology Assistant</p></div>
    <div style="text-align:right;"><span style="color:#00E5A0; font-weight:700;">● LIVE</span><p>AI Model Ready</p></div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR - EXTRA FEATURE, FRIEND DOES NOT HAVE ---
with st.sidebar:
    st.markdown("### 🔬 DermaLens AI")
    st.caption("Your Skin Health Companion")
    st.divider()
    menu = st.radio("Navigate", ["🏠 Home - Scanner", "📖 How It Works", "ℹ️ About Model"])
    st.divider()
    st.markdown("**Model Info**")
    st.info("Architecture: CNN\nInput: 128 x 128\nClasses: Benign / Malignant")
    st.warning("⚠️ For educational use only. Not a medical diagnosis.")
    st.caption("Made by DermaLens Team")

if menu == "📖 How It Works":
    st.markdown("## How DermaLens Works?")
    st.markdown("**1.** Upload a clear image\n\n**2.** Our CNN model scans 128x128 pixels\n\n**3.** You get Benign / Malignant result with confidence\n\n**4.** Download your report")
    st.stop()

if menu == "ℹ️ About Model":
    st.markdown("## About This Project")
    st.write("DermaLens AI is a Final Year Project using Convolutional Neural Networks (CNN) trained on skin lesion dataset to detect skin cancer early.")
    st.write("It helps in early screening, so patients can consult doctors on time.")
    st.stop()

# --- MAIN LAYOUT - 2 COLUMNS, DIFFERENT FROM FRIEND ---
left, right = st.columns([1.1, 1])

with left:
    st.markdown("""
    <div class="left-card">
        <span class="pill">✦ AI-Powered</span> <span class="pill">🔒 Private</span>
        <h2>See What Your<br>Skin Is<br>Telling You.</h2>
        <p>Upload a lesion image and let DermaLens AI analyze it in seconds. Early detection can save lives.</p>
        <p>✅ <b>Fast</b> &nbsp; ✅ <b>Accurate</b> &nbsp; ✅ <b>Free</b></p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("#### Why Choose DermaLens?")
    c1, c2, c3 = st.columns(3)
    c1.metric("Speed", "2 Sec", "Instant")
    c2.metric("Input", "128x128", "CNN")
    c3.metric("Privacy", "100%", "No Save")

with right:
    st.markdown("### 📸 Scan Your Skin")
    st.caption("Drag & drop or browse your image. JPG, PNG supported.")

    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

    # --- EXTRA BUTTONS - FRIEND DOES NOT HAVE ---
    b1, b2 = st.columns(2)
    with b1:
        use_sample = st.button("🖼️ Try Sample Image")
    with b2:
        clear_btn = st.button("🗑️ Clear")

    if clear_btn:
        st.rerun()

    image = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
    elif use_sample:
        st.info("Sample feature: Please upload your own image to test. Sample images coming soon.")
    
    if image is not None:
        st.image(image, use_container_width=True)

        # Preprocess
        resized = image.resize((128, 128))
        img_array = np.array(resized) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # --- MAIN + EXTRA BUTTONS ---
        col_a, col_b = st.columns([2, 1])
        with col_a:
            analyze = st.button("🚀 Analyze Now", type="primary", use_container_width=True)
        with col_b:
            download_report = st.button("📄 Report", use_container_width=True)

        if analyze:
            @st.cache_resource
            def load_my_model():
                return tf.keras.models.load_model('skin_cancer_cnn_model.keras')
            try:
                model = load_my_model()
            except Exception as e:
                st.error(f"Model Error: {e}")
                st.stop()

            with st.spinner("DermaLens is scanning..."):
                prediction = model.predict(img_array)[0][0]

            st.divider()
            if prediction > 0.5:
                conf = prediction * 100
                st.error(f"### ⚠️ Result: MALIGNANT")
                st.progress(float(prediction))
                st.write(f"**Confidence:** {conf:.2f}%  |  **Risk Level:** High")
                st.warning("Please visit a Dermatologist immediately.")
                report_text = f"DermaLens AI Report\nResult: Malignant\nConfidence: {conf:.2f}%\nAdvice: Consult Dermatologist"
            else:
                conf = (1 - prediction) * 100
                st.success(f"### ✅ Result: BENIGN")
                st.progress(float(1 - prediction))
                st.write(f"**Confidence:** {conf:.2f}%  |  **Risk Level:** Low")
                st.info("Looks Benign. Still get a doctor checkup for confirmation.")
                report_text = f"DermaLens AI Report\nResult: Benign\nConfidence: {conf:.2f}%\nAdvice: Routine Checkup"

            # --- EXTRA BUTTON: DOWNLOAD REPORT ---
            if download_report or True:
                st.download_button("⬇️ Download Full Report (.txt)", data=report_text, file_name="DermaLens_Report.txt", mime="text/plain")

st.markdown('<div class="footer">DermaLens AI • Early Detection Saves Lives • Final Year Project</div>', unsafe_allow_html=True)
