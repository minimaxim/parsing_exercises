import requests
from bs4 import BeautifulSoup as bs

# получаем код страницы
get_html = requests.get('https://books.toscrape.com/')
# print(get_html.status_code)
# почитать коды состояния (тут результат 200)

html = get_html.content
# print(html)
# видно тоже, что я вижу при нажатии на код страницы

soup = bs(html, 'html.parser')
# первое это формат

# print(soup)
# исходный код в удобном виде

sections = soup.select('section')
# тег который хотим получить (может быть много - зависит от названия)

# print(sections)
# print(len(sections))

section = sections[0]
books_block = section.select_one('ol[class=row]')
# select_one - позволяет выбрать один единственный тег. Если их несколько - выберет первый

# print(books_block)

books = books_block.select('li')
# print(len(books))
# по тегу li мы отделили код книг на странице. Их 20 на сайте

books_data = []
for book in books:
    image = 'https://books.toscrape.com/' + book.find('div', attrs={'class': 'image_container'}).find('img')['src']
    title = book.find('h3').find('a')['title']
    price = book.find('p', attrs={'class': 'price_color'}).text
    book_dict = {
        'image': image,
        'title': title,
        'price': price
    }
    books_data.append(book_dict)

print(len(books_data))

# проверять статусы кода

get_html = requests.get('https://books.toscrape.com/catalogue/page-1.html')
if get_html.status_code == 200:
    soup = bs(get_html.content, 'html.parser')
    next_page = 'https://books.toscrape.com/catalogue/' + soup.find('li', attrs={'class': 'next'}).find('a')['href']
    # print(next_page)

    get_next_html = requests.get(next_page)
    if get_next_html.status_code == 200:
        print(get_next_html.content)


def get_books(content):
    soup = bs(content, 'html.parser')
    ol = soup.find('ol', attrs={'class': 'row'})
    books = ol.select('li')

    books_data = []
    for book in books:
        image = 'https://books.toscrape.com/' + book.find('div', attrs={'class': 'image_container'}).find('img')['src']
        title = book.find('h3').find('a')['title']
        price = book.find('p', attrs={'class': 'price_color'}).text

        book_dict = {
            'image' : image,
            'title' : title,
            'price' : price
        }
        books_data.append(book_dict)

    return books_data


def get_next_page(content):
    soup = bs(content, 'html.parser')
    try:
        next_page = 'https://books.toscrape.com/catalogue/' + soup.find('li', attrs={'class': 'next'}).find('a')['href']
        return next_page
    except:
        pass

final_data = []
page_number = 1
url = 'https://books.toscrape.com/catalogue/page-1.html'
get_html = requests.get(url)
if get_html.status_code == 200:
    while True:
        books = get_books(get_html.content)
        print(f"получено {len(books)} с {page_number} страницы")
        final_data += books

        next_page = get_next_page(get_html.content)
        if next_page:
            page_number += 1
            get_html = requests.get(next_page)
            if get_html.status_code == 200:
                print(f"начинается парсинг {page_number} страницы")
        else:
            break

print(f"Данные спарсились: {page_number} страниц, {len(final_data)} книг")

