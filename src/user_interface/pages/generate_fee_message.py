import streamlit as st
from src.user_interface.data_handler import get_all_seat_numbers, generate_fee_message_text, get_student_details

def show():
    st.header("Generate Fee Message")
    
    # Get all seat numbers
    seat_nos, error = get_all_seat_numbers()
    
    if error:
        st.error(error)
        return
    
    # Select seat number
    selected_seat = str(st.selectbox("Select Seat Number", seat_nos))
    
    if st.button("Generate Message", width='stretch'):
        details, error = get_student_details(selected_seat)
        if error:
            st.error(error)
        else:
            st.subheader(f"Student: {details['name']}")
            st.write(f"Seat No.: {details['seat_no']}")
            st.write(f"Mobile No.: {details['mobile_no']}")
            st.write(f"Received Amount: {details['received_amount']}")
            st.write(f"Due Amount: {details['due_amount']}")
            st.write(f"Total Amount: {details['total_amount']}")
            st.write(f"Payment Receive Date: {details['payment_receive_date']}")
            st.write(f"Start Date: {details['start_date']}")
            st.write(f"End Date: {details['end_date']}")
            st.write(f"Pay Mode: {details['pay_mode']}")
            st.write(f"Time Type: {details['time_type']}")
            message, error = generate_fee_message_text(selected_seat)
            if error:
                st.error(error)
            else:
                st.success("Message generated successfully!")
                st.text_area("Fee Message", message, height=300)
                st.code(message, language=None)
                st.info("You can copy the message from the code box above")