"""Bound a real number to be between two values."""
from gemd.entity.bounds.base_bounds import BaseBounds
import gemd.units as units

from typing import Union


class RealBounds(BaseBounds):
    """
    Bounded subset of the real numbers, parameterized by a lower and upper bound.

    Parameters
    ----------
    lower_bound: float
        Lower endpoint.
    upper_bound: float
        Upper endpoint.
    default_units: str
        A string describing the units. Units must be present and they must be parseable by Pint.
        An empty string can be used for the units of a dimensionless quantity.

    """

    typ = "real_bounds"

    def __init__(self, lower_bound=None, upper_bound=None, default_units=None):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        self._default_units = None
        self.default_units = default_units

        if self.lower_bound is None or abs(self.lower_bound) >= float("inf"):
            raise ValueError("Lower bound must be given and finite: {}".format(self.lower_bound))

        if self.upper_bound is None or abs(self.upper_bound) >= float("inf"):
            raise ValueError("Upper bound must be given and finite")

        if self.upper_bound < self.lower_bound:
            raise ValueError("Upper bound must be greater than or equal to lower bound")

    @property
    def default_units(self):
        """Get default units."""
        return self._default_units

    @default_units.setter
    def default_units(self, default_units):
        if default_units is None:
            raise ValueError("Real bounds must have units. "
                             "Use an empty string for a dimensionless quantity.")
        self._default_units = units.parse_units(default_units)

    def contains(self, bounds: Union[BaseBounds, "BaseValue"]) -> bool:
        """
        Check if another bounds or value object is a subset of this range.

        The other object must also be Real and its lower and upper bound must *both*
        be within the range of this bounds object.  Values that are unbounded
        distributions (e.g., Gaussian) are generally assumed to be truncated and
        logic around permissibility is delegated to the Value implementation.

        Parameters
        ----------
        bounds: Union[BaseBounds, BaseValue]
            Other bounds or value object to check.

        Returns
        -------
        bool
            True if the other object is contained by this bounds.

        """
        from gemd.entity.value.base_value import BaseValue

        if not super().contains(bounds):
            return False
        if isinstance(bounds, BaseValue):
            bounds = bounds._to_bounds()
        if not isinstance(bounds, RealBounds):
            return False

        lower, upper = self._convert_bounds(bounds.default_units)
        if lower is None:
            return False

        return bounds.lower_bound >= lower and bounds.upper_bound <= upper

    def _convert_bounds(self, target_units):
        """
        Convert the bounds to the target unit system, or None if not possible.

        Parameters
        ----------
        target_units: str
            The units to convert into.

        Returns
        -------
        tuple (float, float)
            A tuple of the (lower_bound, upper_bound) in the target units.

        """
        try:
            lower_bound = units.convert_units(
                self.lower_bound, self.default_units, target_units)
            upper_bound = units.convert_units(
                self.upper_bound, self.default_units, target_units)
            return lower_bound, upper_bound
        except units.IncompatibleUnitsError:
            return None, None
