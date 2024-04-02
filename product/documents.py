from users.models import User
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from product.models import CategoryProduct, Product


@registry.register_document
class UserDocument(Document):
    class Index:
        name = "users"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
        ]


@registry.register_document
class CategoryDocument(Document):
    id = fields.IntegerField()

    class Index:
        name = "categories"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = CategoryProduct
        fields = [
            "cat_name",
        ]


@registry.register_document
class ProductDocument(Document):
    categories = fields.ObjectField(properties={
        "id": fields.IntegerField(),
        "cat_name": fields.TextField(),
    })

    class Index:
        name = "products"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

    class Django:
        model = Product
        fields = [
            "name",
            "description",
            "time_create",
            "time_update",
        ]
