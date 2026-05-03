from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

DEPARTMENT_CHOICES = [
    ('engineering', 'Engineering'),
    ('marketing', 'Marketing'),
    ('finance', 'Finance'),
    ('hr', 'Human Resources'),
    ('operations', 'Operations'),
    ('legal', 'Legal'),
    ('sales', 'Sales'),
    ('executive', 'Executive'),
]

ROLE_CHOICES = [
    ('intern', 'Intern'),
    ('junior', 'Junior'),
    ('mid', 'Mid-level'),
    ('senior', 'Senior'),
    ('lead', 'Lead'),
    ('manager', 'Manager'),
    ('director', 'Director'),
    ('vp', 'Vice President'),
    ('c_level', 'C-Level'),
]


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, blank=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class EncryptedFile(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    original_filename = models.CharField(max_length=255)
    encrypted_file = models.FileField(upload_to='encrypted_files/')
    encryption_key = models.BinaryField()  # stored encrypted key
    allowed_department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    allowed_role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.BigIntegerField(default=0)
    download_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-uploaded_at']


class FileAccessLog(models.Model):
    file = models.ForeignKey(EncryptedFile, on_delete=models.CASCADE, related_name='access_logs')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='file_accesses')
    accessed_at = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=20, choices=[('view', 'Viewed'), ('download', 'Downloaded')])

    class Meta:
        ordering = ['-accessed_at']
