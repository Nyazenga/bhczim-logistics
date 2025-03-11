import uuid
from datetime import datetime

class Line:
    """Storage line within a warehouse rack"""
    
    def __init__(self, line_number, max_capacity, capacity_type="weight", max_quality_types=1, serial_number=None):
        """
        Initialize a storage line
        
        Args:
            line_number (int): Line identifier number
            max_capacity (float/int): Maximum capacity (in kg for loose packages, count for cartons)
            capacity_type (str): Either "weight" for loose packages or "count" for cartons
            max_quality_types (int): Maximum number of different quality types allowed (default 1)
            serial_number (str, optional): Unique serial number for the line
        """
        self.serial_number = serial_number or str(uuid.uuid4())
        self.line_number = line_number
        self.max_capacity = max_capacity
        self.capacity_type = capacity_type  # "weight" or "count"
        self.max_quality_types = max_quality_types
        self.packages = []  # For cartons
        self.pallets = []   # For loose packages
        self.package_history = []  # All packages ever placed in this line
        self.mixed_quality_approved = max_quality_types > 1
        self.warehouse = None  # Will be set when assigned to a warehouse
    
    @property
    def current_capacity_usage(self):
        """Calculate current capacity usage based on type"""
        if self.capacity_type == "count":
            return len(self.packages)
        else:  # weight
            total = sum(pallet.total_mass for pallet in self.pallets)
            return total
    
    @property
    def available_capacity(self):
        """Calculate available capacity"""
        return self.max_capacity - self.current_capacity_usage
    
    @property
    def is_mixed(self):
        """Check if line contains mixed quality packages"""
        return len(self.quality_marks) > 1
    
    @property
    def quality_marks(self):
        """Get all unique quality marks in this line"""
        if self.capacity_type == "count":
            return set(package.quality_mark for package in self.packages)
        else:
            return set(pallet.quality_mark for pallet in self.pallets)
    
    @property
    def line_type(self):
        """Return the type of packages this line holds"""
        if self.capacity_type == "count":
            return "cartons"
        else:
            return "loose packages"
    
    def can_add_quality(self, quality_mark):
        """
        Check if a new quality mark can be added to this line
        
        Args:
            quality_mark (str): The quality mark to check
            
        Returns:
            bool: True if quality can be added, False otherwise
        """
        # If quality already exists in the line
        if quality_mark in self.quality_marks:
            return True
            
        # If this would exceed max allowed quality types
        if len(self.quality_marks) >= self.max_quality_types:
            return False
            
        # If this would mix qualities but it's not approved
        if len(self.quality_marks) > 0 and not self.mixed_quality_approved:
            return False
            
        return True
    
    def add_carton(self, carton):
        """
        Add a carton package directly to the line
        
        Args:
            carton: A Carton object to add to the line
            
        Returns:
            bool: True if added successfully, False otherwise
        """
        # Check if line is for cartons
        if self.capacity_type != "count":
            raise ValueError("This line is for loose packages (pallets), not cartons")
        
        # Check capacity
        if self.current_capacity_usage >= self.max_capacity:
            return False
        
        # Check quality compatibility
        if not self.can_add_quality(carton.quality_mark):
            return False
        
        # Add carton to line
        self.packages.append(carton)
        carton.assign_location(self)
        self.package_history.append({
            "package": carton,
            "action": "added",
            "timestamp": datetime.now()
        })
        return True
    
    def add_pallet(self, pallet):
        """
        Add a pallet of loose packages to the line
        
        Args:
            pallet: A Pallet object to add to the line
            
        Returns:
            bool: True if added successfully, False otherwise
        """
        # Check if line is for loose packages
        if self.capacity_type != "weight":
            raise ValueError("This line is for cartons, not loose packages (pallets)")
        
        # Check capacity
        if self.current_capacity_usage + pallet.total_mass > self.max_capacity:
            return False
        
        # Check quality compatibility
        if not self.can_add_quality(pallet.quality_mark):
            return False
        
        # Add pallet to line
        self.pallets.append(pallet)
        pallet.assign_location(self)
        
        # Add all packages in pallet to history
        for package in pallet.packages:
            self.package_history.append({
                "package": package,
                "action": "added",
                "timestamp": datetime.now()
            })
        
        return True
    
    def remove_carton(self, carton):
        """
        Remove a carton from the line
        
        Args:
            carton: The carton to remove
            
        Returns:
            bool: True if removed successfully, False if carton not found
        """
        if carton in self.packages:
            self.packages.remove(carton)
            carton.location = None
            self.package_history.append({
                "package": carton,
                "action": "removed",
                "timestamp": datetime.now()
            })
            return True
        return False
    
    def remove_pallet(self, pallet):
        """
        Remove a pallet from the line
        
        Args:
            pallet: The pallet to remove
            
        Returns:
            bool: True if removed successfully, False if pallet not found
        """
        if pallet in self.pallets:
            self.pallets.remove(pallet)
            pallet.location = None
            
            # Record removal of all packages in pallet
            for package in pallet.packages:
                self.package_history.append({
                    "package": package,
                    "action": "removed",
                    "timestamp": datetime.now()
                })
            
            return True
        return False
    
    def set_mixed_quality_approval(self, approved, max_types=3):
        """
        Set approval for mixed quality packages on this line
        
        Args:
            approved (bool): Whether mixed quality is approved
            max_types (int): Maximum number of different quality types (default 3)
        """
        self.mixed_quality_approved = approved
        self.max_quality_types = max_types if approved else 1
        return True
    
    def get_package_history(self):
        """
        Get the history of all packages ever placed in this line
        
        Returns:
            list: List of all package history entries
        """
        return self.package_history
    
    def __str__(self):
        return f"Line({self.line_number}, Type: {self.line_type}, Usage: {self.current_capacity_usage}/{self.max_capacity})"