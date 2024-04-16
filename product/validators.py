from rest_framework.exceptions import ValidationError


class ValidateBasics:

    def validate_product_review(self, attrs):
        if not attrs:
            raise ValidationError('Это поле не может быть пустым')
        return attrs
