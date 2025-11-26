import streamlit as st
from src.user_interface.data_handler import get_all_seat_numbers, get_student_details, update_fee_details

def show():
    st.header("Update Fee Details")
    
    # Get all seat numbers
    seat_nos, error = get_all_seat_numbers()
    
    if error:
        st.error(error)
        return
    
    # Select seat number
    selected_seat = str(st.selectbox("Select Seat Number", seat_nos))
    
    if st.button("Load Student Details"):
        details, error = get_student_details(selected_seat)
        
        if error:
            st.error(error)
        else:
            st.session_state['student_details'] = details
    
    # Show form if details are loaded
    if 'student_details' in st.session_state:
        details = st.session_state['student_details']
        
        st.subheader(f"Student: {details['name']}")
        
        with st.form("update_fee_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                received_amount = st.number_input(
                    "Received Amount*", 
                    value=details['received_amount'],
                    min_value=0.0, 
                    step=100.0
                )
                due_amount = st.number_input(
                    "Due Amount*", 
                    value=details['due_amount'],
                    min_value=0.0, 
                    step=100.0
                )
                total_amount = st.number_input(
                    "Total Amount*", 
                    value=details['total_amount'],
                    min_value=0.0, 
                    step=100.0
                )
                pay_mode = st.selectbox(
                    "Payment Mode*", 
                    ["Cash", "Online", "Card", "UPI", "Other"],
                    index=0 if details['pay_mode'] == '' else ["Cash", "Online", "Card", "UPI", "Other"].index(details['pay_mode']) if details['pay_mode'] in ["Cash", "Online", "Card", "UPI", "Other"] else 0
                )
            
            with col2:
                from datetime import datetime
                
                # Parse dates
                payment_receive_date = st.date_input(
                    "Payment Receive Date*",
                    value=datetime.strptime(details['payment_receive_date'], '%d/%m/%Y') if details['payment_receive_date'] != 'N/A' else None
                )
                start_date = st.date_input(
                    "Start Date*",
                    value=datetime.strptime(details['start_date'], '%d/%m/%Y') if details['start_date'] != 'N/A' else None
                )
                end_date = st.date_input(
                    "End Date*",
                    value=datetime.strptime(details['end_date'], '%d/%m/%Y') if details['end_date'] != 'N/A' else None
                )
            
            submit_button = st.form_submit_button("Update Fee Details", width='stretch')
            
            if submit_button:
                fee_data = {
                    'received_amount': received_amount,
                    'due_amount': due_amount,
                    'total_amount': total_amount,
                    'payment_receive_date': payment_receive_date,
                    'pay_mode': pay_mode,
                    'start_date': start_date,
                    'end_date': end_date
                }
                
                success, message = update_fee_details(selected_seat, fee_data)
                
                if success:
                    st.success(message)
                    del st.session_state['student_details']
                    st.rerun()
                else:
                    st.error(message)