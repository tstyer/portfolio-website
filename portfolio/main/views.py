from django.shortcuts import render
from .models import Project, Tag

# Create your views here.

def Home(request):
    return render(request, "home.html") # Rendering justr means to show on the screen.

def contact(request):
    return render(request, "contact.html")

def project(request, id):
    return render(request, "project.html")

# Self-learn note:
 # Views are functions called when wanting to display a page. 
 # You need to import models to do so. 


