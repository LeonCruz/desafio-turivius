"""Crawler para pegar as informações do site http://books.toscrape.com."""
from asyncio import gather, run
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from httpx import AsyncClient
from requests import get, post

URL_BASE = "http://books.toscrape.com/catalogue/"
CATEGORY = "category/books/sequential-art_5/"

URL = urljoin(URL_BASE, CATEGORY)


def get_urls(page=None):
    """Retorna uma lista com os links dos livros da página."""
    print("Pegandos urls dos livros")
    if page is not None:
        url = urljoin(URL, page)
        html = get(url).content
    else:
        html = get(URL).content

    soup = BeautifulSoup(html, "html.parser")

    links = []
    for a in soup.select("h3 > a"):
        links.append(a)

    try:
        next_page = soup.select_one("li.next > a")["href"]
    except TypeError as e:
        return links, 0

    return links, next_page


async def get_book_information(book):
    """Retorna as informações de cada livro."""
    print(f"Pegando informações do livro {book['title']}")
    url = urljoin(URL_BASE, urljoin("catalogue/", book["href"]))

    async with AsyncClient() as client:
        html = await client.get(url)

    soup = BeautifulSoup(html, "html.parser")

    title = soup.find("h1").text
    price = soup.find("p", class_="price_color").text.removeprefix("£")
    tag_description = soup.find("div", id="product_description")
    description = tag_description.find_next_sibling("p").text

    return dict(title=title, price=price, description=description, url=url)


def save_book(book):
    """Função que envia os livros para a api."""
    api_url = "http://localhost:8000/books/"
    response = post(api_url, data=book)
    if response.status_code == 201:
        print(f"O livro {book['title']} foi salvo com sucesso")


async def main():
    """Função principal."""
    links, next_page = get_urls()

    books = []
    while True:
        book = await gather(*[get_book_information(link) for link in links])
        books.extend(book)

        if next_page == 0:
            break

        links, next_page = get_urls(next_page)

    for book in books:
        save_book(book)

    print(f"Total de livros salvos: {len(books)}")


run(main())
