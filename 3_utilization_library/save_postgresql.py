import os
import psycopg2

conn = psycopg2.connect(os.environ['PSQL_DB_CONNECT'])

c = conn.cursor()

c.execute('DROP TABLE IF EXISTS cities')
c.execute('CREATE TABLE cities(rank integer, city text, population integer)')
c.execute('INSERT INTO cities VALUES(%s, %s, %s)', (1, '上海', 24_150_000))
c.execute('INSERT INTO cities VALUES(%(rank)s, %(city)s, %(population)s)', {'rank': 2, 'city': 'カラチ', 'population': 23_500_000})
c.executemany('INSERT INTO cities VALUES (%(rank)s, %(city)s, %(population)s)',[
    {'rank': 3, 'city': '北京', 'population': 21_516_000},
    {'rank': 4, 'city': '天津', 'population': 14_722_100},
    {'rank': 5, 'city': 'イスタンブル', 'population': 14_160_467}
])

conn.commit()

c.execute('SELECT * FROM cities')

for row in c.fetchall():
    print(row)

conn.close()

