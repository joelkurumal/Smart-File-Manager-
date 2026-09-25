import hashlib
import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import LoginForm, RegisterForm
from .models import File


# =========================================================
# HOME
# =========================================================

def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    return redirect("login")


# =========================================================
# REGISTER
# =========================================================

def register_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                "Account created successfully."
            )

            return redirect("dashboard")

    else:
        form = RegisterForm()

    return render(
        request,
        "filemanager/register.html",
        {
            "form": form
        }
    )


# =========================================================
# LOGIN
# =========================================================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":

        form = LoginForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(
                username=username,
                password=password
            )

            if user is not None:

                login(request, user)

                messages.success(
                    request,
                    "Welcome back!"
                )

                return redirect("dashboard")

    else:
        form = LoginForm()

    return render(
        request,
        "filemanager/login.html",
        {
            "form": form
        }
    )


# =========================================================
# LOGOUT
# =========================================================

@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out."
    )

    return redirect("login")


# =========================================================
# FILE CATEGORY
# =========================================================

def get_category(filename):

    extension = os.path.splitext(filename)[1].lower()

    image_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".webp",
        ".svg",
        ".ico",
    }

    video_extensions = {
        ".mp4",
        ".avi",
        ".mkv",
        ".mov",
        ".wmv",
        ".webm",
        ".flv",
        ".m4v",
    }

    document_extensions = {
        ".pdf",
        ".doc",
        ".docx",
        ".txt",
        ".xls",
        ".xlsx",
        ".ppt",
        ".pptx",
        ".csv",
        ".odt",
        ".ods",
        ".odp",
    }

    if extension in image_extensions:
        return "image"

    elif extension in video_extensions:
        return "video"

    elif extension in document_extensions:
        return "document"

    return "other"


# =========================================================
# FILE HASH
# =========================================================

def get_file_hash(uploaded_file):

    sha256 = hashlib.sha256()

    for chunk in uploaded_file.chunks():
        sha256.update(chunk)

    uploaded_file.seek(0)

    return sha256.hexdigest()


# =========================================================
# DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    files = File.objects.filter(
        user=request.user,
        is_deleted=False
    )

    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    search = request.GET.get(
        "search",
        ""
    ).strip()

    if search:

        files = files.filter(
            Q(name__icontains=search)
        )

    # -----------------------------------------------------
    # CATEGORY FILTER
    # -----------------------------------------------------

    category = request.GET.get(
        "category",
        ""
    )

    if category:

        files = files.filter(
            category=category
        )

    # -----------------------------------------------------
    # SORTING
    # -----------------------------------------------------

    sort = request.GET.get(
        "sort",
        "newest"
    )

    if sort == "oldest":

        files = files.order_by(
            "uploaded_at"
        )

    elif sort == "largest":

        files = files.order_by(
            "-file_size"
        )

    elif sort == "smallest":

        files = files.order_by(
            "file_size"
        )

    else:

        # Newest first
        files = files.order_by(
            "-uploaded_at"
        )

    # -----------------------------------------------------
    # STATISTICS
    # -----------------------------------------------------

    all_files = File.objects.filter(
        user=request.user,
        is_deleted=False
    )

    total_files = all_files.count()

    image_count = all_files.filter(
        category="image"
    ).count()

    video_count = all_files.filter(
        category="video"
    ).count()

    document_count = all_files.filter(
        category="document"
    ).count()

    other_count = all_files.filter(
        category="other"
    ).count()

    total_size = sum(
        file.file_size
        for file in all_files
    )

    context = {

        "files": files,

        "search": search,

        "category": category,

        "sort": sort,

        "total_files": total_files,

        "image_count": image_count,

        "video_count": video_count,

        "document_count": document_count,

        "other_count": other_count,

        "total_size": total_size,
    }

    return render(
        request,
        "filemanager/dashboard.html",
        context
    )


# =========================================================
# UPLOAD
# =========================================================

@login_required
def upload_file(request):

    if request.method != "POST":

        return redirect("dashboard")

    uploaded_files = request.FILES.getlist(
        "files"
    )

    if not uploaded_files:

        messages.error(
            request,
            "Please select at least one file."
        )

        return redirect("dashboard")

    uploaded_count = 0
    duplicate_count = 0

    for uploaded_file in uploaded_files:

        # -------------------------------------------------
        # HASH
        # -------------------------------------------------

        file_hash = get_file_hash(
            uploaded_file
        )

        # -------------------------------------------------
        # DUPLICATE CHECK
        # -------------------------------------------------

        duplicate = File.objects.filter(
            user=request.user,
            file_hash=file_hash,
            is_deleted=False
        ).exists()

        if duplicate:

            duplicate_count += 1

            continue

        # -------------------------------------------------
        # CATEGORY
        # -------------------------------------------------

        category = get_category(
            uploaded_file.name
        )

        # -------------------------------------------------
        # SAVE
        # -------------------------------------------------

        File.objects.create(

            user=request.user,

            file=uploaded_file,

            name=uploaded_file.name,

            category=category,

            file_size=uploaded_file.size,

            file_hash=file_hash,
        )

        uploaded_count += 1

    # -----------------------------------------------------
    # MESSAGES
    # -----------------------------------------------------

    if uploaded_count:

        messages.success(
            request,
            f"{uploaded_count} file(s) uploaded successfully."
        )

    if duplicate_count:

        messages.warning(
            request,
            f"{duplicate_count} duplicate file(s) skipped."
        )

    return redirect("dashboard")


# =========================================================
# FILE DETAIL
# =========================================================

@login_required
def file_detail(request, file_id):

    file = get_object_or_404(
        File,
        id=file_id,
        user=request.user
    )

    if file.is_deleted:

        messages.warning(
            request,
            "This file is in the trash."
        )

        return redirect("trash")

    return render(
        request,
        "filemanager/file_detail.html",
        {
            "file": file
        }
    )


# =========================================================
# PREVIEW
# =========================================================

@login_required
def preview_file(request, file_id):

    file = get_object_or_404(
        File,
        id=file_id,
        user=request.user,
        is_deleted=False
    )

    extension = file.extension

    previewable_extensions = {

        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".webp",
        ".svg",

        ".pdf",

        ".mp4",
        ".webm",
        ".ogg",
    }

    if extension not in previewable_extensions:

        return redirect(
            "download",
            file_id=file.id
        )

    if not file.file:

        raise Http404("File not found.")

    response = FileResponse(
        file.file.open("rb"),
        content_type="application/octet-stream"
    )

    response[
        "Content-Disposition"
    ] = f'inline; filename="{file.name}"'

    return response


# =========================================================
# DOWNLOAD
# =========================================================

@login_required
def download_file(request, file_id):

    file = get_object_or_404(
        File,
        id=file_id,
        user=request.user,
        is_deleted=False
    )

    if not file.file:

        raise Http404("File not found.")

    response = FileResponse(
        file.file.open("rb"),
        as_attachment=True,
        filename=file.name
    )

    return response


# =========================================================
# MOVE TO TRASH
# =========================================================

@login_required
def move_to_trash(request, file_id):

    file = get_object_or_404(
        File,
        id=file_id,
        user=request.user,
        is_deleted=False
    )

    file.is_deleted = True

    file.deleted_at = timezone.now()

    file.save(
        update_fields=[
            "is_deleted",
            "deleted_at"
        ]
    )

    messages.success(
        request,
        f'"{file.name}" moved to trash.'
    )

    return redirect("dashboard")


# =========================================================
# TRASH
# =========================================================

@login_required
def trash(request):

    files = File.objects.filter(
        user=request.user,
        is_deleted=True
    )

    return render(
        request,
        "filemanager/trash.html",
        {
            "files": files
        }
    )


# =========================================================
# RESTORE
# =========================================================

@login_required
def restore_file(request, file_id):

    file = get_object_or_404(
        File,
        id=file_id,
        user=request.user,
        is_deleted=True
    )

    file.is_deleted = False

    file.deleted_at = None

    file.save(
        update_fields=[
            "is_deleted",
            "deleted_at"
        ]
    )

    messages.success(
        request,
        f'"{file.name}" restored successfully.'
    )

    return redirect("trash")


# =========================================================
# PERMANENT DELETE
# =========================================================

@login_required
def permanent_delete(request, file_id):

    file = get_object_or_404(
        File,
        id=file_id,
        user=request.user,
        is_deleted=True
    )

    file_name = file.name

    if file.file:

        file.file.delete(
            save=False
        )

    file.delete()

    messages.success(
        request,
        f'"{file_name}" permanently deleted.'
    )

    return redirect("trash")