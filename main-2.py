import csv
import json
import os
from datetime import datetime

def convert_to_json(csv_file_path):
    """
    Converts data from a CSV file to a list of JSON objects.

    Args:
        csv_file_path (str): The path to the CSV file.

    Returns:
        list: A list of JSON objects representing the data from the CSV file.
    """
    json_data = []
    time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Timestamp created only once
    rfid_numbers = set()  # Set to store unique RFID numbers
    try:
        with open(csv_file_path, newline='', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            for row in csv_reader:

                # Convert date and time strings to datetime objects
                date_str = f"{row['date']}"
                time_str = f"{row['time']}"
                date_obj = datetime.strptime(date_str, '%d.%m.%Y')
                time_obj = datetime.strptime(time_str, '%H:%M:%S')

                # Build JSON object
                entry = {
                    'id': int(row['id']),
                    'rfid_number': row['rfid_number'],
                    'date': date_obj.strftime('%Y-%m-%d'),  # Convert datetime to string
                    'time': time_obj.strftime('%H:%M:%S')  # Convert datetime to string
                }
                json_data.append(entry)

            # Create JSON object with data and timestamp
            json_output = {
                'time_stamp': time_stamp,
                'data': json_data
            }
            return json_output

    except FileNotFoundError:
        return None  # Return None if CSV file does not exist

def write_json_file(data, output_path):
    """
    Writes the JSON data to a file.

    Args:
        data (list): The JSON data to be written.
        output_path (str): The path to the output file.
    """
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def move_to_done_folder(csv_file_path):
    """
    Moves the CSV file to a 'done' folder.

    Args:
        csv_file_path (str): The path to the CSV file.
    """
    done_folder = 'done' # Create a folder named 'done' to store processed files
    if not os.path.exists(done_folder):
        os.makedirs(done_folder)
    filename = os.path.basename(csv_file_path)
    os.rename(csv_file_path, os.path.join(done_folder, filename))

    try: 
        with open(csv_file_path, 'r', newline='', encoding='utf-8-sig') as csv_file: 
            csv_data = csv_file.read()
        done_folder = 'done'
        with open(f"{done_folder}/{csv_file_path.split('/')[-1]}", 'w') as done_file: 
            done_file.write(csv_data)
        os.remove(csv_file_path)
    except FileNotFoundError: 
        pass

def calculate_time_spent(data):
    """
    Calculates the time spent in the building for each RFID entry.

    Args:
        data (list): The list of JSON objects containing RFID entries.

    Returns:
        dict: A dictionary mapping RFID numbers to the total time spent in the building.
    """
    time_spent = {}
    for entry in data:
        rfid_number = entry['rfid_number']
        entry_time = datetime.strptime(entry['date'] + ' ' + entry['time'], '%Y-%m-%d %H:%M:%S')
        if rfid_number not in time_spent:
            time_spent[rfid_number] = {'hours': 0, 'minutes': 0}  # Initialize hours and minutes
        
        # Calculate time difference from entry time to current time
        time_difference = datetime.now() - entry_time
        hours = time_difference.seconds // 3600  # Convert seconds to hours
        minutes = (time_difference.seconds % 3600) // 60  # Calculate remaining minutes
        
        # Add calculated time to total time spent
        time_spent[rfid_number]['hours'] += hours
        time_spent[rfid_number]['minutes'] += minutes
        
        # Adjust minutes if it exceeds 60
        if time_spent[rfid_number]['minutes'] >= 60:
            time_spent[rfid_number]['hours'] += 1
            time_spent[rfid_number]['minutes'] -= 60
    
    return time_spent


if __name__ == '__main__':
    csv_file_path = 'rfid_tags_original.csv'
    json_data = convert_to_json(csv_file_path)

    if json_data is not None:
        current_date = datetime.now().strftime("%Y-%m-%d")
        output_path = f"rfid_tags_{current_date}.json"
        write_json_file(json_data, output_path)
        move_to_done_folder(csv_file_path)
        
        # Calculate and print time spent in the building for each RFID number
        time_spent = calculate_time_spent(json_data['data'])
        for rfid_number, time in time_spent.items():
            print(f"RFID Number: {rfid_number}, Time Spent in Building: {time} minutes")
        
        print("Conversion successful. JSON file created and CSV file moved to 'done' folder.")
    else:
        print("No CSV file found or empty CSV file detected. No conversion performed.")

