from django import template

register = template.Library()


@register.filter
def basket_total_quantity(basket):
    return sum([basket_slot.quantity for basket_slot in basket])


@register.filter
def basket_total_cost(basket):
    return sum([basket_slot.cost for basket_slot in basket])
