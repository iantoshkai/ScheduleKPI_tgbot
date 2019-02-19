from pymongo import MongoClient
from datetime import datetime
from schedule_kpi import config

connect_db = MongoClient('localhost', 27017)
#подключение к бд
db_schedule = connect_db[config.name_db]
def get_now_lesson_number():
    now_time = int(get_date_now().strftime('%H%M'))
    if now_time in range(830,1000):        #
        lesson_number = '1'
    elif now_time in range(1025,1155):     #
        lesson_number = '2'
    elif now_time in range(1220,1350):     #
        lesson_number = '3'
    elif now_time in range(1415,1545):     #
        lesson_number = '4'
    elif now_time in range(1610,1805):     #
        lesson_number = '5'
    else:
        return None
    return lesson_number
def get_date_now():
    return datetime.now()
def week_number():
    if int(get_date_now().strftime('%W'))%2>0:
        return 2
    else:
        return 1
def day_number():
    return get_date_now().isoweekday()
def today(group,day_number,lesson_week):
    collection = db_schedule['{}'.format(group)]
    schedule = collection.find({'day_number': '{}'.format(day_number),
                                'lesson_week': '{}'.format(lesson_week)})
    send_schedule = ''
    try:
        day_name = schedule[0]['day_name']
        send_schedule = '<b>{}</b>\n'.format(day_name)
        for lesson in schedule:
            lesson_number = lesson['lesson_number']
            lesson_name = lesson['lesson_name']
            lesson_room = lesson['lesson_room']
            lesson_type = lesson['lesson_type']
            teacher_name = lesson['teacher_name']
            teacher_url = lesson['teachers'][0]['teacher_url']
            send_schedule +='{}. {}\n<pre>{} {} </pre>\n<a href="{}">{}</a>\n'.format(lesson_number,
                                                                                     lesson_name,
                                                                                     lesson_room,
                                                                                     lesson_type,
                                                                                     teacher_url,
                                                                                     teacher_name)
        return send_schedule
    except IndexError:
        send_schedule += 'Немає пар, відпочивай😎'
        return send_schedule
def tommorow(group,day_number,lesson_week):
    if day_number == 7:
        day_number = 1
    else:
        day_number = day_number+1
    collection = db_schedule['{}'.format(group)]
    schedule = collection.find({'day_number': '{}'.format(day_number),
                                'lesson_week': '{}'.format(lesson_week)})
    send_schedule = ''
    try:
        day_name = schedule[0]['day_name']
        send_schedule = '<b>{}</b>\n'.format(day_name)
        for lesson in schedule:
            lesson_number = lesson['lesson_number']
            lesson_name = lesson['lesson_name']
            lesson_room = lesson['lesson_room']
            lesson_type = lesson['lesson_type']
            teacher_name = lesson['teacher_name']
            teacher_url = lesson['teachers'][0]['teacher_url']
            send_schedule +='{}. {}\n<pre>{} {} </pre>\n<a href="{}">{}</a>\n'.format(lesson_number,
                                                                                     lesson_name,
                                                                                     lesson_room,
                                                                                     lesson_type,
                                                                                     teacher_url,
                                                                                     teacher_name)
        return send_schedule
    except IndexError:
        send_schedule += 'Немає пар, відпочивай😎'
        return send_schedule
def get_one_week(group,lesson_week):
    collection = db_schedule['{}'.format(group)]
    send_schedule = ''
    for num in range(1,8):
        schedule = collection.find({'day_number':'{}'.format(num),
                                    'lesson_week':'{}'.format(lesson_week)})
        try:
            day_name = schedule[0]['day_name']
            send_schedule += '<b>{}</b>\n'.format(day_name)
            for lesson in schedule:
                lesson_number = lesson['lesson_number']
                lesson_name = lesson['lesson_name']
                lesson_room = lesson['lesson_room']
                lesson_type = lesson['lesson_type']
                teacher_name = lesson['teacher_name']
                teacher_url = lesson['teachers'][0]['teacher_url']
                send_schedule +='{}. {}\n<pre>{} {} </pre>\n<a href="{}">{}</a>\n'.format(lesson_number,
                                                                                         lesson_name,
                                                                                         lesson_room,
                                                                                         lesson_type,
                                                                                         teacher_url,
                                                                                         teacher_name)

        except IndexError:
            continue
    return send_schedule
def get_now_lesson(group,day_number,lesson_week):
    lesson_number = get_now_lesson_number()
    send_schedule = ''
    collection = db_schedule['{}'.format(group)]
    lesson = collection.find_one({'day_number': '{}'.format(day_number),
                                'lesson_week': '{}'.format(lesson_week),
                                'lesson_number':'{}'.format(lesson_number)})
    try:
        lesson_name = lesson['lesson_name']
        lesson_room = lesson['lesson_room']
        lesson_type = lesson['lesson_type']
        teacher_name = lesson['teacher_name']
        teacher_url = lesson['teachers'][0]['teacher_url']
        send_schedule ='{}. {}\n<pre>{} {} </pre>\n<a href="{}">{}</a>\n'.format(lesson_number,
                                                                                 lesson_name,
                                                                                 lesson_room,
                                                                                 lesson_type,
                                                                                 teacher_url,
                                                                                 teacher_name)
        return send_schedule
    except IndexError :
        send_schedule = 'Зараз немає пари😀'
        return send_schedule
    except TypeError:
        send_schedule = 'Зараз немає пари😀'
        return send_schedule


