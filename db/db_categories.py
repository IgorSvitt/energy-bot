import sqlite3


class Categories:
    def __init__(self):
        self.conn = sqlite3.connect("db_data/energy.db")
        self.cur = self.conn.cursor()
        self.conn.commit()

    async def create_table(self):
        self.cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
                );
            '''
        )
        self.conn.commit()

    async def get_all(self):
        self.cur.execute(
            '''SELECT * FROM categories'''
        )
        return self.cur.fetchall()

    async def add(self, id):
        self.cur.execute(
            '''INSERT INTO categories (name) VALUES (?)''', (id,)
        )
        self.conn.commit()

    async def delete(self, id):
        self.cur.execute(
            '''DELETE FROM categories WHERE id = (?)''', (id,)
        )
        self.conn.commit()

    def __del__(self):
        self.conn.close()
