from django.contrib import admin
from .models import User, EncryptedFile, FileAccessLog

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'department', 'role', 'is_admin', 'is_active']
    list_filter = ['department', 'role', 'is_admin']

@admin.register(EncryptedFile)
class EncryptedFileAdmin(admin.ModelAdmin):
    list_display = ['title', 'allowed_department', 'allowed_role', 'uploaded_by', 'uploaded_at']

@admin.register(FileAccessLog)
class FileAccessLogAdmin(admin.ModelAdmin):
    list_display = ['file', 'user', 'action', 'accessed_at']
