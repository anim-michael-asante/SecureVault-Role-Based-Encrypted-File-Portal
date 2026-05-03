import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.core.files.base import ContentFile
from django.db.models import Count, Sum
from .models import User, EncryptedFile, FileAccessLog
from .forms import LoginForm, RegisterForm, UploadFileForm
from .encryption import encrypt_file, decrypt_file


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                if not form.cleaned_data.get('remember_me'):
                    request.session.set_expiry(0)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
    return render(request, 'core/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! Please log in.')
            return redirect('login')
    return render(request, 'core/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    user = request.user
    if user.is_admin:
        return redirect('admin_dashboard')
    # Get files matching user's department AND role
    accessible_files = EncryptedFile.objects.filter(
        allowed_department=user.department,
        allowed_role=user.role
    )
    recent_access = FileAccessLog.objects.filter(user=user).select_related('file')[:5]
    return render(request, 'core/user_dashboard.html', {
        'files': accessible_files,
        'recent_access': recent_access,
        'file_count': accessible_files.count(),
    })


@login_required
def admin_dashboard(request):
    if not request.user.is_admin:
        return redirect('dashboard')
    total_files = EncryptedFile.objects.count()
    total_users = User.objects.filter(is_admin=False).count()
    total_downloads = FileAccessLog.objects.filter(action='download').count()
    recent_files = EncryptedFile.objects.all()[:8]
    recent_logs = FileAccessLog.objects.select_related('file', 'user').all()[:10]
    dept_stats = User.objects.filter(is_admin=False).values('department').annotate(count=Count('id'))
    return render(request, 'core/admin_dashboard.html', {
        'total_files': total_files,
        'total_users': total_users,
        'total_downloads': total_downloads,
        'recent_files': recent_files,
        'recent_logs': recent_logs,
        'dept_stats': dept_stats,
    })


@login_required
def upload_file(request):
    if not request.user.is_admin:
        return redirect('dashboard')
    form = UploadFileForm()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded = request.FILES['file']
            file_bytes = uploaded.read()
            encrypted_bytes, encrypted_key = encrypt_file(file_bytes)

            enc_file = form.save(commit=False)
            enc_file.original_filename = uploaded.name
            enc_file.uploaded_by = request.user
            enc_file.file_size = len(file_bytes)
            enc_file.encryption_key = encrypted_key

            filename = f"enc_{uploaded.name}.vault"
            enc_file.encrypted_file.save(filename, ContentFile(encrypted_bytes))
            enc_file.save()
            messages.success(request, f'"{enc_file.title}" encrypted and uploaded successfully.')
            return redirect('admin_dashboard')
    return render(request, 'core/upload_file.html', {'form': form})


@login_required
def download_file(request, file_id):
    enc_file = get_object_or_404(EncryptedFile, id=file_id)
    user = request.user

    # Check access
    if not user.is_admin:
        if enc_file.allowed_department != user.department or enc_file.allowed_role != user.role:
            raise Http404("Access denied.")

    # Read and decrypt
    enc_file.encrypted_file.open('rb')
    encrypted_bytes = enc_file.encrypted_file.read()
    enc_file.encrypted_file.close()

    decrypted = decrypt_file(encrypted_bytes, enc_file.encryption_key)

    # Log access
    FileAccessLog.objects.create(file=enc_file, user=user, action='download')
    enc_file.download_count += 1
    enc_file.save(update_fields=['download_count'])

    response = HttpResponse(decrypted, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename="{enc_file.original_filename}"'
    return response


@login_required
def manage_users(request):
    if not request.user.is_admin:
        return redirect('dashboard')
    users = User.objects.filter(is_admin=False).order_by('-date_joined')
    return render(request, 'core/manage_users.html', {'users': users})


@login_required
def delete_file(request, file_id):
    if not request.user.is_admin:
        return redirect('dashboard')
    enc_file = get_object_or_404(EncryptedFile, id=file_id)
    if request.method == 'POST':
        if enc_file.encrypted_file:
            try:
                os.remove(enc_file.encrypted_file.path)
            except:
                pass
        enc_file.delete()
        messages.success(request, 'File deleted successfully.')
    return redirect('admin_dashboard')


@login_required
def toggle_user(request, user_id):
    if not request.user.is_admin:
        return redirect('dashboard')
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
    return redirect('manage_users')
