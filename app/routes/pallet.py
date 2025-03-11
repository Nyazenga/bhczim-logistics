from flask import Blueprint, render_template, request, jsonify, current_app

bp = Blueprint('pallet', __name__, url_prefix='/pallet')

@bp.route('/', methods=['GET'])
def index():
    """List all pallets"""
    pallets = current_app.warehouse_system.manager.pallets
    return render_template('pallet/index.html', pallets=pallets)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new pallet"""
    if request.method == 'POST':
        try:
            quality_mark = request.form['quality_mark']
            max_capacity = int(request.form['max_capacity'])
            
            if not quality_mark:
                return jsonify({'status': 'error', 'message': 'Quality mark is required'}), 400
                
            if max_capacity <= 0:
                return jsonify({'status': 'error', 'message': 'Maximum capacity must be positive'}), 400
            
            # Create pallet
            pallet = current_app.warehouse_system.create_pallet(quality_mark, max_capacity)
            
            return jsonify({
                'status': 'success',
                'message': 'Pallet created successfully',
                'pallet': {
                    'id': pallet.serial_number,
                    'quality_mark': pallet.quality_mark,
                    'max_capacity': pallet.max_capacity
                }
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    return render_template('pallet/create.html')

@bp.route('/load-to-line', methods=['POST'])
def load_to_line():
    """Load a pallet to a line"""
    try:
        pallet_id = request.form['pallet_id']
        line_id = request.form['line_id']
        
        # Find pallet and line
        pallet = None
        for p in current_app.warehouse_system.manager.pallets:
            if p.serial_number == pallet_id:
                pallet = p
                break
        
        line = None
        for warehouse in current_app.warehouse_system.get_all_warehouses():
            for l in warehouse.lines:
                if l.serial_number == line_id:
                    line = l
                    break
        
        if pallet is None:
            return jsonify({'status': 'error', 'message': 'Pallet not found'}), 404
        
        if line is None:
            return jsonify({'status': 'error', 'message': 'Line not found'}), 404
        
        # Load pallet to line
        result = current_app.warehouse_system.load_pallet_to_line(pallet, line)
        
        if result:
            return jsonify({
                'status': 'success',
                'message': 'Pallet loaded to line successfully'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to load pallet to line. Check line type and capacity.'
            }), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    

@bp.route('/offload', methods=['POST'])
def offload():
    """Offload a pallet from its current location"""
    try:
        pallet_id = request.form['pallet_id']
        
        # Find pallet
        pallet = None
        for p in current_app.warehouse_system.manager.pallets:
            if p.serial_number == pallet_id:
                pallet = p
                break
        
        if pallet is None:
            return jsonify({'status': 'error', 'message': 'Pallet not found'}), 404
        
        # Offload pallet
        result = current_app.warehouse_system.offload_pallet(pallet)
        
        if result:
            return jsonify({
                'status': 'success',
                'message': 'Pallet offloaded successfully'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to offload pallet. Pallet might not be assigned to a location.'
            }), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/search', methods=['GET', 'POST'])
def search():
    """Search for a pallet by serial number"""
    result = None
    
    if request.method == 'POST':
        try:
            serial_number = request.form['serial_number']
            
            # Search for pallet
            result = current_app.warehouse_system.search_pallet(serial_number)
            
            if result is None:
                return jsonify({
                    'status': 'error',
                    'message': 'Pallet not found'
                }), 404
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    return render_template('pallet/search.html', result=result)