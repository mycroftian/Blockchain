
from storage.mining import mine_pending_transactions
from storage.file_storage import load_users
import streamlit as st
from cryptography.hazmat.primitives import serialization


def validator_tab():
    st.header("Validator: Mine Pending Transactions")
    users = load_users()
    doctor_users = [(uid, u['name'])
                    for uid, u in users.items() if u['role'] == 'doctor']
    if not doctor_users:
        st.warning("No doctors registered.")
        return
    doctor_names = [u[1] for u in doctor_users]
    doctor_name = st.selectbox(
        "Validator (Doctor) Name", doctor_names, index=None, placeholder="Select a validator")
    doctor_id = None
    if doctor_name:
        for uid, name in doctor_users:
            if name == doctor_name:
                doctor_id = uid
                break
    if not doctor_id:
        st.warning("Please select a validator.")
        return
    private_key_pem = st.text_area("Paste your private key (PEM format):")
    if st.button("Mine Oldest 3 Pending Transactions"):
        if not private_key_pem:
            st.error("You must paste your private key.")
            return
        try:
            private_key = serialization.load_pem_private_key(
                private_key_pem.encode(), password=None)
        except Exception as e:
            st.error(f"Invalid private key: {e}")
            return
        success, message = mine_pending_transactions(doctor_id, private_key)
        if success:
            st.success(message)
        else:
            st.error(message)
