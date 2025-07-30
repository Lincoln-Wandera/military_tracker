# Military Personnel Tracker

A secure, role-based Django web application for tracking soldiers, managing missions, and facilitating communication with family members.

##  Features

###  Authentication & Roles
- Custom user model with roles: `admin`, `family`
- Login, logout, registration, password change and reset
- Role-based dashboard access

### Admin
- CRUD operations for soldier profiles
- Assign soldiers to missions and units
- Track status changes with full history logs
- Emergency contacts management (with primary contact logic)

### Family Members
- Link to soldiers via a secure request system
- View connected soldiers' status and mission history
- Unlink from soldiers with confirmation
- Access to a clean family dashboard and notifications

### Missions & Units
- Admins can create, update, assign soldiers to missions
- Track mission status (active, completed, cancelled)
- Unit organization and filtering

### Email Notifications
- Password reset and account management via **SendGrid**
- Uses `.env` for secure credentials via `python-decouple`

## 🛠 Tech Stack
Django - Core backend framework 
PostgreSQL - Production-grade database 
Bootstrap & Crispy Forms - UI styling 
SendGrid - Transactional emails 
Render - Live deployment 

##  Live Demo
 [View the Live Site](https://military-tracker.onrender.com/)
