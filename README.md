# Resistor Value Calculator

This repository provides a set of functions for working with resistor values and performing calculations related to voltage dividers, parallel resistances, and shorthand notation for resistor values. It utilizes the standard E24 resistor series to find the best resistor combinations for various electrical applications.

## Features

This project includes the following functionalities:
- **Voltage Divider Calculations**: Calculate various parameters of a voltage divider circuit, such as input voltage, output voltage, or resistor values.
- **E24 Resistor Values**: Utilize a predefined set of resistor values based on the E24 series.
- **Resistor Shorthand Conversion**: Convert resistor values to shorthand notation (e.g., 10k, 1M).
- **Closest Parallel Resistor**: Find the best combination of two resistors in parallel to achieve a target resistance.
- **Voltage Divider Resistances Calculator**: Calculate the resistor values required in a voltage divider circuit based on the input and output voltages.

## Installation

To install and use the Resistor Value Calculator:

1. Clone the repository:

    ```bash
    git clone https://github.com/CFMVCarlos/OhmCalculators.git
    cd OhmCalculators
    ```

## Usage

### 1. Voltage Divider Calculations

The `voltage_divider_calculations` function allows you to calculate various parameters in a voltage divider circuit, such as the input voltage (`vin`) or output voltage (`vout`), given two resistors.

**Example**:

```python
from lib.voltage_divider_calculations import voltage_divider_calculations

vout = 5.0  # Output voltage in volts
r1 = 18e3  # Resistor R1 in ohms
r2 = 13e3  # Resistor R2 in ohms

result = voltage_divider_calculations(vout=vout, r1=r1, r2=r2)  # Calculate Vin
print(f"Calculated Vin: {result} V")  # Output: 11.92 V
```

### 2. Resistor Value Lookup

The `all_resistor_values` function generates all standard resistor values based on the E24 series, ranging from 1.0Ω to 9.1MΩ.

**Example**:

```python
from lib.e24_resistor_values import all_resistor_values

for value in all_resistor_values():
    print(value)
```

### 3. Converting Resistor Values to Shorthand

The `convert_to_shorthand` function converts resistor values to shorthand notation, making it easier to display resistor values in a more compact form.

**Example**:

```python
from lib.common import convert_to_shorthand

resistor_value = 10000.0  # Resistor value in ohms
shorthand = convert_to_shorthand(resistor_value)
print(f"Shorthand notation: {shorthand}")  # Output: 10k
```

### 4. Closest Parallel Resistor

The `find_best_parallel_combination` function helps you find the best pair of resistors from the E24 series that, when connected in parallel, yield the closest possible resistance to a target value. It iterates through all available resistor values in the E24 series, calculates the equivalent resistance for each pair, and compares the result to the target resistance, selecting the combination with the least error.

**Example**:

```python
from lib import find_best_parallel_combination
from lib.common import convert_resistor_value, convert_to_shorthand

target_resistance_str = "4k7"  # Target resistance in shorthand notation (e.g., '4k7')
target_resistance = convert_resistor_value(target_resistance_str)

r1, r2, error = find_best_parallel_combination(target_resistance)
print(f"Best R1: {convert_to_shorthand(r1)}, Best R2: {convert_to_shorthand(r2)} with error: {error:.4f}")
```

### 5. Finding the Best Resistor Combination for a Voltage Divider

The `find_resistor_values` function helps you find the best combination of two resistors from the E24 series to achieve a target output voltage in a voltage divider circuit. It ensures that the current through the circuit does not exceed the maximum allowable current (provided by the user). The function iterates through all possible resistor combinations, calculates the output voltage for each pair, and selects the combination that minimizes the error between the calculated and target output voltage.

**Example**:

```python
from lib import find_resistor_values
from lib.common import convert_to_shorthand

vin = 12.0  # Input voltage in volts
vout = 5.0  # Desired output voltage in volts
maximum_current = 10.0  # Maximum allowable current in milliamps

r1, r2, error, current = find_resistor_values(vin=vin, vout=vout, maximum_current=maximum_current)
print(f"Best R1: {convert_to_shorthand(r1)}, Best R2: {convert_to_shorthand(r2)} with error: {error:.4f} and current: {current*1e3:.4f} mA")
```

## Project Structure

The project follows a modular structure:

```
OhmCalculators/
│
├── lib/
│   ├── common.py                   # Utility functions for converting resistor values and shorthand notations.
│   ├── e24_resistor_values.py      # Functions to generate E24 series resistor values.
│   └── voltage_divider.py          # Voltage divider calculation functions.
│
├── closest_parallel_resistor.py    # Functions for finding the best parallel resistor combination.
├── voltage_divider_resistances.py  # Functions for calculating the resistance values in a voltage divider circuit.
└── README.md                       # Project overview and documentation.
```

## Author

- [Carlos Valente](https://github.com/CFMVCarlos)