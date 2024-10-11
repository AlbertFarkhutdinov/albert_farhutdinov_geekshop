from shop.main_app.common_context import common_context


def auth_app_context(request):
    user = request.user
    context = common_context(user)
    return {'auth_app_context': context}
