#!/usr/bin/env python3

import sqlite3
from contextlib import closing
from objects import Session

conn = None
def connect():
    global conn
    if not conn:
        conn = sqlite3.connect("session_db.sqlite")
        conn.row_factory = sqlite3.Row

def close():
    if conn:
        conn.close()

def create_session():
    query = '''CREATE TABLE IF NOT EXISTS Session (sessionID INTEGER PRIMARY KEY,
        startTime TEXT, startMoney REAL, stopTime TEXT, stopMoney REAL);'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        conn.commit()
    last_Session = get_last_session()
    if last_Session == None:
        query = '''INSERT INTO Session (sessionID, startTime, startMoney, stopTime, stopMoney)
            VALUES (0, 'x', 199, 'y', 199);'''
        with closing(conn.cursor()) as c:
            c.execute(query)
            conn.commit()
    else:
        pass

def make_session(row):
    return Session(row["sessionID"],row["startTime"],row["startMoney"],row["stopTime"],row["stopMoney"])

def get_last_session():
    query = '''SELECT * FROM Session ORDER BY sessionID DESC;'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        row = c.fetchone()
    if row == None:
        return None
    else:
        return make_session(row)

def add_session(s):
    query = '''INSERT INTO Session (sessionID, startTime, startMoney, stopTime, stopMoney)
        VALUES (?, ?, ?, ?, ?);'''
    with closing(conn.cursor()) as c:
            c.execute(query,(s.sessionID,s.startTime,float(s.startMoney),s.stopTime,float(s.stopMoney)))
            conn.commit()

def main():
    connect()
    create_session()
    session = get_last_session()
    print("Money:", session.stopMoney)
    close()

if __name__ == "__main__":
    main()
    
