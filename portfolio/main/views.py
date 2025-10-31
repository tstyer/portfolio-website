from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import Project, Tag, Comment
from .forms import CommentForm

import gspread 
from django.conf import settings
from datetime import datetime

import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST

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

# small partial view so the home page modal can load comments for a single project
def project_comments_partial(request, id):
    """
    Render just the comments + (optional) form for a specific project.
    Used by the home page popup.
    """
    project_obj = get_object_or_404(Project, pk=id)
    comments = project_obj.comments.select_related("user").order_by("-created_at")
    form = CommentForm() if request.user.is_authenticated else None
    return render(
        request,
        "partials/project_comments.html",
        {
            "project": project_obj,
            "comments": comments,
            "form": form,
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


def get_users_sheet():
    """
    Returns the Google Sheet worksheet that stores users.
    Assumes credentials already set up on settings side.
    """
    gc = gspread.service_account(filename=settings.GOOGLE_SERVICE_ACCOUNT_FILE)
    sh = gc.open_by_key(settings.GOOGLE_SHEET_ID)   # set this in settings
    ws = sh.worksheet("user")  # or whatever the tab is called
    return ws

@require_POST
def auth_register(request):
    """
    Registers a user in the Google Sheet.
    Expected fields: email, password, username
    """
    email = request.POST.get("email", "").strip().lower()
    password = request.POST.get("password", "").strip()
    username = request.POST.get("username", "").strip()

    if not email or not password or not username:
      return JsonResponse({"success": False, "error": "All fields required."}, status=400)

    try:
        ws = get_users_sheet()
    except Exception as e:
        return JsonResponse({"success": False, "error": f"Sheet error: {e}"}, status=500)

    # read all emails in sheet
    try:
        records = ws.get_all_records()
    except Exception as e:
        return JsonResponse({"success": False, "error": f"Read error: {e}"}, status=500)

    # check if email already exists
    for row in records:
        if row.get("Email", "").strip().lower() == email:
            return JsonResponse({"success": False, "error": "Email already registered."}, status=400)

    # write new row
    now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    try:
        ws.append_row([username, email, now_str, "", "", password])  # matches columns in screenshot
    except Exception as e:
        return JsonResponse({"success": False, "error": f"Write error: {e}"}, status=500)

    # need to hash password, or do something else? research. 
    # if the sheet has a Password column, do this instead:

    # mark session-like value in Django
    request.session["user_email"] = email
    request.session["user_name"] = username

    return JsonResponse({"success": True, "username": username})


@require_POST
def auth_login(request):
    """
    Logs a user in by checking email + password against Google Sheet.
    """
    email = request.POST.get("email", "").strip().lower()
    password = request.POST.get("password", "").strip()

    if not email or not password:
        return JsonResponse({"success": False, "error": "Email and password required."}, status=400)

    try:
        ws = get_users_sheet()
        records = ws.get_all_records()
    except Exception as e:
        return JsonResponse({"success": False, "error": f"Sheet error: {e}"}, status=500)

    matched = None
    for row in records:
        row_email = row.get("Email", "").strip().lower()
        row_pass = row.get("Password", "").strip() if "Password" in row else ""
        if row_email == email and row_pass == password:
            matched = row
            break

    if not matched:
        return JsonResponse({"success": False, "error": "Invalid credentials."}, status=401)

    # set session
    request.session["user_email"] = matched.get("Email")
    request.session["user_name"] = matched.get("User Name") or matched.get("Username") or "Guest"

    return JsonResponse({
        "success": True,
        "username": request.session["user_name"],
    })

# Self-learn note:
#  Views are functions called when wanting to display a page.
#  You need to import models to do so.
