from datetime import datetime, timezone
from app.models import db

class MaintenanceRecord(db.Model):
    """Vehicle maintenance and workshop service history record."""
    __tablename__ = 'maintenance_records'

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False, index=True)
    date = db.Column(db.String(20), nullable=False)  # ISO Date YYYY-MM-DD
    odometer = db.Column(db.Integer, nullable=False, default=0)
    service_type = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text, nullable=True)
    service_center = db.Column(db.String(100), nullable=True)
    cost = db.Column(db.Float, nullable=False, default=0.0)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    vehicle = db.relationship(
        'Vehicle',
        backref=db.backref('maintenance_records', lazy=True, cascade='all, delete-orphan', order_by='MaintenanceRecord.date.desc()')
    )

    def __repr__(self):
        return f"<MaintenanceRecord {self.service_type} on {self.date} (Rs.{self.cost})>"
