from mainapp.common_context import common_context


def adminapp_context(request):
    user = request.user
    context = common_context(user)
    return {'adminapp_context': context}
