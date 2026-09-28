import sqlite3,pytest
from core import seed,execute,plan
@pytest.fixture
def database(tmp_path):p=tmp_path/'sales.db';seed(p);return p

def test_totals(database):
 rows=execute('SELECT COUNT(*) AS n FROM orders',path=database);assert rows==[{'n':300}]
@pytest.mark.parametrize('sql',["DELETE FROM orders","DROP TABLE orders","PRAGMA table_info(orders)","SELECT name FROM sqlite_master","ATTACH DATABASE ':memory:' AS extra"])
def test_database_denies_mutation_and_metadata(database,sql):
 with pytest.raises(sqlite3.DatabaseError):execute(sql,path=database)
@pytest.mark.parametrize('q',['drop orders','revenue; delete','tell me a story','top 999 products'])
def test_bad_question(q):
 with pytest.raises(ValueError):plan(q)
def test_limit_parameterized(database):
 _,sql,params=plan('top 3 products');assert params==(3,) and len(execute(sql,params,database))==3
