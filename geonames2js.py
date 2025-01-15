"""
Downloads data from GeoNames and saves it as JS or JSON files.

Requirements: Python 3.5 or higher.

Usage: python3 geonames2js.py [options]

Options and help: python3 geonames2js.py -h

Todo: Replace cases of "Union[list, dict]" with "list | dict" once
Python 3.10 becomes more widely used.

License: MIT.
Copyright: Jonas B.
"""



import sys, argparse, urllib.request, urllib.error, json
from zipfile import ZipFile
from io import BytesIO
from typing import Union



PLACE_NAME_URLS = {
  'countries': 'https://download.geonames.org/export/dump/countryInfo.txt',
  'regions': 'https://download.geonames.org/export/dump/admin1CodesASCII.txt',
  'cities': 'https://download.geonames.org/export/dump/cities5000.zip'
}
# Camel-cased because the output is JS or JSON whose file names are often camel-cased:
OUTPUT_FILE_NAME='geoNames'



def unzip_content(content: bytes) -> bytes:
  """ Unzip the first file in a ZIP archive and return its content. """
  with ZipFile(BytesIO(content)) as zip_file:
    return zip_file.read(zip_file.namelist()[0])

def parse_csv(data: str) -> list:
  """ Parse the CSV data; ignoring the header, empty lines, and comments. """
  lines = data.split('\n')[1:]
  return [line.split('\t') for line in lines if len(line) and line[0] != '#']

def to_json(data: Union[list, dict]) -> str:
  """ Return compact JSON (as small as possible). """
  return json.dumps(data, separators=(',', ':'))

def to_js(data: Union[list, dict]) -> str:
  return f'export default{to_json(data)}'

def compile_countries(data: list) -> list:
  return {val[0]: val[4] for val in data}

def compile_regions(data: list) -> list:
  return {val[0]: val[1] for val in data}

def compile_cities(data: list) -> Union[list, dict]:
  rows = {} if options.include_ids else []
  for val in data:
    parts = {
      'id': int(val[0]),
      'name': val[1],
      'region': val[10],
      'country': val[8],
      'latitude': float(val[4]),
      'longitude': float(val[5])
    }

    row = [parts['name'], parts['region'], parts['country']]

    if not options.exclude_locations:
      row.extend([parts['latitude'], parts['longitude']])

    if options.include_ids:
      rows[parts['id']] = row
    else:
      rows.append(row)

  return rows



# Setting up the command-line options and the help text:
option_parser = argparse.ArgumentParser(
  description='Download and save GeoNames data as JS or JSON files.'
)
option_parser.add_argument(
  '--format',
  choices=['JS', 'JSON'],
  default='JS',
  help='Output format (JS or JSON). Default is JS.'
)
option_parser.add_argument(
  '--individual-files',
  action='store_true',
  help='Save countries, regions, and cities to individual files as opposed to a single file.'
)
option_parser.add_argument(
  '--include-ids',
  action='store_true',
  help='Include GeoNames IDs in the city data.'
)
option_parser.add_argument(
  '--exclude-locations',
  action='store_true',
  help='Don\'t include locations in the city data.'
)
options = option_parser.parse_args()



# Downloading and treating each place-name file.
data = {}
for key, url in PLACE_NAME_URLS.items():
  try:
    response = urllib.request.urlopen(url)
  except urllib.error.URLError as e:
    sys.exit(f'Failed to download {url}. Reason: "{e.reason}".')

  content = response.read()
  if url.lower().endswith('.zip'):
    content = unzip_content(content)
  content = parse_csv(content.decode('utf-8'))

  # Getting the relevant data that we need from the full data:
  data[key] = globals()[f'compile_{key}'](content)

  # If the user wants indidual files for each category:
  if options.individual_files:
    file_name = OUTPUT_FILE_NAME + key.capitalize()

    if options.format == 'JS':
      with open(f'{file_name}.js', 'w') as file:
        file.write(to_js(data[key]))
    else:
      with open(f'{file_name}.json', 'w') as file:
        file.write(to_json(data[key]))

# If the user wants a single output file:
if not options.individual_files:
  if options.format == 'JS':
    with open(f'{OUTPUT_FILE_NAME}.js', 'w') as file:
      file.write(to_js(data))
  else:
    with open(f'{OUTPUT_FILE_NAME}.json', 'w') as file:
      file.write(to_json(data))