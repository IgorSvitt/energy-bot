import sqlite3


class Goods:
    def __init__(self):
        self.conn = sqlite3.connect("db_data/energy.db")
        self.cur = self.conn.cursor()
        self.conn.commit()

    async def create_table(self):
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS goods (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL,
                count INTEGER,
                category_id INTEGER,
                description TEXT,
                photo_id TEXT,
                FOREIGN KEY(category_id) REFERENCES categories(id)
            );'''
        )
        self.conn.commit()

    async def get_by_category_id(self, category_id):
        self.cur.execute(
            f'''SELECT * FROM goods WHERE category_id = {category_id}'''
        )
        goods = self.cur.fetchall()
        return goods

    async def get_by_id(self, good_id):
        self.cur.execute(
            f'''SELECT * FROM goods WHERE id = {good_id}'''
        )
        good = self.cur.fetchone()
        return good

    async def get_all(self):
        self.cur.execute(
            '''SELECT * FROM goods'''
        )
        goods = self.cur.fetchall()
        return goods

    async def update_count(self, good_id, count):
        self.cur.execute(
            f'''UPDATE goods SET count = {count} WHERE id = {good_id}'''
        )
        self.conn.commit()

    async def update_price(self, good_id, price):
        self.cur.execute(
            f'''UPDATE goods SET price = {price} WHERE id = {good_id}'''
        )
        self.conn.commit()

    async def update_photo(self, good_id, photo_id):
        self.cur.execute(
            f'''UPDATE goods SET photo_id = "{photo_id}" WHERE id = {good_id}'''
        )
        self.conn.commit()

    async def update_description(self, good_id, description):
        self.cur.execute(
            f'''UPDATE goods SET description = "{description}" WHERE id = {good_id}'''
        )
        self.conn.commit()

    async def update_title(self, good_id, title):
        self.cur.execute(
            f'''UPDATE goods SET name = "{title}" WHERE id = {good_id}'''
        )
        self.conn.commit()

    async def update_category(self, good_id, category_id):
        self.cur.execute(
            f'''UPDATE goods SET category_id = {category_id} WHERE id = {good_id}'''
        )
        self.conn.commit()

    async def add(self, name, price, count, category_id, description, photo_id):
        self.cur.execute(
            f'''INSERT INTO goods (name, price, count, category_id, description, photo_id) VALUES
                ("{name}", {price}, {count}, {category_id}, "{description}", "{photo_id}")'''
        )
        self.conn.commit()

    async def delete(self, good_id):
        self.cur.execute(
            f'''DELETE FROM goods WHERE id = {good_id}'''
        )
        self.conn.commit()

    def __del__(self):
        self.conn.close()
