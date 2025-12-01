import os
import streamlit as st
import yagmail
import random
import datetime
from fpdf import FPDF


st.markdown("""
<style>

    /* GLOBAL FONT SIZE REDUCTION FOR MOBILE LOOK */
    html, body, [class*="css"]  {
        font-size: 10px !important;   /* Smaller clean text */
    }

    /* SMALLER INPUT LABELS */
    label, .stTextInput label, .stSelectbox label {
        font-size: 10px !important;
        font-weight: 450 !important;
    }

    /* SMALLER BUTTONS */
    .stButton>button {
        font-size: 10px !important;
        padding: 5px 12px !important;
        border-radius: 5px !important;
    }

    /* SMALLER SELECT BOX TEXT */
    .stSelectbox div, .stSelectbox span, .stSelectbox p {
        font-size: 10px !important;
    }

    /* REDUCE HEADER SIZES */
    h1 { font-size: 20px !important; }
    h2 { font-size: 16px !important; }
    h3 { font-size: 14px !important; }

</style>
""", unsafe_allow_html=True)


# PAGE CONFIG
st.set_page_config(page_title="AJGMB Application", layout="centered")


# STYLING
st.markdown("""
<style>

    /* WHOLE APP BACKGROUND */
    .stApp {
        background-color: #000000 !important;
        color: white !important;
    }

    /* ALL TEXT */
    .stMarkdown, p, label, span, div, h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }

    /* INPUT FIELDS (text, number, email, date, etc.) */
    .stTextInput input, .stNumberInput input, .stDateInput input {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 1px solid #444444 !important;
    }

    /* TEXTAREA */
    textarea {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 1px solid #444444 !important;
    }

    /* SELECTBOX & MULTISELECT (closed box) */
    div[data-baseweb="select"] > div {
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 1px solid #444444 !important;
    }

    /* SELECTED TEXT */
    div[data-baseweb="select"] span {
        color: #ffffff !important;
    }

    /* DROPDOWN MENU BACKGROUND */
    ul[role="listbox"] {
        background-color: #000000 !important;
    }

    /* DROPDOWN OPTIONS */
    ul[role="listbox"] li {
        color: #ffffff !important;
    }

    /* OPTION HOVER */
    ul[role="listbox"] li:hover {
        background-color: #222222 !important;
        color: #ffffff !important;
    }

/* 
.stButton>button {
    background-color: #000000;  /* black background */
    color: #ffffff;             /* white text */
    border: 1px solid #ffffff;  /* optional white border */
}
</style>
""", unsafe_allow_html=True)


# EMAIL CONFIG
YOUR_EMAIL = st.secrets["AJGMB_EMAIL"]
YOUR_APP_PASSWORD = st.secrets["AJGMB_APP_PASSWORD"]

yag = None
if YOUR_EMAIL and YOUR_APP_PASSWORD:
    try:
        yag = yagmail.SMTP(YOUR_EMAIL, YOUR_APP_PASSWORD)
    except Exception as e:
        st.warning(f"Email setup failed: {e}")


# SESSION STATE
st.session_state.setdefault("agreed_terms", False)
st.session_state.setdefault("otp", None)
st.session_state.setdefault("otp_verified", False)


# TERMS PAGE
if not st.session_state.agreed_terms:
    st.title("📄 Terms & Conditions – AJGMB Application")
    st.write(""" 
        **Please read and accept the terms before proceeding to the application form:**
        1. All information provided must be accurate and truthful.
        2. Applicants must be at least 16 years old.
        3. Only one application per person is allowed.
        4. The band reserves the right to accept or reject any application.
        5. Personal information and uploaded media will be used solely for recruitment purposes.
        6. Submitted files must not contain inappropriate or offensive content.
        7. By accepting, you consent to receive emails regarding your application status.
        8. Submission of an application does not guarantee a position in the band.
        9. Any false information may result in immediate disqualification.
        10. By clicking “I Accept the Terms and Conditions”, you acknowledge that you agree to all rules above.
    """)
    if st.button("I Accept the Terms and Conditions"):
        st.session_state.agreed_terms = True
        st.rerun()
else:

    # APPLICATION FORM
    logo_path = "band_logo.png"
    if os.path.exists(logo_path):
        st.markdown(f"""
        <h1>
        <img src="{logo_path}" width="60" style="vertical-align: middle; margin-right:10px;"/>
        AYANFE JESU GOSPEL MUSIC BAND Application Form
        </h1>
        """, unsafe_allow_html=True)
    else:
        st.title("🟦 AYANFE JESU GOSPEL MUSIC BAND Application Form")

    with st.form("app_form"):
        st.subheader("📌 Personal Information")
        fullname = st.text_input("Full Name *")
        email = st.text_input("Email Address *")

        st.subheader("📩 Email Verification (OTP)")
        if st.form_submit_button("Send OTP"):
            if not email:
                st.warning("Enter email first.")
            else:
                st.session_state.otp = str(random.randint(100000, 999999))
                if yag:
                    try:
                        yag.send(email, "Your OTP Code", f"Your OTP is: {st.session_state.otp}")
                    except Exception as e:
                        st.error(f"Failed to send OTP: {e}")
                st.success("OTP sent successfully!")

        otp_entered = st.text_input("Enter OTP")
        if st.form_submit_button("Verify OTP"):
            if otp_entered == st.session_state.otp:
                st.session_state.otp_verified = True
                st.success("OTP Verified!")
            else:
                st.error("Incorrect OTP")

        col1, col2 = st.columns(2)
        phone = col1.text_input("Phone Number *")
        age = col2.number_input("Your Age *", min_value=16, max_value=100)

        st.subheader("📌 Location Details")
        state = st.text_input("State *")
        address = st.text_area("Residential Address *")

        st.subheader("📌 Music Experience & Education")
        experience = st.number_input("Years of Experience *", min_value=0)
        education = st.selectbox("Educational Level *",
                                 ["Primary", "Secondary", "Diploma", "Degree", "Masters", "None"])

        st.subheader("📌 Musical Instruments")
        primary = st.selectbox("Primary Instrument *",
                               ["Keyboard", "Guitar", "Drums", "Vocals", "Bass", "Other"])
        secondary = st.multiselect("Secondary Instruments (Optional)",
                                  ["Keyboard", "Guitar", "Drums", "Vocals", "Bass", "Other"])

        st.subheader("📌 Additional Information")
        position = st.selectbox("Position Applying For *",
                                ["Talking Drummer", "Drumsetter", "Backup Singer",
                                 "Keyboardist", "Guitarist", "Cameraman", "Engineer",
                                 "Manager", "Other"])
        bio = st.text_area("Brief Description (Optional)")

        st.subheader("📌 Upload Portrait / Image")
        image_file = st.file_uploader("Upload Your Portrait", type=["png", "jpg", "jpeg"])

        agree = st.checkbox("I agree to the terms and conditions *")
        submit = st.form_submit_button("Submit Application")

    
    # AFTER SUBMIT
    if submit:
        if not agree:
            st.error("You must agree to the terms.")
        elif not st.session_state.otp_verified:
            st.error("Verify OTP first.")
        else:
            st.success("🎉 Your form has been submitted successfully!")

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

            # Save portrait if uploaded
            portrait_file_path = None
            if image_file is not None:
                ext = os.path.splitext(image_file.name)[1]
                portrait_file_path = f"portrait_{fullname.replace(' ','_')}_{timestamp}{ext}"
                with open(portrait_file_path, "wb") as f:
                    f.write(image_file.getbuffer())

            # Generate PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "AJGMB Application", ln=True, align="C")
            pdf.ln(10)

            if portrait_file_path:
                pdf.image(portrait_file_path, x=10, y=30, w=40)
                pdf.ln(45)

            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 8, f"Full Name: {fullname}", ln=True)
            pdf.cell(0, 8, f"Email: {email}", ln=True)
            pdf.cell(0, 8, f"Phone: {phone}", ln=True)
            pdf.cell(0, 8, f"Age: {age}", ln=True)
            pdf.cell(0, 8, f"State: {state}", ln=True)
            pdf.multi_cell(0, 8, f"Address: {address}")
            pdf.cell(0, 8, f"Experience: {experience} years", ln=True)
            pdf.cell(0, 8, f"Education: {education}", ln=True)
            pdf.cell(0, 8, f"Primary Instrument: {primary}", ln=True)
            pdf.cell(0, 8, f"Secondary Instruments: {', '.join(secondary)}", ln=True)
            pdf.cell(0, 8, f"Position Applied: {position}", ln=True)
            pdf.multi_cell(0, 8, f"Bio: {bio}")

            pdf_file_path = f"AJGMB_Application_{fullname.replace(' ','_')}_{timestamp}.pdf"
            pdf.output(pdf_file_path)

        
            # Send email to applicant with PDF attached
            if yag:
                try:
                    applicant_subject = "AJGMB Application Submitted Successfully"
                    applicant_body = f"""
🎉 Hello {fullname},

Your application has been successfully submitted to AYANFE JESU GOSPEL MUSIC BAND!

We have received your details and will review your application shortly.

Please find attached a copy of your submitted application (PDF).

Thank you for applying.

Best regards,
AYANFE JESU GOSPEL MUSIC BAND
                    """
                    yag.send(
                        to=email,
                        subject=applicant_subject,
                        contents=applicant_body,
                        attachments=[pdf_file_path]
                    )
                    st.success("✅ Confirmation email sent to applicant with PDF attached!")
                except Exception as e:
                    st.error(f"Failed to send email to applicant: {e}")

            
            # Send email to admin with PDF attached
            if yag:
                try:
                    yag.send(
                        to=YOUR_EMAIL,
                        subject="New AJGMB Application Submitted",
                        contents=f"New application received from {fullname}. PDF attached.",
                        attachments=[pdf_file_path]
                    )
                    st.info("✅ Admin notified via email with PDF attached!")
                except Exception as e:
                    st.error(f"Failed to send email to admin: {e}")
