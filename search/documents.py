from django_elasticsearch_dsl import Document, fields
from elasticsearch_dsl import analyzer, Index
from django_elasticsearch_dsl.registries import registry
from product.models import Product

product = Index('products')

product.settings(
    number_of_shards=1,
    number_of_replicas=1
)

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


@registry.register_document
@product.document
class ProductDocument(Document):
    """Product Document"""

    id = fields.IntegerField(attr='id')

    name = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )

    description = fields.TextField(
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )

    category = fields.TextField(
        attr='get_category',
        analyzer=html_strip,
        fields={
            'raw': fields.TextField(analyzer='keyword'),
        }
    )

    discount_price = fields.FloatField(attr='discount_price')
    img = fields.FileField(attr='img')

    class Index:
        name = 'products'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Product
        # fields = ('discount',)