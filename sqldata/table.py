class Table(object):
    def __init__(self, table, db):
        self.table = db.meta.tables[table]
        self.db = db
        self.name = self.table.description
    
    @property
    def column_names(self):
        return self.table.columns.keys()
    
    @property
    def dtypes(self):
        return {col.description: col.type for col in self.table.columns}
    
    def head(self, n=10):
        records = self.db.query('Select * from {} limit {}'.format(self.name, n))
        _ = records.fetch()
        return records
    
    def __repr__(self):
        return "Table({}, {})".format(self.name, self.db)