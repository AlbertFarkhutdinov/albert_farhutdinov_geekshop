from shop.main_app.common_context import common_context


def orders_app_context(request):
    user = request.user
    context = common_context(user)
    context['path_to_orders_inc'] = 'orders_app/includes/'
    return {'orders_app_context': context}
