from flask import Blueprint, render_template, request, jsonify, current_app, redirect, url_for

bp = Blueprint('line', __name__, url_prefix='/line')

@bp.route('/', methods=['GET'])
def index():
    """List all lines"""
    warehouses = current_app.warehouse_system.get_all_warehouses()
    lines = []
    for warehouse in warehouses:
        lines.extend(warehouse.lines)
    return render_template('line/index.html', lines=lines)


@bp.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new line"""
    # Get all warehouses for the form
    warehouses = current_app.warehouse_system.get_all_warehouses()
    
    # Check if there are no warehouses
    if request.method == 'GET' and not warehouses:
        return render_template('line/create.html', warehouses=[])
    
    if request.method == 'POST':
        try:
            line_number = int(request.form['line_number'])
            max_capacity = float(request.form['max_capacity'])
            capacity_type = request.form['capacity_type']
            warehouse_id = request.form['warehouse_id']
            
            if line_number < 1:
                return jsonify({'status': 'error', 'message': 'Line number must be positive'}), 400
                
            if max_capacity <= 0:
                return jsonify({'status': 'error', 'message': 'Maximum capacity must be positive'}), 400
                
            if capacity_type not in ['weight', 'count']:
                return jsonify({'status': 'error', 'message': 'Invalid capacity type'}), 400
            
            # Find warehouse
            warehouse = next((w for w in warehouses if w.serial_number == warehouse_id), None)
            
            if warehouse is None:
                return jsonify({'status': 'error', 'message': 'Warehouse not found'}), 404
            
            # Create line
            line = current_app.warehouse_system.create_line(line_number, max_capacity, capacity_type)
            
            # Add line to warehouse
            current_app.warehouse_system.add_line_to_warehouse(line, warehouse)
            
            return jsonify({
                'status': 'success',
                'message': f'Line {line_number} created successfully',
                'line': {
                    'id': line.serial_number,
                    'line_number': line.line_number,
                    'max_capacity': line.max_capacity,
                    'capacity_type': line.capacity_type
                }
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    return render_template('line/create.html', warehouses=warehouses)

@bp.route('/<serial_number>/approve-mixed', methods=['POST'])
def approve_mixed(serial_number):
    """Approve a line for mixed quality packages"""
    try:
        max_types = int(request.form.get('max_types', 3))
        
        # Find the line
        line = None
        for warehouse in current_app.warehouse_system.get_all_warehouses():
            for l in warehouse.lines:
                if l.serial_number == serial_number:
                    line = l
                    break
        
        if line is None:
            return jsonify({'status': 'error', 'message': 'Line not found'}), 404
        
        # Approve mixed quality
        result = current_app.warehouse_system.approve_mixed_quality_line(line, max_types)
        
        return jsonify({
            'status': 'success',
            'message': f'Line approved for mixed quality (max {max_types} types)'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/<serial_number>/history', methods=['GET'])
def history(serial_number):
    """Get package history for a line"""
    # Find the line
    line = None
    for warehouse in current_app.warehouse_system.get_all_warehouses():
        for l in warehouse.lines:
            if l.serial_number == serial_number:
                line = l
                break
    
    if line is None:
        return jsonify({'status': 'error', 'message': 'Line not found'}), 404
    
    # Get package history
    history = current_app.warehouse_system.get_package_history(line)
    
    # Format history for display
    formatted_history = []
    for entry in history:
        formatted_entry = {
            'package_serial': entry['package'].serial_number,
            'package_quality': entry['package'].quality_mark,
            'package_mass': entry['package'].mass,
            'action': entry['action'],
            'timestamp': entry['timestamp'].isoformat()
        }
        formatted_history.append(formatted_entry)
    
    return render_template('line/history.html', line=line, history=formatted_history)