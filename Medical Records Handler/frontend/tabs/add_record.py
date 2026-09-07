from crypto.digital_signature import sign_data
from storage.medical_records import add_medical_record
from storage.file_storage import load_users
from utils.file_utils import get_user_id_by_name
import streamlit as st
import uuid
from datetime import datetime
from cryptography.hazmat.primitives import serialization


# Streamlit page to add a medical record
def add_record():
    st.header("Add Medical Record")
    users = load_users()

    doctor_names = [user['name'] for user in users.values() if user['role'] == 'doctor']
    patient_names = [user['name'] for user in users.values() if user['role'] == 'patient']

    doctor_name = st.selectbox("Doctor Name", doctor_names, index=None, placeholder="Select a doctor")
    doctor_id = get_user_id_by_name(doctor_name) if doctor_name else None

    patient_name = st.selectbox("Patient Name", patient_names, index=None, placeholder="Select a patient")
    patient_id = get_user_id_by_name(patient_name) if patient_name else None

    hospital_id = st.text_input("Hospital ID/Name")
    insurance_id = st.text_input("Insurance ID/Name")

    # Generate a unique record ID and store it in session state
    if 'record_id' not in st.session_state:
        st.session_state['record_id'] = str(uuid.uuid4())[:8]
    if st.button("Regenerate Record ID"):  # Button to regenerate record ID
        st.session_state['record_id'] = str(uuid.uuid4())[:8]

    record_id = st.text_input("Record ID", value=st.session_state['record_id'])
    record_type = st.selectbox("Record Type", ["Diagnosis", "Prescription", "Test Result"], index=None, placeholder="Select a record type")
    details = st.text_area("Details")
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    private_key_pem = st.text_area("Paste your private key (PEM format) to sign this record:")

    if st.button("Add Record"):
        if doctor_id and patient_id:
            record_data = {
                'hospital_id': hospital_id,
                'doctor_id': doctor_id,
                'doctor_name': doctor_name,
                'patient_id': patient_id,
                'patient_name': patient_name,
                'insurance_id': insurance_id,
                'record_id': record_id,
                'record_type': record_type,
                'operation': 'add',
                'prescription': details,
                'amount': amount,
                'timestamp': datetime.now().isoformat()
            }

            # Ensure private key is provided
            if not private_key_pem:
                st.error("You must paste your private key to sign the record.")
            else:
                try:
                    private_key = serialization.load_pem_private_key(private_key_pem.encode(), password=None)
                except Exception as e:
                    st.error(f"Invalid private key: {e}")
                    return
                
                tx_data = {
                    'doctor_id': doctor_id,
                    'patient_id': patient_id,
                    'record_data': record_data
                }

                signature = sign_data(private_key, tx_data)
                success, message = add_medical_record(doctor_id, patient_id, record_data, signature)

                if success:
                    st.success("Record added successfully!")
                else:
                    st.error(message)
        else:
            st.error("Please select both doctor and patient.")
