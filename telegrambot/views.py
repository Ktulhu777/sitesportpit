from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from .serializers import TelegramSerializer
from rest_framework.response import Response


class TelegramViews(APIView):
    def put(self):
        telegram_id = self.kwargs.get('telegram_id')
        user = get_user_model().objects.get(pk=1)
        user.telegram_id = telegram_id
        user.save()
        return Response({'detail': 'Данные успешно сохранены'})


def func(request, telegram):
    telegram_id = telegram
    print(telegram_id)
    user = get_user_model().objects.get(username='user')
    print(user)
    user.telegram_id = telegram_id

    user.save()
    return Response({'detail': 'Данные успешно сохранены'})