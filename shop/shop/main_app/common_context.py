# from django.conf.global_settings import MEDIA_URL


IMAGE_SOURCE = 'image_source'
HREF = 'href'
NAME = 'name'
STUB = '#'


path_to_common_img = 'img/'
path_to_common_inc = 'common_includes/'
path_to_media = '/media/'
main_menu = [
    {
        HREF: 'main_urls:featured',
        NAME: 'HOME',
    },
    {
        HREF: 'products_urls:hot',
        NAME: 'PRODUCTS',
    },
    {
        HREF: 'history_url',
        NAME: 'HISTORY',
    },
    {
        HREF: 'showroom_url',
        NAME: 'SHOWROOM',
    },
    {
        HREF: 'contacts_url',
        NAME: 'CONTACTS',
    },
]

info_menu = [
    {
        HREF: STUB,
        NAME: 'Sales terms',
    },
    {
        HREF: STUB,
        NAME: 'Customer care',
    },
    {
        HREF: STUB,
        NAME: 'Delivery',
    },
    {
        HREF: STUB,
        NAME: 'Architect accounts',
    },
    {
        HREF: STUB,
        NAME: 'Careers',
    },
    {
        HREF: STUB,
        NAME: 'Exchanges & returns',
    },
]

contact_information = {
    'phone': '1900 - 1234 -5678',
    'email': 'info@interior.com',
    'address': '12 W 1st St, 90001 Los Angeles, California',
}

socials = [
    {
        HREF: 'https://www.facebook.com/',
        IMAGE_SOURCE: '{0}facebook.png'.format(path_to_common_img),
        NAME: 'facebook',
    },
    {
        HREF: 'https://twitter.com/',
        IMAGE_SOURCE: '{0}twitter.png'.format(path_to_common_img),
        NAME: 'twitter',
    },
    {
        HREF: 'https://plus.google.com/',
        IMAGE_SOURCE: '{0}google_plus.png'.format(path_to_common_img),
        NAME: 'google_plus',
    },
    {
        HREF: 'https://www.pinterest.com/',
        IMAGE_SOURCE: '{0}pinterest.png'.format(path_to_common_img),
        NAME: 'pinterest',
    },
]


def get_basket(user):
    if user.is_authenticated:
        return user.basket.select_related().all()
    return []


def get_username(user):
    if user.is_anonymous:
        return 'Anonymous'
    return user.first_name


def common_context(user):
    return {
        'path_to_common_img': path_to_common_img,
        'path_to_common_inc': path_to_common_inc,
        'path_to_media': path_to_media,
        'main_menu': main_menu,
        'info_menu': info_menu,
        'socials': socials,
        'contact_information': contact_information,
        'basket_items': get_basket(user),
        'username': get_username(user),
    }


def page_name(context, name):
    context['title'] = name
    context['header_name'] = name
