# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/Agents/11_APOStrategyBase.ipynb.

# %% auto 0
__all__ = ['POstrategybase']

# %% ../../nbs/Agents/11_APOStrategyBase.ipynb 4
import jax
import numpy as np
import itertools as it

import jax.numpy as jnp
from jax import grad, jit, vmap
from functools import partial

from fastcore.utils import *

from .Base import abase
from .POBase import aPObase
from .StrategyBase import strategybase
from ..Utils.Helpers import *

# %% ../../nbs/Agents/11_APOStrategyBase.ipynb 5
class POstrategybase(aPObase, strategybase):
    """
    Base Class for
    deterministic policy-average independent (multi-agent) partially observable
    temporal-difference reinforcement learning in policy space.
    """
    
    def __init__(self, env, learning_rates, discount_factors,
                 choice_intensities=1, **kwargs):
        """
        Parameters
        ----------
        env : environment object
        learning_rates : the learning rate(s) for the agents
        discount_factors : the discount factor(s) for the agents
        choice_intensities : inverse temperature of softmax / exploitation level
        """
        self.env = env
        Tt = env.T; assert np.allclose(Tt.sum(-1), 1)
        Rt = env.R
        Ot = env.O    
        super().__init__(Tt, Rt, Ot, discount_factors, **kwargs)
        assert np.allclose(env.F, 0), 'PO learning w final state not def.'

        # learning rates
        self.alpha = make_variable_vector(learning_rates, self.N)
        
        # intensity of choice
        self.beta = make_variable_vector(choice_intensities, self.N)

