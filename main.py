import sys
import csv
import json

from hashlib import sha256

from lib.csv2json import csv2json

ARGS = sys.argv
FILENAME = ARGS[1]
DATASET = list(csv.reader(open(FILENAME)))
JSON_DATASET = csv2json.load(FILENAME, smoothify=True, sep='_')
HEADER = DATASET.pop(0)
ROWS = DATASET


def main():
    HASHES = engine(JSON_DATASET)
    print(HASHES)
    
    
def engine(json_dataset):
    hashes = []
    for row in json_dataset:
        with open(f'{valid_available_name(row)}.json', 'w') as json_file:
            json.dump(json_transform(row), json_file, indent=4)
        with open(f'{valid_available_name(row)}.json', 'rb') as json_file:
            hashes.append(sha256(json_file.read()).hexdigest())
    return hashes

def json_transform(row):
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
    return json_object

def valid_available_name(row):
    return row.get('name') or row.get('filename') or row.get('file_name') or row.get('nft_name')


if __name__ == '__main__':
    main()