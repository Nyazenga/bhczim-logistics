from datetime import datetime

class LogisticsManager:
    """Manager class to handle logistics operations"""
    
    def __init__(self):
        """Initialize the logistics manager"""
        self.warehouses = []
        self.packages = []
        self.pallets = []
        self.offload_order = "oldest_first"  # Default offload order
    
    def add_warehouse(self, warehouse):
        """
        Add a warehouse to the system
        
        Args:
            warehouse: A Warehouse object to add
            
        Returns:
            bool: True if added successfully
        """
        self.warehouses.append(warehouse)
        return True
    
    def remove_warehouse(self, warehouse):
        """
        Remove a warehouse from the system
        
        Args:
            warehouse: The Warehouse object to remove
            
        Returns:
            bool: True if removed successfully, False if not found
        """
        if warehouse in self.warehouses:
            self.warehouses.remove(warehouse)
            return True
        return False
    
    def register_package(self, package):
        """
        Register a package in the system
        
        Args:
            package: A Package object to register
            
        Returns:
            bool: True if registered successfully
        """
        self.packages.append(package)
        return True
    
    def register_pallet(self, pallet):
        """
        Register a pallet in the system
        
        Args:
            pallet: A Pallet object to register
            
        Returns:
            bool: True if registered successfully
        """
        self.pallets.append(pallet)
        return True
    
    def load_package_to_line(self, package, line):
        """
        Load a package to a line
        
        Args:
            package: The Package object to load
            line: The Line object to load the package to
            
        Returns:
            bool: True if loaded successfully, False otherwise
        """
        # Register package if not registered
        if package not in self.packages:
            self.register_package(package)
        
        # Load package based on type
        try:
            if package.package_type == "carton":
                return line.add_carton(package)
            else:
                return False  # Loose packages must be loaded to pallets first
        except ValueError as e:
            print(f"Error loading package: {e}")
            return False
    
    def load_package_to_pallet(self, package, pallet):
        """
        Load a loose package to a pallet
        
        Args:
            package: The LoosePackage object to load
            pallet: The Pallet object to load the package to
            
        Returns:
            bool: True if loaded successfully, False otherwise
        """
        # Register package if not registered
        if package not in self.packages:
            self.register_package(package)
        
        # Register pallet if not registered
        if pallet not in self.pallets:
            self.register_pallet(pallet)
        
        try:
            return pallet.add_package(package)
        except ValueError as e:
            print(f"Error loading package to pallet: {e}")
            return False
    
    def load_pallet_to_line(self, pallet, line):
        """
        Load a pallet to a line
        
        Args:
            pallet: The Pallet object to load
            line: The Line object to load the pallet to
            
        Returns:
            bool: True if loaded successfully, False otherwise
        """
        # Register pallet if not registered
        if pallet not in self.pallets:
            self.register_pallet(pallet)
        
        try:
            return line.add_pallet(pallet)
        except ValueError as e:
            print(f"Error loading pallet to line: {e}")
            return False
    
    def offload_package(self, package):
        """
        Offload a package from its current location
        
        Args:
            package: The Package object to offload
            
        Returns:
            bool: True if offloaded successfully, False otherwise
        """
        if package.location:
            if package.package_type == "carton":
                return package.location.remove_carton(package)
            else:
                # For loose packages, we need to remove from pallet
                if package.pallet:
                    return package.pallet.remove_package(package)
        return False
    
    def offload_pallet(self, pallet):
        """
        Offload a pallet from its current location
        
        Args:
            pallet: The Pallet object to offload
            
        Returns:
            bool: True if offloaded successfully, False otherwise
        """
        if pallet.location:
            return pallet.location.remove_pallet(pallet)
        return False
    
    def discard_package(self, package):
        """
        Discard a package (mark as bad)
        
        Args:
            package: The Package object to discard
            
        Returns:
            bool: True if discarded successfully
        """
        package.discard()
        return True
    
    def set_offload_order(self, order):
        """
        Set the order of offloading packages
        
        Args:
            order (str): Either "oldest_first" or "newest_first"
            
        Returns:
            bool: True if set successfully, False if invalid order
        """
        if order in ["oldest_first", "newest_first"]:
            self.offload_order = order
            return True
        return False
    
    def get_packages_for_offloading(self, location):
        """
        Get packages for offloading based on current order setting
        
        Args:
            location: The location (Line or Warehouse) to get packages from
            
        Returns:
            list: Ordered list of packages for offloading
        """
        packages = []
        
        if hasattr(location, 'get_all_packages'):
            # For warehouses
            packages = location.get_all_packages()
        elif hasattr(location, 'packages'):
            # For lines with direct packages (cartons)
            packages.extend(location.packages)
            
            # For lines with pallets
            for pallet in location.pallets:
                packages.extend(pallet.packages)
        
        # Sort packages based on offload order
        if self.offload_order == "oldest_first":
            packages.sort(key=lambda p: p.created_at)
        else:  # newest_first
            packages.sort(key=lambda p: p.created_at, reverse=True)
        
        return packages
    
    def approve_mixed_quality_line(self, line, max_types=3):
        """
        Approve a line for mixed quality packages
        
        Args:
            line: The Line object to approve for mixed quality
            max_types (int): Maximum number of different quality types allowed
            
        Returns:
            bool: True if approved successfully
        """
        return line.set_mixed_quality_approval(True, max_types)
    
    def get_package_history(self, line):
        """
        Get the history of all packages ever placed in a line
        
        Args:
            line: The Line object to get history for
            
        Returns:
            list: Package history
        """
        return line.get_package_history()
    
    def get_warehouse_snapshot(self, warehouse):
        """
        Get a snapshot of a warehouse
        
        Args:
            warehouse: The Warehouse object to get snapshot for
            
        Returns:
            dict: Warehouse snapshot
        """
        return warehouse.get_snapshot()
    
    def search_package(self, serial_number):
        """
        Search for a package by its serial number
        
        Args:
            serial_number (str): Serial number to search for
            
        Returns:
            dict: Package information if found, None otherwise
        """
        for warehouse in self.warehouses:
            result = warehouse.search_package(serial_number)
            if result:
                return result
        return None
    
    def search_pallet(self, serial_number):
        """
        Search for a pallet by its serial number
        
        Args:
            serial_number (str): Serial number to search for
            
        Returns:
            dict: Pallet information if found, None otherwise
        """
        for warehouse in self.warehouses:
            result = warehouse.search_pallet(serial_number)
            if result:
                return result
        return None
    
    def get_all_warehouses(self):
        """
        Get all warehouses in the system
        
        Returns:
            list: All warehouses
        """
        return self.warehouses