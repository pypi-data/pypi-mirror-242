"""
Implementation of multivariate degree 2 polynomials over spin vectors.

.. deprecated:: 1.2.1
  `SpinPolynomial` and `SpinQuadraticPolynomial` will be removed in
  simulated-bifurcation 1.3.0. From version 1.3.0 onwards, polynomials will
  no longer have a definition domain. The domain only needs to be specified
  when creating an Ising model, and conversely when converting spins back
  into the original domain.

Multivariate degree 2 polynomials are the sum of a quadratic form and a
linear form plus a constant term:
`ΣΣ Q(i,j)x(i)x(j) + Σ l(i)x(i) + c`
or `x.T Q x + l.T x + c` in matrix notation,
where `Q` is a square matrix, `l` is a vector and `c` is a constant.
The `x(i)`'s values must be either `-1` or `1`.

This polynomial can be translated into an equivalent Ising problem and
solved with the Simulated Bifurcation algorithm.

See Also
--------
BinaryQuadraticPolynomial:
    Multivariate degree 2 polynomials over vectors whose entries are in
    {0, 1}.
BaseMultivariateQuadraticPolynomial:
    Abstract class for multivariate degree 2 polynomials.
IntegerQuadraticPolynomial:
    Multivariate degree 2 polynomials over non-negative integers with a
    fixed number of bits.
models.Ising: Implementation of the Ising problem.
models:
    Package containing the implementation of several common
    combinatorial optimization problems.

Notes
-----
This class describes polynomials in the following form:
`x.T @ matrix @ x + vectors @ x + constant`.
Although equivalent, this is not the same form as the one used for the
IsingCore class:
`-0.5 x.T @ matrix @ x + vector @ x`.

"""

import warnings
from typing import Optional, Union

import numpy as np
import torch

from ..ising_core import IsingCore
from .base_multivariate_polynomial import BaseMultivariateQuadraticPolynomial


class SpinQuadraticPolynomial(BaseMultivariateQuadraticPolynomial):

    """
    Multivariate degree 2 polynomials over spin vectors.

    .. deprecated:: 1.2.1
      `SpinQuadraticPolynomial` will be removed in simulated-bifurcation
      1.3.0. From version 1.3.0 onwards, polynomials will no longer have a
      definition domain. The domain only needs to be specified when
      creating an Ising model, and conversely when converting spins back
      into the original domain.

    Multivariate degree 2 polynomials are the sum of a quadratic form and a
    linear form plus a constant term:
    `ΣΣ Q(i,j)x(i)x(j) + Σ l(i)x(i) + c`
    or `x.T Q x + l.T x + c` in matrix notation,
    where `Q` is a square matrix, `l` is a vector and `c` is a constant.
    The `x(i)`'s values must be either `-1` or `1`.

    This polynomial can be translated into an equivalent Ising problem and
    solved with the Simulated Bifurcation algorithm.

    Parameters
    ----------
    matrix : (M, M) Tensor | ndarray
        Matrix corresponding to the quadratic terms of the polynomial
        (quadratic form). It should be a square matrix, but not necessarily
        symmetric.
    vector : (M,) Tensor | ndarray | None, optional
        Vector corresponding to the linear terms of the polynomial (linear
        form). The default is None which signifies there are no linear
        terms, that is `vector` is the null vector.
    constant : int | float | None, optional
        Constant of the polynomial. The default is None which signifies
        there is no constant term, that is `constant` = 0.
    dtype : torch.dtype, default=torch.float32
        Data-type used for storing the coefficients of the polynomial.
    device : str | torch.device, default="cpu"
        Device on which the polynomial is located. If available, use "cuda"
        to use the polynomial on a GPU.

    Attributes
    ----------
    matrix
    vector
    constant
    dimension
    device
    dtype
    sb_result : (M, A) Tensor | None
        Spin vectors obtained after optimizing the polynomial. None if no
        optimization method has been called.

    See Also
    --------
    BinaryQuadraticPolynomial:
        Multivariate degree 2 polynomials over vectors whose entries are in
        {0, 1}.
    BaseMultivariateQuadraticPolynomial:
        Abstract class for multivariate degree 2 polynomials.
    IntegerQuadraticPolynomial:
        Multivariate degree 2 polynomials over non-negative integers with a
        fixed number of bits.
    models.Ising: Implementation of the Ising problem.
    models:
        Package containing the implementation of several common
        combinatorial optimization problems.

    Notes
    -----
    This class describes polynomials in the following form:
    `x.T @ matrix @ x + vectors @ x + constant`.
    Although equivalent, this is not the same form as the one used for the
    IsingCore class:
    `-0.5 x.T @ matrix @ x + vector @ x`.

    """

    def __init__(
        self,
        matrix: Union[torch.Tensor, np.ndarray],
        vector: Union[torch.Tensor, np.ndarray, None] = None,
        constant: Union[float, int, None] = None,
        dtype: Optional[torch.dtype] = None,
        device: Optional[Union[str, torch.device]] = None,
        *,
        silence_deprecation_warning=False,
    ) -> None:
        if not silence_deprecation_warning:
            # 2023-11-21, 1.2.1
            warnings.warn(
                "`SpinQuadraticPolynomial` is deprecated as of simulated-bifurcation "
                "1.2.1, and it will be removed in simulated-bifurcation 1.3.0. "
                "From version 1.3.0 onwards, polynomials will no longer have a "
                "definition domain. The domain only needs to be specified when "
                "creating an Ising model, and conversely when converting spins "
                "back into the original domain.",
                DeprecationWarning,
                stacklevel=3,
            )

        super().__init__(
            matrix,
            vector,
            constant,
            [-1, 1],
            dtype,
            device,
            silence_deprecation_warning=True,
        )

    def to_ising(self) -> IsingCore:
        return IsingCore(-2 * self.matrix, self.vector, self.dtype, self.device)

    def convert_spins(self, ising: IsingCore) -> torch.Tensor:
        """
        Retrieve the spins from an Ising problem.

        Parameters
        ----------
        ising : IsingCore
            The Ising problem containing the spins.

        Returns
        -------
        Tensor | None
            The spins of `ising`, it is None if `ising.computed_spins` is
            None.

        """
        return ising.computed_spins


class SpinPolynomial(SpinQuadraticPolynomial):

    """
    .. deprecated:: 1.2.1
      `SpinPolynomial` will be removed in simulated-bifurcation 1.3.0. From
      version 1.3.0 onwards, polynomials will no longer have a definition
      domain. The domain only needs to be specified when creating an Ising
      model, and conversely when converting spins back into the original
      domain.

    """

    def __init__(self, *args, **kwargs) -> None:
        # 2023-10-03, 1.2.1
        warnings.warn(
            "`SpinPolynomial` is deprecated as of simulated-bifurcation 1.2.1, and "
            "it will be removed in simulated-bifurcation 1.3.0. From version 1.3.0 "
            "onwards, polynomials will no longer have a definition domain. The domain "
            "only needs to be specified when creating an Ising model, and conversely "
            "when converting spins back into the original domain.",
            DeprecationWarning,
            stacklevel=3,
        )
        super().__init__(*args, **kwargs, silence_deprecation_warning=True)
