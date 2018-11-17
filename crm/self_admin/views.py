from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from self_admin import app_setup
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout

app_setup.self_admin_auth_discover()


from self_admin.sites import site
print(site.enabled_admins)


def acc_login(request):
    context = dict()
    if request.method == "GET":
        return render(request, 'self_admin/login.html', context)
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            print('yes', username, password)
            login(request, user)
            return redirect(request.GET.get('next', '/self_admin'))
        else:
            context['error_msg'] = 'Wrong Username or Password'

    return render(request, 'self_admin/login.html', context)


def acc_logout(request):
    logout(request)
    return redirect('/login/')


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


# def display_table_obj(request, app_name, table_name):
#     # model_module = importlib.import_module('{}.models'.format(app_name))
#     # model_obj = getattr(model_module, table_name)
#     context = dict()
#
#     context['admin_class'] = self_admin.enabled_admins[app_name][table_name]
#     return render(request, 'self_admin/table_obj.html', context)


def app_index(request):
    context = dict()
    enabled_admins = []
    context['site'] = site
    return render(request, 'self_admin/app_index.html', context)


def get_filter_result(request, query_sets):
    filter_conditions = dict()
    for key, val in request.GET.items():
        if val:
            filter_conditions[key] = val

    print(filter_conditions)
    return query_sets.filter(**filter_conditions), filter_conditions


@login_required
def table_obj_list(request, app_name, model_name):
    """取出指定model中的数据返回给前端"""
    admin_class = site.enabled_admins[app_name][model_name]
    query_sets = admin_class.model.objects.all()
    context = dict()

    query_sets, filter_conditions = get_filter_result(request, query_sets)
    admin_class.filter_conditions = filter_conditions

    context['query_sets'] = query_sets
    context['admin_class'] = admin_class
    return render(request, 'self_admin/table_obj_list.html', context)

