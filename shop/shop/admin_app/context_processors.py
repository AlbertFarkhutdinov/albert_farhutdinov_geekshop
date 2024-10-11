from shop.main_app.common_context import common_context


def admin_app_context(request):
    user = request.user
    context = common_context(user)
    return {'admin_app_context': context}
