from collections.abc import Generator
from lib.voltage_divider_calculations import voltage_divider_calculations
from lib.common import convert_to_shorthand
from lib.e24_resistor_values import all_resistor_values


def find_resistor_values(
    vin: float, vout: float, maximum_current: float
) -> tuple[float, float, float, float]:
    """
    Finds the best resistor values for a voltage divider circuit that approximates
    the desired output voltage (vout) from the input voltage (vin) while ensuring
    the current doesn't exceed the specified maximum_current.

    Args:
        vin: The input voltage (in volts).
        vout: The desired output voltage (in volts).
        maximum_current: The maximum allowable current through the voltage divider (in milliamps).

    Returns:
        A tuple containing:
            best_r1: The value of resistor R1 (in ohms).
            best_r2: The value of resistor R2 (in ohms).
            best_error: The error between the calculated and desired output voltage.
            current: The current through the voltage divider (in amps).
    """

    best_r1: float = 0  # Best value for R1 (resistor 1)
    best_r2: float = 0  # Best value for R2 (resistor 2)
    best_error: float = float("inf")  # Initialize best error to infinity
    all_r1_values: Generator[float, None, None] = (
        all_resistor_values()
    )  # Generator for all resistor values

    # Iterate over all possible values for R1
    for r1 in all_r1_values:
        all_r2_values: Generator[float, None, None] = (
            all_resistor_values()
        )  # Generator for all resistor values

        # Iterate over all possible values for R2
        for r2 in all_r2_values:
            # Calculate the output voltage for the current resistor pair
            vout_calc: float | None = voltage_divider_calculations(
                vin=vin, r1=r1, r2=r2
            )

            # If the calculation results in None, skip this combination of resistors
            if vout_calc is None:
                continue

            # Calculate the error between the desired and calculated output voltage
            error: float = abs(vout - vout_calc)

            # Check if the current divider configuration is valid (current does not exceed maximum)
            # and if the error is better than the current best configuration
            if error < best_error and vin / (r1 + r2) <= maximum_current / 1e3:
                best_error = error  # Update best error
                best_r1 = r1  # Update best R1 value
                best_r2 = r2  # Update best R2 value

    # Calculate the current through the voltage divider
    current: float = vin / (best_r1 + best_r2)

    # Return the best resistor values, the error, and the current
    return best_r1, best_r2, best_error, current


if __name__ == "__main__":
    # User input for the input voltage (Vin)
    vin = float(input("Enter Vin: "))

    # User input for the desired output voltage (Vout)
    vout = float(input("Enter Vout: "))

    # User input for the maximum allowable current (in mA)
    maximum_current_str: str = input("Enter maximum current (mA): ")

    # Convert the maximum current from mA to A, defaulting to infinity if not provided
    maximum_current: float = (
        float(maximum_current_str) if maximum_current_str else float("inf")
    )

    # Find the best resistor values
    r1, r2, error, current = find_resistor_values(
        vin=vin, vout=vout, maximum_current=maximum_current
    )

    # Output the results to the user
    print(
        f"Best R1: {convert_to_shorthand(r1)}, Best R2: {convert_to_shorthand(r2)} "
        f"with error: {error:.4f} and a current of {current*1e3:.4f} mA"
    )

    # Pause the program before exit
    input("Press Enter to exit...")
