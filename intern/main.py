import csv
from datetime import datetime, timedelta

# The path to your CSV file
file_path = 'employee_data.csv'

# Read the CSV file and analyze the data
with open(file_path, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)  # Read the header row

    # create the column line based on your CSV File
    employee_id_index = header.index('Position ID')
    status_index = header.index('Position Status')
    shift_start_time_index = header.index('Time')
    shift_end_time_index = header.index('Time Out')
    employee_name_index = header.index('Employee Name')

    # create the  variables to keep find of consecutive days and previous shift end time and not printed agin same employes names
    consecutive_days = 0
    previous_shift_end_time = None
    printed_names = set()

    for row in csvreader:
        employee_id = row[employee_id_index]
        status = row[status_index]
        shift_start_time = row[shift_start_time_index].strip()  # stripe used for Remove leading or trailing whitespace
        shift_end_time = row[shift_end_time_index].strip()      
        employee_name = row[employee_name_index]

        # Skip rows of employess who are  empty shift start or end times
        if not shift_start_time or not shift_end_time:
            continue

        # Convert the shift start time and end times to datetime employess
        shift_start_time = datetime.strptime(shift_start_time, '%m/%d/%Y %I:%M %p')
        shift_end_time = datetime.strptime(shift_end_time, '%m/%d/%Y %I:%M %p')

        # Calculate time difference between shifts
        if previous_shift_end_time:
            time_difference = (shift_start_time - previous_shift_end_time).total_seconds() / 3600

            # Check for if/else
            if time_difference < 10 and time_difference > 1 and employee_name not in printed_names:
                print(f"{employee_name} := worked with less than 10 hours between shifts.")
                printed_names.add(employee_name)
            if time_difference >= 24 * 7:  # 7 consecutive days
                consecutive_days += 1
            else:
                consecutive_days = 0

        previous_shift_end_time = shift_end_time

        if shift_end_time - shift_start_time >= timedelta(hours=14) and employee_name not in printed_names:
            print(f"{employee_name} :=  worked for more than 14 hours in a single shift.")
            printed_names.add(employee_name)
        if consecutive_days >= 7 and employee_name not in printed_names:
            print(f"{employee_name} := worked for 7 consecutive days.")
            printed_names.add(employee_name)
        # Reset consecutive_days if the status is not 'Active'
        if status != 'Active':
            consecutive_days = 0
