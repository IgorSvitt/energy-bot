import sqlite3


class DatabaseUsers:
    def __init__(self):
        self.conn = sqlite3.connect("db_data/users.db")
        self.cur = self.conn.cursor()
        self.conn.commit()

    async def create_table(self):
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users"
            " (userid INTEGER PRIMARY KEY, name username)")
        self.conn.commit()

    async def get(self):
        self.cur.execute("SELECT * FROM users")
        rows = self.cur.fetchall()
        return rows

    async def get_by_id(self, userid):
        self.cur.execute("SELECT * FROM users WHERE userid=?", (userid,))
        rows = self.cur.fetchall()
        return rows

    async def add(self, userid, name):
        self.cur.execute("INSERT INTO users VALUES (?, ?)",
                         (userid, name))
        self.conn.commit()

    async def delete(self, userid):
        self.cur.execute("DELETE FROM users WHERE userid=?", (userid,))
        self.conn.commit()

