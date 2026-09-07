from consensus.staking import load_stakes
from storage.file_storage import load_blockchain
import streamlit as st
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

# Dashboard Page
def show_dashboard():
    st.header("Dashboard")
    try:
        blockchain = load_blockchain()
        stakes = load_stakes()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Blocks", len(blockchain))
        with col2:
            st.metric("Active Validators", len(stakes))
    except Exception as e:
        st.error(f"Error: {e}")
