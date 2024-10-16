from django.conf import settings
from django.db import models

from shop.main_app.models import Product


class OrderItemQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for order_item in self:
            order_item.product.quantity += order_item.quantity
            order_item.product.save()
        super().delete(*args, **kwargs)


class Order(models.Model):
    orders = models.Manager()
    forming = 'FM'
    sent_to_proceed = 'STP'
    proceeded = 'PRD'
    paid = 'PD'
    ready = 'RDY'
    cancel = 'CNC'

    order_status_choices = (
        (forming, 'forming'),
        (sent_to_proceed, 'sent to proceed'),
        (paid, 'paid'),
        (proceeded, 'proceeded'),
        (ready, 'ready'),
        (cancel, 'cancel'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(
        verbose_name='Creating Time',
        auto_now_add=True,
    )
    updated = models.DateTimeField(verbose_name='Update Time', auto_now=True)
    status = models.CharField(
        verbose_name='Status',
        max_length=3,
        choices=order_status_choices,
        default=forming,
    )
    is_active = models.BooleanField(verbose_name='Is active?', default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return 'Order #{0}; {1}'.format(self.pk, self.created)

    def get_summary(self):
        order_items = self.order_items.select_related()
        summary = {'total_cost': 0, 'total_quantity': 0}
        for order_item in order_items:
            quantity = order_item.quantity
            summary['total_cost'] += quantity * order_item.product.price
            summary['total_quantity'] += quantity
        return summary

    def get_items(self):
        return self.order_items.select_related()

    def get_product_type_quantity(self):
        return len(self.get_items())

    # def get_total_quantity(self):
    #     return sum(list(map(lambda x: x.quantity, self.get_items())))

    # def get_total_cost(self):
    #     return sum(
    #         list(
    #             map(lambda x: x.quantity * x.product.price, self.get_items())
    #         )
    #     )

    def delete(self):
        order_items = self.get_items()
        for order_item in order_items:
            order_item.product.quantity += order_item.quantity
            order_item.product.save()
        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order_items = OrderItemQuerySet.as_manager()

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    order = models.ForeignKey(
        Order,
        related_name='order_items',
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Product',
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(verbose_name='Quantity', default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity

    def __str__(self):
        order = self.order
        return '{0} (Order #{1}; {2})'.format(
            self.product.name,
            order.pk,
            order.created,
        )

    @classmethod
    def get_items(cls, user):
        return OrderItem.order_items.filter(
            user=user,
        ).select_related().order_by('product__category')

    @classmethod
    def get_item(cls, pk):
        return OrderItem.order_items.filter(pk=pk).select_related().first()

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
