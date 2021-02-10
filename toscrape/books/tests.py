# from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from books.models import Book


# Create your tests here.
class BooksTestCase(APITestCase):
    fixtures = ["books.json"]

    def test_get_list_of_books(self):
        response = self.client.get("/books/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 20)

    def test_get_a_book_by_id(self):
        response = self.client.get("/books/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)

    def test_get_a_book_by_url_api(self):
        response = self.client.get("/books/")
        results = response.data["results"]
        url = results[0]["url_api"]

        response2 = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 6)

    def test_create_a_book(self):
        book = dict(
            title="Título",
            price=50.0,
            description="Alguma descrição",
            url="http://urldolivro.com",
        )
        response = self.client.post("/books/", data=book, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 6)

    def test_change_a_book_title(self):
        book = self.client.get("/books/1/")
        old_title = book.data["title"]

        new_title = dict(title="Novo título")

        response = self.client.patch("/books/1/", data=new_title)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        book = self.client.get("/books/1/")
        self.assertNotEqual(book.data["title"], old_title)

    def test_change_a_book_price(self):
        book = self.client.get("/books/1/")
        old_price = book.data["price"]

        new_price = dict(price=500.0)

        response = self.client.patch("/books/1/", data=new_price)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        book = self.client.get("/books/1/")
        self.assertNotEqual(book.data["price"], old_price)

    def test_delete_a_book(self):
        old_total = Book.objects.count()

        response = self.client.delete("/books/1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        new_total = Book.objects.count()

        self.assertNotEqual(old_total, new_total)
