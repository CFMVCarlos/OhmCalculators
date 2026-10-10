from pydantic import BaseModel, model_validator
from typing import Optional


class VoltageDividerRequest(BaseModel):
    vin: Optional[float] = None
    vout: Optional[float] = None
    r1: Optional[float] = None
    r2: Optional[float] = None

    @model_validator(mode="after")
    def check_inputs(self):
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
    target_value: float

    @model_validator(mode="after")
    def check_target(self):
        if self.target_value <= 0:
            raise ValueError("Target resistance must be greater than 0.")
        return self


class ResistorDivRequest(BaseModel):
    vin: float
    vout: float
    maximum_current: float

    @model_validator(mode="after")
    def check_voltages(self):
        if self.vin <= 0:
            raise ValueError("Vin must be greater than 0.")
        if self.vout < 0:
            raise ValueError("Vout cannot be negative.")
        if self.maximum_current <= 0:
            raise ValueError("Maximum current must be greater than 0.")
        if self.vout >= self.vin:
            raise ValueError("Vout must be less than Vin in a passive voltage divider.")
        return self
