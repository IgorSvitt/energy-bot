import sqlite3

class Orders:
    def __init__(self):
        self.conn = sqlite3.connect("db_data/energy.db")
        self.cur = self.conn.cursor()
        self.conn.commit()

    async def create_table(self):
        self.cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                good_id INTEGER,
                count INTEGER,
                date TEXT,
                FOREIGN KEY(user_id) REFERENCES users(user_id),
                FOREIGN KEY(good_id) REFERENCES goods(id)
                );
            '''
        )
        self.conn.commit()

    async def add_order(self, user_id, good_id, count, date):
        self.cur.execute(
            '''
            INSERT INTO orders (user_id, good_id, count, date) VALUES (?, ?, ?, ?)
            ''', (user_id, good_id, count, date)
        )
        self.conn.commit()
