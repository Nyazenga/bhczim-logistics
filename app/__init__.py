from flask import Flask

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DEBUG=True
    )
    
    # Initialize warehouse system
    from app.models.warehouse_system import WarehouseSystem
    app.warehouse_system = WarehouseSystem()
    
    # Register blueprints
    from app.routes import warehouse, line, package, pallet, dashboard
    app.register_blueprint(warehouse.bp)
    app.register_blueprint(line.bp)
    app.register_blueprint(package.bp)
    app.register_blueprint(pallet.bp)
    app.register_blueprint(dashboard.bp)
    
    @app.route('/')
    def index():
        return dashboard.index()
    
    return app