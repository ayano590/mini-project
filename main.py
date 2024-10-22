"""main script"""

import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from tqdm import tqdm
from PIL import Image
from my_packages import web_logger, api_logger, save_data, db_config

# define header for HTTP request

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'From': 'aram.sajdak@gmail.com'
        }

# initialize the database with tables

print('Connecting to the database...')

my_class = save_data.MBPostgres(host=db_config.DB_HOST, user=db_config.DB_USER,
                                password=db_config.DB_PASSWORD, db_name=db_config.DB_NAME)

# scrape artist names and feed them into the artists table

print('Scraping the artist names...')

artists = web_logger.web_scrape(headers=headers)

print('Adding artists to the database...')

my_class.add_artists(artists)

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

# get number of events for every artist

print('Getting event count from the database...')

df = my_class.get_event_count()
df_sorted = df.sort_values(by=['event_count'])

# get events for a specific artist

artist_name = input('Enter artist name: ')

artist_events = my_class.get_event_by_artist(artist_name)

artist_img = my_class.get_artist_image(artist_name)

pd.set_option('display.max_colwidth', None)

if isinstance(artist_events, pd.DataFrame):
    print(artist_events)

if artist_img:
    with Image.open(requests.get(artist_img[0], stream=True).raw) as img:
        img.save(f'{artist_name}.png')

# close connection

print('Closing connection...')

my_class.close_connection()

# plot everything

print('Plotting...')

df_list = np.array_split(df_sorted, 5)
count = 1
for i in df_list:

    plt.barh(y=i['name'], width=i['event_count'])
    plt.xlabel('Number of events')
    plt.tight_layout()
    plt.savefig(f'event_count_{count}.png')
    plt.close()
    count += 1

# save to csv

print('Saving to csv...')

df_sorted.to_csv('event_count.csv')