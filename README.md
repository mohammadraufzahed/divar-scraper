# divar-scraper
Divar scraper is a simple web scraper to extract the customer's phone number and poster information from the divar.
# About
This scraper helps us to create a database of the divar users phone number and posters
# Requirements
- Python: 3.9
- selenium: 3.141.0
- url-normalize: 1.4.3
- colorama: 0.4.4
- Unidecode: 1.2.0
- psycopg2-binary: 2.8.6
- autopep8: latest
- pylint: latest
- stdiomask: 0.0.6
## Setup

First, we must install the pipenv to manage our packages:

```shell
$ pip install -U pipenv --user
```

after this, we must install our dependencies:

```shell
$ python -m pipenv install
```

after that, we must enter into the virtualenv that we created in the previous step:

```shell
$ python -m pipenv shell
```

after that, we must initial our database and required files:

```shell
$ python main.py --init y
Database Host: <Your Postgres server address>
Database Username: <Your Postgres username>
Database Password: <Your Postgres password>
Database Name: <Your Postgres database name>
```
# Usage
```shell
$ python main.py
usage: main.py [-h] [--init INIT] [--start START]

Scrap the data from divar

optional arguments:
  -h, --help     show this help message and exit
  --init INIT    Initial the required files and database
  --start START  start the scraper
```