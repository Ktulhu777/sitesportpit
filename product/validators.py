from rest_framework.exceptions import ValidationError
from .models import LikeProduct


class ValidateBasics:

    def validate_like(self, attrs: bool) -> bool | ValidationError:
        if attrs is not True:
            raise ValidationError('Значение обязательно должно быть "True". ')
        elif LikeProduct.objects.filter(user=self.initial_data['user']).exists():
            raise ValidationError('Вы уже поставили лайк')
        return attrs

    def validate_product_review(self, attrs):
        if not attrs:
            raise ValidationError('Это поле не может быть пустым')
        return attrs
