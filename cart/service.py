from decimal import Decimal
from django.conf import settings
from .serializers import CartSerializer
from product.models import Product


class Cart:
    def __init__(self, request):
        """ Инициализируем корзину """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохраняем пустую корзину в сеансе
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        self.session.modified = True

    def add(self, product, quantity=1, overide_quantity=False):
        """Добавляем продукт в корзину и обновляем количество"""

        product_id = str(product['id'])
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0}

        if overide_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        """Удаляем продукт из корзины"""
        product_id = str(product['id'])

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Перебираем товары в корзине и получаем продукты из базы данных."""
        product_ids = self.cart.keys()
        products = Product.published.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = CartSerializer(product).data

        for item in cart.values():
            item['total_price'] = item['product']['price'] * item['quantity']
            yield item

    def __len__(self):
        """Количество товаров в корзине"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['product']['price']) * item['quantity'] for item in self.cart.values())

    def get_total_discount_price(self):
        summ = 0
        for item in self.cart.values():
            if item['product']['discount_price']:
                summ += Decimal(item['product']['discount_price']) * item['quantity']
            else:
                summ += Decimal(item['product']['price']) * item['quantity']
        return summ

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.save()
