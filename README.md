# 🚗 CarCraft — Automotive Inventory & Dealership Suite

CarCraft is a full-stack **Django-based automotive dealership management platform** designed to manage vehicle inventory, customer services, automotive parts/accessories, and service appointments through a single web application.

## 🌐 Live Demo

**Live Website:** https://carcraft-lh5k.onrender.com

**Admin Panel:** https://carcraft-lh5k.onrender.com/admin/

---

## 📌 Project Overview

CarCraft provides a centralized platform for an automobile dealership to manage its day-to-day operations.

The system allows users to explore available vehicles, view vehicle details, purchase automotive parts/accessories, and schedule service appointments.

Administrators can manage vehicles, users, service bookings, and other dealership-related information through the Django administration panel.

---

## ✨ Features

### 🚘 Vehicle Inventory

* Browse available vehicles
* View detailed vehicle information
* Vehicle images
* Vehicle specifications
* Vehicle color
* Kilometers driven
* Registration number
* Seller information
* Vehicle inventory management

### 🛒 Parts & Accessories

* Browse automotive parts and accessories
* Product information and pricing
* E-commerce functionality

### 🔧 Service Booking

* Schedule vehicle service appointments
* Manage service bookings
* Store customer and vehicle service information

### 👤 User Management

* User registration and authentication
* Secure login system
* Django-based admin authentication
* Staff and superuser management

### 🛠️ Admin Dashboard

Administrators can manage:

* Vehicles
* Users
* Service bookings
* Inventory information
* Other application data

---

## 🧑‍💻 Technologies Used

| Technology   | Purpose                |
| ------------ | ---------------------- |
| Python       | Backend programming    |
| Django       | Web framework          |
| HTML5        | Website structure      |
| CSS3         | Styling                |
| JavaScript   | Frontend functionality |
| SQLite       | Database               |
| Pillow       | Image processing       |
| Gunicorn     | Production server      |
| WhiteNoise   | Static file serving    |
| Git & GitHub | Version control        |
| Render       | Cloud deployment       |

---

## 📂 Project Structure

```text
CarCraft/
│
├── carcraft/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
│
├── vehicles/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── media/
│   └── vehicles/
│
├── static/
│
├── manage.py
├── requirements.txt
├── build.sh
├── render.yaml
├── .gitignore
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Krishna24b0311146/CarCraft.git
```

### 2. Navigate to the Project

```bash
cd CarCraft
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Apply Migrations

```bash
python manage.py migrate
```

### 7. Create an Admin User

```bash
python manage.py createsuperuser
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

---

## 🔐 Django Admin

After creating a superuser, access the Django administration panel at:

```text
/admin/
```

Example:

```text
http://127.0.0.1:8000/admin/
```

---

## 🚀 Deployment

CarCraft is deployed using **Render**.

Production configuration includes:

* Gunicorn as the WSGI server
* WhiteNoise for static files
* Django migrations during deployment
* Static file collection using `collectstatic`
* Environment variables for production configuration

### Production Start Command

```bash
gunicorn carcraft.wsgi:application
```

### Build Command

```bash
bash build.sh
```

---

## 🗄️ Database

The project uses **SQLite** for database management.

For local development, the database is stored as:

```text
db.sqlite3
```

Sensitive and environment-specific files are excluded using `.gitignore`.

---

## 🔒 Security

The project uses environment variables for sensitive production configuration such as:

* `SECRET_KEY`
* `DEBUG`
* `ALLOWED_HOSTS`
* `CSRF_TRUSTED_ORIGINS`

Sensitive credentials should never be committed to GitHub.

---

## 📸 Screenshots

Screenshots of the following pages can be added here:

* Home Page
* Vehicle Listing
* Vehicle Details
* Parts & Accessories
* Service Booking
* Login/Register
* Admin Dashboard

Example:

```markdown
![Home Page](screenshots/home.png)
```

---

## 🔮 Future Enhancements

Some possible future improvements include:

* Online payment integration
* Advanced vehicle search and filtering
* Customer reviews and ratings
* Email/SMS notifications
* Dealer analytics dashboard
* Real-time service appointment notifications
* PostgreSQL database for production
* Cloud-based image storage
* Improved mobile responsiveness

---

## 🎯 Project Objectives

The main objectives of CarCraft are:

1. To digitize automobile dealership operations.
2. To simplify vehicle inventory management.
3. To provide an online platform for automotive products.
4. To enable convenient service appointment scheduling.
5. To provide administrators with centralized management tools.
6. To create a scalable web-based dealership management system.

---

## 👨‍💻 Developer

**Krishna Gupta**

GitHub:
https://github.com/Krishna24b0311146

---

## 📄 License

This project is developed for **educational and project demonstration purposes**.

---

⭐ If you find this project useful, consider giving the repository a star!

