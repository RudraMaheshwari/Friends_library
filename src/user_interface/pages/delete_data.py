import streamlit as st
from src.user_interface.data_handler import get_all_student_names, delete_student_by_name

def show():
    st.header("Delete Student Data")
    
    st.warning("⚠️ Warning: This action cannot be undone!")
    
    # Get all student names
    student_names, error = get_all_student_names()
    
    if error:
        st.error(error)
        return
    
    if not student_names:
        st.info("No students found in the database.")
        return
    
    # Select student to delete
    selected_student = st.selectbox("Select Student to Delete", student_names)
    
    # Confirmation checkbox
    confirm = st.checkbox(f"I confirm that I want to delete student: {selected_student}")
    
    if st.button("Delete Student", type="primary", disabled=not confirm, width='stretch'):
        if confirm:
            success, message = delete_student_by_name(selected_student)
            
            if success:
                st.success(message)
                st.balloons()
                st.rerun()
            else:
                st.error(message)
        else:
            st.warning("Please confirm deletion by checking the checkbox above.")