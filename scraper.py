import bs4
import requests


def main():
    def open_page(url):
        try:
            res = requests.get(url, timeout=7)
            res.raise_for_status()
            return res
        except requests.Timeout:
            print(f"Connection timed out when accessing {url} !")
        except requests.ConnectionError as e:
            print(f"ConnectionError when accessing {url} ! Error: {e}")
        except requests.HTTPError as e:
            print(f"HTTPError when accessing {url} ! Error: {e}")
        except requests.TooManyRedirects as e:
            print(f"TooManyRedirects when accessing {url} ! Error: {e}")
            print("Try again.")
        return -1

    while True:
        syote = input('(Input "q" to quit) Search for a game: ')
        if syote.lower() == "q":
            break

        res = open_page(f"https://isthereanydeal.com/search/?q={syote}")
        if res == -1:
            continue
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        card = soup.find("div", {"class": "card-container"})

        if not card:
            print()
            print("Game not found. Check your input for typos.")
            print()
            continue

        game_title = card.find("a", {"class": "card__title"}).text
        price_tags = card.find_all("div", {"class": "numtag__primary"})
        stores = card.find_all("span", {"class": "shopTitle"})
        if not game_title or not price_tags or not stores:
            print("Error, please try again.")
            continue

        historical_low = price_tags[0].text
        historical_low_store = stores[0].text
        current_best = ""
        current_best_store = ""
        if len(price_tags) > 1:
            current_best = price_tags[1].text
            current_best_store = stores[1].text

        print("")
        print(game_title)
        if not current_best:
            print(f"Current best price: No data")
        else:
            print(f"Current best price: {current_best} on {current_best_store}")
        print(f"Historical low: {historical_low} on {historical_low_store}")
        print("")


if __name__ == "__main__":
    main()
