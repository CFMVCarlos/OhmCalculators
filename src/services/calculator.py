"""Calculation services wrapping domain math functions for API routes."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from collections.abc import Generator
from closest_parallel_resistors import find_best_parallel_combination
from lib.e24_resistor_values import all_resistor_values
from lib.voltage_divider_calculations import voltage_divider_calculations
from voltage_divider_resistors_calculator import find_resistor_values


def calculate_voltage_divider(
    vin: float | None = None,
    vout: float | None = None,
    r1: float | None = None,
    r2: float | None = None,
) -> float | None:
    """Calculate an unknown parameter in a voltage divider circuit.

    Parameters
    ----------
    vin : float | None, default=None
        Input voltage in volts.
    vout : float | None, default=None
        Output voltage in volts.
    r1 : float | None, default=None
        Resistor R1 resistance in ohms.
    r2 : float | None, default=None
        Resistor R2 resistance in ohms.

    Returns
    -------
    float | None
        Calculated parameter value based on inputs provided.
    """
    return voltage_divider_calculations(vin=vin, vout=vout, r1=r1, r2=r2)


def calculate_best_parallel(target_value: float) -> tuple[float, float, float]:
    """Find the best pair of parallel resistors approximating a target value.

    Parameters
    ----------
    target_value : float
        Target equivalent resistance in ohms.

    Returns
    -------
    tuple[float, float, float]
        Tuple of (best_r1, best_r2, best_error).
    """
    return find_best_parallel_combination(target_value)


def calculate_divider_resistors(
    vin: float, vout: float, max_current: float
) -> tuple[float, float, float, float]:
    """Find resistor combination for voltage divider matching target voltages.

    Parameters
    ----------
    vin : float
        Input voltage in volts.
    vout : float
        Target output voltage in volts.
    max_current : float
        Maximum allowable current in milliamps.

    Returns
    -------
    tuple[float, float, float, float]
        Tuple of (best_r1, best_r2, best_error, current).
    """
    return find_resistor_values(vin, vout, max_current)
