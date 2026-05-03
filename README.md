# SecureVault — Enterprise Role-Based Encrypted File Portal

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square)
![Django](https://img.shields.io/badge/Django-4.2+-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-gray?style=flat-square)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=flat-square)

A secure, production-ready Django web application for enterprise document management. SecureVault enables administrators to upload and manage AES-256 encrypted files with granular department and role-based access controls. Users access only files matching their organizational attributes with automatic on-the-fly decryption.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage](#usage)
- [Security](#security)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [API Endpoints](#api-endpoints)
- [Development](#development)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features

### 🔐 Security

- **AES-256 Encryption**: Military-grade encryption for all uploaded files using Fernet (symmetric encryption)
- **Master Key Derivation**: PBKDF2-HMAC-SHA256 with 100,000 iterations for key hardening
- **Role-Based Access Control (RBAC)**: Fine-grained permissions based on department and role
- **Access Logging**: Complete audit trail of all file downloads and user actions
- **Secure Password Hashing**: Django's PBKDF2 password hashing with salt

### 👥 User Management

- **Admin Portal**: Comprehensive administrative dashboard for user and file management
- **User Self-Registration**: New users can register with department and role selection
- **User Lifecycle**: Suspend/activate user accounts without deletion
- **Department/Role Framework**: 8 departments × 9 roles for flexible organizational structures
- **Activity Tracking**: View download statistics and access logs per user

### 📁 File Management

- **Multi-Format Support**: Upload any file type with automatic encryption
- **Access Control Rules**: Files visible only to users matching specified department + role
- **Metadata Management**: Store file title, description, upload date, and access counts
- **On-The-Fly Decryption**: Files decrypted securely only when downloaded
- **Unique Encryption Keys**: Each file encrypted with unique key, then key encrypted with master key

### 📊 Monitoring & Analytics

- **Access Logs**: Timestamp, user, file, and IP address for every download
- **Download Statistics**: Track file popularity and access patterns
- **User Activity Dashboard**: Monitor user engagement and suspicious access

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Browser (Client)                     │
└──────────────────┬──────────────────────────────────────────┘
                   │ HTTP/HTTPS
┌──────────────────▼──────────────────────────────────────────┐
│              Django Web Application                          │
│  ┌──────────────────┬──────────────────────────────────────┐ │
│  │   URL Router     │   Views & Forms                       │ │
│  │  (urls.py)       │   (views.py, forms.py)                │ │
│  └──────────────────┴──────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Authentication & Authorization (Django Auth + Custom)   │ │
│  │  • Session-based authentication                          │ │
│  │  • Department/role-based access control                  │ │
│  │  • User permission enforcement                           │ │
│  └──────────────────────────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Models Layer (models.py)                                │ │
│  │  • User (custom with email auth)                         │ │
│  │  • EncryptedFile (metadata + encrypted blob)            │ │
│  │  • FileAccessLog (audit trail)                          │ │
│  └──────────────────────────────────────────────────────────┘ │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  Encryption Engine (encryption.py)                       │ │
│  │  • PBKDF2 master key derivation                          │ │
│  │  • Fernet symmetric encryption/decryption                │ │
│  │  • Per-file unique key generation                        │ │
│  └──────────────────────────────────────────────────────────┘ │
└──────────────────┬──────────────────────────────────────────┘
                   │
        ┌──────────┴──────────────┐
        │                         │
┌───────▼────────┐      ┌────────▼────────┐
│  SQLite DB     │      │  Media Storage  │
│ (db.sqlite3)   │      │  Encrypted      │
│                │      │  Files (.vault) │
│ • Users        │      │                 │
│ • Files        │      │ media/          │
│ • Access Logs  │      │ encrypted_files/│
└────────────────┘      └─────────────────┘
```

---

## Tech Stack

| Layer                 | Technology                           | Version |
| --------------------- | ------------------------------------ | ------- |
| **Backend Framework** | Django                               | 4.2+    |
| **Cryptography**      | cryptography (Fernet)                | 41.0+   |
| **Image Processing**  | Pillow                               | 10.0+   |
| **Database**          | SQLite3                              | Default |
| **Web Server**        | Django Development Server / Gunicorn | Latest  |
| **Language**          | Python                               | 3.11+   |

---

## Prerequisites

- **Python 3.11+** installed on your system
- **pip** package manager
- **Git** (for cloning the repository)
- **4GB RAM** minimum
- **500MB** free disk space (media storage grows with uploads)

### OS-Specific Requirements

**Linux/macOS:**

```bash
# Debian/Ubuntu
sudo apt-get install python3 python3-pip python3-dev

# macOS (Homebrew)
brew install python3
```

**Windows:**

- Download Python 3.11+ from [python.org](https://www.python.org/downloads/)
- Ensure "Add Python to PATH" is checked during installation

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/securevault.git
cd securevault
```

### 2. Create Virtual Environment

```bash
# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run Setup Script

```bash
# Linux/macOS
bash setup.sh

# Windows (PowerShell)
python manage.py makemigrations core
python manage.py migrate
python manage.py shell -c "from core.models import User; User.objects.create_superuser(email='admin@securevault.com', password='admin123', first_name='Admin', last_name='User')"
mkdir -p media/encrypted_files
```

### 5. Verify Installation

```bash
python manage.py check
```

---

## Quick Start

### Launch the Application

```bash
python manage.py runserver
```

Application available at: **http://127.0.0.1:8000**

### Default Admin Account

| Field        | Value                 |
| ------------ | --------------------- |
| **Email**    | admin@securevault.com |
| **Password** | admin123              |
| **Role**     | Administrator         |

⚠️ **SECURITY WARNING**: Change the admin password immediately in production. See [Configuration](#configuration) section.

### First Steps

1. **Log in** with admin credentials
2. **Navigate to Admin Dashboard**
3. **Create new users** via "Manage Users" or let them self-register
4. **Upload encrypted files** with department/role targeting
5. **Test user access** by logging in with a regular user account

---

## Configuration

### Environment Setup

Create a `.env` file in the project root (or modify settings):

```bash
# .env (optional, for future extensions)
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
```

### Modify Admin Credentials

Edit [core/models.py](core/models.py) setup in `setup.sh` or use:

```bash
python manage.py changepassword admin@securevault.com
```

### Master Encryption Key

⚠️ **CRITICAL**: Update the master key in [core/encryption.py](core/encryption.py):

```python
# ❌ CHANGE THIS IN PRODUCTION ❌
MASTER_PASSWORD = b"securevault-master-key-2025"  # Use a strong, random value
MASTER_SALT = b"securevault-salt"                  # Use a random salt
```

**Recommended**: Use environment variables:

```python
import os
MASTER_PASSWORD = os.getenv('MASTER_PASSWORD', b'your-strong-password').encode()
MASTER_SALT = os.getenv('MASTER_SALT', b'your-salt').encode()
```

### Database Configuration

Default: SQLite (`db.sqlite3`)

For production, switch to PostgreSQL by modifying [securevault/settings.py](securevault/settings.py):

```python
# PostgreSQL Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'securevault',
        'USER': 'postgres',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## Usage

### Admin Workflow

#### 1. Upload Encrypted Files

1. Click **"Upload File"** in dashboard
2. Select a file from your computer
3. Enter title and description
4. Choose **Department** (who)
5. Choose **Role** (what access level)
6. Click **"Encrypt & Upload"**
7. File is AES-256 encrypted server-side and stored

#### 2. Manage Users

1. Go to **"Manage Users"**
2. View all registered users with department/role
3. **Suspend** users to block access without deletion
4. **Activate** previously suspended users
5. View user activity and last login

#### 3. View Access Logs

1. Check **download statistics** per file
2. View **audit trail** showing who accessed what and when
3. Monitor **suspicious access patterns**

### User Workflow

#### 1. Register

1. Click **"Register"** on login page
2. Enter name, email, select department and role
3. Create password
4. Account active immediately (optional admin approval)

#### 2. Log In & Browse Files

1. Use email and password to log in
2. Dashboard shows only files matching your department + role
3. Download counts and access logs visible

#### 3. Download Files

1. Click **"Download"** on any accessible file
2. File is **automatically decrypted** server-side
3. File downloads to your computer with original name
4. Access logged with timestamp and IP address

---

## Security

### Encryption Scheme

**File Encryption Process:**

```
Original File
    ↓
[Generate unique Fernet key per file]
    ↓
[Encrypt file with Fernet (AES-256)]
    ↓
[Encrypt file key with Master Key (derived via PBKDF2)]
    ↓
[Store: encrypted file + encrypted file key on disk]
```

**File Decryption Process:**

```
Encrypted File + Encrypted File Key (from disk)
    ↓
[Decrypt file key using Master Key]
    ↓
[Decrypt file using decrypted file key]
    ↓
[Serve to authorized user only]
```

### Key Security Practices

✅ **Implemented:**

- **AES-256 Encryption**: Industry-standard symmetric encryption (Fernet)
- **PBKDF2 Key Derivation**: 100,000 iterations, SHA-256 hash
- **Unique Per-File Keys**: No key reuse across files
- **Session-Based Authentication**: Django built-in session framework
- **CSRF Protection**: Django CSRF middleware enabled
- **SQL Injection Prevention**: Django ORM parameterized queries
- **Password Hashing**: PBKDF2 with salt (Django default)
- **Audit Logging**: All downloads recorded with timestamp/IP

### Security Checklist for Production

- [ ] Change `MASTER_PASSWORD` and `MASTER_SALT` to strong random values
- [ ] Set `DEBUG = False` in settings.py
- [ ] Generate new `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Enable HTTPS (use reverse proxy like Nginx)
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set secure session cookies: `SESSION_COOKIE_SECURE = True`
- [ ] Enable HSTS: `SECURE_HSTS_SECONDS = 31536000`
- [ ] Implement rate limiting on login
- [ ] Regular backups of encrypted files and database
- [ ] Regular security audits of access logs
- [ ] Consider implementing 2FA for admin accounts

---

## Project Structure

```
securevault/
├── manage.py                          # Django management script
├── db.sqlite3                         # SQLite database
├── requirements.txt                   # Python dependencies
├── setup.sh                           # Automated setup script
├── README.md                          # This file
│
├── securevault/                       # Main Django app config
│   ├── __init__.py
│   ├── settings.py                    # Django settings & configuration
│   ├── urls.py                        # Main URL routing
│   └── wsgi.py                        # WSGI entry point
│
├── core/                              # Core application logic
│   ├── __init__.py
│   ├── admin.py                       # Django admin customization
│   ├── apps.py                        # App configuration
│   ├── models.py                      # Database models (User, EncryptedFile, FileAccessLog)
│   ├── views.py                       # View functions (authentication, upload, download)
│   ├── forms.py                       # Django forms (Login, Register, Upload)
│   ├── encryption.py                  # AES-256 encryption/decryption utilities
│   ├── urls.py                        # App-level URL routing
│   │
│   ├── migrations/                    # Database migrations
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   │
│   └── templates/core/                # HTML templates
│       ├── base.html                  # Base template with navigation
│       ├── login.html                 # Login page
│       ├── register.html              # User registration
│       ├── admin_dashboard.html       # Admin control panel
│       ├── base_dashboard.html        # Shared dashboard base
│       ├── manage_users.html          # User management interface
│       ├── upload_file.html           # File upload form
│       └── user_dashboard.html        # User file access portal
│
├── static/                            # Static files
│   └── core/
│       ├── css/                       # Stylesheets
│       └── js/                        # JavaScript
│
└── media/                             # User-uploaded encrypted files
    └── encrypted_files/               # Encrypted files storage
        └── enc_*.vault                # Encrypted file format
```

---

## Database Schema

### User Model

```
User
├── id (AutoField, Primary Key)
├── email (EmailField, Unique)
├── password (CharField, hashed)
├── first_name (CharField)
├── last_name (CharField)
├── department (CharField, choices: 8 departments)
├── role (CharField, choices: 9 roles)
├── is_active (BooleanField)
├── is_staff (BooleanField)
├── is_superuser (BooleanField)
├── date_joined (DateTimeField)
└── last_login (DateTimeField)
```

### EncryptedFile Model

```
EncryptedFile
├── id (AutoField, Primary Key)
├── uploaded_by (ForeignKey → User)
├── title (CharField)
├── description (TextField)
├── department_access (CharField, choices: 8 departments)
├── role_access (CharField, choices: 9 roles)
├── file_blob (BinaryField, encrypted)
├── encrypted_file_key (BinaryField, encrypted key)
├── original_filename (CharField)
├── upload_date (DateTimeField, auto_now_add)
├── download_count (IntegerField, default=0)
└── file_size (IntegerField, bytes)
```

### FileAccessLog Model

```
FileAccessLog
├── id (AutoField, Primary Key)
├── user (ForeignKey → User)
├── encrypted_file (ForeignKey → EncryptedFile)
├── accessed_at (DateTimeField, auto_now_add)
├── ip_address (GenericIPAddressField)
└── user_agent (TextField)
```

---

## API Endpoints

### Authentication

| Method | Endpoint     | Description             |
| ------ | ------------ | ----------------------- |
| GET    | `/login/`    | Login page              |
| POST   | `/login/`    | Process login           |
| GET    | `/register/` | Registration page       |
| POST   | `/register/` | Create new user account |
| GET    | `/logout/`   | Logout user             |

### Admin Panel

| Method | Endpoint               | Description                  |
| ------ | ---------------------- | ---------------------------- |
| GET    | `/admin-dashboard/`    | Admin control panel          |
| POST   | `/upload-file/`        | Upload and encrypt file      |
| GET    | `/manage-users/`       | User management interface    |
| POST   | `/suspend-user/<id>/`  | Suspend user account         |
| POST   | `/activate-user/<id>/` | Reactivate user account      |
| GET    | `/access-logs/`        | View file access audit trail |

### User Portal

| Method | Endpoint               | Description               |
| ------ | ---------------------- | ------------------------- |
| GET    | `/user-dashboard/`     | User file listing         |
| GET    | `/download/<file_id>/` | Download and decrypt file |
| GET    | `/my-activity/`        | User's access history     |

### Admin API (JSON)

| Method | Endpoint          | Description                 |
| ------ | ----------------- | --------------------------- |
| GET    | `/api/users/`     | List all users (admin only) |
| GET    | `/api/files/`     | List all files (admin only) |
| GET    | `/api/logs/`      | Audit logs (admin only)     |
| DELETE | `/api/user/<id>/` | Delete user (admin only)    |

---

## Development

### Running in Development Mode

```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.\.venv\Scripts\Activate.ps1  # Windows

# Run development server with auto-reload
python manage.py runserver

# Run with custom port
python manage.py runserver 8080
```

### Database Migrations

```bash
# Create new migrations after model changes
python manage.py makemigrations core

# Apply pending migrations
python manage.py migrate

# View migration status
python manage.py showmigrations core

# Reverse to previous migration
python manage.py migrate core 0001_initial
```

### Interactive Shell

```bash
python manage.py shell

# Example commands:
from core.models import User, EncryptedFile
User.objects.all()
EncryptedFile.objects.filter(department_access='engineering')
```

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test core.tests.UserTestCase

# Verbose output
python manage.py test -v 2
```

### Code Style

```bash
# Format code with Black
black core/

# Lint with Flake8
flake8 core/
```

---

## Deployment

### Production Checklist

- [ ] Update all default credentials
- [ ] Change MASTER_PASSWORD and MASTER_SALT
- [ ] Set DEBUG=False
- [ ] Generate new SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up HTTPS/SSL certificate
- [ ] Use PostgreSQL (not SQLite)
- [ ] Set up environment variables
- [ ] Configure static file serving (Nginx/Apache)
- [ ] Set up regular backups
- [ ] Configure logging and monitoring

### Using Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn securevault.wsgi:application --bind 0.0.0.0:8000 --workers 4

# Use environment variables
export MASTER_PASSWORD="your-strong-key"
gunicorn securevault.wsgi:application --bind 0.0.0.0:8000
```

### Using Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        alias /path/to/securevault/static/;
    }

    location /media/ {
        alias /path/to/securevault/media/;
    }
}
```

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "securevault.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```bash
docker build -t securevault:latest .
docker run -p 8000:8000 securevault:latest
```

---

## Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError: No module named 'django'

```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
.\.venv\Scripts\Activate.ps1  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### 2. "No such table: core_user"

```bash
# Run migrations
python manage.py migrate
```

#### 3. "CSRF verification failed"

- Clear browser cookies for localhost
- Ensure CSRF middleware is enabled in settings.py
- Check that forms include `{% csrf_token %}`

#### 4. File upload fails / "Permission denied"

```bash
# Ensure media directory exists and is writable
mkdir -p media/encrypted_files
chmod 755 media/encrypted_files
```

#### 5. Static files not loading

```bash
# Collect static files
python manage.py collectstatic --noinput
```

#### 6. "Decryption failed" error

- Verify MASTER_PASSWORD and MASTER_SALT match original encryption
- Check encrypted file not corrupted
- Ensure master key hasn't changed

### Debug Mode

Enable detailed error messages (development only):

```python
# securevault/settings.py
DEBUG = True
ALLOWED_HOSTS = ['*']
```

⚠️ Never enable DEBUG in production!

### Logs

Check Django logs:

```bash
# Enable file logging in settings.py
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
}
```

---

## Departments & Roles

### 8 Supported Departments

1. **Engineering** - Product development, DevOps, QA
2. **Marketing** - Brand, content, campaigns
3. **Finance** - Accounting, budgeting, analysis
4. **Human Resources** - Recruitment, benefits, payroll
5. **Operations** - Supply chain, facilities, admin
6. **Legal** - Contracts, compliance, counsel
7. **Sales** - Business development, account management
8. **Executive** - C-suite, board, strategic

### 9 Supported Roles

1. **Intern** - Entry level, learning
2. **Junior** - Early career (0-3 years)
3. **Mid-level** - Mid career (3-7 years)
4. **Senior** - Experienced (7+ years)
5. **Lead** - Team lead, mentor
6. **Manager** - Department manager, 5-20 reports
7. **Director** - Director level, 20+ reports
8. **Vice President** - VP, strategic responsibility
9. **C-Level** - CTO, CFO, CEO, etc.

---

## Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/your-feature`)
3. **Commit** changes with clear messages
4. **Push** to branch
5. **Create** a Pull Request

### Code Style

- Follow PEP 8
- Use 4-space indentation
- Write docstrings for functions
- Keep functions small and focused

---

## License

This project is licensed under the **MIT License** - see LICENSE file for details.

---

## Support

For issues, questions, or suggestions:

- 📧 Email: support@securevault.io
- 🐛 Report bugs on GitHub Issues
- 💬 Discussions: GitHub Discussions tab

---

## Acknowledgments

- Django Framework
- cryptography library (Fernet)
- Python community

---

**Made with ❤️ | Last Updated: May 2026**
