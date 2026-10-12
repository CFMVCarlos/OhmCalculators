"""Find optimal parallel resistor pairs from standard E24 series."""

from src.core.common import convert_to_shorthand
from src.core.e24_resistor_values import all_resistor_values


def parallel_resistance(resistors: list[float]) -> float:
    """Calculate the equivalent resistance of resistors connected in parallel.

    The formula for parallel resistance is:
    1/R_eq = 1/R1 + 1/R2 + ... + 1/Rn

    Parameters
    ----------
    resistors : list[float]
        A list of resistor values (in ohms) connected in parallel.

    Returns
    -------
    float
        The equivalent resistance (in ohms) of the parallel combination.
    """
    # Using the parallel resistance formula: 1/R = sum(1/R_i)
    return 1 / sum(1 / r for r in resistors)


def find_best_parallel_combination(target_value: float) -> tuple[float, float, float]:
    """Find the two resistors that provide the closest parallel resistance.

    Parameters
    ----------
    target_value : float
        The target resistance value (in ohms) to approximate.

    Returns
    -------
    tuple[float, float, float]
        A tuple of (best_r1, best_r2, best_error).
    """
    best_r1: float = 0.0  # Best R1 value found
    best_r2: float = 0.0  # Best R2 value found
    best_error: float = float("inf")  # Initialize best error as infinity

    # List of all available resistor values
    all_values = list(all_resistor_values())

    # Iterate over all pairs of resistors (R1, R2)
    for r1 in all_values:
        for r2 in all_values:
            # Calculate the equivalent resistance for the current pair of resistors in parallel
            vout_calc: float = parallel_resistance([r1, r2])
            # Calculate the error between the target resistance and the calculated value
            error: float = abs(target_value - vout_calc)
            # If this combination gives a better (smaller) error, update the best combination
            if error < best_error:
                best_error = error
                best_r1 = r1
                best_r2 = r2

    return best_r1, best_r2, best_error


def convert_resistor_value(resistor_str: str) -> int:
    """Convert a resistor value from shorthand notation to numerical value.

    This function supports standard SI suffixes such as 'k' (kilo), 'm' (mega), and 'g' (giga).

    Parameters
    ----------
    resistor_str : str
        The resistor value in shorthand notation (e.g., '4k7', '4.7k').

    Returns
    -------
    int
        The numerical value of the resistor (in ohms).

    Raises
    ------
    ValueError
        If the input string does not represent a valid resistor value.
    """
    # Define the multipliers for SI suffixes
    suffix_multipliers = {
        "k": 1_000,
        "m": 1_000_000,
        "g": 1_000_000_000,
        "r": 1,
    }

    # Remove spaces and standardize the format (lowercase)
    resistor_str = resistor_str.replace(" ", "").lower()

    # If there is no suffix, simply convert the string to a float and return as an integer
    if resistor_str.isdigit():
        return int(float(resistor_str))

    # Search for the suffix and apply the appropriate multiplier
    for suffix, multiplier in suffix_multipliers.items():
        if suffix in resistor_str:
            # Handle decimal values by splitting the string
            if "." in resistor_str:
                value_str = resistor_str.split(suffix)[0]
                return int(float(value_str) * multiplier)
            else:
                # Handle integer values by inserting a decimal point before applying multiplier
                value_str = resistor_str.replace(suffix, ".")
                return int(float(value_str) * multiplier)

    # Raise an error if no valid suffix is found
    raise ValueError(f"Invalid resistor value: {resistor_str}")


# Example usage
if __name__ == "__main__":
    # Ask the user to input the target resistance in shorthand notation
    target_resistance = convert_resistor_value(input("Enter target resistance: "))

    # Check if the target resistance belongs to the standard set of resistor values
    belongs_to_set: bool = target_resistance in all_resistor_values()

    if belongs_to_set:
        print(f"Target resistance {target_resistance} belongs to the standard set.")
    else:
        # Find the best combination of two resistors that approximates the target resistance
        r1, r2, error = find_best_parallel_combination(target_resistance)
        print(
            f"Best combination: R1={convert_to_shorthand(r1)}, R2={convert_to_shorthand(r2)}, Error={error:.4f}"
        )

    # Pause the program to allow the user to see the result
    input("Press Enter to exit.")
