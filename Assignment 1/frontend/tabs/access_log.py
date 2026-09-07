import streamlit as st
import pandas as pd
from storage.access_logger import get_access_logs


def parse_access_log():
    log_entries = get_access_logs(limit=1000)  # Get all logs
    if not log_entries:
        return pd.DataFrame()
    
    return pd.DataFrame(log_entries)


def format_status(status):
    if status == "SUCCESS":
        return f"✅ {status}"
    elif status == "FAILED":
        return f"❌ {status}"
    else:
        return status

def access_log_tab():
    st.header("Access Log")
    st.write("View all system access attempts and their outcomes")
    
    df = parse_access_log()
    
    if df.empty:
        st.warning("No access log entries found.")
        return
    
    # Display the data table
    df['Date'] = df['timestamp'].str[:10]
    df['Time'] = df['timestamp'].str[11:19]
    df['User ID'] = df['user_id']
    df['Action'] = df['operation']
    df['Patient ID'] = df['patient_id']
    df['Status'] = df['success'].apply(lambda x: "SUCCESS" if x else "FAILED")
    df['Message'] = df['details']
    display_df = df[['Date', 'Time', 'User ID', 'Action', 'Patient ID', 'Status', 'Message']].copy()
    
    # Format status column for better display
    display_df['Status'] = display_df['Status'].apply(format_status)
    
    # Display the table
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Date": st.column_config.DateColumn("Date"),
            "Time": st.column_config.TextColumn("Time"),
            "User ID": st.column_config.TextColumn("User ID"),
            "Action": st.column_config.TextColumn("Action"),
            "Patient ID": st.column_config.TextColumn("Patient ID"),
            "Status": st.column_config.TextColumn("Status"),
            "Message": st.column_config.TextColumn("Message")
        }
    )

    st.write("Columns in access log:", df.columns.tolist())