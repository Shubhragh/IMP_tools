import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import io
import base64
from datetime import datetime
import json

# Import all solvers
from solvers.finite_well import FiniteWellSolver
from solvers.harmonic import HarmonicOscillatorSolver
from solvers.hydrogen import HydrogenAtomSolver
from solvers.tunneling import TunnelingSolver
from solvers.particle_box import ParticleBoxSolver

app = Flask(__name__)
app.secret_key = 'quantum_mechanics_solver_2024'

# Available solvers registry
SOLVERS = {
    'finite_well': {
        'name': 'Finite Square Well',
        'description': 'Bound states in a finite potential well',
        'class': FiniteWellSolver,
        'icon': '🏗️',
        'difficulty': 'Intermediate',
        'category': 'Potential Wells'
    },
    'harmonic': {
        'name': 'Quantum Harmonic Oscillator',
        'description': 'Energy levels of harmonic oscillator',
        'class': HarmonicOscillatorSolver,
        'icon': '🌊',
        'difficulty': 'Beginner',
        'category': 'Oscillators'
    },
    'hydrogen': {
        'name': 'Hydrogen Atom',
        'description': 'Electronic states of hydrogen atom',
        'class': HydrogenAtomSolver,
        'icon': '⚛️',
        'difficulty': 'Advanced',
        'category': 'Atomic Physics'
    },
    'tunneling': {
        'name': 'Quantum Tunneling',
        'description': 'Transmission through potential barriers',
        'class': TunnelingSolver,
        'icon': '🚇',
        'difficulty': 'Intermediate',
        'category': 'Transport'
    },
    'particle_box': {
        'name': 'Particle in a Box',
        'description': 'Infinite square well solutions',
        'class': ParticleBoxSolver,
        'icon': '📦',
        'difficulty': 'Beginner',
        'category': 'Potential Wells'
    }
}

@app.route('/')
def index():
    return render_template('index.html', solvers=SOLVERS)

@app.route('/solver/<solver_id>')
def solver_page(solver_id):
    if solver_id not in SOLVERS:
        return render_template('404.html'), 404
    
    solver_info = SOLVERS[solver_id]
    solver_instance = solver_info['class']()
    
    return render_template('solver.html', 
                         solver_id=solver_id,
                         solver_info=solver_info,
                         parameters=solver_instance.get_parameters(),
                         examples=solver_instance.get_examples())

@app.route('/api/solve/<solver_id>', methods=['POST'])
def solve_problem(solver_id):
    try:
        if solver_id not in SOLVERS:
            return jsonify({'error': 'Invalid solver'}), 400
        
        # Get parameters from request
        params = request.json
        
        # Create solver instance and solve
        solver_class = SOLVERS[solver_id]['class']
        solver = solver_class()
        
        # Validate parameters
        validation = solver.validate_parameters(params)
        if not validation['valid']:
            return jsonify({'error': validation['message']}), 400
        
        # Solve the problem
        results = solver.solve(params)
        
        # Generate plot
        plot_data = solver.generate_plot(params, results)
        
        return jsonify({
            'success': True,
            'results': results,
            'plot': plot_data,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/example/<solver_id>/<example_id>')
def get_example(solver_id, example_id):
    try:
        if solver_id not in SOLVERS:
            return jsonify({'error': 'Invalid solver'}), 400
        
        solver_class = SOLVERS[solver_id]['class']
        solver = solver_class()
        examples = solver.get_examples()
        
        if example_id not in examples:
            return jsonify({'error': 'Invalid example'}), 400
        
        return jsonify(examples[example_id])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
