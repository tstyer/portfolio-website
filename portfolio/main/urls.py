from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("contact/", views.contact, name="contact"),

    # Project detail (uses your existing view name 'project')
    path("project/<int:id>/", views.project, name="project"),

    # CRUD for comments
    path("project/<int:id>/comments/create/", views.comment_create, name="comment_create"),
    path("project/<int:id>/comments/<int:comment_id>/update/", views.comment_update, name="comment_update"),
    path("project/<int:id>/comments/<int:comment_id>/delete/", views.comment_delete, name="comment_delete"),
]
