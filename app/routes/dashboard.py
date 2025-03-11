from flask import Blueprint, render_template, request, jsonify, current_app

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/', methods=['GET'])
def index():
    """Dashboard home page"""
    warehouses = current_app.warehouse_system.get_all_warehouses()
    
    # Calculate system statistics
    statistics = {
        'total_warehouses': len(warehouses),
        'total_lines': sum(len(w.lines) for w in warehouses),
        'total_packages': len(current_app.warehouse_system.manager.packages),
        'total_pallets': len(current_app.warehouse_system.manager.pallets),
        'total_capacity': sum(w.max_capacity for w in warehouses),
        'used_capacity': sum(w.current_capacity_usage for w in warehouses)
    }
    
    # Add utilization percentage
    if statistics['total_capacity'] > 0:
        statistics['utilization_percentage'] = (statistics['used_capacity'] / statistics['total_capacity']) * 100
    else:
        statistics['utilization_percentage'] = 0
    
    return render_template('dashboard/index.html', warehouses=warehouses, statistics=statistics)

@bp.route('/set-offload-order', methods=['POST'])
def set_offload_order():
    """Set package offloading order"""
    try:
        order = request.form['order']
        
        if order not in ['oldest_first', 'newest_first']:
            return jsonify({'status': 'error', 'message': 'Invalid offload order'}), 400
        
        # Set offload order
        result = current_app.warehouse_system.set_offload_order(order)
        
        return jsonify({
            'status': 'success',
            'message': f'Offload order set to {order}'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500