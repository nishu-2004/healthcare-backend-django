# 🏥 Healthcare Backend API (Django REST Framework)

A production-style healthcare backend built using **Django REST Framework** with **JWT authentication**, supporting patient and doctor management, appointment scheduling, role-based access, and real-world business rules.

---

## 🚀 Features

* 🔐 JWT Authentication (Login & Refresh)
* 👤 Patient CRUD APIs
* 🧑‍⚕️ Doctor CRUD APIs
* 🔗 Doctor–Patient Assignment Mapping
* 📅 Appointment Scheduling System
* ❌ Appointment Conflict Prevention (No double booking)
* 🔎 Appointment Filtering (by doctor, patient, status)
* 🛂 Role-based Appointment Viewing
* 🧱 Clean modular Django app structure

---

## 🛠 Tech Stack

* **Backend:** Django, Django REST Framework
* **Authentication:** JWT (SimpleJWT)
* **Database:** SQLite (development)
* **API Testing:** Postman
* **Version Control:** Git & GitHub

---

## 📁 Project Structure

```
healthcare-backend-django/
│
├── accounts/        # User registration & auth
├── patients/        # Patient management
├── doctors/         # Doctor management
├── mappings/        # Doctor–Patient mapping
├── appointments/    # Appointment scheduling
│
├── healthcare/      # Project settings & URLs
├── manage.py
└── requirements.txt
```

---

## 🔐 Authentication Flow (JWT)

1. Obtain token:

```
POST /api/token/
```

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

2. Use token in headers for all protected APIs:

```
Authorization: Bearer <access_token>
```

---

## 👤 Patient APIs

```
GET    /api/patients/
POST   /api/patients/
GET    /api/patients/{id}/
PATCH  /api/patients/{id}/
DELETE /api/patients/{id}/
```

---

## 🧑‍⚕️ Doctor APIs

```
GET    /api/doctors/
POST   /api/doctors/
GET    /api/doctors/{id}/
PATCH  /api/doctors/{id}/
DELETE /api/doctors/{id}/
```

---

## 🔗 Doctor–Patient Mapping

Assign doctors to patients using a mapping table.

```
POST /api/mappings/
```

```json
{
  "doctor": 1,
  "patient": 1,
  "reason_for_assignment": "",
  "is_active": true
}
```

---

## 📅 Appointment APIs

### Create Appointment

```
POST /api/appointments/
```

```json
{
  "doctor": 1,
  "patient": 1,
  "appointment_datetime": "2025-12-20T10:30:00Z",
  "reason": "Routine follow-up"
}
```

### Get Appointments

```
GET /api/appointments/
```

### Update Appointment (PATCH)

```
PATCH /api/appointments/{id}/
```

```json
{
  "status": "CANCELLED"
}
```

---

## ❌ Appointment Conflict Prevention

* A doctor **cannot have two appointments at the same time**
* If attempted, API returns:

```json
{
  "non_field_errors": [
    "Doctor already has an appointment at this time."
  ]
}
```

---

## 🔎 Appointment Filtering

```
GET /api/appointments/?doctor=1
GET /api/appointments/?patient=1
GET /api/appointments/?status=SCHEDULED
```

---

## 🛂 Role-Based Access

* Only authenticated users can access APIs
* Appointment viewing is restricted based on user role
* Permissions are enforced at the API level

---

## ▶️ Running the Project Locally

1. Clone the repository

```bash
git clone <github_repo_url>
cd healthcare-backend-django
```

2. Create & activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run migrations

```bash
python manage.py migrate
```

5. Start the server

```bash
python manage.py runserver
```

Server will run at:

```
http://127.0.0.1:8000/
```

---

## 🧠 Design Highlights

* Modular app-based Django architecture
* Serializer-level validation for business rules
* Clean separation of concerns (models, serializers, views)
* Real-world healthcare workflow modeling

---

## 📌 Future Improvements (Optional)

* Appointment time-slot management
* Email/SMS notifications
* Deployment (Docker / Cloud)
* Swagger/OpenAPI documentation

---

## 👨‍💻 Author

Built by **Nishanth P Kashyap**
