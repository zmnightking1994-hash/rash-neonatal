from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, Image, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from PIL import Image as PILImage
import os

# Register fonts
pdfmetrics.registerFont(TTFont('Times New Roman', '/usr/share/fonts/truetype/english/Times-New-Roman.ttf'))
pdfmetrics.registerFont(TTFont('Calibri', '/usr/share/fonts/truetype/english/calibri-regular.ttf'))
registerFontFamily('Times New Roman', normal='Times New Roman', bold='Times New Roman')
registerFontFamily('Calibri', normal='Calibri', bold='Calibri')

# Image directory - using original extracted images
IMG_DIR = "/home/z/my-project/download/original_images"

def get_image(path, width=2.5*inch):
    """Get image with preserved aspect ratio"""
    if not os.path.exists(path):
        print(f"Warning: Image not found: {path}")
        return None
    try:
        pil_img = PILImage.open(path)
        orig_w, orig_h = pil_img.size
        scale = width / orig_w
        height = orig_h * scale
        return Image(path, width=width, height=height)
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        return None

# Create document
doc = SimpleDocTemplate(
    "/home/z/my-project/download/Gomella_Study_Guide.pdf",
    pagesize=letter,
    rightMargin=0.75*inch,
    leftMargin=0.75*inch,
    topMargin=0.75*inch,
    bottomMargin=0.75*inch,
    title="Neonatal Rash and Dermatologic Problems - Study Guide",
    author='Z.ai',
    creator='Z.ai',
    subject='Medical Study Guide with Clinical Photographs from Gomella Neonatology'
)

# Define styles
styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    name='TitleStyle',
    fontName='Times New Roman',
    fontSize=24,
    leading=30,
    alignment=TA_CENTER,
    spaceAfter=12,
    textColor=colors.HexColor('#1F4E79')
)

subtitle_style = ParagraphStyle(
    name='SubtitleStyle',
    fontName='Times New Roman',
    fontSize=14,
    leading=18,
    alignment=TA_CENTER,
    spaceAfter=24,
    textColor=colors.HexColor('#4A4A4A')
)

section_style = ParagraphStyle(
    name='SectionStyle',
    fontName='Times New Roman',
    fontSize=16,
    leading=20,
    spaceBefore=18,
    spaceAfter=12,
    textColor=colors.HexColor('#1F4E79')
)

subsection_style = ParagraphStyle(
    name='SubsectionStyle',
    fontName='Times New Roman',
    fontSize=13,
    leading=16,
    spaceBefore=12,
    spaceAfter=8,
    textColor=colors.HexColor('#2E75B6')
)

body_style = ParagraphStyle(
    name='BodyStyle',
    fontName='Times New Roman',
    fontSize=11,
    leading=14,
    alignment=TA_JUSTIFY,
    spaceAfter=8
)

key_style = ParagraphStyle(
    name='KeyStyle',
    fontName='Times New Roman',
    fontSize=11,
    leading=14,
    leftIndent=15,
    rightIndent=15,
    spaceBefore=6,
    spaceAfter=6,
    backColor=colors.HexColor('#F0F7FF'),
    borderPadding=8
)

header_style = ParagraphStyle(
    name='TableHeader',
    fontName='Times New Roman',
    fontSize=10,
    textColor=colors.white,
    alignment=TA_CENTER,
    leading=12
)

cell_style = ParagraphStyle(
    name='TableCell',
    fontName='Times New Roman',
    fontSize=9,
    alignment=TA_LEFT,
    leading=11
)

caption_style = ParagraphStyle(
    name='Caption', 
    fontName='Times New Roman', 
    fontSize=9, 
    alignment=TA_CENTER, 
    textColor=colors.grey
)

image_caption_style = ParagraphStyle(
    name='ImageCaption',
    fontName='Times New Roman',
    fontSize=10,
    alignment=TA_CENTER,
    textColor=colors.HexColor('#333333'),
    spaceBefore=4,
    spaceAfter=12
)

toc_style = ParagraphStyle(
    name='TOCStyle',
    fontName='Times New Roman',
    fontSize=12,
    leading=20,
    leftIndent=0
)

toc_sub_style = ParagraphStyle(
    name='TOCSubStyle',
    fontName='Times New Roman',
    fontSize=11,
    leading=18,
    leftIndent=20
)

story = []

# ========== COVER PAGE ==========
story.append(Spacer(1, 80))
story.append(Paragraph("<b>Neonatal Rash and Dermatologic Problems</b>", title_style))
story.append(Spacer(1, 20))
story.append(Paragraph("<b>STUDY GUIDE WITH CLINICAL PHOTOGRAPHS</b>", ParagraphStyle(
    name='CoverSubtitle',
    fontName='Times New Roman',
    fontSize=18,
    leading=24,
    alignment=TA_CENTER,
    textColor=colors.HexColor('#2E75B6')
)))
story.append(Spacer(1, 30))
story.append(Paragraph("Based on Gomella's Neonatology, Chapter 80", subtitle_style))
story.append(Spacer(1, 40))
story.append(Paragraph(
    "A comprehensive guide for identifying, differentiating,<br/>"
    "and managing dermatologic conditions in newborns<br/><br/>"
    "<b>Featuring 21 clinical photographs from the original textbook</b>", 
    ParagraphStyle(name='CoverDesc', fontName='Times New Roman', fontSize=12, alignment=TA_CENTER, leading=16)))
story.append(PageBreak())

# ========== TABLE OF CONTENTS ==========
story.append(Paragraph("<b>Table of Contents</b>", section_style))
story.append(Spacer(1, 12))

toc_items = [
    ("1. Overview and Diagnostic Approach", ""),
    ("    1.1 Key Diagnostic Questions", ""),
    ("    1.2 Lesion Morphology Classification", ""),
    ("2. Benign Skin Disorders (No Treatment Required)", ""),
    ("    2.1 Most Common Benign Rashes - With Photos", ""),
    ("    2.2 Vascular and Pigmented Lesions - With Photos", ""),
    ("3. Infectious Causes of Rashes - With Photos", ""),
    ("    3.1 Bacterial Infections", ""),
    ("    3.2 Viral Infections", ""),
    ("    3.3 Fungal Infections", ""),
    ("4. Rashes by Clinical Presentation - With Photos", ""),
    ("    4.1 Scaling Rashes", ""),
    ("    4.2 Blistering and Bullous Rashes", ""),
    ("    4.3 Petechiae and Purpura", ""),
    ("5. Birthmarks and Pigmentation Disorders - With Photos", ""),
    ("6. Malignant Transformation Risk - With Photos", ""),
    ("7. Diagnostic Workup", ""),
    ("8. Treatment Summary", ""),
    ("9. Quick Reference Tables", ""),
]

for item, _ in toc_items:
    if item.startswith("    "):
        story.append(Paragraph(item, toc_sub_style))
    else:
        story.append(Paragraph(f"<b>{item}</b>", toc_style))

story.append(PageBreak())

# ========== SECTION 1: OVERVIEW ==========
story.append(Paragraph("<b>1. Overview and Diagnostic Approach</b>", section_style))
story.append(Paragraph(
    "A rash is any change of skin that affects its color, appearance, or texture. While the majority of rashes "
    "in newborns are benign and require no treatment, certain rashes require a thorough workup and intervention. "
    "The key to diagnosis lies in careful characterization of the lesion morphology and clinical context.",
    body_style))

story.append(Paragraph("<b>1.1 Key Diagnostic Questions</b>", subsection_style))

questions_data = [
    [Paragraph("<b>Question</b>", header_style), Paragraph("<b>What to Assess</b>", header_style), Paragraph("<b>Clinical Significance</b>", header_style)],
    [Paragraph("What are the characteristics of the rash?", cell_style), 
     Paragraph("Morphology: macular, papular, nodular, vesicular, bullous, pustular", cell_style),
     Paragraph("Lesion morphology aids differential diagnosis significantly", cell_style)],
    [Paragraph("Are there petechiae, purpura, or ecchymosis?", cell_style), 
     Paragraph("Check for blanching with pressure; non-blanching indicates intradermal bleeding", cell_style),
     Paragraph("May indicate thrombocytopenia; widespread petechiae are abnormal", cell_style)],
    [Paragraph("History of congenital infection?", cell_style), 
     Paragraph("TORCH infections, maternal history", cell_style),
     Paragraph("Can cause serious systemic disease requiring intervention", cell_style)],
    [Paragraph("Is the infant ill-appearing?", cell_style), 
     Paragraph("Fever, vital signs, overall clinical appearance", cell_style),
     Paragraph("Well infant = likely benign; ill infant = thorough infectious workup needed", cell_style)],
    [Paragraph("Maternal medications?", cell_style), 
     Paragraph("Pregnancy and delivery meds; breastfeeding medications", cell_style),
     Paragraph("Methimazole, valproic acid associated with aplasia cutis", cell_style)],
]

questions_table = Table(questions_data, colWidths=[1.8*inch, 2.2*inch, 2.5*inch])
questions_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F4E79')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
]))
story.append(questions_table)
story.append(Spacer(1, 12))

# Lesion Morphology
story.append(Paragraph("<b>1.2 Lesion Morphology Classification</b>", subsection_style))

morphology_data = [
    [Paragraph("<b>Term</b>", header_style), Paragraph("<b>Size</b>", header_style), Paragraph("<b>Characteristics</b>", header_style)],
    [Paragraph("Macule", cell_style), Paragraph("< 1 cm", cell_style), Paragraph("Flat lesion, not raised above skin surface", cell_style)],
    [Paragraph("Papule", cell_style), Paragraph("up to 1 cm", cell_style), Paragraph("Raised, solid lesion", cell_style)],
    [Paragraph("Vesicle", cell_style), Paragraph("< 1 cm", cell_style), Paragraph("Raised, filled with clear fluid", cell_style)],
    [Paragraph("Bulla", cell_style), Paragraph("> 1 cm", cell_style), Paragraph("Large, filled with clear fluid", cell_style)],
    [Paragraph("Pustule", cell_style), Paragraph("Variable", cell_style), Paragraph("Raised, filled with purulent fluid", cell_style)],
    [Paragraph("Petechiae", cell_style), Paragraph("Pinpoint", cell_style), Paragraph("Tiny red dots, non-blanching", cell_style)],
    [Paragraph("Purpura", cell_style), Paragraph("Larger", cell_style), Paragraph("Large flat area of blood, non-blanching", cell_style)],
]

morphology_table = Table(morphology_data, colWidths=[1.3*inch, 1*inch, 4.2*inch])
morphology_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F4E79')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('ALIGN', (1, 1), (1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(morphology_table)

# ========== SECTION 2: BENIGN DISORDERS WITH ORIGINAL PHOTOS ==========
story.append(PageBreak())
story.append(Paragraph("<b>2. Benign Skin Disorders (No Treatment Required)</b>", section_style))

story.append(Paragraph("<b>2.1 Most Common Benign Rashes</b>", subsection_style))

# Aplasia Cutis
story.append(Spacer(1, 8))
story.append(Paragraph("<b><i>Aplasia Cutis Congenita</i></b>", subsection_style))
img = get_image(os.path.join(IMG_DIR, "01_aplasia_cutis.jpeg"), width=2.5*inch)
if img:
    story.append(img)
    story.append(Paragraph("<i>Figure 1: Aplasia cutis congenita on scalp - localized absence of skin</i>", image_caption_style))

aplasia_data = [
    [Paragraph("<b>Feature</b>", header_style), Paragraph("<b>Description</b>", header_style)],
    [Paragraph("Appearance", cell_style), Paragraph("Localized absence of skin, most commonly on scalp", cell_style)],
    [Paragraph("Cause", cell_style), Paragraph("Can be associated with methimazole or valproic acid exposure in pregnancy", cell_style)],
    [Paragraph("Treatment", cell_style), Paragraph("Small lesions: local wound care; Large lesions: may require surgical excision, skin grafting", cell_style)],
]
aplasia_table = Table(aplasia_data, colWidths=[1.5*inch, 5*inch])
aplasia_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E75B6')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(aplasia_table)

# Erythema Toxicum
story.append(Spacer(1, 12))
story.append(Paragraph("<b><i>Erythema Toxicum</i></b> (Most Common Newborn Rash)", subsection_style))
img = get_image(os.path.join(IMG_DIR, "02_erythema_toxicum.jpeg"), width=2.5*inch)
if img:
    story.append(img)
    story.append(Paragraph("<i>Figure 2: Erythema toxicum - erythematous macules with central papules</i>", image_caption_style))

et_data = [
    [Paragraph("<b>Feature</b>", header_style), Paragraph("<b>Description</b>", header_style)],
    [Paragraph("Appearance", cell_style), Paragraph("Erythematous macules with central papule or pustule", cell_style)],
    [Paragraph("Timing", cell_style), Paragraph("First 48 hours of life; can be present at birth", cell_style)],
    [Paragraph("Location", cell_style), Paragraph("Trunk, extremities, perineum; more common in term infants", cell_style)],
    [Paragraph("Course", cell_style), Paragraph("Resolves by 2 weeks; new lesions may appear", cell_style)],
    [Paragraph("Diagnosis", cell_style), Paragraph("Wright stain shows eosinophils (vs neutrophils in infection)", cell_style)],
]
et_table = Table(et_data, colWidths=[1.5*inch, 5*inch])
et_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E75B6')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(et_table)

# Transient Neonatal Pustular Melanosis
story.append(Spacer(1, 12))
story.append(Paragraph("<b><i>Transient Neonatal Pustular Melanosis</i></b>", subsection_style))
img = get_image(os.path.join(IMG_DIR, "03_transient_pustular_melanosis.jpeg"), width=2.5*inch)
if img:
    story.append(img)
    story.append(Paragraph("<i>Figure 3: Transient neonatal pustular melanosis - pustules and hyperpigmented macules</i>", image_caption_style))

tnpm_data = [
    [Paragraph("<b>Feature</b>", header_style), Paragraph("<b>Description</b>", header_style)],
    [Paragraph("Appearance", cell_style), Paragraph("2-5 mm pustules present at birth", cell_style)],
    [Paragraph("Location", cell_style), Paragraph("Face, sacrum; typically in full-term infants", cell_style)],
    [Paragraph("Course", cell_style), Paragraph("Pustules resolve in 48 hours; hyperpigmented macules fade over months", cell_style)],
]
tnpm_table = Table(tnpm_data, colWidths=[1.5*inch, 5*inch])
tnpm_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E75B6')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(tnpm_table)

# Milia
story.append(PageBreak())
story.append(Paragraph("<b><i>Milia</i></b>", subsection_style))
img = get_image(os.path.join(IMG_DIR, "04_milia.jpeg"), width=2.5*inch)
if img:
    story.append(img)
    story.append(Paragraph("<i>Figure 4: Milia - tiny white-yellow papules on face</i>", image_caption_style))

milia_data = [
    [Paragraph("<b>Feature</b>", header_style), Paragraph("<b>Description</b>", header_style)],
    [Paragraph("Appearance", cell_style), Paragraph("Tiny 1-mm white-yellow papules", cell_style)],
    [Paragraph("Location", cell_style), Paragraph("Face, chin, forehead, scalp", cell_style)],
    [Paragraph("Cause", cell_style), Paragraph("Sebaceous retention cysts", cell_style)],
    [Paragraph("Course", cell_style), Paragraph("Resolves spontaneously; no treatment needed", cell_style)],
]
milia_table = Table(milia_data, colWidths=[1.5*inch, 5*inch])
milia_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E75B6')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(milia_table)

# Acropustulosis
story.append(Spacer(1, 12))
story.append(Paragraph("<b><i>Acropustulosis of Infancy</i></b>", subsection_style))
img = get_image(os.path.join(IMG_DIR, "05_acropustulosis.jpeg"), width=2.5*inch)
if img:
    story.append(img)
    story.append(Paragraph("<i>Figure 5: Acropustulosis of infancy - vesicopustules on palms and soles</i>", image_caption_style))

acro_data = [
    [Paragraph("<b>Feature</b>", header_style), Paragraph("<b>Description</b>", header_style)],
    [Paragraph("Appearance", cell_style), Paragraph("Pruritic vesicopustules", cell_style)],
    [Paragraph("Location", cell_style), Paragraph("Palmar surface of hands, plantar surface of feet", cell_style)],
    [Paragraph("Course", cell_style), Paragraph("Recurrent; each episode lasts 7-14 days", cell_style)],
    [Paragraph("Key Point", cell_style), Paragraph("Distinguish from scabies; intense itching", cell_style)],
]
acro_table = Table(acro_data, colWidths=[1.5*inch, 5*inch])
acro_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E75B6')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(acro_table)

# Neonatal Acne
story.append(Spacer(1, 12))
story.append(Paragraph("<b><i>Neonatal Acne</i></b>", subsection_style))
img = get_image(os.path.join(IMG_DIR, "06_neonatal_acne.jpeg"), width=2.5*inch)
if img:
    story.append(img)
    story.append(Paragraph("<i>Figure 6: Neonatal acne - erythematous comedones and papules</i>", image_caption_style))

acne_data = [
    [Paragraph("<b>Feature</b>", header_style), Paragraph("<b>Description</b>", header_style)],
    [Paragraph("Appearance", cell_style), Paragraph("Erythematous comedones, papules, and pustules", cell_style)],
    [Paragraph("Location", cell_style), Paragraph("Face", cell_style)],
    [Paragraph("Course", cell_style), Paragraph("Resolves over weeks to months", cell_style)],
]
acne_table = Table(acne_data, colWidths=[1.5*inch, 5*inch])
acne_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E75B6')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(acne_table)

# Subcutaneous Fat Necrosis
story.append(PageBreak())
story.append(Paragraph("<b><i>Subcutaneous Fat Necrosis</i></b>", subsection_style))
img = get_image(os.path.join(IMG_DIR, "07_subcutaneous_fat_necrosis.jpeg"), width=2.5*inch)
if img:
    story.append(img)
    story.append(Paragraph("<i>Figure 7: Subcutaneous fat necrosis - erythematous nodules and plaques</i>", image_caption_style))

sfn_data = [
    [Paragraph("<b>Feature</b>", header_style), Paragraph("<b>Description</b>", header_style)],
    [Paragraph("Appearance", cell_style), Paragraph("Erythematous nodules and plaques", cell_style)],
    [Paragraph("Location", cell_style), Paragraph("Face, back, arms, legs, buttocks (areas of trauma)", cell_style)],
    [Paragraph("Timing", cell_style), Paragraph("First few weeks of life; resolves by 2 months", cell_style)],
    [Paragraph("Complication", cell_style), Paragraph("<b>Hypercalcemia</b> can occur if lesions calcify - monitor calcium!", cell_style)],
]
sfn_table = Table(sfn_data, colWidths=[1.5*inch, 5*inch])
sfn_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E75B6')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(sfn_table)

# Vascular lesions
story.append(Spacer(1, 18))
story.append(Paragraph("<b>2.2 Vascular and Pigmented Lesions</b>", subsection_style))

# Mongolian Spots
story.append(Paragraph("<b><i>Mongolian Spots</i> (Congenital Dermal Melanocytosis)</b>", subsection_style))
img = get_image(os.path.join(IMG_DIR, "08_mongolian_spots.jpeg"), width=2.5*inch)
if img:
    story.append(img)
    story.append(Paragraph("<i>Figure 8: Mongolian spots - blue-black discoloration on lower back/buttocks</i>", image_caption_style))

mong_data = [
    [Paragraph("<b>Feature</b>", header_style), Paragraph("<b>Description</b>", header_style)],
    [Paragraph("Appearance", cell_style), Paragraph("Blue-black macular discoloration", cell_style)],
    [Paragraph("Location", cell_style), Paragraph("Base of spine, buttocks", cell_style)],
    [Paragraph("Prevalence", cell_style), Paragraph(">90% in Black infants; 81% in Asian infants", cell_style)],
    [Paragraph("Course", cell_style), Paragraph("Usually fades over several years", cell_style)],
]
mong_table = Table(mong_data, colWidths=[1.5*inch, 5*inch])
mong_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E75B6')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(mong_table)

# ========== SECTION 3: INFECTIOUS CAUSES ==========
story.append(PageBreak())
story.append(Paragraph("<b>3. Infectious Causes of Rashes</b>", section_style))

story.append(Paragraph("<b>3.1 Bacterial Infections</b>", subsection_style))

# SSSS
story.append(Paragraph("<b><i>Staphylococcal Scalded Skin Syndrome (SSSS)</i></b>", subsection_style))
img = get_image(os.path.join(IMG_DIR, "09_ssss.jpeg"), width=2.5*inch)
if img:
    story.append(img)
    story.append(Paragraph("<i>Figure 9: Staphylococcal scalded skin syndrome - desquamation and erythema</i>", image_caption_style))

ssss_data = [
    [Paragraph("<b>Feature</b>", header_style), Paragraph("<b>Description</b>", header_style)],
    [Paragraph("Cause", cell_style), Paragraph("Toxin-mediated disease (exfoliative toxins A and B)", cell_style)],
    [Paragraph("Appearance", cell_style), Paragraph("Tender scarlatiniform rash with flaking and desquamation", cell_style)],
    [Paragraph("Complications", cell_style), Paragraph("Bacteremia rare; superinfection and dehydration can occur", cell_style)],
    [Paragraph("Treatment", cell_style), Paragraph("IV penicillinase-resistant antistaphylococcal antibiotics; supportive care; fluid management", cell_style)],
]
ssss_table = Table(ssss_data, colWidths=[1.5*inch, 5*inch])
ssss_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#C00000')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FFF0F0')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(ssss_table)

# 3.2 Viral Infections
story.append(Spacer(1, 18))
story.append(Paragraph("<b>3.2 Viral Infections</b>", subsection_style))

# HSV
story.append(Paragraph("<b><i>Herpes Simplex Virus (HSV)</i></b>", subsection_style))
img = get_image(os.path.join(IMG_DIR, "10_hsv.jpeg"), width=2.5*inch)
if img:
    story.append(img)
    story.append(Paragraph("<i>Figure 10: Herpes simplex virus - clustered vesicles with intense erythema</i>", image_caption_style))

hsv_data = [
    [Paragraph("<b>Feature</b>", header_style), Paragraph("<b>Description</b>", header_style)],
    [Paragraph("Types", cell_style), Paragraph("Congenital HSV, Neonatal HSV (birth to 6 weeks)", cell_style)],
    [Paragraph("Forms", cell_style), Paragraph("Disseminated, Localized CNS, SEM (Skin/Eyes/Mouth)", cell_style)],
    [Paragraph("Appearance", cell_style), Paragraph("Erythematous papules/vesicles progressing to pustular clusters", cell_style)],
    [Paragraph("Treatment", cell_style), Paragraph("<b>Start acyclovir early, even if diagnosis not confirmed!</b>", cell_style)],
]
hsv_table = Table(hsv_data, colWidths=[1.5*inch, 5*inch])
hsv_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#C00000')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FFF0F0')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(hsv_table)

# Varicella
story.append(Spacer(1, 12))
story.append(Paragraph("<b><i>Varicella-Zoster</i></b>", subsection_style))
img = get_image(os.path.join(IMG_DIR, "11_varicella.jpeg"), width=2.5*inch)
if img:
    story.append(img)
    story.append(Paragraph("<i>Figure 11: Varicella zoster - vesicles in various stages</i>", image_caption_style))

var_data = [
    [Paragraph("<b>Type</b>", header_style), Paragraph("<b>Features</b>", header_style)],
    [Paragraph("Congenital/Fetal syndrome", cell_style), Paragraph("Acquired in utero < 20 weeks; cicatricial scars at birth", cell_style)],
    [Paragraph("Perinatal varicella", cell_style), Paragraph("Acquired late 3rd trimester; centripetal rash days 10-12", cell_style)],
    [Paragraph("Postnatally acquired", cell_style), Paragraph("Typical chickenpox rash; all stages present", cell_style)],
]
var_table = Table(var_data, colWidths=[1.8*inch, 4.7*inch])
var_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#C00000')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FFF0F0')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(var_table)

# 3.3 Fungal Infections
story.append(PageBreak())
story.append(Paragraph("<b>3.3 Fungal Infections</b>", subsection_style))

# Candidiasis
story.append(Paragraph("<b><i>Congenital Cutaneous Candidiasis</i></b>", subsection_style))
img = get_image(os.path.join(IMG_DIR, "12_candidiasis.jpeg"), width=2.5*inch)
if img:
    story.append(img)
    story.append(Paragraph("<i>Figure 12: Congenital candidiasis - diffuse papules involving palms and soles</i>", image_caption_style))

cand_data = [
    [Paragraph("<b>Feature</b>", header_style), Paragraph("<b>Description</b>", header_style)],
    [Paragraph("Timing", cell_style), Paragraph("Acquired in utero; extensive rash within 12 hours of birth", cell_style)],
    [Paragraph("Key Feature", cell_style), Paragraph("<b>Involves palms and soles</b> (unlike erythema toxicum)", cell_style)],
    [Paragraph("Treatment", cell_style), Paragraph("Systemic antifungals for disseminated; topical for isolated skin lesions", cell_style)],
]
cand_table = Table(cand_data, colWidths=[1.5*inch, 5*inch])
cand_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#C00000')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FFF0F0')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(cand_table)

# ========== SECTION 4: RASHES BY PRESENTATION ==========
story.append(Spacer(1, 18))
story.append(Paragraph("<b>4. Rashes by Clinical Presentation</b>", section_style))

# 4.1 Scaling Rashes
story.append(Paragraph("<b>4.1 Scaling Rashes</b>", subsection_style))

# Ichthyosis
story.append(Paragraph("<b><i>Lamellar Ichthyosis</i></b>", subsection_style))
img = get_image(os.path.join(IMG_DIR, "13_ichthyosis.jpeg"), width=2.5*inch)
if img:
    story.append(img)
    story.append(Paragraph("<i>Figure 13: Lamellar ichthyosis - thick, scaly skin</i>", image_caption_style))

ich_data = [
    [Paragraph("<b>Feature</b>", header_style), Paragraph("<b>Description</b>", header_style)],
    [Paragraph("Types", cell_style), Paragraph("May present as 'harlequin fetus' or 'collodion baby'", cell_style)],
    [Paragraph("Appearance", cell_style), Paragraph("Thick, scaly skin; shiny membrane at birth that peels off", cell_style)],
    [Paragraph("Complications", cell_style), Paragraph("Skin prone to cracking and infection; temperature instability", cell_style)],
    [Paragraph("Treatment", cell_style), Paragraph("Aggressive supportive care; fluid/electrolyte monitoring", cell_style)],
]
ich_table = Table(ich_data, colWidths=[1.5*inch, 5*inch])
ich_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E75B6')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(ich_table)

# Neonatal Lupus
story.append(PageBreak())
story.append(Paragraph("<b><i>Neonatal Lupus</i></b>", subsection_style))
img = get_image(os.path.join(IMG_DIR, "14_neonatal_lupus.jpeg"), width=2.5*inch)
if img:
    story.append(img)
    story.append(Paragraph("<i>Figure 14: Neonatal lupus - annular erythematous papules</i>", image_caption_style))

nl_data = [
    [Paragraph("<b>Feature</b>", header_style), Paragraph("<b>Description</b>", header_style)],
    [Paragraph("Cause", cell_style), Paragraph("Maternal autoantibodies (SSA/Ro, SSB/La)", cell_style)],
    [Paragraph("Appearance", cell_style), Paragraph("0.5-3 cm annular erythematous papules with central scale", cell_style)],
    [Paragraph("Manifestations", cell_style), Paragraph("Skin, Cardiac (heart block), Liver/hematologic", cell_style)],
    [Paragraph("Treatment", cell_style), Paragraph("Cardiac exam, LFTs, CBC; sunscreen; avoid sunlight 4-6 months", cell_style)],
]
nl_table = Table(nl_data, colWidths=[1.5*inch, 5*inch])
nl_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E75B6')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(nl_table)

# 4.2 Blistering Rashes
story.append(Spacer(1, 18))
story.append(Paragraph("<b>4.2 Blistering and Bullous Rashes</b>", subsection_style))

# Epidermolysis Bullosa
story.append(Paragraph("<b><i>Epidermolysis Bullosa</i></b>", subsection_style))
img = get_image(os.path.join(IMG_DIR, "15_epidermolysis_bullosa.jpeg"), width=2.5*inch)
if img:
    story.append(img)
    story.append(Paragraph("<i>Figure 15: Epidermolysis bullosa - congenital absence of skin</i>", image_caption_style))

eb_data = [
    [Paragraph("<b>Feature</b>", header_style), Paragraph("<b>Description</b>", header_style)],
    [Paragraph("Type", cell_style), Paragraph("Group of inherited diseases causing blistering", cell_style)],
    [Paragraph("Appearance", cell_style), Paragraph("Trauma-induced blisters; congenital localized absence of skin", cell_style)],
    [Paragraph("Complications", cell_style), Paragraph("Dysphagia from scarring; infection risk", cell_style)],
    [Paragraph("Treatment", cell_style), Paragraph("Meticulous skin care; infection prevention; nutrition support", cell_style)],
]
eb_table = Table(eb_data, colWidths=[1.5*inch, 5*inch])
eb_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E75B6')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(eb_table)

# Incontinentia Pigmenti
story.append(Spacer(1, 12))
story.append(Paragraph("<b><i>Incontinentia Pigmenti</i></b>", subsection_style))
img = get_image(os.path.join(IMG_DIR, "16_incontinentia_pigmenti.jpeg"), width=2.5*inch)
if img:
    story.append(img)
    story.append(Paragraph("<i>Figure 16: Incontinentia pigmenti - linear vesiculobullous lesions</i>", image_caption_style))

ip_data = [
    [Paragraph("<b>Feature</b>", header_style), Paragraph("<b>Description</b>", header_style)],
    [Paragraph("Inheritance", cell_style), Paragraph("Rare X-linked dominant; more common in females", cell_style)],
    [Paragraph("Stage 1", cell_style), Paragraph("Vesiculobullous lesions in linear distribution (can be confused with HSV!)", cell_style)],
    [Paragraph("Associations", cell_style), Paragraph("Neurologic, dental, ophthalmologic abnormalities", cell_style)],
]
ip_table = Table(ip_data, colWidths=[1.5*inch, 5*inch])
ip_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E75B6')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(ip_table)

# ========== SECTION 5: BIRTHMARKS ==========
story.append(PageBreak())
story.append(Paragraph("<b>5. Birthmarks and Vascular Lesions</b>", section_style))

# Port Wine Stain
story.append(Paragraph("<b><i>Port Wine Stain</i> (Nevus Flammeus)</b>", subsection_style))
img = get_image(os.path.join(IMG_DIR, "17_port_wine_stain.jpeg"), width=2.5*inch)
if img:
    story.append(img)
    story.append(Paragraph("<i>Figure 17: Port wine stain - flat capillary angioma</i>", image_caption_style))

pws_data = [
    [Paragraph("<b>Feature</b>", header_style), Paragraph("<b>Description</b>", header_style)],
    [Paragraph("Appearance", cell_style), Paragraph("Flat pink-red capillary angioma", cell_style)],
    [Paragraph("Location", cell_style), Paragraph("Usually face or extremities", cell_style)],
    [Paragraph("Course", cell_style), Paragraph("Permanent; does not fade", cell_style)],
    [Paragraph("Associations", cell_style), Paragraph("Sturge-Weber syndrome (if V1 distribution); Klippel-Trenaunay syndrome", cell_style)],
]
pws_table = Table(pws_data, colWidths=[1.5*inch, 5*inch])
pws_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2E75B6')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(pws_table)

# Blueberry Muffin
story.append(Spacer(1, 12))
story.append(Paragraph("<b><i>'Blueberry Muffin' Lesions</i></b>", subsection_style))
img = get_image(os.path.join(IMG_DIR, "18_blueberry_muffin.jpeg"), width=2.5*inch)
if img:
    story.append(img)
    story.append(Paragraph("<i>Figure 18: 'Blueberry muffin' lesions - widespread purpura and papules</i>", image_caption_style))

bm_data = [
    [Paragraph("<b>Feature</b>", header_style), Paragraph("<b>Description</b>", header_style)],
    [Paragraph("Appearance", cell_style), Paragraph("Widespread purpura and papules", cell_style)],
    [Paragraph("Causes", cell_style), Paragraph("TORCH infections, Hemolytic disease, Neuroblastoma, Congenital leukemia", cell_style)],
    [Paragraph("Workup", cell_style), Paragraph("TORCH titers, CBC, consider malignancy workup", cell_style)],
]
bm_table = Table(bm_data, colWidths=[1.5*inch, 5*inch])
bm_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#C00000')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FFF0F0')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(bm_table)

# ========== SECTION 6: MALIGNANT RISK ==========
story.append(Spacer(1, 18))
story.append(Paragraph("<b>6. Malignant Transformation Risk</b>", section_style))

# Melanocytic Nevus
story.append(Paragraph("<b><i>Congenital Melanocytic Nevus</i></b>", subsection_style))
img = get_image(os.path.join(IMG_DIR, "19_melanocytic_nevus.jpeg"), width=2.5*inch)
if img:
    story.append(img)
    story.append(Paragraph("<i>Figure 19: Congenital melanocytic nevus - pigmented lesion on scalp</i>", image_caption_style))

mn_data = [
    [Paragraph("<b>Size</b>", header_style), Paragraph("<b>Melanoma Risk</b>", header_style), Paragraph("<b>Management</b>", header_style)],
    [Paragraph("Small (< 1.5 cm)", cell_style), Paragraph("Small risk", cell_style), Paragraph("Monitor; removal optional", cell_style)],
    [Paragraph("Intermediate (< 20 cm)", cell_style), Paragraph("Small risk", cell_style), Paragraph("Monitor; consider removal", cell_style)],
    [Paragraph("Large/Giant (> 20 cm)", cell_style), Paragraph("5-15% risk", cell_style), Paragraph("Removal recommended; monitor for neurocutaneous melanosis", cell_style)],
]
mn_table = Table(mn_data, colWidths=[1.8*inch, 1.5*inch, 3.2*inch])
mn_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#C00000')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FFF0F0')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(mn_table)

# Giant Nevus
story.append(PageBreak())
story.append(Paragraph("<b><i>Giant Congenital Melanocytic Nevus</i></b>", subsection_style))
img = get_image(os.path.join(IMG_DIR, "20_giant_nevus.jpeg"), width=2.5*inch)
if img:
    story.append(img)
    story.append(Paragraph("<i>Figure 20: Giant congenital melanocytic nevus - extensive pigmented lesion</i>", image_caption_style))

gn_data = [
    [Paragraph("<b>Feature</b>", header_style), Paragraph("<b>Description</b>", header_style)],
    [Paragraph("Size", cell_style), Paragraph("> 40 cm in diameter", cell_style)],
    [Paragraph("Melanoma risk", cell_style), Paragraph("5-15% lifetime risk", cell_style)],
    [Paragraph("Additional risk", cell_style), Paragraph("Neurocutaneous melanosis - MRI screening may be indicated", cell_style)],
    [Paragraph("Management", cell_style), Paragraph("Dermatology referral; consider surgical removal; close monitoring", cell_style)],
]
gn_table = Table(gn_data, colWidths=[1.5*inch, 5*inch])
gn_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#C00000')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FFF0F0')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(gn_table)

# Sebaceous Nevus
story.append(Spacer(1, 12))
story.append(Paragraph("<b><i>Sebaceous Nevus of Jadassohn</i></b>", subsection_style))
img = get_image(os.path.join(IMG_DIR, "21_sebaceous_nevus.jpeg"), width=2.5*inch)
if img:
    story.append(img)
    story.append(Paragraph("<i>Figure 21: Sebaceous nevus of Jadassohn - yellow-orange plaque on scalp</i>", image_caption_style))

sn_data = [
    [Paragraph("<b>Feature</b>", header_style), Paragraph("<b>Description</b>", header_style)],
    [Paragraph("Appearance", cell_style), Paragraph("Congenital hamartomatous lesion; yellow-orange waxy plaque", cell_style)],
    [Paragraph("Location", cell_style), Paragraph("Scalp", cell_style)],
    [Paragraph("Prevalence", cell_style), Paragraph("~0.3% of newborns", cell_style)],
    [Paragraph("Malignant potential", cell_style), Paragraph("Can transform to basal cell carcinoma or benign trichoblastoma", cell_style)],
]
sn_table = Table(sn_data, colWidths=[1.5*inch, 5*inch])
sn_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#C00000')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FFF0F0')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(sn_table)

# ========== SECTION 7: DIAGNOSTIC WORKUP ==========
story.append(PageBreak())
story.append(Paragraph("<b>7. Diagnostic Workup</b>", section_style))

story.append(Paragraph("<b>7.1 Laboratory Studies</b>", subsection_style))

lab_data = [
    [Paragraph("<b>Test</b>", header_style), Paragraph("<b>Indication</b>", header_style), Paragraph("<b>Findings</b>", header_style)],
    [Paragraph("Sepsis evaluation", cell_style), Paragraph("Systemic infection suspected", cell_style), Paragraph("Cultures, PCR from lesions", cell_style)],
    [Paragraph("CBC, platelets", cell_style), Paragraph("Active bleeding suspected", cell_style), Paragraph("Thrombocytopenia, anemia", cell_style)],
    [Paragraph("TORCH titers", cell_style), Paragraph("Congenital infection", cell_style), Paragraph("Elevated IgM titers", cell_style)],
    [Paragraph("KOH prep", cell_style), Paragraph("Candida/fungal", cell_style), Paragraph("Pseudohyphae", cell_style)],
    [Paragraph("Wright stain", cell_style), Paragraph("Differentiate rash type", cell_style), Paragraph("Eosinophils (benign) vs Neutrophils (infection)", cell_style)],
    [Paragraph("Mineral oil prep", cell_style), Paragraph("Scabies", cell_style), Paragraph("Mites and ova", cell_style)],
    [Paragraph("PCR/DFA", cell_style), Paragraph("Herpes", cell_style), Paragraph("HSV DNA", cell_style)],
    [Paragraph("Coagulation studies", cell_style), Paragraph("Bleeding disorder/DIC", cell_style), Paragraph("Prolonged PT/PTT, low fibrinogen", cell_style)],
]
lab_table = Table(lab_data, colWidths=[1.8*inch, 2*inch, 2.7*inch])
lab_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F4E79')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(lab_table)

# ========== SECTION 8: TREATMENT SUMMARY ==========
story.append(Spacer(1, 18))
story.append(Paragraph("<b>8. Treatment Summary</b>", section_style))

treatment_data = [
    [Paragraph("<b>Condition</b>", header_style), Paragraph("<b>Treatment</b>", header_style)],
    [Paragraph("Benign skin disorders", cell_style), Paragraph("No treatment necessary; parental reassurance", cell_style)],
    [Paragraph("Aplasia cutis congenita", cell_style), Paragraph("Local wound care; larger lesions may need surgical excision", cell_style)],
    [Paragraph("Skin/soft tissue infections", cell_style), Paragraph("I&D; cultures; antibiotics (nafcillin/vancomycin)", cell_style)],
    [Paragraph("HSV infection", cell_style), Paragraph("<b>Start acyclovir early, even before confirmed diagnosis!</b>", cell_style)],
    [Paragraph("Candida", cell_style), Paragraph("Systemic antifungals for disseminated; topical for skin lesions", cell_style)],
    [Paragraph("Ichthyoses/EB", cell_style), Paragraph("Supportive care; fluid/electrolyte monitoring; infection prevention", cell_style)],
    [Paragraph("Neonatal lupus", cell_style), Paragraph("Cardiac exam; sunscreen; avoid sunlight 4-6 months", cell_style)],
]
treatment_table = Table(treatment_data, colWidths=[2*inch, 4.5*inch])
treatment_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F4E79')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(treatment_table)

# Key point
story.append(Spacer(1, 12))
story.append(Paragraph(
    "<b>Critical Point:</b> Acyclovir is recommended early in cases of infants with a vesicular skin rash, "
    "even if the diagnosis of herpes is not confirmed. Early treatment significantly improves outcomes.",
    key_style))

# ========== SECTION 9: QUICK REFERENCE ==========
story.append(PageBreak())
story.append(Paragraph("<b>9. Quick Reference Tables</b>", section_style))

story.append(Paragraph("<b>9.1 Clinical Pearls</b>", subsection_style))

pearls_data = [
    [Paragraph("<b>Finding</b>", header_style), Paragraph("<b>Think of...</b>", header_style)],
    [Paragraph("Palms and soles involved", cell_style), Paragraph("Congenital candidiasis, Syphilis, Scabies, Acropustulosis", cell_style)],
    [Paragraph("'Blueberry muffin' rash", cell_style), Paragraph("TORCH infections, Hemolytic disease, Neuroblastoma, Leukemia", cell_style)],
    [Paragraph("Non-blanching lesions", cell_style), Paragraph("Thrombocytopenia, DIC, infection - check platelets and coagulation", cell_style)],
    [Paragraph("Vesicles in linear distribution", cell_style), Paragraph("Incontinentia pigmenti vs HSV - differentiate urgently!", cell_style)],
    [Paragraph("Ill-appearing infant with rash", cell_style), Paragraph("Immediate sepsis workup; start acyclovir empirically", cell_style)],
    [Paragraph(">6 café-au-lait spots >5 mm", cell_style), Paragraph("Neurofibromatosis, Tuberous sclerosis", cell_style)],
    [Paragraph("Port wine stain in V1", cell_style), Paragraph("Sturge-Weber syndrome - ophthalmology/neurology evaluation", cell_style)],
    [Paragraph("Eosinophils on Wright stain", cell_style), Paragraph("Erythema toxicum (benign)", cell_style)],
    [Paragraph("Neutrophils on Wright stain", cell_style), Paragraph("Bacterial infection (requires treatment)", cell_style)],
]
pearls_table = Table(pearls_data, colWidths=[2.2*inch, 4.3*inch])
pearls_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F4E79')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(pearls_table)

# Red Flags
story.append(Spacer(1, 18))
story.append(Paragraph("<b>9.2 Red Flags Requiring Immediate Action</b>", subsection_style))

escalate_data = [
    [Paragraph("<b>Red Flag</b>", header_style), Paragraph("<b>Action</b>", header_style)],
    [Paragraph("Ill-appearing/febrile infant with rash", cell_style), Paragraph("Immediate sepsis workup; start acyclovir empirically", cell_style)],
    [Paragraph("Widespread petechiae/purpura", cell_style), Paragraph("Urgent CBC, coagulation; consider sepsis, DIC, leukemia", cell_style)],
    [Paragraph("Vesicular rash in newborn", cell_style), Paragraph("PCR for HSV; start acyclovir pending results", cell_style)],
    [Paragraph("Large/giant melanocytic nevus", cell_style), Paragraph("Dermatology referral; monitor for neurocutaneous melanosis", cell_style)],
    [Paragraph("Port wine stain in V1", cell_style), Paragraph("Evaluate for Sturge-Weber; ophthalmology for glaucoma", cell_style)],
]
escalate_table = Table(escalate_data, colWidths=[2.5*inch, 4*inch])
escalate_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#C00000')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, -1), 'Times New Roman'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FFF0F0')]),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
]))
story.append(escalate_table)

# Build PDF
doc.build(story)
print("PDF with original clinical photographs created successfully!")
