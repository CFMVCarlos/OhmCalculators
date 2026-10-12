"""FastAPI router endpoints for voltage divider and parallel resistor calculators."""

from typing import Any
from fastapi import APIRouter, HTTPException
from src.core.common import convert_to_shorthand
from src.models.requests import (
    ResistorDivRequest,
    TargetResistanceRequest,
    VoltageDividerRequest,
)
from src.services.calculator import (
    calculate_best_parallel,
    calculate_divider_resistors,
    calculate_voltage_divider,
)

router = APIRouter()


@router.post("/calculate-missing")
async def calculate_missing(request: VoltageDividerRequest) -> dict[str, Any]:
    """Calculate the missing parameter in a voltage divider circuit.

    Parameters
    ----------
    request : VoltageDividerRequest
        Request payload containing exactly three of vin, vout, r1, r2.

    Returns
    -------
    dict[str, Any]
        Dictionary containing status and calculated parameter value.

    Raises
    ------
    HTTPException
        If validation fails (400) or calculation fails unexpectedly (500).
    """
    try:
        result = calculate_voltage_divider(
            vin=request.vin, vout=request.vout, r1=request.r1, r2=request.r2
        )
        # Find which parameter was calculated
        missing_param = None
        if request.vin is None:
            missing_param = "vin"
        elif request.vout is None:
            missing_param = "vout"
        elif request.r1 is None:
            missing_param = "r1"
        elif request.r2 is None:
            missing_param = "r2"

        return {
            "status": "success",
            "data": {"calculated_parameter": missing_param, "value": result},
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


@router.post("/best-parallel")
async def best_parallel(request: TargetResistanceRequest) -> dict[str, Any]:
    """Find the best two E24 parallel resistors approximating a target resistance.

    Parameters
    ----------
    request : TargetResistanceRequest
        Request payload containing target_value in ohms.

    Returns
    -------
    dict[str, Any]
        Dictionary containing status, resistor values, shorthand, and error.

    Raises
    ------
    HTTPException
        If calculation fails unexpectedly (500).
    """
    try:
        r1, r2, error = calculate_best_parallel(request.target_value)
        return {
            "status": "success",
            "data": {
                "r1": r1,
                "r1_shorthand": convert_to_shorthand(r1),
                "r2": r2,
                "r2_shorthand": convert_to_shorthand(r2),
                "error": error,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/divider-resistors")
async def divider_resistors(request: ResistorDivRequest) -> dict[str, Any]:
    """Find optimal resistor values for a voltage divider circuit.

    Parameters
    ----------
    request : ResistorDivRequest
        Request payload containing vin, vout, and maximum_current.

    Returns
    -------
    dict[str, Any]
        Dictionary containing status, best resistor values, error, and current.

    Raises
    ------
    HTTPException
        If calculation fails unexpectedly (500).
    """
    try:
        r1, r2, error, current = calculate_divider_resistors(
            request.vin, request.vout, request.maximum_current
        )
        return {
            "status": "success",
            "data": {
                "r1": r1,
                "r1_shorthand": convert_to_shorthand(r1),
                "r2": r2,
                "r2_shorthand": convert_to_shorthand(r2),
                "error": error,
                "current": current,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
