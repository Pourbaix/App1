from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView, RedirectView, View
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .decorators import trainer_required

from .models import Formations, Session

class LoginView(TemplateView):
    template_name = 'formationsApp/login.html'

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("formationsApp:list"))
        else: 
            print(user)
            return render(request, 'formationsApp/login.html', {"error": True})

class LogoutView(RedirectView):
    pattern_name = "formationsApp:login"

    def setup(self, request, *args, **kwargs):
        logout(request)
        super().setup(request, *args, **kwargs)

@method_decorator(login_required, name="dispatch")
class FormationListView(ListView):
    template_name = "formationsApp/list.html"
    model = Formations
    context_object_name = "formations_list"
    user = None

    def setup(self, request, *args, **kwargs):
        self.user = request.user
        super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["isTrainer"] = isTrainer(self.user)
        return context
    
@method_decorator(login_required, name="dispatch")
@method_decorator(trainer_required, name="dispatch")
class CreateFormationView(TemplateView):
    template_name = "formationsApp/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if kwargs:
            f = get_object_or_404(Formations, pk=kwargs["id_formation"])
            context["formation"] = f
        return context

@method_decorator(login_required, name="dispatch")
@method_decorator(trainer_required, name="dispatch")
class AddFormationView(RedirectView):
    url = "/formations/list"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        if kwargs:
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
            trainer = request.user 

            f = Formations.objects.create(trainer=trainer, title=title, description=description)
            f.save()

@method_decorator(login_required, name="dispatch")
@method_decorator(trainer_required, name="dispatch")
class DeleteFormView(RedirectView):
    url = "/formations/list"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        Formations.objects.filter(pk=kwargs["id_formation"]).delete()

@method_decorator(login_required, name="dispatch")
class FormationDetails(TemplateView):
    template_name = "formationsApp/details.html"
    user = None

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if kwargs:
            f = get_object_or_404(Formations, pk=kwargs["id_formation"])
            context["formation"] = f
            context["isTrainer"] = isTrainer(self.user)
            context["user"] = self.user
        return context

@method_decorator(login_required, name="dispatch")
@method_decorator(trainer_required, name="dispatch")
class createSessionFormView(TemplateView):
    template_name = "formationsApp/session.html"

    def post(self, request, **kwargs):
        f =  get_object_or_404(Formations, pk=kwargs["id_formation"])
        f.session_set.create(event_date=request.POST["dateTime"], max_student_nbr=request.POST["studentNbr"], place=request.POST["place"])
        f.save()
        return HttpResponseRedirect(reverse("formationsApp:details", args=[f.id]))

@method_decorator(login_required, name="dispatch")
@method_decorator(trainer_required, name="dispatch")
class deleteSessionView(TemplateView):
    template_name = "formationsApp/details.html"
    user = None 

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user

    def get_context_data(self, **kwargs):
        formation = Session.objects.get(pk=kwargs["id_session"]).formation
        s = get_object_or_404(Session, pk=kwargs["id_session"])
        s.delete()
        context = super().get_context_data(**kwargs)
        context["formation"] = formation
        context["isTrainer"] = isTrainer(self.user)
        return context

@method_decorator(login_required, name="dispatch")
@method_decorator(trainer_required, name="dispatch")
class SessionDetailView(TemplateView):
    template_name = 'formationsApp/sessionDetails.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session = Session.objects.get(pk=kwargs["id_session"])
        context["session"] = session
        return context

@method_decorator(login_required, name="dispatch")
class FollowSessionView(TemplateView):
    user = None
    template_name = "formationsApp/details.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        s = Session.objects.get(pk=kwargs["id_session"])
        u = self.user
        u.session_set.add(s)
        u.save()
        formation = Session.objects.get(pk=kwargs["id_session"]).formation
        context["formation"] = formation
        context["isTrainer"] = isTrainer(self.user)
        context["user"] = self.user
        return context
    
@method_decorator(login_required, name="dispatch")
class removeFromSessionView(TemplateView):
    user = None
    template_name = "formationsApp/details.html"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = request.user
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        s = Session.objects.get(pk=kwargs["id_session"])
        u = self.user
        u.session_set.remove(s)
        u.save()
        formation = Session.objects.get(pk=kwargs["id_session"]).formation
        context["formation"] = formation
        context["isTrainer"] = isTrainer(self.user)
        context["user"] = self.user
        return context

# def create(request, **kwargs):
#     # Renders the html form to create or update a formation 

#     if(not request.user.is_authenticated):
#         return HttpResponse("Please authentificate to access the site !!")
#     if(isTrainer(request.user)):
#         if(kwargs):
#             id_formation = kwargs["id_formation"]
#             f = get_object_or_404(Formations, pk=id_formation)
#             return render(request, 'formationsApp/create.html', {"formation": f })
#         else:
#             return render(request, 'formationsApp/create.html', {})
#     else: 
#         return HttpResponse("You need to be a trainer to add formations!")

# def addForm(request, **kwargs):
#     # Adds or updates a formation

#     if(not request.user.is_authenticated):
#         return HttpResponse("Please authentificate to access the site !!")
#     if(isTrainer(request.user)):
#         if(kwargs):
#             id_formation = kwargs["id_formation"]
#             title = request.POST["title"]
#             description = request.POST["description"]
#             trainer = request.user.username 

#             f = Formations.objects.get(pk=id_formation)
#             f.title = title
#             f.description = description
#             f.save()
#         else:
#             title = request.POST["title"]
#             description = request.POST["description"]
#             trainer = request.user 

#             f = Formations.objects.create(trainer=trainer, title=title, description=description)
#             f.save()
#         return HttpResponseRedirect(reverse('formationsApp:list'))
#     else: 
#         return HttpResponse("You need to be a trainer to add formations!")
        

# def list(request):
#     # Lists all the existing formations

#     if(not request.user.is_authenticated):
#         return HttpResponse("Please authentificate to access the site !!")
#     formations_list =  Formations.objects.all()
#     return render(request, 'formationsApp/list.html', {"formations_list": formations_list, "isTrainer": isTrainer(request.user)})            

# def details(request, id_formation):
#     # Renders the details page for a specific formation 

#     if(not request.user.is_authenticated):
#         return HttpResponse("Please authentificate to access the site !!")
#     formation = Formations.objects.get(pk=id_formation)
#     return render(request, 'formationsApp/details.html', {"formation": formation, "isTrainer": isTrainer(request.user), "user": request.user})

# def delete(request, id_formation):
#     # Deletes a specific formation
    
#     if(not request.user.is_authenticated):
#         return HttpResponse("Please authentificate to access the site !!")
#     if isTrainer(request.user):
#         Formations.objects.filter(pk=id_formation).delete()
#         return HttpResponseRedirect(reverse('formationsApp:list'))
#     else:
#         return HttpResponse("You need to be a trainer to remove formations!")

# def createSession(request, id_formation):
#     # Renders the form to create a session for a specific formation 

#     if(not request.user.is_authenticated):
#         return HttpResponse("Please authentificate to access the site !!")
#     if isTrainer(request.user):
#         return render(request, 'formationsApp/session.html', {"id_formation": id_formation})
#     else:
#         return HttpResponse("You need to be a trainer to remove formations!")


# def addSession(request, id_formation):
#     # Creates a session for a specific formation 

#     if(not request.user.is_authenticated):
#         return HttpResponse("Please authentificate to access the site !!")
#     if isTrainer(request.user):
#         f =  get_object_or_404(Formations, pk=id_formation)
#         f.session_set.create(event_date=request.POST["dateTime"], max_student_nbr=request.POST["studentNbr"], place=request.POST["place"])
#         f.save()
#         return HttpResponseRedirect(reverse("formationsApp:details", args=[f.id]))
#     else:
#         return HttpResponse("You need to be a trainer to add sessions!")

# def deleteSession(request, id_session):
#     # Deletes a specific session

#     if(not request.user.is_authenticated):
#         return HttpResponse("Please authentificate to access the site !!")
#     if isTrainer(request.user):
#         formation = Session.objects.get(pk=id_session).formation
#         s = get_object_or_404(Session, pk=id_session)
#         s.delete()
#         return render(request, 'formationsApp/details.html', {"formation": formation, "isTrainer": isTrainer(request.user)})
#     else:
#         return HttpResponse("You need to be a trainer to add sessions!")

# def followSession(request, id_session):
#     # Allows a student to follow a specific session  

#     if(not request.user.is_authenticated):
#         return HttpResponse("Please authentificate to access the site !!")
#     s = Session.objects.get(pk=id_session)
#     u = request.user
#     u.session_set.add(s)
#     u.save()
#     formation = Session.objects.get(pk=id_session).formation
#     return render(request, 'formationsApp/details.html', {"formation": formation, "isTrainer": isTrainer(request.user), "user": request.user})

# def sessionDetails(request, id_session):
#     # Gives details about the session for the trainers 

#     if(not request.user.is_authenticated):
#         return HttpResponse("Please authentificate to access the site !!")
#     if isTrainer(request.user):
#         session = Session.objects.get(pk=id_session)
#         return render(request, 'formationsApp/sessionDetails.html', {"session": session})
#     else:
#         return HttpResponse("You need to be a trainer to view session details!")

# def removeFromSession(request, id_session):
#     if(not request.user.is_authenticated):
#         return HttpResponse("Please authentificate to access the site !!")
#     s = Session.objects.get(pk=id_session)
#     u = request.user
#     u.session_set.remove(s)
#     u.save()
#     formation = Session.objects.get(pk=id_session).formation
#     return render(request, 'formationsApp/details.html', {"formation": formation, "isTrainer": isTrainer(request.user), "user": request.user})

# def loginPage(request):
#     # Renders the login page 

#     return render(request, 'formationsApp/login.html')

# def doLogin(request):
    # Executes the login procedure 
    

# def doLogout(request):
#     # Logs the user out of the site 

#     logout(request)
#     return render(request, 'formationsApp/login.html')

def isTrainer(user):
    # Returns true if the user is part of the 'Trainers' group => Check permissions

    return "Trainers" in user.groups.values_list('name', flat = True)