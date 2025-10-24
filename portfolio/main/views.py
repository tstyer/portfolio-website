from django.shortcuts import render
from .models import Project, Tag

# Create your views here.

def home(request):
    projects = Project.objects.all() # Gives access to all projects on the home page. 
    tags = Tag.objects.all()
    return render(request, "home.html", {"projects": projects, "tags": tags}) # Rendering just means to show on the screen.

def contact(request):
    return render(request, "contact.html")

def project(request, id):
    project = get_object_or_404(project, pk=id) # Look for the pk we specified, within the project model. 
    return render(request, "project.html", {"project": project})

# Self-learn note:
 # Views are functions called when wanting to display a page. 
 # You need to import models to do so. 


