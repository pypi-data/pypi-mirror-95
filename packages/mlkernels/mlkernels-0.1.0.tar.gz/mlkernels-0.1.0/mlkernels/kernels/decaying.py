import lab as B
from algebra.util import identical
from matrix import Dense
from plum import Dispatcher, Self

from . import _dispatch
from .. import Kernel

__all__ = ["DecayingKernel"]


class DecayingKernel(Kernel):
    """Decaying kernel.

    Args:
        alpha (tensor): Shape of the gamma distribution governing the distribution of
            decaying exponentials.
        beta (tensor): Rate of the gamma distribution governing the distribution of
            decaying exponentials.
    """

    _dispatch = Dispatcher(in_class=Self)

    def __init__(self, alpha, beta):
        self.alpha = alpha
        self.beta = beta

    def _compute_beta_raised(self):
        beta_norm = B.sqrt(
            B.maximum(B.sum(B.power(self.beta, 2)), B.cast(B.dtype(self.beta), 1e-30))
        )
        return B.power(beta_norm, self.alpha)

    def render(self, formatter):
        return f"DecayingKernel({formatter(self.alpha)}, {formatter(self.beta)})"

    @_dispatch(Self)
    def __eq__(self, other):
        return identical(self.alpha, other.alpha) and identical(self.beta, other.beta)


@_dispatch(DecayingKernel, B.Numeric, B.Numeric)
def pairwise(k, x, y):
    pw_sums_raised = B.power(B.pw_sums(B.add(x, k.beta), y), k.alpha)
    return Dense(B.divide(k._compute_beta_raised(), pw_sums_raised))


@_dispatch(DecayingKernel, B.Numeric, B.Numeric)
def elwise(k, x, y):
    return B.divide(
        k._compute_beta_raised(),
        B.power(B.ew_sums(B.add(x, k.beta), y), k.alpha),
    )
