from bs4 import BeautifulSoup
import requests
import api


def scrape_reedsy():
    url = 'https://reedsy.com/discovery/blog/best-books-to-read-in-a-lifetime'
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    div_tags = soup.findAll('div', class_='title')

    title_list = []
    author_list = []

    for div in div_tags:
        em = div.find('h2').find('em')
        h2 = div.find('h2').text
        h2_split = h2.split('by')
        title = em.text
        author = h2_split[1].strip()

        title_list.append(title)
        author_list.append(author)

    zip_list = list(zip(title_list, author_list))
    print(zip_list)

    return zip_list


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

    if source == 'reedsy':
        book_list = scrape_reedsy()
        all_book_data = []

        for title, author in book_list:
            raw_book_data = api.request_api_data(title=title, author=author)
            all_book_data.append(raw_book_data)


if __name__ == '__main__':

    get_all_book_data_by_source('reedsy')
    # get_all_book_data_by_source('nyt')
    # scrape_amz_lifetime()
    # scrape_reedsy()
