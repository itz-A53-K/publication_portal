from django.shortcuts import render, redirect, get_object_or_404

from django.db.models import F
from faculty import models as f_model

# Create your views here.


def home(request):
    

    return render(request, 'user/index.html')

def searchResult(request):
    
    return render(request, 'user/searchResult.html')

def viewPublication(request, pubID = None):
    if pubID is None:
        return redirect('/')
    
    pub = get_object_or_404(f_model.Publication, id = pubID)

    f_model.Publication.objects.filter(id = pubID).update(
        view_count = F('views') + 1
    )


    context = {
        'publication': pub
    }
    
    return render(request, 'user/viewPublication.html', context)

def userProfile(request, id = None):
    if id is None:
        return redirect('/')
    
    user = get_object_or_404(f_model.Faculty, fid = id)
    context = {
        'user': user
    }

    return render(request, 'user/profile.html', context)