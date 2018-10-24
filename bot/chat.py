from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, \
    InlineKeyboardMarkup
import util
import pickle

registered_users = {}
user_states = {}
user_answers = {}


def load_user_data(file='users.txt'):
    global registered_users
    try:
        with open(file, 'rb') as f:
            registered_users = pickle.load(f)
    except Exception as e:
        registered_users = {}


def save_user_data(file='users.txt'):
    global registered_users
    with open(file, 'wb') as f:
        pickle.dump(registered_users, f)


def get_auth(user_id):
    if user_id not in registered_users:
        raise ValueError('Вы не зарегистрированы')
    return registered_users[user_id]


def set_user_answer(user_id, field, result):
    if user_id in user_answers:
        user_answers[user_id][field] = result
    else:
        user_answers[user_id] = {field: result}


def get_user_answer(user_id, field):
    if user_id in user_answers:
        if field in user_answers[user_id]:
            return user_answers[user_id][field]
    raise ValueError('Что-то пошло не так..')


def get_user_state(user_id):
    if user_id in user_states:
        return user_states[user_id]
    else:
        return None


def set_user_state(user_id, state):
    user_states[user_id] = state


def check_registration(handler):
    def wrapper(bot, update, *args, **kwargs):
        if update.message.chat_id in registered_users:
            try:
                util.post('/register/check', registered_users[update.message.chat_id])
            except Exception as e:
                update.message.reply_text('Неправильный логин/пароль!')
                return
            handler(bot, update, args, kwargs)
        else:
            update.message.reply_text('Для создания и просмотра событий необходимо авторизироваться!')
            return

    return wrapper


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Привет! Этот бот нужен для организации спортивных мероприятий!🏆\n"
                          "Некоторые команды которые тебе понядобятся:\n"
                          "/register nickname password - регигистрирует пользователя с указанными данными\n"
                          "/login nickname password - вход в систему с указанными данными\n"
                          "/create_event - создать спортивное событие и указать его параметры\n"
                          "/cancel - отменить текущий процесс\n"
                          "/list_all_events - показать все события\n"
                          "/list_my_events - показать события, в которых вы участник\n"
                          "/list_follows - отобразить отслеживаемые события\n"
                          "/create_follow - начать отслеживать событие")


def login(bot, update, args):
    if len(args) != 2:
        bot.send_message(chat_id=update.message.chat_id, text='Логин и пароль необходимы!')
        return
    try:
        util.post('/register/check', {'username': args[0], 'password': args[1]})
        registered_users[update.message.chat_id] = {
            'username': args[0],
            'password': args[1]
        }
        save_user_data()
        msg = 'Вход в систему успешно выполнен!'
    except Exception as e:
        msg = 'Неправильный логин/пароль!'
    bot.send_message(chat_id=update.message.chat_id, text=msg)


def register(bot, update, args):
    if len(args) != 2:
        bot.send_message(chat_id=update.message.chat_id, text='Логин и пароль необходимы!')
        return
    try:
        util.post('/register', {'username': args[0], 'password': args[1]})
        registered_users[update.message.chat_id] = {
            'username': args[0],
            'password': args[1]
        }
        save_user_data()
        msg = 'Регистрация успешно выполнена!'
    except Exception as e:
        msg = 'Невозможно зарегестрироваться с таким логином/паролем!'
    bot.send_message(chat_id=update.message.chat_id, text=msg)


def chose_sport():
    kb = [[KeyboardButton(sport) for sport in util.sport_list()]]
    kb_markup = ReplyKeyboardMarkup(kb, resize_keyboard=True)
    return kb_markup


def chose_time():
    kb = [[KeyboardButton(sport) for sport in util.time_list()]]
    kb_markup = ReplyKeyboardMarkup(kb, resize_keyboard=True)
    return kb_markup


def chose_ranked():
    kb = [[KeyboardButton('Да'), KeyboardButton('Нет')]]
    kb_markup = ReplyKeyboardMarkup(kb, resize_keyboard=True)
    return kb_markup


def chose_location():
    kb = [[KeyboardButton(sport) for sport in util.location_list()]]
    kb_markup = ReplyKeyboardMarkup(kb, resize_keyboard=True)
    return kb_markup


@check_registration
def request_for_creating_event(bot, update, *args, **kwargs):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Выбери вид спорта из предложенных ⚽️🏀🏓',
                     reply_markup=chose_sport())
    set_user_state(update.message.chat_id, 'event_sport')


@check_registration
def request_for_creating_follow(bot, update, *args, **kwargs):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Выбери вид спорта из предложенных ⚽️🏀🏓',
                     reply_markup=chose_sport())
    set_user_state(update.message.chat_id, 'follow_sport')


@check_registration
def request_for_list_your_follow(bot, update, *args, **kwargs):
    generate_follow_buttons(bot, update, get_your_follow_list(update.message.chat_id))


@check_registration
def request_for_list_your_events(bot, update, *args, **kwargs):
    update.message.reply_text('Загружаем события...')
    event_list = get_your_event_list(update.message.chat_id)
    if event_list:
        generate_event_buttons(bot, update.message.chat_id, event_list)
    else:
        update.message.reply_text('Событий нет')


@check_registration
def request_for_list_events(bot, update, *args, **kwargs):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Выбери вид спорта из предложенных ⚽️🏀🏓',
                     reply_markup=chose_sport())
    set_user_state(update.message.chat_id, 'list_sport')


def cancel(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text='Отмена',
                     reply_markup=ReplyKeyboardRemove())
    set_user_state(update.message.chat_id, None)


def process_creating_event(bot, update):
    id = update.message.chat_id
    current_state = get_user_state(id)
    if current_state is None:
        return
    elif current_state is 'event_sport':
        try:
            set_user_answer(id, 'event_sport', util.parse_sport_id(update.message.text))
            update.message.reply_text('Выбери удобное время, или укажи в формате MM-DD-hh🕐', reply_markup=chose_time())
            set_user_state(id, 'event_date')
        except ValueError as e:
            update.message.reply_text(str(e))
        except Exception as e:
            pass
    elif current_state is 'event_date':
        try:
            set_user_answer(id, 'event_date', util.parse_time(update.message.text))
            update.message.reply_text('Выбери локацию🗺', reply_markup=chose_location())
            set_user_state(id, 'event_location')
        except ValueError as e:
            update.message.reply_text(str(e))
        except Exception as e:
            pass
    elif current_state is 'event_location':
        try:
            set_user_answer(id, 'event_location', util.parse_location_id(update.message.text))
            update.message.reply_text('Оставь несколько комментариев о событии📝', reply_markup=ReplyKeyboardRemove())
            set_user_state(id, 'event_description')
        except ValueError as e:
            update.message.reply_text(str(e))
        except Exception as e:
            pass
    elif current_state is 'event_description':
        set_user_answer(id, 'event_description', update.message.text)
        update.message.reply_text('Сколько человек необходимо')
        set_user_state(id, 'event_amount_of_players')
    elif current_state is 'event_amount_of_players':
        try:
            amount = int(update.message.text)
            if amount < 1:
                raise ValueError('Число участников < 1')
            set_user_answer(id, 'event_amount_of_players', amount)
            update.message.reply_text('Это рейтинговое событие?', reply_markup=chose_ranked())
            set_user_state(id, 'event_ranked')
        except ValueError:
            update.message.reply_text('Выбери количество участников еще раз')
    elif current_state is 'event_ranked':
        try:
            set_user_answer(id, 'event_ranked', util.parse_ranked(update.message.text))
            update.message.reply_text('Событие создается...', reply_markup=ReplyKeyboardRemove())
            set_user_state(id, None)
        except ValueError as e:
            update.message.reply_text(str(e))
            return
        try:
            event_id, usernames = event_create(id)
            update.message.reply_text('Событие создано')
        except Exception as e:
            update.message.reply_text(str(e))
            return
        # TODO
        send_notifications(
            bot,
            [chat_id for chat_id in registered_users if registered_users[chat_id]['username'] in usernames],
            [event_id]
        )


def process_creating_follow(bot, update):
    id = update.message.chat_id
    current_state = get_user_state(id)
    if current_state is None:
        return
    elif current_state is 'follow_sport':
        try:
            set_user_answer(id, 'follow_sport', util.parse_sport_id(update.message.text))
            update.message.reply_text('Выбери локацию🗺', reply_markup=chose_location())
            set_user_state(id, 'follow_location')
        except ValueError as e:
            update.message.reply_text(str(e))
    elif current_state is 'follow_location':
        try:
            set_user_answer(id, 'follow_location', util.parse_location_id(update.message.text))
            update.message.reply_text('Подписываем на обновления...', reply_markup=ReplyKeyboardRemove())
            set_user_state(id, None)
        except ValueError as e:
            update.message.reply_text(str(e))
        try:
            event_ids = follow_create(id)
            update.message.reply_text('Вы подписаны')
        except Exception as e:
            update.message.reply_text(str(e))
            return
        # TODO
        send_notifications(bot, [update.message.chat_id], event_ids)


def process_list_events(bot, update):
    id = update.message.chat_id
    current_state = get_user_state(id)
    if current_state is None:
        return
    elif current_state is 'list_sport':
        try:
            set_user_answer(id, 'list_sport', util.parse_sport_id(update.message.text))
            update.message.reply_text('Загружаем события...', reply_markup=ReplyKeyboardRemove())
            set_user_state(id, None)
        except ValueError as e:
            update.message.reply_text(str(e))
            return
        try:
            event_list = get_event_list(id)
            if event_list:
                generate_event_buttons(bot, update.message.chat_id, event_list)
            else:
                update.message.reply_text('Событий нет')
        except Exception as e:
            update.message.reply_text(str(e))


def input(bot, update):
    process_creating_event(bot, update)
    process_list_events(bot, update)
    process_creating_follow(bot, update)


def follow_create(id):
    data = util.post(
        '/follow/add',
        {
            'sport_id': get_user_answer(id, 'follow_sport'),
            'location': get_user_answer(id, 'follow_location')
        },
        get_auth(id)
    )
    return data['event_ids']


def event_create(id):
    data = util.post(
        '/event/create',
        {
            'sport_id': get_user_answer(id, 'event_sport'),
            'timestamp': get_user_answer(id, 'event_date'),
            'location': get_user_answer(id, 'event_location'),
            'description': get_user_answer(id, 'event_description'),
            'participants_number_max': get_user_answer(id, 'event_amount_of_players'),
            'status_rating': get_user_answer(id, 'event_ranked')
        },
        get_auth(id)
    )
    return data['event_id'], data['usernames']


def get_your_follow_list(id):
    follows_ids = util.post(
        '/follow/list',
        {},
        get_auth(id)
    )
    return get_follow_detail(follows_ids['follow_ids'], id)


def get_your_event_list(id):
    event_ids = util.post(
        '/event/user',
        {},
        get_auth(id)
    )
    return get_event_detail(event_ids['event_ids'], id)


def get_event_list(id):
    event_ids = util.post(
        '/event/list',
        {
            'sport_id': get_user_answer(id, 'list_sport')
        },
        get_auth(id)
    )
    return get_event_detail(event_ids['event_ids'], id)


def get_follow_detail(follows_id, tg_id):
    result = dict()
    for follow_id in follows_id:
        result[follow_id] = {}
        data = util.post(
            '/follow/get',
            {
                'follow_id': follow_id
            },
            get_auth(tg_id)
        )
        result[follow_id]['Вид спорта'] = util.id_to_sport(str(data['follow_info']['sport_id']))
        result[follow_id]['Локация'] = util.id_to_location(str(data['follow_info']['location']))
    return result


def get_event_detail(events_id, chat_id):
    result = dict()
    for event_id in events_id:
        result[event_id] = {}
        data = util.post(
            '/event/get',
            {
                'event_id': event_id
            },
            get_auth(chat_id))
        result[event_id]['Вид спорта'] = util.id_to_sport(str(data['event_info']['sport_id']))
        result[event_id]['Время'] = util.timestamp_to_human(data['event_info']['timestamp'])
        result[event_id]['Локация'] = util.id_to_location(str(data['event_info']['location']))
        result[event_id]['Число участников'] = data['event_info']['participants_number_max']
        result[event_id]['Описание'] = data['event_info']['description']
        result[event_id]['Статус'] = data['event_info']['state_open']
    return result


def generate_event_buttons(bot, chat_id, events):
    for event_id in events:
        msg = str()
        for field in events[event_id]:
            msg += str(field) + ': ' + str(events[event_id][field]) + '\n'
        kb = [[InlineKeyboardButton('Присоединиться', callback_data='join:' + str(event_id)),
               InlineKeyboardButton('Покинуть', callback_data='leave:' + str(event_id)),
               InlineKeyboardButton('Удалить', callback_data='delete:' + str(event_id))],
              [InlineKeyboardButton('Вывести список участников', callback_data='show:' + str(event_id)),
               InlineKeyboardButton('Где?', callback_data='map:' + str(event_id))]]
        bot.send_message(chat_id=chat_id, text=msg, reply_markup=InlineKeyboardMarkup(kb))


def generate_follow_buttons(bot, update, follows):
    for follow_id in follows:
        msg = str()
        for field in follows[follow_id]:
            msg += str(field) + ': ' + str(follows[follow_id][field]) + '\n'
        kb = [[InlineKeyboardButton('Отписаться', callback_data='unsubscribe:' + str(follow_id))]]
        update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(kb))


def show_event_participants(bot, update):
    query = update.callback_query
    data = query.data[len('show:'):]

    bot.send_message(text="Готовим список участников события...",
                          chat_id=query.message.chat_id
    )
    try:
        result = util.post(
            '/event/get',
            {
                'event_id': int(data)
            },
            get_auth(query.message.chat_id)
        )
        s_part = str()
        for participant in result['participants']:
            s_part = s_part + "☑️ " + participant + "\n"
        bot.send_message(chat_id=query.message.chat_id,
                         text=s_part)
    except Exception as e:
        bot.send_message(chat_id=query.message.chat_id,
                         text=str(e))


def join_to_event(bot, update):
    query = update.callback_query
    data = query.data[len('join:'):]
    
    bot.send_message(
        text="Присоединяем к событию...",
        chat_id=query.message.chat_id
    )
    try:
        util.post(
            '/event/join',
            {
                'event_id': int(data)
            },
            get_auth(query.message.chat_id)
        )
        bot.send_message(chat_id=query.message.chat_id,
                         text='Добавление успешно')
    except Exception as e:
        bot.send_message(chat_id=query.message.chat_id,
                         text=str(e))


def leave_from_event(bot, update):
    query = update.callback_query
    data = query.data[len('leave:'):]

    bot.send_message(
        text="Покидаем событие...",
        chat_id=query.message.chat_id,
    )
    try:
        util.post(
            '/event/leave',
            {
                'event_id': int(data)
            },
            get_auth(query.message.chat_id)
        )
        bot.send_message(chat_id=query.message.chat_id,
                         text='Событие покинуто')
    except Exception as e:
        bot.send_message(chat_id=query.message.chat_id,
                         text=str(e))


def show_location_event(bot, update):
    query = update.callback_query
    data = query.data[len('map:'):]

    bot.edit_message_text(text="Событие проходит тут:",
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)
    try:
        ans = util.post(
            '/event/get',
            {
                'event_id': int(data)
            },
            get_auth(query.message.chat_id)
        )
        location_id = ans['event_info']['location']
        ans = util.post(
            '/location/list',
            {},
            get_auth(query.message.chat_id)
        )
        ans = ans[str(location_id)]
        bot.send_location(chat_id=query.message.chat_id,
                          longitude=ans['longitude'], latitude=ans['latitude'])
    except Exception as e:
        bot.send_message(chat_id=query.message.chat_id,
                         text=str(e))


def delete_event(bot, update):
    query = update.callback_query
    data = query.data[len('delete:'):]

    bot.edit_message_text(text="Удаляем событие...",
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)
    try:
        util.post(
            '/event/close',
            {
                'event_id': int(data),
                'event_status': 'Canceled',
                'results': {}
            },
            get_auth(query.message.chat_id)
        )
        bot.send_message(chat_id=query.message.chat_id,
                         text='Событие удалено')
    except Exception as e:
        bot.send_message(chat_id=query.message.chat_id,
                         text=str(e))


def unsubscribe(bot, update):
    query = update.callback_query
    data = query.data[len('unsubscribe:'):]

    bot.edit_message_text(text="Отписываемся...",
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)
    try:
        util.post(
            '/follow/remove',
            {
                'follow_id': int(data)
            },
            get_auth(query.message.chat_id)
        )
        bot.send_message(chat_id=query.message.chat_id,
                         text='Подписка удалена')
    except Exception as e:
        bot.send_message(chat_id=query.message.chat_id,
                         text=str(e))


def send_notifications(bot, chat_ids, event_ids):
    print(chat_ids, event_ids)
    for chat_id in chat_ids:
        generate_event_buttons(bot, chat_id, get_event_detail(event_ids, chat_id))

