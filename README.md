# SecureVault — Enterprise Role-Based Encrypted File Portal

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2+-green?style=flat-square&logo=django&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-gray?style=flat-square)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=flat-square)
![Encryption](https://img.shields.io/badge/Encryption-AES--256-red?style=flat-square)

<img width="1412" height="924" alt="image" src="https://github.com/user-attachments/assets/3275314d-9f6a-46a8-9766-843ce7a52d4c" />
<img width="1609" height="927" alt="image" src="https://github.com/user-attachments/assets/a07e822a-aacb-458e-adbe-fa69412c3df8" />
<img width="1813" height="922" alt="image" src="https://github.com/user-attachments/assets/2c3a7fb2-2f08-41bc-838a-7aded7faf358" />
<img width="1740" height="922" alt="image" src="https://github.com/user-attachments/assets/ced2d9da-cbfc-47d3-b37d-622c8dd62a8e" />





> A secure, production-ready Django web application for enterprise document management with AES-256 encryption and granular role-based access control.

---

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
- [Departments & Roles](#departments--roles)
- [License](#license)

---

## Features

### Security

- **AES-256 Encryption** — Military-grade Fernet symmetric encryption for all uploaded files
- **Master Key Derivation** — PBKDF2-HMAC-SHA256 with 100,000 iterations for key hardening
- **Role-Based Access Control (RBAC)** — Fine-grained permissions based on department and role
- **Access Logging** — Complete audit trail of all file downloads and user actions
- **Secure Password Hashing** — Django's PBKDF2 password hashing with salt

### User Management

- **Admin Portal** — Comprehensive administrative dashboard for user and file management
- **User Self-Registration** — New users can register with department and role selection
- **User Lifecycle** — Suspend/activate user accounts without deletion
- **Department/Role Framework** — 8 departments × 9 roles for flexible organizational structures
- **Activity Tracking** — View download statistics and access logs per user

###  File Management

- **Multi-Format Support** — Upload any file type with automatic encryption
- **Access Control Rules** — Files visible only to users matching specified department + role
- **Metadata Management** — Store file title, description, upload date, and access counts
- **On-The-Fly Decryption** — Files decrypted securely only when downloaded
- **Unique Encryption Keys** — Each file encrypted with its own key, then key encrypted with master key

### Monitoring & Analytics

- **Access Logs** — Timestamp, user, file, and IP address for every download
- **Download Statistics** — Track file popularity and access patterns
- **User Activity Dashboard** — Monitor user engagement and suspicious access

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Browser (Client)                     │
└──────────────────┬──────────────────────────────────────────┘
                   │ HTTP/HTTPS
┌──────────────────▼──────────────────────────────────────────┐
│                  Django Web Application                      │
│  ┌──────────────────┬───────────────────────────────────┐   │
│  │   URL Router     │   Views & Forms                   │   │
│  │   (urls.py)      │   (views.py, forms.py)            │   │
│  └──────────────────┴───────────────────────────────────┘   │
│  ┌───────────────────────────────────────────────────────┐   │
│  │  Authentication & Authorization (Django Auth + RBAC)  │   │
│  │  • Session-based authentication                       │   │
│  │  • Department/role-based access control               │   │
│  │  • User permission enforcement                        │   │
│  └───────────────────────────────────────────────────────┘   │
│  ┌───────────────────────────────────────────────────────┐   │
│  │  Models Layer (models.py)                             │   │
│  │  • User (custom with email auth)                      │   │
│  │  • EncryptedFile (metadata + encrypted blob)          │   │
│  │  • FileAccessLog (audit trail)                        │   │
│  └───────────────────────────────────────────────────────┘   │
│  ┌───────────────────────────────────────────────────────┐   │
│  │  Encryption Engine (encryption.py)                    │   │
│  │  • PBKDF2 master key derivation                       │   │
│  │  • Fernet symmetric encryption/decryption             │   │
│  │  • Per-file unique key generation                     │   │
│  └───────────────────────────────────────────────────────┘   │
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

| Layer                 | Technology                   | Version |
| --------------------- | ---------------------------- | ------- |
| **Backend Framework** | Django                       | 4.2+    |
| **Cryptography**      | cryptography (Fernet)        | 41.0+   |
| **Image Processing**  | Pillow                       | 10.0+   |
| **Database**          | SQLite3                      | Default |
| **Web Server**        | Django Dev Server / Gunicorn | Latest  |
| **Language**          | Python                       | 3.11+   |

---

## Prerequisites

- **Python 3.11+** installed on your system
- **pip** package manager
- **Git** (for cloning the repository)
- **4 GB RAM** minimum
- **500 MB** free disk space (media storage grows with uploads)

### OS-Specific Requirements

**Linux / macOS:**

```bash
# Debian/Ubuntu
sudo apt-get install python3 python3-pip python3-dev

# macOS (Homebrew)
brew install python3
```

**Windows:**

Download Python 3.11+ from [python.org](https://www.python.org/downloads/) and ensure **"Add Python to PATH"** is checked during installation.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/anim-michael-asante/securevault.git
cd securevault
```

### 2. Create a Virtual Environment

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

### 4. Run the Setup Script

```bash
# Linux/macOS
bash setup.sh

# Windows (PowerShell — run manually)
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

> ⚠️ **Security Warning:** Change the admin password immediately before deploying to production. See [Configuration](#configuration).

### First Steps

1. **Log in** with admin credentials
2. **Navigate** to the Admin Dashboard
3. **Create users** via "Manage Users" or allow self-registration
4. **Upload encrypted files** with department/role targeting
5. **Test access** by logging in with a regular user account

---

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
MASTER_PASSWORD=your-strong-random-password
MASTER_SALT=your-random-salt
```

### Change Admin Password

```bash
python manage.py changepassword admin@securevault.com
```

### Master Encryption Key

> ⚠️ **Critical:** Update the master key in `core/encryption.py` before going to production.

```python
#  DO NOT USE IN PRODUCTION
MASTER_PASSWORD = b"securevault-master-key-2025"
MASTER_SALT = b"securevault-salt"

#  Use environment variables instead
import os
MASTER_PASSWORD = os.getenv('MASTER_PASSWORD').encode()
MASTER_SALT = os.getenv('MASTER_SALT').encode()
```

### PostgreSQL (Production)

Replace the default SQLite config in `securevault/settings.py`:

```python
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

**Upload Encrypted Files**

1. Click **"Upload File"** in the dashboard
2. Select a file from your computer
3. Enter title and description
4. Choose **Department** and **Role** for access targeting
5. Click **"Encrypt & Upload"** — file is AES-256 encrypted server-side

**Manage Users**

1. Go to **"Manage Users"**
2. View all registered users with department/role
3. **Suspend** users to block access without deletion
4. **Activate** previously suspended users

**View Access Logs**

1. Check download statistics per file
2. View the audit trail — who accessed what and when
3. Monitor suspicious access patterns

### User Workflow

**Register**

1. Click **"Register"** on the login page
2. Enter name, email, department, and role
3. Create a password — account is active immediately

**Browse & Download Files**

1. Log in with email and password
2. Dashboard shows only files matching your department + role
3. Click **"Download"** — file is decrypted on-the-fly and served with the original filename
4. Every download is logged with timestamp and IP address

---

## Security

### Encryption Flow

**Encryption:**

```
Original File
    ↓
[Generate unique Fernet key per file]
    ↓
[Encrypt file with Fernet (AES-256 CBC + HMAC)]
    ↓
[Encrypt file key with Master Key via PBKDF2-HMAC-SHA256]
    ↓
[Store: encrypted blob + encrypted key → .vault file]
```

**Decryption:**

```
Encrypted File + Encrypted File Key
    ↓
[Decrypt file key using Master Key]
    ↓
[Decrypt file using recovered file key]
    ↓
[Serve plaintext to authorized user only]
```

### Implemented Security Controls

| Control          | Implementation                         |
| ---------------- | -------------------------------------- |
| File Encryption  | AES-256 via Fernet (symmetric)         |
| Key Derivation   | PBKDF2-HMAC-SHA256, 100,000 iterations |
| Key Isolation    | Unique per-file key, never reused      |
| Authentication   | Django session-based                   |
| CSRF Protection  | Django CSRF middleware                 |
| SQL Injection    | Django ORM parameterized queries       |
| Password Storage | PBKDF2 with salt (Django default)      |
| Audit Logging    | Timestamp + IP per download            |

### Production Security Checklist

- [ ] Change `MASTER_PASSWORD` and `MASTER_SALT` to strong random values
- [ ] Set `DEBUG = False` in `settings.py`
- [ ] Generate a new `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Enable HTTPS via Nginx reverse proxy
- [ ] Switch to PostgreSQL
- [ ] Set `SESSION_COOKIE_SECURE = True`
- [ ] Enable HSTS: `SECURE_HSTS_SECONDS = 31536000`
- [ ] Implement rate limiting on login
- [ ] Set up automated backups
- [ ] Enable audit log monitoring
- [ ] Consider 2FA for admin accounts

---

## Project Structure

```
securevault/
├── manage.py                       # Django management script
├── db.sqlite3                      # SQLite database
├── requirements.txt                # Python dependencies
├── setup.sh                        # Automated setup script
├── README.md
│
├── securevault/                    # Django project config
│   ├── settings.py                 # Settings & configuration
│   ├── urls.py                     # Main URL routing
│   └── wsgi.py                     # WSGI entry point
│
├── core/                           # Core application
│   ├── models.py                   # User, EncryptedFile, FileAccessLog
│   ├── views.py                    # Auth, upload, download logic
│   ├── forms.py                    # Login, Register, Upload forms
│   ├── encryption.py               # AES-256 encrypt/decrypt utilities
│   ├── urls.py                     # App-level URL routing
│   ├── admin.py                    # Django admin customization
│   ├── migrations/
│   │   └── 0001_initial.py
│   └── templates/core/
│       ├── base.html
│       ├── login.html
│       ├── register.html
│       ├── admin_dashboard.html
│       ├── manage_users.html
│       ├── upload_file.html
│       └── user_dashboard.html
│
├── static/core/
│   ├── css/
│   └── js/
│
└── media/
    └── encrypted_files/
        └── enc_*.vault             # Encrypted file storage
```

---

## Database Schema

### User

```
User
├── id                (AutoField, PK)
├── email             (EmailField, unique)
├── password          (CharField, hashed)
├── first_name        (CharField)
├── last_name         (CharField)
├── department        (CharField, 8 choices)
├── role              (CharField, 9 choices)
├── is_active         (BooleanField)
├── is_staff          (BooleanField)
├── is_superuser      (BooleanField)
├── date_joined       (DateTimeField)
└── last_login        (DateTimeField)
```

### EncryptedFile

```
EncryptedFile
├── id                (AutoField, PK)
├── uploaded_by       (ForeignKey → User)
├── title             (CharField)
├── description       (TextField)
├── department_access (CharField, 8 choices)
├── role_access       (CharField, 9 choices)
├── file_blob         (BinaryField, encrypted)
├── encrypted_file_key(BinaryField, encrypted key)
├── original_filename (CharField)
├── upload_date       (DateTimeField, auto_now_add)
├── download_count    (IntegerField, default=0)
└── file_size         (IntegerField, bytes)
```

### FileAccessLog

```
FileAccessLog
├── id                (AutoField, PK)
├── user              (ForeignKey → User)
├── encrypted_file    (ForeignKey → EncryptedFile)
├── accessed_at       (DateTimeField, auto_now_add)
├── ip_address        (GenericIPAddressField)
└── user_agent        (TextField)
```

---

## API Endpoints

### Authentication

| Method | Endpoint     | Description             |
| ------ | ------------ | ----------------------- |
| `GET`  | `/login/`    | Login page              |
| `POST` | `/login/`    | Process login           |
| `GET`  | `/register/` | Registration page       |
| `POST` | `/register/` | Create new user account |
| `GET`  | `/logout/`   | Logout user             |

### Admin Panel

| Method | Endpoint               | Description               |
| ------ | ---------------------- | ------------------------- |
| `GET`  | `/admin-dashboard/`    | Admin control panel       |
| `POST` | `/upload-file/`        | Upload and encrypt file   |
| `GET`  | `/manage-users/`       | User management interface |
| `POST` | `/suspend-user/<id>/`  | Suspend user account      |
| `POST` | `/activate-user/<id>/` | Reactivate user account   |
| `GET`  | `/access-logs/`        | File access audit trail   |

### User Portal

| Method | Endpoint               | Description               |
| ------ | ---------------------- | ------------------------- |
| `GET`  | `/user-dashboard/`     | User file listing         |
| `GET`  | `/download/<file_id>/` | Download and decrypt file |
| `GET`  | `/my-activity/`        | User's access history     |

### Admin JSON API

| Method   | Endpoint          | Description                 |
| -------- | ----------------- | --------------------------- |
| `GET`    | `/api/users/`     | List all users (admin only) |
| `GET`    | `/api/files/`     | List all files (admin only) |
| `GET`    | `/api/logs/`      | Audit logs (admin only)     |
| `DELETE` | `/api/user/<id>/` | Delete user (admin only)    |

---

## Development

### Run Development Server

```bash
source .venv/bin/activate       # Linux/macOS
.\.venv\Scripts\Activate.ps1    # Windows

python manage.py runserver
python manage.py runserver 8080  # Custom port
```

### Database Migrations

```bash
python manage.py makemigrations core   # Create migrations
python manage.py migrate               # Apply migrations
python manage.py showmigrations core   # View status
```

### Interactive Shell

```bash
python manage.py shell

from core.models import User, EncryptedFile
User.objects.all()
EncryptedFile.objects.filter(department_access='engineering')
```

### Tests

```bash
python manage.py test               # Run all tests
python manage.py test core.tests    # Run specific tests
python manage.py test -v 2          # Verbose output
```

### Code Style

```bash
black core/     # Format with Black
flake8 core/    # Lint with Flake8
```

---

## Deployment

### Gunicorn

```bash
pip install gunicorn

export MASTER_PASSWORD="your-strong-key"
gunicorn securevault.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Nginx Reverse Proxy

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

### Docker

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

| Error                         | Fix                                                                           |
| ----------------------------- | ----------------------------------------------------------------------------- |
| `No module named 'django'`    | Activate virtual environment: `source .venv/bin/activate`                     |
| `No such table: core_user`    | Run `python manage.py migrate`                                                |
| `CSRF verification failed`    | Clear browser cookies; ensure `{% csrf_token %}` in forms                     |
| `Permission denied` on upload | Run `mkdir -p media/encrypted_files && chmod 755 media/encrypted_files`       |
| Static files not loading      | Run `python manage.py collectstatic --noinput`                                |
| `Decryption failed`           | Verify `MASTER_PASSWORD` and `MASTER_SALT` match original encryption settings |

### Enable Debug Logging

```python
# securevault/settings.py — development only
DEBUG = True
ALLOWED_HOSTS = ['*']

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

> ⚠️ Never enable `DEBUG = True` in production.

---

## Departments & Roles

### 8 Departments

| Department      | Typical Teams                    |
| --------------- | -------------------------------- |
| Engineering     | DevOps, QA, Product Dev          |
| Marketing       | Brand, Content, Campaigns        |
| Finance         | Accounting, Budgeting, Analysis  |
| Human Resources | Recruitment, Benefits, Payroll   |
| Operations      | Supply Chain, Facilities, Admin  |
| Legal           | Contracts, Compliance, Counsel   |
| Sales           | Business Dev, Account Management |
| Executive       | C-Suite, Board, Strategic        |

### 9 Roles

| Role           | Experience Level         |
| -------------- | ------------------------ |
| Intern         | Entry level              |
| Junior         | 0–3 years                |
| Mid-level      | 3–7 years                |
| Senior         | 7+ years                 |
| Lead           | Team lead / mentor       |
| Manager        | 5–20 direct reports      |
| Director       | 20+ direct reports       |
| Vice President | Strategic responsibility |
| C-Level        | CTO, CFO, CEO, etc.      |

---

## Contributing

1. **Fork** the repository
2. **Create** a feature branch — `git checkout -b feature/your-feature`
3. **Commit** with a clear message — `git commit -m "feat: add X"`
4. **Push** to your branch — `git push origin feature/your-feature`
5. **Open** a Pull Request

Follow PEP 8, use 4-space indentation, and write docstrings for all functions.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [Django](https://www.djangoproject.com/) — Web framework
- [cryptography](https://cryptography.io/) — Fernet AES-256 implementation
- Python open-source community

---

<p align="center">Made with ❤️ by <a href="https://github.com/anim-michael-asante">0x1aerixis</a> · Last Updated: May 2026</p>
