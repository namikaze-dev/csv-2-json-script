import csv

def load(file_name):
	dataset = list(csv.reader(open(file_name)))
	header = dataset.pop(0)
	return jsonify(dataset, header)


def jsonify(dataset, header):
	return list(map(lambda row: transform(header, row), dataset))

def transform(header, row):
	processed = {}
	for i in range(len(header)):
		if i >= len(row):
			processed[header[i]] = ''
		else:
			value = parse_int(row[i])
			processed[header[i]] = value
	return processed

def parse_int(str_value):
	try:
		return int(str_value)
	except:
		return parse_bool(str_value)

def parse_bool(str_value):
	try:
		return eval(str_value.capitalize())
	except:
		return str_value