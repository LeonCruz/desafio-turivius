from rest_framework.reverse import reverse
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from books.models import Book


class BookSerializer(ModelSerializer):
    url_api = SerializerMethodField("get_url_api")

    class Meta:
        model = Book
        fields = ["id", "title", "price", "description", "url", "url_api"]

    def get_url_api(self, instance):
        """Campo adicional para exibir o url do livro na api."""
        request = self.context.get("request")
        return reverse("book-detail", args=[instance.id], request=request)
