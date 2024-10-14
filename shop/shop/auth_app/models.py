from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now


class ShopUser(AbstractUser):
    class Meta:
        verbose_name = 'Shop user'
        verbose_name_plural = 'Shop users'

    avatar = models.ImageField(
        upload_to='users_avatars',
        blank=True,
    )
    age = models.PositiveIntegerField(
        verbose_name='Age',
        default=18,
    )
    activation_key = models.CharField(
        max_length=128,
        blank=True,
    )
    activation_key_expires = models.DateTimeField(
        default=(now() + timedelta(hours=48)),
    )

    def __str__(self):
        return self.username

    def is_activation_key_expired(self):
        return now() > self.activation_key_expires


class ShopUserProfile(models.Model):
    objects = models.Manager()
    male = 'M'
    female = 'F'

    gender_choices = (
        (male, 'M'),
        (female, 'F'),
    )
    user = models.OneToOneField(
        ShopUser,
        unique=True,
        null=False,
        db_index=True,
        on_delete=models.CASCADE,
    )
    tag_line = models.CharField(
        verbose_name='Tags',
        max_length=128,
        blank=True,
    )
    about_me = models.TextField(
        verbose_name='About Me',
        max_length=512,
        blank=True,
    )
    gender = models.CharField(
        verbose_name='Gender',
        max_length=1,
        choices=gender_choices,
        blank=True,
    )
    vk_page = models.CharField(
        verbose_name='VK account',
        max_length=128,
        blank=True,
    )
    country = models.CharField(
        verbose_name='Country',
        max_length=128,
        blank=True,
    )
    city = models.CharField(
        verbose_name='City',
        max_length=128,
        blank=True,
    )

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, *args, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, *args, **kwargs):
        instance.shopuserprofile.save()
