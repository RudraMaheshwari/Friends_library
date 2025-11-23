import pandas as pd
import os
import shutil

# Construct the absolute path to the Excel file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXCEL_FILE_PATH = os.path.join(BASE_DIR, 'LIBRARY LIST.xlsx')

def read_excel():
    """Read the Excel file and return DataFrame"""
    return pd.read_excel(EXCEL_FILE_PATH)

def save_excel(df):
    """Save DataFrame to Excel file"""
    temp_file_path = os.path.join(BASE_DIR, 'temp_LIBRARY_LIST.xlsx')
    df.to_excel(temp_file_path, index=False)
    shutil.move(temp_file_path, EXCEL_FILE_PATH)

def format_date(date_value):
    """Format date to YYYY-MM-DD string"""
    if pd.notnull(date_value):
        return pd.Timestamp(date_value).strftime('%Y-%m-%d')
    return "N/A"

def add_student_to_excel(student_data):
    """Add a new student to the Excel file"""
    try:
        df = read_excel()
        
        new_student = pd.DataFrame({
            'SEAT NO.': [student_data['seat_no']],
            'NAME': [student_data['name']],
            'MOB. NO.': [student_data['mobile_no']],
            'START DATE': [student_data['starting_date']],
            'END DATE': [student_data['end_date']],
            'PAYMENT RE. DATE': [student_data['payment_receive_date']],
            'RE . AMOUNT': [student_data['received_amount']],
            'DUE': [student_data['due_amount']],
            'TOTAL': [student_data['total_amount']],
            'PAY MODE': [student_data['pay_mode']],
            'TIME': [student_data['time_type']]
        })
        
        df = pd.concat([df, new_student], ignore_index=True)
        save_excel(df)
        return True, "Student added successfully"
    except Exception as e:
        return False, f"Error: {str(e)}"

def update_fee_details(seat_no, fee_data):
    """Update fee details for a student"""
    try:
        df = read_excel()
        df['SEAT NO.'] = df['SEAT NO.'].astype(str).str.strip()
        seat_no = seat_no.strip()
        
        if seat_no not in df['SEAT NO.'].values:
            return False, f"Seat No. {seat_no} not found"
        
        df.loc[df['SEAT NO.'] == seat_no, 'RE . AMOUNT'] = fee_data['received_amount']
        df.loc[df['SEAT NO.'] == seat_no, 'DUE'] = fee_data['due_amount']
        df.loc[df['SEAT NO.'] == seat_no, 'TOTAL'] = fee_data['total_amount']
        df.loc[df['SEAT NO.'] == seat_no, 'PAYMENT RE. DATE'] = fee_data['payment_receive_date']
        df.loc[df['SEAT NO.'] == seat_no, 'PAY MODE'] = fee_data['pay_mode']
        df.loc[df['SEAT NO.'] == seat_no, 'START DATE'] = fee_data['start_date']
        df.loc[df['SEAT NO.'] == seat_no, 'END DATE'] = fee_data['end_date']
        
        save_excel(df)
        return True, "Fee details updated successfully"
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_student_details(seat_no):
    """Get details of a specific student"""
    try:
        df = read_excel()
        df['SEAT NO.'] = df['SEAT NO.'].astype(str).str.strip()
        seat_no = seat_no.strip()
        
        student = df[df['SEAT NO.'] == seat_no]
        
        if student.empty:
            return None, "Student not found"
        
        student = student.iloc[0]
        
        # Convert date columns to datetime
        date_columns = ['PAYMENT RE. DATE', 'START DATE', 'END DATE']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        details = {
            'name': student['NAME'],
            'seat_no': student['SEAT NO.'],
            'mobile_no': student['MOB. NO.'],
            'received_amount': float(student['RE . AMOUNT']) if pd.notnull(student['RE . AMOUNT']) else 0.0,
            'due_amount': float(student['DUE']) if pd.notnull(student['DUE']) else 0.0,
            'total_amount': float(student['TOTAL']) if pd.notnull(student['TOTAL']) else 0.0,
            'payment_receive_date': format_date(student['PAYMENT RE. DATE']),
            'start_date': format_date(student['START DATE']),
            'end_date': format_date(student['END DATE']),
            'pay_mode': student['PAY MODE'] if pd.notnull(student['PAY MODE']) else '',
            'time_type': student['TIME'] if pd.notnull(student['TIME']) else ''
        }
        
        return details, None
    except Exception as e:
        return None, f"Error: {str(e)}"

def generate_fee_message_text(seat_no):
    """Generate fee message for a student"""
    details, error = get_student_details(seat_no)
    
    if error:
        return None, error
    
    message = (f"Dear {details['name']} (Seat No. {details['seat_no']}),\n\n"
               f"Your fee details are as follows:\n"
               f"Received Amount: {details['received_amount']}\n"
               f"Due Amount: {details['due_amount']}\n"
               f"Total Amount: {details['total_amount']}\n"
               f"Payment Receive Date: {details['payment_receive_date']}\n\n"
               f"Start Date: {details['start_date']}\n"
               f"End Date: {details['end_date']}\n\n"
               f"Thank you.\n"
               f"Friends Library.\n"
               f"+91 9636117578")
    
    return message, None

def get_all_data_sorted():
    """Get all data sorted by end date"""
    try:
        df = read_excel()
        df['END DATE'] = pd.to_datetime(df['END DATE'], errors='coerce')
        sorted_df = df.sort_values(by='END DATE')
        return sorted_df, None
    except Exception as e:
        return None, f"Error: {str(e)}"

def get_filtered_data(seat_no):
    """Get filtered data by seat number"""
    try:
        df = read_excel()
        df['SEAT NO.'] = df['SEAT NO.'].astype(str).str.strip()
        seat_no = seat_no.strip()
        
        filtered_df = df[df['SEAT NO.'] == seat_no]
        
        if filtered_df.empty:
            return None, "Student not found"
        
        return filtered_df, None
    except Exception as e:
        return None, f"Error: {str(e)}"

def get_all_seat_numbers():
    """Get list of all seat numbers"""
    try:
        df = read_excel()
        return df['SEAT NO.'].tolist(), None
    except Exception as e:
        return None, f"Error: {str(e)}"

def get_all_student_names():
    """Get list of all student names"""
    try:
        df = read_excel()
        return df['NAME'].dropna().unique().tolist(), None
    except Exception as e:
        return None, f"Error: {str(e)}"

def delete_student_by_name(student_name):
    """Delete a student by name"""
    try:
        df = read_excel()
        df = df[df['NAME'] != student_name]
        save_excel(df)
        return True, f"Student {student_name} deleted successfully"
    except Exception as e:
        return False, f"Error: {str(e)}"