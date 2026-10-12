"""
AutoVault Sample Data Seeder
----------------------------
Utility to populate realistic demonstration data for academic presentations and testing.
Usage: python seed.py
"""

from datetime import date, timedelta
from app import create_app
from app.models import db
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.fuel import FuelEntry
from app.models.maintenance import MaintenanceRecord
from app.models.reminder import Reminder

def seed_demo_data_in_context():
    """Seed demo data within an already active Flask app context."""
    # Check if demo user already exists
    demo_user = User.query.filter_by(username='demo_driver').first()
    if not demo_user:
        demo_user = User(
            name='Arjun Verma',
            email='arjun.demo@autovault.in',
            username='demo_driver'
        )
        demo_user.set_password('AutoVault@2026')
        db.session.add(demo_user)
        db.session.commit()
        print("Created demo account: demo_driver / AutoVault@2026")


        # Check if vehicle exists
        vehicle = Vehicle.query.filter_by(user_id=demo_user.id, model='i20').first()
        if not vehicle:
            vehicle = Vehicle(
                user_id=demo_user.id,
                manufacturer='Hyundai',
                model='i20',
                variant='Sportz 1.2 Petrol',
                registration_number='DL 01 AB 9988',
                fuel_type='Petrol',
                transmission='Manual',
                manufacturing_year=2023,
                purchase_date='2023-04-15',
                current_odometer=14850,
                color='Titan Gray',
                insurance_expiry='2027-04-14',
                pollution_expiry='2027-01-10'
            )
            db.session.add(vehicle)
            db.session.commit()
            print(f"Added vehicle: {vehicle.display_name}")

        # Seed Fuel Entries
        if not FuelEntry.query.filter_by(vehicle_id=vehicle.id).first():
            fills = [
                {'date': '2026-08-10', 'odometer': 12000, 'litres': 35.0, 'price': 96.50, 'station': 'IndianOil NH48', 'notes': 'Highway drive start'},
                {'date': '2026-08-25', 'odometer': 12520, 'litres': 34.5, 'price': 96.80, 'station': 'Shell Sector 22', 'notes': 'City commute'},
                {'date': '2026-09-12', 'odometer': 13080, 'litres': 36.0, 'price': 97.00, 'station': 'BPCL Expressway', 'notes': 'Full tank fill'},
                {'date': '2026-09-28', 'odometer': 13650, 'litres': 35.5, 'price': 96.90, 'station': 'HPCL AutoCare', 'notes': 'Weekend roadtrip'},
                {'date': '2026-10-04', 'odometer': 14220, 'litres': 36.2, 'price': 97.20, 'station': 'IndianOil Ring Road', 'notes': 'Office commute'},
                {'date': '2026-10-06', 'odometer': 14850, 'litres': 38.0, 'price': 97.10, 'station': 'Shell Aerocity', 'notes': 'Recent refill'}
            ]
            for f in fills:
                entry = FuelEntry(
                    vehicle_id=vehicle.id,
                    date=f['date'],
                    odometer=f['odometer'],
                    litres=f['litres'],
                    price_per_litre=f['price'],
                    total_cost=round(f['litres'] * f['price'], 2),
                    station=f['station'],
                    notes=f['notes']
                )
                db.session.add(entry)
            db.session.commit()
            print("Populated realistic fuel logs with consecutive mileage intervals.")

        # Seed Maintenance Records
        if not MaintenanceRecord.query.filter_by(vehicle_id=vehicle.id).first():
            services = [
                {
                    'date': '2026-05-10', 'odometer': 10000, 'service_type': 'General Service',
                    'cost': 4800.0, 'service_center': 'Hyundai Motor Plaza',
                    'description': '10,000 km scheduled inspection, engine oil flush, synthetic 5W-30 filled, OEM oil filter replaced.',
                    'notes': 'Invoice #HMP-78190'
                },
                {
                    'date': '2026-07-22', 'odometer': 11800, 'service_type': 'Wheel Alignment',
                    'cost': 950.0, 'service_center': 'Bridgestone Tyre Care',
                    'description': '4-wheel computerized alignment and balancing with tyre rotation.',
                    'notes': 'Tyre tread depth 6.5mm'
                },
                {
                    'date': '2026-09-15', 'odometer': 13200, 'service_type': 'AC Service',
                    'cost': 1850.0, 'service_center': 'Bosch Car Workshop',
                    'description': 'Cabin AC pollen filter replaced, refrigerant gas pressure checked, evaporator duct disinfection.',
                    'notes': 'Optimal cooling restored'
                }
            ]
            for s in services:
                rec = MaintenanceRecord(
                    vehicle_id=vehicle.id,
                    date=s['date'],
                    odometer=s['odometer'],
                    service_type=s['service_type'],
                    cost=s['cost'],
                    service_center=s['service_center'],
                    description=s['description'],
                    notes=s['notes']
                )
                db.session.add(rec)
            db.session.commit()
            print("Populated service and maintenance history.")

        # Seed Reminders
        if not Reminder.query.filter_by(vehicle_id=vehicle.id).first():
            today = date.today()
            reminders = [
                {
                    'title': 'Pollution (PUCC) Certificate Renewal',
                    'description': 'Visit authorized emission testing kiosk before deadline.',
                    'due_date': (today + timedelta(days=5)).isoformat(),
                    'due_mileage': None,
                    'priority': 'High',
                    'status': 'Upcoming'
                },
                {
                    'title': '20,000 KM Major Periodic Service',
                    'description': 'Spark plugs check, brake fluid flush, throttle body cleaning.',
                    'due_date': (today + timedelta(days=120)).isoformat(),
                    'due_mileage': 20000,
                    'priority': 'Medium',
                    'status': 'Upcoming'
                },
                {
                    'title': 'Tyre Pressure & Rotation Check',
                    'description': 'Rotate front and rear tyres to ensure even tread wear.',
                    'due_date': (today + timedelta(days=20)).isoformat(),
                    'due_mileage': 15000,
                    'priority': 'Medium',
                    'status': 'Upcoming'
                }
            ]
            for r in reminders:
                rem = Reminder(
                    vehicle_id=vehicle.id,
                    title=r['title'],
                    description=r['description'],
                    due_date=r['due_date'],
                    due_mileage=r['due_mileage'],
                    priority=r['priority'],
                    status=r['status']
                )
                db.session.add(rem)
            db.session.commit()
            print("Populated predictive reminders.")

    print("=== Demo Data Seeding Completed Successfully! ===")
    print("You can log in with:")
    print("Username: demo_driver")
    print("Password: AutoVault@2026")

def seed_demo_data():
    """Create app instance and populate demo data."""
    app = create_app()
    with app.app_context():
        seed_demo_data_in_context()

if __name__ == '__main__':
    seed_demo_data()

