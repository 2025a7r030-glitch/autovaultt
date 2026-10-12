from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db

class User(db.Model):
    """User account model with secure password hashing."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(60), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship to user's vehicles
    vehicles = db.relationship('Vehicle', backref='owner', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password: str):
        """Hashes the plaintext password before storage using PBKDF2/scrypt via Werkzeug."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verifies the candidate password against the stored cryptographic hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"
