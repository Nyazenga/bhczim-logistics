# Company X Logistics Management System

## Overview

This project is a **Logistics Management System** designed for Company X, which handles the storage and logistics of packages in warehouses. The system automates operations such as loading and offloading packages, managing warehouse capacities, and tracking package locations. It provides a user-friendly web interface built with **Python Flask** and modern front-end technologies like **Bootstrap** and **JavaScript**.

The system is designed to:
- Manage warehouses, lines, pallets, and packages
- Allow loading packages into pallets and lines
- Approve lines for mixed quality packages
- Provide real-time snapshots of warehouse utilization

This project was developed by **Munashe Nyazenga**. You can contact me at **+263782794721** or check out my other projects on my portfolio: [https://munashe.netlify.app/#portfolio](https://munashe.netlify.app/#portfolio).

## Table of Contents

1. [Technologies Used](#technologies-used)
2. [Data Structures](#data-structures)
3. [Why an Interface Instead of Console?](#why-an-interface-instead-of-console)
4. [Installation](#installation)
5. [Testing the System](#testing-the-system)
6. [Attribution](#attribution)

## Technologies Used

### Backend
- **Python Flask**: A lightweight web framework used to build the backend of the application. Flask was chosen for its simplicity and flexibility.
- **JSON**: Used for data serialization and storage.

### Frontend
- **HTML/CSS/JavaScript**: For building the user interface.
- **Bootstrap**: A CSS framework used to create a modern, responsive, and mobile-friendly design.
- **DataTables**: A jQuery plugin used to display tabular data with sorting, searching, and pagination.
- **SweetAlert2**: A JavaScript library used for displaying beautiful and customizable alerts.

### Development Tools
- **Git**: For version control.
- **VS Code**: The code editor used for development.

## Data Structures

The system uses the following **Object-Oriented Programming (OOP)** data structures:

1. **Package** (Class):
   - Implemented using Python classes with instance attributes
   - Uses dictionaries to store package properties
   - Represents a package with attributes like `serial_number`, `quality_mark`, `mass`, and `package_type` (loose or carton)
   - Methods include `discard()` and `assign_location()`

2. **Pallet** (Class):
   - Implemented as a container class
   - Uses lists to maintain a collection of Package objects
   - Uses dictionary for property storage
   - Represents a pallet that can hold loose packages of the same quality
   - Attributes include `serial_number`, `quality_mark`, and `max_capacity`
   - Methods include `add_package()` and `remove_package()`

3. **Line** (Class):
   - Composite data structure that contains Pallet objects and Carton objects
   - Uses dictionaries for property storage and lists for collections
   - Represents a storage line in a warehouse
   - Attributes include `line_number`, `max_capacity`, and `capacity_type` (weight or count)
   - Methods include `add_pallet()`, `add_carton()`, and `set_mixed_quality_approval()`

4. **Warehouse** (Class):
   - Tree-like structure where the Warehouse is the root and Lines are nodes
   - Uses dictionaries for property storage and lists for the line collection
   - Represents a warehouse that contains multiple lines
   - Attributes include `name`, `max_capacity`, and `lines`
   - Methods include `add_line()` and `get_snapshot()`

5. **LogisticsManager** (Singleton Class):
   - Implements the Singleton design pattern to ensure only one instance exists
   - Uses dictionaries to track all system entities
   - Uses queues for order processing (FIFO/LIFO depending on configuration)
   - Manages all operations, including loading, offloading, and approving mixed quality lines
   - Acts as the central controller for the system

## Why an Interface Instead of Console?

We chose to build a **web interface** instead of a console-based system for the following reasons:
1. **User-Friendly**: A web interface is more intuitive and easier to use for non-technical users.
2. **Real-Time Feedback**: Users can see changes and results immediately without running commands.
3. **Scalability**: A web interface can be easily extended with new features and accessed from anywhere.
4. **Modern Experience**: A responsive and animated interface provides a better user experience compared to a console.

## Installation

Follow these steps to set up the project on your local machine:

### Prerequisites
- **Python 3.8 or higher**: Download and install Python from [python.org](https://www.python.org/).
- **Git**: Download and install Git from [git-scm.com](https://git-scm.com/).

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Nyazenga/bhczim-logistics.git
   cd bhczim-logistics
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**:
   ```bash
   python run.py
   ```

6. **Access the Application**:
   - Open your browser and go to http://localhost:5000.

## Testing the System

Follow these steps to test the system and verify that everything works as expected:

### Step 1: Create a Warehouse
1. Go to the Warehouses page.
2. Click Create New Warehouse.
3. Fill in the form:
   - Warehouse Name: Main Warehouse
   - Maximum Capacity (kg): 10000
4. Click Create Warehouse.
5. Verify that the warehouse appears in the list.

### Step 2: Create a Line
1. Go to the Lines page.
2. Click Create New Line.
3. Fill in the form:
   - Line Number: 1
   - Maximum Capacity: 1000
   - Capacity Type: Select Weight (kg).
   - Warehouse: Select Main Warehouse.
4. Click Create Line.
5. Verify that the line appears in the list.

### Step 3: Create a Pallet
1. Go to the Pallets page.
2. Click Create New Pallet.
3. Fill in the form:
   - Quality Mark: A1
   - Maximum Capacity (packages): 20
4. Click Create Pallet.
5. Verify that the pallet appears in the list.

### Step 4: Create a Loose Package
1. Go to the Packages page.
2. Click Create New Package.
3. Fill in the form:
   - Package Type: Select Loose.
   - Quality Mark: A1
   - Mass (kg): 10
4. Click Create Package.
5. Verify that the package appears in the list.

### Step 5: Load the Package to the Pallet
1. On the Packages page, click the Load to Pallet button next to the package.
2. In the modal, enter the pallet's serial number.
3. Click Load.
4. Verify that the package is loaded into the pallet.

### Step 6: Load the Pallet to the Line
1. On the Pallets page, click the Load to Line button next to the pallet.
2. In the modal, enter the line's serial number.
3. Click Load.
4. Verify that the pallet is loaded into the line.

### Step 7: Approve Mixed Quality
1. On the Lines page, click the Approve Mixed button next to the line.
2. In the modal, enter the maximum number of quality types (e.g., 3).
3. Click Approve.
4. Verify that the line is approved for mixed quality packages.

### Step 8: Verify Warehouse Utilization
1. Go to the Warehouses page.
2. Click View next to Main Warehouse.
3. Verify that the warehouse's utilization is updated to reflect the added packages and pallets.

## Attribution

This project was developed by Munashe Nyazenga. You can contact me at +263782794721 or check out my other projects on my portfolio: [https://munashe.netlify.app/#portfolio](https://munashe.netlify.app/#portfolio).

---

Thank you for using the Company X Logistics Management System! If you have any questions or feedback, feel free to reach out.