import uuid
from datetime import datetime

class Warehouse:
    """Warehouse to store lines of packages"""
    
    def __init__(self, name, max_capacity, serial_number=None):
        """
        Initialize a warehouse
        
        Args:
            name (str): Name of the warehouse for identification
            max_capacity (float): Maximum weight capacity in kg
            serial_number (str, optional): Unique serial number for the warehouse
        """
        self.serial_number = serial_number or str(uuid.uuid4())
        self.name = name
        self.max_capacity = max_capacity
        self.lines = []  # List of storage lines
        self.created_at = datetime.now()
    
    @property
    def current_capacity_usage(self):
        """Calculate current weight capacity usage"""
        total = 0
        for line in self.lines:
            total += line.current_capacity_usage
        return total
    
    @property
    def available_capacity(self):
        """Calculate available capacity"""
        return self.max_capacity - self.current_capacity_usage
    
    @property
    def capacity_utilization_percentage(self):
        """Calculate capacity utilization as a percentage"""
        if self.max_capacity == 0:
            return 0
        return (self.current_capacity_usage / self.max_capacity) * 100
    
    def add_line(self, line):
        """
        Add a storage line to the warehouse
        
        Args:
            line: A Line object to add to the warehouse
            
        Returns:
            bool: True if added successfully, False otherwise
        """
        # Set warehouse reference for the line
        line.warehouse = self
        self.lines.append(line)
        return True
    
    def remove_line(self, line):
        """
        Remove a line from the warehouse
        
        Args:
            line: The line to remove
            
        Returns:
            bool: True if removed successfully, False if line not found
        """
        if line in self.lines:
            self.lines.remove(line)
            line.warehouse = None
            return True
        return False
    
    def get_all_packages(self):
        """
        Get all packages currently stored in the warehouse
        
        Returns:
            list: All packages in the warehouse
        """
        all_packages = []
        
        for line in self.lines:
            # Add direct packages (cartons)
            all_packages.extend(line.packages)
            
            # Add packages in pallets
            for pallet in line.pallets:
                all_packages.extend(pallet.packages)
        
        return all_packages
    
    def get_snapshot(self):
        """
        Get a snapshot of the warehouse showing all packages and their locations
        
        Returns:
            dict: Warehouse snapshot with packages and statistics
        """
        snapshot = {
            "warehouse_name": self.name,
            "capacity_usage": self.current_capacity_usage,
            "max_capacity": self.max_capacity,
            "utilization_percentage": self.capacity_utilization_percentage,
            "lines": [],
            "total_packages": 0
        }
        
        for line in self.lines:
            line_data = {
                "line_number": line.line_number,
                "capacity_usage": line.current_capacity_usage,
                "max_capacity": line.max_capacity,
                "line_type": line.line_type,
                "packages": []
            }
            
            # Add cartons
            for package in line.packages:
                line_data["packages"].append({
                    "serial_number": package.serial_number,
                    "quality_mark": package.quality_mark,
                    "mass": package.mass,
                    "type": "carton",
                    "created_at": package.created_at.isoformat()
                })
            
            # Add pallets with loose packages
            for pallet in line.pallets:
                pallet_data = {
                    "serial_number": pallet.serial_number,
                    "quality_mark": pallet.quality_mark,
                    "package_count": pallet.current_count,
                    "max_capacity": pallet.max_capacity,
                    "total_mass": pallet.total_mass,
                    "packages": []
                }
                
                for package in pallet.packages:
                    pallet_data["packages"].append({
                        "serial_number": package.serial_number,
                        "quality_mark": package.quality_mark,
                        "mass": package.mass,
                        "created_at": package.created_at.isoformat()
                    })
                
                line_data["pallets"] = pallet_data
                line_data["packages"].extend(pallet_data["packages"])
            
            snapshot["lines"].append(line_data)
            snapshot["total_packages"] += len(line_data["packages"])
        
        return snapshot
    
    def search_package(self, serial_number):
        """
        Search for a package by its serial number
        
        Args:
            serial_number (str): The serial number to search for
            
        Returns:
            dict: Package information with location if found, None otherwise
        """
        for line in self.lines:
            # Search among cartons
            for package in line.packages:
                if package.serial_number == serial_number:
                    return {
                        "package": package,
                        "line_number": line.line_number,
                        "warehouse_name": self.name,
                        "type": "carton",
                        "pallet": None
                    }
            
            # Search among loose packages in pallets
            for pallet in line.pallets:
                for package in pallet.packages:
                    if package.serial_number == serial_number:
                        return {
                            "package": package,
                            "line_number": line.line_number,
                            "warehouse_name": self.name,
                            "type": "loose",
                            "pallet": pallet
                        }
        
        return None
    
    def search_pallet(self, serial_number):
        """
        Search for a pallet by its serial number
        
        Args:
            serial_number (str): The serial number to search for
            
        Returns:
            dict: Pallet information with location if found, None otherwise
        """
        for line in self.lines:
            for pallet in line.pallets:
                if pallet.serial_number == serial_number:
                    return {
                        "pallet": pallet,
                        "line_number": line.line_number,
                        "warehouse_name": self.name,
                        "packages": pallet.packages
                    }
        
        return None
    
    def __str__(self):
        return f"Warehouse({self.name}, Capacity: {self.current_capacity_usage}/{self.max_capacity}kg, Lines: {len(self.lines)})"