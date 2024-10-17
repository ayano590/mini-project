"""main script"""

from my_packages import web_logger, api_logger, save_data

my_class = save_data.MBPostgres(db_name='musicbrainz', user='postgres', password='123', host='localhost')

artists = web_logger.web_scrape()

my_class.add_artists(artists)

# til here it should work, fingers crossed

# next step is to fetch the artist id and name, in order to give them to api_events

artist_table = my_class.get_artists()

for _, row in artist_table.iterrows():
    events = api_logger.api_events(row['id'], row['name'])

    # then feed the events data into the events table

    my_class.add_events(events)