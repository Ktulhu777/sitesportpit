from rest_framework import status, mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.views import APIView

from .service import Cart
from product.models import Product
from .models import Order
from .serializers import OrderSerializer
from .permissions import OrderPermissions


class CartAPI(APIView):
    """Единый API для обработки операций с корзиной"""

    def get(self, request, format=None):
        cart = Cart(request)

        return Response(
            {'cart': list(cart.__iter__()),
             'cart_total_price': cart.get_total_price(),
             'cart_total_discount_price': cart.get_total_discount_price(),
             },
            status=status.HTTP_200_OK
        )

    def post(self, request, **kwargs):
        cart = Cart(request)

        product = request.data
        if Product.objects.filter(id=product['product']['id']).exists():
            cart.add(
                product=product['product'],
                quantity=product['quantity'],
                overide_quantity=product['overide_quantity'] if 'overide_quantity' in product else False
            )
        else:
            return Response(
                {'message': 'Такого товара нет'},
                status=status.HTTP_202_ACCEPTED)

        return Response(
            {'message': 'Корзина обновлена'},
            status=status.HTTP_202_ACCEPTED)

    def delete(self, request, **kwargs):
        cart = Cart(request)

        if 'remove' in request.data:
            product = request.data['product']
            cart.remove(product)
            return Response(
                {'message': 'Товар удален'},
                status=status.HTTP_202_ACCEPTED)

        elif 'clear' in request.data:
            cart.clear()
            return Response(
                {'message': 'Корзина очищена'},
                status=status.HTTP_202_ACCEPTED)


class OrderView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = OrderPermissions,

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
