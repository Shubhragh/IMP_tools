from . import BaseSolver
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import assoc_laguerre, factorial  # Updated import

class HydrogenAtomSolver(BaseSolver):
    def __init__(self):
        super().__init__()
        self.name = "Hydrogen Atom"
        self.description = "Electronic states and energy levels of hydrogen atom"
    
    def get_parameters(self):
        return {
            'max_n': {
                'name': 'Maximum n',
                'type': 'int',
                'default': 4,
                'min': 1,
                'max': 8,
                'unit': 'principal quantum number',
                'description': 'Maximum principal quantum number'
            },
            'Z': {
                'name': 'Nuclear Charge (Z)',
                'type': 'float',
                'default': 1.0,
                'min': 1.0,
                'max': 20.0,
                'unit': 'elementary charges',
                'description': 'Nuclear charge (Z=1 for hydrogen)'
            },
            'a0': {
                'name': 'Bohr Radius (a₀)',
                'type': 'float',
                'default': 1.0,
                'min': 0.1,
                'max': 10.0,
                'unit': 'length units',
                'description': 'Bohr radius (atomic unit of length)'
            },
            'Ry': {
                'name': 'Rydberg Energy',
                'type': 'float',
                'default': 13.6,
                'min': 1.0,
                'max': 100.0,
                'unit': 'eV',
                'description': 'Rydberg constant (13.6 eV)'
            }
        }
    
    def validate_parameters(self, params):
        try:
            max_n = int(params.get('max_n', 4))
            Z = float(params.get('Z', 1.0))
            a0 = float(params.get('a0', 1.0))
            Ry = float(params.get('Ry', 13.6))
            
            if any(x <= 0 for x in [max_n, Z, a0, Ry]):
                return {'valid': False, 'message': 'All parameters must be positive!'}
                
            if max_n > 8:
                return {'valid': False, 'message': 'Maximum n should not exceed 8!'}
                
            return {'valid': True, 'message': 'Parameters valid'}
            
        except (ValueError, TypeError):
            return {'valid': False, 'message': 'Invalid parameter values!'}
    
    def solve(self, params):
        max_n = int(params['max_n'])
        Z = float(params['Z'])
        a0 = float(params['a0'])
        Ry = float(params['Ry'])
        
        energy_levels = []
        
        for n in range(1, max_n + 1):
            # Energy levels
            energy = -Ry * Z**2 / n**2
            
            # Degeneracy
            degeneracy = n**2
            
            # Orbital details
            orbitals = []
            for l in range(n):
                orbital_name = self.get_orbital_name(n, l)
                for m in range(-l, l + 1):
                    orbitals.append({
                        'n': n,
                        'l': l,
                        'm': m,
                        'orbital': orbital_name
                    })
            
            energy_levels.append({
                'n': n,
                'energy': round(energy, 4),
                'degeneracy': degeneracy,
                'orbitals': orbitals
            })
        
        # System properties
        ionization_energy = Ry * Z**2
        ground_state_radius = a0 / Z
        
        return {
            'system_info': {
                'nuclear_charge': Z,
                'bohr_radius': round(a0, 4),
                'rydberg_energy': round(Ry, 4),
                'ionization_energy': round(ionization_energy, 4),
                'ground_state_radius': round(ground_state_radius, 4)
            },
            'energy_levels': energy_levels
        }
    
    def get_orbital_name(self, n, l):
        """Convert quantum numbers to orbital names"""
        l_names = {0: 's', 1: 'p', 2: 'd', 3: 'f', 4: 'g', 5: 'h'}
        return f"{n}{l_names.get(l, '?')}"
    
    def generate_plot(self, params, results):
        max_n = int(params['max_n'])
        Z = float(params['Z'])
        a0 = float(params['a0'])
        Ry = float(params['Ry'])
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Plot 1: Energy Level Diagram
        colors = plt.cm.viridis(np.linspace(0, 1, max_n))
        
        for i, level in enumerate(results['energy_levels']):
            n = level['n']
            energy = level['energy']
            degeneracy = level['degeneracy']
            
            # Energy level line
            ax1.hlines(energy, 0, degeneracy, colors=colors[i], linewidth=3)
            
            # Level labels
            ax1.text(degeneracy + 0.5, energy, f'n={n}', 
                    verticalalignment='center', fontweight='bold')
            
            # Individual orbitals
            x_positions = np.linspace(0.1, degeneracy - 0.1, level['degeneracy'])
            for j in range(level['degeneracy']):
                ax1.plot(x_positions[j], energy, 'ko', markersize=6)
        
        ax1.set_xlabel('Degeneracy')
        ax1.set_ylabel('Energy (eV)')
        ax1.set_title(f'Hydrogen Atom Energy Levels (Z={Z})')
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=0, color='r', linestyle='--', alpha=0.5, label='Ionization')
        ax1.legend()
        
        # Plot 2: Radial Wavefunctions
        r = np.linspace(0.01, 20*a0/Z, 1000)
        
        for n in range(1, min(4, max_n + 1)):  # Show first 3 levels
            l = 0  # s orbitals only for simplicity
            R_nl = self.radial_wavefunction(r, n, l, Z, a0)
            ax2.plot(r, R_nl, linewidth=2, label=f'R_{n}{l}(r)')
        
        ax2.set_xlabel('Distance (a₀)')
        ax2.set_ylabel('Radial Wavefunction')
        ax2.set_title('Radial Wavefunctions (s orbitals)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return self.plot_to_base64(fig)
    
    def radial_wavefunction(self, r, n, l, Z, a0):
        """Calculate radial wavefunction R_nl(r)"""
        rho = 2 * Z * r / (n * a0)
        
        # Normalization constant
        norm = (2 * Z / (n * a0))**(3/2) * np.sqrt(
            factorial(n - l - 1) / (2 * n * factorial(n + l))
        )
        
        # Associated Laguerre polynomial
        L = assoc_laguerre(rho, n - l - 1, 2*l + 1)
        
        # Radial wavefunction
        R_nl = norm * np.exp(-rho/2) * (rho**l) * L
        
        return R_nl
    
    def get_examples(self):
        return {
            'hydrogen': {
                'name': 'Hydrogen Atom',
                'description': 'Standard hydrogen atom (Z=1)',
                'parameters': {'max_n': 4, 'Z': 1.0, 'a0': 1.0, 'Ry': 13.6}
            },
            'helium_ion': {
                'name': 'He⁺ Ion',
                'description': 'Helium ion (Z=2, hydrogen-like)',
                'parameters': {'max_n': 3, 'Z': 2.0, 'a0': 1.0, 'Ry': 13.6}
            },
            'lithium_ion': {
                'name': 'Li²⁺ Ion',
                'description': 'Lithium ion (Z=3, hydrogen-like)',
                'parameters': {'max_n': 3, 'Z': 3.0, 'a0': 1.0, 'Ry': 13.6}
            },
            'high_n': {
                'name': 'High Energy Levels',
                'description': 'Hydrogen with high n levels',
                'parameters': {'max_n': 6, 'Z': 1.0, 'a0': 1.0, 'Ry': 13.6}
            }
        }
