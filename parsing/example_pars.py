import requests
from bs4 import BeautifulSoup
import json

URL = 'https://www.hltv.org/results'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.2.615 Yowser/2.5 Safari/537.36',
    'upgrade-insecure-requests': '1'}
PATH = 'hltv.json'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def save_file(data, path):
    with open(path, "w") as write_file:
        json.dump(data, write_file)


def get_content(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('div', class_='results-sublist')
    __games = {}
    for item in items:
        games = item.find_all('div', class_='result-con')
        _games = []
        for game in games:
            teams = game.find_all('div', class_='team')
            _teams = []
            for team in teams:
                _teams.append(team.get_text())
            _games.append({'team1': _teams[0],
                           'team2': _teams[1],
                           'score': game.find('td', class_='result-score').get_text()})
        __games[item.find('span', class_='standard-headline').get_text()] = _games
    return __games


def parse():
    html = get_html(URL)
    # check if we correctly made html request
    if html.status_code == 200:
        days = get_content(html.text)
        save_file(days, PATH)
    else:
        print("Something went wrong")


parse()
