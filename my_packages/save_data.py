import psycopg2
import pandas as pd

class DatabaseError(Exception):
    pass

class MBPostgres:
    def __init__(self, host, user, password, db_name):
        try:
            # connect to database
            self.conn = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=db_name)
            self.cur = self.conn.cursor()
            self._drop_table()
            self._create_table()

        except psycopg2.Error as e:
            print(f'Error while connecting to database: {e}')

    def _drop_table(self):
        try:
            self.cur.execute('DROP TABLE IF EXISTS artists CASCADE')
            self.cur.execute('DROP TABLE IF EXISTS events CASCADE')

        except psycopg2.Error as e:
            print(f'Error while dropping table: {e}')

    def _create_table(self):
        try:
            self.cur.execute('''
            CREATE TABLE IF NOT EXISTS artists (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL)
                ''')
            self.cur.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id SERIAL PRIMARY KEY,
                artist_id INT REFERENCES artists(id),
                event_name VARCHAR(255) NOT NULL,
                begin_time VARCHAR,
                end_time VARCHAR
                )''')

        except psycopg2.Error as e:
            print(f'Error while creating table: {e}')

    def add_artists(self, artists):
        try:
            query = '''
            INSERT INTO artists (name)
            VALUES (%s)'''
            self.cur.executemany(query, artists)

        except psycopg2.Error as e:
            raise DatabaseError(f'Error while adding artists: {e}')

    def add_events(self, event_tup):
        try:
            query = '''
            INSERT INTO events (artist_id, event_name, begin_time, end_time)
            VALUES (%s, %s, %s, %s)'''
            self.cur.executemany(query, event_tup)

        except psycopg2.Error as e:
            raise DatabaseError(f'Error while adding events: {e}')

    def get_artists(self):
        try:
            self.cur.execute('SELECT * FROM artists')
            rows = self.cur.fetchall()
            if not rows:
                raise DatabaseError(f'No artists found')
            df = pd.DataFrame(rows, columns=['id', 'name'])
            return df
        except psycopg2.Error as e:
            print(f'Error while getting artists: {e}')

    def get_events(self):
        try:
            self.cur.execute('SELECT * FROM events')
            rows = self.cur.fetchall()
            if not rows:
                raise DatabaseError(f'No events found')
            df = pd.DataFrame(rows, columns=['id', 'artist_id', 'event_name', 'begin_time', 'end_time'])
            return df
        except psycopg2.Error as e:
            print(f'Error while getting events: {e}')

    def get_event_by_artist(self, artist_name):
        try:
            self.cur.execute('''SELECT e.event_name, e.begin_time, e.end_time
            FROM artists a INNER JOIN events e ON a.id = e.artist_id
            WHERE a.name ILIKE %s''', (artist_name,))
            rows = self.cur.fetchall()
            if not rows:
                print(f'No artist events found')
                return
            df = pd.DataFrame(rows, columns=['event_name', 'begin_time', 'end_time'])
            return df
        except psycopg2.Error as e:
            print(f'Error while getting artist events: {e}')

    def get_event_count(self):
        try:
            self.cur.execute('''SELECT a.name, COUNT(*) FROM artists a INNER JOIN events e
            ON e.artist_id = a.id
            GROUP BY a.name''')
            rows = self.cur.fetchall()
            if not rows:
                raise DatabaseError(f'No events found')
            df = pd.DataFrame(rows, columns=['name', 'event_count'])
            return df
        except psycopg2.Error as e:
            print(f'Error while getting events: {e}')

    def close_connection(self):
        try:
            self.conn.commit()
            self.conn.close()
        except psycopg2.Error as e:
            print(f'Error while closing connection: {e}')