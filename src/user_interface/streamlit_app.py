import streamlit as st
from src.user_interface.pages import add_student, update_fee, generate_fee_message, show_data, delete_data

def main():
    st.set_page_config(
        page_title="Library Management System",
        page_icon="📚",
        layout="wide"
    )
    
    st.title("📚 Friends Library Management System")
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select Operation",
        ["Home", "Add Student", "Update Fee", "Generate Fee Message", "Show Data", "Delete Student"]
    )
    
    if page == "Home":
        show_home()
    elif page == "Add Student":
        add_student.show()
    elif page == "Update Fee":
        update_fee.show()
    elif page == "Generate Fee Message":
        generate_fee_message.show()
    elif page == "Show Data":
        show_data.show()
    elif page == "Delete Student":
        delete_data.show()

def show_home():
    st.header("Welcome to Friends Library Management System")
    st.write("Contact: +91 9636117578")
    
    st.markdown("""
    ### Available Operations:
    - **Add Student**: Register new students to the library
    - **Update Fee**: Update payment and fee details for existing students
    - **Generate Fee Message**: Generate fee notification messages for students
    - **Show Data**: View all student records (sorted by end date)
    - **Delete Student**: Remove student records from the system
    
    Please select an operation from the sidebar to get started.
    """)