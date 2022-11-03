import sys
import csv
import json
import os.path
import os

from hashlib import sha256
from lib.csv2json import csv2json

ARGS = sys.argv
FILENAME = ARGS[1]
OUTPUT_DIR_NAME = 'output'
DATASET = list(csv.reader(open(FILENAME)))
HEADER = DATASET.pop(0)
ROWS = list(filter(lambda row: row != [] and row[0] != '', DATASET))


def main():
    create_folder(OUTPUT_DIR_NAME)
    HASHES = {}
    
    for team_name, rows in groupify(ROWS).items():
        json_dataset = csv2json.jsonify(rows, csv2json.smoothify(HEADER))
        current_hashes = engine(json_dataset, team_name=team_name, path=team_name)
        HASHES.update(current_hashes)
    
    write_csv(f'{file_base_name(FILENAME)}.output.csv', ROWS, HEADER, HASHES)
    print('SUCCESS!')
    
    
def groupify(rows):
    grouped_rows, curr_team = {}, None
    for row in rows:
        if 'team' in row[0].lower():
            curr_team = row[0]
            grouped_rows[curr_team] = []
        else:
            grouped_rows[curr_team].append(row)
    return grouped_rows
    

def write_csv(filename, rows, header, hashes, col_name='Sha256 Json Hash'):
    new_header = header + [col_name]
    with open(os.path.join(OUTPUT_DIR_NAME, filename), 'w', encoding='UTF-8', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(new_header)
        for row in rows:
            csv_writer.writerow(row + [hashes.get(row[0])])
    
    
def engine(json_dataset, path='', team_name='Team X'):
    hashes = {}
    for row in json_dataset:
        create_folder(os.path.join(OUTPUT_DIR_NAME, path))
        filename = os.path.join(OUTPUT_DIR_NAME, path, f'{valid_available_name(row)}.json')
        with open(filename, 'w') as json_file:
            json_object = json_transform(row, team_name)
            json.dump(json_object, json_file, indent=4)
        with open(filename, 'rb') as json_file:
            key = str(row.get('series_number') or row.get('series-number'))
            hashes[key] = sha256(json_file.read()).hexdigest() 
    return hashes


def json_transform(row, mint_tool):
    attributes_object = parse_attributes(row)
    
    json_object = {
        "format": "CHIP-0007",
        "name": valid_available_name(row) or "",
        "description": row.get('description') or "",
        "minting_tool": mint_tool,
        "sensitive_content": False,
        "series_number": row.get('series_number') or row.get('series-number'),
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


def valid_available_name(row):
    return row.get('filename') or row.get('file_name') or row.get('nft_name') or row.get('name')


def file_base_name(filename):
    return filename.removesuffix('.csv')


def parse_attributes(json_object):
    str_attributes = json_object.get('attributes')
    if not str_attributes:
        # print('NOTE: There are Invalid "attributes" field(s) in your csv file!')
        return {'': ''}
    if ',' in str_attributes:
        attributes = str_attributes.split(',')
    else:
        attributes = str_attributes.split('.')
    attributes_object = make_attributes_object(attributes)
    return attributes_object
    

def make_attributes_object(attributes):
    processed = list(map(lambda atr: atr.split(':'), attributes))
    return {key.strip(): val.strip() for key, val in processed}


def create_folder(folder_name):
    try:
        os.mkdir(folder_name)
    except Exception:
        pass
    
    
if __name__ == '__main__':
    main()