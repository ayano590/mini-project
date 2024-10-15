import requests

def api_events():

    root_url = 'https://musicbrainz.org/ws/2/'

    url = root_url + 'event?query="Ella Fitzgerald"&fmt=json'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'From': 'aram.sajdak@gmail.com'
        }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:

            event_json = response.json()['events']
            events = [(i['name'], i['life-span']['begin'], i['life-span']['end']) for i in event_json]
            return events

        else:
            print(f'ERROR: Unsuccessful request: {response.status_code}')

        return

    except Exception as e:
        print(f'ERROR: {e}')