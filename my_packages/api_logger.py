import requests
import time

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

        # if the server is temporarily unavailable
        while response.status_code == 503:
            time.sleep(1.1)
            response = requests.get(url, headers=headers)

        if response.status_code == 200:

            event_num = response.json()['count']

            offset_iter = -(event_num // -100)  # upside down floor division (DIY ceiling division)

            event_name = []
            event_begin = []
            event_end = []

            for i in range(offset_iter):  # for count = 185: offset_iter = 2; i = 0 -> offset = 0; i = 1 -> offset = 100
                time.sleep(1.1)
                response_offset = requests.get(url + f'&offset={i * 100}', headers=headers)

                while response_offset.status_code == 503:
                    time.sleep(1.1)
                    response_offset = requests.get(url + f'&offset={i * 100}', headers=headers)

                if response_offset.status_code == 200:

                    event_json = response.json()['events']

                    event_name.extend([k['name'] for k in event_json])

                    # for some reason <if 'life-span' in i>, <if i['life-span']['end']> do NOT work
                    for j in event_json:
                        if 'life-span' not in j:
                            event_begin.append('-')
                            event_end.append('-')
                        else:
                            if 'begin' not in j['life-span']:
                                event_begin.append('-')
                            else:
                                event_begin.append(j['life-span']['begin'])
                            if 'end' not in j['life-span']:
                                event_end.append('-')
                            else:
                                event_end.append(j['life-span']['end'])

                else:
                    print(f'ERROR at loop {i}')

            num_list = [num for _ in range(len(event_name))]
            events_zip = zip(num_list, event_name, event_begin, event_end)
            events = (i for i in events_zip)
            return events

        else:
            print(f'ERROR: Unsuccessful request: {response.status_code}')

        return

    except Exception as e:
        print(f'ERROR: {e}')