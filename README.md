# 🎓 College Management System

A professional, full-featured College Management System built with **Django + SQLite**.

---

## 🚀 Features

| Module | Features |
|--------|----------|
| **Authentication** | 4 Role-based logins: Principal, Staff, Clerk, Accountant |
| **Dashboard** | Role-specific stats, charts, quick actions |
| **Students** | Full CRUD, PRN/Admission No, parent info, photos |
| **Classes** | Class-wise management, department-wise grouping |
| **Attendance** | Subject-wise, lecture-wise, % calculation, low attendance alerts |
| **Results** | Exams, marks entry, auto grading, practical marks |
| **Finance** | Fee collection, receipts, expense tracking, scholarships |
| **Bonafide** | Certificate generator with print layout |
| **Leaving Cert** | Leaving certificate with print layout |
| **Admin Panel** | Full Django admin for superusers |

---

## 📋 Setup Instructions

### 1. Install Python (3.10+)
Download from https://python.org

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Migrations
```bash
python manage.py makemigrations accounts
python manage.py makemigrations students
python manage.py makemigrations attendance
python manage.py makemigrations results
python manage.py makemigrations finance
python manage.py makemigrations bonafide
python manage.py makemigrations core
python manage.py migrate
```

### 4. Load Demo Data (includes 40 students, staff, subjects, fee structures)
```bash
python setup_demo.py
```

### 5. Start Server
```bash
python manage.py runserver
```

### 6. Open Browser
```
http://127.0.0.1:8000/
```

---

## 🔑 Login Credentials (after running setup_demo.py)

| Role | Username | Password |
|------|----------|----------|
| Admin (Django Admin) | `admin` | `admin123` |
| Principal | `principal` | `principal@123` |
| Staff / Teacher | `staff1` | `staff@123` |
| Clerk | `clerk1` | `clerk@123` |
| Accountant | `accountant1` | `accountant@123` |

---

## 🔐 Role Permissions

| Feature | Principal | Staff | Clerk | Accountant |
|---------|-----------|-------|-------|------------|
| Dashboard | ✅ Full | ✅ Limited | ✅ Limited | ✅ Limited |
| View Students | ✅ | ✅ | ✅ | ✅ |
| Add/Edit Students | ✅ | ❌ | ✅ | ❌ |
| Take Attendance | ✅ | ✅ | ❌ | ❌ |
| Enter Marks | ✅ | ✅ | ❌ | ❌ |
| Collect Fee | ✅ | ❌ | ❌ | ✅ |
| View Finance | ✅ | ❌ | ❌ | ✅ |
| Issue Bonafide | ✅ | ❌ | ✅ | ❌ |
| Issue Leaving Cert | ✅ | ❌ | ✅ | ❌ |
| Manage Staff | ✅ | ❌ | ❌ | ❌ |
| Admin Panel | ✅ | ❌ | ❌ | ❌ |

---

## 📁 Project Structure

```
college_mgmt/
├── college_mgmt/        ← Django project settings
│   ├── settings.py
│   └── urls.py
├── accounts/            ← Custom user model, login/logout
├── students/            ← Student, Class, Department models
├── attendance/          ← Subject, Attendance models
├── results/             ← Exam, Marks, Practical models
├── finance/             ← Fee, Expense, Scholarship models
├── bonafide/            ← Bonafide, Leaving Certificate
├── core/                ← Dashboard
├── templates/           ← All HTML templates
├── static/              ← CSS, JS assets
├── setup_demo.py        ← Demo data loader
├── requirements.txt
└── manage.py
```

---

## 🖨️ Printing Certificates & Receipts

- **Bonafide Certificate**: Go to Certificates → Issue Bonafide → Print
- **Leaving Certificate**: Go to Certificates → Issue Leaving Cert → Print
- **Fee Receipt**: Go to Finance → Collect Fee → View Receipt → Print
- **Result Marksheet**: Go to Results → Result Report → Generate → Print
- **Attendance Report**: Go to Attendance → Report → Generate → Print (Ctrl+P)

All print pages hide the sidebar/header automatically using CSS `@media print`.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, Django 4.2
- **Database**: SQLite (no extra setup required)
- **Frontend**: Bootstrap 5.3, Bootstrap Icons, Chart.js
- **Fonts**: Inter + Plus Jakarta Sans (Google Fonts)

---

## 📞 Support

Run into issues? Check:
1. All migrations applied: `python manage.py migrate`
2. Setup script run: `python setup_demo.py`
3. Server running: `python manage.py runserver`
