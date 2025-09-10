from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from shop.auth_app.models import ShopUserProfile

TITLE = 'title'


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'vk-oauth2':
        api_url1 = urlunparse(
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
                        v='5.92',
                    ),
                ),
                None,
            ),
        )
        resp1 = requests.get(api_url1)
        if resp1.status_code != 200:
            print('Error from VK API', resp1, sep='\n')
            return

        data1 = resp1.json()['response'][0]
        print('Answer from VK API: ', data1, sep='\n')
        if data1['about'] and not user.shopuserprofile.about_me:
            user.shopuserprofile.about_me = data1['about']
        if data1['sex']:
            if data1['sex'] == 2:
                user.shopuserprofile.gender = ShopUserProfile.male
            else:
                user.shopuserprofile.gender = ShopUserProfile.female
        if data1['bdate']:
            b_date = datetime.strptime(data1['bdate'], '%d.%m.%Y').date()
            age = timezone.now().date().year - b_date.year
            if age < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.vk.VKOAuth2')
            user.age = age
        if data1['domain']:
            user.shopuserprofile.vk_page = 'https://vk.com/{0}'.format(
                data1['domain'],
            )
        if data1['country'][TITLE]:
            user.shopuserprofile.country = data1['country'][TITLE]
        if data1['city'][TITLE]:
            user.shopuserprofile.city = data1['city'][TITLE]

        user.save()
