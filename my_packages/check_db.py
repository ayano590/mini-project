"""definition of check_db function"""

import time
from tqdm import tqdm
from . import api_logger

def add_get(my_class, jazz_artists, rock_artists, headers):
    # get genre IDs and insert them into the tuples

    jazz_id = my_class.get_genre_id('Jazz')

    jazz_entries = [(jazz_artists[i][0], jazz_artists[i][1], jazz_id) for i in range(len(jazz_artists))]

    rock_id = my_class.get_genre_id('Rock')

    rock_entries = [(rock_artists[i][0], rock_artists[i][1], rock_id) for i in range(len(rock_artists))]

    print('Adding artists to the database...')

    my_class.add_artists(jazz_entries)

    my_class.add_artists(rock_entries)

    # fetch the artist id and name from artists table

    print('Getting artists from the database...')

    artist_list = my_class.get_artists()

    # for each artist, fetch the events from the API and save them together with the artist id

    print('Fetching events from the API and adding them to the database...')

    # add progress bar, access the df rows accordingly
    for i in tqdm(range(artist_list.shape[0])):
        row = artist_list.iloc[i]
        # set delay in HTTP requests to prevent getting blocked, musicbrainz API limit is 1 request per second
        time.sleep(1.1)

        events = api_logger.api_events(int(row.iloc[0]), row.iloc[1], headers=headers)

        my_class.add_events(events)

    return