from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from flask_mail import Message
from models import Project, ContactMessage, SiteSettings
from forms import ContactForm, ProjectForm, LoginForm, SettingsForm
from app import db, mail
import logging
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail as SendGridMail

main_bp = Blueprint('main', __name__)

def check_admin_auth():
    """Check if user is authenticated as admin"""
    return session.get('admin_logged_in', False)

def require_admin_auth(f):
    """Decorator to require admin authentication"""
    def wrapper(*args, **kwargs):
        if not check_admin_auth():
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login"""
    if check_admin_auth():
        return redirect(url_for('main.admin_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # Simple authentication check
        if form.username.data == 'admin' and form.password.data == 'admin123':
            session['admin_logged_in'] = True
            flash('Successfully logged in!', 'success')
            return redirect(url_for('main.admin_dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('admin/login.html', form=form)

@main_bp.route('/logout')
def logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))

@main_bp.route('/')
def index():
    """Home page with all sections"""
    completed_projects = Project.query.filter_by(is_completed=True).order_by(Project.created_at.desc()).all()
    current_projects = Project.query.filter_by(is_completed=False).order_by(Project.created_at.desc()).all()
    
    contact_form = ContactForm()
    
    return render_template('index.html', 
                         completed_projects=completed_projects,
                         current_projects=current_projects,
                         contact_form=contact_form)

@main_bp.route('/contact', methods=['POST'])
def contact():
    """Handle contact form submission"""
    form = ContactForm()
    
    if form.validate_on_submit():
        # Save message to database
        message = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        db.session.add(message)
        db.session.commit()
        
        # Send email notification using Gmail SMTP
        email_sent = False
        try:
            # Try Gmail SMTP first (simpler setup)
            gmail_user = os.environ.get('GMAIL_USER', 'omkartanajipatilofficial@gmail.com')
            gmail_password = os.environ.get('GMAIL_APP_PASSWORD')
            
            if gmail_password:
                # Use Gmail SMTP
                import smtplib
                from email.mime.text import MIMEText
                from email.mime.multipart import MIMEMultipart
                
                msg = MIMEMultipart()
                msg['From'] = gmail_user
                msg['To'] = gmail_user
                msg['Subject'] = f'Portfolio Contact: {form.name.data}'
                
                body = f"""
New contact form submission from your portfolio website:

Name: {form.name.data}
Email: {form.email.data}
Message: {form.message.data}

Reply directly to: {form.email.data}
                """
                
                msg.attach(MIMEText(body, 'plain'))
                
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(gmail_user, gmail_password)
                text = msg.as_string()
                server.sendmail(gmail_user, gmail_user, text)
                server.quit()
                
                email_sent = True
                logging.info('Gmail email sent successfully')
            else:
                # Fallback: Just save to database
                logging.info('No email configuration found, message saved to database only')
                
        except Exception as e:
            logging.error(f'Error sending email: {e}')
        
        # Show appropriate message
        if email_sent:
            flash('Thank you for your message! I\'ll get back to you soon.', 'success')
        else:
            flash('Message saved! I\'ll get back to you soon.', 'success')
    else:
        flash('Please correct the errors in the form.', 'error')
    
    return redirect(url_for('main.index') + '#contact')

@main_bp.route('/admin')
@require_admin_auth
def admin_dashboard():
    """Admin dashboard"""
    total_projects = Project.query.count()
    completed_projects = Project.query.filter_by(is_completed=True).count()
    current_projects = Project.query.filter_by(is_completed=False).count()
    unread_messages = ContactMessage.query.filter_by(is_read=False).count()
    
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_projects=total_projects,
                         completed_projects=completed_projects,
                         current_projects=current_projects,
                         unread_messages=unread_messages,
                         recent_messages=recent_messages)

@main_bp.route('/admin/projects')
@require_admin_auth
def admin_projects():
    """Admin projects management"""
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('admin/projects.html', projects=projects)

@main_bp.route('/admin/projects/add', methods=['GET', 'POST'])
@require_admin_auth
def add_project():
    """Add new project"""
    form = ProjectForm()
    
    if form.validate_on_submit():
        project = Project(
            title=form.title.data,
            description=form.description.data,
            tech_stack=form.tech_stack.data,
            github_url=form.github_url.data,
            live_url=form.live_url.data,
            image_url=form.image_url.data,
            is_completed=form.is_completed.data
        )
        db.session.add(project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('main.admin_projects'))
    
    return render_template('admin/add_project.html', form=form)

@main_bp.route('/admin/projects/<int:id>/edit', methods=['GET', 'POST'])
@require_admin_auth
def edit_project(id):
    """Edit existing project"""
    project = Project.query.get_or_404(id)
    form = ProjectForm(obj=project)
    
    if form.validate_on_submit():
        form.populate_obj(project)
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('main.admin_projects'))
    
    return render_template('admin/edit_project.html', form=form, project=project)

@main_bp.route('/admin/projects/<int:id>/delete', methods=['POST'])
@require_admin_auth
def delete_project(id):
    """Delete project"""
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('main.admin_projects'))

@main_bp.route('/admin/messages/<int:id>/toggle-read', methods=['POST'])
@require_admin_auth
def toggle_message_read(id):
    """Toggle message read/unread status"""
    message = ContactMessage.query.get_or_404(id)
    message.is_read = not message.is_read
    db.session.commit()
    
    status = 'read' if message.is_read else 'unread'
    return jsonify({
        'status': 'success',
        'is_read': message.is_read,
        'new_status': status
    })

@main_bp.route('/admin/settings', methods=['GET', 'POST'])
@require_admin_auth
def admin_settings():
    """Admin settings management"""
    form = SettingsForm()
    
    if form.validate_on_submit():
        # Update each setting
        settings_data = {
            'site_name': form.site_name.data,
            'site_title': form.site_title.data,
            'about_intro': form.about_intro.data,
            'about_description': form.about_description.data,
            'technical_skills': form.technical_skills.data,
            'contact_email': form.contact_email.data,
            'contact_phone': form.contact_phone.data,
            'social_github': form.social_github.data,
            'social_linkedin': form.social_linkedin.data,
            'social_twitter': form.social_twitter.data,
            'social_email': form.social_email.data
        }
        
        for setting_name, setting_value in settings_data.items():
            setting = SiteSettings.query.filter_by(setting_name=setting_name).first()
            if setting:
                setting.setting_value = setting_value or ''
            else:
                setting = SiteSettings(setting_name=setting_name, setting_value=setting_value or '')
                db.session.add(setting)
        
        db.session.commit()
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('main.admin_settings'))
    
    # Load current settings
    settings = {}
    for field_name in ['site_name', 'site_title', 'about_intro', 'about_description', 
                       'technical_skills', 'contact_email', 'contact_phone',
                       'social_github', 'social_linkedin', 'social_twitter', 'social_email']:
        setting = SiteSettings.query.filter_by(setting_name=field_name).first()
        if setting:
            settings[field_name] = setting.setting_value
            # Pre-populate form
            if hasattr(form, field_name):
                getattr(form, field_name).data = setting.setting_value
    
    return render_template('admin/settings.html', form=form, settings=settings)

@main_bp.route('/admin/messages')
@require_admin_auth
def admin_messages():
    """Admin messages management"""
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', messages=messages)
