#! /usr/bin/python
# -*- coding: UTF-8 -*-

#
# Small script to show PostgresSQL and Pyscopg together
#

import psycopg2

try:
    conn = psycopg2.connect("dbname='test' user='postgres' host='localhost' password='wanggang'")
except:
    print 'I am unable to connect to the database'

cur = conn.cursor()

cur.execute("""SELECT * FROM test.user""")
rows = cur.fetchall()
print '\n rows', cur.rowcount, '\n'
print '\nShow me the database:\n'
for row in rows:
    print '   ', row

