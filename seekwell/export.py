def to_ascii(rows, n=None):
    from terminaltables import AsciiTable
    
    if n is None:
        n = rows.max_display_rows
    
    table_data = [rows.headers]
    
    for each in rows.rows[:n]:
        table_data.append(each)
    
    if len(table_data) < len(rows):
        table_data.append(['...']*len(table_data[0]))
    
    asciitable = AsciiTable(table_data)
    asciitable.outer_border = False

    return asciitable.table

def _html_table_row(row, header=False):
    tag = 'th' if header else 'td'
    row_items = ' '.join('<{tag}>{}</{tag}>'.format(each, tag=tag) for each in row)

    return '<tr>{}</tr>'.format(row_items)

def to_html(rows, n=None):

    if n is None:
        n = rows.max_display_rows
    
    headers = rows.headers
    print_rows = rows.rows[:n]
    
    more = _html_table_row(['...']*len(headers)) if n < len(rows.rows) else ''
    
    html_rows = '\n'.join(_html_table_row(row) for row in print_rows)
    html_table = '\n'.join(['<table style="font-size:10pt; white-space:nowrap;">',
                            _html_table_row(headers, header=True),
                            html_rows,
                            more,
                            '</table>'])
    return html_table

def to_pandas(rows):
    import pandas as pd
    return pd.DataFrame(rows.rows, columns=rows.headers)

def to_csv(rows, file, **kwargs):
    """
    For the keyword arguments that let you set the delimiter, etc. :
        https://docs.python.org/3/library/csv.html#csv-fmt-params
    """
    import csv
    with open(file, 'w') as f:
        csv_writer = csv.writer(f, **kwargs)
        csv_writer.writerow(rows.headers)
        csv_writer.writerows(rows.rows)