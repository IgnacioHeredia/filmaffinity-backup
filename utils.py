"""
Utils to parse FilmAffinity webpage
"""
import re
import time

from bs4 import BeautifulSoup
import requests
from rich import print


session = requests.Session()
session.headers.update(
    {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
    }
)


def check_user(
        user_id: str,
    ):
    """
    Check that the provided user_id does indeed exist.
    """
    url = f'https://www.filmaffinity.com/es/userlists.php?user_id={user_id}'
    response = session.get(url, verify=True)
    if response.status_code != 200:
        raise Exception(
            "The user ID you provided does not exists. Could not find: \n" \
            f"    {url}"
            )


def get_user_lists(
        user_id: str,
    ):
    """
    Retrieve list from a user
    """
    user_lists = {}
    page = 1
    while True:
        url = f'https://www.filmaffinity.com/es/userlists.php?user_id={user_id}&p={page}'

        # Check for pagination end
        response = session.get(url, verify=True)
        if response.status_code != 200:
            break

        print(f'  [grey50]Parsing page {page}[/grey50]')
        soup = BeautifulSoup(response.text, "html.parser")
        lists = soup.find(attrs={'class': 'user-lists'})
        for tmp in lists.find_all('li'):
            ele = tmp.find(
                lambda tag: tag.name == "a" and tag.get("class", []) != ["ls-imgs"]
                )
            user_lists[ele.text] = ele['href']

        page += 1
        time.sleep(5)  # sleep to avoid IP block

    return user_lists


def get_list_movies(
        base_url: str,
        order_by: str ='voto',
    ):
    categories = {
        "posición": 0,
        "título": 1,
        "año": 2,
        "voto": 3,
        "nota media": 4,
    }
    order_id = categories[order_by]

    info = {
        'title': [],
        'year': [],
        'country': [],
        'user score': [],
        'FA score': [],
        'FA movie ID': [],
        'directors': [],
    }

    page = 1
    while True:
        url = f'{base_url}&page={page}&orderby={order_id}'

        # Check for pagination end
        response = session.get(url, verify=True)
        if response.status_code != 200:
            break

        print(f'  [grey50]Parsing page {page}[/grey50]')
        soup = BeautifulSoup(response.text, "html.parser")

        # Find list title
        if page == 1:
            ele = soup.find(attrs={'class': 'list-name-desc'})
            title = ele.text.split(':')[1].strip()

        # Parse movies
        movies = soup.find('ul', attrs={'class': 'movies_list'})
        for movie in movies.find_all('li'):
            info['FA movie ID'].append(
                movie['data-movie-id']
            )
            info['FA score'].append(
                movie.find(attrs={'class': 'avgrat-box'}).text
            )
            info['user score'].append(
                movie.find(attrs={'class': 'user-rat-movie'}).text
            )
            directors = movie.find(attrs={'class': 'mc-director'})
            info['directors'].append(
                ', '.join([i.text for i in directors.find_all('a')])
            )

            ele = movie.find(attrs={'class': 'mc-title'})
            info['title'].append(
                ele.find('a').text.strip()
            )
            info['country'].append(
                ele.find('img')['alt'].strip()
            )
            year = ele.find(text=True, recursive=False)
            year = re.search(r'\((\d{4})\)', year).group(1)
            info['year'].append(year)

        page += 1
        time.sleep(5)  # sleep to avoid IP block

    return title, info


def get_watched_movies(
        user_id: str,
    ):
    """
    Retrieve watched movies from a user.
    """
    info = {
        'genre': [],
        'title': [],
        'year': [],
        'country': [],
        'user score': [],
        'FA score': [],
        'FA movie ID': [],
        'directors': [],
    }
    # We enforce orderby=genre so that we can also extract the genre from the list (otherwise not available)
    orderby = 8

    page = 1
    while True:

        url = f'https://www.filmaffinity.com/es/userratings.php?user_id={user_id}&p={page}&orderby={orderby}'

        # Check for pagination end
        response = session.get(url, verify=True)
        if response.status_code != 200:
            break

        print(f'  [grey50]Parsing page {page}[/grey50]')
        soup = BeautifulSoup(response.text, "html.parser")

        groups = soup.find_all('div', attrs={'class': 'user-ratings-wrapper'})
        for group in groups:
            genre = group.find('div', attrs={'class': 'user-ratings-header'})
            genre = genre.text.split(':')[1].strip()

            movies = group.find_all('div', attrs={'class': 'user-ratings-movie'})
            for movie in movies:
                info['genre'].append(genre)

                info['user score'].append(
                    movie.find(attrs={'class': 'ur-mr-rat'}).text
                )

                movie = movie.find('div', attrs={'class': 'movie-card'})

                info['FA movie ID'].append(
                    movie['data-movie-id']
                )
                info['FA score'].append(
                    movie.find(attrs={'class': 'avgrat-box'}).text
                )
                info['title'].append(
                    movie.find(attrs={'class': 'mc-title'}).find('a').text.strip()
                )
                info['country'].append(
                    movie.find('img', attrs={'class': 'nflag'})['alt'].strip()
                )
                # There are several year fields, keep the first non-zero one
                years = movie.find_all('span', attrs={'class': 'mc-year'})
                info['year'].append(
                    [i.text for i in years if i.text][0]
                )

                directors = movie.find(attrs={'class': 'mc-director'})
                info['directors'].append(
                    ', '.join([i.text for i in directors.find_all('a')])
                )

        page += 1
        time.sleep(5)  # sleep to avoid IP block

    return info
