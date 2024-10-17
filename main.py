"""main script"""

import pandas as pd
import matplotlib.pyplot as plt
import time
from my_packages import web_logger, api_logger, save_data

# define header for HTTP request

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'From': 'aram.sajdak@gmail.com'
        }

# initialize the database with tables

my_class = save_data.MBPostgres(host='localhost', user='postgres', password='123', db_name='musicbrainz')

# scrape artist names and feed them into the artists table

artists = web_logger.web_scrape(headers=headers)

my_class.add_artists(artists)

# fetch the artist id and name from artists table

artist_table = my_class.get_artists()

# for each artist, fetch the events from the API and save them together with the artist id

for _, row in artist_table.iterrows():
    # set delay in HTTP requests to prevent getting blocked, musicbrainz API limit is 1 request per second
    time.sleep(2)

    events = api_logger.api_events(row['id'], row['name'], headers=headers)

    my_class.add_events(events)

# get number of events for every artist

df = my_class.get_event_count()
df_sorted = df.sort_values(by=['event_count'])

# close connection

my_class.close_connection()

# plot everything

plt.barh(y=df_sorted['name'][:16], width=df_sorted['event_count'][:16])
plt.xlabel('Number of events')
plt.tight_layout()
plt.savefig('event_count_1.png')
plt.close()

plt.barh(y=df_sorted['name'][16:], width=df_sorted['event_count'][16:])
plt.xlabel('Number of events')
plt.tight_layout()
plt.savefig('event_count_2.png')
plt.close()

# save to csv

df_sorted.to_csv('event_count.csv')