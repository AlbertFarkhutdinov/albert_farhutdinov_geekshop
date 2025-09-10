from django.core.management.base import BaseCommand

from shop.auth_app.models import ShopUser, ShopUserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = ShopUser.objects.all()
        for user in users:
            users_profile = ShopUserProfile.profiles.create(user=user)
            users_profile.save()
