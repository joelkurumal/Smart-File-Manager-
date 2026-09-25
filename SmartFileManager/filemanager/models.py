import os

from django.contrib.auth.models import User
from django.db import models


def file_upload_path(instance, filename):
    """
    Store uploaded files inside folders based on category.
    """

    extension = os.path.splitext(filename)[1].lower()

    image_extensions = {
        ".jpg", ".jpeg", ".png", ".gif",
        ".bmp", ".webp", ".svg", ".ico"
    }

    video_extensions = {
        ".mp4", ".avi", ".mkv", ".mov",
        ".wmv", ".webm", ".flv", ".m4v"
    }

    document_extensions = {
        ".pdf", ".doc", ".docx", ".txt",
        ".xls", ".xlsx", ".ppt", ".pptx",
        ".csv", ".odt", ".ods", ".odp"
    }

    if extension in image_extensions:
        folder = "images"

    elif extension in video_extensions:
        folder = "videos"

    elif extension in document_extensions:
        folder = "documents"

    else:
        folder = "others"

    return f"{folder}/{filename}"


class File(models.Model):

    CATEGORY_CHOICES = [
        ("image", "Images"),
        ("video", "Videos"),
        ("document", "Documents"),
        ("other", "Others"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="managed_files"
    )

    file = models.FileField(
        upload_to=file_upload_path
    )

    name = models.CharField(
        max_length=255
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    file_size = models.BigIntegerField(
        default=0
    )

    file_hash = models.CharField(
        max_length=64
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    is_deleted = models.BooleanField(
        default=False
    )

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.name

    @property
    def extension(self):
        return os.path.splitext(self.name)[1].lower()

    @property
    def category_label(self):
        return self.get_category_display()