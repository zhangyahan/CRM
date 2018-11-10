from django.shortcuts import render
from self_admin import self_admin
import importlib


def index(request):
    context = dict()

    context['table_list'] = self_admin.enabled_admins
    return render(request, 'self_admin/table_index.html', context)


def display_table_obj(request, app_name, table_name):
    print(app_name, table_name)
    model_module = importlib.import_module('{}.models'.format(app_name))
    model_obj = getattr(model_module, table_name)
    context = dict()

    context['model_obj'] = model_obj
    return render(request, 'self_admin/table_obj.html', context)
