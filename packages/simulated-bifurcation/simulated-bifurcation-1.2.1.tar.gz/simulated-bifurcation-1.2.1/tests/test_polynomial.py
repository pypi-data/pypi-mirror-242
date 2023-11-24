import pytest
import torch

from src.simulated_bifurcation import build_model
from src.simulated_bifurcation.ising_core import IsingCore
from src.simulated_bifurcation.polynomial import (
    BaseMultivariateQuadraticPolynomial,
    IsingPolynomialInterface,
)

matrix = torch.tensor(
    [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ],
    dtype=torch.float32,
)
vector = torch.tensor([[1], [2], [3]], dtype=torch.float32)
constant = 1


class BaseMultivariateQuadraticPolynomialImpl(BaseMultivariateQuadraticPolynomial):
    def to_ising(self):
        pass  # pragma: no cover

    def convert_spins(self, ising: IsingCore):
        pass  # pragma: no cover


class IsingPolynomialInterfaceImpl(IsingPolynomialInterface):
    def to_ising(self):
        pass  # pragma: no cover

    def convert_spins(self, ising: IsingCore):
        pass  # pragma: no cover


def test_init_polynomial_from_tensors():
    polynomial = BaseMultivariateQuadraticPolynomialImpl(
        matrix, vector, constant, silence_deprecation_warning=True
    )
    assert torch.equal(polynomial.matrix, matrix)
    assert torch.equal(polynomial.vector, vector.reshape(3))
    assert polynomial.constant == 1.0
    assert polynomial.dimension == 3
    assert len(polynomial) == 3
    assert polynomial[0] == 1.0
    assert torch.equal(polynomial[2], matrix)
    assert torch.equal(polynomial[1], vector.reshape(3))
    assert polynomial.dtype == torch.float32
    assert polynomial.device == torch.device("cpu")
    with pytest.raises(ValueError):
        # noinspection PyStatementEffect
        polynomial[3]


def test_init_polynomial_from_arrays():
    polynomial = BaseMultivariateQuadraticPolynomialImpl(
        matrix.numpy(), vector.numpy(), constant, silence_deprecation_warning=True
    )
    assert torch.equal(polynomial.matrix, matrix)
    assert torch.equal(polynomial.vector, vector.reshape(3))
    assert polynomial.constant == 1.0
    assert polynomial.dimension == 3
    assert len(polynomial) == 3
    assert polynomial[0] == 1.0
    assert torch.equal(polynomial[2], matrix)
    assert torch.equal(polynomial[1], vector.reshape(3))


def test_init_polynomial_without_order_one_and_zero():
    polynomial = BaseMultivariateQuadraticPolynomialImpl(
        matrix, silence_deprecation_warning=True
    )
    assert torch.equal(polynomial.matrix, matrix)
    assert torch.equal(polynomial.vector, torch.zeros(polynomial.dimension))
    assert polynomial.constant == 0.0
    assert polynomial.dimension == 3
    assert len(polynomial) == 3
    assert torch.equal(polynomial[2], matrix)
    assert torch.equal(polynomial[1], torch.zeros(polynomial.dimension))
    assert polynomial[0] == 0.0


def test_init_with_wrong_parameters():
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        BaseMultivariateQuadraticPolynomialImpl(None, silence_deprecation_warning=True)
    with pytest.raises(ValueError):
        BaseMultivariateQuadraticPolynomialImpl(
            torch.unsqueeze(matrix, 0), silence_deprecation_warning=True
        )
    with pytest.raises(ValueError):
        BaseMultivariateQuadraticPolynomialImpl(
            torch.tensor(
                [
                    [1, 2, 3],
                    [4, 5, 6],
                ],
                dtype=torch.float32,
            ),
            silence_deprecation_warning=True,
        )
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        BaseMultivariateQuadraticPolynomialImpl(
            matrix, ("hello", "world!"), silence_deprecation_warning=True
        )
    with pytest.raises(ValueError):
        # noinspection PyTypeChecker
        BaseMultivariateQuadraticPolynomialImpl(
            matrix, 1, silence_deprecation_warning=True
        )
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        BaseMultivariateQuadraticPolynomialImpl(
            matrix, constant="hello world!", silence_deprecation_warning=True
        )


def test_check_device():
    BaseMultivariateQuadraticPolynomialImpl(
        matrix, device="cpu", silence_deprecation_warning=True
    )
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        BaseMultivariateQuadraticPolynomialImpl(
            matrix, device=1, silence_deprecation_warning=True
        )
    if not torch.cuda.is_available():  # pragma: no cover
        with pytest.raises(RuntimeError):
            BaseMultivariateQuadraticPolynomialImpl(
                matrix, device="cuda", silence_deprecation_warning=True
            )
    else:  # pragma: no cover
        BaseMultivariateQuadraticPolynomialImpl(
            matrix, device="cuda", silence_deprecation_warning=True
        )


def test_call_polynomial():
    polynomial = BaseMultivariateQuadraticPolynomialImpl(
        matrix, silence_deprecation_warning=True
    )
    assert polynomial(torch.tensor([0, 0, 0], dtype=torch.float32)) == 0.0
    assert torch.equal(
        polynomial(
            torch.tensor(
                [
                    [0, 0, 0],
                    [1, 2, 3],
                ],
                dtype=torch.float32,
            )
        ),
        torch.tensor([0, 228], dtype=torch.float32),
    )
    assert isinstance(
        polynomial(torch.tensor([0, 0, 0], dtype=torch.float32)), torch.Tensor
    )
    assert polynomial(torch.tensor([0, 0, 0], dtype=torch.float32)).shape == ()
    assert polynomial(torch.tensor([[0, 0, 0]], dtype=torch.float32)).shape == (1,)
    assert polynomial(torch.zeros((1, 5, 3, 1, 2, 1, 3))).shape == (1, 5, 3, 1, 2, 1)
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        polynomial("hello world!")
    with pytest.raises(ValueError):
        polynomial(torch.tensor([1, 2, 3, 4, 5], dtype=torch.float32))


def test_call_polynomial_with_accepted_values():
    polynomial = BaseMultivariateQuadraticPolynomialImpl(
        matrix, accepted_values=[0, 1], silence_deprecation_warning=True
    )
    assert polynomial(torch.tensor([0, 0, 0], dtype=torch.float32)) == 0
    with pytest.raises(ValueError):
        polynomial(torch.tensor([0, 1, 2], dtype=torch.float32))
    assert (
        polynomial(
            torch.tensor([0, 1, 2], dtype=torch.float32), input_values_check=False
        )
        == 69
    )


def test_ising_interface():
    with pytest.raises(NotImplementedError):
        # noinspection PyTypeChecker
        BaseMultivariateQuadraticPolynomial.to_ising(None)
    with pytest.raises(NotImplementedError):
        # noinspection PyTypeChecker
        BaseMultivariateQuadraticPolynomial.convert_spins(None, None)


def test_best_only():
    model = build_model(
        matrix=matrix,
        vector=vector,
        constant=constant,
        domain="spin",
        dtype=torch.float32,
        device="cpu",
    )
    spins_best_only, energy_best_only = model.optimize(agents=42, best_only=True)
    assert model.sb_result.shape == (3, 42)
    assert spins_best_only.shape == (3,)
    assert isinstance(energy_best_only, torch.Tensor)
    assert energy_best_only.shape == ()
    assert energy_best_only == -2
    spins_all, energies_all = model.optimize(agents=42, best_only=False)
    assert model.sb_result.shape == (3, 42)
    assert spins_all.shape == (42, 3)
    assert isinstance(energies_all, torch.Tensor)
    assert energies_all.shape == (42,)


def test_minimize():
    torch.manual_seed(42)
    model = build_model(
        matrix=matrix,
        vector=vector,
        constant=constant,
        domain="spin",
        dtype=torch.float32,
        device="cpu",
    )
    best_combination, best_value = model.minimize()
    assert torch.equal(
        best_combination, torch.tensor([1.0, 1.0, -1.0], dtype=torch.float32)
    ) or torch.equal(
        best_combination, torch.tensor([-1.0, -1.0, 1.0], dtype=torch.float32)
    )
    assert best_value == -2.0


def test_maximize():
    model = build_model(
        matrix=matrix,
        vector=vector,
        constant=constant,
        domain="spin",
        dtype=torch.float32,
        device="cpu",
    )
    best_combination, best_value = model.maximize()
    assert torch.equal(
        best_combination, torch.tensor([1.0, 1.0, 1.0], dtype=torch.float32)
    )
    assert 52.0 == best_value


def test_deprecation_warning():
    with pytest.warns(DeprecationWarning):
        BaseMultivariateQuadraticPolynomialImpl(matrix, accepted_values=[0, 1])
    with pytest.warns(DeprecationWarning):
        IsingPolynomialInterfaceImpl(matrix, accepted_values=[0, 1])
