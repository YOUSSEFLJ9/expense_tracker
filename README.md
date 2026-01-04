# Expense Tracker - Django Web Application

A comprehensive Django web application designed for individual users to manage their personal finances and track expenses.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Django](https://img.shields.io/badge/Django-5.0-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Features

### ✅ User Authentication
- User registration with email
- Secure login/logout functionality
- Each user has isolated data (can only view/manage their own expenses)

### 💰 Expense Management
- **Add** new expenses with amount, category, description, and date
- **Edit** existing expenses
- **Delete** unwanted expenses
- **List** all expenses with filtering options

### 🏷️ Category Management
- **Predefined categories**: Food, Transport, Rent, Entertainment, Health, Shopping, Utilities, Education, Other
- **Custom categories**: Users can create their own categories
- Ability to delete custom categories

### 📊 Monthly Reports
- Filter expenses by month and year
- View total spending per month
- Category-wise breakdown with percentages
- **CSV Export**: Download monthly reports as CSV files

### 📈 Data Visualization (Chart.js)
- **Pie Chart**: Visual breakdown of expenses by category
- **Bar Chart**: Daily expenses for the last 7 days
- Interactive and responsive charts

### 🎯 Dashboard
- Quick overview of monthly and total expenses
- Recent expenses list
- Visual charts and statistics
- Quick action buttons

## 🛠️ Technical Stack

- **Backend**: Django 5.0.1
- **Database**: SQLite (for development)
- **Frontend**: Django Templates + Bootstrap 5
- **Charts**: Chart.js 4.4.0
- **Icons**: Font Awesome 6.4.0

## 📁 Project Structure

```
project/
├── manage.py
├── requirements.txt
├── db.sqlite3 (created after migrations)
├── expense_tracker/          # Main project configuration
│   ├── __init__.py
│   ├── settings.py          # Project settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── expenses/                 # Main application
│   ├── __init__.py
│   ├── models.py            # Category & Expense models
│   ├── views.py             # All view logic
│   ├── forms.py             # Django forms
│   ├── urls.py              # App URL patterns
│   ├── admin.py             # Admin interface configuration
│   ├── apps.py
│   └── management/          # Custom management commands
│       └── commands/
│           └── create_categories.py
└── templates/               # HTML templates
    ├── base.html           # Base template with Bootstrap
    └── expenses/
        ├── login.html
        ├── register.html
        ├── dashboard.html
        ├── expense_list.html
        ├── expense_form.html
        ├── expense_confirm_delete.html
        ├── category_list.html
        ├── category_form.html
        ├── category_confirm_delete.html
        └── monthly_report.html
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step-by-Step Setup

1. **Clone or navigate to the project directory**
   ```bash
   cd /root/ymomen/project
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create predefined categories**
   ```bash
   python manage.py create_categories
   ```

6. **Create a superuser (for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main app: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📖 Usage Guide

### Getting Started

1. **Register a new account**
   - Navigate to the registration page
   - Fill in username, email, and password
   - You'll be automatically logged in after registration

2. **Add your first expense**
   - Click "Add Expense" button
   - Enter amount, select category, choose date
   - Optionally add a description
   - Click "Save Expense"

3. **View your dashboard**
   - See monthly and total spending summaries
   - View charts showing expense breakdown
   - Check recent expenses

4. **Manage categories**
   - View all predefined categories
   - Create custom categories for your needs
   - Delete custom categories if not needed

5. **Generate reports**
   - Go to "Reports" section
   - Select month and year
   - View detailed breakdown
   - Export to CSV for external use

### Key Features Explained

#### Expense Filtering
- Filter by category to see specific types of expenses
- Filter by month and year to analyze spending patterns
- View total amounts for filtered results

#### Monthly Reports
- Comprehensive breakdown by category
- Shows count and percentage for each category
- Detailed list of all expenses in the month
- One-click CSV export

#### Data Security
- Each user can only see their own data
- Secure authentication required
- Database-level isolation ensures privacy

## 🎨 UI Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Bootstrap 5**: Modern and clean interface
- **Font Awesome Icons**: Visual clarity and appeal
- **Color-coded Cards**: Easy identification of different metrics
- **Interactive Charts**: Hover for detailed information
- **Alert Messages**: User feedback for all actions

## 🔧 Django Best Practices Implemented

### Models
- Proper field types with validation
- Database indexes for performance
- Relationships with appropriate `on_delete` behavior
- Model methods and properties for reusability

### Views
- Function-based views (FBVs) for clarity
- `@login_required` decorator for security
- Proper user filtering to ensure data isolation
- Django ORM aggregation (Sum, Count, Annotate)

### Forms
- Django ModelForms for DRY principle
- Custom widgets for better UX
- Form validation
- Dynamic form field queries based on user

### Templates
- Template inheritance with `base.html`
- Context processors for global data
- Template filters for formatting
- DRY principle with reusable components

### Security
- CSRF protection enabled
- User-specific queries prevent data leaks
- Password validation
- SQL injection protection via ORM

## 📊 Database Schema

### Category Model
- `name`: CharField (max 100 characters)
- `user`: ForeignKey to User (nullable for predefined)
- `is_predefined`: BooleanField
- `created_at`: DateTimeField (auto)
- Unique together constraint on (name, user)

### Expense Model
- `user`: ForeignKey to User
- `amount`: DecimalField (10 digits, 2 decimal places)
- `category`: ForeignKey to Category (nullable, SET_NULL on delete)
- `description`: TextField (max 500 characters, optional)
- `date`: DateField
- `created_at`, `updated_at`: DateTimeField (auto)
- Indexes on (user, date) and (user, category)

## 🔮 Future Enhancements (Optional)

- Budget setting and alerts
- Recurring expenses
- Income tracking
- Multi-currency support
- Mobile app version
- Email notifications
- Advanced analytics and trends
- Data import from CSV
- Expense categories with subcategories
- Tags for expenses
- Search functionality
- Pagination for large datasets

## 🐛 Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'django'`
- **Solution**: Make sure you've activated your virtual environment and installed requirements

**Issue**: Database errors
- **Solution**: Run `python manage.py migrate` to ensure all migrations are applied

**Issue**: No categories showing
- **Solution**: Run `python manage.py create_categories` to create predefined categories

**Issue**: Static files not loading
- **Solution**: Make sure `DEBUG = True` in settings.py for development

## 📝 License

This project is open-source and available under the MIT License.

## 👨‍💻 Development

### Running Tests
```bash
python manage.py test
```

### Creating Additional Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting Static Files (for production)
```bash
python manage.py collectstatic
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues, questions, or suggestions, please open an issue in the repository.

---

**Built with ❤️ using Django**
