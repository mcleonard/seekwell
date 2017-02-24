
# SeekWell

[![Build Status](https://travis-ci.org/mcleonard/seekwell.svg?branch=master)](https://travis-ci.org/mcleonard/seekwell)

SeekWell is a Python package built for data analysts who want an easier way to get data from SQL databases. SeekWell is built on top of SQLAlchemy, so it can connect to pretty much any database. Using it is straightforward, as you can see in [this walkthrough I recorded](https://www.youtube.com/watch?v=FKANqEBTaOc).

## Usage

Import the Database object and connect to your database. Defining the database path uses the same URL structure as SQLAlchemy so [read up on their documentation](http://docs.sqlalchemy.org/en/latest/core/engines.html).
```python
from seekwell import Database

db = Database('sqlite:///database.sqlite')
```

Then to get data, simply pass in a SQL statement as a string to the `query` method.
```python
records = db.query('SELECT * from Player limit 50')
```

Data is returned lazily, so you have to fetch it before it's available.

```python
rows = records.fetch()
```

The fetched rows are cached in `records.rows`. Once you're happy with your data, you can write it out as a CSV, or convert it to a Pandas DataFrame.

```python
records.to_csv('filename.csv')
df = records.to_pandas()
```

## Documentation

No real documentation yet, but check out the notebook (seekwell.ipynb) for an example. You can view the notebook in GitHub just by clicking on it.



## Dependencies

SeekWell depends on SQLAlchemy and terminaltables. You'll need Pandas if you want to convert to a DataFrame.


## Installation

```
pip install seekwell
```

## The Future

Tests, documentation, add more export formats, etc. If you want to contribute, make some pull requests and I'll try to keep on top of it.
