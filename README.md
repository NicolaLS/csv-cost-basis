# csv-cost-basis

Export transaction history from the BitBox App and calculate the fiat value for each transaction and the overall cost basis.

## How to use this

Open your terminal on linux or mac, on windows you can use powershell.

You'll need Python and either globally or in a virtual env installed:

- pandas
- requests

##### Virtual Environment

```shell
python -m venv venv
source ./venv/bin/activate
pip install pandas requests
```

You can also just pip install the dependencies globally without venv.

### 1. Clone this repository and create data dir

`git clone https://github.com/NicolaLS/csv-cost-basis.git`
`mkdir data`

### 2. Export the transaction history as CSV from the BitBox App

Move it to the data folder of this repository and give it the name `history.csv`
you can choose another file name and path as the second command line argument if you want.

### 3. Run the script

The script will default to USD if no currency is given (lowercase 3 letter code e.g chf, usd, eur)
examples:
`python ./src/main.py`
`python ./src/main.py chf`
`python ./src/main.py eur /home/myuser/myspecial/file.csv`

The result will be stored in the data directory even if you give a custom path
