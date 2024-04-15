from rest_framework.exceptions import ValidationError
from .models import LikeProduct


class ValidateBasicsLike:

    def validate_like(self, attrs: bool) -> bool | ValidationError:
        if attrs is not True:
            raise ValidationError('Значение обязательно должно быть "True". ')
        elif LikeProduct.objects.filter(user=self.initial_data['user']).exists():
            raise ValidationError('Вы уже поставили лайк')
        return attrs
