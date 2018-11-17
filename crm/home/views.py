from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def index(request):
    context = {}
    return render(request, 'index.html', context)


def sales_index(request):
    context = {}
    return render(request, 'index.html', context)


def customer_list(request):
    context = {}
    return render(request, 'sales/customers.html', context)
