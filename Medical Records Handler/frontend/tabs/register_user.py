from models.user import Patient, Doctor, Administrator
from storage.access_logger import log_access
from storage.file_storage import load_users, save_users
import streamlit as st
from cryptography.hazmat.primitives import serialization


def register_user():
    st.header("Register User")
    user_type = st.selectbox(
        "User Type", ["Patient", "Doctor", "Administrator"])
    name = st.text_input("Name")
    if user_type == "Doctor":
        hospital_id = st.text_input("Hospital ID")
    else:
        hospital_id = ""
    if st.button("Register"):
        if name:
            users = load_users()
            if user_type == "Patient":
                user = Patient(name)
            elif user_type == "Doctor":
                user = Doctor(name, hospital_id)
            else:
                user = Administrator(name, hospital_id)
            user_dict, private_key = user.to_dict_with_keypair()
            users[user.user_id] = user_dict
            save_users(users)
            
            # Log user registration
            log_access(user.user_id, None, "register_user", success=True, details=f"User {name} ({user_type}) registered successfully")
            
            st.success(f"User {name} registered with ID: {user.user_id}")
            st.info(
                "Below is your private key. Save it securely. It will not be shown again!")
            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode()
            st.code(private_pem, language="text")
        else:
            st.error("Please enter a name.")
