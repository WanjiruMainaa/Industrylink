# IndustryLink 🎓

![Django](https://img.shields.io/badge/Django-5.2.8-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

**Bridging the Gap Between Academia and Industry**

IndustryLink is a comprehensive platform connecting students with real-world opportunities, professional mentorship, and skill development resources. Built for SDG 4: Quality Education.

---

## Problem Statement

The gap between academic learning and industry requirements creates challenges for graduates:
- Students lack practical industry experience despite theoretical knowledge
- Difficulty finding mentors and guidance from experienced professionals
- Limited platforms to showcase student projects to potential employers
- Unclear understanding of skill gaps for target career roles

## Solution

IndustryLink provides an integrated platform offering:

### For Students
- **Project Portfolio**: Showcase academic and personal projects
- **Mentorship Access**: Connect with industry professionals
- **Skill Gap Analysis**: Identify missing skills for target roles
- **Learning Resources**: Get personalized recommendations

### For Mentors & Professionals
- **Knowledge Sharing**: Guide the next generation
- **Talent Discovery**: Find skilled students for opportunities
- **Professional Branding**: Build your mentoring reputation

### For Organizations
- **Talent Pool**: Discover students based on skills and projects
- **Project Opportunities**: Post real-world projects for students
- **CSR Initiatives**: Support education through mentorship

---

## Key Features

### 1. Multi-User Registration
- **Students**: Academic profile with projects and skills
- **Mentors**: Professional profile with expertise areas
- **Freelancers**: Showcase specializations
- **Organizations**: Post opportunities and find talent

### 2. Campus-to-Career Portal
- Project showcase with GitHub integration
- Filter by technology stack and status
- Direct contact with project creators

### 3. Mentorship Marketplace
- Browse mentors by expertise
- View availability and rates
- M-Pesa payment integration

### 4. Skill Gap Analyzer
- Input current skills
- Select target role
- Get personalized learning paths
- Progress tracking


## Tech Stack

### Backend
- **Framework**: Django 5.2.8
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **Authentication**: Django Auth System
- **Payment**: M-Pesa Daraja API

### Frontend
- **Framework**: Bootstrap 5.3
- **Icons**: Bootstrap Icons
- **JavaScript**: Vanilla JS

### Deployment
- **Version Control**: Git & GitHub
- **Environment**: Python Virtual Environment

---

## Installation & Setup

### Prerequisites
```bash
Python 3.8 or higher
Git
```

### 1. Clone Repository
```bash
git clone https://github.com/WanjiruMainaa/Industrylink
cd industrylink
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv env
env\Scripts\activate

# macOS/Linux
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create `.env` file in project root:
```env
SECRET_KEY=your_secret_key_here
DEBUG=True
MPESA_CONSUMER_KEY=your_mpesa_key
MPESA_CONSUMER_SECRET=your_mpesa_secret
MPESA_PASSKEY=your_passkey
```

### 5. Run Migrations
```bash
cd core
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

### 8. Access Application
- **Main Site**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Admin Dashboard**: http://127.0.0.1:8000/admin-dashboard/

---

##Usage Guide

### For Students

1. **Register**: Choose "Student" and fill in academic details
2. **Complete Profile**: Add bio, skills, and contact info
3. **Add Projects**: Showcase your work with descriptions and links
4. **Find Mentors**: Browse by expertise and availability
5. **Analyze Skills**: Use Skill Gap Analyzer for career guidance

### For Mentors

1. **Register**: Choose "Mentor" and add professional details
2. **Set Availability**: Indicate your mentoring availability
3. **Review Projects**: Help students by reviewing their work
4. **Connect**: Engage with students seeking guidance

### For Organizations

1. **Register**: Choose "Organization" type
2. **Browse Talent**: Filter students by skills and projects
3. **Post Opportunities**: Share internship/project opportunities
4. **Connect**: Reach out to potential candidates

## M-Pesa Integration

### Setup Instructions

1. Register at [Safaricom Daraja](https://developer.safaricom.co.ke/)
2. Create a sandbox app
3. Copy credentials to `.env` file
4. Test with sandbox phone number

### Payment Features
- Mentor session payments
- Student tip functionality
- Platform donations
- Real-time STK push notifications

---

##Project Structure
```
industrylink/
├── core/
│   ├── core/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── main/
│   │   ├── migrations/
│   │   ├── static/
│   │   │   └── main/
│   │   │       └── images/
│   │   ├── templates/
│   │   │   └── main/
│   │   │       ├── base.html
│   │   │       ├── home.html
│   │   │       ├── dashboard.html
│   │   │       ├── projects.html
│   │   │       ├── mentors.html
│   │   │       └── ...
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   └── admin.py
│   ├── manage.py
│   └── db.sqlite3
├── env/
├── screenshots/
├── README.md
├── requirements.txt
└── .gitignore
```

##Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

Wanjiru Maina
- GitHub: [@WanjruMainaa](https://github.com/WanjiruMainaa)
- Email:  mainawanjiru.mymail@gmail.com

---

## Acknowledgments

- **SDG 4**: Quality Education
- **Safaricom**: Daraja API for payment integration
- **Bootstrap**: UI framework
- **Django Community**: For excellent documentation


---

For support:
- Email: mainawanjiru.mymail@gmail.com
- Issues: [GitHub Issues](https://github.com/WanjiruMainaa/industrylink/issues)

---


**For SDG 4: Quality Education | Bridging Academia and Industry**