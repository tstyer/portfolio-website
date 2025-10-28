from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import Project, Tag, Comment
from .forms import CommentForm

# Create your views here.

def home(request):
    projects = Project.objects.all()  # Gives access to all projects on the home page.
    tags = Tag.objects.all()
    # Rendering just means to show on the screen.
    return render(request, "home.html", {"projects": projects, "tags": tags})

def contact(request):
    return render(request, "contact.html")

def project(request, id):
    # Look for the pk we specified, within the project model.
    project_obj = get_object_or_404(Project, pk=id)

    # ADDED: list comments and show empty form
    comments = project_obj.comments.select_related("user").all()
    form = CommentForm()

    return render(
        request,
        "project.html",
        {
            "project": project_obj,
            "comments": comments,
            "form": form,  # used for the "create comment" form
        },
    )

# Below is the ability to add comments to satisfy CRUD.

@login_required
@require_POST
def comment_create(request, id):
    """
    Create a new comment on a project.
    """
    project_obj = get_object_or_404(Project, pk=id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.project = project_obj
        comment.user = request.user
        comment.save()
        messages.success(request, "Comment posted.")
    else:
        messages.error(request, "Please fix the errors and try again.")
    # Go back to the project page
    return redirect(reverse("project", kwargs={"id": project_obj.pk}))

@login_required
def comment_update(request, id, comment_id):
    """
    Update an existing comment (only by its owner).
    """
    project_obj = get_object_or_404(Project, pk=id)
    comment = get_object_or_404(Comment, pk=comment_id, project=project_obj, user=request.user)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated.")
        else:
            messages.error(request, "Please fix the errors and try again.")

    return redirect(reverse("project", kwargs={"id": project_obj.pk}))

@login_required
@require_POST
def comment_delete(request, id, comment_id):
    """
    Delete a comment (only by its owner).
    """
    project_obj = get_object_or_404(Project, pk=id)
    comment = get_object_or_404(Comment, pk=comment_id, project=project_obj, user=request.user)

    comment.delete()
    messages.success(request, "Comment deleted.")

    return redirect(reverse("project", kwargs={"id": project_obj.pk}))

# Self-learn note:
#  Views are functions called when wanting to display a page.
#  You need to import models to do so.
