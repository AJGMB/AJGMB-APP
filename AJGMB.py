import os
import streamlit as st
import yagmail
import random
import datetime
from fpdf import FPDF

# -----------------------------
# CONFIGURATION
# -----------------------------
YOUR_EMAIL = st.secrets["AJGMB_EMAIL"]
YOUR_APP_PASSWORD = st.secrets["AJGMB_APP_PASSWORD"]

# Initialize email client if credentials exist
yag = None
if YOUR_EMAIL and YOUR_APP_PASSWORD:
    try:
        yag = yagmail.SMTP(YOUR_EMAIL, YOUR_APP_PASSWORD)
    except Exception as e:
        st.warning(f"Unable to initialize email client: {e}")

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AJGMB Application", layout="centered")

# -----------------------------
# SESSION STATE
# -----------------------------
st.session_state.setdefault("agreed_terms", False)
st.session_state.setdefault("otp", None)
st.session_state.setdefault("otp_verified", False)

# -----------------------------
# STYLING
# -----------------------------
st.markdown("""
<style>
    .stApp { background-color: #ffffff !important; }
    body, label, span, div { color: #000 !important; font-size: 13px !important; }
    input[type="text"], input[type="email"], input[type="number"], textarea {
        background-color: #ffffff !important; color: #000 !important;
        border: 1px solid #d0d0d0 !important; border-radius: 8px !important; padding: 7px !important;
        box-shadow: 0px 0px 4px rgba(0,0,0,0.05) !important;
    }
    div[data-baseweb="select"] > div { background-color: white !important; color: black !important;
        border-radius: 8px !important; border: 1px solid #d0d0d0 !important; box-shadow: 0px 0px 4px rgba(0,0,0,0.05) !important; }
    .stButton>button { background-color: #ffffff !important; border: 1px solid #1b75ff !important;
        color: #000 !important; padding: 7px 20px !important; border-radius: 8px !important; }
    .stButton>button:hover { background-color: #d8e6ff !important; border-color: #1b75ff !important; }
    .stButton>button:active { background-color: #1b75ff !important; color: white !important; }
    input[type="checkbox"] { accent-color: #1b75ff !important; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# TERMS & CONDITIONS
# -----------------------------
if not st.session_state.agreed_terms:
    st.title("📄 Terms & Conditions – AJGMB Application")
    st.markdown("""
**Please read and accept the terms before proceeding:**

1. All information provided must be accurate and truthful.
2. Applicants must be at least 16 years old.
3. Only one application per person is allowed.
4. The band reserves the right to accept or reject any application.
5. Personal information and uploaded media will be used solely for recruitment purposes.
6. Submitted files must not contain inappropriate content.
7. By accepting, you consent to receive emails regarding your application.
8. Submission of an application does not guarantee a position.
9. False information may result in disqualification.
10. By clicking “I Accept the Terms and Conditions”, you agree to all rules above.
""")
    if st.button("I Accept the Terms and Conditions"):
        st.session_state.agreed_terms = True
        st.rerun()

# -----------------------------
# APPLICATION FORM
# -----------------------------
else:
    st.title("AYANFE JESU GOSPEL MUSIC BAND Application Form")

    with st.form("application_form"):
        # Personal Info
        st.subheader("📌 Personal Information")
        fullname = st.text_input("Full Name *")
        email = st.text_input("Email Address *")

        # OTP Section
        st.subheader("📩 Email Verification (OTP)")
        send_otp = st.form_submit_button("Send OTP")
        if send_otp:
            if not email:
                st.error("❗ Please enter your email first.")
            else:
                st.session_state.otp = str(random.randint(100000, 999999))
                if yag:
                    try:
                        yag.send(email, "Your OTP Code", f"Your OTP is: {st.session_state.otp}")
                        st.success(f"OTP sent to {email}")
                    except Exception as e:
                        st.error(f"Failed to send OTP: {e}")
                else:
                    st.info("Email not configured.")

        otp_input = st.text_input("Enter OTP")
        verify_otp = st.form_submit_button("Verify OTP")
        if verify_otp:
            if otp_input == st.session_state.otp:
                st.session_state.otp_verified = True
                st.success("✅ OTP Verified Successfully!")
            else:
                st.session_state.otp_verified = False
                st.error("❌ Invalid OTP")

        # Contact Info
        col1, col2 = st.columns(2)
        phone = col1.text_input("Phone Number *")
        age = col2.number_input("Your Age *", min_value=16, max_value=100)

        # Location
        st.subheader("📌 Location Details")
        state = st.text_input("State *")
        address = st.text_area("Residential Address *")

        # Music Experience & Education
        st.subheader("📌 Music Experience & Education")
        experience = st.number_input("Years of Experience in Music *", min_value=0)
        education = st.selectbox("Educational Level *", ["Primary", "Secondary", "Diploma", "Degree", "Masters", "None"])

        # Instruments
        st.subheader("📌 Musical Instruments")
        primary = st.selectbox("Primary Instrument *", ["Keyboard", "Guitar", "Drums", "Vocals", "Bass", "Other"])
        secondary = st.multiselect("Secondary Instruments (Optional)", ["Keyboard", "Guitar", "Drums", "Vocals", "Bass", "Other"])

        # Additional Info
        st.subheader("📌 Additional Information")
        position = st.selectbox("Position Applying For *", ["Talking Drummer", "Drumsetter", "Backup Singer",
                                                          "Keyboardist", "Guitarist", "Cameraman", "Engineer",
                                                          "Manager", "Other"])
        bio = st.text_area("Brief Description (Optional)")

        # Upload Files
        st.subheader("📌 Upload Portrait / Image")
        image_file = st.file_uploader("Upload Your Portrait", type=["png", "jpg", "jpeg"])

        agree = st.checkbox("I agree to the terms and conditions *")

        # Final submit
        submit = st.form_submit_button("Submit Application")

    # -----------------------------
    # AFTER SUBMIT
    # -----------------------------
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

            # Send email to applicant
            if yag:
                try:
                    yag.send(
                        to=email,
                        subject="AJGMB Application Submitted Successfully",
                        contents=f"Hello {fullname},\n\nYour application has been submitted successfully. PDF attached.",
                        attachments=[pdf_file_path]
                    )
                    st.success("✅ Confirmation email sent to applicant!")
                except Exception as e:
                    st.error(f"Failed to send email to applicant: {e}")

            # Send email to admin
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
