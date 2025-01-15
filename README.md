# geonames2js

Save place-name data (countries, regions, and cities) from GeoNames into JavaScript or JSON files.

This project is not intended to convert everything from GeoNames into JavaScript or JSON. It's intended to save specific pieces of data that are commonly needed when you want to create, say, a location widget in an app.

A location widget in this context could e.g. be a widget that allows you to autocomplete a city or country name. In order to make such a widget and have the data on the client-side (which is sometimes preferable), you'd typically need a JS version of the data. That is what this project provides.

Note that, in order to keep the output JS files small - they will often by used on the client-side - this project only downloads data from cities with at least 5,000 inhabitants. In other words, smaller towns will be ignored.