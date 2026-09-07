from storage.record_history import get_patient_record_history
from storage.file_storage import load_users
from utils.file_utils import get_user_id_by_name
import streamlit as st


# Streamlit page to view any patients records
def view_records():
    st.header("View Patient Records")
    users = load_users()
    patient_names = [user['name'] for user in users.values() if user['role'] == 'patient']

    patient_name = st.selectbox("Patient Name", patient_names, index=None, placeholder="Select a patient")
    patient_id = get_user_id_by_name(patient_name)

    if st.button("Get Records") and patient_id:
        records = get_patient_record_history(patient_id)
        if records:
            for i, record in enumerate(records):

                status = record.get('status', 'unknown')
                # Display status based on transaction validation
                status_icon = "PENDING" if status == 'pending' else "CONFIRMED" if status == 'confirmed' else "UNKNOWN"
                st.write(f"Record {i+1}: {status_icon}")

                def show_field(label, value):
                    if value not in (None, '', [], {}):
                        st.write(f"{label}: {value}")

                show_field("Hospital", record.get('hospital_id', ''))
                show_field("Doctor", record.get('doctor_name', ''))
                show_field("Patient", record.get('patient_name', ''))
                show_field("Insurance", record.get('insurance_id', ''))
                show_field("Record ID", record.get('record_id', ''))
                show_field("Type", record.get('record_type', ''))
                show_field("Operation", record.get('operation', '').capitalize())
                show_field("Prescription", record.get('prescription', ''))
                show_field("Amount", record.get('amount', ''))
                show_field("Timestamp", record.get('timestamp', ''))

                if status == 'confirmed' and record.get('block_number', '') not in (None, '', [], {}):
                    st.write(f"Block: {record.get('block_number')}")
                st.write("---")
        else:
            st.warning("No records found")
