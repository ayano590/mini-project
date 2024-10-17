import requests

def api_events(num, artist, headers):

    if ' and ' in artist:
        artist = artist.split(' and ')
    elif ' & ' in artist:
        artist = artist.split(' & ')

    root_url = 'https://musicbrainz.org/ws/2/'

    if isinstance(artist, list):
        url = root_url + f'event?query=(+"{artist[0]}" +"{artist[1]}")&limit=100&fmt=json'
    else:
        url = root_url + f'event?query="{artist}"&limit=100&fmt=json'

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:

            event_json = response.json()['events']
            event_name = [i['name'] for i in event_json]
            event_begin = [i['life-span']['begin'] for i in event_json]
            event_end = [i['life-span']['end'] for i in event_json]
            num_list = [num for _ in range(len(event_json))]
            events_zip = zip(num_list, event_name, event_begin, event_end)
            events = (i for i in events_zip)
            return events

        else:
            print(f'ERROR: Unsuccessful request: {response.status_code}')

        return

    except Exception as e:
        print(f'ERROR: {e}')