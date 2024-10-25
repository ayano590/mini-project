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
            # only uncomment this if you want a fresh start everytime you run the program
            # self._drop_table()
            self._create_table()

        except psycopg2.Error as e:
            raise DatabaseError(f'Error while connecting to database: {e}')

    def _drop_table(self):
        try:
            self.cur.execute('DROP TABLE IF EXISTS events CASCADE')
            self.cur.execute('DROP TABLE IF EXISTS artists CASCADE')
            self.cur.execute('DROP TABLE IF EXISTS genres CASCADE')

        except psycopg2.Error as e:
            raise DatabaseError(f'Error while dropping table: {e}')

    def _create_table(self):
        try:
            self.cur.execute('''
            CREATE TABLE IF NOT EXISTS genres (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL
                )''')
            self.cur.execute('''
            CREATE TABLE IF NOT EXISTS artists (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                genre_id INT REFERENCES genres(id),
                img TEXT
                )''')
            self.cur.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id SERIAL PRIMARY KEY,
                artist_id INT REFERENCES artists(id),
                event_name VARCHAR(255) NOT NULL,
                begin_time VARCHAR,
                end_time VARCHAR
                )''')

        except psycopg2.Error as e:
            raise DatabaseError(f'Error while creating table: {e}')

    def add_genres(self, genres):
        try:
            query = '''
            INSERT INTO genres (name)
            VALUES (%s)'''
            self.cur.executemany(query, genres)

        except psycopg2.Error as e:
            raise DatabaseError(f'Error while adding artists: {e}')

    def add_artists(self, artists):
        try:
            query = '''
            INSERT INTO artists (name, img, genre_id)
            VALUES (%s, %s, %s)'''
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

    def get_genre_id(self, genre):
        try:
            self.cur.execute('SELECT id FROM genres WHERE name ILIKE %s', (genre, ))
            entry = self.cur.fetchone()
            if not entry:
                raise DatabaseError('Genre not found')
            return entry[0]
        except psycopg2.Error as e:
            raise DatabaseError(f'Error while getting genres: {e}')

    def get_genres(self):
        try:
            self.cur.execute('SELECT * FROM genres')
            rows = self.cur.fetchall()
            if not rows:
                raise DatabaseError('No genres found')
            df = pd.DataFrame(rows, columns=['id', 'name'])
            return df
        except psycopg2.Error as e:
            raise DatabaseError(f'Error while getting genres: {e}')

    def get_artists(self):
        try:
            self.cur.execute('SELECT id, name FROM artists')
            rows = self.cur.fetchall()
            if not rows:
                raise DatabaseError(f'No artists found')
            df = pd.DataFrame(rows, columns=['id', 'name'])
            return df
        except psycopg2.Error as e:
            raise DatabaseError(f'Error while getting artists: {e}')

    def get_artist_by_name(self, artist_name):
        try:
            self.cur.execute('SELECT id FROM artists WHERE name ILIKE %s', (artist_name, ))
            num = self.cur.fetchall()
            if not num:
                print(f'Artist {artist_name} not found')
                return
            return num[0]
        except psycopg2.Error as e:
            raise DatabaseError(f'Error while getting artist: {e}')

    def get_artist_image(self, artist_name):
        try:
            self.cur.execute('SELECT img FROM artists WHERE name ILIKE %s', (artist_name,))
            img = self.cur.fetchone()
            if img == ('-', ):
                print(f'No image available for {artist_name}')
                return
            return img[0]
        except psycopg2.Error as e:
            print(f'Error while getting artist image: {e}')

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
            self.cur.execute('''SELECT a.name, MAX(g.id), MAX(g.name), COUNT(*) FROM artists a INNER JOIN events e
            ON e.artist_id = a.id INNER JOIN genres g ON g.id = a.genre_id
            GROUP BY a.name''')
            rows = self.cur.fetchall()
            if not rows:
                raise DatabaseError(f'No events found')
            df = pd.DataFrame(rows, columns=['name', 'id', 'genre', 'event_count'])
            return df
        except psycopg2.Error as e:
            print(f'Error while getting events: {e}')

    def get_event_count_per_genre(self):
        try:
            self.cur.execute('''SELECT MAX(g.id), g.name, COUNT(*) FROM artists a INNER JOIN events e
                        ON e.artist_id = a.id
                        INNER JOIN genres g ON g.id = a.genre_id
                        GROUP BY g.name''')
            rows = self.cur.fetchall()
            if not rows:
                raise DatabaseError(f'No events found')
            df = pd.DataFrame(rows, columns=['id', 'name', 'event_count'])
            return df
        except psycopg2.Error as e:
            print(f'Error while getting events: {e}')

    def close_connection(self):
        try:
            self.conn.commit()
            self.conn.close()
        except psycopg2.Error as e:
            print(f'Error while closing connection: {e}')