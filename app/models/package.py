import datetime
import uuid

class Package:
    """Base Package class for all package types"""
    
    def __init__(self, quality_mark, mass, serial_number=None, created_at=None):
        """
        Initialize a package
        
        Args:
            quality_mark (str): Indicator of the package content quality
            mass (float): Weight of the package in kg
            serial_number (str, optional): Unique serial number for the package
            created_at (datetime, optional): Creation timestamp
        """
        self.serial_number = serial_number or str(uuid.uuid4())
        self.quality_mark = quality_mark
        self.mass = mass
        self.created_at = created_at or datetime.datetime.now()
        self.location = None  # Will be set when assigned to a location
        self.discarded = False
    
    def discard(self):
        """Mark package as discarded"""
        self.discarded = True
        if self.location:
            self.location.remove_package(self)
            self.location = None
        return True
    
    def assign_location(self, location):
        """
        Assign package to a location
        
        Args:
            location: The location object where the package will be stored
        """
        # If package is already in a location, remove it first
        if self.location:
            self.location.remove_package(self)
        
        self.location = location
        return True
    
    def __str__(self):
        return f"Package({self.serial_number}, Quality: {self.quality_mark}, Mass: {self.mass}kg)"


class LoosePackage(Package):
    """Class for loose packages that need to be placed in pallets"""
    
    def __init__(self, quality_mark, mass, serial_number=None, created_at=None):
        super().__init__(quality_mark, mass, serial_number, created_at)
        self.package_type = "loose"
        self.pallet = None  # Will be set when assigned to a pallet


class Carton(Package):
    """Class for carton packages that can be placed directly on lines"""
    
    def __init__(self, quality_mark, mass, serial_number=None, created_at=None):
        super().__init__(quality_mark, mass, serial_number, created_at)
        self.package_type = "carton"