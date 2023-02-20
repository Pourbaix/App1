from functools import wraps 
from django.shortcuts import redirect
from django.http import Http404

def trainer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if isTrainer(request.user):
            return view_func(request, *args, **kwargs)
        else:
            raise Http404
    return wrapper


def isTrainer(user):
    # Returns true if the user is part of the 'Trainers' group => Check permissions

    return "Trainers" in user.groups.values_list('name', flat = True)
