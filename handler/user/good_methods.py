from aiogram.utils.media_group import MediaGroupBuilder

from db import db_goods, db_categories, db_orders, db_users


db_goods = db_goods.Goods()
db_categories = db_categories.Categories()
db_orders = db_orders.Orders()
db_users = db_users.Users()


async def get_category():
    categories = await db_categories.get_all()
    return categories


async def get_goods(category_id):
    goods = await db_goods.get_by_category_id(category_id)
    text = ""
    album = MediaGroupBuilder()
    for good in goods:
        if good[3] > 0:
            text += f"<b>{good[1]}</b> {good[5]}| {good[2]} руб/шт |В наличие {good[3]} шт.\n"
            album.add_photo(media=good[6])

    if text == "":
        text = "Товаров в данной категории нет"
        return text, None

    return text, album


async def get_goods_for_sell(category_id):
    goods = await db_goods.get_by_category_id(category_id)
    return goods


async def get_good_for_sell(good_id):
    good = await db_goods.get_by_id(good_id)
    text = f'''<b>Наименование:</b> <code>{good[1]}</code>\n<b>Описание:</b> {good[5]}\n<b>Цена:</b> <code>{good[2]} руб/шт</code>\n<b>В наличии:</b> <code>{good[3]} шт</code>\n<b>Минимальное количество к покупке:</b> <code>1 шт</code>\n\n<b>Для покупки введите необходимое количество или выберите ниже</b>'''
    return text


async def get_good_count(good_id):
    print(good_id)
    good = await db_goods.get_by_id(good_id)
    print(good)
    return good[3]


async def check_info(id, count, room):
    good = await db_goods.get_by_id(id)
    price = good[2]
    title = good[1]
    text = f"Вы хотите купить <code>{title}</code> в количестве <code>{count}</code> шт. на сумму <code>{count * price}</code> руб. с доставкой в <code>{room}</code>?"
    return text


async def write_order(user_id, good_id, count):
    from datetime import datetime
    now = datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")
    await update_good_count(good_id, count)
    await update_count_orders(user_id, count)
    await db_orders.add_order(user_id, good_id, count, date)


async def update_good_count(good_id, buy_count):
    good = await db_goods.get_by_id(good_id)
    count = good[3] - buy_count
    await db_goods.update_count(good_id, count)


async def update_count_orders(user_id, buy_count):
    count = await db_users.get_count_orders(user_id)
    new_count = count + buy_count
    await db_users.update_count_orders(user_id, new_count)
