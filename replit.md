# Professional Portfolio Website

## Overview

This is a modern, responsive portfolio website built with Flask for Python/ML developers. The application features a dark theme, project showcase, contact form, and a complete admin panel for content management. It's designed to be professional, SEO-optimized, and mobile-responsive.

## System Architecture

### Backend Architecture
- **Flask Application**: Python web framework serving as the main backend
- **SQLAlchemy ORM**: Database abstraction layer with declarative models
- **SQLite Database**: Default database (easily switchable to PostgreSQL)
- **Flask-WTF**: Form handling with CSRF protection
- **Flask-Mail**: Email functionality for contact forms

### Frontend Architecture
- **Bootstrap 5**: Responsive CSS framework
- **Vanilla JavaScript**: Custom interactions and animations
- **Font Awesome**: Icon library
- **Google Fonts**: Inter font family for typography
- **Dark Theme**: Professional color scheme with CSS variables

### Application Structure
- **Single Page Application**: Main content on index page with smooth scrolling
- **Admin Panel**: Separate admin interface for content management
- **Responsive Design**: Mobile-first approach with Bootstrap grid system

## Key Components

### Models (models.py)
1. **Project Model**: Stores project information with fields for title, description, tech stack, URLs, and completion status
2. **ContactMessage Model**: Handles contact form submissions with read status tracking
3. **Sample Data Generator**: Creates demonstration projects for new installations

### Forms (forms.py)
1. **ContactForm**: Handles visitor contact submissions with validation
2. **ProjectForm**: Admin form for creating/editing projects with URL validation

### Routes (routes.py)
1. **Main Routes**: Home page, contact handling
2. **Admin Routes**: Dashboard, project management (CRUD operations)
3. **API Endpoints**: RESTful operations for project management

### Templates
1. **Base Template**: Common layout with navigation and footer
2. **Index Template**: Main portfolio page with hero, about, projects, and contact sections
3. **Admin Templates**: Dashboard, project management, and form pages

## Data Flow

1. **Public View**: Users browse the portfolio, view projects, and submit contact forms
2. **Contact Handling**: Form submissions are stored in database and optionally emailed
3. **Admin Management**: Authenticated users can manage projects through admin panel
4. **Database Operations**: SQLAlchemy handles all database interactions with automatic migrations

## External Dependencies

### Python Packages
- Flask (web framework)
- Flask-SQLAlchemy (database ORM)
- Flask-WTF (form handling)
- Flask-Mail (email functionality)
- WTForms (form validation)

### Frontend CDN Resources
- Bootstrap 5 CSS/JS
- Font Awesome icons
- Google Fonts (Inter)

### Email Service
- SendGrid integration for reliable email delivery
- Contact form saves messages to database and sends email notifications
- Fallback SMTP configuration available
- Environment variable based configuration

## Deployment Strategy

### Environment Configuration
- Database URL configurable via environment variables
- Email settings through environment variables
- Secret key management for security
- Debug mode controlled by environment

### Production Considerations
- SQLite for development, PostgreSQL recommended for production
- ProxyFix middleware for reverse proxy deployments
- Connection pooling and database optimization
- CSRF protection enabled
- Logging configuration for monitoring

### Deployment Options
- Can be deployed to Heroku, Railway, or any Python hosting platform
- Docker-ready with proper configuration
- Static files served through Flask (CDN recommended for production)

## Changelog
- July 03, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.