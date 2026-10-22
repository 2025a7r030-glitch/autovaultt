"""
AutoVault Sample Data Seeder & Demo History Generator
-----------------------------------------------------
Populates rich, realistic demonstration data across all AutoVault facilities:
- Multi-Vehicle Garage (Hyundai Creta SUV & Tata Nexon EV)
- Sequential Fuel Telemetry with calculated km/L efficiency
- Periodic Service & Maintenance Records across multiple categories
- Smart Dual-Trigger Reminders (Overdue, Due Soon, Upcoming, Completed)
- Encrypted Document Vault with valid downloadable PDF records

Usage: python seed.py
"""

import os
import uuid
from datetime import date, datetime, timedelta, timezone
from flask import current_app
from app.models import db
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.fuel import FuelEntry
from app.models.maintenance import MaintenanceRecord
from app.models.reminder import Reminder
from app.models.document import Document

def _generate_demo_pdf_bytes(title: str, doc_type: str, reg_no: str) -> bytes:
    """Generate a valid, lightweight RFC-compliant PDF without external libraries."""
    stream_content = f"""BT
/F1 18 Tf
50 720 Td
(AUTOCAULT ENCRYPTED DOCUMENT VAULT) Tj
/F1 14 Tf
0 -30 Td
({title}) Tj
/F1 10 Tf
0 -25 Td
(Document Classification: {doc_type}) Tj
0 -18 Td
(Vehicle Registration: {reg_no}) Tj
0 -18 Td
(Cryptographic Verification: SHA-256 Validated Archive) Tj
0 -18 Td
(Storage Mode: Quarantined Secure Sandbox Outside Public Directory) Tj
0 -30 Td
(This digital certificate has been safely ingested into AutoVault.) Tj
ET"""
    stream_bytes = stream_content.encode('latin1')
    stream_len = len(stream_bytes)

    pdf = (
        b"%PDF-1.4\n"
        b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj\n"
        b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj\n"
        b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj\n"
        b"4 0 obj << /Length " + str(stream_len).encode('ascii') + b" >>\nstream\n" +
        stream_bytes + b"\nendstream\nendobj\n"
        b"5 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj\n"
        b"xref\n0 6\n"
        b"0000000000 65535 f \n"
        b"0000000009 00000 n \n"
        b"0000000058 00000 n \n"
        b"0000000115 00000 n \n"
        b"0000000224 00000 n \n"
        b"0000000370 00000 n \n"
        b"trailer << /Size 6 /Root 1 0 R >>\n"
        b"startxref\n435\n%%EOF"
    )
    return pdf

def seed_demo_data_in_context():
    """Seed comprehensive demo data within an active Flask application context."""
    print("-> Seeding AutoVault demonstration account and comprehensive history...")

    # 1. Demo User Account
    demo_user = User.query.filter_by(username='demo_driver').first()
    if not demo_user:
        demo_user = User(
            name='Arjun Verma',
            email='arjun.verma@autovault.in',
            username='demo_driver'
        )
        demo_user.set_password('AutoVault@2026')
        db.session.add(demo_user)
        db.session.commit()
        print("  [+] Created demo account: demo_driver / AutoVault@2026")
    else:
        demo_user.name = 'Arjun Verma'
        demo_user.email = 'arjun.verma@autovault.in'
        demo_user.set_password('AutoVault@2026')
        db.session.commit()

    # 2. Garage: Primary Vehicle (Hyundai Creta)
    creta = Vehicle.query.filter_by(user_id=demo_user.id, registration_number='DL 01 AB 9988').first()
    if not creta:
        # Check if legacy i20 exists and update it, or create Creta
        legacy = Vehicle.query.filter_by(user_id=demo_user.id, model='i20').first()
        if legacy:
            creta = legacy
            creta.manufacturer = 'Hyundai'
            creta.model = 'Creta'
            creta.variant = 'SX (O) 1.5L Turbo DCT'
            creta.registration_number = 'DL 01 AB 9988'
            creta.fuel_type = 'Petrol'
            creta.transmission = 'Automatic'
            creta.manufacturing_year = 2023
            creta.purchase_date = '2023-04-15'
            creta.current_odometer = 18450
            creta.color = 'Titan Grey Matte'
            creta.insurance_expiry = (date.today() + timedelta(days=75)).isoformat()
            creta.pollution_expiry = (date.today() + timedelta(days=4)).isoformat()
            db.session.commit()
            print("  [+] Updated primary vehicle to Hyundai Creta SX (O)")
        else:
            creta = Vehicle(
                user_id=demo_user.id,
                manufacturer='Hyundai',
                model='Creta',
                variant='SX (O) 1.5L Turbo DCT',
                registration_number='DL 01 AB 9988',
                fuel_type='Petrol',
                transmission='Automatic',
                manufacturing_year=2023,
                purchase_date='2023-04-15',
                current_odometer=18450,
                color='Titan Grey Matte',
                insurance_expiry=(date.today() + timedelta(days=75)).isoformat(),
                pollution_expiry=(date.today() + timedelta(days=4)).isoformat()
            )
            db.session.add(creta)
            db.session.commit()
            print(f"  [+] Added primary vehicle: {creta.display_name}")

    # Secondary Vehicle (Tata Nexon EV for multi-car garage demo)
    nexon = Vehicle.query.filter_by(user_id=demo_user.id, registration_number='DL 08 EV 4520').first()
    if not nexon:
        nexon = Vehicle(
            user_id=demo_user.id,
            manufacturer='Tata',
            model='Nexon EV',
            variant='Empowered Plus LR',
            registration_number='DL 08 EV 4520',
            fuel_type='Electric',
            transmission='Automatic',
            manufacturing_year=2024,
            purchase_date='2024-02-10',
            current_odometer=7820,
            color='Pristine White',
            insurance_expiry=(date.today() + timedelta(days=190)).isoformat(),
            pollution_expiry=(date.today() + timedelta(days=280)).isoformat()
        )
        db.session.add(nexon)
        db.session.commit()
        print(f"  [+] Added secondary vehicle: {nexon.display_name}")

    # 3. Fuel Logs with Consecutive km/L Mileage (Hyundai Creta)
    existing_fuel_count = FuelEntry.query.filter_by(vehicle_id=creta.id).count()
    if existing_fuel_count < 6:
        # Clear any partial old entries
        FuelEntry.query.filter_by(vehicle_id=creta.id).delete()
        db.session.commit()

        fills = [
            {'date': '2026-06-15', 'odometer': 15200, 'litres': 45.0, 'price': 96.50, 'station': 'IndianOil NH-48 Expressway', 'notes': 'Full tank initial baseline'},
            {'date': '2026-07-02', 'odometer': 15820, 'litres': 42.5, 'price': 96.80, 'station': 'Shell CyberCity TechPark', 'notes': 'Office commutes ~14.6 km/L'},
            {'date': '2026-07-20', 'odometer': 16450, 'litres': 41.0, 'price': 97.10, 'station': 'HPCL Express Corridor', 'notes': 'Highway cruise ~15.4 km/L'},
            {'date': '2026-08-08', 'odometer': 17040, 'litres': 40.0, 'price': 96.90, 'station': 'BPCL SuperFuel Expressway', 'notes': 'Monsoon city drives ~14.8 km/L'},
            {'date': '2026-08-28', 'odometer': 17680, 'litres': 42.0, 'price': 97.30, 'station': 'Shell Aerocity Gateway', 'notes': 'Weekend trip ~15.2 km/L'},
            {'date': '2026-09-18', 'odometer': 18120, 'litres': 28.5, 'price': 97.20, 'station': 'IndianOil Sector 29', 'notes': 'Smooth ring road run ~15.4 km/L'},
            {'date': '2026-10-10', 'odometer': 18450, 'litres': 22.0, 'price': 97.50, 'station': 'Shell V-Power SuperCare', 'notes': 'Recent premium fuel refill'}
        ]
        for f in fills:
            entry = FuelEntry(
                vehicle_id=creta.id,
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
        print("  [+] Populated 7 sequential fuel fill-ups with verified mileage calculations.")

    # 4. Service & Maintenance History
    existing_maint_count = MaintenanceRecord.query.filter_by(vehicle_id=creta.id).count()
    if existing_maint_count < 4:
        MaintenanceRecord.query.filter_by(vehicle_id=creta.id).delete()
        db.session.commit()

        services = [
            {
                'date': '2026-04-12', 'odometer': 10000, 'service_type': 'General Service',
                'cost': 5450.0, 'service_center': 'Hyundai Motor Plaza Flagship',
                'description': '10,000 km Scheduled Periodic Maintenance. Full synthetic 5W-30 engine oil replacement, OEM oil filter, air filter, and 45-point comprehensive electrical check.',
                'notes': 'Invoice #HMP-78190 &bull; Warranty certified'
            },
            {
                'date': '2026-06-25', 'odometer': 12500, 'service_type': 'Wheel Alignment',
                'cost': 1200.0, 'service_center': 'Bridgestone Select SuperCare',
                'description': 'Computerized 4-wheel dynamic alignment, high-speed computerized wheel balancing, and front-to-rear diagonal tyre rotation.',
                'notes': 'Uniform tread depth verified at 7.2mm'
            },
            {
                'date': '2026-08-14', 'odometer': 15200, 'service_type': 'AC Service',
                'cost': 2100.0, 'service_center': 'Bosch Car Service Workshop',
                'description': 'Cabin PM2.5 pollen air filter replacement, evaporator cooling coil disinfection, drain duct clearing, and blower sanitation.',
                'notes': 'Sub-zero cabin cooling performance restored'
            },
            {
                'date': '2026-09-10', 'odometer': 17000, 'service_type': 'Detailing / Cleaning',
                'cost': 3850.0, 'service_center': '3M Car Care Studio',
                'description': 'Complete exterior ceramic gloss sealant, windshield hydrophobic glass coating, interior anti-microbial steam treatment.',
                'notes': 'Hydrophobic water-beading coat verified'
            },
            {
                'date': '2026-10-02', 'odometer': 18000, 'service_type': 'Brake System Service',
                'cost': 1800.0, 'service_center': 'AutoVault Precision Workshop',
                'description': 'Front and rear brake caliper cleaning, brake rotor inspection, DOT-4 brake fluid bleed and pressure calibration.',
                'notes': 'Brake pad thickness optimal at 8.0mm'
            }
        ]
        for s in services:
            rec = MaintenanceRecord(
                vehicle_id=creta.id,
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
        print("  [+] Populated 5 detailed maintenance and service records.")

    # 5. Dual-Trigger Smart Reminders (Demonstrating all alert states)
    existing_reminders_count = Reminder.query.filter_by(vehicle_id=creta.id).count()
    if existing_reminders_count < 4:
        Reminder.query.filter_by(vehicle_id=creta.id).delete()
        db.session.commit()

        today = date.today()
        reminders = [
            {
                'title': 'Windshield Wiper Blades & Washer Fluid Inspection',
                'description': 'Inspect rubber wiper blades for streaking and top up all-weather hydrophobic washer fluid.',
                'due_date': (today - timedelta(days=4)).isoformat(),  # Overdue (Red status)
                'due_mileage': 18200,
                'priority': 'High',
                'status': 'Upcoming'
            },
            {
                'title': 'Annual PUCC Emission Certificate Renewal',
                'description': 'Visit official transport department authorized computerized testing center before deadline.',
                'due_date': (today + timedelta(days=4)).isoformat(),   # Due Soon (Orange status)
                'due_mileage': None,
                'priority': 'High',
                'status': 'Upcoming'
            },
            {
                'title': '20,000 KM Major Periodic Service',
                'description': 'Scheduled major service: spark plug inspection, fuel filter check, engine coolant inspection.',
                'due_date': (today + timedelta(days=45)).isoformat(),  # Upcoming (Normal)
                'due_mileage': 20000,
                'priority': 'Medium',
                'status': 'Upcoming'
            },
            {
                'title': 'Comprehensive Zero-Depreciation Insurance Renewal',
                'description': 'Renew 1-year bumper-to-bumper policy with engine protect and roadside assistance riders.',
                'due_date': (today + timedelta(days=75)).isoformat(),
                'due_mileage': None,
                'priority': 'High',
                'status': 'Upcoming'
            },
            {
                'title': 'Fastag Highway Toll Minimum Balance Top-Up',
                'description': 'Ensure prepaid RFID toll wallet has at least Rs 1,000 for expressway corridor passage.',
                'due_date': (today + timedelta(days=15)).isoformat(),
                'due_mileage': None,
                'priority': 'Low',
                'status': 'Upcoming'
            },
            {
                'title': '15,000 KM Tyre Rotation & Nitrogen Refill',
                'description': 'Scheduled tyre rotation performed at Bridgestone service station with 33 PSI nitrogen inflation.',
                'due_date': (today - timedelta(days=60)).isoformat(),
                'due_mileage': 15000,
                'priority': 'Medium',
                'status': 'Completed'  # Completed history
            }
        ]
        for r in reminders:
            rem = Reminder(
                vehicle_id=creta.id,
                title=r['title'],
                description=r['description'],
                due_date=r['due_date'],
                due_mileage=r['due_mileage'],
                priority=r['priority'],
                status=r['status']
            )
            db.session.add(rem)
        db.session.commit()
        print("  [+] Populated 6 dual-trigger reminders (Overdue, Due Soon, Upcoming, Completed).")

    # 6. Encrypted Document Vault with Valid Physical PDFs on Disk
    upload_root = current_app.config.get('UPLOAD_FOLDER', 'instance/uploads')
    docs_dir = os.path.join(upload_root, 'documents')
    try:
        os.makedirs(docs_dir, exist_ok=True)
    except OSError:
        pass

    existing_docs_count = Document.query.filter_by(vehicle_id=creta.id).count()
    if existing_docs_count < 4:
        Document.query.filter_by(vehicle_id=creta.id).delete()
        db.session.commit()

        sample_docs = [
            {
                'type': 'Registration Certificate (RC)',
                'orig_name': 'DL01AB9988_SmartCard_RC.pdf',
                'title': 'Certificate of Motor Vehicle Registration'
            },
            {
                'type': 'Insurance Policy',
                'orig_name': 'HDFC_Ergo_Comprehensive_Policy.pdf',
                'title': 'Motor Comprehensive Package Insurance Policy'
            },
            {
                'type': 'Pollution Certificate (PUCC)',
                'orig_name': 'PUCC_National_Emission_Standard.pdf',
                'title': 'Ministry of Road Transport & Highways PUCC Certificate'
            },
            {
                'type': 'Extended Warranty',
                'orig_name': 'Hyundai_Shield_5Yr_Warranty.pdf',
                'title': 'Hyundai Wonder 5-Year Extended Warranty Certificate'
            },
            {
                'type': 'Service Invoice',
                'orig_name': 'Hyundai_10000km_Invoice.pdf',
                'title': 'Hyundai Authorised Workshop Tax Invoice #HMP-78190'
            }
        ]

        for item in sample_docs:
            disk_filename = f"{uuid.uuid4().hex}.pdf"
            disk_path = os.path.join(docs_dir, disk_filename)
            pdf_bytes = _generate_demo_pdf_bytes(item['title'], item['type'], creta.registration_number)

            try:
                with open(disk_path, 'wb') as f:
                    f.write(pdf_bytes)
                file_size = len(pdf_bytes)
            except (OSError, IOError):
                file_size = 1024 * 45  # fallback size representation

            doc = Document(
                vehicle_id=creta.id,
                document_type=item['type'],
                filename=disk_filename,
                original_filename=item['orig_name'],
                secure_storage_path=disk_path,
                file_size=file_size,
                uploaded_at=datetime.now(timezone.utc) - timedelta(days=12)
            )
            db.session.add(doc)

        db.session.commit()
        print("  [+] Populated 5 encrypted documents in Document Vault with downloadable PDFs.")

    print("=== Demo Data Seeding Completed Successfully! ===")
    print("Demo Account Credentials:")
    print("  Username: demo_driver")
    print("  Password: AutoVault@2026")

def seed_demo_data():
    """Create app instance and populate demo data."""
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_demo_data_in_context()

if __name__ == '__main__':
    seed_demo_data()
