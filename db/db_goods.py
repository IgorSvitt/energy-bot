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

    async def create_test_data(self):
        self.cur.execute(
            '''INSERT INTO goods (name, price, count, category_id, description, photo_id) VALUES ("Тестовый товар", 100, 10, 1, "Тестовое описание", "https://yandex-images.clstorage.net/9GIx83k50/d12552Yj3k/gmPOxsJ-V-ErSl6Zd_8VrmosNEGAHPeuMx1IEVTSqx9bSr7uXRXd8fHTk9X_4pYFOzij3sMhXUbeyNYr13sm5JdjjoqBPU29fAlE1Tv4HKp1ZykJgFvr_DgKU0IPmqBIB0i0iDVl_4Gb-aOojZrsT2Iwoo6LOEwEs6XOJPI1W-GMRuPrw38rzRVAI5db1R6Ma3QrXKdg6_0uMB1uN6zXU1gBzpsOZvGQj9mhuZC98UxGJqyegX9xIZWZuznxDEjTu03vztNYDMcWXwaDWPA7u19SKm65YNrADC4hawS-70VdDdanOGvUrJPGpYmskdJzRwu3k5dgaCuIr6s59hhKwrh17O_DSBrNO18xgVjSHr19RzRnmEPG8Bg_Omc7o9h3ViDemQJ325mLz4S3nbrRZHYMg4GfRl8XjY2gB-QEZcaESP7t21871hVNB5V96Da4cWc4Uo1D7-YfISR3JoXTTm0r6bUycciRoP-whb2n53t7O7WGgEJ2BaOZmSv2JFvdh0nI7tl-DO45SSSPf8EHmktoDk6Hfcv-GwsXZga8yk90PuyCIWvXgrTTtK2plcdySBaikpt0cBi1qoE19BVwxJhz0cPBfBX6AVoIuEPHFJ11WxlJgUL55BA1L3MWs91QTDbXlTJK-Kis77CZsKLudEwyko25e08CoLubCtYVc9CQUvjS9V0X2zhwOKR80B-Pf0UuZq1779YzPA9bDJz3b2wL0ockbsSAqPSJlq6g73FJCaCnvntaB5uTiinRDmjCkFfzzfNfGsM8SBqVQdk2r1ZuFUmlVeTrEwMNUySrz1R9G_aBJm_qgoL6tZaNvcdBSxK1jr1wXDSYs7Y-1ihl7J5n3sDodRP6OnoTtWL3NJ9nYzxApEnO2yAAA00AntNEYhDMtih-5LCW-L-vibHqZFQoqqWgeFMriouUBeAZSOCSc9nt_XgW1jtYBLd4xwWvYm4Md7pk3fs_IyV2MoI")'''
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
