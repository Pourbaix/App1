from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Formations

# Create your views here.

def create(request, **kwargs):
    if(kwargs):
        id_formation = kwargs["id_formation"]
        f = get_object_or_404(Formations, pk=id_formation)
        return render(request, 'formationsApp/create.html', {"formation": f })
    else:
        return render(request, 'formationsApp/create.html', {})

def addForm(request, **kwargs):
    if(kwargs):
        id_formation = kwargs["id_formation"]
        title = request.POST["title"]
        description = request.POST["description"]

        f = Formations.objects.get(pk=id_formation)
        f.title = title
        f.description = description
        f.save()
    else:
        title = request.POST["title"]
        description = request.POST["description"]

        f = Formations.objects.create(title=title, description=description)
        f.save()
    return HttpResponseRedirect(reverse('formationsApp:list'))

def list(request):
    formations_list =  Formations.objects.all()
    return render(request, 'formationsApp/list.html', {"formations_list": formations_list})

def details(request, id_formation):
    formation = Formations.objects.get(pk=id_formation)
    return render(request, 'formationsApp/details.html', {"formation": formation})
