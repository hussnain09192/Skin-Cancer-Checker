import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import io
import requests
from datetime import datetime

DEVELOPER_NAME = "Hussnain Khalid"

st.set_page_config(page_title=f"SkinSense AI - by {DEVELOPER_NAME}", page_icon="👁️", layout="centered")

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0
if "use_sample" not in st.session_state:
    st.session_state.use_sample = False
if "show_how" not in st.session_state:
    st.session_state.show_how = False
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "result" not in st.session_state:
    st.session_state.result = None
if "conf" not in st.session_state:
    st.session_state.conf = 0
if "risk" not in st.session_state:
    st.session_state.risk = ""
if "want_pdf" not in st.session_state:
    st.session_state.want_pdf = False

SAMPLE_URL = "https://upload.wikimedia.org/wikipedia/commons/5/5d/Melanoma_in_situ.jpg"

def load_sample_image():
    try:
        r = requests.get(SAMPLE_URL, timeout=10)
        return Image.open(io.BytesIO(r.content)).convert("RGB")
    except:
        img = Image.new("RGB", (400, 400), color=(180, 120, 90))
        return img

def create_pdf_report(result, confidence, risk):
    date_str = datetime.now().strftime('%d %B %Y, %I:%M %p')
    advice = "Please consult a Dermatologist immediately." if result == "Malignant" else "Looks Benign. Still consult a doctor."
    lines = [
        "SkinSense AI - Early Skin Cancer Detection Report",
        "",
        f"Date: {date_str}",
        f"Developed by: {DEVELOPER_NAME}",
        "",
        "Prediction Result:",
        f"{result.upper()}",
        "",
        f"Confidence: {confidence:.2f}%",
        f"Risk Level: {risk}",
        "Model: CNN | Input: 128 x 128",
        "",
        f"Recommendation: {advice}",
        "",
        "Disclaimer: For educational purposes only. Not a final medical diagnosis.",
        f"SkinSense AI | Developed by {DEVELOPER_NAME}",
    ]
    content = "BT /F1 14 Tf 50 750 Td "
    for i, line in enumerate(lines):
        clean = line.replace("(", "[").replace(")", "]").replace("\\", "")
        if i == 0:
            content += f"18 TL 0 -30 Td ({clean}) Tj "
        elif line == result.upper():
            content += f"0 -30 Td /F1 20 Tf ({clean}) Tj /F1 12 Tf "
        else:
            content += f"0 -22 Td ({clean}) Tj "
    content += "ET"
    objects = []
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objects.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    objects.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>".encode())
    objects.append(f"<< /Length {len(content)} >>\nstream\n{content}\nendstream".encode())
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    pdf = io.BytesIO()
    pdf.write(b"%PDF-1.4\n")
    offsets = []
    for i, obj in enumerate(objects, start=1):
        offsets.append(pdf.tell())
        pdf.write(f"{i} 0 obj\n".encode())
        pdf.write(obj)
        pdf.write(b"\nendobj\n")
    xref_pos = pdf.tell()
    pdf.write(f"xref\n0 {len(objects)+1}\n".encode())
    pdf.write(b"0000000000 65535 f \n")
    for off in offsets:
        pdf.write(f"{off:010d} 00000 n \n".encode())
    pdf.write(f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF".encode())
    pdf.seek(0)
    return pdf

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
    .dev-badge {
        background: #F59E0B; color: #1A1A1A;
        padding: 8px 18px; border-radius: 50px;
        font-size: 13px; font-weight: 800;
        display: inline-block; margin-top: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
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
    [data-testid="stFileUploader"] {
        background: white;
        border: 2.5px dashed #14B8A6 !important;
        border-radius: 18px !important;
        padding: 18px 18px 14px 18px !important;
        margin-top: 18px;
    }
    [data-testid="stFileUploaderDropzone"] button {
        background: #0F766E !important;
        color: white !important;
        border-radius: 14px !important;
        padding: 14px 20px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        border: none !important;
        width: 100% !important;
    }
    [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] {
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
        width: 100% !important;
    }
    [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] button {
        width: auto !important;
        min-width: 36px !important;
        height: 36px !important;
        padding: 0px 8px !important;
        border-radius: 50% !important;
        flex-shrink: 0 !important;
        background: #F1F5F9 !important;
        color: #0F172A !important;
        border: 1px solid #E2E8F0 !important;
    }
    button[data-testid="stFileUploaderDeleteBtn"] {
        width: 36px !important;
        min-width: 36px !important;
        background: #FEE2E2 !important;
        color: #DC2626 !important;
    }
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
    .footer b { color: #0F766E; font-size: 14px; }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="header-box">
    <div class="logo-circle">👁️</div>
    <h1>Skin<span>Sense</span> AI</h1>
    <p>Early Skin Cancer Detection • Benign vs Malignant • Powered by Deep Learning</p>
    <br>
    <span class="badge-green">● AI MODEL ACTIVE</span>
    &nbsp;
    <span class="badge-white">CNN • 128 x 128 • High Accuracy</span>
    <br>
    <span class="dev-badge">👨‍💻 Developed by {DEVELOPER_NAME}</span>
</div>
""", unsafe_allow_html=True)

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

uploaded_file = st.file_uploader("📸 Upload Skin Lesion Image", type=["jpg", "jpeg", "png"], key=f"uploader_{st.session_state.uploader_key}")

eb1, eb2, eb3 = st.columns(3)
with eb1:
    if st.button("🖼️ Try Sample Image", use_container_width=True):
        st.session_state.use_sample = True
        st.session_state.show_how = False
        st.session_state.analysis_done = False
        st.session_state.want_pdf = False
        st.rerun()
with eb2:
    if st.button("🗑️ Clear Image", use_container_width=True):
        st.session_state.use_sample = False
        st.session_state.show_how = False
        st.session_state.analysis_done = False
        st.session_state.want_pdf = False
        st.session_state.uploader_key += 1
        st.rerun()
with eb3:
    if st.button("ℹ️ How It Works", use_container_width=True):
        st.session_state.show_how = not st.session_state.show_how
        st.rerun()

if st.session_state.show_how:
    st.info("""
    **How It Works - 3 Easy Steps:**
    1️⃣ **Upload Image** - Apni skin wali tasveer upload karo ya Try Sample dabao
    2️⃣ **Analyze Now** - AI tumhari tasveer ko check karega
    3️⃣ **PDF (Optional)** - Agar chaho to Generate PDF dabao, warna nahi
    """)

image = None
image_source = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    image_source = "Your Uploaded Image"
    st.session_state.use_sample = False
elif st.session_state.use_sample:
    image = load_sample_image()
    image_source = "Sample Image - Try Karne Ke Liye"

if image is not None:
    st.markdown('<div class="image-box">', unsafe_allow_html=True)
    st.image(image, caption=f'{image_source} - Full View', use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    resized = image.resize((128, 128))
    img_array = np.array(resized) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    if st.button('🔬 Analyze Now', type="primary", use_container_width=True):
        with st.spinner('SkinSense AI is analyzing...'):
            prediction = model.predict(img_array)[0][0]
        if prediction > 0.5:
            st.session_state.result = "Malignant"
            st.session_state.conf = prediction * 100
            st.session_state.risk = "High"
            st.session_state.pred_value = float(prediction)
        else:
            st.session_state.result = "Benign"
            st.session_state.conf = (1 - prediction) * 100
            st.session_state.risk = "Low"
            st.session_state.pred_value = float(1 - prediction)
        st.session_state.analysis_done = True
        st.session_state.want_pdf = False
        st.rerun()

    # --- RESULT DIKHAO, PDF NAHI ---
    if st.session_state.analysis_done:
        st.markdown("---")
        result = st.session_state.result
        conf = st.session_state.conf
        risk = st.session_state.risk

        if result == "Malignant":
            st.error(f"### ⚠️ Prediction: Malignant")
            st.progress(st.session_state.pred_value)
            st.write(f"**Confidence:** {conf:.2f}%  |  **Risk:** High")
            st.warning("Please consult a Dermatologist immediately.")
        else:
            st.success(f"### ✅ Prediction: Benign")
            st.progress(st.session_state.pred_value)
            st.write(f"**Confidence:** {conf:.2f}%  |  **Risk:** Low")
            st.info("Good news! It looks Benign. Please still consult a doctor for confirmation.")

        st.markdown("---")
        # --- AB SIRF YE BUTTON AAYEGA, DOWNLOAD NAHI ---
        if not st.session_state.want_pdf:
            if st.button("📄 Generate PDF Report", use_container_width=True):
                st.session_state.want_pdf = True
                st.rerun()

        # --- JAB USER KHUD CHAHEGA TAB HI DOWNLOAD AAYEGA ---
        if st.session_state.want_pdf:
            pdf_buffer = create_pdf_report(result, conf, risk)
            st.success("PDF Ready hai! Neeche se download karo 👇")
            st.download_button("⬇️ Download PDF Report", data=pdf_buffer, file_name="SkinSense_Report.pdf", mime="application/pdf", use_container_width=True)

st.markdown(f"""
<div style="background:#FFFBEB; padding:12px; border-radius:12px; margin-top:20px; text-align:center; font-size:12px; color:#92400E;">
⚠️ <b>Disclaimer:</b> This tool is for educational purposes only. It is not a final medical diagnosis.
</div>
<div class="footer">Made with ❤️ by <b>{DEVELOPER_NAME}</b><br><b>SkinSense AI</b> | Early Detection Saves Lives • Final Year Project</div>
""", unsafe_allow_html=True)
