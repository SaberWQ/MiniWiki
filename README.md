# Mini-Wiki - Personal Notes Management System

A simple and effective web application for creating, organizing, and managing personal notes, built on Django.

## 🚀 Features

- ✅ **User registration and authentication**
- 📝 **Creating, editing, and deleting notes**
- 🔍 **Searching notes** (by title and content)
- 📁 **Organization by categories**
- 🏷️ **Tagging system**
- 💬 **Comments on notes**
- 🔒 **Private and public notes**
- 📊 **View counter**
- 🎨 **Responsive Bootstrap 5 interface**
- 👨‍💼 **Admin panel for management**

## 📋 Requirements

- Python 3.8+
- Django 4.2+
- Pillow (for working with images)

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone <your-repository>
cd mini-wiki
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Activation on Windows
venv\Scripts\activate

# Activation on Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open a browser and navigate to: `http://127.0.0.1:8000/`

## 📁 Project Structure

```
mini-wiki/
│
├── wiki_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── notes/
│   ├── migrations/
│   │   └── __init__.py
│   ├── management/
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── populate_db.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── notes/
│   │   │   ├── home.html
│   │   │   ├── note_detail.html
│   │   │   ├── note_form.html
│   │   │   ├── note_confirm_delete.html
│   │   │   ├── my_notes.html
│   │   │   └── category_notes.html
│   │   └── registration/
│   │       ├── login.html
│   │       └── register.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── static/
├── media/
├── venv/
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

## 🎯 Usage

### For regular users:

1. **Registration**: Create an account on the `/register/` page
2. **Create a note**: Click "Create a note" in navigation
3. **Organization**: Assign categories and tags to your notes
4. **Search**: Use the search form to quickly find notes
5. **Privacy**: Choose which notes to make public

### For administrators:

1. Log in to the admin panel: `http://127.0.0.1:8000/admin/`
2. Manage categories, tags, and users
3. Moderate content and comments

## 🔧 Extensibility

The project is easily expanded with the following features:

- 📎 Attaching files to notes
- 🌐 API for mobile apps
- 📧 Email notifications
- 🔗 Collaborating on notes
- 📤 Export to PDF/Markdown
- 🎨 Markdown editor
- 🔔 Notification system
- ⭐ Featured Notes
- 📌 Pinned Notes

## 📝 Data Models

- **Note**: Main note model
- **Category**: Categories for organizing notes
- **Tag**: Tags for categorization
- **Comment**: Comments on notes
- **User**: Built-in Django user model

## 🤝 Contributing

Pull requests are welcome! For significant changes, please open an issue for discussion first.

## 📄 License

This project is for educational purposes and is freely available.

## 👤 Author

Created as a demo project for learning Django.

## 📞 Support

If you have questions or suggestions, please create an issue in the repository.

# Activation in Windows
venv\Scripts\activate

# Activation on Linux/Mac
source venv/bin/activate
