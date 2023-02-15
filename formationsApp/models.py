from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class User(models.Model):
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    role = "formateur"

class Formations(models.Model):
    # trainer = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

class Session(models.Model):
    formation = models.ForeignKey(Formations, on_delete=models.CASCADE)
    students = models.ManyToManyField(User)
    event_date = models.DateTimeField('date of the session')
    max_student_nbr = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10000)])
    place = models.CharField(max_length=50)