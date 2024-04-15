from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя (User).
    Этот сериализатор исключает поле пароля.
    """
    class Meta:
        model = User
        exclude = ('password', )

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=20, required=True, write_only=True)
    password2 = serializers.CharField(min_length=8, max_length=20, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'password2', 'avatar')

    def validate(self, obj):
        password = obj['password']
        password2 = obj.pop('password2')
        if password2 != password:
            raise serializers.ValidationError('Пароли не совпадают')
        validate_password(password)
        return obj

    def create(self, validated_data: dict) -> User:
        """
        Создание нового пользователя.

        Параметры:
        - validated_data: Валидированные данные.

        Возвращает:
        - Новый пользователь.
        """
        user = User.objects.create_user(**validated_data)
        return user
