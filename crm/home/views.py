from django.shortcuts import render

# Create your views here.


def index(request):
    context = {}
    return render(request, 'index.html', context)


def sales_index(request):
    context = {}
    return render(request, 'index.html', context)


def customer_list(request):
    context = {}
    return render(request, 'sales/customers.html', context)
