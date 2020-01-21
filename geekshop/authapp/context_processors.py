from mainapp.common_context import common_context


def authapp_context(request):
    user = request.user
    context = common_context(user)
    return {'authapp_context': context}
