import psycopg2

class DatabaseError(Exception):
    pass

class MBPostgres:
    def __init__(self, db_name, user, password, host):
        try:
            # connect to database
            self.conn = psycopg2.connect(db_name, user, password, host)
            self.cur = self.conn.cursor()
            self._create_table()

        except psycopg2.Error as e:
            raise DatabaseError(f'Error while connecting to database: {e}')

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
                artist_id INT NOT NULL,
                event_name VARCHAR(255) NOT NULL,
                begin_time DATE,
                end_time DATE,
                CONSTRAINT FOREIGN KEY (artist_id) REFERENCES artists (id)
                )''')
            self.conn.commit()

        except psycopg2.Error as e:
            raise DatabaseError(f'Error while creating table: {e}')

    def add_artists(self, artists):
        try:
            query = '''
            INSERT INTO artists (name)
            VALUES (%s)'''
            self.cur.executemany(query, artists)

        except psycopg2.Error as e:
            raise DatabaseError(f'Error while adding artists: {e}')

    def add_events(self, artist_id, event_tup):
        try:
            query = '''
            INSERT INTO events (artist_id, event_name, begin_time, end_time)
            VALUES (%s, %s, %s, %s)'''
            self.cur.executemany(query, (artist_id, event_tup[0], event_tup[1], event_tup[2]))
            # TODO: convert incoming tuple into tuple of lists containing all events
            # TODO: if you want to add all events at once, but not necessary

        except psycopg2.Error as e:
            raise DatabaseError(f'Error while adding events: {e}')