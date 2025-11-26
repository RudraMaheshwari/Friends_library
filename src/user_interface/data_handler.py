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
    """Format date to DD/MM/YYYY string"""
    if pd.notnull(date_value):
        return pd.Timestamp(date_value).strftime('%d/%m/%Y')
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

def get_all_data_sorted_by_seat():
    """Get all data sorted by seat number (numeric first, then alphabetic)"""
    try:
        df = read_excel()
        df['SEAT NO.'] = df['SEAT NO.'].astype(str).str.strip()
        
        # Separate numeric and alphabetic seat numbers
        df['is_numeric'] = df['SEAT NO.'].str.isnumeric()
        df['seat_numeric'] = pd.to_numeric(df['SEAT NO.'], errors='coerce')
        
        # Sort: numeric seats first (by numeric value), then alphabetic seats (by string)
        sorted_df = df.sort_values(
            by=['is_numeric', 'seat_numeric', 'SEAT NO.'],
            ascending=[False, True, True]
        ).drop(columns=['is_numeric', 'seat_numeric'])
        
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

def generate_reminder_message_text(seat_no):
    """Generate reminder message for a student based on days remaining"""
    from datetime import datetime
    
    details, error = get_student_details(seat_no)
    
    if error:
        return None, error
    
    # Calculate days remaining
    try:
        if details['end_date'] != 'N/A':
            end_date = datetime.strptime(details['end_date'], '%d/%m/%Y')
            today = datetime.now()
            days_remaining = (end_date - today).days
            
            greeting = "Dear" if days_remaining >= 0 else "Hello"
            
            if days_remaining > 0:
                reminder_text = f"you only have {days_remaining} day{'s' if days_remaining != 1 else ''} remaining to submit the fees"
            elif days_remaining == 0:
                reminder_text = "today is the last day to submit the fees"
            else:
                reminder_text = f"your fee payment is overdue by {abs(days_remaining)} day{'s' if abs(days_remaining) != 1 else ''}"
            
            message = (f"{greeting} {details['name']},\n\n"
                       f"Greetings from Friends Library!\n\n"
                       f"{reminder_text}.\n\n"
                       f"Fee Details:\n"
                       f"Received Amount: ₹{details['received_amount']}\n"
                       f"Due Amount: ₹{details['due_amount']}\n"
                       f"Total Amount: ₹{details['total_amount']}\n"
                       f"End Date: {details['end_date']}\n\n"
                       f"Please ensure timely payment.\n\n"
                       f"Thanks and Regards,\n"
                       f"Friends Library\n"
                       f"+91 9636117578")
            
            return message, None
        else:
            return None, "End date not available"
    except Exception as e:
        return None, f"Error calculating days: {str(e)}"

def update_student_details(seat_no, student_data):
    """Update all details for a student"""
    try:
        df = read_excel()
        df['SEAT NO.'] = df['SEAT NO.'].astype(str).str.strip()
        seat_no = seat_no.strip()
        
        if seat_no not in df['SEAT NO.'].values:
            return False, f"Seat No. {seat_no} not found"
        
        df.loc[df['SEAT NO.'] == seat_no, 'NAME'] = student_data['name']
        df.loc[df['SEAT NO.'] == seat_no, 'MOB. NO.'] = student_data['mobile_no']
        df.loc[df['SEAT NO.'] == seat_no, 'START DATE'] = student_data['start_date']
        df.loc[df['SEAT NO.'] == seat_no, 'END DATE'] = student_data['end_date']
        df.loc[df['SEAT NO.'] == seat_no, 'PAYMENT RE. DATE'] = student_data['payment_receive_date']
        df.loc[df['SEAT NO.'] == seat_no, 'RE . AMOUNT'] = student_data['received_amount']
        df.loc[df['SEAT NO.'] == seat_no, 'DUE'] = student_data['due_amount']
        df.loc[df['SEAT NO.'] == seat_no, 'TOTAL'] = student_data['total_amount']
        df.loc[df['SEAT NO.'] == seat_no, 'PAY MODE'] = student_data['pay_mode']
        df.loc[df['SEAT NO.'] == seat_no, 'TIME'] = student_data['time_type']
        
        save_excel(df)
        return True, "Student details updated successfully"
    except Exception as e:
        return False, f"Error: {str(e)}"