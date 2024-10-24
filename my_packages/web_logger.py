import requests
from bs4 import BeautifulSoup

def scrape_jazz(headers):

    artists = []
    img = []

    url_jazz = 'https://jazzfuel.com/best-jazz-albums/'

    try:
        response = requests.get(url_jazz, headers=headers)

        if response.status_code == 200:
            # Parsing the HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            div = soup.body.find('div', class_='site grid-container container hfeed')
            article = div.find('div', class_='inside-article')
            content = article.find('div', class_='entry-content')
            for val in content.findAll('h2'):
                rm_enum = val.text.split('. ', maxsplit=1)
                if len(rm_enum) == 1:  # unwanted h2 element not belonging to the list
                    continue
                rm_colon = rm_enum[-1].split(': ', maxsplit=1)
                artists.append(rm_colon[0])

            artists_set = sorted(list(set(artists)))
            img.extend(['-' for _ in artists_set])

            artists_tup = list(zip(artists_set, img))
            return artists_tup

        else:
            raise Exception(f'ERROR: Could not fetch jazz artists')

    except Exception as e:
        print(e)

def scrape_rock(headers):

    artists = []
    img = []

    url_rock = 'https://www.forbes.com/sites/entertainment/article/best-rock-bands/'

    try:
        response = requests.get(url_rock, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            div = soup.body.find('div', class_='article-body fs-article fs-responsive-text current-article')
            for val in div.findAll('h3')[:32]:
                rm_enum = val.text.split('. ', maxsplit=1)
                if len(rm_enum) == 1:
                    continue
                artists.append(rm_enum[1].strip())

            img_list = div.findAll('figure')[1:31]
            for img_ele in img_list:
                img.append(img_ele.find('progressive-image')['src'])

            artists_tup = list(zip(artists, img))
            return artists_tup

        else:
            raise Exception(f'ERROR: Could not fetch rock artists')

    except Exception as e:
        print(e)