from django.urls import path

from . import views

app_name='formationsApp'
urlpatterns = [
    path('createFormation/', views.create,  name="createFormation"), # Used to render HTML
    path('<int:id_formation>/updateFormation/', views.create,  name="updateFormation"), # Used to render HTML
    path('create/', views.addForm, name="create"), # Used to send the request 
    path('<int:id_formation>/update/', views.addForm, name="update"), # Used to send the request 
    path('list/', views.list, name="list"), # Used to render HTML
    path('<int:id_formation>/details/', views.details, name="details")
]