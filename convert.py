import csv
import json

csv_file_path = 'rfid_tags_orginal.csv'

if __name__ == '__main__':
    with open(csv_file_path, encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            print(line)
