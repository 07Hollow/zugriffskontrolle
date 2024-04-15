import csv
import json
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
    start_time = datetime.now()  # Record start time for processing
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
                json_data.append(entry)
    except FileNotFoundError:
        return None  # Return None if CSV file does not exist
    end_time = datetime.now()  # Record end time for processing
    processing_time = end_time - start_time  # Calculate processing time
    # Update each record with processing time
    for entry in json_data:
        entry['processing_time'] = processing_time.total_seconds()
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
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8-sig') as csv_file:
            csv_data = csv_file.read()
        done_folder = 'done'
        with open(f"{done_folder}/{csv_file_path.split('/')[-1]}", 'w') as done_file:
            done_file.write(csv_data)
        import os
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

