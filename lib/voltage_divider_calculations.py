def voltage_divider_calculations(
    vin: float | None = None,
    vout: float | None = None,
    r1: float | None = None,
    r2: float | None = None,
) -> float | None:
    """
    Calculate a missing value in a voltage divider circuit based on the available inputs.

    The voltage divider equation is:
        Vout = Vin * (R2 / (R1 + R2))  (for calculating Vout)
        Vin = Vout * (R1 + R2) / R2    (for calculating Vin)
        R1 = (Vout * R2) / (Vin - Vout) (for calculating R1)
        R2 = (Vout * R1) / (Vin - Vout) (for calculating R2)

    Args:
        vin: The input voltage (Vin). Optional.
        vout: The output voltage (Vout). Optional.
        r1: The resistance R1 in ohms. Optional.
        r2: The resistance R2 in ohms. Optional.

    Returns:
        The calculated value (Vin, Vout, R1, or R2) based on the inputs provided.

    Raises:
        ValueError: If there is insufficient data to perform the calculation or too many arguments are provided.
    """

    # If Vin is not provided, calculate Vin based on the other values
    if vin is None:
        # Ensure vout, r1, and r2 are provided to calculate Vin
        if vout is None or r1 is None or r2 is None:
            raise ValueError(
                "Insufficient data to calculate Vin. Provide Vout, R1, and R2."
            )
        # Calculate Vin using the rearranged voltage divider formula: Vin = Vout * (R1 + R2) / R2
        return vout * (r1 + r2) / r2

    # If Vout is not provided, calculate Vout based on the other values
    if vout is None:
        # Ensure vin, r1, and r2 are provided to calculate Vout
        if vin is None or r1 is None or r2 is None:
            raise ValueError(
                "Insufficient data to calculate Vout. Provide Vin, R1, and R2."
            )
        # Calculate Vout using the voltage divider formula: Vout = Vin * (R2 / (R1 + R2))
        return vin * (r2 / (r1 + r2))

    # If R1 is not provided, calculate R1 based on the other values
    if r1 is None:
        # Ensure vout, vin, and r2 are provided to calculate R1
        if vout is None or vin is None or r2 is None:
            raise ValueError(
                "Insufficient data to calculate R1. Provide Vout, Vin, and R2."
            )
        # Calculate R1 using the rearranged formula: R1 = (Vout * R2) / (Vin - Vout)
        return vout * r2 / (vin - vout)

    # If R2 is not provided, calculate R2 based on the other values
    if r2 is None:
        # Ensure vout, vin, and r1 are provided to calculate R2
        if vout is None or vin is None or r1 is None:
            raise ValueError(
                "Insufficient data to calculate R2. Provide Vout, Vin, and R1."
            )
        # Calculate R2 using the rearranged formula: R2 = (Vout * R1) / (Vin - Vout)
        return vout * r1 / (vin - vout)

    # If all four parameters are provided, raise an error because too many arguments are given
    raise ValueError("Too many arguments provided. Provide at most three parameters.")
