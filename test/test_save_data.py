"""unittest of MBPostgres class"""

import unittest
import pandas as pd
import sys
import os

os.chdir("../")
sys.path.append(os.getcwd())

from my_packages import save_data, db_config

class TestMBPostgres(unittest.TestCase):

    def setUp(self):
        print("\nSetup called")
        self.db_class = save_data.MBPostgres(
            host=db_config.DB_HOST,
            user=db_config.DB_USER,
            password=db_config.DB_PASSWORD,
            db_name=db_config.DB_NAME
        )

    def tearDown(self):
        print("\nTeardown called")
        self.db_class.close_connection()

    def test_add_get_genres(self):
        with self.assertRaises(save_data.DatabaseError):
            self.db_class.get_genres()
        with self.assertRaises(save_data.DatabaseError):
            self.db_class.get_genre_id('rvigz4wv98gsdzgvse')
        self.db_class.add_genres([('Jazz', )])
        data = {'id': [1], 'name': ['Jazz']}
        df = pd.DataFrame(data)
        self.assertTrue(self.db_class.get_genres().equals(df))
        self.assertEqual(self.db_class.get_genre_id('Jazz'), 1)

    def test_add_get_artists(self):
        with self.assertRaises(save_data.DatabaseError):
            self.db_class.get_artists()
        self.db_class.add_genres([('Jazz', )])
        self.db_class.add_artists([('Post Melone', '-', 1), ('Ayran Grande', '-', 1)])
        data = {'id': [1, 2], 'name': ['Post Melone', 'Ayran Grande']}
        df = pd.DataFrame(data)
        self.assertTrue(self.db_class.get_artists().equals(df))
        self.assertEqual(self.db_class.get_artist_by_name('Post Melone'), 1)

    def test_add_get_events(self):
        with self.assertRaises(save_data.DatabaseError):
            self.db_class.get_events()
        self.db_class.add_genres([('Jazz',)])
        self.db_class.add_artists([('Post Melone', '-', 1), ('Ayran Grande', '-', 1)])
        self.db_class.add_events([(1, 'The Best Festival', '2050-07-12', '2052-03-11')])
        data = {'id': [1], 'artist_id': [1], 'event_name': ['The Best Festival'],
                'begin_time': ['2050-07-12'], 'end_time': ['2052-03-11']}
        df = pd.DataFrame(data)
        self.assertTrue(self.db_class.get_events().equals(df))
        self.assertIsNone(self.db_class.get_event_by_artist('Ayran Grande'))

    def test_get_event_count(self):
        with self.assertRaises(save_data.DatabaseError):
            self.db_class.get_event_count()
        self.db_class.add_genres([('Jazz',)])
        self.db_class.add_artists([('Post Melone', '-', 1), ('Ayran Grande', '-', 1)])
        self.db_class.add_events([(1, 'The Best Festival', '2050-07-12', '2052-03-11')])
        data1 = {'name': ['Post Melone'], 'id': [1], 'genre': ['Jazz'], 'event_count': [1]}
        df1 = pd.DataFrame(data1)
        self.assertTrue(self.db_class.get_event_count().equals(df1))
        data2 = {'id': [1], 'name': ['Jazz'], 'event_count': [1]}
        df2 = pd.DataFrame(data2)
        self.assertTrue(self.db_class.get_event_count_per_genre().equals(df2))

    def test_get_artist_image(self):
        self.assertIsNone(self.db_class.get_artist_image('Post Melone'))
        self.db_class.add_genres([('Jazz', )])
        self.db_class.add_artists([('Post Melone', 'https://www.google.com', 1)])
        self.assertEqual(self.db_class.get_artist_image('Post Melone'),
                         'https://www.google.com')

if __name__ == '__main__':
    unittest.main()