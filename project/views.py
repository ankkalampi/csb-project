from django.shortcuts import render



from django.http import HttpResponse
from django.template import Context, loader
from django.contrib.auth.forms import AuthenticationForm


def index(request):
    form = AuthenticationForm(request)
    return render(request, 'project/index.html', {'form': form})

