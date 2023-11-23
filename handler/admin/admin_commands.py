from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import ADMINS
from state.energy import Good, UpdateCountGood, DeleteGood, Mailing, Category, DeleteCategory
from db import db_users, db_goods, db_orders, db_categories

router = Router()
db_users = db_users.Users()
db_goods = db_goods.Goods()
db_orders = db_orders.Orders()
db_categories = db_categories.Categories()


@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    if message.from_user.username in ADMINS:
        await state.clear()
        await message.answer("Вы отменили действие")
    else:
        await message.answer("У вас нет доступа к этой команде")


@router.message(Command("add"))
async def add(message: Message, state: FSMContext):
    if message.from_user.username in ADMINS:
        await message.answer("Введите название товара")
        await state.set_state(Good.GET_TITLE)
    else:
        await message.answer("У вас нет доступа к этой команде")


@router.message(Command("get"))
async def check(message: Message):
    if message.from_user.username in ADMINS:
        goods = await db_goods.get_all()
        text = ""
        for item in goods:
            text = text + f"{item[0]} | {item[1]} {item[5]} | {item[2]} руб/шт | В наличии: {item[3]} шт. \n"
        await message.answer("Вот что у нас есть в наличии:\n\n" + text + "\n\n Всего товаров: " + str(len(goods)))
    else:
        await message.answer("У вас нет доступа к этой команде")


@router.message(Command("updatecount"))
async def change(message: Message, state: FSMContext):
    if message.from_user.username in ADMINS:
        await message.answer("Введите Id товара, который хотите изменить")
        await state.set_state(UpdateCountGood.GET_ID)
    else:
        await message.answer("У вас нет доступа к этой команде")


@router.message(Good.GET_TITLE)
async def get_title(message: Message, state: FSMContext):
    title = message.text
    await state.update_data(title=title)
    await message.answer("Введите описание товара")
    await state.set_state(Good.GET_DESCRIPTION)


@router.message(Good.GET_DESCRIPTION)
async def get_description(message: Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    await message.answer("Введите количество товара")
    await state.set_state(Good.GET_COUNT)


@router.message(Good.GET_COUNT)
async def get_count(message: Message, state: FSMContext):
    count = message.text
    await state.update_data(count=count)
    await message.answer("Введите цену товара")
    await state.set_state(Good.GET_PRICE)


@router.message(Good.GET_PRICE)
async def get_price(message: Message, state: FSMContext):
    price = message.text
    await state.update_data(price=price)
    await message.answer("Введите id категории товара")
    await state.set_state(Good.GET_CATEGORYID)


@router.message(Good.GET_CATEGORYID)
async def get_categoryid(message: Message, state: FSMContext):
    category_id = message.text
    await state.update_data(category_id=category_id)
    await message.answer("Введите ссылку на фото товара")
    await state.set_state(Good.GET_PHOTO)


@router.message(Good.GET_PHOTO)
async def get_photo(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(photo=message.text)
    await state.update_data(photo=message.text)
    data = await state.get_data()
    title = data.get("title")
    description = data.get("description")
    count = data.get("count")
    price = data.get("price")
    photo = data.get("photo")
    category_id = data.get("category_id")
    await db_goods.add(name=title, count=count, price=price, description=description, photo_id=photo,
                       category_id=category_id)
    try:
        await message.answer("Товар добавлен")
    except Exception as e:
        await message.answer("Товар не добавлен")
    await state.clear()


@router.message(UpdateCountGood.GET_ID)
async def get_id(message: Message, state: FSMContext):
    id = message.text
    await state.update_data(id=id)
    await message.answer("Введите количество напитка")
    await state.set_state(Good.CHANGE_COUNT)


@router.message(Good.CHANGE_COUNT)
async def change_count(message: Message, state: FSMContext):
    count = int(message.text)
    await state.update_data(count=count)
    data = await state.get_data()
    id = data.get("id")
    count = data.get("count")
    await db_goods.update_count(id, count)
    await message.answer("Количество напитка изменено")
    await state.clear()


@router.message(Command("getusers"))
async def get_users(message: Message):
    if message.from_user.username in ADMINS:
        users = await db_users.get_all()
        text = ""
        for item in users:
            text = text + f"{item[0]} | @{item[1]} | Кол-во покупок: {item[2]}\n"
        await message.answer("Вот все пользователи:\n\n" + text + "\n\n Всего пользователей: " + str(len(users)))
    else:
        await message.answer("У вас нет доступа к этой команде")


@router.message(Command("delete"))
async def delete(message: Message, state: FSMContext):
    if message.from_user.username in ADMINS:
        await message.answer("Введите Id напитка, который хотите удалить")
        await state.set_state(DeleteGood.GET_ID)
    else:
        await message.answer("У вас нет доступа к этой команде")


@router.message(DeleteGood.GET_ID)
async def delete_id(message: Message, state: FSMContext):
    id = message.text
    await state.update_data(id=int(id))
    data = await state.get_data()
    id = data.get("id")
    await db_goods.delete(id)
    await message.answer("Напиток удален")
    await state.clear()


@router.message(Command("addcategory"))
async def add_category(message: Message, state: FSMContext):
    if message.from_user.username in ADMINS:
        await message.answer("Введите название категории")
        await state.set_state(Category.GET_TITLE)
    else:
        await message.answer("У вас нет доступа к этой команде")


@router.message(Category.GET_TITLE)
async def get_title(message: Message, state: FSMContext):
    title = message.text
    await state.update_data(title=title)
    data = await state.get_data()
    title = data.get("title")
    await db_categories.add(title)
    await message.answer("Категория добавлена")
    await state.clear()


@router.message(Command("getcategories"))
async def get_categories(message: Message):
    if message.from_user.username in ADMINS:
        categories = await db_categories.get_all()
        text = ""
        for item in categories:
            text = text + f"{item[0]} | {item[1]}\n"
        await message.answer("Вот все категории:\n\n" + text + "\n\n Всего категорий: " + str(len(categories)))
    else:
        await message.answer("У вас нет доступа к этой команде")


@router.message(Command("deletecategory"))
async def delete_category(message: Message, state: FSMContext):
    if message.from_user.username in ADMINS:
        await message.answer("Введите Id категории, которую хотите удалить")
        await state.set_state(DeleteCategory.GET_ID)
    else:
        await message.answer("У вас нет доступа к этой команде")


@router.message(DeleteCategory.GET_ID)
async def delete_id(message: Message, state: FSMContext):
    id = message.text
    await state.update_data(id=int(id))
    data = await state.get_data()
    id = data.get("id")
    await db_categories.delete(id)
    await message.answer("Категория удалена")
    await state.clear()


# @router.message(Command('mailing'))
# async def mailing(message: Message, state: FSMContext):
#     if message.from_user.username in ADMINS:
#         await message.answer('Введите текст рассылки')
#         await state.set_state(Mailing.GET_TEXT)
#     else:
#         await message.answer("У вас нет доступа к этой команде")
#
#
# @router.message(Mailing.GET_TEXT)
# async def get_text(message: Message, state: FSMContext):
#     text = message.text
#     await state.update_data(text=text)
#     await message.answer('Введите фото')
#     await state.set_state(Mailing.GET_PHOTO)
#
#
# @router.message(Mailing.GET_PHOTO)
# async def get_photo(message: Message, state: FSMContext, bot: Bot):
#     users = await db_users.get()
#     print(users)
#     if message.text == "no":
#         data = await state.get_data()
#         text = data.get("text")
#         for user in users:
#             try:
#                 await bot.send_message(user[0], text)
#             except:
#                 pass
#
#     await state.clear()


@router.message(Command("addusers"))
async def add_users(message: Message, state: FSMContext):
    users = [
        {'userid': 176653910, 'username': '@lomatoff'},
        {'userid': 263185439, 'username': '@sumingson'},
        {'userid': 278432261, 'username': '@polinabaz'},
        {'userid': 317033699, 'username': '@eliaaah'},
        {'userid': 333697317, 'username': '@MiLord322'},
        {'userid': 335672439, 'username': '@vmoshikova'},
        {'userid': 379181013, 'username': '@coldoglikebee'},
        {'userid': 398969406, 'username': '@sashullel'},
        {'userid': 403062158, 'username': '@alomatov'},
        {'userid': 418849724, 'username': '@ivanstasevich'},
        {'userid': 419672615, 'username': '@lincentpega'},
        {'userid': 420923585, 'username': '@ddinarrrr'},
        {'userid': 432188597, 'username': '@nik0laevig0r'},
        {'userid': 433598410, 'username': '@bihemia'},
        {'userid': 458200036, 'username': '@vadyukkha'},
        {'userid': 495280201, 'username': '@aanefedovv'},
        {'userid': 518899252, 'username': '@lit_trog_project'},
        {'userid': 574747511, 'username': '@whncrwstrtm'},
        {'userid': 584320307, 'username': '@crabstickss'},
        {'userid': 592465853, 'username': '@Aigerim_Murzakanova'},
        {'userid': 594521251, 'username': '@abdul_1109'},
        {'userid': 598928947, 'username': '@KersolWis'},
        {'userid': 628113442, 'username': '@reevolutiiion'},
        {'userid': 652552734, 'username': '@watercolourblue'},
        {'userid': 678879883, 'username': '@ttdddl'},
        {'userid': 711733487, 'username': '@LizB1106'},
        {'userid': 740855159, 'username': '@Shashmura'},
        {'userid': 741040495, 'username': '@kamawwanai'},
        {'userid': 753970613, 'username': '@dorishhh'},
        {'userid': 777199643, 'username': '@notkana'},
        {'userid': 781603680, 'username': '@dontgettoocloseitisdarkinside'},
        {'userid': 811516472, 'username': '@ekaterina_hom'},
        {'userid': 814405139, 'username': '@Dashkere2005'},
        {'userid': 827241960, 'username': '@arsmll'},
        {'userid': 836918131, 'username': '@vsplak8'},
        {'userid': 846297760, 'username': '@g_safinaa'},
        {'userid': 847538904, 'username': '@timuruzakbaev'},
        {'userid': 854547636, 'username': '@None'},
        {'userid': 863589322, 'username': '@Vse_imena_zanyaty_pidorasy'},
        {'userid': 870606533, 'username': '@ssowru'},
        {'userid': 870890087, 'username': '@zarretsskaya'},
        {'userid': 886433207, 'username': '@lizareinfi'},
        {'userid': 893901104, 'username': '@RiinaAriina'},
        {'userid': 895600335, 'username': '@Kdnzm'},
        {'userid': 907781657, 'username': '@kirchsss'},
        {'userid': 908526211, 'username': '@blynchek'},
        {'userid': 915412484, 'username': '@weeq123'},
        {'userid': 931017033, 'username': '@kulebyaka1'},
        {'userid': 936308342, 'username': '@vrchns'},
        {'userid': 980705481, 'username': '@frostikamya'},
        {'userid': 985901502, 'username': '@drunkvermicelli'},
        {'userid': 991515932, 'username': '@iamnotlera'},
        {'userid': 1000331130, 'username': '@Batko_Mahnoo'},
        {'userid': 1002134918, 'username': '@xramokkk'},
        {'userid': 1005026088, 'username': '@ksenniaksen'},
        {'userid': 1054523993, 'username': '@AlexandraDav18'},
        {'userid': 1064084693, 'username': '@ivdarin'},
        {'userid': 1075868597, 'username': '@ek_zhuickova'},
        {'userid': 1088964094, 'username': '@hse_slave'},
        {'userid': 1094011521, 'username': '@beskonechnaya_pauza'},
        {'userid': 1095237731, 'username': '@alenasinsav'},
        {'userid': 1116717403, 'username': '@ssuunraayyy'},
        {'userid': 1120563749, 'username': '@KforestChan'},
        {'userid': 1133023911, 'username': '@lisssaolesya20'},
        {'userid': 1158553044, 'username': '@sk74453'},
        {'userid': 1183531666, 'username': '@Sonenka0'},
        {'userid': 1206969232, 'username': '@sa_vlr'},
        {'userid': 1218574768, 'username': '@ppponchichek'},
        {'userid': 1222875288, 'username': '@immedeg'},
        {'userid': 1228035769, 'username': '@polintyyssss'},
        {'userid': 1232646731, 'username': '@fadedhappiness'},
        {'userid': 1307748495, 'username:': '@wtfwithname'},
        {'userid': 1319061322, 'username': '@maksmolch'},
        {'userid': 1331692828, 'username': '@None'},
        {'userid': 1440016079, 'username': '@RuKatvorec'},
        {'userid': 1525517758, 'username': '@courtoise'},
        {'userid': 1534872106, 'username': '@neperestupai'},
        {'userid': 1541557076, 'username': '@miirabelle'},
        {'userid': 1765527168, 'username': '@alinochka05'},
        {'userid': 1990661074, 'username': '@maksim_dostovalov'},
        {'userid': 1991070195, 'username': '@nuzhdina_alena'},
        {'userid': 2101194522, 'username': '@vsevolodpapin'},
        {'userid': 5003511058, 'username': '@Aveshik'},
        {'userid': 5023323379, 'username': '@m_gootze'},
        {'userid': 5060226866, 'username': '@iam_zmm'},
        {'userid': 5965451035, 'username': '@theghostofyouuu'},
        {'userid': 6624329021, 'username': '@yalakovaal'}
    ]
    for user in users:
        try:
            await db_users.add(user['userid'], user['username'], 0, True)
        except:
            print(user)
