from flask import Blueprint, render_template, request, jsonify, current_app

bp = Blueprint('package', __name__, url_prefix='/package')

@bp.route('/', methods=['GET'])
def index():
    """List all packages"""
    packages = current_app.warehouse_system.manager.packages
    return render_template('package/index.html', packages=packages)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new package"""
    if request.method == 'POST':
        try:
            package_type = request.form['package_type']
            quality_mark = request.form['quality_mark']
            mass = float(request.form['mass'])
            
            if package_type not in ['loose', 'carton']:
                return jsonify({'status': 'error', 'message': 'Invalid package type'}), 400
                
            if not quality_mark:
                return jsonify({'status': 'error', 'message': 'Quality mark is required'}), 400
                
            if mass <= 0:
                return jsonify({'status': 'error', 'message': 'Mass must be positive'}), 400
            
            # Create package
            package = current_app.warehouse_system.create_package(package_type, quality_mark, mass)
            
            return jsonify({
                'status': 'success',
                'message': f'{package_type.capitalize()} package created successfully',
                'package': {
                    'id': package.serial_number,
                    'type': package.package_type,
                    'quality_mark': package.quality_mark,
                    'mass': package.mass
                }
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    return render_template('package/create.html')

@bp.route('/load-to-pallet', methods=['POST'])
def load_to_pallet():
    """Load a package to a pallet"""
    try:
        package_id = request.form['package_id']
        pallet_id = request.form['pallet_id']
        
        # Find package and pallet
        package = None
        for p in current_app.warehouse_system.manager.packages:
            if p.serial_number == package_id:
                package = p
                break
        
        pallet = None
        for p in current_app.warehouse_system.manager.pallets:
            if p.serial_number == pallet_id:
                pallet = p
                break
        
        if package is None:
            return jsonify({'status': 'error', 'message': 'Package not found'}), 404
        
        if pallet is None:
            return jsonify({'status': 'error', 'message': 'Pallet not found'}), 404
        
        # Load package to pallet
        result = current_app.warehouse_system.load_package_to_pallet(package, pallet)
        
        if result:
            return jsonify({
                'status': 'success',
                'message': 'Package loaded to pallet successfully'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to load package to pallet. Check quality mark and capacity.'
            }), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/load-to-line', methods=['POST'])
def load_to_line():
    """Load a carton package directly to a line"""
    try:
        package_id = request.form['package_id']
        line_id = request.form['line_id']
        
        # Find package and line
        package = None
        for p in current_app.warehouse_system.manager.packages:
            if p.serial_number == package_id:
                package = p
                break
        
        line = None
        for warehouse in current_app.warehouse_system.get_all_warehouses():
            for l in warehouse.lines:
                if l.serial_number == line_id:
                    line = l
                    break
        
        if package is None:
            return jsonify({'status': 'error', 'message': 'Package not found'}), 404
        
        if line is None:
            return jsonify({'status': 'error', 'message': 'Line not found'}), 404
        
        # Load carton to line
        if package.package_type != 'carton':
            return jsonify({
                'status': 'error',
                'message': 'Only carton packages can be loaded directly to lines'
            }), 400
        
        result = current_app.warehouse_system.load_carton_to_line(package, line)
        
        if result:
            return jsonify({
                'status': 'success',
                'message': 'Carton loaded to line successfully'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to load carton to line. Check line type and capacity.'
            }), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/offload', methods=['POST'])
def offload():
    """Offload a package from its current location"""
    try:
        package_id = request.form['package_id']
        
        # Find package
        package = None
        for p in current_app.warehouse_system.manager.packages:
            if p.serial_number == package_id:
                package = p
                break
        
        if package is None:
            return jsonify({'status': 'error', 'message': 'Package not found'}), 404
        
        # Offload package
        result = current_app.warehouse_system.offload_package(package)
        
        if result:
            return jsonify({
                'status': 'success',
                'message': 'Package offloaded successfully'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to offload package. Package might not be assigned to a location.'
            }), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/discard', methods=['POST'])
def discard():
    """Discard a package (mark as bad)"""
    try:
        package_id = request.form['package_id']
        
        # Find package
        package = None
        for p in current_app.warehouse_system.manager.packages:
            if p.serial_number == package_id:
                package = p
                break
        
        if package is None:
            return jsonify({'status': 'error', 'message': 'Package not found'}), 404
        
        # Discard package
        result = current_app.warehouse_system.discard_package(package)
        
        return jsonify({
            'status': 'success',
            'message': 'Package discarded successfully'
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/search', methods=['GET', 'POST'])
def search():
    """Search for a package by serial number"""
    result = None
    
    if request.method == 'POST':
        try:
            serial_number = request.form['serial_number']
            
            # Search for package
            result = current_app.warehouse_system.search_package(serial_number)
            
            if result is None:
                return jsonify({
                    'status': 'error',
                    'message': 'Package not found'
                }), 404
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    return render_template('package/search.html', result=result)