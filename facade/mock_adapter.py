'''
Заглушка для DB

все методы, возвращающие что-то:
    return data, 0, None        # в случае успеха
    return None, status, error  # status > 0, error=сообщение об ошибке

все методы, которые ничего не возвращают:
    return 0, None        # в случае успеха
    return status, error  # status > 0, error=сообщение об ошибке
'''

class DB:
    @staticmethod
    def create_user(username, password):
        print("create user: username={}, password={}".format(username, password))
        return 0, None

    @staticmethod
    def auth(username, password):
        '''
        проверяем наличие записи username-password в таблице users
        возвращаем user_id
        '''
        print("auth: username={}, password={}".format(username, password))
        return 23, 0, None

    @staticmethod
    def get_event_admin_id(event_id):
        '''
        вернуть admin_id для event_id
        '''
        print("get event_id={} admin".format(event_id))
        return 23, 0, None

    @staticmethod
    def update_event_status(event_id, event_status):
        print("set event_id={} status={}".format(event_id, event_status))
        return 0, None

    # следующий метод - костыльный
    # мы забыли обсудить внесение результатов
    @staticmethod
    def set_result(event_id, username, result):
        '''
        обновить результат для username в event_id
        должны обновляться обе таблицы - participants и ratings
        '''
        print("set result={} for username={} in event_id={}".format(result, username, event_id))
        return 0, None

    @staticmethod
    def get_event_info(event_id):
        '''
        вернуть подробную информацию для event_id (без списка участников!)
        '''
        print("get event_id={} info".format(event_id))
        data =  {
                    'sport_id': 7,
                    'timestamp': 78123217,
                    'location': 'Таймс',
                    'description': 'Покер SNG 9MAX',
                    'participants_number_max': 9,
                    'status_rating': True
                }
        return data, 0, None
    
    @staticmethod
    def get_event_participants(event_id):
        '''
        вернуть список участников для event_id
        '''
        print("get event_id={} participants".format(event_id))
        return ['oleg', 'anna'], 0, None
    
    @staticmethod
    def create_event(admin_id, sport_id, timestamp, location, description, participants_number_max, status_rating):
        '''
        создать событие
        вернуть event_id
        '''
        print("user_id={} creates sport_id={} event".format(admin_id, sport_id))
        return 8, 0, None


    @staticmethod
    def get_list_events(sport_id):
        '''
        вернуть список opened event_id для значения sport_id
        '''
        print("get list of sport_id={} events".format(sport_id))
        return [12, 14, 15, 28, 31, 190], 0, None

    @staticmethod
    def join_event(user_id, event_id):
        '''
        user_id присоединяется к event_id
        проверки на количество участников/повторное присоединение сделал у себя
        '''
        print("user_id={} joins event_id={}".format(user_id, event_id))
        return 0, None

    @staticmethod
    def leave_event(user_id, event_id):
        '''
        user_id покидает event_id
        проверки на админа/отсутствие в списке сделал у себя
        '''
        print("user_id={} leaves event_id={}".format(user_id, event_id))
        return 0, None

    @staticmethod
    def get_top(sport_id, count=10):
        '''
        вернуть топ игроков в sport_id
        '''
        print("get top{} for sport_id={}".format(count, sport_id))
        data = [('oleg', 120), ('irina', 102), ('rex', '87')]
        return data, 0, None

    @staticmethod
    def get_user_result(username, event_id):
        '''
        вернуть результат username(по имени!) в event_id (только по closed?)
        если результата нет - можно None
        '''
        print("get username={} result for event_id={}".format(username, event_id))
        return 'W', 0, None

    @staticmethod
    def get_list_sports():
        '''
        вернуть данные из таблицы sports
        '''
        print("get sports list")
        data = [(2, 'футбол', 'футбол в зале на петроградской'), (6, 'шахматы', 'шахматы online')]
        return data, 0, None

    @staticmethod
    def get_list_users(sport_id):
        '''
        вернуть список имен пользователей для sport_id
        можно тех, у кого есть follow sport_id
        или тех, кто когда-нибудь участвовал в sport_id событиях
        '''
        print("get sport_id={} users".format(sport_id))
        data = ['fish11', 'rex99', 'dogdog']
        return data, 0, None

    # 3 метода для работы с подписками
    @staticmethod
    def get_list_follows(user_id):
        print("get follows list for user_id={}".format(user_id))
        data = [1,2,3,6,8,12]
        return data, 0, None

    @staticmethod
    def add_follow(user_id, sport_id, location):
        print("add follow for user_id={}: sport_id={}, location={}".format(user_id, sport_id, location))
        return 0, None

    @staticmethod
    def remove_follows(user_id, sport_id):
        print("remove follows for user_id={}: sport_id={}".format(user_id, sport_id))
        return 0, None
