from django.conf import settings
from django.db import models

from shop.main_app.models import Product


class BasketQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for basket_item in self:
            basket_item.product.quantity += basket_item.quantity
            basket_item.product.save()
        super().delete()


class BasketSlot(models.Model):
    objects = BasketQuerySet.as_manager()

    class Meta:
        verbose_name = 'Basket Slot'
        verbose_name_plural = 'Basket slots'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='basket',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Quantity',
        default=1,
    )
    created = models.DateTimeField(
        verbose_name='Creating Time',
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        verbose_name='Update Time',
        auto_now=True,
    )

    def __str__(self):
        return '{0} - {1}'.format(self.user.username, self.product.name)

    @property
    def cost(self):
        return self.product.price * self.quantity

    @classmethod
    def get_items(cls, user):
        return BasketSlot.objects.filter(
            user=user,
        ).select_related().order_by('product__category')

    @classmethod
    def get_item(cls, pk):
        return BasketSlot.objects.filter(pk=pk).select_related().first()

    # def delete(self):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super(self.__class__, self).delete()
    #
    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         self.product.quantity -= (
    #             self.quantity - self.__class__.get_item(self.pk).quantity
    #         )
    #     else:
    #         self.product.quantity -= self.quantity
    #     self.product.save()
    #     super(self.__class__, self).save(*args, **kwargs)
