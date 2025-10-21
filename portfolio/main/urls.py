from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"), # Going to nothing = home page.
    path("home/", views.home, name="home"), # Standard home url. 
    path("contact/", views.contact, name="contact"),
    path("project/<int:id>/", views.project, name="project"), # after project, you go to a specific variable (given to each project)
]