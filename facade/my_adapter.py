import mysql.connector

mysqlparams = {
        'user': 'root',
        'password': 'testmysql',
        'host': 'localhost',
        'database': 'testdb2',
        }

class DB:
    conn = None

    @staticmethod
    def connect():
        DB.conn = mysql.connector.connect(**mysqlparams) #connection with database

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
    def add_user(user_id, name, user_password):
        statement = 'INSERT INTO users(%s) VALUES(%s)'
        fields = ['user_id', 'name', 'user_password']
        params = (user_id, name, user_password)

        sql = statement % (
            ', '.join(fields),
            ', '.join(['%s'] * len(params))
        )
        DB.query(sql, params)
        DB.conn.commit()

    @staticmethod
    def add_sport(sport_id, name, description):
        statement = 'INSERT INTO sports(%s) VALUES(%s)'
        fields = ['sport_id', 'name', 'description']
        params = (sport_id, name, description)

        sql = statement % (
            ', '.join(fields),
            ', '.join(['%s'] * len(params))
        )
        DB.query(sql, params)
        DB.conn.commit()

    @staticmethod
    def add_event(event_id, admin_id, sport_id, event_date, location, description, participants_number_max, status_rating, state_open):
        statement = 'INSERT INTO events(%s) VALUES(%s)'
        fields = ['event_id', 'admin_id', 'sport_id', 'event_date', 'location', 'description', 'participants_number_max', 'status_rating', 'state_open']
        params = (event_id, admin_id, sport_id, event_date, location, description, participants_number_max, status_rating, state_open)

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
    def add_following(user_id, sport_id, location, radius):
        statement = 'INSERT INTO follows(%s) VALUES(%s)'
        fields = ['user_id', 'sport_id', 'location', 'radius']
        params = (user_id, sport_id, location, radius)

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
        print(sql)
        c = DB.query(sql)
        result = c.fetchall()
        if len(result) == 0:
            raise Exception('No such user in database')
        return result[0][0]

    @staticmethod
    def get_user_name(user_id):
        statement = 'SELECT * FROM users WHERE user_id=\'%s\';'
        sql = statement % user_id
        print(sql)
        c = DB.query(sql)
        result = c.fetchall()
        if len(result) == 0:
            raise Exception('No such user in database')
        return result[0][1]

