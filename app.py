import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import io
from datetime import datetime

# For PDF Report
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

st.set_page_config(page_title="SkinSense AI - Skin Cancer Detector", page_icon="👁️", layout="centered")

def create_pdf_report(result, confidence, risk):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4
    # Header
    c.setFillColor(HexColor("#0F766E"))
    c.rect(0, h-110, w, 110, fill=1, stroke=0)
    c.setFillColor(HexColor("#FFFFFF"))
    c.setFont("Helvetica-Bold", 26)
    c.drawString(40, h-55, "SkinSense AI")
    c.setFont("Helvetica", 11)
    c.drawString(40, h-80, "Early Skin Cancer Detection Report")
    c.setFont("Helvetica", 9)
    c.drawString(40, h-98, f"Date: {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    # Body
    c.setFillColor(HexColor("#0F172A"))
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, h-160, "Prediction Result")
    c.setFont("Helvetica", 13)
    if result == "Malignant":
        c.setFillColor(HexColor("#DC2626"))
    else:
        c.setFillColor(HexColor("#16A34A"))
    c.setFont("Helvetica-Bold", 22)
    c.drawString(40, h-195, f"{result.upper()}")
    c.setFillColor(HexColor("#334155"))
    c.setFont("Helvetica", 12)
    c.drawString(40, h-230, f"Confidence: {confidence:.2f}%")
    c.drawString(40, h-255, f"Risk Level: {risk}")
    c.drawString(40, h-280, "Model: CNN  |  Input: 128 x 128  |  Classes: Benign / Malignant")
    c.setFont("Helvetica-Bold", 13)
    c.drawString(40, h-320, "Recommendation:")
    c.setFont("Helvetica", 11)
    if result == "Malignant":
        c.drawString(40, h-340, "Please consult a Dermatologist immediately for further examination.")
    else:
        c.drawString(40, h-340, "Looks Benign. Still consult a doctor for final confirmation.")
    c.setFont("Helvetica", 9)
    c.setFillColor(HexColor("#94A3B8"))
    c.drawString(40, 50, "Disclaimer: This is an AI screening tool for educational purposes only. Not a final medical diagnosis.")
    c.drawString(40, 35, "SkinSense AI | Final Year Project")
    c.save()
    buffer.seek(0)
    return buffer

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
    }
    .header-box h1 { color: white !important; font-size: 40px; margin: 0; }
    .header-box h1 span { color: #5EEAD4; }
    .header-box p { color: #CCFBF1 !important; font-size: 15px; margin-top: 6px; }
    .badge-green { background: #22C55E; color: white; padding: 7px 16px; border-radius: 20px; font-size: 12px; font-weight: 700; }
    .badge-white { background: rgba(255,255,255,0.16); color: white; padding: 7px 16px; border-radius: 20px; font-size: 12px; font-weight: 600; border: 1px solid rgba(255,255,255,0.3); }
    .feature-box {
        background: white;
        padding: 18px 6px;
        border-radius: 16px;
        text-align: center;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        min-height: 115px;
    }
    .feature-box b { font-size: 14px; color: #0F172A; }
    .feature-box p { font-size: 11px; color: #64748B; margin: 3px 0 0 0; line-height: 1.3; }
    /* SINGLE UPLOAD BOX - BIGGER */
    [data-testid="stFileUploader"] {
        background: white;
        border: 2.5px dashed #14B8A6 !important;
        border-radius: 18px !important;
        padding: 30px 20px 22px 20px !important;
        margin-top: 18px;
    }
    [data-testid="stFileUploader"] section { border: none !important; padding: 0 !important; }
    [data-testid="stFileUploader"] button {
        background: #0F766E !important; color: white !important;
        border-radius: 50px !important; padding: 10px 28px !important;
        font-weight: 700 !important; border: none !important;
    }
    /* IMAGE - FULL INSIDE BOX, BIG */
    [data-testid="stImage"] img {
        width: 100% !important;
        max-height: 420px !important;
        object-fit: contain !important;
        border-radius: 14px;
        background: #F1F5F9;
        padding: 10px;
    }
    .image-box {
        background: white;
        border: 2px solid #CCFBF1;
        border-radius: 18px;
        padding: 14px;
        margin-top: 14px;
    }
    .stButton > button {
        border-radius: 50px !important; font-weight: 700 !important;
        padding: 14px 20px !important; font-size: 16px !important;
        border: none !important; box-shadow: 0 8px 18px rgba(0,0,0,0.15) !important;
    }
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(135deg, #0F766E, #14B8A6) !important;
        color: white !important; font-size: 19px !important; padding: 16px !important; width: 100%;
    }
    .footer { text-align: center; color: #94A3B8; font-size: 12px; margin-top: 22px; }
</style>
""", unsafe_allow_html=True)

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

# --- NEW 4 CARDS - CHANGED ---
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="feature-box"><div style="font-size:26px;">🔍</div><b>Early Detection</b><p>Detect at Early Stage</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="feature-box"><div style="font-size:26px;">🧠</div><b>Smart AI</b><p>Deep Learning CNN</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="feature-box"><div style="font-size:26px;">🛡️</div><b>Safe & Private</b><p>Your Data Stays Private</p></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="feature-box"><div style="font-size:26px;">📄</div><b>PDF Report</b><p>Download PDF Report</p></div>', unsafe_allow_html=True)

@st.cache_resource
def load_my_model():
    return tf.keras.models.load_model('skin_cancer_cnn_model.keras')

try:
    model = load_my_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

uploaded_file = st.file_uploader("📸 Upload Skin Lesion Image", type=["jpg", "jpeg", "png"], help="Upload a clear, close-up image for best accuracy")

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
    st.info("1. Upload Image -> 2. Click Analyze -> 3. Get Result + Download PDF Report")
if sample_btn:
    st.info("Please upload your own image to test.")

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    # IMAGE IN BIG BOX - FULL VISIBLE
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    st.image(image, caption='Your Uploaded Image - Full View', use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    resized = image.resize((128, 128))
    img_array = np.array(resized) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    if st.button('🔬 Analyze Now', type="primary", use_container_width=True):
        with st.spinner('SkinSense AI is analyzing...'):
            prediction = model.predict(img_array)[0][0]

        st.markdown("---")
        if prediction > 0.5:
            conf = prediction * 100
            result, risk = "Malignant", "High"
            st.error(f"### ⚠️ Prediction: Malignant")
            st.progress(float(prediction))
            st.write(f"**Confidence:** {conf:.2f}%  |  **Risk:** High")
            st.warning("Please consult a Dermatologist immediately.")
        else:
            conf = (1 - prediction) * 100
            result, risk = "Benign", "Low"
            st.success(f"### ✅ Prediction: Benign")
            st.progress(float(1 - prediction))
            st.write(f"**Confidence:** {conf:.2f}%  |  **Risk:** Low")
            st.info("Good news! It looks Benign. Please still consult a doctor for confirmation.")

        # --- PDF DOWNLOAD ---
        pdf_buffer = create_pdf_report(result, conf, risk)
        st.download_button("⬇️ Download PDF Report", data=pdf_buffer, file_name="SkinSense_Report.pdf", mime="application/pdf", use_container_width=True)

st.markdown("""
<div style="background:#FFFBEB; padding:12px; border-radius:12px; margin-top:20px; text-align:center; font-size:12px; color:#92400E;">
⚠️ <b>Disclaimer:</b> This tool is for educational purposes only. It is not a final medical diagnosis.
</div>
<div class="footer"><b>SkinSense AI</b> | Early Detection Saves Lives • Final Year Project</div>
""", unsafe_allow_html=True)
