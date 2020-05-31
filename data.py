import sqlite3
import app


class Data:
    data_file = 'data/data.db'

    def __init__(self):
        self.conn = sqlite3.connect(self.data_file)
        self.init()

    def init(self):
        c = self.conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS logs
            (id integer primary key, windowtitle text, cmdline text, screenshot text, logtime text)
        """)

    def insert(self, le: app.LogEntry):
        print("inserting into database...")
        c = self.conn.cursor()
        row = (le.title, le.cmdline, le.screenshot_filename)
        c.execute("INSERT INTO logs (windowtitle,cmdline,screenshot,logtime) VALUES(?,?,?, datetime('now', 'localtime'))", row)
        self.conn.commit()

