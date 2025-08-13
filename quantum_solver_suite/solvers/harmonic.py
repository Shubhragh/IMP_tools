from . import BaseSolver
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import hermite
from scipy.special import factorial

class HarmonicOscillatorSolver(BaseSolver):
    def __init__(self):
        super().__init__()
        self.name = "Quantum Harmonic Oscillator"
        self.description = "Energy levels and wavefunctions of quantum harmonic oscillator"
    
    def get_parameters(self):
        return {
            'omega': {
                'name': 'Angular Frequency (ω)',
                'type': 'float',
                'default': 1.0,
                'min': 0.1,
                'max': 10.0,
                'unit': 'rad/s',
                'description': 'Angular frequency of oscillator'
            },
            'm': {
                'name': 'Mass (m)',
                'type': 'float',
                'default': 1.0,
                'min': 0.1,
                'max': 10.0,
                'unit': 'mass units',
                'description': 'Mass of oscillating particle'
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
            'max_n': {
                'name': 'Maximum n',
                'type': 'int',
                'default': 5,
                'min': 1,
                'max': 20,
                'unit': 'levels',
                'description': 'Maximum quantum number to calculate'
            },
            'x_range': {
                'name': 'Position Range',
                'type': 'float',
                'default': 5.0,
                'min': 1.0,
                'max': 20.0,
                'unit': 'length units',
                'description': 'Range for position plots (±x_range)'
            }
        }
    
    def validate_parameters(self, params):
        try:
            omega = float(params.get('omega', 1.0))
            m = float(params.get('m', 1.0))
            hbar = float(params.get('hbar', 1.0))
            max_n = int(params.get('max_n', 5))
            x_range = float(params.get('x_range', 5.0))
            
            if any(x <= 0 for x in [omega, m, hbar, max_n, x_range]):
                return {'valid': False, 'message': 'All parameters must be positive!'}
                
            if max_n > 20:
                return {'valid': False, 'message': 'Maximum n should not exceed 20!'}
                
            return {'valid': True, 'message': 'Parameters valid'}
            
        except (ValueError, TypeError):
            return {'valid': False, 'message': 'Invalid parameter values!'}
    
    def solve(self, params):
        omega = float(params['omega'])
        m = float(params['m'])
        hbar = float(params['hbar'])
        max_n = int(params['max_n'])
        
        # Characteristic length
        x0 = np.sqrt(hbar / (m * omega))
        
        # Energy levels
        energy_levels = []
        for n in range(max_n + 1):
            energy = hbar * omega * (n + 0.5)
            energy_levels.append({
                'n': n,
                'energy': round(energy, 6),
                'classical_turning_points': round(np.sqrt(2 * energy / (m * omega**2)), 4)
            })
        
        # Zero-point energy
        zero_point = hbar * omega / 2
        
        return {
            'system_info': {
                'characteristic_length': round(x0, 6),
                'zero_point_energy': round(zero_point, 6),
                'energy_spacing': round(hbar * omega, 6),
                'classical_frequency': round(omega / (2 * np.pi), 6)
            },
            'energy_levels': energy_levels
        }
    
    def generate_plot(self, params, results):
        omega = float(params['omega'])
        m = float(params['m'])
        hbar = float(params['hbar'])
        max_n = int(params['max_n'])
        x_range = float(params['x_range'])
        
        x0 = np.sqrt(hbar / (m * omega))
        x = np.linspace(-x_range, x_range, 1000)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Plot 1: Energy levels
        ax1.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        
        # Potential
        V = 0.5 * m * omega**2 * x**2
        ax1.plot(x, V, 'k-', linewidth=2, label='Potential V(x)')
        
        # Energy levels and wavefunctions
        colors = plt.cm.viridis(np.linspace(0, 1, max_n + 1))
        
        for n in range(max_n + 1):
            energy = hbar * omega * (n + 0.5)
            
            # Energy line
            ax1.axhline(y=energy, color=colors[n], linestyle='--', alpha=0.7)
            ax1.text(x_range * 0.8, energy, f'n={n}', color=colors[n], fontweight='bold')
            
            # Wavefunction (normalized)
            xi = x / x0
            H_n = hermite(n)
            psi = (1 / (2**n * factorial(n))**0.5) * (m * omega / (np.pi * hbar))**(1/4) * \
                  np.exp(-m * omega * x**2 / (2 * hbar)) * H_n(xi)
            
            # Scale and shift wavefunction for display
            psi_scaled = energy + psi * hbar * omega * 0.3
            ax1.plot(x, psi_scaled, color=colors[n], linewidth=2, alpha=0.8)
        
        ax1.set_xlim(-x_range, x_range)
        ax1.set_ylim(0, hbar * omega * (max_n + 2))
        ax1.set_xlabel('Position x')
        ax1.set_ylabel('Energy')
        ax1.set_title('Quantum Harmonic Oscillator\nEnergy Levels & Wavefunctions')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Probability densities
        for n in range(min(4, max_n + 1)):  # Show only first 4 levels
            xi = x / x0
            H_n = hermite(n)
            psi = (1 / (2**n * factorial(n))**0.5) * (m * omega / (np.pi * hbar))**(1/4) * \
                  np.exp(-m * omega * x**2 / (2 * hbar)) * H_n(xi)
            
            prob_density = psi**2
            ax2.plot(x, prob_density, color=colors[n], linewidth=2, 
                    label=f'|ψ_{n}(x)|²', alpha=0.8)
        
        ax2.set_xlim(-x_range, x_range)
        ax2.set_xlabel('Position x')
        ax2.set_ylabel('Probability Density')
        ax2.set_title('Probability Densities')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return self.plot_to_base64(fig)
    
    def get_examples(self):
        return {
            'standard': {
                'name': 'Standard Oscillator',
                'description': 'Basic harmonic oscillator',
                'parameters': {'omega': 1.0, 'm': 1.0, 'hbar': 1.0, 'max_n': 5, 'x_range': 5.0}
            },
            'high_frequency': {
                'name': 'High Frequency',
                'description': 'Fast oscillator with large energy spacing',
                'parameters': {'omega': 3.0, 'm': 1.0, 'hbar': 1.0, 'max_n': 5, 'x_range': 3.0}
            },
            'heavy_particle': {
                'name': 'Heavy Particle',
                'description': 'Heavy particle oscillator',
                'parameters': {'omega': 1.0, 'm': 5.0, 'hbar': 1.0, 'max_n': 5, 'x_range': 3.0}
            },
            'many_levels': {
                'name': 'Many Energy Levels',
                'description': 'Show many energy levels',
                'parameters': {'omega': 1.0, 'm': 1.0, 'hbar': 1.0, 'max_n': 10, 'x_range': 6.0}
            }
        }
