"""
Current version

Converts csv to json and moves the csv file to done folder with timestamp
"""

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
    time_stamp = datetime.now()
    try:
        with open(csv_file_path, newline='', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            for row in csv_reader:
                # Convert date and time strings to a datetime object
                datetime_str = f"{row['date']} {row['time']}"
                date_time_obj = datetime.strptime(datetime_str, '%d.%m.%Y %H:%M:%S')

                # Build JSON object
                entry = {
                    'id': int(row['id']),
                    'rfid_number': row['rfid_number'],
                    'date_time': date_time_obj.strftime('%Y-%m-%d %H:%M:%S')  # Convert datetime to string
                }
                entry = {
                    'time_stamp': time_stamp
                }
                json_data.append(entry)
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
    done_folder = 'done'
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

if __name__ == '__main__':
    csv_file_path = 'rfid_tags_original.csv'
    json_data = convert_to_json(csv_file_path)

    if json_data is not None:
        current_date = datetime.now().strftime("%Y-%m-%d")
        output_path = f"rfid_tags_{current_date}.json"
        write_json_file(json_data, output_path)
        move_to_done_folder(csv_file_path)
        print("Conversion successful. JSON file created and CSV file moved to 'done' folder.")
    else:
        print("No CSV file found or empty CSV file detected. No conversion performed.")

