from . import BaseSolver
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

class FiniteWellSolver(BaseSolver):
    def __init__(self):
        super().__init__()
        self.name = "Finite Square Well"
        self.description = "Find bound state energy eigenvalues"
    
    def get_parameters(self):
        return {
            'a': {
                'name': 'Well Width (a)',
                'type': 'float',
                'default': 1.0,
                'min': 0.1,
                'max': 10.0,
                'unit': 'length units',
                'description': 'Width of the potential well'
            },
            'V0': {
                'name': 'Well Depth (V₀)',
                'type': 'float', 
                'default': 1.0,
                'min': 0.1,
                'max': 50.0,
                'unit': 'energy units',
                'description': 'Depth of the potential well'
            },
            'm': {
                'name': 'Particle Mass (m)',
                'type': 'float',
                'default': 0.5,
                'min': 0.1,
                'max': 10.0,
                'unit': 'mass units',
                'description': 'Mass of the quantum particle'
            },
            'hbar': {
                'name': 'ℏ (Reduced Planck)',  
                'type': 'float',
                'default': 1.0,
                'min': 0.1,
                'max': 10.0,
                'unit': 'action units',
                'description': 'Reduced Planck constant'
            },
            'precision': {
                'name': 'Decimal Precision',
                'type': 'int',
                'default': 7,
                'min': 3,
                'max': 15,
                'unit': 'digits',
                'description': 'Number of decimal places in results'
            }
        }
    
    def validate_parameters(self, params):
        try:
            a = float(params.get('a', 1.0))
            V0 = float(params.get('V0', 1.0))
            m = float(params.get('m', 0.5))
            hbar = float(params.get('hbar', 1.0))
            precision = int(params.get('precision', 7))
            
            if any(x <= 0 for x in [a, V0, m, hbar]):
                return {'valid': False, 'message': 'All physical parameters must be positive!'}
            
            if precision < 1 or precision > 15:
                return {'valid': False, 'message': 'Precision must be between 1 and 15!'}
                
            return {'valid': True, 'message': 'Parameters valid'}
            
        except (ValueError, TypeError):
            return {'valid': False, 'message': 'Invalid parameter values!'}
    
    def solve(self, params):
        a = float(params['a'])
        V0 = float(params['V0'])
        m = float(params['m'])
        hbar = float(params['hbar'])
        precision = int(params['precision'])
        
        # Calculate z0
        z0 = np.sqrt(2 * m * V0 / hbar**2)
        
        def transcendental_equation(z):
            if z <= 1e-8 or z >= z0 - 1e-8:
                return 1000
            try:
                ratio = z0 / z
                ratio_squared = ratio**2
                if ratio_squared <= 1.01:
                    return 1000
                numerator = 2 * np.sqrt(ratio_squared - 1)
                denominator = 2 - ratio_squared
                if abs(denominator) < 1e-12:
                    return 1000
                rhs = numerator / denominator
                lhs = np.tan(z * a)
                return lhs - rhs
            except:
                return 1000
        
        # Find solutions using multiple starting points
        start_points = np.linspace(0.2, z0 - 0.2, 20)
        solutions = []
        
        for z_start in start_points:
            try:
                z_sol = fsolve(transcendental_equation, z_start)[0]
                if (0.01 < z_sol < z0 - 0.01 and 
                    abs(transcendental_equation(z_sol)) < 1e-10):
                    # Check if new solution
                    is_new = True
                    for existing_z, _ in solutions:
                        if abs(z_sol - existing_z) < 1e-10:
                            is_new = False
                            break
                    if is_new:
                        energy = -(z0**2 - z_sol**2) * hbar**2 / (2 * m)
                        solutions.append((z_sol, energy))
            except:
                continue
        
        # Sort by energy (most bound first)
        solutions.sort(key=lambda x: x[1])
        
        # Format results
        formatted_solutions = []
        for i, (z_val, energy) in enumerate(solutions):
            binding_energy = abs(energy)
            penetration_depth = hbar / np.sqrt(2 * m * binding_energy) if binding_energy > 0 else np.inf
            
            formatted_solutions.append({
                'state_number': i + 1,
                'z_value': round(z_val, precision),
                'energy': round(energy, precision),
                'binding_energy': round(binding_energy, precision),
                'penetration_depth': round(penetration_depth, 3) if penetration_depth != np.inf else 'infinite'
            })
        
        return {
            'system_info': {
                'z0': round(z0, 6),
                'valid_range': f'0 < z < {z0:.6f}',
                'num_bound_states': len(solutions),
                'threshold_condition': f'z₀ = {z0:.3f} {">" if z0 > np.pi/2 else "<"} π/2 = {np.pi/2:.3f}'
            },
            'bound_states': formatted_solutions,
            'has_solutions': len(solutions) > 0
        }
    
    def generate_plot(self, params, results):
        a = float(params['a'])
        V0 = float(params['V0'])
        m = float(params['m'])
        hbar = float(params['hbar'])
        
        z0 = np.sqrt(2 * m * V0 / hbar**2)
        z_range = np.linspace(0.01, z0 - 0.01, 1000)
        
        # Calculate function values
        lhs_values = []
        rhs_values = []
        
        for z in z_range:
            try:
                lhs = np.tan(z * a)
                ratio = z0 / z
                ratio_squared = ratio**2
                if ratio_squared > 1:
                    numerator = 2 * np.sqrt(ratio_squared - 1)
                    denominator = 2 - ratio_squared
                    if abs(denominator) > 1e-12:
                        rhs = numerator / denominator
                    else:
                        rhs = np.nan
                else:
                    rhs = np.nan
                
                lhs_values.append(lhs if abs(lhs) < 50 else np.nan)
                rhs_values.append(rhs if abs(rhs) < 50 else np.nan)
            except:
                lhs_values.append(np.nan)
                rhs_values.append(np.nan)
        
        # Create plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(z_range, lhs_values, 'b-', linewidth=2, label=f'tan({a}z)')
        ax.plot(z_range, rhs_values, 'r-', linewidth=2, 
                label='2√((z₀/z)² - 1)/(2 - (z₀/z)²)')
        
        # Mark solutions
        if results['has_solutions']:
            for state in results['bound_states']:
                z_val = state['z_value']
                try:
                    y_val = np.tan(z_val * a)
                    if abs(y_val) < 50:
                        ax.plot(z_val, y_val, 'go', markersize=8, 
                               label=f'State {state["state_number"]}: z={z_val:.4f}')
                except:
                    pass
        
        ax.set_xlim(0, z0)
        ax.set_ylim(-20, 20)
        ax.set_xlabel('z')
        ax.set_ylabel('Function value')
        ax.set_title(f'Finite Square Well: Transcendental Equation\na={a}, V₀={V0}, m={m}, ℏ={hbar}')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='k', linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        return self.plot_to_base64(fig)
    
    def get_examples(self):
        return {
            'standard': {
                'name': 'Standard Problem',
                'description': 'Basic finite well with one bound state',
                'parameters': {'a': 1.0, 'V0': 1.0, 'm': 0.5, 'hbar': 1.0, 'precision': 7}
            },
            'deep_well': {
                'name': 'Deep Well',
                'description': 'Deep well with multiple bound states',
                'parameters': {'a': 2.0, 'V0': 10.0, 'm': 0.5, 'hbar': 1.0, 'precision': 7}
            },
            'wide_well': {
                'name': 'Wide Well',
                'description': 'Wide well with multiple bound states',
                'parameters': {'a': 5.0, 'V0': 2.0, 'm': 0.5, 'hbar': 1.0, 'precision': 7}
            },
            'shallow_well': {
                'name': 'Shallow Well',
                'description': 'Very shallow well (may have no bound states)',
                'parameters': {'a': 1.0, 'V0': 0.2, 'm': 0.5, 'hbar': 1.0, 'precision': 7}
            }
        }
