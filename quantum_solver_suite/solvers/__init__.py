from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

class BaseSolver(ABC):
    """Base class for all quantum mechanics solvers"""
    
    def __init__(self):
        self.name = ""
        self.description = ""
        
    @abstractmethod
    def get_parameters(self):
        """Return parameter definitions for the solver"""
        pass
    
    @abstractmethod
    def validate_parameters(self, params):
        """Validate input parameters"""
        pass
    
    @abstractmethod
    def solve(self, params):
        """Solve the quantum mechanics problem"""
        pass
    
    @abstractmethod
    def generate_plot(self, params, results):
        """Generate visualization plot"""
        pass
    
    @abstractmethod
    def get_examples(self):
        """Return example parameter sets"""
        pass
    
    def plot_to_base64(self, fig):
        """Convert matplotlib figure to base64 string"""
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close(fig)
        return f"data:image/png;base64,{img_base64}"
