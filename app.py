import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.colors import HexColor

DEVELOPER_NAME = "Hussnain Khalid"

def create_pdf_report(result, confidence, risk):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0, bottomMargin=0, leftMargin=0, rightMargin=0)
    story = []

    TEAL = HexColor("#0F766E")
    TEAL_LIGHT = HexColor("#CCFBF1")
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

    # --- STYLES ---
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

    # --- 1. HEADER ---
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

    # --- 2. REPORT INFO BAR ---
    info_data = [
        [Paragraph("<b>Report Date</b>", sLabel), Paragraph(f"<b>{date_str}</b>", sValue),
         Paragraph("<b>Report ID</b>", sLabel), Paragraph(f"<b>SS-{datetime.now().strftime('%Y%m%d%H%M')}</b>", sValue)],
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

    # --- 3. RESULT BOX ---
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

    # --- 4. DETAILED ANALYSIS TABLE ---
    story.append(Paragraph("DETAILED ANALYSIS", sSection))
    # Confidence Bar - visual
    bar_width = int(confidence)  # 0-100
    # Hum bar ko text se banayenge - 20 blocks
    filled = int(bar_width / 5)
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

    # --- 5. RECOMMENDATION BOX ---
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

    # --- 6. FOOTER ---
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
