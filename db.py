import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("db_data/energy.db")
        self.cur = self.conn.cursor()
        self.conn.commit()

    async def create_table(self):
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS energetics"
            " (id INTEGER PRIMARY KEY, title text, count integer, price integer, description text)")
        self.conn.commit()

    async def get(self):
        self.cur.execute("SELECT * FROM energetics")
        rows = self.cur.fetchall()
        return rows

    async def get_by_id(self, id):
        self.cur.execute("SELECT * FROM energetics WHERE id=?", (id,))
        rows = self.cur.fetchall()
        return rows

    async def update_count(self, id, count):
        self.cur.execute("UPDATE energetics SET count = ? WHERE id = ?", (count, id))
        self.conn.commit()

    async def add(self, title, count, price, description, photo):
        self.cur.execute("INSERT INTO energetics VALUES (NULL, ?, ?, ?, ?, ?)",
                         (title, count, price, description, photo))
        self.conn.commit()

    async def delete(self, id):
        self.cur.execute("DELETE FROM energetics WHERE id=?", (id,))
        self.conn.commit()

    async def update(self, id, title, count, price, description):
        self.cur.execute("UPDATE energetics SET title = ?, count = ?, price = ?, description = ? WHERE id = ?",
                         (title, count, price, description, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
