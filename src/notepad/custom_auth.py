import json
from random import choice
from string import ascii_letters, digits, punctuation

import requests
from django.conf import settings
from django.contrib.auth.hashers import make_password

from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import F
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import authentication
from rest_framework import exceptions

from notepad.models import CountAccess
from notepad.settings.base import CHECK_TOKEN_URL_BASE, REQUEST_TIME_OUT


def write_log_access(request):
    id_access = CountAccess.objects.all()

    with transaction.atomic():
        if not id_access.exists():
            CountAccess.objects.create()
        CountAccess.objects.all().update(counter=F('counter') + 1)

    request_params = json.loads(request.body)
    type_request = request_params.get('method_api')
    value_request = request.method + ' ' + request.path + ' ' + ' '.join([str(k + '=' + str(v)) for k, v in request_params.items()])

    with open(str(settings.VAR_PATH / 'logs' / 'access' / 'log_{}.log'.format(timezone.now().date())), 'ab') as f:
        f.write(
            bytes('{date_time} - id: {id} - type: {type} - value: {value}\n'.format(
                date_time=timezone.now(),
                id=CountAccess.objects.all()[0].counter,
                type=type_request,
                value=value_request

                ), encoding='utf-8'
            )
        )


class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        write_log_access(request)
        if request.method == 'POST' and request.is_secure():
            try:
                data = json.loads(request.body)
                token = data.get('token')
                user_id = data.get('user_id')
                method_api = data.get('method_api')
                if method_api:
                    request.method = method_api
            except:
                raise exceptions.AuthenticationFailed('Пользователь не найден')

            if not token or not user_id:
                return None

            try:
                response = requests.get(
                    url=CHECK_TOKEN_URL_BASE,
                    data={'token': token},
                    json=True,
                    timeout=REQUEST_TIME_OUT)

                if response.status_code == HttpResponse.status_code:
                    try:
                        response = response.json()
                        result = response['result']
                        if result in 'token invalid токен некорректный':
                            raise exceptions.AuthenticationFailed('Пользователь не найден')

                        user_id_response = response['user_id']
                        if user_id_response != user_id:
                            raise exceptions.AuthenticationFailed('Пользователь не найден')
                    except:
                        raise exceptions.AuthenticationFailed('Пользователь не найден')
            except:
                raise exceptions.AuthenticationFailed('Пользователь не найден')

            try:
                user = User.objects.get(username=settings.ADMIN_LOGIN)
            except User.DoesNotExist:
                symbols = []

                symbols.extend(ascii_letters)
                symbols.extend(punctuation)
                symbols.extend(digits)

                user = User(
                    username=settings.ADMIN_LOGIN,
                    password=make_password(
                        ''.join(choice(symbols) for _ in range(20)),
                        salt=None,
                        hasher='default')
                )
                user.is_staff = True
                user.is_superuser = True
                user.save()
            return (user, None)
        raise exceptions.AuthenticationFailed('Пользователь не найден')
