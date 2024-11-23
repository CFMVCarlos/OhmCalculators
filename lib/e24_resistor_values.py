from collections.abc import Generator

# List of base resistor values in the E24 series (values between 1 and 10)
# These values are multiplied by powers of 10 to generate the standard resistor values.
RESISTOR_BASE_VALUES: list[float] = [
    1.0,
    1.1,
    1.2,
    1.3,
    1.5,
    1.6,
    1.8,
    2.0,
    2.2,
    2.4,
    2.7,
    3.0,
    3.3,
    3.6,
    3.9,
    4.3,
    4.7,
    5.1,
    5.6,
    6.2,
    6.8,
    7.5,
    8.2,
    9.1,
]


def all_resistor_values() -> Generator[float, None, None]:
    """
    Generates all standard resistor values in the E24 series.

    The E24 series includes resistors with base values that are multiplied by powers of 10
    (1, 10, 100, etc.) to produce a range of resistor values. This generator yields each of these values
    rounded to one decimal place.

    The standard E24 values range from 1 ohm to 9.1 megaohms and follow a logarithmic scale.

    Yields:
        float: The next resistor value in the E24 series.
    """
    # Loop through six powers of 10 (1, 10, 100, 1000, 10000, 100000)
    for i in range(6):
        # For each base value (e.g., 1.0, 1.1, ..., 9.1), multiply it by the current power of 10
        for j in RESISTOR_BASE_VALUES:
            # Yield the calculated value, rounded to one decimal place
            yield round(j * (10**i), 1)
