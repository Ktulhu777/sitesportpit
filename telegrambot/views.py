from rest_framework.views import APIView
from rest_framework.response import Response


class TelegramViews(APIView):

    def get(self, request, telegram_id):
        telegram_id = self.kwargs.get('telegram_id')

        user = self.request.user
        if not user.telegram_id:
            user.telegram_id = telegram_id
            user.save()
            return Response({'detail': 'Данные успешно сохранены'})
        return Response({'detail': 'Ваш телеграм уже привязан'})


