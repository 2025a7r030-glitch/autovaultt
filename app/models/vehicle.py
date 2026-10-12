from datetime import datetime, timezone
from app.models import db

class Vehicle(db.Model):
    """Vehicle model representing vehicles owned by a registered user."""
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    manufacturer = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    variant = db.Column(db.String(50), nullable=True)
    registration_number = db.Column(db.String(30), nullable=True)
    fuel_type = db.Column(db.String(30), nullable=False, default='Petrol')
    transmission = db.Column(db.String(30), nullable=False, default='Manual')
    manufacturing_year = db.Column(db.Integer, nullable=True)
    purchase_date = db.Column(db.String(20), nullable=True)
    current_odometer = db.Column(db.Integer, nullable=False, default=0)
    color = db.Column(db.String(30), nullable=True)
    insurance_expiry = db.Column(db.String(20), nullable=True)
    pollution_expiry = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    @property
    def display_name(self) -> str:
        """Helper to return readable title e.g. 'Hyundai i20'."""
        return f"{self.manufacturer} {self.model}"

    def __repr__(self):
        return f"<Vehicle {self.manufacturer} {self.model} ({self.registration_number})>"
