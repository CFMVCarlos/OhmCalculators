def convert_to_shorthand(number: float) -> str:
    """
    Convert a number to a shorthand notation with suffixes (e.g., 10000 -> '10k', 1000000 -> '1M').

    This function takes a floating-point number and converts it into a more readable format by
    applying common metric prefixes: k (thousand), M (million), and G (billion).
    For values smaller than 1000, the function simply returns the number as a string.

    Args:
        number (float): The number to be converted to shorthand notation.

    Returns:
        str: The shorthand notation of the input number.
    """

    # Define suffixes and their corresponding thresholds
    suffixes = [
        (1_000_000_000, "G"),  # 1 billion (G for Giga)
        (1_000_000, "M"),  # 1 million (M for Mega)
        (1_000, "k"),  # 1 thousand (k for kilo)
    ]

    # Loop through the suffixes and check if the number is greater than or equal to the threshold
    for factor, suffix in suffixes:
        if number >= factor:
            # Calculate the shorthand value by dividing the number by the factor
            value = round(number / factor, 1)
            # Return the value with the appropriate suffix (e.g., "10k" for 10000)
            return f"{value:g}{suffix}"

    # If the number is less than 1000, return it as a string without any suffix
    return str(number)
