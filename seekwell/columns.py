from collections import OrderedDict
from export import to_html

class Columns(object):
    def __init__(self, headers, dict=None):
        self.headers = headers
        self.dict = {each: None for each in headers}

    def update(self, dict):
        self.dict.update(dict)

    def print(self, n=None, returns=False):
        if n is None:
            n = self.max_display_rows
        table_data = [self.column_names]
        if self.rows:
            for each in self.rows[:n]:
                table_data.append(each)
        
        if len(table_data) < len(self.rows):
            table_data.append(['...']*len(table_data[0]))
        
        asciitable = PrintTable(table_data)
        asciitable.outer_border = False
        
        if returns:
            return asciitable.table
        else:
            print(asciitable.table)

    def __repr__(self):
        return self.print(self.max_display_rows, returns=True)

    def _repr_html_(self):
        return to_html(self, self.max_display_rows)


