import jax

# noinspection PyUnresolvedReferences
import lab.jax as B

# noinspection PyUnresolvedReferences
from . import *

# We need `float64`s for accurate kernels.
jax.config.update("jax_enable_x64", True)
