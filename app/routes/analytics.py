import json
from collections import defaultdict
from flask import Blueprint, render_template, request
from app.models.vehicle import Vehicle
from app.models.fuel import FuelEntry
from app.models.maintenance import MaintenanceRecord
from app.routes.auth import login_required, get_current_user

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics')
@login_required
def index():
    user = get_current_user()
    vehicles = Vehicle.query.filter_by(user_id=user.id).order_by(Vehicle.created_at.desc()).all()
    selected_id = request.args.get('selected', type=int)

    selected_vehicle = None
    if selected_id:
        selected_vehicle = Vehicle.query.filter_by(id=selected_id, user_id=user.id).first()
    if not selected_vehicle and vehicles:
        selected_vehicle = vehicles[0]

    has_data = False
    analytics_payload = {
        'months': [],
        'fuel_spending': [],
        'maintenance_spending': [],
        'expense_breakdown': {'fuel': 0.0, 'maintenance': 0.0},
        'mileage_dates': [],
        'mileage_values': [],
        'maintenance_categories': {'labels': [], 'values': []}
    }

    total_fuel_expense = 0.0
    total_maint_expense = 0.0

    if selected_vehicle:
        fuel_entries = FuelEntry.query.filter_by(vehicle_id=selected_vehicle.id).order_by(FuelEntry.date.asc(), FuelEntry.odometer.asc()).all()
        maint_records = MaintenanceRecord.query.filter_by(vehicle_id=selected_vehicle.id).order_by(MaintenanceRecord.date.asc()).all()

        if fuel_entries or maint_records:
            has_data = True

        # Monthly aggregation
        monthly_fuel = defaultdict(float)
        for f in fuel_entries:
            month_key = f.date[:7] if len(f.date) >= 7 else 'Unknown'
            monthly_fuel[month_key] += f.total_cost
            total_fuel_expense += f.total_cost

        monthly_maint = defaultdict(float)
        category_maint = defaultdict(float)
        for m in maint_records:
            month_key = m.date[:7] if len(m.date) >= 7 else 'Unknown'
            monthly_maint[month_key] += m.cost
            category_maint[m.service_type] += m.cost
            total_maint_expense += m.cost

        all_months = sorted(list(set(list(monthly_fuel.keys()) + list(monthly_maint.keys()))))
        analytics_payload['months'] = all_months
        analytics_payload['fuel_spending'] = [round(monthly_fuel[m], 2) for m in all_months]
        analytics_payload['maintenance_spending'] = [round(monthly_maint[m], 2) for m in all_months]
        analytics_payload['expense_breakdown'] = {
            'fuel': round(total_fuel_expense, 2),
            'maintenance': round(total_maint_expense, 2)
        }

        # Mileage trend calculations
        sorted_fuels = sorted(fuel_entries, key=lambda x: (x.odometer, x.date))
        for i in range(1, len(sorted_fuels)):
            curr = sorted_fuels[i]
            prev = sorted_fuels[i - 1]
            dist = curr.odometer - prev.odometer
            if dist > 0 and curr.litres > 0:
                mpg = round(dist / curr.litres, 2)
                analytics_payload['mileage_dates'].append(curr.date)
                analytics_payload['mileage_values'].append(mpg)

        # Maintenance category breakdown
        analytics_payload['maintenance_categories'] = {
            'labels': list(category_maint.keys()),
            'values': [round(v, 2) for v in category_maint.values()]
        }

    return render_template(
        'analytics.html',
        user=user,
        vehicles=vehicles,
        selected_vehicle=selected_vehicle,
        has_data=has_data,
        analytics_json=json.dumps(analytics_payload),
        total_expense=round(total_fuel_expense + total_maint_expense, 2),
        total_fuel=round(total_fuel_expense, 2),
        total_maint=round(total_maint_expense, 2)
    )
