from django.shortcuts import render, redirect, get_object_or_404



from django.http import HttpResponse
from django.template import Context, loader
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views


def index(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)

            if user.check_password(password):
                return redirect(f'/{user.username}')
            else:
                return render(request, "project/index.html")

        except User.DoesNotExist:
            return redirect('/')
        
    return render(request, "project/index.html")

def logout_view(request):
    request.session.flush()
    return redirect('/')

def user_view(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'project/user.html', {'user': user})