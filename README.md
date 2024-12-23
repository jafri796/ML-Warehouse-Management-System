# AS/RS Warehouse Management System with Vehicle Loading Optimization

A comprehensive Automated Storage and Retrieval System (AS/RS) that combines warehouse management with intelligent vehicle loading optimization. Built with Python and machine learning algorithms, this system provides an end-to-end solution for warehouse operations and logistics optimization.

## 🚀 Features

### Warehouse Management
- **Dual Category Management**: 
  - Finished/Semi-Finished Products handling
  - Raw Materials and Packaging management
- **Smart Product Placement**: Optimized allocation using machine learning algorithms
- **Dynamic Retrieval System**: Date-based product retrieval with location tracking
- **Customizable Layout**: Adjustable cell dimensions and product limits per cell
- **4D Coordinate System**: Precise product tracking (row, column, shelf level, depth)

### Vehicle Loading Optimization
- **Intelligent Load Planning**: 
  - Volume and weight constraint handling
  - Axle load distribution optimization
- **Multi-dimensional Visualization**:
  - 2D and 3D loading diagrams
  - Interactive placement coordinates
- **Constraint Management**:
  - Real-time weight limit validation
  - Automated excess weight notifications

## 💻 Requirements

### Core Dependencies
- Python with Anaconda environment
- Required Python packages:
  - pyomo
  - tk (tkmacosx for MAC-OS)
  - ortools
  - mayavi
  - sklearn
  - mlxtend

### Additional Software
- GLPK Solver
- CBC Solver
- Python environment managers:
  - Anaconda Navigator
  - Spyder IDE

## 🛠️ Installation

1. **Set up Python Environment**:
```bash
# Install Anaconda first
conda create -n warehouse-env python=3.8
conda activate warehouse-env
```

2. **Install Required Packages**:
```bash
pip install -r requirements.txt
```

3. **Install Solvers**:
- For Windows:
  - Download and install GLPK
  - Download and install CBC
  - Add both to system PATH
- For MacOS:
  - Follow MacOS-specific installation guide in documentation

4. **System Configuration**:
- Set environment variables for solvers
- Configure warehouse layout parameters (default: 290cm cell length, 3 products per cell)

## 📊 Usage

1. **Launch Application**:
```bash
python main.py
```

2. **Warehouse Management**:
- Select product category (Finished/Raw Materials)
- Upload product data in specified Excel format
- Use placement menu for product allocation
- Retrieve products using dispatch date

3. **Vehicle Loading**:
- Enter vehicle constraints (volume, weight limits)
- Upload loading manifest
- View 2D/3D optimization results

## 📋 File Format Requirements

### Product Data Excel Format
- Required columns:
  - Product ID
  - Dimensions
  - Weight
  - Category
  - Dispatch Date

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📧 Contact

For support or queries, please open an issue in the repository.

---
**Note**: This system is designed for enterprise-level warehouse operations and requires proper configuration of all dependencies for optimal performance.
