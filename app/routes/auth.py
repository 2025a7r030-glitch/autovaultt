from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from app.models import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    """Decorator to protect routes requiring authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            session.clear()
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Retrieve the currently authenticated user from database, or None."""
    if 'user_id' in session:
        return db.session.get(User, session['user_id'])
    return None

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration with validation and password hashing."""
    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        username = request.form.get('username', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Basic validations
        if not name or not email or not username or not password or not confirm_password:
            flash('All fields are required.', 'danger')
            return render_template('register.html', name=name, email=email, username=username)

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('register.html', name=name, email=email, username=username)

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html', name=name, email=email, username=username)

        # Check uniqueness
        if User.query.filter_by(email=email).first():
            flash('An account with this email address already exists.', 'danger')
            return render_template('register.html', name=name, username=username)

        if User.query.filter_by(username=username).first():
            flash('This username is already taken. Please choose another.', 'danger')
            return render_template('register.html', name=name, email=email)

        # Create new user with hashed password
        new_user = User(name=name, email=email, username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in with your credentials.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login with secure generic error messages."""
    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip().lower()
        password = request.form.get('password', '')

        if not identifier or not password:
            flash('Please provide both username/email and password.', 'danger')
            return render_template('login.html', identifier=identifier)

        # Query by username or email
        user = User.query.filter(
            (User.email == identifier) | (User.username == identifier)
        ).first()

        # Secure verification: generic error message to prevent account enumeration
        if user and user.check_password(password):
            session.clear()
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Welcome back, {user.name}!', 'success')

            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid username/email or password.', 'danger')
            return render_template('login.html', identifier=identifier)

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    """Securely log out by destroying session data."""
    session.clear()
    flash('You have been securely logged out.', 'info')
    return redirect(url_for('auth.login'))
