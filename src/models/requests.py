"""Pydantic request models and validators for OhmCalculators endpoints."""

from typing import Optional, Self
from pydantic import BaseModel, model_validator


class VoltageDividerRequest(BaseModel):
    """Request model for solving an unknown variable in a voltage divider.

    Parameters
    ----------
    vin : Optional[float], default=None
        Input voltage in volts.
    vout : Optional[float], default=None
        Output voltage in volts.
    r1 : Optional[float], default=None
        Resistance of resistor R1 in ohms.
    r2 : Optional[float], default=None
        Resistance of resistor R2 in ohms.
    """

    vin: Optional[float] = None
    vout: Optional[float] = None
    r1: Optional[float] = None
    r2: Optional[float] = None

    @model_validator(mode="after")
    def check_inputs(self) -> Self:
        """Validate that exactly three of the four parameters are supplied.

        Returns
        -------
        Self
            Validated model instance.

        Raises
        ------
        ValueError
            If parameter count is invalid or physics constraints are violated.
        """
        provided = sum(
            [
                self.vin is not None,
                self.vout is not None,
                self.r1 is not None,
                self.r2 is not None,
            ]
        )
        if provided < 3:
            raise ValueError("Insufficient data. Provide exactly three parameters.")
        if provided > 3:
            raise ValueError(
                "Too many arguments provided. Provide at most three parameters."
            )

        # Validation rules based on calculations
        if self.r1 is None and self.vin == self.vout:
            raise ValueError("Vin and Vout cannot be equal when calculating R1.")
        if self.r2 is None and self.vin == self.vout:
            raise ValueError("Vin and Vout cannot be equal when calculating R2.")
        if self.vin is None and self.r2 == 0:
            raise ValueError("Resistance R2 cannot be zero when calculating Vin.")
        if self.vout is None and self.r1 == 0 and self.r2 == 0:
            raise ValueError("Total resistance (R1 + R2) cannot be zero.")

        if self.r1 is not None and self.r1 < 0:
            raise ValueError("Resistance R1 cannot be negative.")
        if self.r2 is not None and self.r2 < 0:
            raise ValueError("Resistance R2 cannot be negative.")

        return self


class TargetResistanceRequest(BaseModel):
    """Request model for approximating a target resistance with parallel resistors.

    Parameters
    ----------
    target_value : float
        Target resistance in ohms (must be greater than 0).
    """

    target_value: float

    @model_validator(mode="after")
    def check_target(self) -> Self:
        """Validate that the target resistance is strictly positive.

        Returns
        -------
        Self
            Validated model instance.

        Raises
        ------
        ValueError
            If target_value is less than or equal to zero.
        """
        if self.target_value <= 0:
            raise ValueError("Target resistance must be greater than 0.")
        return self


class ResistorDivRequest(BaseModel):
    """Request model for selecting standard resistors for a voltage divider.

    Parameters
    ----------
    vin : float
        Input voltage in volts.
    vout : float
        Output voltage in volts.
    maximum_current : float
        Maximum allowed current in milliamps.
    """

    vin: float
    vout: float
    maximum_current: float

    @model_validator(mode="after")
    def check_voltages(self) -> Self:
        """Validate voltage and current constraints for divider calculation.

        Returns
        -------
        Self
            Validated model instance.

        Raises
        ------
        ValueError
            If voltages or current violate circuit feasibility.
        """
        if self.vin <= 0:
            raise ValueError("Input voltage (vin) must be greater than 0.")
        if self.vout <= 0:
            raise ValueError("Output voltage (vout) must be greater than 0.")
        if self.vout >= self.vin:
            raise ValueError("Output voltage (vout) must be less than input voltage (vin).")
        if self.maximum_current <= 0:
            raise ValueError("Maximum current must be greater than 0.")
        return self
