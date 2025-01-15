# geonames2js

Save place-name data (countries, regions, and cities) from [GeoNames](https://www.geonames.org/) into JavaScript or JSON files.

This project is not intended to convert everything from GeoNames into JavaScript or JSON. It's intended to save specific pieces of data that are commonly needed when you want to create e.g. a location widget in an app or website.

A location widget in this context could e.g. be a widget that allows you to autocomplete a city or country name. In order to make such a widget and have the data on the client-side (which is sometimes preferable), you'd typically need a JS version of the data. That is what this project provides.



## Before using the script

1. Make sure you have Python 3.5+ installed on your computer.
1. Download geonames2js.py.
1. Open your terminal and change directory to where you downloaded the script into.
1. Continue to [Usage](#usage). If the ```python3``` command doesn't work on your system even if Python is installed, try with ```python``` or ```py``` instead.



## Usage

### Normal usage:
```shell
# This will create a geoNames.js file in your current directory.
python3 geonames2js.py
```

### Viewing the command-line options:
```shell
# Get help:
python3 geonames2js.py --help
```

### Getting custom output:
```shell
# Output JSON instead of JavaScript:
python3 geonames2js.py --format=JSON

# Output a country file, region file, and
# city file instead of merging the three:
python3 geonames2js.py --individual-files

# Include GeoNames city IDs in the city
# data. For regions and countries, IDs are
# already included. This option will make
# the output larger.
python3 geonames2js.py --include-ids

# Don't include latitude and longitude in
# the city output. This makes the output
# smaller.
python3 geonames2js.py --exclude-locations

```



## Notes

In order to keep the output JS files small - they will often be used on the client-side - this project only downloads data from cities with at least 5,000 inhabitants. In other words, smaller towns will be ignored.
