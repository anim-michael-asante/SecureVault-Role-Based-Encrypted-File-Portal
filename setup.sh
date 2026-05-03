#!/bin/bash
# SecureVault Setup Script
# Run this once to set up the application

echo "============================================"
echo "       SecureVault — First Time Setup"
echo "============================================"
echo ""

# Install dependencies
echo "[1/4] Installing Python dependencies..."
pip install django cryptography --break-system-packages -q 2>/dev/null || pip install django cryptography -q

echo "[2/4] Creating database tables..."
python manage.py makemigrations core
python manage.py migrate

echo "[3/4] Creating admin account..."
python manage.py shell -c "
from core.models import User
if not User.objects.filter(email='admin@securevault.com').exists():
    User.objects.create_superuser(
        email='admin@securevault.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print('Admin created: admin@securevault.com / admin123')
else:
    print('Admin already exists.')
"

echo "[4/4] Creating media directories..."
mkdir -p media/encrypted_files

echo ""
echo "============================================"
echo "  Setup Complete!"
echo "============================================"
echo ""
echo "  Admin Login:"
echo "    Email:    admin@securevault.com"
echo "    Password: admin123"
echo ""
echo "  Run the server with:"
echo "    python manage.py runserver"
echo ""
echo "  Then open: http://127.0.0.1:8000"
echo "============================================"
