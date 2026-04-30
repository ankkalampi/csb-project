from django.shortcuts import render



from django.http import HttpResponse
from django.template import Context, loader
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


def index(request):
    form = AuthenticationForm(request)
    return render(request, 'project/index.html', {'form': form})

@login_required
def user_view(request):
    return render(request, 'project/user.html', {'user': request.user})