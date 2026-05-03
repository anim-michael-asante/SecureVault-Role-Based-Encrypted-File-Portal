from django import forms
from .models import User, EncryptedFile, DEPARTMENT_CHOICES, ROLE_CHOICES


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'you@company.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))
    remember_me = forms.BooleanField(required=False)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '••••••••'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'department', 'role']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'John'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Doe'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@company.com'}),
        }

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password')
        p2 = cleaned.get('confirm_password')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UploadFileForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = EncryptedFile
        fields = ['title', 'description', 'allowed_department', 'allowed_role']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Document title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Brief description...', 'rows': 3}),
        }
