import mysql.connector

mysqlparams = {
    'user': 'database_user',
    'password': 'database_password',
    'host': 'db',
    'database': 'database',
    'auth_plugin': 'mysql_native_password'
}


class DB:
    def __init__(self):
        self.conn = mysql.connector.connect(**mysqlparams)

    def __del__(self):
        self.conn.close()

    def query(self, sql, params=tuple()):
        cursor = self.conn.cursor()
        cursor.execute(sql, params)
        return cursor

    def add_user(self, name, user_password):
        statement = 'INSERT INTO users(%s) VALUES(%s)'
        fields = ['name', 'user_password']
        params = (name, user_password)

        sql = statement % (
            ', '.join(fields),
            ', '.join(['%s'] * len(params))
        )
        self.query(sql, params)
        self.conn.commit()

    def add_sport(self, name, description):
        statement = 'INSERT INTO sports(%s) VALUES(%s)'
        fields = ['name', 'description']
        params = (name, description)

        sql = statement % (
            ', '.join(fields),
            ', '.join(['%s'] * len(params))
        )
        self.query(sql, params)
        self.conn.commit()

    def add_event(self,
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
        self.query(sql, params)
        self.conn.commit()

    def add_participant(self, user_id, event_id, result):
        statement = 'INSERT INTO participants(%s) VALUES(%s)'
        fields = ['user_id', 'event_id', 'result']
        params = (user_id, event_id, result)

        sql = statement % (
            ', '.join(fields),
            ', '.join(['%s'] * len(params))
        )
        self.query(sql, params)
        self.conn.commit()

    def add_rating(self, user_id, sport_id, points):
        statement = 'INSERT INTO ratings(%s) VALUES(%s)'
        fields = ['user_id', 'sport_id', 'points']
        params = (user_id, sport_id, points)

        sql = statement % (
            ', '.join(fields),
            ', '.join(['%s'] * len(params))
        )
        self.query(sql, params)
        self.conn.commit()

    def add_follow(self, user_id, sport_id, location):
        statement = 'INSERT INTO follows(%s) VALUES(%s)'
        fields = ['user_id', 'sport_id', 'location']
        params = (user_id, sport_id, location)

        sql = statement % (
            ', '.join(fields),
            ', '.join(['%s'] * len(params))
        )
        self.query(sql, params)
        self.conn.commit()

    def add_place(self, name, description, longtitude, latitude):
        statement = 'INSERT INTO places(%s) VALUES(%s)'
        fields = ['name', 'description', 'longitude', 'latitude']
        params = (name, description, longtitude, latitude)

        sql = statement % (
            ', '.join(fields),
            ', '.join(['%s'] * len(params))
        )
        self.query(sql, params)
        self.conn.commit()

    def get_user_id(self, name):
        statement = 'SELECT * FROM users WHERE name=\'%s\';'
        sql = statement % name
        c = self.query(sql)
        result = c.fetchall()
        if len(result) == 0:
            return None, 1, 'No such user in database'
        return result[0][0], 0, 0

    def get_user_name(self, user_id):
        statement = 'SELECT * FROM users WHERE user_id=\'%s\';'
        sql = statement % user_id
        c = self.query(sql)
        result = c.fetchall()
        if len(result) == 0:
            return None # 'No such user in database'
        return result[0][1]

    def get_sport_id(self, name):
        statement = 'SELECT * FROM sports WHERE name=\'%s\';'
        sql = statement % name
        c = self.query(sql)
        result = c.fetchall()
        if len(result) == 0:
            return None, 1, 'No such sport in database'
        return result[0][0], 0, 0

    def get_sport_name(self, sport_id):
        statement = 'SELECT * FROM sports WHERE sport_id=\'%s\';'
        sql = statement % sport_id
        c = self.query(sql)
        result = c.fetchall()
        if len(result) == 0:
            return None, 1, 'No such user in database'
        return result[0][1], 0, 0

    def create_user(self, username, password):
        if len(password) < 8:
            return 1, 'Too short password'
        if not password.isalnum():
            return 1, 'Password must contain only letters or numbers'
        if password.isalpha():
            return 1, 'Password must contain also numbers'
        if password.isdigit():
            return 1, 'Password must contain also letters'
        self.add_user(username, password)
        return 0, 0

    def auth(self, username, password):
        statement = 'SELECT * FROM users WHERE %s;'
        fields = ['name=\'%s\'']
        params = (username)
        sql = statement % (
            ', '.join(fields)
        )
        sql = sql % params
        c = self.query(sql)
        result = c.fetchall()
        if len(result) == 0:
            return None, 1, "No such user"
        if result[0][2] != password:
            return None, 1, "Wrong password"
        return result[0][0], 0, 0

    def get_event_admin_id(self, event_id):
        statement = 'SELECT * FROM events WHERE %s;'
        fields = ['event_id=\'%s\'']
        params = (event_id)
        sql = statement % (
            ', '.join(fields)
        )
        sql = sql % params
        c = self.query(sql)
        result = c.fetchall()
        if len(result) == 0:
            return None, 1, "No such event"
        return result[0][1], 0, 0

    def update_event_status(self, event_id, event_status):
        if self.get_event_admin_id(event_id) == []:
            return 1, "No such event"
        statement = 'UPDATE events SET %s WHERE %s;'
        fields1 = ['state_open=\'%s\'']
        fields2 = ['event_id=\'%s\'']
        params = (event_status, event_id)
        sql = statement % (
            ', '.join(fields1),
            ', '.join(fields2)
        )
        sql = sql % params
        cursor = self.conn.cursor(buffered=True)
        cursor.execute(sql)
        self.conn.commit()
        return 0, 0

    def set_result(self, event_id, username, result, points):
        sql = "SELECT * FROM events WHERE event_id=%s" % (event_id)
        c = self.query(sql)
        res = c.fetchall()
        sport_id = res[0][2]
        user_id = self.get_user_id(username)
        sql = "SELECT * FROM ratings WHERE user_id=%s" % (user_id)
        c = self.query(sql)
        res = c.fetchall()
        if res == []:
            self.add_rating(user_id, sport_id, 0)
        statement = 'UPDATE ratings SET %s WHERE %s;'
        fields1 = ['points=%s', ]
        fields2 = ['sport_id=%s', 'user_id=%s']
        params = (points, sport_id, user_id)
        sql = statement % (
            ', '.join(fields1),
            ' AND '.join(fields2)
        )
        sql = sql % params
        cursor = self.conn.cursor(buffered=True)
        cursor.execute(sql)
        self.conn.commit()
        statement = 'UPDATE participants SET %s WHERE %s;'
        fields1 = ['result=\'%s\'', ]
        fields2 = ['user_id=%s', 'event_id=%s']
        params = (result, user_id, event_id)
        sql = statement % (
            ', '.join(fields1),
            ' AND '.join(fields2)
        )
        sql = sql % params
        cursor = self.conn.cursor(buffered=True)
        cursor.execute(sql)
        self.conn.commit()
        return 0, 0

    def get_event_info(self, event_id):
        statement = 'SELECT * FROM events WHERE %s;'
        fields = ['event_id=\'%s\'']
        params = (event_id)
        sql = statement % (
            ', '.join(fields)
        )
        sql = sql % params
        c = self.query(sql)
        result = c.fetchall()
        if len(result) == 0:
            return None, 1, "No such event"
        lst = result[0]

        data = {
            'sport_id': lst[2],
            'timestamp': lst[3],
            'location': lst[4],
            'description': lst[5],
            'participants_number_max': lst[6],
            'status_rating': lst[7],
            'state_open': lst[8]
        }
        return data, 0, 0

    def get_event_participants(self, event_id):
        statement = 'SELECT * FROM participants WHERE %s;'
        fields = ['event_id=\'%s\'']
        params = (event_id)
        sql = statement % (
            ', '.join(fields)
        )
        sql = sql % params
        c = self.query(sql)
        result = c.fetchall()
        lst = []
        for res in result:
            lst.append(self.get_user_name(res[0]))
        if len(lst) == 0:
            return None, 1, "No event participants"
        return lst, 0, 0

    def create_event(self,
            admin_id,
            sport_id,
            timestamp,
            location,
            description,
            participants_number_max,
            status_rating):
        self.add_event(
            admin_id,
            sport_id,
            timestamp,
            location,
            description,
            participants_number_max,
            status_rating,
            'Opened')
        c = self.query("SELECT LAST_INSERT_ID()")
        last_id = c.fetchall();
        self.join_event(admin_id, last_id[0][0])
        return 1, 0, 0

    def get_list_events(self, sport_id):
        sql = "SELECT * FROM events WHERE state_open=\'Opened\' AND sport_id=\'%s\'" % (
            sport_id)
        c = self.query(sql)
        result = c.fetchall()
        lst = []
        for res in result:
            lst.append(res[0])
        return lst, 0, 0

    def join_event(self, user_id, event_id):
        if self.get_event_admin_id(event_id) is None:
            return 0, 0
        self.add_participant(user_id, event_id, None)
        return 0, 0

    def leave_event(self, user_id, event_id):
        sql = "DELETE FROM participants WHERE user_id=\'%s\' AND event_id=\'%s\'" % (
            user_id, event_id)
        cursor = self.conn.cursor(buffered=True)
        cursor.execute(sql)
        self.conn.commit()
        return 0, 0

    def get_top(self, sport_id, count=10):
        sql = "SELECT * FROM ratings WHERE sport_id=%s ORDER BY points DESC LIMIT 0,%s" % (
            sport_id, count)
        c = self.query(sql)
        result = c.fetchall()
        lst = []
        for res in result:
            lst.append(self.get_user_name(res[0]))
        return lst, 0, 0

    def get_user_result(self, username, event_id):
        user_id = self.get_user_id(username)
        sql = "SELECT * FROM participants WHERE user_id=%s AND event_id=%s" % (
            user_id, event_id)
        c = self.query(sql)
        result = c.fetchall()
        if result == []:
            return None, 1, "%s didn't participate this event\n" % (username)
        return result[0][2], 0, 0

    def get_list_sports(self):
        sql = "SELECT * FROM sports"
        c = self.query(sql)
        result = c.fetchall()
        return result, 0, 0

    def get_list_users(self, sport_id):
        sql = "SELECT * FROM follows WHERE sport_id=%s" % (sport_id)
        c = self.query(sql)
        result = c.fetchall()
        lst = []
        for res in result:
            lst.append(self.get_user_name(res[0]))
        return lst, 0, 0

    def get_list_follows(self, user_id):
        sql = "SELECT * FROM follows WHERE user_id=%s" % (user_id)
        c = self.query(sql)
        result = c.fetchall()
        lst = []
        for res in result:
            lst.append(res[1])
        return lst, 0, 0

    def remove_follows(self, user_id, sport_id=0, location=0):
        if not sport_id and not location:
            sql = "DELETE FROM follows WHERE user_id=\'%s\'" % (
            user_id)
        elif not location:
            sql = "DELETE FROM follows WHERE user_id=\'%s\' AND sport_id=\'%s\'" % (
                user_id, sport_id)
        elif not sport_id:
            sql = "DELETE FROM follows WHERE user_id=\'%s\' AND location=\'%s\'" % (
                user_id, location)
        else:
            sql = "DELETE FROM follows WHERE user_id=\'%s\' AND sport_id=\'%s\' AND location=\'%s\'" % (
                user_id, sport_id, location)
        cursor = self.conn.cursor(buffered=True)
        cursor.execute(sql)
        self.conn.commit()
        return 0, 0

    def get_list_locations(self):
        sql = 'SELECT * FROM places;'
        c = self.query(sql)
        result = c.fetchall()
        return result, 0, None

    def get_user_events(self, username):
        user_id = self.get_user_id(username)
        sql = 'SELECT * FROM participants WHERE user_id=%s;' % (user_id[0])
        c = self.query(sql)
        result = c.fetchall()
        lst = []
        for res in result:
            lst.append(res[1])
        return lst, 0, None
