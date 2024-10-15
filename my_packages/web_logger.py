import requests
import pandas as pd
from bs4 import BeautifulSoup

def web_scrape():

    url = 'https://jazzfuel.com/best-jazz-albums/'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            # Parsing the HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            div = soup.body.find('div', class_='site grid-container container hfeed')
            article = div.find('div', class_='inside-article')
            content = article.find('div', class_='entry-content')
            album = []
            for val in content.findAll('h2'):
                rm_enum = val.text.split('. ', maxsplit=1)
                rm_colon = rm_enum.split(': ', maxsplit=1)
                album.append(rm_colon[-1])

            df = pd.DataFrame({'Album Name': album})

            return df

        else:
            print(f'ERROR: Connection unsuccessful: {response.status_code}')

        return

    except Exception as e:
        print(f'ERROR: {e}')