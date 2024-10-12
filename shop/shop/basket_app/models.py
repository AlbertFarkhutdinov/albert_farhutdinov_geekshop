from django.db import models
from django.conf import settings
from shop.main_app.models import Product


class BasketQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.product.quantity += obj.quantity
            obj.product.save()
        super(BasketQuerySet, self).delete(*args, **kwargs)


class BasketSlot(models.Model):
    objects = BasketQuerySet.as_manager()

    class Meta:
        verbose_name = 'Basket Slot'
        verbose_name_plural = 'Basket slots'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Quantity', default=1)
    created = models.DateTimeField(verbose_name='Creating Time', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Update Time', auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.product.name}'

    @property
    def cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_items(user):
        return BasketSlot.objects.filter(user=user).select_related().order_by('product__category')

    @staticmethod
    def get_item(pk):
        return BasketSlot.objects.filter(pk=pk).select_related().first()

    # def delete(self):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super(self.__class__, self).delete()
    #
    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
    #     else:
    #         self.product.quantity -= self.quantity
    #     self.product.save()
    #     super(self.__class__, self).save(*args, **kwargs)
