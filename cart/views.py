from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.service import Cart


class CartAPI(APIView):
    """Единый API для обработки операций с корзиной"""

    def get(self, request, format=None):
        cart = Cart(request)

        return Response(
            {"cart": list(cart.__iter__()),
             'cart_total_price': cart.get_total_price(),
             'cart_total_discount_price': cart.get_total_discount_price(),
             },
            status=status.HTTP_200_OK
        )

    def post(self, request, **kwargs):
        cart = Cart(request)

        if 'remove' in request.data:
            product = request.data['product']
            cart.remove(product)

        elif 'clear' in request.data:
            cart.clear()

        else:
            product = request.data
            cart.add(
                product=product['product'],
                quantity=product['quantity'],
                overide_quantity=product['overide_quantity'] if 'overide_quantity' in product else False
            )

        return Response(
            {'message': 'Корзина обновлена'},
            status=status.HTTP_202_ACCEPTED)
