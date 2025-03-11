import uuid
from datetime import datetime

class Pallet:
    """Pallet to hold loose packages of the same quality"""
    
    def __init__(self, quality_mark, max_capacity, serial_number=None, created_at=None):
        """
        Initialize a pallet
        
        Args:
            quality_mark (str): Quality mark that the pallet will hold
            max_capacity (int): Maximum number of packages the pallet can hold
            serial_number (str, optional): Unique serial number for the pallet
            created_at (datetime, optional): Creation timestamp
        """
        self.serial_number = serial_number or str(uuid.uuid4())
        self.quality_mark = quality_mark
        self.max_capacity = max_capacity
        self.created_at = created_at or datetime.now()
        self.packages = []
        self.location = None  # Will be set when assigned to a location
    
    @property
    def current_count(self):
        """Get the current number of packages in the pallet"""
        return len(self.packages)
    
    @property
    def available_capacity(self):
        """Get the remaining capacity of the pallet"""
        return self.max_capacity - self.current_count
    
    @property
    def total_mass(self):
        """Calculate the total mass of all packages in the pallet"""
        return sum(package.mass for package in self.packages)
    
    def add_package(self, package):
        """
        Add a loose package to the pallet
        
        Args:
            package: A LoosePackage object to add to the pallet
            
        Returns:
            bool: True if added successfully, False otherwise
        """
        # Check if package is loose and of the same quality
        if package.package_type != "loose":
            raise ValueError("Only loose packages can be added to pallets")
        
        if package.quality_mark != self.quality_mark:
            raise ValueError(f"Package quality ({package.quality_mark}) does not match pallet quality ({self.quality_mark})")
        
        # Check if pallet has space
        if self.current_count >= self.max_capacity:
            return False
        
        # Add package to pallet and update package's pallet reference
        self.packages.append(package)
        package.pallet = self
        return True
    
    def remove_package(self, package):
        """
        Remove a package from the pallet
        
        Args:
            package: The package to remove
            
        Returns:
            bool: True if removed successfully, False if package not found
        """
        if package in self.packages:
            self.packages.remove(package)
            package.pallet = None
            return True
        return False
    
    def assign_location(self, location):
        """
        Assign pallet to a location
        
        Args:
            location: The line object where the pallet will be stored
        """
        # If pallet is already in a location, remove it first
        if self.location:
            self.location.remove_pallet(self)
        
        self.location = location
        return True
    
    def __str__(self):
        return f"Pallet({self.serial_number}, Quality: {self.quality_mark}, Packages: {self.current_count}/{self.max_capacity})"