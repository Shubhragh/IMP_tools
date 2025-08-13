# Quantum Mechanics Solver Suite

A comprehensive web-based toolkit for solving quantum mechanical problems with interactive visualizations and professional results display.

## Features

### 🧮 Multiple Solvers
- **Finite Square Well**: Bound state energies and wavefunctions
- **Quantum Harmonic Oscillator**: Energy levels and probability densities  
- **Hydrogen Atom**: Electronic states and orbital properties
- **Quantum Tunneling**: Transmission and reflection coefficients
- **Particle in a Box**: Infinite well solutions

### 🎨 Professional Interface
- Modern responsive web design
- Interactive parameter input with validation
- Real-time visualization with matplotlib
- Mathematical notation with MathJax
- Export functionality for results and plots

### 🔧 Advanced Features
- Parameter validation and error handling
- Example problem presets
- Keyboard shortcuts (Ctrl+Enter to solve)
- Progress indicators and notifications
- Mobile-responsive design

## Installation

1. **Clone the repository:**
git clone <repository-url>
cd quantum_solver_suite

2. **Create virtual environment:**
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

3. **Install dependencies:**
pip install -r requirements.txt

4. **Run the application:**
python app.py

5. **Open browser:**
Navigate to `http://localhost:5000`

## Usage

### Web Interface
1. Select a solver from the homepage
2. Enter parameters or choose an example
3. Click "Solve" to calculate results
4. View interactive plots and detailed results
5. Export results if needed

### API Usage
The application also provides REST API endpoints:

Solve a problem
POST /api/solve/<solver_id>
Content-Type: application/json

{
"parameter1": value1,
"parameter2": value2
}

Get example parameters
GET /api/example/<solver_id>/<example_id>

## Solver Details

### Finite Square Well
- Solves transcendental equation: tan(za) = 2√((z₀/z)² - 1) / (2 - (z₀/z)²)
- Finds bound state energies using Newton's method
- Visualizes energy levels and wavefunctions

### Quantum Harmonic Oscillator  
- Energy levels: E_n = ℏω(n + 1/2)
- Hermite polynomials for wavefunctions
- Classical vs quantum probability distributions

### Hydrogen Atom
- Energy levels: E_n = -Ry Z²/n²
- Orbital classifications (1s, 2s, 2p, etc.)
- Radial wavefunctions with Laguerre polynomials

### Quantum Tunneling
- Transmission coefficients through barriers
- Both tunneling (E < V₀) and over-barrier (E > V₀) cases
- Wavefunction visualization

### Particle in a Box
- Energy levels: E_n = n²π²ℏ²/(2mL²)
- Sine wave solutions
- Quantum vs classical probability comparison

## Project Structure

quantum_solver_suite/
├── app.py # Main Flask application
├── solvers/ # Solver modules
│ ├── init.py # Base solver class
│ ├── finite_well.py # Finite square well
│ ├── harmonic.py # Harmonic oscillator
│ ├── hydrogen.py # Hydrogen atom
│ ├── tunneling.py # Quantum tunneling
│ └── particle_box.py # Particle in box
├── templates/ # HTML templates
│ ├── base.html # Base template
│ ├── index.html # Homepage
│ └── solver.html # Solver page
├── static/ # Static assets
│ ├── css/
│ │ └── style.css # Custom styles
│ └── js/
│ └── app.js # JavaScript application
├── requirements.txt # Python dependencies
└── README.md # This file

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add new solver in `solvers/` directory
4. Register solver in `app.py` SOLVERS dictionary
5. Test thoroughly
6. Submit pull request

## Adding New Solvers

To add a new quantum mechanics solver:

1. Create new file in `solvers/new_solver.py`
2. Inherit from `BaseSolver` class
3. Implement required methods:
   - `get_parameters()`: Define input parameters
   - `validate_parameters()`: Validate inputs
   - `solve()`: Main calculation logic
   - `generate_plot()`: Create visualization
   - `get_examples()`: Provide example problems

4. Register in `app.py`:
SOLVERS['new_solver'] = {
'name': 'New Solver',
'description': 'Description of the solver',
'class': NewSolverClass,
'icon': '🔬',
'difficulty': 'Intermediate',
'category': 'Category Name'
}

text

## License

This project is open source and available under the MIT License.

## Support

For questions, issues, or contributions, please create an issue on the repository.