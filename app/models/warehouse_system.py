import json
import os
import datetime
from app.models.package import Package, LoosePackage, Carton
from app.models.pallet import Pallet
from app.models.line import Line
from app.models.warehouse import Warehouse
from app.models.logistics_manager import LogisticsManager

class WarehouseSystem:
    """Main system class to interact with the logistics system"""
    
    def __init__(self, data_file="warehouse_data.json"):
        """
        Initialize the warehouse system
        
        Args:
            data_file (str): File path to save/load data
        """
        self.manager = LogisticsManager()
        self.data_file = data_file
        self.load_data()
    
    def create_warehouse(self, name, max_capacity):
        """
        Create a new warehouse
        
        Args:
            name (str): Name of the warehouse
            max_capacity (float): Maximum capacity in kg
            
        Returns:
            Warehouse: The created warehouse object
        """
        warehouse = Warehouse(name, max_capacity)
        self.manager.add_warehouse(warehouse)
        self.save_data()
        return warehouse
    
    def create_line(self, line_number, max_capacity, capacity_type="weight"):
        """
        Create a new storage line
        
        Args:
            line_number (int): Line identifier number
            max_capacity (float/int): Maximum capacity
            capacity_type (str): Either "weight" for loose packages or "count" for cartons
            
        Returns:
            Line: The created line object
        """
        line = Line(line_number, max_capacity, capacity_type)
        self.save_data()
        return line
    
    def add_line_to_warehouse(self, line, warehouse):
        """
        Add a line to a warehouse
        
        Args:
            line: The Line object to add
            warehouse: The Warehouse object to add the line to
            
        Returns:
            bool: True if added successfully
        """
        result = warehouse.add_line(line)
        self.save_data()
        return
    
    def create_package(self, package_type, quality_mark, mass):
            """
            Create a new package
            
            Args:
                package_type (str): Either "loose" or "carton"
                quality_mark (str): Quality indicator of the package
                mass (float): Weight of the package in kg
                
            Returns:
                Package: The created package object
            """
            if package_type == "loose":
                package = LoosePackage(quality_mark, mass)
            else:
                package = Carton(quality_mark, mass)
            
            self.manager.register_package(package)
            self.save_data()
            return package
        
    def create_pallet(self, quality_mark, max_capacity):
        """
        Create a new pallet
        
        Args:
            quality_mark (str): Quality mark that the pallet will hold
            max_capacity (int): Maximum number of packages the pallet can hold
            
        Returns:
            Pallet: The created pallet object
        """
        pallet = Pallet(quality_mark, max_capacity)
        self.manager.register_pallet(pallet)
        self.save_data()
        return pallet

    def load_package_to_pallet(self, package, pallet):
        """
        Load a package to a pallet
        
        Args:
            package: The package object to load
            pallet: The pallet object to load the package to
            
        Returns:
            bool: True if loaded successfully
        """
        result = self.manager.load_package_to_pallet(package, pallet)
        self.save_data()
        return result

    def load_pallet_to_line(self, pallet, line):
        """
        Load a pallet to a line
        
        Args:
            pallet: The pallet object to load
            line: The line object to load the pallet to
            
        Returns:
            bool: True if loaded successfully
        """
        result = self.manager.load_pallet_to_line(pallet, line)
        self.save_data()
        return result

    def load_carton_to_line(self, carton, line):
        """
        Load a carton directly to a line
        
        Args:
            carton: The carton object to load
            line: The line object to load the carton to
            
        Returns:
            bool: True if loaded successfully
        """
        result = self.manager.load_package_to_line(carton, line)
        self.save_data()
        return result

    def offload_package(self, package):
        """
        Offload a package from its current location
        
        Args:
            package: The package to offload
            
        Returns:
            bool: True if offloaded successfully
        """
        result = self.manager.offload_package(package)
        self.save_data()
        return result

    def offload_pallet(self, pallet):
        """
        Offload a pallet from its current location
        
        Args:
            pallet: The pallet to offload
            
        Returns:
            bool: True if offloaded successfully
        """
        result = self.manager.offload_pallet(pallet)
        self.save_data()
        return result

    def discard_package(self, package):
        """
        Discard a package (mark as bad)
        
        Args:
            package: The package to discard
            
        Returns:
            bool: True if discarded successfully
        """
        result = self.manager.discard_package(package)
        self.save_data()
        return result

    def set_offload_order(self, order):
        """
        Set package offloading order
        
        Args:
            order (str): Either "oldest_first" or "newest_first"
            
        Returns:
            bool: True if set successfully
        """
        result = self.manager.set_offload_order(order)
        self.save_data()
        return result

    def approve_mixed_quality_line(self, line, max_types=3):
        """
        Approve a line for mixed quality packages
        
        Args:
            line: The line to approve
            max_types (int): Maximum number of quality types allowed (default 3)
            
        Returns:
            bool: True if approved successfully
        """
        result = self.manager.approve_mixed_quality_line(line, max_types)
        self.save_data()
        return result

    def get_package_history(self, line):
        """
        Get package history for a line
        
        Args:
            line: The line to get history for
            
        Returns:
            list: Package history
        """
        return self.manager.get_package_history(line)

    def get_warehouse_snapshot(self, warehouse):
        """
        Get a snapshot of a warehouse
        
        Args:
            warehouse: The warehouse to get snapshot for
            
        Returns:
            dict: Warehouse snapshot
        """
        return self.manager.get_warehouse_snapshot(warehouse)

    def search_package(self, serial_number):
        """
        Search for a package by serial number
        
        Args:
            serial_number (str): Serial number to search for
            
        Returns:
            dict: Package information if found
        """
        return self.manager.search_package(serial_number)

    def search_pallet(self, serial_number):
        """
        Search for a pallet by serial number
        
        Args:
            serial_number (str): Serial number to search for
            
        Returns:
            dict: Pallet information if found
        """
        return self.manager.search_pallet(serial_number)

    def get_all_warehouses(self):
        """
        Get all warehouses
        
        Returns:
            list: All warehouses
        """
        return self.manager.get_all_warehouses()

    def save_data(self):
        """Save system data to file"""
        try:
            # This is a placeholder for data serialization
            # In a real system, you would implement proper serialization
            # of complex objects to JSON or use a database
            data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "warehouses_count": len(self.manager.warehouses),
                "packages_count": len(self.manager.packages),
                "pallets_count": len(self.manager.pallets)
            }
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f)
                
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

    def load_data(self):
        """Load system data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    
                # This is a placeholder for data deserialization
                # In a real system, you would implement proper deserialization
                # of complex objects from JSON or use a database
                    
                return True
            return False
        except Exception as e:
            print(f"Error loading data: {e}")
            return False