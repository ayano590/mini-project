import requests
import pandas as pd
from bs4 import BeautifulSoup

def web_scrape():

    url = 'https://jazzfuel.com/best-jazz-albums/'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'From': 'aram.sajdak@gmail.com'  # This is another valid field
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Parsing the HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            div = soup.body.find('div', class_='site grid-container container hfeed')
            article = div.find('div', class_='inside-article')
            content = article.find('div', class_='entry-content')
            album = []
            for val in content.findAll('h2'):
                rm_enum = val.text.split('. ', maxsplit=1)
                if len(rm_enum) == 1:  # unwanted h2 element not belonging to the list
                    continue
                rm_colon = rm_enum[-1].split(': ', maxsplit=1)
                album.append(rm_colon[-1])

            df = pd.DataFrame({'Album Name': album})

            return df

        else:
            print(f'ERROR: Connection unsuccessful: {response.status_code}')

        return

    except Exception as e:
        print(f'ERROR: {e}')