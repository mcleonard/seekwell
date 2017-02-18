import seekwell

db = seekwell.Database('sqlite:///:memory:')

db.query('CREATE TABLE foo (bar integer)')


def test_db_fetch():
    db.query('INSERT INTO foo VALUES (42)')
    db.query('INSERT INTO foo VALUES (43)')
    records = db.query('SELECT * from foo')
    rows = records.fetch()
    assert len(rows) == 2
