from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton
import logging
from pymongo import MongoClient
from ScheduleKPI_tgbot import config,func


connect_db = MongoClient('localhost', 27017)
db_schedule = connect_db[config.name_db]
logging.basicConfig(level=logging.INFO)

def start_markup():
    b1 = KeyboardButton('✏Вибрати групу')
    start_markup = ReplyKeyboardMarkup(resize_keyboard=True).add(b1)
    return start_markup
def create_main_markup():
    b1 = KeyboardButton('📜Розклад на сьогодні')
    b2 = KeyboardButton('Яка зараз пара❓')
    b3 = KeyboardButton('📜Розклад на завтра')
    b4 = KeyboardButton('📋Поточний тиждень')
    b5 = KeyboardButton('📚Повний розклад')
    b6 = KeyboardButton('📋Наступний тиждень')
    b7 = KeyboardButton('✏Змінити групу')
    b8 = KeyboardButton("📞Зв'язок з розробником")


    main_markup = ReplyKeyboardMarkup(resize_keyboard=True).row(b1,b2,b3).row(b4,b6).add(b5).row(b7,b8)
    return main_markup

bot = Bot(token=config.token)
dp = Dispatcher(bot)
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = db_schedule.users
    if user.find_one({'chat_id':'{}'.format(message.chat.id)}) == None:
        user.insert_one({'chat_id':'{}'.format(message.chat.id),
                          'full_name':'{}'.format(message.from_user.full_name),
                          'username':'{}'.format(message.from_user.username)})
    else:
        None


    await message.reply("Мої вітання, {}!👋🏻\n"
                        "Тисни 'Вибрати групу'👇🏻👇🏻👇🏻"
                        .format(message.from_user.full_name),reply_markup=start_markup())
@dp.message_handler(regexp='📜Розклад на сьогодні')
async def today(message: types.Message):
    statistics = db_schedule.statistics
    statistics.insert_one({'function':'{}'.format(message.text),
                       'chat_id':'{}'.format(message.chat.id),
                       'username':'{}'.format(message.from_user.username)})
    try:
        group = db_schedule.users.find_one({ "chat_id" : "{}".format(message.chat.id)})['group']
        msg = func.today(group, func.day_number(), func.week_number())

        await bot.send_message(message.chat.id,msg,parse_mode='HTML',reply_markup=create_main_markup())
    except:
        msg = '<code>Спочатку виберіть свою групу</code>'
        await bot.send_message(message.chat.id,msg,parse_mode='HTML',reply_markup=create_main_markup())
@dp.message_handler(regexp='Яка зараз пара❓')
async def now(message: types.Message):
    statistics = db_schedule.statistics
    statistics.insert_one({'function':'{}'.format(message.text),
                       'chat_id':'{}'.format(message.chat.id),
                       'username':'{}'.format(message.from_user.username)})
    try:
        group = db_schedule.users.find_one({ "chat_id" : "{}".format(message.chat.id)})['group']
        msg = func.get_now_lesson(group, func.day_number(), func.week_number())
        await bot.send_message(message.chat.id,msg,parse_mode='HTML',reply_markup=create_main_markup())
    except:
        msg = '<code>Спочатку виберіть свою групу</code>'
        await bot.send_message(message.chat.id,msg,parse_mode='HTML',reply_markup=create_main_markup())
@dp.message_handler(regexp='📜Розклад на завтра')
async def tomorrow(message: types.Message):
    statistics = db_schedule.statistics
    statistics.insert_one({'function':'{}'.format(message.text),
                       'chat_id':'{}'.format(message.chat.id),
                       'username':'{}'.format(message.from_user.username)})
    try:
        group = db_schedule.users.find_one({ "chat_id" : "{}".format(message.chat.id)})['group']
        day_number = func.day_number()
        week_number = func.week_number()
        if day_number == 7:
            day_number = 1
            if week_number == 1:
                week_number = 2
            else:
                week_number = 1
        else:
            day_number = day_number+1
        msg = func.today(group, day_number, week_number)
        await bot.send_message(message.chat.id,msg,parse_mode='HTML',reply_markup=create_main_markup())
    except:
        msg = '<code>Спочатку виберіть свою групу</code>'
        await bot.send_message(message.chat.id,msg,parse_mode='HTML',reply_markup=create_main_markup())
@dp.message_handler(regexp='📋Поточний тиждень')
async def week(message: types.Message):
    statistics = db_schedule.statistics
    statistics.insert_one({'function':'{}'.format(message.text),
                       'chat_id':'{}'.format(message.chat.id),
                       'username':'{}'.format(message.from_user.username)})
    try:
        group = db_schedule.users.find_one({ "chat_id" : "{}".format(message.chat.id)})['group']
        msg = func.get_one_week(group, func.week_number())
        await bot.send_message(message.chat.id,msg,parse_mode='HTML',reply_markup=create_main_markup())
    except:
        msg = '<code>Спочатку виберіть свою групу</code>'
        await bot.send_message(message.chat.id,msg,parse_mode='HTML',reply_markup=create_main_markup())
@dp.message_handler(regexp='📚Повний розклад')
async def all(message: types.Message):
    statistics = db_schedule.statistics
    statistics.insert_one({'function':'{}'.format(message.text),
                       'chat_id':'{}'.format(message.chat.id),
                       'username':'{}'.format(message.from_user.username)})
    try:
        group = db_schedule.users.find_one({ "chat_id" : "{}".format(message.chat.id)})['group']
        week1 = func.get_one_week(group, 1)
        week2 = func.get_one_week(group, 2)
        msg = "<i>Тиждень 1</i>\n"+week1+"<i>Тиждень 2</i>\n"+week2
        await bot.send_message(message.chat.id,msg,parse_mode='HTML',reply_markup=create_main_markup())
    except:
        msg = '<code>Спочатку виберіть свою групу</code>'
        await bot.send_message(message.chat.id,msg,parse_mode='HTML',reply_markup=create_main_markup())
@dp.message_handler(regexp='📋Наступний тиждень')
async def week(message: types.Message):
    statistics = db_schedule.statistics
    statistics.insert_one({'function':'{}'.format(message.text),
                       'chat_id':'{}'.format(message.chat.id),
                       'username':'{}'.format(message.from_user.username)})
    if func.week_number() == 1:
        week = 2
    elif func.week_number() == 2:
        week = 1
    try:

        group = db_schedule.users.find_one({ "chat_id" : "{}".format(message.chat.id)})['group']
        msg = func.get_one_week(group, week)
        await bot.send_message(message.chat.id,msg,parse_mode='HTML',reply_markup=create_main_markup())
    except:
        msg = '<code>Спочатку виберіть свою групу</code>'
        await bot.send_message(message.chat.id,msg,parse_mode='HTML',reply_markup=create_main_markup())
@dp.message_handler(lambda message: message.text == '✏Вибрати групу' or message.text == '✏Змінити групу')
async def chose_group(message: types.Message):
    await message.reply("Пиши: /set номер_групи\n"
                        "Приклад: /set ік-52")
@dp.message_handler(commands=['set'])
async def set_group(message: types.Message):

    try:
        _, group = message.text.lower().split(' ')
        groups = db_schedule.groups.find_one({ "group_full_name" : "{}".format(group)})['group_id']
        user = db_schedule.users
        user.update_one({'chat_id':'{}'.format(message.chat.id)},{"$set":{'group':'{}'.format(groups)}})
        msg = "Готово!\nПриємного користування:)"
        db_schedule.set_log.insert_one({'mesage':'{}'.format(message.text),
                          'answer':'True',
                          'username':'{}'.format(message.from_user.username)})
        await message.reply(msg,reply_markup=create_main_markup())
    except:
        msg = "Упс, група не існує❌"
        db_schedule.set_log.insert_one({'mesage':'{}'.format(message.text),
                          'answer':'False',
                          'username':'{}'.format(message.from_user.username)})
        await message.reply(msg,reply_markup=create_main_markup())
@dp.message_handler(regexp="📞Зв'язок з розробником")
async def contacts(message: types.Message):
    msg = "Є запитання/пропозиції?\nТобі сюди: @geek_ua"
    await bot.send_message(message.chat.id,msg,parse_mode='HTML',reply_markup=create_main_markup())
if __name__ == '__main__':
    executor.start_polling(dp)
