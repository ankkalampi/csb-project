from django.shortcuts import render, redirect, get_object_or_404

from django.db import connection

from django.http import HttpResponse
from django.template import Context, loader
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from project.models import Profile

import traceback
import sys
from django.conf import settings


def index(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)

            # FIXES AUTHENTICATION FAILURE (FLAW 1)
            """
            if not user.check_password(password):
                error = "wrong password"
                return render(request, "project/index.html" , {"error": error})
            """

            login(request, user)
            return redirect(f'/{user.username}')
                

        except User.DoesNotExist:
            return redirect('/')
        
    return render(request, "project/index.html")

def logout_view(request):
    request.session.flush()
    return redirect('/')

# FIXES CSRF VULNERABILITY (when commented out) (FLAW 2)
@csrf_exempt
def alter_secret(request):
    username = request.POST.get("username")
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)

    if request.method == "POST":
        new_secret = request.POST.get("secret")

        profile.secret = new_secret
        profile.save()

        return redirect(f"/{username}")

def busted_view(request):

    # FIXES SECURITY MISCONFIGURATION (FLAW 3)
    """
    return render(request, 'project/not_permitted.html')
    """

    try:
        raise Exception("Access denied")
    except Exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        stack_trace = traceback.format_exception(exc_type, exc_value, exc_traceback)

    formatted_stack_trace = "\n".join(stack_trace)

    modules = "\n".join(sys.modules.keys())

    settings_info = "\n".join([f"{k}: {getattr(settings, k)}" for k in dir(settings) if not k.startswith('_')])

    middleware = "\n".join(settings.MIDDLEWARE)

    return HttpResponse(f"""
                        ACCESS BLOCKED
                        </br>
                        If access should be granted, review debug information:</br>
                        ------------------------------------------------------</br>
                        Stack trace:</br>
                        <pre>{formatted_stack_trace}</pre></br>
                        ------------------------------------------------------</br>
                        Loaded modules:</br>
                        <pre>{modules}</pre></br>
                        ------------------------------------------------------</br>
                        Django settings:</br>
                        <pre>{settings_info}</pre></br>
                        ------------------------------------------------------</br>
                        Used middleware:</br>
                        <pre>{middleware}</pre></br>
                        """)

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        secret = request.POST.get("secret")

        if User.objects.filter(username=username).exists():
            return render(request, "project/register.html", {"error": "user exists"})
        
        user = User.objects.create_user(username=username, password=password)

        Profile.objects.create(user=user, username=username, secret=secret)

        return redirect("/")
    
    return render(request, "project/register.html")

def user_view(request, username):

    # FIXES BROKEN ACCESS CONTROL (FLAW 4)
    """
    if request.user.username != username:
        return redirect('/busted/')
    """

    

    user = get_object_or_404(User, username=username)

    # REMEBER TO REMOVE THIS AS WELL TO FIX FLAW 5
    # START REMOVING ->
    with connection.cursor() as cursor:
        cursor.execute(f"""
                       SELECT secret 
                       FROM project_profile 
                       WHERE username = '{username}'
""")
        row = cursor.fetchall()

    secret = row[0][0]
    # REMOVE UNTIL HERE <-


    # FIXES SQL INJECTION (FLAW 5)
    """
    profile = get_object_or_404(Profile, user=user)
    secret = profile.secret
    """


    


    return render(request, 'project/user.html', {'user': user, 'secret': secret})