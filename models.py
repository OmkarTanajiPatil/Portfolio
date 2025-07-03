from app import db
from datetime import datetime
from sqlalchemy import Text

class SiteSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    setting_name = db.Column(db.String(100), unique=True, nullable=False)
    setting_value = db.Column(Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(Text, nullable=False)
    tech_stack = db.Column(db.String(500), nullable=False)
    github_url = db.Column(db.String(500))
    live_url = db.Column(db.String(500))
    image_url = db.Column(db.String(500))
    is_completed = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Project {self.title}>'

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<ContactMessage from {self.name}>'

def create_sample_data():
    """Create sample projects for demonstration"""
    completed_projects = [
        {
            'title': 'E-Commerce Analytics Dashboard',
            'description': 'A comprehensive analytics dashboard for e-commerce platforms with real-time data visualization, sales tracking, and customer behavior analysis.',
            'tech_stack': 'Python, Flask, PostgreSQL, Chart.js, Bootstrap',
            'github_url': 'https://github.com/username/ecommerce-dashboard',
            'live_url': 'https://demo-dashboard.herokuapp.com',
            'is_completed': True
        },
        {
            'title': 'Machine Learning Model Deployment',
            'description': 'RESTful API for deploying ML models with automatic scaling, model versioning, and performance monitoring.',
            'tech_stack': 'Python, FastAPI, Docker, AWS, TensorFlow',
            'github_url': 'https://github.com/username/ml-deployment',
            'live_url': 'https://ml-api.example.com',
            'is_completed': True
        },
        {
            'title': 'Data Visualization Library',
            'description': 'Open-source Python library for creating interactive data visualizations with minimal code.',
            'tech_stack': 'Python, Plotly, Pandas, NumPy',
            'github_url': 'https://github.com/username/dataviz-lib',
            'is_completed': True
        }
    ]
    
    current_projects = [
        {
            'title': 'AI-Powered Content Generator',
            'description': 'Building an AI application that generates high-quality content for blogs, social media, and marketing materials.',
            'tech_stack': 'Python, OpenAI API, React, MongoDB',
            'github_url': 'https://github.com/username/ai-content-gen',
            'is_completed': False
        },
        {
            'title': 'Real-time Chat Application',
            'description': 'Developing a scalable real-time chat application with WebSocket support, file sharing, and group messaging.',
            'tech_stack': 'Python, Socket.IO, Redis, PostgreSQL',
            'github_url': 'https://github.com/username/realtime-chat',
            'is_completed': False
        }
    ]
    
    all_projects = completed_projects + current_projects
    
    for project_data in all_projects:
        project = Project(**project_data)
        db.session.add(project)
    
    db.session.commit()

def create_default_settings():
    """Create default site settings"""
    from app import db
    
    default_settings = {
        'site_name': 'Omkar Tanaji Patil',
        'site_title': 'Python & ML Developer',
        'about_intro': 'Hello! I\'m a passionate Python developer with a love for machine learning and data science.',
        'about_description': 'I specialize in building intelligent applications that solve real-world problems using cutting-edge technology. With expertise in Python, machine learning, and web development, I create scalable solutions that make a difference.',
        'technical_skills': 'Python,Machine Learning,Data Science,Flask,Django,TensorFlow,PyTorch,Pandas,NumPy,Scikit-learn,SQL,PostgreSQL,Git,AWS,Docker',
        'contact_email': 'omkartanajipatilofficial@gmail.com',
        'contact_phone': '+1 (555) 123-4567',
        'social_github': 'https://github.com/yourusername',
        'social_linkedin': 'https://linkedin.com/in/yourusername',
        'social_twitter': 'https://twitter.com/yourusername',
        'social_email': 'mailto:omkartanajipatilofficial@gmail.com'
    }
    
    for setting_name, setting_value in default_settings.items():
        existing_setting = SiteSettings.query.filter_by(setting_name=setting_name).first()
        if not existing_setting:
            setting = SiteSettings(setting_name=setting_name, setting_value=setting_value)
            db.session.add(setting)
    
    db.session.commit()
