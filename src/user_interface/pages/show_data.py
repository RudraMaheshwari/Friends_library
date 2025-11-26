import streamlit as st
from src.user_interface.data_handler import get_all_data_sorted, get_all_data_sorted_by_seat, get_filtered_data, get_all_seat_numbers

def show():
    st.header("View Student Data")
    
    # Filter and sort options
    filter_option = st.radio("View Options", ["All Students", "Filter by Seat Number"])
    
    # Add sorting option for All Students view
    sort_by = None
    if filter_option == "All Students":
        sort_by = st.radio("Sort By", ["End Date", "Seat Number"])
    
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
        # Show all data sorted by selected option
        if sort_by == "Seat Number":
            df, error = get_all_data_sorted_by_seat()
            sort_label = "Seat Number"
        else:
            df, error = get_all_data_sorted()
            sort_label = "End Date"
        
        if error:
            st.error(error)
        else:
            st.info(f"Showing all student records (sorted by {sort_label}) - Total: {len(df)} students")
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