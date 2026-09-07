from crypto.digital_signature import sign_data
from consensus.staking import stake_tokens, load_stakes
from storage.file_storage import load_users
from utils.file_utils import get_user_id_by_name
import streamlit as st
from cryptography.hazmat.primitives import serialization


def get_user_name_by_id(user_id):
    users = load_users()
    return users.get(user_id, {}).get('name', user_id)


def staking_page():
    st.header("Token Staking")
    users = load_users()
    doctor_names = [user['name']
                    for user in users.values() if user['role'] == 'doctor']
    doctor_name = st.selectbox(
        "Doctor Name", doctor_names, index=None, placeholder="Select a doctor")
    doctor_id = get_user_id_by_name(doctor_name) if doctor_name else None
    amount = st.number_input("Amount", min_value=1, step=1)
    private_key_pem = st.text_area(
        "Paste your private key (PEM format) to sign this action:")
    if st.button("Stake Tokens"):
        if doctor_id and amount and private_key_pem:
            try:
                private_key = serialization.load_pem_private_key(
                    private_key_pem.encode(), password=None)
            except Exception as e:
                st.error(f"Invalid private key: {e}")
                return
            stake_data = {'doctor_id': doctor_id,
                          'amount': amount, 'action': 'stake'}
            signature = sign_data(private_key, stake_data)
            success, message = stake_tokens(doctor_id, amount, signature)
            if success:
                st.success(message)
            else:
                st.error(message)
        else:
            st.error(
                "Please select a doctor, enter an amount, and paste your private key.")
    st.subheader("Current Stakes")
    stakes = load_stakes()
    for doctor_id, stake_info in stakes.items():
        doctor_name = get_user_name_by_id(doctor_id)
        st.write(f"{doctor_name}: {stake_info.get('amount', 0)} tokens")
