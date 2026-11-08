# Harley Nemeth Art Gallery

A full-stack Django e-commerce application developed to showcase, manage and sell original artwork through a dedicated online platform.

**Live Website:** [harleynemethart.com](https://harleynemethart.com)  
**GitHub Repository:** [HarleyNemeth/Harley-Nemeth-Art-Gallery](https://github.com/HarleyNemeth/Harley-Nemeth-Art-Gallery)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Application Architecture](#application-architecture)
- [Project Structure](#project-structure)
- [Database Models](#database-models)
- [Deployment](#deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Development Roadmap](#development-roadmap)

---

## Overview

Harley Nemeth Art Gallery is a full-stack web application developed to establish an independent online presence for my artwork and provide the foundations of a small art e-commerce business.

The application combines an artist portfolio, artwork catalogue and shopping cart within a single platform.

The backend is developed using Python and Django, with a custom frontend built using HTML, CSS and JavaScript. The application uses PostgreSQL for production data storage and integrates external image hosting through Cloudinary.

Beyond application development, the project also includes containerisation, cloud infrastructure and automated deployment. The application is hosted on Oracle Cloud using Docker, Nginx and Gunicorn, with HTTPS configured for secure access.

**Project objectives:**
- Develop a real-world, database-backed web application.
- Implement core e-commerce functionality.
- Build a maintainable full-stack application.
- Deploy and maintain the application using cloud infrastructure.
- Automate deployment through GitHub Actions.

## Features

### Artwork Catalogue
- Database-backed artwork listings.
- Individual artwork descriptions, prices and dimensions.
- Artwork categories.
- Featured artwork functionality.
- Stock and availability tracking.
- Externally hosted artwork images.

### Shopping Cart
- Session-based shopping cart.
- Add and remove artwork.
- Quantity and subtotal calculations.
- Stock availability checks.

### Content Management
- Django Admin integration.
- Create and manage artwork records.
- Manage categories and artwork availability.
- Edit homepage biography content.

### Portfolio and Contact
- Artist biography and introduction.
- Featured artwork presentation.
- Dedicated shop and contact pages.
- Contact form with validation.

*Note: Online payment processing and order management are planned but not yet fully implemented.*

## Technology Stack

| Category | Technologies |
|---|---|
| Backend | Python, Django 5.2 |
| Frontend | HTML5, CSS3, JavaScript |
| Database | PostgreSQL, SQLite |
| ORM | Django ORM |
| Database configuration | dj-database-url |
| Application server | Gunicorn |
| Web server | Nginx |
| Static files | WhiteNoise, collectstatic |
| Containerisation | Docker, Docker Compose |
| Cloud hosting | Oracle Cloud Infrastructure |
| Image hosting | Cloudinary |
| Version control | Git, GitHub |
| CI/CD | GitHub Actions |
| Security | SSH, HTTPS, environment variables |

### Key Technical Decisions

**Django:** Handles application routing, backend logic, database operations, forms, sessions and administration.

**PostgreSQL:** Provides persistent relational database storage in production.

**Docker:** Packages the application and its dependencies into a reproducible container.

**Nginx and Gunicorn:** Nginx acts as the reverse proxy, while Gunicorn runs the Django application.

**WhiteNoise:** Handles serving collected static assets.

**Cloudinary:** Stores artwork media externally rather than committing large image files to the repository.

**GitHub Actions:** Automates deployment whenever changes are pushed to the main branch.

## Application Architecture

The application follows a conventional Django architecture, separating request handling, application logic, database models and presentation.

```text
             User / Browser
                    |
                  HTTPS
                    |
                    v
               Nginx Server
                    |
               Reverse Proxy
                    |
                    v
              Gunicorn Server
                    |
                    v
             Django Application
                    |
              +-----+-----+
              |           |
              v           v
           Views       Models
                          |
                          v
                      Django ORM
                          |
                          v
                     PostgreSQL

External services:
- Cloudinary: Artwork media
- SMTP: Contact form emails
```

## Project Structure

```text
Harley-Nemeth-Art-Gallery/
│
├── .github/
│   └── workflows/
│       └── deploy.yml          # Automated deployment workflow
│
├── nemeth_art/
│   ├── settings.py             # Django configuration
│   ├── urls.py                 # Root URL routing
│   ├── asgi.py
│   └── wsgi.py                 # Gunicorn entry point
│
├── static/
│   ├── css/                    # Stylesheets
│   ├── images/                 # Static images
│   └── js/                     # JavaScript
│
├── store/
│   ├── migrations/             # Database migrations
│   ├── templates/              # HTML templates
│   ├── admin.py                # Admin configuration
│   ├── context_processors.py
│   ├── forms.py                # Form validation
│   ├── models.py               # Database models
│   ├── tests.py                # Application tests
│   ├── urls.py                 # Store URL routing
│   └── views.py                # Application logic
│
├── Dockerfile
├── docker-compose.yml
├── manage.py
├── requirements.txt
├── Procfile
└── README.md
```

## Database Models

The application currently uses three principal Django models.

| Model | Purpose |
|---|---|
| Category | Stores artwork categories |
| Artwork | Stores artwork details, pricing, images and availability |
| AboutSection | Stores editable homepage biography content |

Django's ORM manages database interactions, while the Django Admin interface provides a way to manage records without directly modifying the database.

## Deployment

The application is deployed to an Oracle Cloud virtual machine using Docker, Docker Compose, Nginx and Gunicorn.

### Production Infrastructure

- **Oracle Cloud:** Hosts the application.
- **Docker:** Runs the Django application in a container.
- **Docker Compose:** Manages the application container.
- **Nginx:** Handles incoming web traffic and reverse proxying.
- **Gunicorn:** Runs the Django WSGI application.
- **Neon PostgreSQL:** Provides production database storage.
- **Cloudinary:** Hosts artwork media.
- **HTTPS:** Secures communication with the website.

### Useful Server Commands

```bash
# Build and start the application
sudo docker compose up -d --build web

# Check running containers
sudo docker compose ps

# View application logs
sudo docker compose logs -f web

# Restart the application
sudo docker compose restart web
```

## CI/CD Pipeline

GitHub Actions automates deployment to Oracle Cloud whenever changes are pushed to the `main` branch.

The workflow is defined in:

`.github/workflows/deploy.yml`

### Deployment Process

1. GitHub Actions checks out the repository.
2. Required deployment secrets are validated.
3. SSH authentication is configured.
4. A secure connection is established with the Oracle server.
5. The latest changes are fetched from GitHub.
6. The server synchronises with the main branch.
7. Docker rebuilds and restarts the Django application.

### Deployment Workflow

```text
Local Development
       |
       v
   Git Commit
       |
       v
   Git Push
       |
       v
  GitHub Actions
       |
       v
  SSH Connection
       |
       v
   Oracle Cloud
       |
       v
   Docker Build
       |
       v
 Updated Website
```

The current workflow automates deployment. Automated testing, post-deployment health checks and rollback functionality are planned improvements.

## Development Roadmap

### Application Development
- [ ] Complete Stripe payment integration.
- [ ] Implement secure checkout.
- [ ] Introduce persistent order records and order management.
- [ ] Implement payment confirmation and webhook handling.
- [ ] Improve stock management and order processing.
- [ ] Add customer order confirmation emails.
- [ ] Complete custom artwork enquiry functionality.

### Testing and Quality Assurance
- [ ] Expand Django unit and integration tests.
- [ ] Test shopping cart and stock behaviour.
- [ ] Test contact form and email delivery.
- [ ] Test payment and checkout workflows.
- [ ] Add automated Django checks to GitHub Actions.
- [ ] Add post-deployment health checks.
- [ ] Implement deployment rollback procedures.

### Infrastructure and Security
- [x] Docker containerisation.
- [x] Oracle Cloud deployment.
- [x] Nginx reverse proxy.
- [x] HTTPS configuration.
- [x] PostgreSQL integration.
- [x] External artwork media hosting.
- [x] Automated GitHub Actions deployment.
- [ ] Automated database backups and recovery.
- [ ] Dependency vulnerability scanning.
- [ ] Production monitoring and alerting.
- [ ] Review deployment security and permissions.

### Business Readiness
- [ ] Finalise privacy policy.
- [ ] Add terms and conditions.
- [ ] Add shipping, delivery and returns information.
- [ ] Review cookie usage and consent requirements.
- [ ] Complete payment provider configuration.
- [ ] Test the complete customer purchase journey.
- [ ] Complete pre-launch security and functionality review.

---

**Live Website:** [harleynemethart.com](https://harleynemethart.com)  
**Source Code:** [GitHub Repository](https://github.com/HarleyNemeth/Harley-Nemeth-Art-Gallery)
