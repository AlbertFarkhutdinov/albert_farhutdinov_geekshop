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
from django.db.models import Case, DecimalField, F, IntegerField, Q, When

from shop.orders_app.models import OrderItem

ACTION_1 = 1
ACTION_2 = 2
ACTION_EXPIRED = 3


class Command(BaseCommand):
    def handle(self, *args, **options):
        action_1__time_delta = timedelta(hours=12)
        action_2__time_delta = timedelta(days=1)
        action_1__discount = 0.3
        action_2__discount = 0.15
        action_expired__discount = 0.05
        action_1__condition = Q(
            order__updated__lte=F('order__created') + action_1__time_delta,
        )
        action_2__condition = (
            Q(order__updated__gt=F('order__created') + action_1__time_delta)
            & Q(order__updated__lte=F('order__created') + action_2__time_delta)
        )
        action_expired__condition = Q(
            order__updated__gt=F('order__created') + action_2__time_delta,
        )
        action_1__order = When(action_1__condition, then=ACTION_1)
        action_2__order = When(action_2__condition, then=ACTION_2)
        action_expired__order = When(
            action_expired__condition,
            then=ACTION_EXPIRED,
        )
        action_1__price = When(
            action_1__condition,
            then=F('product__price') * F('quantity') * action_1__discount,
        )
        action_2__price = When(
            action_2__condition,
            then=F('product__price') * F('quantity') * -action_2__discount,
        )
        action_expired__price = When(
            action_expired__condition,
            then=(
                F('product__price')
                * F('quantity')
                * action_expired__discount
            ),
        )
        test_orders = OrderItem.objects.annotate(
            action_order=Case(
                action_1__order,
                action_2__order,
                action_expired__order,
                output_field=IntegerField(),
            ),
        ).annotate(
            total_price=Case(
                action_1__price,
                action_2__price,
                action_expired__price,
                output_field=DecimalField(),
            ),
        ).order_by('action_order', 'total_price').select_related()

        for order_item in test_orders:
            msg = ' | '.join(
                str(order_item.action_order),
                'Order #{0: 3.0f}'.format(order_item.pk),
                str(order_item.product.name),
                'Discount: {0: .2f} rub.'.format(
                    abs(order_item.total_price),
                ),
                str(order_item.order.updated - order_item.order.created),
            )
            print(msg)
