import streamlit as st
from src.user_interface.data_handler import get_all_data_sorted, get_filtered_data, get_all_seat_numbers

def show():
    st.header("View Student Data")
    
    # Filter options
    filter_option = st.radio("View Options", ["All Students", "Filter by Seat Number"])
    
    if filter_option == "Filter by Seat Number":
        seat_nos, error = get_all_seat_numbers()
        
        if error:
            st.error(error)
            return
        
        selected_seat = str(st.selectbox("Select Seat Number", seat_nos))
        
        if st.button("Filter Data"):
            df, error = get_filtered_data(selected_seat)
            
            if error:
                st.error(error)
            else:
                st.success(f"Showing data for Seat No: {selected_seat}")
                # Ensure Arrow compatibility for date columns
                for col in ['START DATE', 'END DATE', 'PAYMENT RE. DATE']:
                    if col in df.columns:
                        df[col] = df[col].astype(str)
                df['SEAT NO.'] = df['SEAT NO.'].astype(str)
                st.dataframe(df, width='stretch', hide_index=True)
    else:
        # Show all data sorted by end date
        df, error = get_all_data_sorted()
        
        if error:
            st.error(error)
        else:
            st.info(f"Showing all student records (sorted by End Date) - Total: {len(df)} students")
            # Ensure Arrow compatibility for date columns
            for col in ['START DATE', 'END DATE', 'PAYMENT RE. DATE']:
                if col in df.columns:
                    df[col] = df[col].astype(str)
            df['SEAT NO.'] = df['SEAT NO.'].astype(str)
            st.dataframe(df, width='stretch', hide_index=True)
            
            # Add download button
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Data as CSV",
                data=csv,
                file_name="library_data.csv",
                mime="text/csv",
                width='stretch'
            )