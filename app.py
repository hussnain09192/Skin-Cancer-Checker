import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import io
import requests
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.colors import HexColor

DEVELOPER_NAME = "Hussnain Khalid"

st.set_page_config(page_title=f"SkinSense AI - by {DEVELOPER_NAME}", page_icon="👁️", layout="centered")

# --- SESSION STATE ---
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0
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
if "show_download" not in st.session_state:
    st.session_state.show_download = False

# =====================================================
# --- PROFESSIONAL PDF REPORT - BILKUL REAL JESI ---
# =====================================================
def create_pdf_report(result, confidence, risk):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0, bottomMargin=0, leftMargin=0, rightMargin=0)
    story = []
    TEAL = HexColor("#0F766E")
    TEAL_DARK = HexColor("#020617")
    GREEN = HexColor("#16A34A")
    GREEN_BG = HexColor("#DCFCE7")
    RED = HexColor("#DC2626")
    RED_BG = HexColor("#FEE2E2")
    ORANGE = HexColor("#F59E0B")
    GREY = HexColor("#64748B")
    LIGHT_GREY = HexColor("#F1F5F9")
    BLACK = HexColor("#0F172A")
    is_malignant = result == "Malignant"
    main_color = RED if is_malignant else GREEN
    main_bg = RED_BG if is_malignant else GREEN_BG
    result_text = "MALIGNANT - HIGH RISK" if is_malignant else "BENIGN - LOW RISK"
    result_icon = "⚠️" if is_malignant else "✅"
    advice = "Please consult a Dermatologist immediately. Early treatment is very important." if is_malignant else "Good News! It looks Benign. Still consult a doctor once for confirmation."
    date_str = datetime.now().strftime('%d %B %Y, %I:%M %p')
    report_id = f"SS-{datetime.now().strftime('%Y%m%d%H%M')}"
    sTitle = ParagraphStyle('Title', fontName='Helvetica-Bold', fontSize=24, leading=28, textColor=colors.white, alignment=TA_CENTER)
    sSub = ParagraphStyle('Sub', fontName='Helvetica', fontSize=10, leading=13, textColor=HexColor("#CCFBF1"), alignment=TA_CENTER)
    sHeadSmall = ParagraphStyle('HeadSmall', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white, alignment=TA_CENTER)
    sSection = ParagraphStyle('Section', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=TEAL, alignment=TA_LEFT, spaceAfter=6)
    sLabel = ParagraphStyle('Label', fontName='Helvetica', fontSize=10, leading=13, textColor=GREY, alignment=TA_LEFT)
    sValue = ParagraphStyle('Value', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=BLACK, alignment=TA_LEFT)
    sResult = ParagraphStyle('Result', fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=main_color, alignment=TA_CENTER)
    sConf = ParagraphStyle('Conf', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=BLACK, alignment=TA_CENTER)
    sRec = ParagraphStyle('Rec', fontName='Helvetica', fontSize=10.5, leading=15, textColor=BLACK, alignment=TA_LEFT)
    sFooter = ParagraphStyle('Footer', fontName='Helvetica', fontSize=8, leading=10, textColor=colors.white, alignment=TA_CENTER)
    sDisc = ParagraphStyle('Disc', fontName='Helvetica-Oblique', fontSize=8, leading=11, textColor=GREY, alignment=TA_CENTER)
    header_data = [
        [Paragraph("👁️ SkinSense AI", sTitle)],
        [Paragraph("Early Skin Cancer Detection &nbsp;|&nbsp; Benign vs Malignant &nbsp;|&nbsp; Powered by Deep Learning", sSub)],
        [Paragraph(f"DEVELOPED BY {DEVELOPER_NAME.upper()} &nbsp;•&nbsp; FINAL YEAR PROJECT", sHeadSmall)],
    ]
    header_table = Table(header_data, colWidths=[210*mm])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), TEAL_DARK),
        ('TOPPADDING', (0,0), (-1,0), 18),
        ('BOTTOMPADDING', (0,-1), (-1,-1), 16),
        ('LEFTPADDING', (0,0), (-1,-1), 15),
        ('RIGHTPADDING', (0,0), (-1,-1), 15),
        ('LINEBELOW', (0,-1), (-1,-1), 4, TEAL),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 8*mm))
    info_data = [
        [Paragraph("<b>Report Date</b>", sLabel), Paragraph(f"<b>{date_str}</b>", sValue),
         Paragraph("<b>Report ID</b>", sLabel), Paragraph(f"<b>{report_id}</b>", sValue)],
        [Paragraph("<b>Patient Type</b>", sLabel), Paragraph("<b>General Checkup</b>", sValue),
         Paragraph("<b>Model</b>", sLabel), Paragraph("<b>CNN | 128 x 128</b>", sValue)],
    ]
    info_table = Table(info_data, colWidths=[30*mm, 55*mm, 30*mm, 55*mm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_GREY),
        ('BOX', (0,0), (-1,-1), 0.5, HexColor("#E2E8F0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('ROUNDEDCORNERS', [6,6,6,6]),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 7*mm))
    story.append(Paragraph("PREDICTION RESULT", sSection))
    result_data = [
        [Paragraph(f"{result_icon} &nbsp; {result_text}", sResult)],
        [Paragraph(f"Confidence: {confidence:.2f}% &nbsp;&nbsp; | &nbsp;&nbsp; Risk Level: {risk}", sConf)],
    ]
    result_table = Table(result_data, colWidths=[170*mm])
    result_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), main_bg),
        ('BOX', (0,0), (-1,-1), 1.5, main_color),
        ('TOPPADDING', (0,0), (-1,0), 14),
        ('BOTTOMPADDING', (0,0), (-1,0), 2),
        ('TOPPADDING', (0,1), (-1,1), 2),
        ('BOTTOMPADDING', (0,1), (-1,-1), 14),
        ('ROUNDEDCORNERS', [8,8,8,8]),
    ]))
    story.append(result_table)
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("DETAILED ANALYSIS", sSection))
    filled = int(confidence / 5)
    bar_text = "█" * filled + "░" * (20 - filled)
    detail_data = [
        [Paragraph("Prediction", sLabel), Paragraph(f"{result.upper()}", sValue)],
        [Paragraph("Confidence Score", sLabel), Paragraph(f"{confidence:.2f}%", sValue)],
        [Paragraph("Confidence Level", sLabel), Paragraph(f"{bar_text} &nbsp; {confidence:.0f}/100", ParagraphStyle('bar', fontName='Helvetica-Bold', fontSize=9, textColor=main_color))],
        [Paragraph("Risk Level", sLabel), Paragraph(f"{risk.upper()} {'🔴' if is_malignant else '🟢'}", ParagraphStyle('risk', fontName='Helvetica-Bold', fontSize=11, textColor=main_color))],
        [Paragraph("AI Model", sLabel), Paragraph("Convolutional Neural Network (CNN)", sValue)],
        [Paragraph("Image Size", sLabel), Paragraph("128 x 128 Pixels", sValue)],
        [Paragraph("Analysis Type", sLabel), Paragraph("Benign vs Malignant Classification", sValue)],
    ]
    detail_table = Table(detail_data, colWidths=[55*mm, 115*mm])
    detail_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.7, HexColor("#E2E8F0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(detail_table)
    story.append(Spacer(1, 6*mm))
    story.append(Paragraph("DOCTOR'S RECOMMENDATION", sSection))
    rec_data = [[Paragraph(f"<b>💡 Recommendation:</b> {advice}", sRec)]]
    rec_table = Table(rec_data, colWidths=[170*mm])
    rec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor("#FFFBEB")),
        ('BOX', (0,0), (-1,-1), 1, ORANGE),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('ROUNDEDCORNERS', [8,8,8,8]),
    ]))
    story.append(rec_table)
    story.append(Spacer(1, 8*mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=HexColor("#E2E8F0")))
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph("⚠️ Disclaimer: This report is generated by AI for educational purposes only. It is NOT a final medical diagnosis. Please consult a qualified Dermatologist for proper examination.", sDisc))
    story.append(Spacer(1, 6*mm))
    footer_data = [[Paragraph(f"SkinSense AI &nbsp;|&nbsp; Developed by <b>{DEVELOPER_NAME}</b> &nbsp;|&nbsp; Early Detection Saves Lives", sFooter)]]
    footer_table = Table(footer_data, colWidths=[210*mm])
    footer_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), TEAL),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(footer_table)
    doc.build(story)
    buffer.seek(0)
    return buffer

# --- APP DESIGN ---
st.markdown("""
<style>
    .main { background-color: #F8FAFC; }
    .header-box { background: linear-gradient(135deg, #020617 0%, #0F766E 60%, #14B8A6 100%); padding: 32px 25px 26px 25px; border-radius: 22px; color: white; text-align: center; box-shadow: 0 15px 30px rgba(0,0,0,0.22); margin-bottom: 18px; }
    .logo-circle { background: white; width: 82px; height: 82px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 12px auto; font-size: 42px; }
    .header-box h1 { color: white !important; font-size: 40px; margin: 0; }
    .header-box h1 span { color: #5EEAD4; }
    .header-box p { color: #CCFBF1 !important; font-size: 15px; margin-top: 6px; }
    .badge-green { background: #22C55E; color: white; padding: 7px 16px; border-radius: 20px; font-size: 12px; font-weight: 700; }
    .badge-white { background: rgba(255,255,255,0.16); color: white; padding: 7px 16px; border-radius: 20px; font-size: 12px; font-weight: 600; border: 1px solid rgba(255,255,255,0.3); }
    .dev-badge { background: #F59E0B; color: #1A1A1A; padding: 8px 18px; border-radius: 50px; font-size: 13px; font-weight: 800; display: inline-block; margin-top: 14px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
    .feature-box { background: white; padding: 18px 6px; border-radius: 16px; text-align: center; border: 1px solid #E2E8F0; box-shadow: 0 4px 12px rgba(0,0,0,0.05); min-height: 115px; }
    .feature-box b { font-size: 14px; color: #0F172A; }
    .feature-box p { font-size: 11px; color: #64748B; margin: 3px 0 0 0; line-height: 1.3; }
    [data-testid="stFileUploader"] { background: white; border: 2.5px dashed #14B8A6 !important; border-radius: 18px !important; padding: 18px 18px 14px 18px !important; margin-top: 18px; }
    [data-testid="stFileUploaderDropzone"] button { background: #0F766E !important; color: white !important; border-radius: 14px !important; padding: 14px 20px !important; font-weight: 700 !important; font-size: 16px !important; border: none !important; width: 100% !important; }
    [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] { display: flex !important; align-items: center !important; gap: 8px !important; width: 100% !important; }
    [data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] button { width: auto !important; min-width: 36px !important; height: 36px !important; padding: 0px 8px !important; border-radius: 50% !important; flex-shrink: 0 !important; background: #F1F5F9 !important; color: #0F172A !important; border: 1px solid #E2E8F0 !important; }
    button[data-testid="stFileUploaderDeleteBtn"] { width: 36px !important; min-width: 36px !important; background: #FEE2E2 !important; color: #DC2626 !important; }
    [data-testid="stImage"] img { width: 100% !important; max-height: 420px !important; object-fit: contain !important; border-radius: 14px; background: #F1F5F9; padding: 10px; }
    .image-box { background: white; border: 2px solid #CCFBF1; border-radius: 18px; padding: 14px; margin-top: 14px; }
    .stButton > button { border-radius: 50px !important; font-weight: 700 !important; padding: 14px 20px !important; font-size: 16px !important; border: none !important; box-shadow: 0 8px 18px rgba(0,0,0,0.15) !important; }
    div[data-testid="stButton"] button[kind="primary"] { background: linear-gradient(135deg, #0F766E, #14B8A6) !important; color: white !important; font-size: 19px !important; padding: 16px !important; width: 100%; }
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

# --- NAYA FIX: Try Sample KHATAM, sirf 2 button - dono FULL WIDTH ---
eb1, eb2 = st.columns(2)
with eb1:
    if st.button("🗑️ Clear Image", use_container_width=True):
        st.session_state.show_how = False
        st.session_state.analysis_done = False
        st.session_state.show_download = False
        st.session_state.uploader_key += 1
        st.rerun()
with eb2:
    if st.button("ℹ️ How It Works", use_container_width=True):
        st.session_state.show_how = not st.session_state.show_how
        st.rerun()

if st.session_state.show_how:
    st.info("""
    **How It Works - 3 Easy Steps:**
    1️⃣ **Upload Image** - Apni skin wali tasveer upload karo
    2️⃣ **Analyze Now** - AI tumhari tasveer ko check karega
    3️⃣ **Download PDF** - Agar chaho to Download PDF dabao, warna nahi
    """)

image = None
image_source = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    image_source = "Your Uploaded Image"

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
        st.session_state.show_download = False
        st.rerun()

    # --- RESULT + DOWNLOAD - AB AUTO DOWNLOAD NAHI HOGA ---
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

        # STEP 1: Ye sirf normal button hai, is se file download NAHI hogi
        if not st.session_state.show_download:
            if st.button("⬇️ Download PDF Report", use_container_width=True):
                st.session_state.show_download = True
                st.rerun()

        # STEP 2: Ab asli download button aayega, is ko dabao ge tabhi file download hogi
        if st.session_state.show_download:
            pdf_buffer = create_pdf_report(result, conf, risk)
            st.success("PDF Ready hai! Ab neeche wale button ko dabao, tabhi file download hogi 👇")
            st.download_button("✅ Click Here to Save PDF", data=pdf_buffer, file_name="SkinSense_Report.pdf", mime="application/pdf", use_container_width=True)

st.markdown(f"""
<div style="background:#FFFBEB; padding:12px; border-radius:12px; margin-top:20px; text-align:center; font-size:12px; color:#92400E;">
⚠️ <b>Disclaimer:</b> This tool is for educational purposes only. It is not a final medical diagnosis.
</div>
<div class="footer">Made with ❤️ by <b>{DEVELOPER_NAME}</b><br><b>SkinSense AI</b> | Early Detection Saves Lives • Final Year Project</div>
""", unsafe_allow_html=True)
