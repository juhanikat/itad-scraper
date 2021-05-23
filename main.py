# WORK IN PROGRESS

import bs4
import requests


def html_class_filter(html_class: str, list: list):
    new_list = []
    list = str(list)
    soup = bs4.BeautifulSoup(list, 'html.parser')
    for tag in soup.find_all():
        if html_class in str(tag.get('class')):
            new_list.append(tag)
    return new_list


while True:
    print('')
    print('Search for a game. Input "q" to exit.')
    syote = input()
    if syote.lower() == 'q':
        break

    res = requests.get(f'https://isthereanydeal.com/search/?q={syote}', timeout=10)
    res.raise_for_status()

    my_soup = bs4.BeautifulSoup(res.text, 'html.parser')
    selection = my_soup.find_all()

    game_not_found = html_class_filter('widget__nodata', selection)
    if game_not_found:
        print('Game not found. Check your input for typos.')
        continue

    game_title = None
    price_tags = None
    stores = None

    selection = my_soup.select('div')
    cards = html_class_filter('card-container', selection)
    for card in cards:
        price_tags = html_class_filter('numtag__primary', card)
        if not price_tags:
            continue
        game_title = html_class_filter('card__title', card)[0].text
        stores = html_class_filter('shopTitle', card)
        break

    if not price_tags or not stores or not game_title:
        print('Error, please try again.')
        continue

    historical_low = price_tags[0].text
    historical_low_store = stores[0].text

    current_best = ''
    current_best_store = ''
    if len(price_tags) > 1:
        current_best = price_tags[1].text
        current_best_store = stores[1].text

    print('')
    print(game_title)
    if not current_best:
        print(f'Current best price: No data')
    else:
        print(f'Current best price: {current_best} on {current_best_store}')
    print(f'Historical low: {historical_low} on {historical_low_store}')
    print('')
