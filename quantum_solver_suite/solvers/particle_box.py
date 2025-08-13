from . import BaseSolver
import numpy as np
import matplotlib.pyplot as plt

class ParticleBoxSolver(BaseSolver):
    def __init__(self):
        super().__init__()
        self.name = "Particle in a Box"
        self.description = "Infinite square well energy levels and wavefunctions"
    
    def get_parameters(self):
        return {
            'box_length': {
                'name': 'Box Length (L)',
                'type': 'float',
                'default': 1.0,
                'min': 0.1,
                'max': 10.0,
                'unit': 'length units',
                'description': 'Length of the infinite square well'
            },
            'm': {
                'name': 'Particle Mass (m)',
                'type': 'float',
                'default': 1.0,
                'min': 0.1,
                'max': 10.0,
                'unit': 'mass units',
                'description': 'Mass of confined particle'
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
                'max': 15,
                'unit': 'quantum number',
                'description': 'Maximum quantum number to calculate'
            },
            'show_classical': {
                'name': 'Show Classical',
                'type': 'bool',
                'default': True,
                'unit': 'comparison',
                'description': 'Show classical probability distribution'
            }
        }
    
    def validate_parameters(self, params):
        try:
            L = float(params.get('box_length', 1.0))
            m = float(params.get('m', 1.0))
            hbar = float(params.get('hbar', 1.0))
            max_n = int(params.get('max_n', 5))
            
            if any(x <= 0 for x in [L, m, hbar, max_n]):
                return {'valid': False, 'message': 'All parameters must be positive!'}
                
            if max_n > 15:
                return {'valid': False, 'message': 'Maximum n should not exceed 15!'}
                
            return {'valid': True, 'message': 'Parameters valid'}
            
        except (ValueError, TypeError):
            return {'valid': False, 'message': 'Invalid parameter values!'}
    
    def solve(self, params):
        L = float(params['box_length'])
        m = float(params['m'])
        hbar = float(params['hbar'])
        max_n = int(params['max_n'])
        
        # Energy levels
        energy_levels = []
        for n in range(1, max_n + 1):
            energy = n**2 * np.pi**2 * hbar**2 / (2 * m * L**2)
            wavelength = 2 * L / n  # de Broglie wavelength in the box
            
            energy_levels.append({
                'n': n,
                'energy': round(energy, 6),
                'energy_ratio': round(energy / (np.pi**2 * hbar**2 / (2 * m * L**2)), 2),
                'wavelength': round(wavelength, 4),
                'nodes': n - 1  # Number of nodes (excluding boundaries)
            })
        
        # Ground state properties
        ground_state_energy = np.pi**2 * hbar**2 / (2 * m * L**2)
        
        # Zero-point motion
        ground_state_momentum = np.pi * hbar / L
        uncertainty_product = (L / np.sqrt(12)) * ground_state_momentum  # Δx * Δp
        
        return {
            'system_info': {
                'box_length': L,
                'ground_state_energy': round(ground_state_energy, 6),
                'energy_scale': round(ground_state_energy, 6),
                'uncertainty_product': round(uncertainty_product, 6),
                'heisenberg_minimum': round(hbar/2, 6)
            },
            'energy_levels': energy_levels
        }
    
    def generate_plot(self, params, results):
        L = float(params['box_length'])
        m = float(params['m'])
        hbar = float(params['hbar'])
        max_n = int(params['max_n'])
        show_classical = params.get('show_classical', True)
        
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
        
        x = np.linspace(0, L, 1000)
        
        # Plot 1: Energy level diagram
        colors = plt.cm.viridis(np.linspace(0, 1, max_n))
        
        for i, level in enumerate(results['energy_levels']):
            n = level['n']
            energy = level['energy']
            
            # Energy level
            ax1.axhline(y=energy, color=colors[i], linewidth=2, 
                       label=f'n={n}, E={energy:.3f}')
            
            # Energy level annotation
            ax1.text(L*1.02, energy, f'n={n}', verticalalignment='center', 
                    color=colors[i], fontweight='bold')
        
        # Potential walls
        ax1.axvline(x=0, color='black', linewidth=4, alpha=0.8, label='Infinite Walls')
        ax1.axvline(x=L, color='black', linewidth=4, alpha=0.8)
        
        ax1.set_xlim(-0.1*L, 1.3*L)
        ax1.set_ylim(0, results['energy_levels'][-1]['energy'] * 1.1)
        ax1.set_xlabel('Position')
        ax1.set_ylabel('Energy')
        ax1.set_title('Particle in a Box: Energy Levels')
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Wavefunctions
        for i in range(min(4, max_n)):  # Show first 4 wavefunctions
            n = i + 1
            energy = results['energy_levels'][i]['energy']
            
            # Normalized wavefunction
            psi = np.sqrt(2/L) * np.sin(n * np.pi * x / L)
            
            # Shift wavefunction to energy level
            psi_shifted = energy + psi * (results['energy_levels'][-1]['energy'] * 0.15)
            
            ax2.plot(x, psi_shifted, color=colors[i], linewidth=2, label=f'ψ_{n}(x)')
            ax2.axhline(y=energy, color=colors[i], linestyle='--', alpha=0.5)
        
        # Potential walls
        ax2.axvline(x=0, color='black', linewidth=4, alpha=0.8)
        ax2.axvline(x=L, color='black', linewidth=4, alpha=0.8)
        
        ax2.set_xlim(-0.05*L, 1.05*L)
        ax2.set_xlabel('Position')
        ax2.set_ylabel('Energy + ψ(x)')
        ax2.set_title('Wavefunctions')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Probability densities
        for i in range(min(4, max_n)):  # Show first 4 probability densities
            n = i + 1
            
            # Probability density
            prob_density = (2/L) * np.sin(n * np.pi * x / L)**2
            
            ax3.plot(x, prob_density, color=colors[i], linewidth=2, 
                    label=f'|ψ_{n}(x)|²', alpha=0.8)
        
        # Classical probability (uniform)
        if show_classical:
            classical_prob = np.ones_like(x) / L
            ax3.plot(x, classical_prob, 'k--', linewidth=2, alpha=0.5, 
                    label='Classical (uniform)')
        
        # Potential walls
        ax3.axvline(x=0, color='black', linewidth=4, alpha=0.8)
        ax3.axvline(x=L, color='black', linewidth=4, alpha=0.8)
        
        ax3.set_xlim(-0.05*L, 1.05*L)
        ax3.set_xlabel('Position')
        ax3.set_ylabel('Probability Density')
        ax3.set_title('Quantum vs Classical Probability Distributions')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return self.plot_to_base64(fig)
    
    def get_examples(self):
        return {
            'standard': {
                'name': 'Standard Box',
                'description': 'Basic particle in a box',
                'parameters': {'box_length': 1.0, 'm': 1.0, 'hbar': 1.0, 'max_n': 5, 'show_classical': True}
            },
            'narrow_box': {
                'name': 'Narrow Box',
                'description': 'Small confinement, high energy',
                'parameters': {'box_length': 0.5, 'm': 1.0, 'hbar': 1.0, 'max_n': 5, 'show_classical': True}
            },
            'wide_box': {
                'name': 'Wide Box',
                'description': 'Large confinement, low energy',
                'parameters': {'box_length': 3.0, 'm': 1.0, 'hbar': 1.0, 'max_n': 8, 'show_classical': True}
            },
            'heavy_particle': {
                'name': 'Heavy Particle',
                'description': 'Massive particle, smaller quantum effects',
                'parameters': {'box_length': 1.0, 'm': 10.0, 'hbar': 1.0, 'max_n': 6, 'show_classical': True}
            }
        }
