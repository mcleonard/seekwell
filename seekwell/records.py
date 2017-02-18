from __future__ import print_function
from .export import to_html, to_ascii, to_pandas, to_csv
from numbers import Number

class Rows(object):

    def __init__(self, rows=None, headers=None):
        self.rows = rows
        self.headers = headers
        self.max_display_rows = 50

    def to_ascii(self, n=None):
        """ Return the rows as a table written in ASCII characters. """
        return to_ascii(self, n=n)

    def to_html(self, n=None):
        """ Return the rows as an HTML table """
        return to_html(self, n=n)

    def to_pandas(self):
        """ Return the rows as a Pandas DataFrame """
        return to_pandas(self)

    def to_csv(self, filename, **kwargs):
        """ Write the rows out to a CSV file.

            For the keyword arguments that let you set the delimiter, etc. :
            https://docs.python.org/3/library/csv.html#csv-fmt-params

        """
        to_csv(self, filename, **kwargs)
        return None

    def head(self, n=10):
        """ Return the first n rows """
        return self[:n]

    def print(self, n=None):
        """ Print out the rows as an ASCII table """
        print(self.to_ascii(n=n))

    def __getattr__(self, name):
        if name not in self.headers:
            raise AttributeError("Column {} doesn't exist.")
        return self[name]

    def __len__(self):
        return len(self.rows)

    def _get_column(self, key):
        if isinstance(key, str) and key not in self.headers:
            raise KeyError("Column {} doesn't exist!".format(key))
        idx = self.headers.index(key)
        return [[row[idx]] for row in self]

    def _get_columns(self, keys):
        for key in keys:
            if isinstance(key, str) and key not in self.headers:
                raise KeyError("Column {} doesn't exist!".format(key))
        idxs = [self.headers.index(each) for each in keys]
        col_rows = [[row[ii] for ii in idxs] for row in self.rows]
        return col_rows

    def __getitem__(self, key):
        # Here we'll get columns, rows, and slices - similar to Pandas
        if isinstance(key, list):
            # Input = list of column names
            new_rows = self._get_columns(key)
            return Rows(rows=new_rows, headers=key)
        elif isinstance(key, str):
            # Input = one column name
            new_rows = self._get_column(key)
            return Rows(new_rows, headers=[key])
        elif isinstance(key, Number):
            # Return a row
            return Rows([self.rows[key]], self.headers)
        else:
            # Slicing here
            return Rows(self.rows[key], self.headers)

    def __repr__(self):
        return self.to_ascii()

    def _repr_html_(self):
        return self.to_html()


class Records(Rows):

    def __init__(self, result_object, rows=None):

        self.result = result_object
        self.column_names = self.result.keys()
        super(Records, self).__init__(rows=[] if rows is None else rows,
                         headers=self.column_names)

    def __iter__(self):
        # If we've already got the results, iterate from cache
        if self.result.closed:
            for row in self.rows:
                yield row
        else:
            row = self.result.fetchone()
            while row is not None:
                self.rows.append(row)
                yield row
                row = self.result.fetchone()
            else:
                # Close results after getting all the data
                self.result.close()

    def fetch(self, n=None):
        """  """
        if n is None:
            values = [row for row in self]
        else:
            values = list(next(self.__iter__()) for _ in range(n))
        return self

    def __getitem__(self, key):

        # First try slicing
        try:
            stop = key.stop
        except AttributeError:
            pass
        else:
            # If we haven't fetched up to 'stop' yet, need to get those rows
            if stop is None:
                self.fetch()
            elif not self.result.closed and stop > len(self.rows):
                self.fetch(stop-len(self.rows))

            new = Rows(self.rows[key], self.headers)
            return new

        return super().__getitem__(key)
