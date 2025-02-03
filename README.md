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

![image](https://github.com/user-attachments/assets/b5dee768-e177-400e-9b01-c60b5a6d6cdf) ![image](https://github.com/user-attachments/assets/c40ba4f6-9e6e-4017-946a-55153d483e10)
![image](https://github.com/user-attachments/assets/ec67666c-071c-479f-99a5-31e6c874e184) ![image](https://github.com/user-attachments/assets/37fc10c1-7d6c-4894-a3b8-cf23a5c1eb1c)
![image](https://github.com/user-attachments/assets/3099cf88-1951-4a4c-93c5-9a4f0d29ec66)


## 📧 Contact

For support or queries, please open an issue in the repository.

---
**Note**: This system is designed for enterprise-level warehouse operations and requires proper configuration of all dependencies for optimal performance.
