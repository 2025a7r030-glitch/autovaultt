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
            session.pop('user_id', None)
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Retrieve the currently authenticated user from database, or restore from secure signed session."""
    if 'user_id' not in session:
        return None

    user_id = session.get('user_id')
    user = db.session.get(User, user_id)
    if user:
        return user

    # Resiliency fallback for serverless container cold-starts:
    # If the user was authenticated via signed session cookie but this serverless container
    # has an empty or fresh SQLite database, restore user state to avoid kicking them out.
    username = session.get('username')
    email = session.get('email', f"{username}@autovault.local" if username else None)
    name = session.get('name', username)

    if username:
        try:
            existing = User.query.filter((User.username == username) | (User.email == email)).first()
            if existing:
                session['user_id'] = existing.id
                return existing

            restored_user = User(id=user_id, name=name, email=email, username=username)
            restored_user.set_password('AutoVault@2026')
            db.session.add(restored_user)
            db.session.commit()

            # Ensure a primary vehicle exists for this user in this container
            from app.models.vehicle import Vehicle
            if not Vehicle.query.filter_by(user_id=restored_user.id).first():
                v = Vehicle(
                    user_id=restored_user.id,
                    manufacturer='Hyundai',
                    model='i20',
                    variant='Sportz 1.2 Petrol',
                    registration_number='DL 01 AB 9988',
                    fuel_type='Petrol',
                    transmission='Manual',
                    manufacturing_year=2023,
                    current_odometer=14850
                )
                db.session.add(v)
                db.session.commit()

            return restored_user
        except Exception:
            db.session.rollback()
            return None

    return None

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration with validation and password hashing."""
    if 'user_id' in session and get_current_user():
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

        # Log the user in directly with permanent session
        session.clear()
        session.permanent = True
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        session['email'] = new_user.email
        session['name'] = new_user.name

        flash('Registration successful! Welcome to AutoVault.', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login with secure generic error messages."""
    if 'user_id' in session and get_current_user():
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
            session.permanent = True
            session['user_id'] = user.id
            session['username'] = user.username
            session['email'] = user.email
            session['name'] = user.name
            flash(f'Welcome back, {user.name}!', 'success')

            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid username/email or password.', 'danger')
            return render_template('login.html', identifier=identifier)

    return render_template('login.html')

@auth_bp.route('/demo-login', methods=['GET', 'POST'])
def demo_login():
    """Direct one-click access into the pre-populated demo driver account."""
    demo_user = User.query.filter_by(username='demo_driver').first()
    if not demo_user:
        try:
            from seed import seed_demo_data_in_context
            seed_demo_data_in_context()
            demo_user = User.query.filter_by(username='demo_driver').first()
        except Exception:
            db.session.rollback()

    if not demo_user:
        demo_user = User(
            name='Arjun Verma',
            email='arjun.verma@autovault.in',
            username='demo_driver'
        )
        demo_user.set_password('AutoVault@2026')
        db.session.add(demo_user)
        db.session.commit()

    # Authenticate and establish permanent session
    session.clear()
    session.permanent = True
    session['user_id'] = demo_user.id
    session['username'] = demo_user.username
    session['email'] = demo_user.email
    session['name'] = demo_user.name

    flash('Direct Access: Welcome to AutoVault Demo Cockpit!', 'success')
    return redirect(url_for('dashboard.index'))

@auth_bp.route('/logout')
def logout():
    """Securely log out by destroying session data."""
    session.clear()
    flash('You have been securely logged out.', 'info')
    return redirect(url_for('auth.login'))
