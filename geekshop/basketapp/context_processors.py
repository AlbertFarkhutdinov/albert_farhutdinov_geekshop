from mainapp.common_context import common_context


def basketapp_context(request):
    user = request.user
    context = common_context(user)
    context['path_to_basket_inc'] = 'basketapp/includes/'
    return {'basketapp_context': context}
