import sqlite3,re,json
from pathlib import Path
ROOT=Path(__file__).parent;DB=ROOT/'var/sales.sqlite'
def seed(path=DB):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
 with sqlite3.connect(path) as c:
  c.executescript('CREATE TABLE IF NOT EXISTS orders(id INTEGER PRIMARY KEY,month TEXT,product TEXT,category TEXT,quantity INTEGER,cents INTEGER);')
  if c.execute('SELECT count(*) FROM orders').fetchone()[0]==0:
   c.executemany('INSERT INTO orders VALUES(?,?,?,?,?,?)',[(i,f'2026-{i%6+1:02}',f'Product {i%9+1}',['Home','Electronics','Books'][i%3],i%4+1,(i%4+1)*(1200+i%9*350)) for i in range(1,301)])
def plan(question):
 if not isinstance(question,str) or not 3<=len(question)<=500:raise ValueError('Enter a question of 3–500 characters')
 q=question.lower().strip()
 if any(x in q for x in [';','--','/*']) or re.search(r'\b(drop|delete|insert|update|attach|pragma|alter|create)\b',q):raise ValueError('Only the documented read-only business questions are supported')
 if 'category' in q or 'categories' in q:return ('Revenue by category','SELECT category,ROUND(SUM(cents)/100.0,2) AS revenue_usd FROM orders GROUP BY category ORDER BY revenue_usd DESC',())
 if 'month' in q:return ('Revenue by month','SELECT month,ROUND(SUM(cents)/100.0,2) AS revenue_usd FROM orders GROUP BY month ORDER BY month',())
 if 'product' in q:
  match=re.search(r'\btop\s+(\d+)\b',q);limit=int(match.group(1)) if match else 5
  if not 1<=limit<=20:raise ValueError('Top product count must be 1–20')
  return ('Top products','SELECT product,ROUND(SUM(cents)/100.0,2) AS revenue_usd FROM orders GROUP BY product ORDER BY revenue_usd DESC,product LIMIT ?', (limit,))
 if 'average' in q or 'aov' in q:return ('Average order value','SELECT ROUND(AVG(cents)/100.0,2) AS average_order_usd FROM orders',())
 if 'count' in q or 'how many' in q:return ('Order count','SELECT COUNT(*) AS orders FROM orders',())
 raise ValueError('Unsupported question. Ask about category revenue, monthly revenue, top products, order count, or average order value.')
def execute(sql,params=(),path=DB):
 c=sqlite3.connect(Path(path).resolve().as_uri()+'?mode=ro',uri=True);c.row_factory=sqlite3.Row
 def authorize(action,a,b,database,trigger):
  if action==sqlite3.SQLITE_SELECT:return sqlite3.SQLITE_OK
  if action==sqlite3.SQLITE_READ:return sqlite3.SQLITE_OK if a=='orders' else sqlite3.SQLITE_DENY
  if action==sqlite3.SQLITE_FUNCTION:return sqlite3.SQLITE_OK if (b or '').lower() in ['sum','count','avg','round'] else sqlite3.SQLITE_DENY
  return sqlite3.SQLITE_DENY
 c.set_authorizer(authorize);steps=0
 def budget():
  nonlocal steps
  steps+=1;return int(steps>100)
 c.set_progress_handler(budget,1000)
 try:return [dict(x) for x in c.execute(sql,params).fetchmany(101)]
 finally:c.close()
def analyze(p):
 seed();intent,sql,params=plan(p.get('question','What is revenue by category?'));rows=execute(sql,params)
 if len(rows)>100:raise ValueError('Query exceeded row budget')
 bars=[dict(label=str(next(iter(x.values()))),value=x['revenue_usd']) for x in rows] if rows and 'revenue_usd' in rows[0] else []
 return dict(metrics={'Intent':intent,'Rows':len(rows),'Access':'read-only'},rows=rows,bars=bars,answer=sql,details={'parameters':params,'planner':'Deterministic intent grammar; no LLM','execution':'SQLite read-only URI, authorizer, instruction and row budgets'},notice='Synthetic sales data. This deliberately bounded interface rejects unsupported questions rather than guessing SQL.')
