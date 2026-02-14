"""
Neonatal Rash and Dermatologic Problems - Study Guide
A comprehensive Streamlit web application with clinical photographs
Based on Gomella's Neonatology, Chapter 80
"""

import streamlit as st
from PIL import Image
import os

# Page configuration
st.set_page_config(
    page_title="Neonatal Dermatology Study Guide",
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Image directory
IMG_DIR = "/home/z/my-project/download/original_images"

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
    }
    .condition-card {
        border-left: 4px solid;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 0.25rem;
    }
    .benign { border-color: #22c55e; background-color: #f0fdf4; }
    .infectious { border-color: #ef4444; background-color: #fef2f2; }
    .serious { border-color: #f97316; background-color: #fff7ed; }
    .malignant { border-color: #a855f7; background-color: #faf5ff; }
    .red-flag {
        background-color: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
    .pearl-box {
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Data structures
CONDITIONS = {
    "benign": [
        {
            "name": "Aplasia Cutis Congenita",
            "image": "01_aplasia_cutis.jpeg",
            "figure": "Figure 1",
            "features": [
                ("Appearance", "Localized absence of skin, most commonly on scalp"),
                ("Cause", "Can be associated with methimazole or valproic acid exposure in pregnancy"),
                ("Treatment", "Small lesions: local wound care; Large lesions: may require surgical excision, skin grafting"),
            ]
        },
        {
            "name": "Erythema Toxicum (Most Common Newborn Rash)",
            "image": "02_erythema_toxicum.jpeg",
            "figure": "Figure 2",
            "features": [
                ("Appearance", "Erythematous macules with central papule or pustule"),
                ("Timing", "First 48 hours of life; can be present at birth"),
                ("Location", "Trunk, extremities, perineum; more common in term infants"),
                ("Course", "Resolves by 2 weeks; new lesions may appear"),
                ("Diagnosis", "Wright stain shows eosinophils (vs neutrophils in infection)"),
            ]
        },
        {
            "name": "Transient Neonatal Pustular Melanosis",
            "image": "03_transient_pustular_melanosis.jpeg",
            "figure": "Figure 3",
            "features": [
                ("Appearance", "2-5 mm pustules present at birth"),
                ("Location", "Face, sacrum; typically in full-term infants"),
                ("Course", "Pustules resolve in 48 hours; hyperpigmented macules fade over months"),
            ]
        },
        {
            "name": "Milia",
            "image": "04_milia.jpeg",
            "figure": "Figure 4",
            "features": [
                ("Appearance", "Tiny 1-mm white-yellow papules"),
                ("Location", "Face, chin, forehead, scalp"),
                ("Cause", "Sebaceous retention cysts"),
                ("Course", "Resolves spontaneously; no treatment needed"),
            ]
        },
        {
            "name": "Acropustulosis of Infancy",
            "image": "05_acropustulosis.jpeg",
            "figure": "Figure 5",
            "features": [
                ("Appearance", "Pruritic vesicopustules"),
                ("Location", "Palmar surface of hands, plantar surface of feet"),
                ("Course", "Recurrent; each episode lasts 7-14 days"),
                ("Key Point", "Distinguish from scabies; intense itching"),
            ]
        },
        {
            "name": "Neonatal Acne",
            "image": "06_neonatal_acne.jpeg",
            "figure": "Figure 6",
            "features": [
                ("Appearance", "Erythematous comedones, papules, and pustules"),
                ("Location", "Face"),
                ("Course", "Resolves over weeks to months; no treatment needed"),
            ]
        },
        {
            "name": "Subcutaneous Fat Necrosis",
            "image": "07_subcutaneous_fat_necrosis.jpeg",
            "figure": "Figure 7",
            "features": [
                ("Appearance", "Erythematous nodules and plaques"),
                ("Location", "Face, back, arms, legs, buttocks (areas of trauma)"),
                ("Timing", "First few weeks of life; resolves by 2 months"),
                ("Complication", "⚠️ Hypercalcemia can occur if lesions calcify - monitor calcium!"),
            ]
        },
        {
            "name": "Mongolian Spots (Congenital Dermal Melanocytosis)",
            "image": "08_mongolian_spots.jpeg",
            "figure": "Figure 8",
            "features": [
                ("Appearance", "Blue-black macular discoloration"),
                ("Location", "Base of spine, buttocks"),
                ("Prevalence", ">90% in Black infants; 81% in Asian infants"),
                ("Course", "Usually fades over several years"),
            ]
        },
    ],
    "infectious": [
        {
            "name": "Staphylococcal Scalded Skin Syndrome (SSSS)",
            "image": "09_ssss.jpeg",
            "figure": "Figure 9",
            "features": [
                ("Cause", "Toxin-mediated disease (exfoliative toxins A and B)"),
                ("Appearance", "Tender scarlatiniform rash with flaking and desquamation"),
                ("Complications", "Bacteremia rare; superinfection and dehydration can occur"),
                ("Treatment", "IV penicillinase-resistant antistaphylococcal antibiotics; supportive care; fluid management"),
            ]
        },
        {
            "name": "Herpes Simplex Virus (HSV)",
            "image": "10_hsv.jpeg",
            "figure": "Figure 10",
            "features": [
                ("Types", "Congenital HSV, Neonatal HSV (birth to 6 weeks)"),
                ("Forms", "Disseminated, Localized CNS, SEM (Skin/Eyes/Mouth)"),
                ("Appearance", "Erythematous papules/vesicles progressing to pustular clusters with intense erythema"),
                ("Treatment", "🔴 Start acyclovir early, even if diagnosis not confirmed!"),
            ]
        },
        {
            "name": "Varicella-Zoster",
            "image": "11_varicella.jpeg",
            "figure": "Figure 11",
            "features": [
                ("Congenital/Fetal syndrome", "Acquired in utero < 20 weeks; cicatricial scars at birth"),
                ("Perinatal varicella", "Acquired late 3rd trimester; centripetal rash days 10-12"),
                ("Postnatally acquired", "Typical chickenpox rash; all stages present (red macules, clear vesicles, crusting)"),
            ]
        },
        {
            "name": "Congenital Cutaneous Candidiasis",
            "image": "12_candidiasis.jpeg",
            "figure": "Figure 12",
            "features": [
                ("Timing", "Acquired in utero; extensive rash within 12 hours of birth"),
                ("Key Feature", "⚠️ Involves palms and soles (unlike erythema toxicum)"),
                ("Treatment", "Systemic antifungals for disseminated; topical for isolated skin lesions"),
            ]
        },
    ],
    "other": [
        {
            "name": "Lamellar Ichthyosis",
            "image": "13_ichthyosis.jpeg",
            "figure": "Figure 13",
            "features": [
                ("Types", "May present as 'harlequin fetus' or 'collodion baby'"),
                ("Appearance", "Thick, scaly skin; shiny membrane at birth that peels off"),
                ("Complications", "Skin prone to cracking and infection; temperature instability"),
                ("Treatment", "Aggressive supportive care; fluid/electrolyte monitoring"),
            ]
        },
        {
            "name": "Neonatal Lupus",
            "image": "14_neonatal_lupus.jpeg",
            "figure": "Figure 14",
            "features": [
                ("Cause", "Maternal autoantibodies (SSA/Ro, SSB/La)"),
                ("Appearance", "0.5-3 cm annular erythematous papules with central scale"),
                ("Manifestations", "Skin, Cardiac (heart block), Liver/hematologic"),
                ("Treatment", "Cardiac exam, LFTs, CBC; sunscreen; avoid sunlight 4-6 months"),
            ]
        },
        {
            "name": "Epidermolysis Bullosa",
            "image": "15_epidermolysis_bullosa.jpeg",
            "figure": "Figure 15",
            "features": [
                ("Type", "Group of inherited diseases causing blistering"),
                ("Appearance", "Trauma-induced blisters; congenital localized absence of skin"),
                ("Complications", "Dysphagia from scarring; infection risk"),
                ("Treatment", "Meticulous skin care; infection prevention; nutrition support"),
            ]
        },
        {
            "name": "Incontinentia Pigmenti",
            "image": "16_incontinentia_pigmenti.jpeg",
            "figure": "Figure 16",
            "features": [
                ("Inheritance", "Rare X-linked dominant; more common in females"),
                ("Stage 1", "Vesiculobullous lesions in linear distribution (can be confused with HSV!)"),
                ("Associations", "Neurologic, dental, ophthalmologic abnormalities"),
            ]
        },
        {
            "name": "Port Wine Stain (Nevus Flammeus)",
            "image": "17_port_wine_stain.jpeg",
            "figure": "Figure 17",
            "features": [
                ("Appearance", "Flat pink-red capillary angioma"),
                ("Location", "Usually face or extremities"),
                ("Course", "Permanent; does not fade"),
                ("Associations", "Sturge-Weber syndrome (if V1 distribution); Klippel-Trenaunay syndrome"),
            ]
        },
        {
            "name": "'Blueberry Muffin' Lesions",
            "image": "18_blueberry_muffin.jpeg",
            "figure": "Figure 18",
            "features": [
                ("Appearance", "Widespread purpura and papules"),
                ("Causes", "TORCH infections, Hemolytic disease, Neuroblastoma, Congenital leukemia"),
                ("Workup", "TORCH titers, CBC, consider malignancy workup"),
            ]
        },
    ],
    "malignant": [
        {
            "name": "Congenital Melanocytic Nevus",
            "image": "19_melanocytic_nevus.jpeg",
            "figure": "Figure 19",
            "features": [
                ("Small (< 1.5 cm)", "Small melanoma risk; monitor; removal optional"),
                ("Intermediate (< 20 cm)", "Small risk; monitor; consider removal"),
                ("Large/Giant (> 20 cm)", "⚠️ 5-15% melanoma risk; removal recommended; monitor for neurocutaneous melanosis"),
            ]
        },
        {
            "name": "Giant Congenital Melanocytic Nevus",
            "image": "20_giant_nevus.jpeg",
            "figure": "Figure 20",
            "features": [
                ("Size", "> 40 cm in diameter"),
                ("Melanoma risk", "5-15% lifetime risk"),
                ("Additional risk", "Neurocutaneous melanosis - MRI screening may be indicated"),
                ("Management", "Dermatology referral; consider surgical removal; close monitoring"),
            ]
        },
        {
            "name": "Sebaceous Nevus of Jadassohn",
            "image": "21_sebaceous_nevus.jpeg",
            "figure": "Figure 21",
            "features": [
                ("Appearance", "Congenital hamartomatous lesion; yellow-orange waxy plaque"),
                ("Location", "Scalp"),
                ("Prevalence", "~0.3% of newborns"),
                ("Malignant potential", "Can transform to basal cell carcinoma or benign trichoblastoma"),
            ]
        },
    ],
}

CLINICAL_PEARLS = [
    ("Palms and soles involved", "Congenital candidiasis, Syphilis, Scabies, Acropustulosis"),
    ("'Blueberry muffin' rash", "TORCH infections, Hemolytic disease, Neuroblastoma, Leukemia"),
    ("Non-blanching lesions", "Thrombocytopenia, DIC, infection - check platelets and coagulation"),
    ("Vesicles in linear distribution", "Incontinentia pigmenti vs HSV - differentiate urgently!"),
    ("Ill-appearing infant with rash", "Immediate sepsis workup; start acyclovir empirically"),
    (">6 café-au-lait spots >5 mm", "Neurofibromatosis, Tuberous sclerosis"),
    ("Port wine stain in V1", "Sturge-Weber syndrome - ophthalmology/neurology evaluation"),
    ("Eosinophils on Wright stain", "Erythema toxicum (benign)"),
    ("Neutrophils on Wright stain", "Bacterial infection (requires treatment)"),
]

RED_FLAGS = [
    ("Ill-appearing/febrile infant with rash", "Immediate sepsis workup; start acyclovir empirically"),
    ("Widespread petechiae/purpura", "Urgent CBC, coagulation; consider sepsis, DIC, leukemia"),
    ("Vesicular rash in newborn", "PCR for HSV; start acyclovir pending results"),
    ("Large/giant melanocytic nevus", "Dermatology referral; monitor for neurocutaneous melanosis"),
    ("Port wine stain in V1", "Evaluate for Sturge-Weber; ophthalmology for glaucoma"),
]

LAB_TESTS = [
    ("Sepsis evaluation", "Systemic infection suspected", "Cultures, PCR from lesions"),
    ("CBC, platelets", "Active bleeding suspected", "Thrombocytopenia, anemia"),
    ("TORCH titers", "Congenital infection", "Elevated IgM titers"),
    ("KOH prep", "Candida/fungal", "Pseudohyphae"),
    ("Wright stain", "Differentiate rash type", "Eosinophils (benign) vs Neutrophils (infection)"),
    ("Mineral oil prep", "Scabies", "Mites and ova"),
    ("PCR/DFA", "Herpes", "HSV DNA"),
    ("Coagulation studies", "Bleeding disorder/DIC", "Prolonged PT/PTT, low fibrinogen"),
]

TREATMENTS = [
    ("Benign skin disorders", "No treatment necessary; parental reassurance"),
    ("Aplasia cutis congenita", "Local wound care; larger lesions may need surgical excision"),
    ("Skin/soft tissue infections", "I&D; cultures; antibiotics (nafcillin/vancomycin)"),
    ("HSV infection", "🔴 Start acyclovir early, even before confirmed diagnosis!"),
    ("Candida", "Systemic antifungals for disseminated; topical for skin lesions"),
    ("Ichthyoses/EB", "Supportive care; fluid/electrolyte monitoring; infection prevention"),
    ("Neonatal lupus", "Cardiac exam; sunscreen; avoid sunlight 4-6 months"),
]

DIAGNOSTIC_QUESTIONS = [
    ("What are the rash characteristics?", "Morphology: macular, papular, vesicular, bullous, pustular", "Lesion morphology aids differential diagnosis"),
    ("Are there petechiae, purpura, ecchymosis?", "Check for blanching; non-blanching = intradermal bleeding", "May indicate thrombocytopenia"),
    ("History of congenital infection?", "TORCH infections, maternal history", "Can cause serious systemic disease"),
    ("Is the infant ill-appearing?", "Fever, vital signs, overall appearance", "Well infant = likely benign; ill = workup needed"),
    ("Maternal medications?", "Pregnancy/delivery meds; breastfeeding meds", "Methimazole, valproic acid → aplasia cutis"),
]

LESION_MORPHOLOGY = [
    ("Macule", "< 1 cm", "Flat lesion"),
    ("Papule", "up to 1 cm", "Raised, solid"),
    ("Vesicle", "< 1 cm", "Clear fluid"),
    ("Bulla", "> 1 cm", "Large, clear fluid"),
    ("Pustule", "Variable", "Purulent fluid"),
    ("Petechiae", "Pinpoint", "Non-blanching red dots"),
    ("Purpura", "Larger", "Non-blanching, blood under tissue"),
    ("Nodule", "up to 2 cm", "Raised, deeper"),
]


def load_image(image_name):
    """Load image from the images directory"""
    image_path = os.path.join(IMG_DIR, image_name)
    if os.path.exists(image_path):
        return Image.open(image_path)
    return None


def display_condition(condition, category_style):
    """Display a single condition with image and features"""
    st.markdown(f'<div class="condition-card {category_style}">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        img = load_image(condition["image"])
        if img:
            st.image(img, use_container_width=True)
            st.caption(condition["figure"])
    
    with col2:
        st.markdown(f"### {condition['name']}")
        for label, value in condition["features"]:
            st.markdown(f"**{label}:** {value}")
    
    st.markdown('</div>', unsafe_allow_html=True)


# Main App
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 style="color: white; margin: 0;">👶 Neonatal Rash and Dermatologic Problems</h1>
        <p style="color: #bfdbfe; margin: 0.5rem 0 0 0;">Study Guide with Clinical Photographs - Based on Gomella's Neonatology, Chapter 80</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("📚 Navigation")
    page = st.sidebar.radio(
        "Go to:",
        ["Overview", "Benign Rashes", "Infectious Rashes", "Other Conditions", 
         "Malignant Risk", "Quick Reference", "Search All"],
        label_visibility="collapsed"
    )
    
    # Search in sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔍 Quick Search")
    search_term = st.sidebar.text_input("Search conditions...", key="search")
    
    # Overview Page
    if page == "Overview":
        st.header("1. Key Diagnostic Questions")
        st.markdown("Ask these questions when evaluating a neonatal rash:")
        
        questions_df = [{
            "Question": q[0],
            "What to Assess": q[1],
            "Clinical Significance": q[2]
        } for q in DIAGNOSTIC_QUESTIONS]
        st.table(questions_df)
        
        st.header("2. Lesion Morphology Classification")
        morphology_cols = st.columns(4)
        for i, (term, size, desc) in enumerate(LESION_MORPHOLOGY):
            with morphology_cols[i % 4]:
                st.markdown(f"""
                <div style="background: white; padding: 1rem; border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <h4 style="color: #1e40af; margin: 0;">{term}</h4>
                    <p style="color: #6b7280; font-size: 0.875rem; margin: 0.25rem 0;">{size}</p>
                    <p style="margin: 0;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.header("3. Critical Point")
        st.warning("🔴 Acyclovir is recommended early in cases of infants with a vesicular skin rash, even if the diagnosis of herpes is not confirmed. Early treatment significantly improves outcomes.")
    
    # Benign Rashes Page
    elif page == "Benign Rashes":
        st.header("🌿 Benign Skin Disorders")
        st.info("These rashes are very common in newborns and typically resolve spontaneously without intervention. Recognition helps avoid unnecessary testing.")
        
        for condition in CONDITIONS["benign"]:
            display_condition(condition, "benign")
    
    # Infectious Rashes Page
    elif page == "Infectious Rashes":
        st.header("🦠 Infectious Causes of Rashes")
        st.error("These typically require intervention. Common pathogens: *S. aureus*, *Streptococcus*, *Candida albicans*, and HSV.")
        
        for condition in CONDITIONS["infectious"]:
            display_condition(condition, "infectious")
    
    # Other Conditions Page
    elif page == "Other Conditions":
        st.header("⚠️ Other Conditions")
        
        st.subheader("Scaling & Blistering Rashes")
        for condition in CONDITIONS["other"][:4]:
            display_condition(condition, "serious")
        
        st.subheader("Vascular Birthmarks & Serious Lesions")
        for condition in CONDITIONS["other"][4:]:
            display_condition(condition, "serious")
    
    # Malignant Risk Page
    elif page == "Malignant Risk":
        st.header("⚠️ Conditions with Malignant Transformation Risk")
        st.warning("These lesions require close monitoring and may need surgical intervention.")
        
        for condition in CONDITIONS["malignant"]:
            display_condition(condition, "malignant")
    
    # Quick Reference Page
    elif page == "Quick Reference":
        st.header("📖 Quick Reference")
        
        # Clinical Pearls
        st.subheader("Clinical Pearls")
        for finding, diagnosis in CLINICAL_PEARLS:
            st.markdown(f"""
            <div class="pearl-box">
                <strong>{finding}</strong><br/>
                → {diagnosis}
            </div>
            """, unsafe_allow_html=True)
        
        # Red Flags
        st.subheader("🚨 Red Flags - Immediate Action Required")
        for flag, action in RED_FLAGS:
            st.markdown(f"""
            <div class="red-flag">
                <strong>⚠️ {flag}</strong><br/>
                <span style="color: #dc2626;">→ {action}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Laboratory Studies
        st.subheader("Laboratory Studies")
        lab_df = [{
            "Test": t[0],
            "Indication": t[1],
            "Findings": t[2]
        } for t in LAB_TESTS]
        st.table(lab_df)
        
        # Treatment Summary
        st.subheader("Treatment Summary")
        treatment_df = [{
            "Condition": t[0],
            "Treatment": t[1]
        } for t in TREATMENTS]
        st.table(treatment_df)
    
    # Search All Page
    elif page == "Search All":
        st.header("🔍 Search All Conditions")
        
        search = st.text_input("Enter search term:", value=search_term)
        
        if search:
            results = []
            for category, conditions in CONDITIONS.items():
                for condition in conditions:
                    # Search in name and features
                    if (search.lower() in condition["name"].lower() or
                        any(search.lower() in f[1].lower() for f in condition["features"])):
                        results.append((category, condition))
            
            if results:
                st.success(f"Found {len(results)} matching conditions")
                for category, condition in results:
                    display_condition(condition, category)
            else:
                st.warning("No matching conditions found")
        else:
            st.info("Enter a search term to find conditions")
            
            # Show all conditions count
            total = sum(len(c) for c in CONDITIONS.values())
            st.markdown(f"**Total conditions in database: {total}**")
            
            # Show all conditions as a list
            for category, conditions in CONDITIONS.items():
                st.markdown(f"**{category.title()} ({len(conditions)} conditions)**")
                for condition in conditions:
                    st.markdown(f"- {condition['name']}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #6b7280;">
        <p>Neonatal Dermatology Study Guide - Based on Gomella's Neonatology, Chapter 80</p>
        <p style="font-size: 0.875rem;">21 Clinical Photographs • All Information Preserved</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
