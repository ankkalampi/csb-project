from django.shortcuts import render, redirect, get_object_or_404



from django.http import HttpResponse
from django.template import Context, loader
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt

# FIXES CSRF VULNERABILITY
# @csrf_exempt
def index(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)

            # FIXES AUTHENTICATION FAILURE
            """
            if not user.check_password(password):
                
                return render(request, "project/index.html")
            """

            request.session['username'] = user.username
            return redirect(f'/{user.username}')
                

        except User.DoesNotExist:
            return redirect('/')
        
    return render(request, "project/index.html")

def logout_view(request):
    request.session.flush()
    return redirect('/')

def busted_view(request):

    # FIXES LOGGING AND MONITORING FAILURES
    """
    return render(request, 'project/not_permitted.html')
    """

    return HttpResponse(f"""
                        ACCESS BLOCKED
                        
                        Session meta: {dict(request.META)}
                        """)

def user_view(request, username):

    # FIXES BROKEN ACCESS CONTROL
    """
    if request.session.get('username') != username:
        return redirect('/busted/')
    """

    user = get_object_or_404(User, username=username)
    return render(request, 'project/user.html', {'user': user})