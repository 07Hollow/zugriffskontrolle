"""
This is the first version of the code. It is depracated and should not be used.
The current version of the code is in main-2.py.

Only Converts csv to json and moves the csv file to done folder.
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
    with open(csv_file_path, encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            # Convert date and time strings to a datetime object
            datetime_str = f"{row['date']} {row['time']}"
            date_time_obj = datetime.strptime(datetime_str, '%d.%m.%Y %H:%M:%S')
            
            # Build JSON object
            entry = {
                'id': int(row['id']),
                'rfid_number': row['rfid_number'],
                'date_time': date_time_obj.strftime('%Y-%m-%d %H:%M:%S')
            }
            json_data.append(entry)
    return json_data

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

if __name__ == '__main__':
    csv_file_path = 'rfid_tags_orginal.csv'
    json_data = convert_to_json(csv_file_path)
    output_path = 'rfid_tags_converted.json'
    write_json_file(json_data, output_path)
    move_to_done_folder(csv_file_path)
