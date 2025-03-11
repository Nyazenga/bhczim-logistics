from flask import Blueprint, render_template, request, jsonify, current_app, flash, redirect, url_for

bp = Blueprint('warehouse', __name__, url_prefix='/warehouse')

@bp.route('/', methods=['GET'])
def index():
    """Show all warehouses"""
    warehouses = current_app.warehouse_system.get_all_warehouses()
    return render_template('warehouse/index.html', warehouses=warehouses)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new warehouse"""
    if request.method == 'POST':
        try:
            name = request.form['name']
            max_capacity = float(request.form['max_capacity'])
            
            if not name:
                return jsonify({'status': 'error', 'message': 'Warehouse name is required'}), 400
            
            if max_capacity <= 0:
                return jsonify({'status': 'error', 'message': 'Maximum capacity must be positive'}), 400
            
            warehouse = current_app.warehouse_system.create_warehouse(name, max_capacity)
            
            return jsonify({
                'status': 'success',
                'message': f'Warehouse {name} created successfully',
                'warehouse': {
                    'id': warehouse.serial_number,
                    'name': warehouse.name,
                    'max_capacity': warehouse.max_capacity
                }
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    return render_template('warehouse/create.html')

@bp.route('/<serial_number>', methods=['GET'])
def detail(serial_number):
    """Show warehouse details"""
    warehouses = current_app.warehouse_system.get_all_warehouses()
    warehouse = next((w for w in warehouses if w.serial_number == serial_number), None)
    
    if warehouse is None:
        return jsonify({'status': 'error', 'message': 'Warehouse not found'}), 404
    
    snapshot = current_app.warehouse_system.get_warehouse_snapshot(warehouse)
    return render_template('warehouse/detail.html', warehouse=warehouse, snapshot=snapshot)

@bp.route('/<serial_number>/snapshot', methods=['GET'])
def snapshot(serial_number):
    """Get warehouse snapshot in JSON format"""
    warehouses = current_app.warehouse_system.get_all_warehouses()
    warehouse = next((w for w in warehouses if w.serial_number == serial_number), None)
    
    if warehouse is None:
        return jsonify({'status': 'error', 'message': 'Warehouse not found'}), 404
    
    snapshot = current_app.warehouse_system.get_warehouse_snapshot(warehouse)
    return jsonify(snapshot)