# Benfords law 
This web app allows you to upload datasets and see how your data compares to Benford's law.  User upload a dataset and provide the name for the numeric column to be compared against Benford's law. 

Benford's law predicts the following frequency distribution for the leading digits of numbers in a dataset:
    1: 0.334, 
    2: 0.185,
    3: 0.124,
    4: 0.075,
    5: 0.071,
    6: 0.065,
    7: 0.055,
    8: 0.049,
    9: 0.042

Limitation: I only handle numbers that are larger than 1.

## Requirements
You need Python3 for this project. You also need the libraries `flask`, `plotly` and `pandas`. 

## Quick-start:
Checkout program, install libraries and run program:
```
git clone https://github.com/torasirkka/benfords-law.git
cd benfords-law
virtualenv env
source env/bin/activate
pip3 install -r requirementsn.txt
python3 server.py
```