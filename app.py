from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
import shutil
app = Flask(__name__)

# Construct the absolute path to the Excel file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_FILE_PATH = os.path.join(BASE_DIR, 'LIBRARY LIST.xlsx')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        try:
            df = pd.read_excel(EXCEL_FILE_PATH)

            name = request.form['name']
            seat_no = request.form['seatNo']
            mobile_no = request.form['mobileNo']
            starting_date = request.form['startingDate']
            end_date = request.form['endDate']
            payment_receive_date = request.form['paymentReceiveDate']
            received_amount = request.form['receivedAmount']
            due_amount = request.form['dueAmount']
            total_amount = request.form['totalAmount']
            pay_mode = request.form['acType']
            time_type = request.form['timeType']

            # Add the new student to the DataFrame
            new_student = pd.DataFrame({
                'SEAT NO.': [seat_no],
                'NAME': [name],
                'MOB. NO.': [mobile_no],
                'START DATE': [starting_date],
                'END DATE': [end_date],
                'PAYMENT RE. DATE': [payment_receive_date],
                'RE . AMOUNT': [received_amount],
                'DUE': [due_amount],
                'TOTAL': [total_amount],
                'PAY MODE': [pay_mode],
                'TIME': [time_type]
            })
            df = pd.concat([df, new_student], ignore_index=True)

            # Save the updated DataFrame back to the Excel file
            temp_file_path = os.path.join(BASE_DIR, 'temp_LIBRARY_LIST.xlsx')
            df.to_excel(temp_file_path, index=False)
            shutil.move(temp_file_path, EXCEL_FILE_PATH)

            return jsonify({'message': 'Student added successfully'})
        except Exception as e:
            return jsonify({'error': str(e)})

    return render_template('add_student.html')

@app.route('/update_fee', methods=['GET', 'POST'])
def update_fee():
    if request.method == 'POST':
        try:
            data = request.get_json()
            seat_no = data['seatNo'].strip()  # Strip leading/trailing spaces
            received_amount = float(data['receivedAmount']) if data['receivedAmount'] else 0.0
            due_amount = float(data['dueAmount']) if data['dueAmount'] else 0.0
            total_amount = float(data['totalAmount']) if data['totalAmount'] else 0.0
            payment_receive_date = data['paymentReceiveDate']
            pay_mode = data['payMode']
            start_date = data['startDate']
            end_date = data['endDate']

            # Read the Excel file
            df = pd.read_excel(EXCEL_FILE_PATH, engine='openpyxl')

            # Strip leading/trailing spaces from seat numbers in the DataFrame
            df['SEAT NO.'] = df['SEAT NO.'].astype(str).str.strip()

            # Check if the seat number exists in the DataFrame
            if seat_no not in df['SEAT NO.'].values:
                return jsonify({'error': f'Seat No. {seat_no} not found in the Excel file'})

            # Update the fee details for the student
            df.loc[df['SEAT NO.'] == seat_no, 'RE . AMOUNT'] = received_amount
            df.loc[df['SEAT NO.'] == seat_no, 'DUE'] = due_amount
            df.loc[df['SEAT NO.'] == seat_no, 'TOTAL'] = total_amount
            df.loc[df['SEAT NO.'] == seat_no, 'PAYMENT RE. DATE'] = payment_receive_date
            df.loc[df['SEAT NO.'] == seat_no, 'PAY MODE'] = pay_mode
            df.loc[df['SEAT NO.'] == seat_no, 'START DATE'] = start_date
            df.loc[df['SEAT NO.'] == seat_no, 'END DATE'] = end_date

            # Save the updated DataFrame back to the Excel file
            temp_file_path = os.path.join(BASE_DIR, 'temp_LIBRARY_LIST.xlsx')
            df.to_excel(temp_file_path, index=False)
            shutil.move(temp_file_path, EXCEL_FILE_PATH)

            return jsonify({'message': 'Fee details updated successfully'})
        except Exception as e:
            return jsonify({'error': str(e)})

    try:
        # Read the Excel file to populate the dropdowns
        df = pd.read_excel(EXCEL_FILE_PATH)
        seat_nos = df['SEAT NO.'].tolist()
    except Exception as e:
        return jsonify({'error': str(e)})

    return render_template('update_fee.html', seat_nos=seat_nos)

@app.route('/generate_fee_message', methods=['GET', 'POST'])
def generate_fee_message():
    if request.method == 'POST':
        try:
            data = request.get_json()
            seat_no = data['seatNo'].strip()  # Strip leading/trailing spaces

            # Read the Excel file
            df = pd.read_excel(EXCEL_FILE_PATH)

            # Convert date columns to datetime objects
            date_columns = ['PAYMENT RE. DATE', 'START DATE', 'END DATE']
            for col in date_columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

            # Strip leading/trailing spaces from seat numbers in the DataFrame
            df['SEAT NO.'] = df['SEAT NO.'].astype(str).str.strip()

            # Find the student and generate the fee message
            student = df[df['SEAT NO.'] == seat_no]
            if not student.empty:
                name = student['NAME'].values[0]
                received_amount = student['RE . AMOUNT'].values[0]
                due_amount = student['DUE'].values[0]
                total_amount = student['TOTAL'].values[0]

                # Format dates to remove time and fractional seconds
                def format_date(date_value):
                    if pd.notnull(date_value):
                        return pd.Timestamp(date_value).strftime('%Y-%m-%d')
                    return "N/A"

                payment_receive_date = format_date(student['PAYMENT RE. DATE'].values[0])
                start_date = format_date(student['START DATE'].values[0])
                end_date = format_date(student['END DATE'].values[0])

                message = (f"Dear {name} (Seat No. {seat_no}),\n\n"
                           f"Your fee details are as follows:\n"
                           f"Received Amount: {received_amount}\n"
                           f"Due Amount: {due_amount}\n"
                           f"Total Amount: {total_amount}\n"
                           f"Payment Receive Date: {payment_receive_date}\n\n"
                           f"Start Date: {start_date}\n"
                           f"End Date: {end_date}\n\n"
                           f"Thank you.\n"
                           f"Friends Library.\n"
                           f"+91 9636117578")
            else:
                message = f"Student with Seat No. {seat_no} not found."

            return jsonify({'message': message})
        except Exception as e:
            return jsonify({'error': str(e)})

    try:
        df = pd.read_excel(EXCEL_FILE_PATH)
        seat_nos = df['SEAT NO.'].tolist()
    except Exception as e:
        return jsonify({'error': str(e)})

    return render_template('generate_fee_message.html', seat_nos=seat_nos)

@app.route('/show_data')
def show_data():
    try:
        # Read the Excel file
        df = pd.read_excel(EXCEL_FILE_PATH)

        # Convert "END DATE" to datetime for sorting
        df['END DATE'] = pd.to_datetime(df['END DATE'], errors='coerce')

        # Sort the DataFrame by "END DATE" in descending order
        sorted_df = df.sort_values(by='END DATE')

        # Convert the sorted DataFrame to HTML
        data_html = sorted_df.to_html(index=False)
    except Exception as e:
        return jsonify({'error': str(e)})

    return render_template('show_data.html', data_html=data_html)


@app.route('/filter_data', methods=['POST'])
def filter_data():
    seat_no = request.form.get('seat_no')
    if seat_no is None:
        return jsonify({'error': 'Seat number is required'}), 400

    try:
        # Read the Excel file
        df = pd.read_excel(EXCEL_FILE_PATH)

        # Strip leading/trailing spaces from seat numbers in the DataFrame
        df['SEAT NO.'] = df['SEAT NO.'].astype(str).str.strip()

        # Filter the DataFrame based on the seat number
        filtered_df = df[df['SEAT NO.'] == seat_no]

        if filtered_df.empty:
            return jsonify({'error': 'Student not found'}), 404

        # Convert the filtered DataFrame to HTML
        data_html = filtered_df.to_html(index=False)
    except Exception as e:
        return jsonify({'error': str(e)})

    return render_template('show_data.html', data_html=data_html)

@app.route('/get_student_details', methods=['POST'])
def get_student_details():
    data = request.get_json()
    seat_no = data.get('seatNo')

    if seat_no is None:
        return jsonify({'error': 'Seat number is required'}), 400

    try:
        # Read the Excel file
        df = pd.read_excel(EXCEL_FILE_PATH)

        # Strip leading/trailing spaces from seat numbers in the DataFrame
        df['SEAT NO.'] = df['SEAT NO.'].astype(str).str.strip()

        # Find the student details
        student_details = df[df['SEAT NO.'] == seat_no]

        if student_details.empty:
            return jsonify({'error': 'Student not found'}), 404

        student_details = student_details.iloc[0]

        # Helper function to format dates
        def format_date(date_value):
            if pd.notnull(date_value):
                return pd.Timestamp(date_value).strftime('%Y-%m-%d')
            return "N/A"

        response_data = {
            'studentName': student_details['NAME'],
            'seatNumber': student_details['SEAT NO.'],
            'receivedAmount': float(student_details['RE . AMOUNT']) if pd.notnull(student_details['RE . AMOUNT']) else 0.0,
            'dueAmount': float(student_details['DUE']) if pd.notnull(student_details['DUE']) else 0.0,
            'totalAmount': float(student_details['TOTAL']) if pd.notnull(student_details['TOTAL']) else 0.0,
            'paymentReceiveDate': format_date(student_details['PAYMENT RE. DATE']),
            'startingDate': format_date(student_details['START DATE']),
            'end_date': format_date(student_details['END DATE'])
        }

        return jsonify(response_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_data', methods=['GET', 'POST'])
def delete_data():
    try:
        # Read the Excel file
        df = pd.read_excel(EXCEL_FILE_PATH)

        # Get the list of student names for the dropdown
        student_names = df['NAME'].dropna().unique().tolist()

        if request.method == 'POST':
            # Get the selected student's name from the form
            selected_student_name = request.form.get('student_name')

            if selected_student_name:
                # Delete the student data from the DataFrame
                df = df[df['NAME'] != selected_student_name]

                # Save the updated DataFrame back to the Excel file
                temp_file_path = os.path.join(BASE_DIR, 'temp_LIBRARY_LIST.xlsx')
                df.to_excel(temp_file_path, index=False)
                shutil.move(temp_file_path, EXCEL_FILE_PATH)

                return jsonify({'message': f'Student {selected_student_name} deleted successfully.'})

            return jsonify({'error': 'No student selected for deletion.'}), 400

    except Exception as e:
        return jsonify({'error': str(e)})

    return render_template('delete_data.html', student_names=student_names)

if __name__ == '__main__':
    app.run(debug=True)
