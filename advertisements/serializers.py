from django.contrib.auth.models import User
from django_filters import DateFromToRangeFilter
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    created_at = DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at')
        # read_only_fields = ('id', 'creator', 'created_at')

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        print(validated_data)
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        if len(list(Advertisement.objects.filter(creator=self.context['request'].user, status='OPEN'))) >= 10:
            if self.context['request'].method == 'POST':
                raise ValidationError('Too much open advertisements')
            elif self.context['request'].method == 'PATCH':
                _data = dict(data)
                if _data.get('status', False) == 'CLOSED':
                    return data
            raise ValidationError('Too much open advertisements')
        return data
