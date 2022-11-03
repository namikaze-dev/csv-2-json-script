import sys
import csv
import json
import os.path
import os

from hashlib import sha256
from lib.csv2json import csv2json

ARGS = sys.argv
FILENAME = None
OUTPUT_DIR_NAME = None
DATASET = None
HEADER = None
ROWS = None


def main():
    load_globals()
    create_dir(OUTPUT_DIR_NAME)
    
    HASHES = {}
    
    for team_name, rows in groupify(ROWS).items():
        json_dataset = csv2json.jsonify(rows, csv2json.smoothify(HEADER))
        current_hashes = json_hash_handler(json_dataset, sub_dir_path=team_name)
        HASHES.update(current_hashes)
    
    write_csv(f'{file_base_name(FILENAME)}.output.csv', ROWS, HEADER, HASHES)
    print('SUCCESS!')
    
    
def load_globals():
    global FILENAME
    global OUTPUT_DIR_NAME
    global HEADER
    global ROWS
    global DATASET
    
    try:
        FILENAME = ARGS[1]
    except Exception:
        print('filename argument missing!\npass the name of the file as an argument')
        sys.exit(-1)
        
    OUTPUT_DIR_NAME = 'output'
    DATASET = list(csv.reader(open(FILENAME)))
    HEADER = DATASET.pop(0)
    ROWS = list(filter(lambda row: row != [], DATASET))
    
     
def groupify(rows):
    grouped_rows, curr_team = {}, None
    for row in rows:
        if 'team' in row[0].lower():
            curr_team = row[0]
            grouped_rows[curr_team] = [row]
        else:
            row[0] = curr_team
            grouped_rows[curr_team].append(row)
    return grouped_rows
    

def write_csv(filename, rows, header, hashes, col_name='Sha256 Json Hash'):
    new_header = header + [col_name]
    with open(os.path.join(OUTPUT_DIR_NAME, filename), 'w', encoding='UTF-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(new_header)
        for row in rows:
            key = int(row[1])
            writer.writerow(row + [hashes.get(key)])
    
    
def json_hash_handler(json_dataset, sub_dir_path):
    hashes = {}
    for row in json_dataset:
        create_dir(os.path.join(OUTPUT_DIR_NAME, sub_dir_path))
        json_filename = os.path.join(OUTPUT_DIR_NAME, sub_dir_path, row.get('filename') + '.json')
        with open(json_filename, 'w') as json_file:
            json_object = json_transform(row)
            json.dump(json_object, json_file, indent=4)
        with open(json_filename, 'rb') as json_file:
            key = row.get('series-number')
            hashes[key] = sha256(json_file.read()).hexdigest() 
    return hashes


def json_transform(row):
    attributes_object = parse_attributes(row)
    json_object = {
        "format": "CHIP-0007",
        "name": row.get('name') or "",
        "description": row.get('description') or "",
        "minting_tool": row.get('team-names'),
        "sensitive_content": False,
        "series_number": row.get('series-number') or 0,
        "series_total": 420,
        "attributes": [{
            "trait_type": "gender",
            "value": row.get('gender') or ""
        }],
        "collection": {
            "name":
            "Zuri NFT Tickets for Free Lunch",
            "id":
            "b774f676-c1d5-422e-beed-00ef5510c64d",
            "attributes": [{
                "type": "description",
                "value": "Rewards for accomplishments during HNGi9."
            }]
        }
    }
    
    for key, val in attributes_object.items():
        if not key:
            continue
        attribute = { "trait_type": key, "value": val }
        json_object['attributes'].append(attribute)
    
    return json_object


def file_base_name(filename):
    return filename.removesuffix('.csv')


def parse_attributes(json_object):
    str_attributes = json_object.get('attributes')
    if not str_attributes:
        print('NOTE: There are Invalid/Empty "attributes" field(s) in your csv file!')
        return {'': ''}
    attributes = str_attributes.split(';')
    attributes_object = make_attributes_object(attributes)
    return attributes_object
    

def make_attributes_object(attributes):
    try:
        filtered = list(filter(lambda atr: bool(atr), attributes))
        processed = list(map(lambda atr: atr.split(':'), filtered))
        return {key.strip(): val.strip() for key, val in processed}
    except ValueError as error:
        print(f'Invalid attributes field: {filtered}\nerror:', error)
        sys.exit(-1)
        


def create_dir(folder_name):
    try:
        os.mkdir(folder_name)
    except Exception:
        pass
    
    
if __name__ == '__main__':
    main()