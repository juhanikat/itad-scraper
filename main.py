import bs4
import requests


while True:
    syote = input('Search for a game. Input "Q" to quit. ')
    if syote.upper() == 'Q':
        break

    res = requests.get(
        f'https://isthereanydeal.com/search/?q={syote}', timeout=10)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    card = soup.find('div', {'class': "card-container"})

    if not card:
        print()
        print('Game not found. Check your input for typos.')
        print()
        continue

    game_title = card.find('a', {'class': "card__title"}).text
    price_tags = card.find_all('div', {'class': "numtag__primary"})
    stores = card.find_all('span', {'class': "shopTitle"})
    if not game_title or not price_tags or not stores:
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
