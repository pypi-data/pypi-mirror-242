import numpy as np
from typing import Callable, Any

def _promote_objective(f, f_dim):
    if not callable(f):
        raise TypeError("Objective function must be callable.")
    if f_dim == '3D':
        return f
    elif f_dim == '2D':
        return cbx_objective_f2D(f)
    elif f_dim == '1D':
        return cbx_objective_f1D(f)
    else:
        raise ValueError("f_dim must be '1D', '2D' or '3D'.")
    

def _apply_unimplemented(self, *input: Any) -> None:
    r"""

    .. note::
        This is copied from PyTorch. The code can be found here
        https://github.com/pytorch/pytorch/blob/main/torch/nn/modules/module.py#L362
    """
    raise NotImplementedError(f"Objective [{type(self).__name__}] is missing the required \"apply\" function")


class cbx_objective:
    def __init__(self, f_extra=None):
        super().__init__()
        self.num_eval = 0
        
    def __call__(self, x):
        self.num_eval += np.prod(np.atleast_2d(x).shape[:-1], dtype = int)
        return self.apply(x)
        
    apply: Callable[..., Any] = _apply_unimplemented
        
    def reset(self,):
        self.num_eval = 0
        
        
class cbx_objective_fh(cbx_objective):
    def __init__(self, f):
        super().__init__()
        self.f = f
        
    def apply(self, x):
        return self.f(x)
    
class cbx_objective_f1D(cbx_objective_fh):
    def __init__(self, f):
        super().__init__(f)
    
    def apply(self, x):
        x = np.atleast_2d(x)
        return np.apply_along_axis(self.f, 1, x.reshape(-1, x.shape[-1])).reshape(-1,x.shape[-2])
    
    
class cbx_objective_f2D(cbx_objective_fh):
    def __init__(self, f):
        super().__init__(f)
    
    def apply(self, x):
        x = np.atleast_2d(x)
        return self.f(np.atleast_2d(x.reshape(-1, x.shape[-1]))).reshape(-1,x.shape[-2])