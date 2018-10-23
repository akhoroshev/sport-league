import mysql.connector

mysqlparams = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'staff'
}


class DB:
    conn = None
    cursor = None
    next_user_id = 0
    next_event_id = 0

    @staticmethod
    def connect():
        DB.conn = mysql.connector.connect(**mysqlparams)
        cursor = DB.conn.cursor()
        DB.next_user_id = 1
        DB.next_event_id = 1

    @staticmethod
    def query(sql, params=tuple()):
        try:
            cursor = DB.conn.cursor()
            cursor.execute(sql, params)
        except (AttributeError, mysql.connector.OperationalError) as e:
            DB.connect()
            cursor = DB.conn.cursor()
            cursor.execute(sql, params)
        return cursor

    @staticmethod
    def add_user(name, user_password):
        statement = 'INSERT INTO users(%s) VALUES(%s)'
        fields = ['name', 'user_password']
        params = (name, user_password)

        sql = statement % (
            ', '.join(fields),
            ', '.join(['%s'] * len(params))
        )
        DB.query(sql, params)
        DB.conn.commit()

    @staticmethod
    def add_sport(name, description):
        statement = 'INSERT INTO sports(%s) VALUES(%s)'
        fields = ['name', 'description']
        params = (name, description)

        sql = statement % (
            ', '.join(fields),
            ', '.join(['%s'] * len(params))
        )
        DB.query(sql, params)
        DB.conn.commit()

    @staticmethod
    def add_event(
            admin_id,
            sport_id,
            event_date,
            location,
            description,
            participants_number_max,
            status_rating,
            state_open):
        statement = 'INSERT INTO events(%s) VALUES(%s)'
        fields = [
            'admin_id',
            'sport_id',
            'event_date',
            'location',
            'description',
            'participants_number_max',
            'status_rating',
            'state_open']
        params = (
            admin_id,
            sport_id,
            event_date,
            location,
            description,
            participants_number_max,
            status_rating,
            state_open)

        sql = statement % (
            ', '.join(fields),
            ', '.join(['%s'] * len(params))
        )
        DB.query(sql, params)
        DB.conn.commit()

    @staticmethod
    def add_participant(user_id, event_id, result):
        statement = 'INSERT INTO participants(%s) VALUES(%s)'
        fields = ['user_id', 'event_id', 'result']
        params = (user_id, event_id, result)

        sql = statement % (
            ', '.join(fields),
            ', '.join(['%s'] * len(params))
        )
        DB.query(sql, params)
        DB.conn.commit()

    @staticmethod
    def add_rating(user_id, sport_id, points):
        statement = 'INSERT INTO ratings(%s) VALUES(%s)'
        fields = ['user_id', 'sport_id', 'points']
        params = (user_id, sport_id, points)

        sql = statement % (
            ', '.join(fields),
            ', '.join(['%s'] * len(params))
        )
        DB.query(sql, params)
        DB.conn.commit()

    @staticmethod
    def add_follow(user_id, sport_id, location):
        statement = 'INSERT INTO follows(%s) VALUES(%s)'
        fields = ['user_id', 'sport_id', 'location']
        params = (user_id, sport_id, location)

        sql = statement % (
            ', '.join(fields),
            ', '.join(['%s'] * len(params))
        )
        DB.query(sql, params)
        DB.conn.commit()

    @staticmethod
    def get_user_id(name):
        statement = 'SELECT * FROM users WHERE name=\'%s\';'
        sql = statement % name
        c = DB.query(sql)
        result = c.fetchall()
        if len(result) == 0:
            return 'No such user in database'
        return result[0][0]

    @staticmethod
    def get_user_name(user_id):
        statement = 'SELECT * FROM users WHERE user_id=\'%s\';'
        sql = statement % user_id
        c = DB.query(sql)
        result = c.fetchall()
        if len(result) == 0:
            return 'No such user in database'
        return result[0][1]

    @staticmethod
    def get_sport_id(name):
        statement = 'SELECT * FROM sports WHERE name=\'%s\';'
        sql = statement % name
        c = DB.query(sql)
        result = c.fetchall()
        if len(result) == 0:
            return 'No such sport in database'
        return result[0][0]

    @staticmethod
    def get_sport_name(sport_id):
        statement = 'SELECT * FROM sports WHERE sport_id=\'%s\';'
        sql = statement % sport_id
        c = DB.query(sql)
        result = c.fetchall()
        if len(result) == 0:
            return 'No such user in database'
        return result[0][1]

    @staticmethod
    def create_user(username, password):
        if len(password) < 8:
            return 'Too short password'
        if not password.isalnum():
            return 'Password must contain only letters or numbers'
        if password.isalpha():
            return 'Password must contain also numbers'
        if password.isdigit():
            return 'Password must contain also letters'
        DB.add_user(username, password)
        DB.next_user_id += 1

    @staticmethod
    def auth(username, password):
        statement = 'SELECT * FROM users WHERE %s;'
        fields = ['name=\'%s\'']
        params = (username)
        sql = statement % (
            ', '.join(fields)
        )
        sql = sql % params
        c = DB.query(sql)
        result = c.fetchall()
        if len(result) == 0:
            return "No such user"
        if result[0][2] != password:
            return "Wrong password"
#        print("auth: username={}, password={}".format(username, password))
        return result[0][0]

    @staticmethod
    def get_event_admin_id(event_id):
        statement = 'SELECT * FROM events WHERE %s;'
        fields = ['event_id=\'%s\'']
        params = (event_id)
        sql = statement % (
            ', '.join(fields)
        )
        sql = sql % params
        c = DB.query(sql)
        result = c.fetchall()
        if len(result) == 0:
            return "No such event"
        return result[0][1]

    @staticmethod
    def update_event_status(event_id, event_status):
        if DB.get_event_admin_id(event_id) == []:
            return "No such event"
        statement = 'UPDATE events SET %s WHERE %s;'
        fields1 = ['state_open=\'%s\'']
        fields2 = ['event_id=\'%s\'']
        params = (event_status, event_id)
        sql = statement % (
            ', '.join(fields1),
            ', '.join(fields2)
        )
        sql = sql % params
        cursor = DB.conn.cursor(buffered=True)
        cursor.execute(sql)
        DB.conn.commit()

    @staticmethod
    def set_result(event_id, username, result, points):
        sql = "SELECT * FROM events WHERE event_id=%s" % (event_id)
        c = DB.query(sql)
        res = c.fetchall()
        sport_id = res[0][2]
        user_id = DB.get_user_id(username)
        sql = "SELECT * FROM ratings WHERE user_id=%s" % (user_id)
        c = DB.query(sql)
        res = c.fetchall()
        if res == []:
            DB.add_rating(user_id, sport_id, 0)
        statement = 'UPDATE ratings SET %s WHERE %s;'
        fields1 = ['points=%s', ]
        fields2 = ['sport_id=%s', 'user_id=%s']
        params = (points, sport_id, user_id)
        sql = statement % (
            ', '.join(fields1),
            ' AND '.join(fields2)
        )
        sql = sql % params
        cursor = DB.conn.cursor(buffered=True)
        cursor.execute(sql)
        DB.conn.commit()
        statement = 'UPDATE participants SET %s WHERE %s;'
        fields1 = ['result=\'%s\'', ]
        fields2 = ['user_id=%s', 'event_id=%s']
        params = (result, user_id, event_id)
        sql = statement % (
            ', '.join(fields1),
            ' AND '.join(fields2)
        )
        sql = sql % params
        cursor = DB.conn.cursor(buffered=True)
        cursor.execute(sql)
        DB.conn.commit()
        return

    @staticmethod
    def get_event_info(event_id):
        statement = 'SELECT * FROM events WHERE %s;'
        fields = ['event_id=\'%s\'']
        params = (event_id)
        sql = statement % (
            ', '.join(fields)
        )
        sql = sql % params
        c = DB.query(sql)
        result = c.fetchall()
        if len(result) == 0:
            return "No such event"
        lst = result[0]

        data = {
            'sport_id': lst[2],
            'timestamp': lst[3],  # распарсить вывод
            'location': lst[4],
            'description': lst[5],
            'participants_number_max': lst[6],
            'status_rating': lst[7],
            'state_open': lst[8]
        }
        return data

    @staticmethod
    def get_event_participants(event_id):
        statement = 'SELECT * FROM participants WHERE %s;'
        fields = ['event_id=\'%s\'']
        params = (event_id)
        sql = statement % (
            ', '.join(fields)
        )
        sql = sql % params
        c = DB.query(sql)
        result = c.fetchall()
        lst = []
        for res in result:
            lst.append(DB.get_user_name(res[0]))
        if len(lst) == 0:
            return "No such event"
        return lst

    @staticmethod
    def create_event(
            admin_id,
            sport_id,
            timestamp,
            location,
            description,
            participants_number_max,
            status_rating):
        DB.add_event(
            DB.next_event_id,
            admin_id,
            sport_id,
            timestamp,
            location,
            description,
            participants_number_max,
            status_rating,
            'Opened')
        DB.next_event_id += 1
        return DB.next_event_id - 1

    @staticmethod
    def get_list_events(sport_id):
        sql = "SELECT * FROM events WHERE state_open=\'Opened\' AND sport_id=\'%s\'" % (
            sport_id)
        c = DB.query(sql)
        result = c.fetchall()
        lst = []
        for res in result:
            lst.append(res[0])
        return lst

    @staticmethod
    def join_event(user_id, event_id):
        if DB.get_event_admin_id(event_id) is None:
            return
        DB.add_participant(user_id, event_id, 'D')

    @staticmethod
    def leave_event(user_id, event_id):
        sql = "DELETE FROM participants WHERE user_id=\'%s\' AND event_id=\'%s\'" % (
            user_id, event_id)
        cursor = DB.conn.cursor(buffered=True)
        cursor.execute(sql)
        DB.conn.commit()
        return 0, None

    @staticmethod
    def get_top(sport_id, count=10):
        sql = "SELECT * FROM ratings WHERE sport_id=%s ORDER BY points DESC LIMIT 0,%s" % (
            sport_id, count)
        c = DB.query(sql)
        result = c.fetchall()
        lst = []
        for res in result:
            lst.append(DB.get_user_name(res[0]))
        return lst

    @staticmethod
    def get_user_result(username, event_id):
        user_id = DB.get_user_id(username)
        sql = "SELECT * FROM participants WHERE user_id=%s AND event_id=%s" % (
            user_id, event_id)
        c = DB.query(sql)
        result = c.fetchall()
        if result == []:
            return "%s didn't participate this event\n" % (username)
        return result[0][2]

    @staticmethod
    def get_list_sports():
        sql = "SELECT * FROM sports"
        c = DB.query(sql)
        result = c.fetchall()
        return result

    @staticmethod
    def get_list_users(sport_id):
        sql = "SELECT * FROM follows WHERE sport_id=%s" % (sport_id)
        c = DB.query(sql)
        result = c.fetchall()
        lst = []
        for res in result:
            lst.append(DB.get_user_name(res[0]))
        return lst

    @staticmethod
    def get_list_follows(user_id):
        sql = "SELECT * FROM follows WHERE user_id=%s" % (user_id)
        c = DB.query(sql)
        result = c.fetchall()
        lst = []
        for res in result:
            lst.append(res[1])
        return lst

    @staticmethod
    def remove_follows(user_id, sport_id):
        sql = "DELETE FROM follows WHERE user_id=\'%s\' AND sport_id=\'%s\'" % (
            user_id, sport_id)
        cursor = DB.conn.cursor(buffered=True)
        cursor.execute(sql)
        DB.conn.commit()
