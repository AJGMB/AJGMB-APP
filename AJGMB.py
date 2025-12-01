
import os
import streamlit as st
import yagmail
import random
from fpdf import FPDF
import io
import tempfile
from pathlib import Path


# Configuration - use env var
YOUR_EMAIL = st.secrets["AJGMB_EMAIL"]
YOUR_APP_PASSWORD = st.secrets["AJGMB_APP_PASSWORD"]

# Initialize email client only if credentials are provided
yag = None
if YOUR_EMAIL and YOUR_APP_PASSWORD:
    try:
        yag = yagmail.SMTP(YOUR_EMAIL, YOUR_APP_PASSWORD)
    except Exception as e:
        st.warning(f"Unable to initialize email client: {e}")


# Session state defaults
st.set_page_config(page_title="AJGMB Application", layout="centered")
st.session_state.setdefault("agreed_terms", False)
st.session_state.setdefault("otp", None)
st.session_state.setdefault("otp_verified", False)


# Terms page
if not st.session_state.agreed_terms:
    st.title("📄 Terms and Conditions for AYANFE JESU GOSPEL MUSIC BAND Application")
    st.markdown("""
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
    st.title("🟦 AYANFE JESU GOSPEL MUSIC BAND Application Form")

    with st.form("application_form"):
        st.subheader("📌 Personal Information")
        fullname = st.text_input("Full Name *")
        email = st.text_input("Email Address *")
        
        # OTP UNDER EMAIL 
        st.subheader("📩 Email Verification (OTP)")
        if st.form_submit_button("Send OTP"):
            if not email:
                st.error("❗ Please enter your email before requesting an OTP.")
            else:
                st.session_state.otp = str(random.randint(100000, 999999))
                subject = "Your OTP Verification Code"
                message = f"Your OTP code is: {st.session_state.otp}"
                if yag:
                    try:
                        yag.send(email, subject, message)
                        st.success(f"OTP sent to {email}. Check your inbox.")
                    except Exception as e:
                        st.error(f"Failed to send OTP email: {e}")
                else:
                    st.info("Email client not configured. Set AJGMB_EMAIL and AJGMB_APP_PASSWORD environment variables to enable sending emails.")

        otp_input = st.text_input("Enter OTP")
        if st.form_submit_button("Verify OTP"):
            if otp_input == st.session_state.otp:
                st.session_state.otp_verified = True
                st.success("✅ OTP Verified Successfully!")
            else:
                st.session_state.otp_verified = False
                st.error("❌ Invalid OTP. Please try again.")

        col1, col2 = st.columns(2)
        with col1:
            phone = st.text_input("Phone Number *")
        with col2:
            age = st.number_input("Your Age *", min_value=16, max_value=100, step=1)
        st.subheader("📌 Location Details")
        state = st.text_input("State *")
        address = st.text_area("Residential Address *")
        st.subheader("📌 Music Experience & Education")
        experience = st.number_input("Years of Experience in Music Industry *", min_value=0, step=1)
        education = st.selectbox("Educational Level *", ["Primary", "Secondary", "Diploma", "Degree", "Masters", "None"], index=3)
        st.subheader("📌 Musical Instruments")
        primary_instrument = st.selectbox("Primary Instrument *", ["Keyboard", "Guitar", "Drums", "Vocals", "Bass", "Other"], index=3)
        secondary_instrument = st.multiselect("Secondary Instruments (if any)", ["Keyboard", "Guitar", "Drums", "Vocals", "Bass", "Other"])
        st.subheader("📌 Additional Information")
        position = st.selectbox("Which position are you applying for? *", ["Talking Drummer", "Drumsetter", "Backup Singer", "Keyboardist", "Guitarist", "Cameraman", "Engineer", "Manager", "Other"])
        bio = st.text_area("Briefly describe yourself (Optional)")
        st.subheader("📌 Upload Portrait / Image")
        image_file = st.file_uploader("Upload Your Portrait (JPG/PNG)", type=["png", "jpg", "jpeg"])
        st.subheader("📌 Upload Band Logo")
        band_logo_file = st.file_uploader("Upload Band Logo (JPG/PNG)", type=["png", "jpg", "jpeg"])
        agree = st.checkbox("I agree to the terms and conditions *")
        submit_form = st.form_submit_button("Submit Application")

    # Helpful note for operator
    if not (YOUR_EMAIL and YOUR_APP_PASSWORD):
        st.info("Email is not configured. Set AJGMB_EMAIL and AJGMB_APP_PASSWORD environment variables to enable sending emails.")



import os
import streamlit as st
import yagmail
import random
import datetime
from fpdf import FPDF


# PAGE CONFIG
st.set_page_config(page_title="AJGMB Application", layout="centered")


# STYLING
st.markdown("""
<style>
    .stApp { background-color: #ffffff !important; }
    body, label, span, div { color: #000 !important; font-size: 13px !important; }
    input[type="text"], input[type="email"], input[type="number"], textarea {
        background-color: #ffffff !important; color: #000 !important;
        border: 1px solid #d0d0d0 !important; border-radius: 8px !important; padding: 7px !important;
        box-shadow: 0px 0px 4px rgba(0,0,0,0.05) !important;
    }
    textarea { background-color: white !important; }
    div[data-baseweb="select"] > div { background-color: white !important; color: black !important;
        border-radius: 8px !important; border: 1px solid #d0d0d0 !important; box-shadow: 0px 0px 4px rgba(0,0,0,0.05) !important; }
    div[data-baseweb="select"] * { color: black !important; }
    .css-1rhbuit-multiValue { background-color: #eaf1ff !important; color: black !important; }
    .css-12jo7m5 { color: black !important; }
    .stFileUploader { background-color: white !important; padding: 10px !important;
        border: 1px solid #d0d0d0 !important; border-radius: 10px !important; }
    .stButton>button { background-color: #ffffff !important; border: 1px solid #1b75ff !important;
        color: #000 !important; padding: 7px 20px !important; border-radius: 8px !important; transition: 0.2s; }
    .stButton>button:hover { background-color: #d8e6ff !important; border-color: #1b75ff !important; }
    .stButton>button:active { background-color: #1b75ff !important; color: white !important; }
    input[type="checkbox"] { accent-color: #1b75ff !important; }
    .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; max-width: 700px !important; }
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
                   Updated Streamlit app with PDF and email features

