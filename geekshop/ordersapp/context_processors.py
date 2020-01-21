from mainapp.common_context import common_context


def ordersapp_context(request):
    user = request.user
    context = common_context(user)
    context['path_to_orders_inc'] = 'ordersapp/includes/'
    return {'ordersapp_context': context}
