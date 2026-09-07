import streamlit as st
import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

frontend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, frontend_dir)

from tabs.validator import validator_tab
from tabs.staking import staking_page
from tabs.view_records import view_records
from tabs.share_record import share_record_tab
from tabs.update_record import update_record_tab
from tabs.add_record import add_record
from tabs.register_user import register_user
from tabs.dashboard import show_dashboard
from tabs.access_log import access_log_tab



def main():
    st.title("Medical Blockchain System")
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", [
        "Dashboard", "Register User", "Add Record", "Update Record", "Share Record", "View Records", "Staking", "Validator", "Access Log"], index=0)
    if page == "Dashboard":
        show_dashboard()
    elif page == "Register User":
        register_user()
    elif page == "Add Record":
        add_record()
    elif page == "Update Record":
        update_record_tab()
    elif page == "Share Record":
        share_record_tab()
    elif page == "View Records":
        view_records()
    elif page == "Staking":
        staking_page()
    elif page == "Validator":
        validator_tab()
    elif page == "Access Log":
        access_log_tab()


if __name__ == "__main__":
    main()
