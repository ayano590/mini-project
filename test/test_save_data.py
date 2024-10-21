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

    def test_add_get_artists(self):
        with self.assertRaises(save_data.DatabaseError):
            self.db_class.get_artists()
        self.db_class.add_artists([('Post Melone', ), ('Ayran Grande', )])
        data = {'id': [1, 2], 'name': ['Post Melone', 'Ayran Grande']}
        df = pd.DataFrame(data)
        self.assertTrue(self.db_class.get_artists().equals(df))

    def test_add_get_events(self):
        with self.assertRaises(save_data.DatabaseError):
            self.db_class.get_events()
        self.db_class.add_artists([('Post Melone',), ('Ayran Grande',)])
        self.db_class.add_events([(1, 'The Best Festival', '2050-07-12', '2052-03-11')])
        data = {'id': [1], 'artist_id': [1], 'event_name': ['The Best Festival'],
                'begin_time': ['2050-07-12'], 'end_time': ['2052-03-11']}
        df = pd.DataFrame(data)
        self.assertTrue(self.db_class.get_events().equals(df))
        self.assertIsNone(self.db_class.get_event_by_artist('Ayran Grande'))

    def test_get_event_count(self):
        with self.assertRaises(save_data.DatabaseError):
            self.db_class.get_event_count()
        self.db_class.add_artists([('Post Melone',), ('Ayran Grande',)])
        self.db_class.add_events([(1, 'The Best Festival', '2050-07-12', '2052-03-11')])
        data = {'name': ['Post Melone'], 'event_count': [1]}
        df = pd.DataFrame(data)
        self.assertTrue(self.db_class.get_event_count().equals(df))

if __name__ == '__main__':
    unittest.main()