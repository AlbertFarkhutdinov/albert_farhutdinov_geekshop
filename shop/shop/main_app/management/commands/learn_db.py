# from django.core.management.base import BaseCommand
# from shop.main_app.models import Product
# from django.db import connection
# from django.db.models import Q
# from shop.admin_app.views import db_profile_by_type
#
#
# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         test_products = Product.objects.filter(
#             Q(category__name='office') |
#             Q(category__name='modern')
#         )
#         # print(len(test_products))
#         print(test_products)
#         db_profile_by_type('learn db', '', connection.queries)

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import models

from shop.orders_app.models import OrderItem

ACTION1 = 1
ACTION2 = 2
ACTION_EXPIRED = 3

ORDER_CREATED = 'order__created'


class Command(BaseCommand):
    def handle(self, *args, **options):
        action1_time_delta = timedelta(hours=12)
        action2_time_delta = timedelta(days=1)
        action1_discount = 0.3
        action2_discount = 0.15
        action_expired_discount = 0.05
        action1_condition = models.Q(
            order__updated__lte=models.F(ORDER_CREATED) + action1_time_delta,
        )
        gt = models.Q(
            order__updated__gt=models.F(ORDER_CREATED) + action1_time_delta,
        )
        lte = models.Q(
            order__updated__lte=models.F(ORDER_CREATED) + action2_time_delta,
        )
        action2_condition = gt & lte
        action_expired_condition = models.Q(
            order__updated__gt=models.F(ORDER_CREATED) + action2_time_delta,
        )
        action1_order = models.When(action1_condition, then=ACTION1)
        action2_order = models.When(action2_condition, then=ACTION2)
        action_expired_order = models.When(
            action_expired_condition,
            then=ACTION_EXPIRED,
        )
        product_cost = models.F('product__price') * models.F('quantity')
        action1_price = models.When(
            action1_condition,
            then=product_cost * action1_discount,
        )
        action2_price = models.When(
            action2_condition,
            then=product_cost * -action2_discount,
        )
        action_expired_price = models.When(
            action_expired_condition,
            then=product_cost * action_expired_discount,
        )
        action_order = models.Case(
            action1_order,
            action2_order,
            action_expired_order,
            output_field=models.IntegerField(),
        )
        total_price = models.Case(
            action1_price,
            action2_price,
            action_expired_price,
            output_field=models.DecimalField(),
        )
        test_orders = OrderItem.objects.annotate(
            action_order=action_order,
        ).annotate(
            total_price=total_price,
        ).order_by('action_order', 'total_price').select_related()

        for order_item in test_orders:
            msg = ' | '.join(
                str(order_item.action_order),
                'Order #{0: 3.0f}'.format(order_item.pk),
                str(order_item.product.name),
                'Discount: {0: .2f}USD'.format(
                    abs(order_item.total_price),
                ),
                str(order_item.order.updated - order_item.order.created),
            )
            print(msg)
