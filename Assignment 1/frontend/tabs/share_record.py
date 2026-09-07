from crypto.digital_signature import sign_data
from storage.medical_records import share_medical_record
from storage.record_history import get_patient_record_history
from storage.file_storage import load_users
from utils.file_utils import get_user_id_by_name
import streamlit as st
from cryptography.hazmat.primitives import serialization


def share_record_tab():
    st.header("Share Medical Record")
    users = load_users()
    doctor_names = [user['name']
                    for user in users.values() if user['role'] == 'doctor']
    doctor_name = st.selectbox(
        "Your Doctor Name", doctor_names, index=None, placeholder="Select your doctor name")
    doctor_id = get_user_id_by_name(doctor_name) if doctor_name else None
    all_records = []
    for user in users.values():
        if user['role'] == 'patient':
            patient_id = user['user_id']
            patient_records = get_patient_record_history(patient_id)
            for rec in patient_records:
                if rec.get('doctor_id') == doctor_id:
                    all_records.append(rec)
    record_options = [
        f"{rec['record_id']} (Patient: {rec.get('patient_name', '')})" for rec in all_records]
    record_map = {
        f"{rec['record_id']} (Patient: {rec.get('patient_name', '')})": rec for rec in all_records}
    record_choice = st.selectbox("Record ID to Share", record_options,
                                 index=None, placeholder="Select a record") if record_options else None
    selected_record = record_map[record_choice] if record_choice else None
    patient_name = selected_record['patient_name'] if selected_record else ''
    patient_id = selected_record['patient_id'] if selected_record else ''
    share_with_doctor_name = st.selectbox("Share With Doctor", [
                                          n for n in doctor_names if n != doctor_name], index=None, placeholder="Select a doctor to share with")
    share_with_doctor_id = get_user_id_by_name(
        share_with_doctor_name) if share_with_doctor_name else None
    private_key_pem = st.text_area(
        "Paste your private key (PEM format) to sign this share:")
    if st.button("Share Record"):
        if doctor_id and patient_id and selected_record and share_with_doctor_id:
            record_data = {
                'hospital_id': '',
                'doctor_id': doctor_id,
                'doctor_name': doctor_name,
                'patient_id': patient_id,
                'patient_name': patient_name,
                'insurance_id': '',
                'record_id': selected_record['record_id'],
                'record_type': selected_record.get('record_type', ''),
                'operation': 'share',
                'prescription': f"SHARE_WITH:{share_with_doctor_id}",
                'amount': 0.0
            }
            if not private_key_pem:
                st.error("You must paste your private key to sign the share.")
            else:
                try:
                    private_key = serialization.load_pem_private_key(
                        private_key_pem.encode(), password=None)
                except Exception as e:
                    st.error(f"Invalid private key: {e}")
                    return
                tx_data = {
                    'doctor_id': doctor_id,
                    'patient_id': patient_id,
                    'record_data': record_data
                }
                signature = sign_data(private_key, tx_data)
                success, message = share_medical_record(
                    doctor_id, patient_id, record_data, signature)
                if success:
                    st.success("Record share submitted.")
                else:
                    st.error(message)
        else:
            st.error("Please fill all fields.")
