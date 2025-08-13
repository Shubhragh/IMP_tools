from . import BaseSolver
import numpy as np
import matplotlib.pyplot as plt

class TunnelingSolver(BaseSolver):
    def __init__(self):
        super().__init__()
        self.name = "Quantum Tunneling"
        self.description = "Transmission and reflection through potential barriers"
    
    def get_parameters(self):
        return {
            'barrier_height': {
                'name': 'Barrier Height (V₀)',
                'type': 'float',
                'default': 2.0,
                'min': 0.1,
                'max': 10.0,
                'unit': 'energy units',
                'description': 'Height of potential barrier'
            },
            'barrier_width': {
                'name': 'Barrier Width (a)',
                'type': 'float',
                'default': 1.0,
                'min': 0.1,
                'max': 5.0,
                'unit': 'length units',
                'description': 'Width of potential barrier'
            },
            'particle_energy': {
                'name': 'Particle Energy (E)',
                'type': 'float',
                'default': 1.0,
                'min': 0.1,
                'max': 5.0,
                'unit': 'energy units',
                'description': 'Energy of incident particle'
            },
            'm': {
                'name': 'Particle Mass (m)',
                'type': 'float',
                'default': 1.0,
                'min': 0.1,
                'max': 10.0,
                'unit': 'mass units',
                'description': 'Mass of tunneling particle'
            },
            'hbar': {
                'name': 'ℏ (Reduced Planck)',
                'type': 'float',
                'default': 1.0,
                'min': 0.1,
                'max': 10.0,
                'unit': 'action units',
                'description': 'Reduced Planck constant'
            }
        }
    
    def validate_parameters(self, params):
        try:
            V0 = float(params.get('barrier_height', 2.0))
            a = float(params.get('barrier_width', 1.0))
            E = float(params.get('particle_energy', 1.0))
            m = float(params.get('m', 1.0))
            hbar = float(params.get('hbar', 1.0))
            
            if any(x <= 0 for x in [V0, a, E, m, hbar]):
                return {'valid': False, 'message': 'All parameters must be positive!'}
                
            return {'valid': True, 'message': 'Parameters valid'}
            
        except (ValueError, TypeError):
            return {'valid': False, 'message': 'Invalid parameter values!'}
    
    def solve(self, params):
        V0 = float(params['barrier_height'])
        a = float(params['barrier_width'])
        E = float(params['particle_energy'])
        m = float(params['m'])
        hbar = float(params['hbar'])
        
        # Wave numbers
        k1 = np.sqrt(2 * m * E / hbar**2)  # Outside barrier
        
        if E < V0:
            # Tunneling case
            k2 = np.sqrt(2 * m * (V0 - E) / hbar**2)  # Inside barrier (imaginary momentum)
            regime = "Tunneling"
            
            # Transmission coefficient
            gamma = k2 * a
            sinh_gamma = np.sinh(gamma)
            cosh_gamma = np.cosh(gamma)
            
            denominator = cosh_gamma**2 + (V0**2 * sinh_gamma**2) / (4 * E * (V0 - E))
            T = 1 / denominator
            
        else:
            # Over-barrier case
            k2 = np.sqrt(2 * m * (E - V0) / hbar**2)  # Inside barrier
            regime = "Over-barrier"
            
            # Transmission coefficient
            sin_term = np.sin(k2 * a)**2
            denominator = 1 + (V0**2 * sin_term) / (4 * E * (E - V0))
            T = 1 / denominator
        
        # Reflection coefficient
        R = 1 - T
        
        # Classical turning point (if E < V0)
        classical_turning = a if E < V0 else 0
        
        # Penetration depth (characteristic length scale)
        if E < V0:
            penetration_depth = 1 / k2
        else:
            penetration_depth = np.inf
        
        # De Broglie wavelength
        lambda_db = 2 * np.pi * hbar / np.sqrt(2 * m * E)
        
        return {
            'system_info': {
                'regime': regime,
                'barrier_parameter': round(V0/E, 3),
                'de_broglie_wavelength': round(lambda_db, 4),
                'penetration_depth': round(penetration_depth, 4) if penetration_depth != np.inf else 'infinite',
                'classical_turning_point': round(classical_turning, 4)
            },
            'tunneling_results': {
                'transmission_coefficient': round(T, 6),
                'reflection_coefficient': round(R, 6),
                'transmission_probability': round(T * 100, 4),
                'reflection_probability': round(R * 100, 4)
            },
            'wave_numbers': {
                'k_outside': round(k1, 4),
                'k_inside': round(k2.real, 4) if E >= V0 else f"{k2:.4f}i",
                'barrier_phase': round(k2 * a, 4) if E >= V0 else f"{k2 * a:.4f}i"
            }
        }
    
    def generate_plot(self, params, results):
        V0 = float(params['barrier_height'])
        a = float(params['barrier_width'])
        E = float(params['particle_energy'])
        m = float(params['m'])
        hbar = float(params['hbar'])
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Plot 1: Potential and Energy
        x = np.linspace(-2*a, 3*a, 1000)
        V = np.where((x >= 0) & (x <= a), V0, 0)
        
        ax1.fill_between(x, 0, V, alpha=0.3, color='red', label='Potential Barrier')
        ax1.axhline(y=E, color='blue', linestyle='--', linewidth=2, label=f'Particle Energy E={E}')
        ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax1.axvline(x=0, color='gray', linestyle=':', alpha=0.5)
        ax1.axvline(x=a, color='gray', linestyle=':', alpha=0.5)
        
        ax1.set_xlim(-2*a, 3*a)
        ax1.set_ylim(-0.5, max(V0, E) + 0.5)
        ax1.set_xlabel('Position')
        ax1.set_ylabel('Potential Energy')
        ax1.set_title(f'Quantum Tunneling: {results["system_info"]["regime"]} Regime')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Add annotations
        ax1.text(-1.5*a, E + 0.1, 'Incident\nWave', ha='center', fontsize=10, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue'))
        ax1.text(a/2, V0 + 0.1, f'V₀ = {V0}', ha='center', fontweight='bold')
        ax1.text(2*a, E + 0.1, 'Transmitted\nWave', ha='center', fontsize=10,
                bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen'))
        
        # Plot 2: Wavefunction
        x_wave = np.linspace(-2*a, 3*a, 2000)
        
        k1 = np.sqrt(2 * m * E / hbar**2)
        T = results['tunneling_results']['transmission_coefficient']
        R = results['tunneling_results']['reflection_coefficient']
        
        if E < V0:
            # Tunneling case
            k2 = np.sqrt(2 * m * (V0 - E) / hbar**2)
            
            # Wavefunction components
            psi = np.zeros_like(x_wave, dtype=complex)
            
            # Region 1: x < 0 (incident + reflected)
            mask1 = x_wave < 0
            psi[mask1] = np.exp(1j * k1 * x_wave[mask1]) + np.sqrt(R) * np.exp(-1j * k1 * x_wave[mask1])
            
            # Region 2: 0 < x < a (exponential decay)
            mask2 = (x_wave >= 0) & (x_wave <= a)
            A = (1 + np.sqrt(R)) * np.exp(k2 * a) / (np.exp(k2 * a) + np.exp(-k2 * a))
            psi[mask2] = A * (np.exp(-k2 * x_wave[mask2]) + np.exp(k2 * (x_wave[mask2] - 2*a)))
            
            # Region 3: x > a (transmitted)
            mask3 = x_wave > a
            psi[mask3] = np.sqrt(T) * np.exp(1j * k1 * x_wave[mask3])
            
        else:
            # Over-barrier case
            k2 = np.sqrt(2 * m * (E - V0) / hbar**2)
            
            psi = np.zeros_like(x_wave, dtype=complex)
            
            # Region 1: x < 0
            mask1 = x_wave < 0
            psi[mask1] = np.exp(1j * k1 * x_wave[mask1]) + np.sqrt(R) * np.exp(-1j * k1 * x_wave[mask1])
            
            # Region 2: 0 < x < a
            mask2 = (x_wave >= 0) & (x_wave <= a)
            # Simplified wavefunction inside barrier
            phase_shift = k1 * 0 - k2 * 0  # Approximate
            psi[mask2] = (1 + np.sqrt(R)) * np.cos(k2 * x_wave[mask2] + phase_shift)
            
            # Region 3: x > a
            mask3 = x_wave > a
            psi[mask3] = np.sqrt(T) * np.exp(1j * k1 * x_wave[mask3])
        
        # Plot real part and probability density
        ax2.plot(x_wave, np.real(psi), 'b-', linewidth=1.5, label='Re(ψ)', alpha=0.7)
        ax2.plot(x_wave, np.abs(psi)**2, 'r-', linewidth=2, label='|ψ|²')
        
        # Shade barrier region
        ax2.axvspan(0, a, alpha=0.2, color='red')
        
        ax2.set_xlim(-2*a, 3*a)
        ax2.set_xlabel('Position')
        ax2.set_ylabel('Wavefunction')
        ax2.set_title(f'T = {T:.4f} ({T*100:.2f}%), R = {R:.4f} ({R*100:.2f}%)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return self.plot_to_base64(fig)
    
    def get_examples(self):
        return {
            'tunneling': {
                'name': 'Quantum Tunneling',
                'description': 'E < V₀, particle tunnels through barrier',
                'parameters': {'barrier_height': 2.0, 'barrier_width': 1.0, 'particle_energy': 1.0, 'm': 1.0, 'hbar': 1.0}
            },
            'over_barrier': {
                'name': 'Over-barrier',
                'description': 'E > V₀, particle goes over barrier',
                'parameters': {'barrier_height': 1.0, 'barrier_width': 1.0, 'particle_energy': 2.0, 'm': 1.0, 'hbar': 1.0}
            },
            'thick_barrier': {
                'name': 'Thick Barrier',
                'description': 'Wide barrier with strong attenuation',
                'parameters': {'barrier_height': 2.0, 'barrier_width': 3.0, 'particle_energy': 1.0, 'm': 1.0, 'hbar': 1.0}
            },
            'high_barrier': {
                'name': 'High Barrier',
                'description': 'Very high barrier',
                'parameters': {'barrier_height': 5.0, 'barrier_width': 1.0, 'particle_energy': 1.0, 'm': 1.0, 'hbar': 1.0}
            }
        }
