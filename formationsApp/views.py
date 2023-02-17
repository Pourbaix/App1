from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Formations, Session


def create(request, **kwargs):
    # Renders the html form to create or update a formation 

    if(not request.user.is_authenticated):
        return HttpResponse("Please authentificate to access the site !!")
    if(isTrainer(request.user)):
        if(kwargs):
            id_formation = kwargs["id_formation"]
            f = get_object_or_404(Formations, pk=id_formation)
            return render(request, 'formationsApp/create.html', {"formation": f })
        else:
            return render(request, 'formationsApp/create.html', {})
    else: 
        return HttpResponse("You need to be a trainer to add formations!")

def addForm(request, **kwargs):
    # Adds or updates a formation

    if(not request.user.is_authenticated):
        return HttpResponse("Please authentificate to access the site !!")
    if(isTrainer(request.user)):
        if(kwargs):
            id_formation = kwargs["id_formation"]
            title = request.POST["title"]
            description = request.POST["description"]
            trainer = request.user.username 

            f = Formations.objects.get(pk=id_formation)
            f.title = title
            f.description = description
            f.save()
        else:
            title = request.POST["title"]
            description = request.POST["description"]
            trainer = request.user 

            f = Formations.objects.create(trainer=trainer, title=title, description=description)
            f.save()
        return HttpResponseRedirect(reverse('formationsApp:list'))
    else: 
        return HttpResponse("You need to be a trainer to add formations!")
        

def list(request):
    # Lists all the existing formations

    if(not request.user.is_authenticated):
        return HttpResponse("Please authentificate to access the site !!")
    formations_list =  Formations.objects.all()
    return render(request, 'formationsApp/list.html', {"formations_list": formations_list, "isTrainer": isTrainer(request.user)})            
        

def details(request, id_formation):
    # Renders the details page for a specific formation 

    if(not request.user.is_authenticated):
        return HttpResponse("Please authentificate to access the site !!")
    formation = Formations.objects.get(pk=id_formation)
    return render(request, 'formationsApp/details.html', {"formation": formation, "isTrainer": isTrainer(request.user), "user": request.user})

def delete(request, id_formation):
    # Deletes a specific formation
    
    if(not request.user.is_authenticated):
        return HttpResponse("Please authentificate to access the site !!")
    if isTrainer(request.user):
        Formations.objects.filter(pk=id_formation).delete()
        return HttpResponseRedirect(reverse('formationsApp:list'))
    else:
        return HttpResponse("You need to be a trainer to remove formations!")

def createSession(request, id_formation):
    # Renders the form to create a session for a specific formation 

    if(not request.user.is_authenticated):
        return HttpResponse("Please authentificate to access the site !!")
    if isTrainer(request.user):
        return render(request, 'formationsApp/session.html', {"id_formation": id_formation})
    else:
        return HttpResponse("You need to be a trainer to remove formations!")


def addSession(request, id_formation):
    # Creates a session for a specific formation 

    if(not request.user.is_authenticated):
        return HttpResponse("Please authentificate to access the site !!")
    if isTrainer(request.user):
        f =  get_object_or_404(Formations, pk=id_formation)
        f.session_set.create(event_date=request.POST["dateTime"], max_student_nbr=request.POST["studentNbr"], place=request.POST["place"])
        f.save()
        return HttpResponseRedirect(reverse("formationsApp:details", args=[f.id]))
    else:
        return HttpResponse("You need to be a trainer to add sessions!")

def deleteSession(request, id_session):
    # Deletes a specific session

    if(not request.user.is_authenticated):
        return HttpResponse("Please authentificate to access the site !!")
    if isTrainer(request.user):
        formation = Session.objects.get(pk=id_session).formation
        s = get_object_or_404(Session, pk=id_session)
        s.delete()
        return render(request, 'formationsApp/details.html', {"formation": formation, "isTrainer": isTrainer(request.user)})
    else:
        return HttpResponse("You need to be a trainer to add sessions!")


def followSession(request, id_session):
    # Allows a student to follow a specific session  

    if(not request.user.is_authenticated):
        return HttpResponse("Please authentificate to access the site !!")
    s = Session.objects.get(pk=id_session)
    u = request.user
    u.session_set.add(s)
    u.save()
    formation = Session.objects.get(pk=id_session).formation
    return render(request, 'formationsApp/details.html', {"formation": formation, "isTrainer": isTrainer(request.user), "user": request.user})

def sessionDetails(request, id_session):
    # Gives details about the session for the trainers 

    if(not request.user.is_authenticated):
        return HttpResponse("Please authentificate to access the site !!")
    if isTrainer(request.user):
        session = Session.objects.get(pk=id_session)
        return render(request, 'formationsApp/sessionDetails.html', {"session": session})
    else:
        return HttpResponse("You need to be a trainer to view session details!")


def removeFromSession(request, id_session):
    if(not request.user.is_authenticated):
        return HttpResponse("Please authentificate to access the site !!")
    s = Session.objects.get(pk=id_session)
    u = request.user
    u.session_set.remove(s)
    u.save()
    formation = Session.objects.get(pk=id_session).formation
    return render(request, 'formationsApp/details.html', {"formation": formation, "isTrainer": isTrainer(request.user), "user": request.user})

def loginPage(request):
    # Renders the login page 

    return render(request, 'formationsApp/login.html')

def doLogin(request):
    # Executes the login procedure 

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("formationsApp:list"))
    else: 
        print(user)
        return render(request, 'formationsApp/login.html', {"error": True})

def doLogout(request):
    # Logs the user out of the site 

    logout(request)
    return render(request, 'formationsApp/login.html')

def isTrainer(user):
    # Returns true if the user is part of the 'Trainers' group => Check permissions

    return "Trainers" in user.groups.values_list('name', flat = True)