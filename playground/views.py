from django.shortcuts import render

from store.models import Order


# Create your views here.


def home(request):
    # ordered_products = OrderItem.objects.values('product_id').distinct()
    queryset = (
        Order.objects.select_related("customer")
        .prefetch_related("orderitem_set__product")
        .all()
        .order_by("-placed_at")[:5]
    )
    context = {"orders": queryset}

    return render(request, "playground/index.html", context=context)
