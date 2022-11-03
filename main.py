import sys
import csv
import json

from hashlib import sha256

from attr import attributes

from lib.csv2json import csv2json

ARGS = sys.argv
FILENAME = ARGS[1]
DATASET = list(csv.reader(open(FILENAME)))
JSON_DATASET = csv2json.load(FILENAME, smoothify=True, sep='_')
HEADER = DATASET.pop(0)
ROWS = DATASET


def main():
    HASHES = engine(JSON_DATASET)
    write_csv(f'{file_base_name(FILENAME)}.output.csv', ROWS, HEADER, HASHES)
    print('SUCCESS!')
    

def write_csv(fileName, rows, header, hashes, col_name='Sha256 Json Hash'):
    new_header = header + [col_name]
    with open(fileName, 'w', encoding='UTF-8', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(new_header)
        for i, row in enumerate(rows):
            csv_writer.writerow(row + [hashes[i]])
    
    
def engine(json_dataset):
    hashes = []
    for row in json_dataset:
        with open(f'{valid_available_name(row)}.json', 'w') as json_file:
            json_object = json_transform(row)
            json.dump(json_object, json_file, indent=4)
        with open(f'{valid_available_name(row)}.json', 'rb') as json_file:
            hashes.append(sha256(json_file.read()).hexdigest())
    return hashes

def json_transform(row):
    attributes_object = parse_attributes(row)
    
    json_object = {
        "format": "CHIP-0007",
        "name": valid_available_name(row) or "",
        "description": row.get('description') or "",
        "minting_tool": "Team x",
        "sensitive_content": False,
        "series_number": row.get('series_number'),
        "series_total": 526,
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
            return
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
        print('No / Invalid "attributes" field(s) in your csv file!')
        return {'':''}
    if ',' in str_attributes:
        attributes = str_attributes.split(',')
    else:
        attributes = str_attributes.split('.')
    attributes_object = make_attributes_object(attributes)
    return attributes_object
    

def make_attributes_object(attributes):
    processed = list(map(lambda atr: atr.split(':'), attributes))
    return {key.strip(): val.strip() for key, val in processed}
    
    

if __name__ == '__main__':
    main()