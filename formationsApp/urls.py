from django.urls import path

from . import views

app_name='formationsApp'
urlpatterns = [
    path('createFormation/', views.CreateFormationView.as_view(),  name="createFormation"), # Used to render HTML
    path('<int:id_formation>/updateFormation/', views.CreateFormationView.as_view(),  name="updateFormation"), # Used to render HTML
    path('create/', views.AddFormationView.as_view(), name="create"), # Used to send a request 
    path('<int:id_formation>/update/', views.AddFormationView.as_view(), name="update"), # Used to send a request 
    path('list/', views.FormationListView.as_view(), name="list"), # Used to render HTML
    path('<int:id_formation>/details/', views.FormationDetails.as_view(), name="details"), # Used to render HTML
    path('<int:id_formation>/delete/', views.DeleteFormView.as_view(), name="delete"), # Used to send a request 
    path('<int:id_formation>/createSession/', views.createSessionFormView.as_view(), name="createSession"), # Used to render HTML
    path('<int:id_formation>/addSession/', views.createSessionFormView.as_view(), name="addSession"), # Used to send a request 
    path('<int:id_session>/deleteSession/', views.deleteSessionView.as_view(), name="deleteSession"), # Used to send a request 
    path('<int:id_session>/followSession/', views.FollowSessionView.as_view(), name="followSession"), # Used to send a request
    path('<int:id_session>/removeFromSession/', views.removeFromSessionView.as_view(), name="removeFromSession"), # Used to send a request
    path('<int:id_session>/sessionDetails/', views.SessionDetailView.as_view(), name="sessionDetails"), # Used to render HTML
    path('login', views.LoginView.as_view(), name="login"), # Used to login the site  
    path('doLogin', views.LoginView.as_view(), name="doLogin"), # Used to login the site
    path('logout', views.LogoutView.as_view(), name="doLogout"), # Used to logout from the site   
]