import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from collections.abc import Generator
from lib.e24_resistor_values import all_resistor_values
from lib.voltage_divider_calculations import voltage_divider_calculations
from closest_parallel_resistors import find_best_parallel_combination
from voltage_divider_resistors_calculator import find_resistor_values


def calculate_voltage_divider(vin=None, vout=None, r1=None, r2=None):
    return voltage_divider_calculations(vin=vin, vout=vout, r1=r1, r2=r2)


def calculate_best_parallel(target_value: float):
    return find_best_parallel_combination(target_value)


def calculate_divider_resistors(vin: float, vout: float, max_current: float):
    return find_resistor_values(vin, vout, max_current)
