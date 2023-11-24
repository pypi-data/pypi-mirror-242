from __future__ import annotations

import abc

import equinox as eqx
import jax
import jax.numpy as jnp

from dilax.pdf import Flat, Gauss, HashablePDF, Poisson
from dilax.util import as1darray

__all__ = [
    "Parameter",
    "Effect",
    "unconstrained",
    "gauss",
    "lnN",
    "poisson",
    "shape",
    "modifier",
    "staterror",
    "compose",
]


def __dir__():
    return __all__


class Parameter(eqx.Module):
    value: jax.Array = eqx.field(converter=as1darray)
    bounds: tuple[jax.Array, jax.Array] = eqx.field(
        static=True, converter=lambda x: tuple(map(as1darray, x))
    )
    constraints: set[HashablePDF] = eqx.field(static=True)

    def __init__(
        self,
        value: jax.Array,
        bounds: tuple[jax.Array, jax.Array] = (as1darray(-jnp.inf), as1darray(jnp.inf)),
    ) -> None:
        self.value = value
        self.bounds = bounds
        self.constraints: set[HashablePDF] = set()

    def update(self, value: jax.Array) -> Parameter:
        return eqx.tree_at(lambda t: t.value, self, value)

    @property
    def boundary_penalty(self) -> jax.Array:
        return jnp.where(
            (self.value < self.bounds[0]) | (self.value > self.bounds[1]),
            jnp.inf,
            0,
        )


class Effect(eqx.Module):
    @property
    @abc.abstractmethod
    def constraint(self) -> HashablePDF:
        ...

    @abc.abstractmethod
    def scale_factor(self, parameter: Parameter, sumw: jax.Array) -> jax.Array:
        ...


class unconstrained(Effect):
    @property
    def constraint(self) -> HashablePDF:
        return Flat()

    def scale_factor(self, parameter: Parameter, sumw: jax.Array) -> jax.Array:
        return parameter.value


DEFAULT_EFFECT = unconstrained()


class gauss(Effect):
    width: jax.Array = eqx.field(static=True, converter=as1darray)

    def __init__(self, width: jax.Array) -> None:
        self.width = width

    @property
    def constraint(self) -> HashablePDF:
        return Gauss(mean=0.0, width=1.0)

    def scale_factor(self, parameter: Parameter, sumw: jax.Array) -> jax.Array:
        # gx = Gauss(mean=1.0, width=self.width)  # type: ignore[arg-type]
        # g1 = Gauss(mean=1.0, width=1.0)
        # return gx.inv_cdf(g1.cdf(parameter.value + 1))
        return (parameter.value * self.width) + 1  # fast analytical solution


class shape(Effect):
    up: jax.Array = eqx.field(converter=as1darray)
    down: jax.Array = eqx.field(converter=as1darray)

    def __init__(
        self,
        up: jax.Array,
        down: jax.Array,
    ) -> None:
        self.up = up  # +1 sigma
        self.down = down  # -1 sigma

    @eqx.filter_jit
    def vshift(self, sf: jax.Array, sumw: jax.Array) -> jax.Array:
        factor = sf
        dx_sum = self.up + self.down - 2 * sumw
        dx_diff = self.up - self.down

        # taken from https://github.com/nsmith-/jaxfit/blob/8479cd73e733ba35462287753fab44c0c560037b/src/jaxfit/roofit/combine.py#L173C6-L192
        _asym_poly = jnp.array([3.0, -10.0, 15.0, 0.0]) / 8.0

        abs_value = jnp.abs(factor)
        return 0.5 * (
            dx_diff * factor
            + dx_sum
            * jnp.where(
                abs_value > 1.0,
                abs_value,
                jnp.polyval(_asym_poly, factor * factor),
            )
        )

    @property
    def constraint(self) -> HashablePDF:
        return Gauss(mean=0.0, width=1.0)

    def scale_factor(self, parameter: Parameter, sumw: jax.Array) -> jax.Array:
        sf = parameter.value
        # clip, no negative values are allowed
        return jnp.maximum((sumw + self.vshift(sf=sf, sumw=sumw)) / sumw, 0.0)


class lnN(Effect):
    width: jax.Array | tuple[jax.Array, jax.Array] = eqx.field(static=True)

    def __init__(
        self,
        width: jax.Array | tuple[jax.Array, jax.Array],
    ) -> None:
        self.width = width

    def scale(self, parameter: Parameter) -> jax.Array:
        if isinstance(self.width, tuple):
            down, up = self.width
            scale = jnp.where(parameter.value > 0, up, down)
        else:
            scale = self.width
        return scale

    @property
    def constraint(self) -> HashablePDF:
        return Gauss(mean=0.0, width=1.0)

    def scale_factor(self, parameter: Parameter, sumw: jax.Array) -> jax.Array:
        # width = self.scale(parameter=parameter)
        # g1 = Gauss(mean=1.0, width=1.0)
        # gx = Gauss(mean=jnp.exp(parameter.value), width=width)  # type: ignore[arg-type]
        # return gx.inv_cdf(g1.cdf(parameter.value + 1))
        return jnp.exp(
            parameter.value * self.scale(parameter=parameter)
        )  # fast analytical solution


class poisson(Effect):
    lamb: jax.Array = eqx.field(static=True, converter=as1darray)

    def __init__(self, lamb: jax.Array) -> None:
        self.lamb = lamb

    @property
    def constraint(self) -> HashablePDF:
        return Poisson(lamb=self.lamb)

    def scale_factor(self, parameter: Parameter, sumw: jax.Array) -> jax.Array:
        return parameter.value + 1


class ModifierBase(eqx.Module):
    @abc.abstractmethod
    def scale_factor(self, sumw: jax.Array) -> jax.Array:
        ...

    def __call__(self, sumw: jax.Array) -> jax.Array:
        return jnp.atleast_1d(self.scale_factor(sumw=sumw)) * sumw


class modifier(ModifierBase):
    """
    Create a new modifier for a given parameter and penalty.

    Example:

    .. code-block:: python

        import jax.numpy as jnp
        from dilax.parameter import modifier, Parameter, unconstrained, lnN, poisson, shape

        mu = Parameter(value=1.1, bounds=(0, 100))
        norm = Parameter(value=0.0, bounds=(-jnp.inf, jnp.inf))

        # create a new parameter and a penalty
        modify = modifier(name="mu", parameter=mu, effect=unconstrained())

        # apply the modifier
        modify(jnp.array([10, 20, 30]))
        # -> Array([11., 22., 33.], dtype=float32, weak_type=True),

        # lnN effect
        modify = modifier(name="norm", parameter=norm, effect=lnN(0.2))
        modify(jnp.array([10, 20, 30]))

        # poisson effect
        hist = jnp.array([10, 20, 30])
        modify = modifier(name="norm", parameter=norm, effect=poisson(hist))
        modify(jnp.array([10, 20, 30]))

        # shape effect
        up = jnp.array([12, 23, 35])
        down = jnp.array([8, 19, 26])
        modify = modifier(name="norm", parameter=norm, effect=shape(up, down))
        modify(jnp.array([10, 20, 30]))
    """

    name: str
    parameter: Parameter
    effect: Effect

    def __init__(
        self, name: str, parameter: Parameter, effect: Effect = DEFAULT_EFFECT
    ) -> None:
        self.name = name
        self.parameter = parameter
        self.effect = effect
        self.parameter.constraints.add(self.effect.constraint)

    def scale_factor(self, sumw: jax.Array) -> jax.Array:
        return self.effect.scale_factor(parameter=self.parameter, sumw=sumw)


class staterror(ModifierBase):
    """
    Create a staterror (barlow-beeston) modifier which acts on each bin with a different _underlying_ modifier.

    Example:

    .. code-block:: python

        import jax.numpy as jnp
        from dilax.parameter import modifier, Parameter, unconstrained, lnN, poisson, shape

        hist = jnp.array([10, 20, 30])

        p1 = Parameter(value=1.0)
        p2 = Parameter(value=0.0)
        p3 = Parameter(value=0.0)

        # all bins with bin content below 10 (threshold) are treated as poisson, else gauss
        modify = staterror(
            parameters=[p1, p2, p3],
            sumw=hist,
            sumw2=hist,
            threshold=10.0,
        )
        modify(hist)
        # -> Array([13.162277, 20.      , 30.      ], dtype=float32)

        fast_modify = eqx.filter_jit(modify)
    """

    name: str = "staterror"
    parameters: list[Parameter]
    sumw: jax.Array
    sumw2: jax.Array
    sumw2sqrt: jax.Array
    widths: jax.Array
    mask: jax.Array
    threshold: float

    def __init__(
        self,
        parameters: list[Parameter],
        sumw: jax.Array,
        sumw2: jax.Array,
        threshold: float,
    ) -> None:
        assert len(parameters) == len(sumw2) == len(sumw)

        self.parameters = parameters
        self.sumw = sumw
        self.sumw2 = sumw2
        self.sumw2sqrt = jnp.sqrt(sumw2)
        self.threshold = threshold

        # calculate width
        self.widths = self.sumw2sqrt / self.sumw

        # store if sumw is below threshold
        self.mask = self.sumw < self.threshold

        for i, param in enumerate(self.parameters):
            effect = poisson(self.sumw[i]) if self.mask[i] else gauss(self.widths[i])
            param.constraints.add(effect.constraint)

    def scale_factor(self, sumw: jax.Array) -> jax.Array:
        from functools import partial

        assert len(sumw) == len(self.parameters) == len(self.sumw2)

        values = jnp.concatenate([param.value for param in self.parameters])
        idxs = jnp.arange(len(sumw))

        # sumw where mask (poisson) else widths (gauss)
        _widths = jnp.where(self.mask, self.sumw, self.widths)

        def _mod(
            value: jax.Array,
            width: jax.Array,
            idx: jax.Array,
            effect: Effect,
        ) -> jax.Array:
            return effect(width).scale_factor(
                parameter=Parameter(value=value),
                sumw=sumw[idx],
            )[0]

        _poisson_mod = partial(_mod, effect=poisson)
        _gauss_mod = partial(_mod, effect=gauss)

        # where mask use poisson else gauss
        return jnp.where(
            self.mask,
            jax.vmap(_poisson_mod)(values, _widths, idxs),
            jax.vmap(_gauss_mod)(values, _widths, idxs),
        )


class compose(ModifierBase):
    """
    Composition of multiple modifiers, i.e.: `(f ∘ g ∘ h)(hist) = f(hist) * g(hist) * h(hist)`
    It behaves like a single modifier, but it is composed of multiple modifiers; it can be arbitrarly nested.

    Example:

    .. code-block:: python

        from dilax.parameter import modifier, compose, Parameter, unconstrained, lnN

        mu = Parameter(value=1.1, bounds=(0, 100))
        sigma = Parameter(value=0.1, bounds=(-100, 100))

        # create a new parameter and a composition of modifiers
        composition = compose(
            modifier(name="mu", parameter=mu),
            modifier(name="sigma1", parameter=sigma, effect=lnN(0.1)),
        )

        # apply the composition
        composition(jnp.array([10, 20, 30]))

        # nest compositions
        composition = compose(
            composition,
            modifier(name="sigma2", parameter=sigma, effect=lnN(0.2)),
        )

        # jit
        eqx.filter_jit(composition)(jnp.array([10, 20, 30]))
    """

    modifiers: tuple[modifier, ...]
    names: list[str] = eqx.field(static=True)

    def __init__(self, *modifiers: modifier) -> None:
        self.modifiers = modifiers

        # set names
        self.names = []
        for m in range(len(self)):
            modifier = self.modifiers[m]
            if isinstance(modifier, compose):
                self.names.extend(modifier.names)
            else:
                self.names.append(modifier.name)

        # check for duplicate names
        duplicates = [name for name in self.names if self.names.count(name) > 1]
        if duplicates:
            msg = f"Modifier need to have unique names, got: {duplicates}"
            raise ValueError(msg)

    def __len__(self) -> int:
        return len(self.modifiers)

    def scale_factors(self, sumw: jax.Array) -> dict[str, jax.Array]:
        sfs = {}
        for m in range(len(self)):
            modifier = self.modifiers[m]
            if isinstance(modifier, compose):
                sfs.update(modifier.scale_factors(sumw=sumw))
            else:
                sf = jnp.atleast_1d(modifier.scale_factor(sumw=sumw))
                sfs[modifier.name] = jnp.broadcast_to(sf, sumw.shape)
        return sfs

    def scale_factor(self, sumw: jax.Array) -> jax.Array:
        sfs = jnp.stack(list(self.scale_factors(sumw=sumw).values()))
        # calculate the product in log-space for numerical precision
        return jnp.exp(jnp.sum(jnp.log(sfs), axis=0))
