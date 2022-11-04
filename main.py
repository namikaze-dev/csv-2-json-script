import sys
import csv
import json
import os.path
import os

from hashlib import sha256
from helpers import transform, json_transform


def main():
    # get inputs
    filename = get_args()
    dataset = read_csv(filename)
    header = dataset[0]
    rows = dataset[1:]
    output_dir_name = 'OUTPUT'
    
    # process
    create_dir(output_dir_name)
    output_header, output_rows = write_json_files(header, rows, output_dir_name)
 
    # write
    write_csv(output_header, output_rows, filename, output_dir_name)
    print('SUCCESS!')
        
    
def read_csv(filename):
    dataset = list(csv.reader(open(filename)))
    filtered = list(filter(lambda row: bool(row), dataset))
    return filtered


def write_csv(header, rows, filename, output_dir_name=''):
    with open(os.path.join(output_dir_name, filename + 'output.csv'), 'w', encoding='UTF-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)


def write_json_files(header, rows, output_dir_name=''):
    json_rows = jsonify(header, rows)
    output_header = header + ['Hash']
    output_rows = []
    for i, json_row in enumerate(json_rows):
        sub_dir_name = os.path.join(output_dir_name, json_row.get('TEAM NAMES'))
        create_dir(sub_dir_name)
        json_filename = os.path.join(sub_dir_name, json_row.get('Filename') + '.json')
        with open(json_filename, 'w') as json_file:
            json_object = json_transform(json_row)
            json.dump(json_object, json_file, indent=4)
        with open(json_filename, 'rb') as json_file:
            json_hash = sha256(json_file.read()).hexdigest() 
            output_rows.append(rows[i] + [json_hash])
    return output_header, output_rows
    
                        
        
        
def jsonify(header, rows):
    json_rows, team_name  = [], rows[0]
    for row in rows:
        if row[0] == '':
            row[0] = team_name
        else:
            team_name = row[0]
        json_rows.append(transform(header, row))
    return json_rows
        


def get_args():
    args = sys.argv
    try:
        filename = args[1]
        return filename
    except Exception:
        print('filename argument missing!\npass the name of the file as an argument')
        sys.exit(-1)


def create_dir(folder_name):
    try:
        os.mkdir(folder_name)
    except Exception:
        pass


if __name__ == '__main__':
    main()