from bs4 import BeautifulSoup
import requests
import api


def scrape_ny():

    url = 'https://www.nytimes.com/books/best-sellers/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    h3_tags = soup.findAll('h3', itemprop='name')
    p_tags = soup.findAll('p', itemprop='author')

    h = [h3.text for h3 in h3_tags]
    p = [p.text[3:] for p in p_tags]
    zip_list = list(zip(h, p))

    # print(zip_list)

    return zip_list


def get_all_book_data_by_source(source):
    if source == 'nyt':
        book_list = scrape_ny()
        all_book_data = []

        for title, author in book_list:
            raw_book_data = api.request_api_data(title=title, author=author)
            all_book_data.append(raw_book_data)
            # print(title, author)

            # print(raw_book_data)

        print(all_book_data)


if __name__ == '__main__':

    get_all_book_data_by_source('nyt')
