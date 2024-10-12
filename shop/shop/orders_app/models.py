from django.db import models
from django.conf import settings
from shop.main_app.models import Product


class OrderItemQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.product.quantity += obj.quantity
            obj.product.save()
        super(OrderItemQuerySet, self).delete(*args, **kwargs)


class Order(models.Model):
    objects = models.Manager()
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'forming'),
        (SENT_TO_PROCEED, 'sent to proceed'),
        (PAID, 'paid'),
        (PROCEEDED, 'proceeded'),
        (READY, 'ready'),
        (CANCEL, 'cancel'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Creating Time', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Update Time', auto_now=True)
    status = models.CharField(verbose_name='Status', max_length=3, choices=ORDER_STATUS_CHOICES, default=FORMING)
    is_active = models.BooleanField(verbose_name='Is active?', default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'Current order: {self.pk}'

    def get_summary(self):
        items = self.order_items.select_related()
        return {
            'total_cost': sum(list(map(lambda x: x.quantity * x.product.price, items))),
            'total_quantity': sum(list(map(lambda x: x.quantity, items)))
        }

    def get_items(self):
        return self.order_items.select_related()

    def get_product_type_quantity(self):
        return len(self.get_items())

    # def get_total_quantity(self):
    #     return sum(list(map(lambda x: x.quantity, self.get_items())))

    # def get_total_cost(self):
    #     return sum(list(map(lambda x: x.quantity * x.product.price, self.get_items())))

    def delete(self):
        items = self.get_items()
        for item in items:
            item.product.quantity += item.quantity
            item.product.save()
        self.is_active = False
        self.save()

    def __str__(self):
        return f'Order #{self.pk}; {self.created}'


class OrderItem(models.Model):
    objects = OrderItemQuerySet.as_manager()

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Quantity', default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity

    def __str__(self):
        order = self.order
        return f'{self.product.name} (Order #{order.pk}; {order.created})'

    @staticmethod
    def get_items(user):
        return OrderItem.objects.filter(user=user).select_related().order_by('product__category')

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.filter(pk=pk).select_related().first()

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
