import streamlit as st
from src.user_interface.data_handler import get_all_seat_numbers, generate_reminder_message_text, get_student_details

def show():
    st.header("Generate Reminder Message")
    
    # Get all seat numbers
    seat_nos, error = get_all_seat_numbers()
    
    if error:
        st.error(error)
        return
    
    # Select seat number
    selected_seat = str(st.selectbox("Select Seat Number", seat_nos))
    
    if st.button("Generate Reminder", width='stretch'):
        details, error = get_student_details(selected_seat)
        if error:
            st.error(error)
        else:
            st.subheader(f"Student: {details['name']}")
            st.write(f"Seat No.: {details['seat_no']}")
            st.write(f"Mobile No.: {details['mobile_no']}")
            st.write(f"End Date: {details['end_date']}")
            st.write(f"Due Amount: ₹{details['due_amount']}")
            
            st.divider()
            
            message, error = generate_reminder_message_text(selected_seat)
            if error:
                st.error(error)
            else:
                st.success("Reminder message generated successfully!")
                st.text_area("Reminder Message", message, height=350)
                st.code(message, language=None)
                st.info("You can copy the message from the code box above")
