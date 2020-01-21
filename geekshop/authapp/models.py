from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver


class ShopUser(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='Возраст', default=18)
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=48)))

    def __str__(self):
        return self.username

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True


class ShopUserProfile(models.Model):
    objects = models.Manager()
    MALE = 'M'
    FEMALE = 'W'

    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )
    user = models.OneToOneField(ShopUser, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    tag_line = models.CharField(verbose_name='Теги', max_length=128, blank=True)
    about_me = models.TextField(verbose_name='О себе', max_length=512, blank=True)
    gender = models.CharField(verbose_name='Пол', max_length=1, choices=GENDER_CHOICES, blank=True)
    vk_page = models.CharField(verbose_name='URL-адрес аккаунта ВК', max_length=128, blank=True)
    country = models.CharField(verbose_name='Страна', max_length=128, blank=True)
    city = models.CharField(verbose_name='Город', max_length=128, blank=True)

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, *args, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, *args, **kwargs):
        instance.shopuserprofile.save()
