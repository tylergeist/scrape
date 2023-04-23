from bs4 import BeautifulSoup
import requests
import api


def scrape_ny():

    url = 'https://www.nytimes.com/books/best-sellers/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    h3_tags = soup.findAll('h3', itemprop='name')
    p_tags = soup.findAll('p', itemprop='author')

    book_arr = []

    for h3 in h3_tags:
        for p in p_tags:
            title = h3.text
            author = p.text[3:]

            book_arr.append((title, author))

    return book_arr


def get_all_book_data_by_source(source):
    if source == 'nyt':
        book_list = scrape_ny()

        for book in book_list:
            raw_book_data = api.request_api_data(title=book[0], author=book[1])

            print(raw_book_data)


if __name__ == '__main__':

    get_all_book_data_by_source('nyt')
