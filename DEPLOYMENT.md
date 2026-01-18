# GeniusGSM Django Deployment Guide for Windows Server

## المتطلبات:
- Windows Server 2019+ 
- Python 3.8+
- PostgreSQL 12+
- Nginx

---

## 1️⃣ على جهازك المحلي (قبل رفع الملفات):

### تحضير المشروع:
```bash
# جمع Static Files
python manage.py collectstatic --noinput

# إنشاء Migrations
python manage.py makemigrations
python manage.py migrate

# اختبر الإعدادات
python manage.py check --deploy
```

### تحديث المتطلبات:
```bash
pip freeze > requirements.txt
```

### رفع على GitHub:
```bash
git add .
git commit -m "Deployment: Production settings configured"
git push origin main
```

---

## 2️⃣ على Windows Server:

### A. تثبيت البرامج:

```powershell
# تثبيت PostgreSQL (استخدم installer من postgresql.org)
# تثبيت Nginx (من nginx.org)
```

### B. استنساخ المشروع:

```powershell
cd C:\
git clone https://github.com/anahhal98-dot/GeniusGsm.git
cd GeniusGsm
```

### C. إعداد البيئة الافتراضية:

```powershell
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
```

### D. إعداد قاعدة البيانات PostgreSQL:

```sql
-- في PostgreSQL
CREATE DATABASE geniusgsm;
CREATE USER geniusgsm_user WITH PASSWORD 'strong_password_here';
ALTER ROLE geniusgsm_user SET client_encoding TO 'utf8';
ALTER ROLE geniusgsm_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE geniusgsm_user SET default_transaction_deferrable TO on;
ALTER ROLE geniusgsm_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE geniusgsm TO geniusgsm_user;
```

### E. تحديث settings.py:

أضف في `project/settings.py`:

```python
import os
from decouple import config

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'geniusgsm',
        'USER': 'geniusgsm_user',
        'PASSWORD': 'strong_password_here',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### F. تشغيل Migrations:

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### G. تشغيل Gunicorn:

```powershell
gunicorn -c gunicorn_config.py project.wsgi:application
```

### H. إعداد Nginx:

انسخ ملف `nginx.conf` إلى مجلد Nginx:
```
C:\nginx\conf\sites-available\geniusgsm.conf
```

### I. ربط الدومين:

1. تأكد من DNS يشير إلى `20.106.211.19`
2. قم بتشغيل Nginx
3. اختبر في المتصفح

### J. SSL Certificate (Let's Encrypt):

```powershell
# تثبيت Certbot
pip install certbot certbot-nginx

# الحصول على شهادة
certbot certonly --nginx -d geniusgsm.com -d www.geniusgsm.com
```

---

## 3️⃣ إنشاء Windows Service لـ Gunicorn:

استخدم `NSSM` (Non-Sucking Service Manager):

```powershell
nssm install GeniusGsm "C:\GeniusGsm\venv\Scripts\gunicorn.exe" "-c gunicorn_config.py project.wsgi:application"
nssm set GeniusGsm AppDirectory "C:\GeniusGsm"
nssm start GeniusGsm
```

---

## ✅ اختبار النشر:

```bash
# التحقق من أن Gunicorn يعمل:
netstat -an | findstr ":8000"

# التحقق من الخطأ في logs:
type C:\GeniusGsm\logs\error.log

# اختبر الموقع:
curl http://localhost:8000/
```

---

## 🔧 استكشاف الأخطاء:

### Nginx لا يقرأ الملفات:
```powershell
# تحقق من مسارات Static و Media في nginx.conf
# تأكد من وجود المجلدات
mkdir C:\GeniusGsm\logs
```

### PostgreSQL لا يتصل:
```powershell
# تحقق من أن PostgreSQL يعمل:
Get-Service postgresql-x64-*

# اختبر الاتصال:
psql -U geniusgsm_user -d geniusgsm -h localhost
```

### SSL لا يعمل:
```powershell
# تحقق من أن الملفات موجودة:
dir "C:\letsencrypt\live\geniusgsm.com\"
```

---

## 📞 الدعم والمراقبة:

- Logs: `C:\GeniusGsm\logs\`
- Database Backup:
  ```powershell
  pg_dump -U geniusgsm_user geniusgsm > backup.sql
  ```

---

**تم بنجاح! 🎉**
