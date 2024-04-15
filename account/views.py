from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from core.tasks import send_confirm_email_task

from . import serializers
from .send_mail import send_confirm_email

User = get_user_model()  # CustomUser


class UserViewSet(ListModelMixin, GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.UserSerializer
        elif self.action == 'register':
            return serializers.RegisterSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticated()]
        return [AllowAny()]

    @action(['POST'], detail=False)
    def register(self, request, *args, **kwargs):
        serializer = serializers.RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        try:
            send_confirm_email_task.delay(user.email, user.activation_code)
        except Exception as e:
            print(e, '!!!!!!!!!!!!!!!!!!')
            return Response({'msg': 'Registered, but troubles with email occured!',
                             'data': serializer.data}, status=201)
        return Response({'msg': 'Registered and sent email', 'data': serializer.data}, status=201)

    @action(['GET'], detail=False, url_path='activate/(?P<uuid>[0-9A-Fa-f-]+)')
    def activate(self, request, uuid):
        try:
            user = User.objects.get(activation_code=uuid)
        except User.DoesNotExist:
            return Response({'msg': 'Invalid Link or Link expired'}, status=400)

        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response({'msg': 'Account activated!'}, status=200)












# from django.contrib.auth import get_user_model
# from rest_framework.decorators import action
# from rest_framework.viewsets import GenericViewSet
# from rest_framework.mixins import ListModelMixin
# from rest_framework.response import Response
#
# from core.tasks import send_confirmation_email_task
# from . import serializers
# # from .send_mail import send_confirmation_email
# from rest_framework.permissions import AllowAny, IsAuthenticated
#
#
#
# #hello world
# #ne helloworld
#
# User = get_user_model()
#
# class UserViewSet(ListModelMixin, GenericViewSet):
#     """
#     Viewset для просмотра и редактирования экземпляров пользователей.
#     """
#     queryset = User.objects.all()
#     serializer_class = serializers.UserSerializer
#
#     def get_permissions(self):
#         """
#         Определение разрешений, с которыми должен быть авторизован запрос.
#         """
#         if self.action == 'list':
#             return [IsAuthenticated()]
#         return [AllowAny()]
#
#     @action(['POST'], detail=False)
#     def register(self, request, *args, **kwargs):
#         """
#         Зарегистрировать нового пользователя.
#         """
#         serializer = serializers.RegisterSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         if user:
#             try:
#                 send_confirmation_email_task.delay(user.email, user.activation_code)
#             except Exception as e:
#                 print('!!!!')
#                 return Response({'msg': 'Зарегистрирован, но возникли проблемы с электронной почтой!',
#                                  'data': serializer.data}, status=201)
#         return Response({'message': 'Зарегистрирован и отправлено письмо', 'data': serializer.data},
#                         status=201)
#
#     @action(['GET'], detail=False, url_path='activate/(?P<uuid>[0-9a-zA-Z-]+)')
#     def activate(self, request, uuid):
#         """
#         Активировать аккаунт с использованием кода активации.
#         """
#         try:
#             user = User.objects.get(activation_code=uuid)
#         except User.DoesNotExist:
#             return Response({'message': 'Неверный код активации.'}, status=400)
#
#         user.is_active = True
#         user.activation_code = ''
#         user.save()
#         return Response({'message': 'Аккаунт активирован.'}, status=200)
#
#
