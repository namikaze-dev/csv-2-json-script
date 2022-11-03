# Process-CSV-Script
<hr>


## Description
This script processes a given csv file with appropiate columns.

For each row in the csv, generate a <strong>CHIP-0007</strong> compatible json file,
makes a hash of the json file, adds a <strong>Sha256 Json Hash</strong> header
to the given and appends it the original row(row from
which json was created) under this header, outputs a new csv file with
name original-filename.output.csv.
Does not modify input csv file.

## Input
An appropiate/valid csv file.
The following csv columns are required:
<ul>
	<li>Series Number</li>
	<li>NFT Name</li>
	<li>Description</li>
	<li>Gender</li>
	<li>
		Attributes
		<div>&nbsp;&nbsp;&nbsp;&nbsp;format: "key: value, key-2: value-2, key-3: value-3"</div>
	</li>
</ul>

## Output
<ul>
	<li>A modified csv file with a new <strong>Sha256 Json Hash</strong> header column</li>
	<li>Json file of each csv row</li>
</ul>

csv format: input-filename.output.csv  
json format: nft-name.json  
All inside a folder named <em>output</em>

## Installation
Before proceeding, makes sure python is installed in your machine.
<ol>
	<li>Download process-csv.zip</li>
	<li>Extract download to <strong>C:\process-csv</strong> or your desired location</li>
	<li>Done :)</li>
</ol>

## Usage
Copy the csv file to process to the extraction directory.

run the command below  
<code>
	python main.py your-csv-file.csv
</code>  
or  
<code>
	python3 main.py your-csv-file.csv
</code>  

Output files should be in a folder named <em>output</em>