from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Formations, Session


def create(request, **kwargs):
    # This view is used to 
    if(not request.user.is_authenticated):
        return HttpResponse("Authentificate to acces to the site !!")
    else:
        if(kwargs):
            id_formation = kwargs["id_formation"]
            f = get_object_or_404(Formations, pk=id_formation)
            return render(request, 'formationsApp/create.html', {"formation": f })
        else:
            return render(request, 'formationsApp/create.html', {})

def addForm(request, **kwargs):
    if(not request.user.is_authenticated):
        return HttpResponse("Authentificate to acces to the site !!")
    else:
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
    if(not request.user.is_authenticated):
        return HttpResponse("Authentificate to acces to the site !!")
    else:
        formations_list =  Formations.objects.all()
        return render(request, 'formationsApp/list.html', {"formations_list": formations_list})

def details(request, id_formation):
    if(not request.user.is_authenticated):
        return HttpResponse("Authentificate to acces to the site !!")
    else:
        formation = Formations.objects.get(pk=id_formation)
        return render(request, 'formationsApp/details.html', {"formation": formation})

def delete(request, id_formation):
    if(not request.user.is_authenticated):
        return HttpResponse("Authentificate to acces to the site !!")
    else:
        Formations.objects.filter(pk=id_formation).delete()
        return HttpResponseRedirect(reverse('formationsApp:list'))

def createSession(request, id_formation):
    if(not request.user.is_authenticated):
        return HttpResponse("Authentificate to acces to the site !!")
    else:
        return render(request, 'formationsApp/session.html', {"id_formation": id_formation})


def addSession(request, id_formation):
    f =  get_object_or_404(Formations, pk=id_formation)
    f.session_set.create(event_date=request.POST["dateTime"], max_student_nbr=request.POST["studentNbr"], place=request.POST["place"])
    f.save()
    return HttpResponseRedirect(reverse("formationsApp:details", args=[f.id]))

def deleteSession(request, id_session):
    s = get_object_or_404(Session, pk=id_session)
    s.delete()
    return HttpResponse("Session Deleted !")

def followSession(request, id_session):
    return HttpResponse("Followed this formation.")