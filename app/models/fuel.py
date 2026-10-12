from datetime import datetime, timezone
from app.models import db

class FuelEntry(db.Model):
    """Fuel transaction record tracking mileage, fuel quantity, and running expenditure."""
    __tablename__ = 'fuel_entries'

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False, index=True)
    date = db.Column(db.String(20), nullable=False)  # ISO Date YYYY-MM-DD
    odometer = db.Column(db.Integer, nullable=False)
    litres = db.Column(db.Float, nullable=False)
    price_per_litre = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    station = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    vehicle = db.relationship(
        'Vehicle',
        backref=db.backref('fuel_entries', lazy=True, cascade='all, delete-orphan', order_by='FuelEntry.odometer.asc()')
    )

    def __repr__(self):
        return f"<FuelEntry {self.date} {self.litres}L @ Rs.{self.total_cost}>"
