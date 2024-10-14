from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from shop.auth_app.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':
        api_url_1 = urlunparse(
            (
                'https',
                'api.vk.com',
                '/method/users.get',
                None,
                urlencode(
                    OrderedDict(
                        fields=','.join(
                            (
                                'domain',
                                'about',
                                'bdate',
                                'sex',
                                'city',
                                'country',
                            ),
                        ),
                        access_token=response['access_token'],
                        v='5.92'),
                ),
                None,
            ),
        )
        resp_1 = requests.get(api_url_1)
        if resp_1.status_code != 200:
            print('Error from VK API', resp_1, sep='\n')
            return

        data_1 = resp_1.json()['response'][0]
        print('Answer from VK API: ', data_1, sep='\n')
        if data_1['about'] and not user.shopuserprofile.about_me:
            user.shopuserprofile.about_me = data_1['about']
        if data_1['sex']:
            if data_1['sex'] == 2:
                user.shopuserprofile.gender = ShopUserProfile.MALE
            else:
                user.shopuserprofile.gender = ShopUserProfile.FEMALE
        if data_1['bdate']:
            b_date = datetime.strptime(data_1['bdate'], '%d.%m.%Y').date()
            age = timezone.now().date().year - b_date.year
            if age < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.vk.VKOAuth2')
            user.age = age
        if data_1['domain']:
            user.shopuserprofile.vk_page = 'https://vk.com/' + data_1['domain']
        if data_1['country']['title']:
            user.shopuserprofile.country = data_1['country']['title']
        if data_1['city']['title']:
            user.shopuserprofile.city = data_1['city']['title']

        user.save()
