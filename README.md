# SecureVote - Online Voting System 🗳️

SecureVote is a secure, fair, and visually stunning web-based **Online Voting System** application built using **Python and Django**. Designed as an academic portfolio project, it demonstrates backend engineering best practices, relational database design, secure session authentication, and modern glassmorphic styling.

---

## ✨ Features

- **🔒 Double-Voting Prevention**: Implements a strict database-level unique constraint (`unique_together = ('user', 'election')`) ensuring a voter can cast exactly one ballot per election. Any attempt to double-vote is blocked at both the application view layer and the database layer.
- **🛡️ Secure Authentication**: Leverages Django's built-in session authentication and encryption standards. User passwords are encrypted using salted PBKDF2 hashing.
- **📊 Real-time Result Charts**: Interactive results screen with fluid gradient progress bars displaying candidate vote shares and tallies instantly.
- **👑 Automatic Winner Declaration**: Automatically calculates and highlights the declared winner with a crown badge once an election's closing date has passed.
- **💻 Admin Stats Panel**: A custom analytical panel for administrators to supervise election parameters, count overall voter turnout, and track leaders.
- **🎨 Premium Dark UI**: Glassmorphic interfaces designed using CSS grid, backdrop filters, responsive designs, and custom interactive hover scales.
- **👁️ Password Visibility Toggles**: Custom show/hide eye icons embedded in both login and registration inputs for improved user experience.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.14+, Django 6.0+
- **Database**: SQLite (Fully compliant with MySQL/PostgreSQL via Django ORM)
- **Frontend**: HTML5, Vanilla CSS3, Javascript
- **Testing**: Django Test Client assertions

---

## 📂 Codebase Structure

- `voting/models.py`: Database tables (`Election`, `Candidate`, `Vote`) and status calculation helper methods.
- `voting/views.py`: Route controller logic, authorization decorator checks, and statistical data aggregation.
- `voting/forms.py`: Registration forms inheriting from Django `UserCreationForm` with email uniqueness verification.
- `voting/static/css/style.css`: Primary styling system for glassmorphism, glowing accents, and responsive layout grids.
- `voting/templates/voting/`: HTML structures for dashboards, voter ballots, results, and authentication panels.
- `seed_data.py`: Administrative seeding script to populate users, candidates, and sample votes.

---

## 🚀 Local Installation & Running Guide

Ensure you have **Python 3** and **Git** installed, then execute these commands in your terminal:

### 1. Clone & Setup Directory
```bash
git clone <your-repository-url>
cd online-voting
```

### 2. Create & Activate Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install django
```

### 4. Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Seed Default Data (Elections, Candidates, & Voters)
```bash
python seed_data.py
```

### 6. Run Server
```bash
python manage.py runserver
```
Visit **[http://localhost:8000/](http://localhost:8000/)** in your browser.

---

## 🔑 Seeding Account Credentials

The seeder generates the following test credentials for evaluation:

- **Standard Voter 1**:
  - **Username**: `voter1`
  - **Password**: `voter1secure`
- **Standard Voter 2**:
  - **Username**: `voter2`
  - **Password**: `voter2secure`
- **Superuser (Admin)**:
  - **Username**: `admin`
  - **Password**: `adminsecure123`
  - **Admin Dashboard**: `http://localhost:8000/admin-dashboard/`
  - **Django Administration Console**: `http://localhost:8000/admin/`

---

## 🧑‍💻 Author

- **Avinash Kumar Sah**
- **Noida, Uttar Pradesh**
- **Email**: [avinashdev025@gmail.com](mailto:avinashdev025@gmail.com)
