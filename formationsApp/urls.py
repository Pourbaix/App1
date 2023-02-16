from django.urls import path

from . import views

app_name='formationsApp'
urlpatterns = [
    path('createFormation/', views.create,  name="createFormation"), # Used to render HTML
    path('<int:id_formation>/updateFormation/', views.create,  name="updateFormation"), # Used to render HTML
    path('create/', views.addForm, name="create"), # Used to send a request 
    path('<int:id_formation>/update/', views.addForm, name="update"), # Used to send a request 
    path('list/', views.list, name="list"), # Used to render HTML
    path('<int:id_formation>/details/', views.details, name="details"), # Used to render HTML
    path('<int:id_formation>/delete/', views.delete, name="delete"), # Used to send a request 
    path('<int:id_formation>/createSession/', views.createSession, name="createSession"), # Used to render HTML
    path('<int:id_formation>/addSession/', views.addSession, name="addSession"), # Used to send a request 
    path('<int:id_session>/deleteSession/', views.deleteSession, name="deleteSession"), # Used to send a request 
    path('<int:id_session>/followSession/', views.followSession, name="followSession"), # Used to send a request
    path('<int:id_session>/removeFromSession/', views.removeFromSession, name="removeFromSession"), # Used to send a request
    path('login', views.loginPage, name="login"), # Used to login the site  
    path('doLogin', views.doLogin, name="doLogin"), # Used to login the site
    path('logout', views.doLogout, name="doLogout"), # Used to logout from the site   
]