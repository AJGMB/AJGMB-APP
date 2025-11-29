import os
import streamlit as st
import yagmail
import random
from fpdf import FPDF
import io
import tempfile
from pathlib import Path

# -----------------------------
# Configuration - use env vars
# -----------------------------
YOUR_EMAIL = st.secrets["AJGMB_EMAIL"]
YOUR_APP_PASSWORD = st.secrets["AJGMB_APP_PASSWORD"]

# Initialize email client only if credentials are provided
yag = None
if YOUR_EMAIL and YOUR_APP_PASSWORD:
    try:
        yag = yagmail.SMTP(YOUR_EMAIL, YOUR_APP_PASSWORD)
    except Exception as e:
        st.warning(f"Unable to initialize email client: {e}")

# -----------------------------
# Session state defaults
# -----------------------------
st.set_page_config(page_title="AJGMB Application", layout="centered")
st.session_state.setdefault("agreed_terms", False)
st.session_state.setdefault("otp", None)
st.session_state.setdefault("otp_verified", False)

# -----------------------------
# Terms page
# -----------------------------
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
        
        # ---------------- OTP UNDER EMAIL ----------------
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


