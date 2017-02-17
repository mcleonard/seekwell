from sqlalchemy import create_engine, MetaData, inspect, text
from .table import Table
from .records import Records

class Database(object):
    """ Connect to a database using SQLAlchemy

        Example
        -------
        db = Database('sqlite:///database.sql')

    """
    def __init__(self, path=None, dialect=None, user=None, 
                 pword=None, host=None, port=None, database=None,
                 **kwargs):

        if path is None:
            path = '{}://{}:{}@{}:{}/{}'.format(dialect, user, pword, host, port, database)
        self.engine = create_engine(path, **kwargs)
        self.db_path = path
        self.con = self.engine.connect()
        self.meta = MetaData(bind=self.engine)
        self.meta.reflect()
    
    @property
    def table_names(self):
        return list(self.meta.tables.keys())

    @property
    def schema_names(self):
        ins = inspect(self.engine)
        return ins.get_schema_names()
    
    def query(self, statement, **kwargs):
        """ Query the database, returns a Records object

            Parameters
            ----------
            s: SQL statement querying the database.

            This uses SQLAlchemy's text query system: 
            http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.expression.text

            
            Examples
            --------
            records = db.query('SELECT * FROM users')

            You can pass in parameters using keyword arguments:
            records = db.query('SELECT * FROM users WHERE user_name=:name', name='Fred')

        """
        return Records(self.con.execute(text(statement), **kwargs))

    def set_schema(self, schema):
        """ If you have schemas (in PostgreSQL for instance), set which schema you're 
            getting the tables from. """
        meta = MetaData(bind=self.engine, schema=schema)
        meta.reflect()
        self.meta = meta
        return self
    
    def __getitem__(self, key):

        if '.' in key:
            schema, table = key.split('.')
            schemas = self.schema_names
            if schema not in schemas:
                raise KeyError("Schema {} doesn't exist!".format(schema))

            _ = self.set_schema(schema)

            return Table(key, self)

        if key not in self.table_names:
            raise KeyError("Table {} doesn't exist!".format(key))
        else:
            return Table(key, self)
        
    def __repr__(self):
        return "Database('{}')".format(self.db_path)