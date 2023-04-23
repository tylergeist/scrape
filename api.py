import json
import requests


def get_google_book_by_isbn(isbn):
    try:
        url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&printType=books'

        response = requests.get(url)
        resp_obj = json.loads(response.text)
        item = resp_obj['items'][0]
        info = item['volumeInfo']
        cover_id = item['id']
        google_keys = ['title', 'authors', 'pageCount',
                       'categories', 'description', 'averageRating', 'publisher']
        book = {}
        for gkey in google_keys:
            if gkey == 'authors':
                tmp = info.get(gkey, None)[0]
            else:
                tmp = info.get(gkey, None)
            book[gkey] = tmp

        book_out = {
            'coverId': cover_id,
            'title': book.get('title'),
            'author': book.get('authors'),
            'isbn': isbn,
            'pages': book.get('pageCount'),
            'category': book.get('categories'),
            'description': book.get('description'),
            'rating': str(book.get('averageRating')),
            'publisher': book.get('publisher'),
        }

        return book_out
    except KeyError:
        return


def request_api_data(title, author):

    url = f'https://openlibrary.org/search.json?title={title}&author={author}'
    response = requests.get(url)
    res = response.json()

    if res['numFound'] == 0:
        with open('failed_books.txt', 'a') as f:
            f.write(f'{title}, {author} \n')
            return

    isbn_list = res['docs'][0]['isbn']
    isbn = ''
    for i in isbn_list:
        if len(i) == 13 and i[0] == '9':
            isbn = i
            break

    # print(isbn)

    book_data = get_google_book_by_isbn(isbn)

    print(book_data)

    return book_data


# request_api_data('The Alchemist', 'Paulo Coelho')
