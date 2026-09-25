from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from filemanager import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "register/",
        views.register_view,
        name="register"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "upload/",
        views.upload_file,
        name="upload"
    ),

    path(
        "file/<int:file_id>/",
        views.file_detail,
        name="file_detail"
    ),

    path(
        "file/<int:file_id>/preview/",
        views.preview_file,
        name="preview"
    ),

    path(
        "download/<int:file_id>/",
        views.download_file,
        name="download"
    ),

    path(
        "trash/",
        views.trash,
        name="trash"
    ),

    path(
        "trash/move/<int:file_id>/",
        views.move_to_trash,
        name="move_to_trash"
    ),

    path(
        "trash/restore/<int:file_id>/",
        views.restore_file,
        name="restore"
    ),

    path(
        "trash/delete/<int:file_id>/",
        views.permanent_delete,
        name="permanent_delete"
    ),
]


if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )