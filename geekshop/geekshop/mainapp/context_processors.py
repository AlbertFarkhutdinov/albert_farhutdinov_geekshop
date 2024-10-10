from mainapp.common_context import common_context


def mainapp_context(request):
    user = request.user
    context = common_context(user)
    context['path_to_main_img'] = 'mainapp/img/'
    context['path_to_main_inc'] = 'mainapp/includes/'
    return {'mainapp_context': context}
