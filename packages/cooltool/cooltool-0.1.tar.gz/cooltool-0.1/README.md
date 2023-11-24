# Lindvall tools

# Table of Contents

1. [Geodesy](#geodesy)
2. [Transform geographic latitude and longitude to grid x and y](#transform-geographic-latitude-and-longitude-to-grid-x-and-y)
3. [Examples](#exapmles)
4. [Using the terminal (CLI)](#using-the-terminal-(cli))
5. [Function import](#function-import)
6. [Run tests](#run-tests)

# Geodesy

## Transform geographic latitude and longitude to grid x and y
Using Gauss conformal projection and Krüger's formulas to transform geographic latitude and longitude to grid x and y.

The calculations and variable values used herein are directly taken from the [documentation](https://www.lantmateriet.se/globalassets/geodata/gps-och-geodetisk-matning/gauss_conformal_projection.pdf) by [Lantmäteriet](https://www.lantmateriet.se/en/).

### Examples
#### Using the terminal (CLI)
Print the function help section:
```
python main.py --help
```
Single input latitude and longitude in decimal degrees:
```
python main.py --phi 55.1 --lam 12.2 --ellipsoid GRS1980 --projection SWEREF99TM
```
Sinlge input latitude and longitude in degrees minutes and seconds:
```
python main.py --phi 55,10,0 --lam 12,1,0 --ellipsoid GRS1980 --projection SWEREF99TM
```
#### Function import
```
from lindvall_tools.geodesy.geodetic_to_grid import geodetic_to_grid

input_var = [
            [(55, 0, 0), (12, 45, 0)],
            [(55, 0, 0), (14, 15, 0)],
            [(57, 0, 0), (12, 45, 0)],
            [(57, 0, 0), (19, 30, 0)],
            [(59, 0, 0), (11, 15, 0)],
            [(59, 0, 0), (19, 30, 0)],
        ]
for _, var in enumerate(input_var):
    x, y = geodetic_to_grid(phi=var[0], lam=var[1], ellipsoid='GRS1980', projection='SWEREF99TM')
```
#### Run tests
Path to package root directory and run:
```
pytest
```