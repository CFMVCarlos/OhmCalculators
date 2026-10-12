"""Formulas for solving unknown variables in voltage divider circuits."""

def voltage_divider_calculations(
    vin: float | None = None,
    vout: float | None = None,
    r1: float | None = None,
    r2: float | None = None,
) -> float | None:
    """Calculate a missing value in a voltage divider circuit.

    Parameters
    ----------
    vin : float | None, default=None
        The input voltage (Vin).
    vout : float | None, default=None
        The output voltage (Vout).
    r1 : float | None, default=None
        The resistance R1 in ohms.
    r2 : float | None, default=None
        The resistance R2 in ohms.

    Returns
    -------
    float | None
        The calculated value based on the inputs provided.

    Raises
    ------
    ValueError
        If there is insufficient data or too many arguments provided.
    """

    inputs = [x is not None for x in (vin, vout, r1, r2)]
    if sum(inputs) > 3:
        raise ValueError(
            "Too many arguments provided. Provide at most three parameters."
        )
    if sum(inputs) < 3:
        raise ValueError("Insufficient data. Provide exactly three parameters.")

    if r1 is not None and r1 < 0:
        raise ValueError("Resistance R1 cannot be negative.")
    if r2 is not None and r2 < 0:
        raise ValueError("Resistance R2 cannot be negative.")

    # If Vin is not provided, calculate Vin based on the other values
    if vin is None:
        if r2 == 0:
            raise ValueError("Resistance R2 cannot be zero when calculating Vin.")
        return vout * (r1 + r2) / r2  # type: ignore

    # If Vout is not provided, calculate Vout based on the other values
    if vout is None:
        if r1 + r2 == 0:  # type: ignore
            raise ValueError("Total resistance (R1 + R2) cannot be zero.")
        return vin * (r2 / (r1 + r2))  # type: ignore

    # If R1 is not provided, calculate R1 based on the other values
    if r1 is None:
        if vin == vout:
            raise ValueError("Vin and Vout cannot be equal when calculating R1.")
        return vout * r2 / (vin - vout)  # type: ignore

    # If R2 is not provided, calculate R2 based on the other values
    if r2 is None:
        if vin == vout:
            raise ValueError("Vin and Vout cannot be equal when calculating R2.")
        return vout * r1 / (vin - vout)  # type: ignore

    return None
