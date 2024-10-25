"""main script"""

import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from my_packages import web_logger, save_data, db_config, check_db

# define header for HTTP request

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                      '(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'From': 'aram.sajdak@gmail.com'
        }

# initialize the database with tables

print('Connecting to the database...')

my_class = save_data.MBPostgres(host=db_config.DB_HOST, user=db_config.DB_USER,
                                password=db_config.DB_PASSWORD, db_name=db_config.DB_NAME)

# add genres Jazz and Rock to the genres table

genres = [('Jazz', ), ('Rock', )]

my_class.add_genres(genres=genres)

# scrape artist names

print('Scraping the artist names...')

jazz_artists = web_logger.scrape_jazz(headers=headers)

rock_artists = web_logger.scrape_rock(headers=headers)

# check if all artists are already in the database

for i in jazz_artists + rock_artists:
    check = my_class.get_artist_by_name(i)
    if not check:
        check_db.add_get(my_class=my_class, jazz_artists=jazz_artists,
                         rock_artists=rock_artists, headers=headers)
        break

print('All artists are in the database')

# get all events

print('Getting events from the database...')

df = my_class.get_events()

# get number of events for every artist

print('Getting event count from the database...')

df_count = my_class.get_event_count()
df_count_sorted = df_count.sort_values(by=['event_count'])

# get number of events per genre

print('Getting event count per genre from the database...')

df_genre = my_class.get_event_count_per_genre()

# get events for a specific artist

artist_name = input('Enter artist name: ')

artist_events = my_class.get_event_by_artist(artist_name)

artist_img = my_class.get_artist_image(artist_name)

pd.set_option('display.max_colwidth', None)

if isinstance(artist_events, pd.DataFrame):
    print(artist_events)

if artist_img:
    with Image.open(requests.get(artist_img[0], stream=True).raw) as img:
        img.save('artist.png')

# close connection

print('Closing connection...')

my_class.close_connection()

# plot everything

print('Plotting...')

df_jazz = df_count_sorted[df_count_sorted['genre'] == 'Jazz']
df_rock = df_count_sorted[df_count_sorted['genre'] == 'Rock']

df_jazz_list = np.array_split(df_jazz, 3)

j_count = 1
for i in df_jazz_list:

    plt.barh(y=i['name'], width=i['event_count'])
    plt.xlabel('Number of events')
    plt.title('Jazz artists')
    plt.tight_layout()
    plt.savefig(f'jazz_events_{j_count}.png')
    plt.close()
    j_count += 1

df_rock_list = np.array_split(df_rock, 2)

r_count = 1
for i in df_rock_list:

    plt.barh(y=i['name'], width=i['event_count'])
    plt.xlabel('Number of events')
    plt.title('Rock bands')
    plt.tight_layout()
    plt.savefig(f'rock_events_{r_count}.png')
    plt.close()
    r_count += 1

plt.bar(x=df_genre['name'], height=df_genre['event_count'], width=0.4)
plt.title('Jazz vs Rock')
plt.tight_layout()
plt.savefig(f'jazz_vs_rock.png')
plt.close()

# save event list to csv

print('Saving to csv...')

df.to_csv('events.csv')