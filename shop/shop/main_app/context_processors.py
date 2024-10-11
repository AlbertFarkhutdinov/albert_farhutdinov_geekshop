from shop.main_app.common_context import common_context


def main_app_context(request):
    user = request.user
    context = common_context(user)
    context['path_to_main_img'] = 'main_app/img/'
    context['path_to_main_inc'] = 'main_app/includes/'
    return {'main_app_context': context}
