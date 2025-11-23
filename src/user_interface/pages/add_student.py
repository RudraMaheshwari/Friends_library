import streamlit as st
from src.user_interface.data_handler import add_student_to_excel

def show():
    st.header("Add New Student")
    
    with st.form("add_student_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name*", placeholder="Enter student name")
            seat_no = st.text_input("Seat No.*", placeholder="Enter seat number")
            mobile_no = st.text_input("Mobile No.*", placeholder="Enter mobile number")
            starting_date = st.date_input("Starting Date*")
            end_date = st.date_input("End Date*")
            payment_receive_date = st.date_input("Payment Receive Date*")
        
        with col2:
            received_amount = st.number_input("Received Amount*", min_value=0.0, step=100.0)
            due_amount = st.number_input("Due Amount*", min_value=0.0, step=100.0)
            total_amount = st.number_input("Total Amount*", min_value=0.0, step=100.0)
            pay_mode = st.selectbox("Payment Mode*", ["Cash", "Online", "Card", "UPI", "Other"])
            time_type = st.selectbox("Time Type*", ["Full Day", "Morning", "Evening", "Night"])
        
        submit_button = st.form_submit_button("Add Student", width='stretch')
        
        if submit_button:
            # Validation
            if not name or not seat_no or not mobile_no:
                st.error("Please fill all required fields marked with *")
            else:
                student_data = {
                    'name': name,
                    'seat_no': seat_no,
                    'mobile_no': mobile_no,
                    'starting_date': str(starting_date),
                    'end_date': str(end_date),
                    'payment_receive_date': str(payment_receive_date),
                    'received_amount': received_amount,
                    'due_amount': due_amount,
                    'total_amount': total_amount,
                    'pay_mode': pay_mode,
                    'time_type': time_type
                }
                
                success, message = add_student_to_excel(student_data)
                
                if success:
                    st.success(message)
                    st.balloons()
                else:
                    st.error(message)