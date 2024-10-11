from shop.main_app.common_context import common_context


def basket_app_context(request):
    user = request.user
    context = common_context(user)
    context['path_to_basket_inc'] = 'basket_app/includes/'
    return {'basket_app_context': context}
