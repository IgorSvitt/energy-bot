import sqlite3


class Users:
    def __init__(self):
        self.conn = sqlite3.connect("db_data/energy.db")
        self.cur = self.conn.cursor()
        self.conn.commit()

    async def create_table(self):
        self.cur.execute(
            '''
                CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                count_orders INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 0
                );
            '''
        )
        self.conn.commit()

    async def add(self, userid, name, count_orders, is_active):
        self.cur.execute(
            '''
                INSERT INTO users (user_id, username, count_orders, is_active) VALUES (?, ?, ?, ?)
            ''', (userid, name, count_orders, is_active)
        )
        self.conn.commit()

    async def get_by_id(self, userid):
        self.cur.execute(
            '''
                SELECT * FROM users WHERE user_id = ?
            ''', (userid,)
        )
        return self.cur.fetchone()

    async def update_count_orders(self, userid, count_orders):
        self.cur.execute(
            '''
                UPDATE users SET count_orders = ? WHERE user_id = ?
            ''', (count_orders, userid)
        )
        self.conn.commit()

    async def get_count_orders(self, userid):
        self.cur.execute(
            '''
                SELECT count_orders FROM users WHERE user_id = ?
            ''', (userid,)
        )
        return self.cur.fetchone()[0]

    async def get_all(self):
        self.cur.execute(
            '''
                SELECT * FROM users
            '''
        )
        return self.cur.fetchall()

    async def update_active(self, userid, is_active):
        self.cur.execute(
            '''
                UPDATE users SET is_active = ? WHERE user_id = ?
            ''', (is_active, userid)
        )
        self.conn.commit()
