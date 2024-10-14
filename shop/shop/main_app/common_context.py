# from django.conf.global_settings import MEDIA_URL

path_to_common_img = 'img/'
path_to_common_inc = 'common_includes/'
path_to_media = '/media/'
main_menu = [
    {
        'href': 'main_urls:featured',
        'name': 'HOME',
    },
    {
        'href': 'products_urls:hot',
        'name': 'PRODUCTS',
    },
    {
        'href': 'history_url',
        'name': 'HISTORY',
    },
    {
        'href': 'showroom_url',
        'name': 'SHOWROOM',
    },
    {
        'href': 'contacts_url',
        'name': 'CONTACTS',
    },
]

info_menu = [
    {
        'href': '#',
        'name': 'Sales terms',
    },
    {
        'href': '#',
        'name': 'Customer care',
    },
    {
        'href': '#',
        'name': 'Delivery',
    },
    {
        'href': '#',
        'name': 'Architect accounts',
    },
    {
        'href': '#',
        'name': 'Careers',
    },
    {
        'href': '#',
        'name': 'Exchanges & returns',
    },
]

contact_information = {
    'phone': '1900 - 1234 -5678',
    'email': 'info@interior.com',
    'address': '12 W 1st St, 90001 Los Angeles, California',
}

socials = [
    {
        'href': 'https://www.facebook.com/',
        'image_source': path_to_common_img + 'facebook.png',
        'name': 'facebook',
    },
    {
        'href': 'https://twitter.com/',
        'image_source': path_to_common_img + 'twitter.png',
        'name': 'twitter',
    },
    {
        'href': 'https://plus.google.com/',
        'image_source': path_to_common_img + 'google_plus.png',
        'name': 'google_plus',
    },
    {
        'href': 'https://www.pinterest.com/',
        'image_source': path_to_common_img + 'pinterest.png',
        'name': 'pinterest',
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
