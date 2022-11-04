import sys

from attr import attributes


def transform(header, row):
    return {key: val for key, val in zip(header, row)}


def json_transform(row_object):
    json_object = {
        "format": "CHIP-0007",
        "name": row_object.get('Name') or "",
        "description": row_object.get('Description') or "",
        "minting_tool": row_object.get('TEAM NAMES'),
        "sensitive_content": False,
        "series_number": row_object.get('Series Number') or 0,
        "series_total": 420,
        "attributes": [{
            "trait_type": "gender",
            "value": row_object.get('Gender') or ""
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
    
    attributes_object = parse_attributes(row_object)
    for key, val in attributes_object.items():
        if not key:
            continue
        attribute = { "trait_type": key, "value": val }
        json_object['attributes'].append(attribute)
    return json_object


def parse_attributes(row_object):
    str_attr = row_object.get('Attributes')
    if not str_attr:
        print('NOTE: There are Invalid/Empty "attributes" field(s) in your csv file!')
        return {'': ''}
    attributes = str_attr.split(';')
    return make_attributes_object(attributes)
    

def make_attributes_object(attributes):
    try:
        filtered = list(filter(lambda atr: bool(atr), attributes))
        processed = list(map(lambda atr: atr.split(':'), filtered))
        return {key.strip(): val.strip() for key, val in processed}
    except ValueError as error:
        print(f'Invalid attributes field: {filtered}\nerror:', error)
        sys.exit(-1)