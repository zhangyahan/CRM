from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def acc_login(request):
    context = dict()
    if request.method == "GET":
        return render(request, 'login.html', context)
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            print('yes', username, password)
            login(request, user)
            return redirect(request.GET.get('next', '/crm'))
        else:
            context['error_msg'] = 'Wrong Username or Password'

    return render(request, 'login.html', context)


def acc_logout(request):
    logout(request)
    return redirect('/login/')

