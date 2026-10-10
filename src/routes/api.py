from fastapi import APIRouter, HTTPException
from src.models.requests import (
    VoltageDividerRequest,
    TargetResistanceRequest,
    ResistorDivRequest,
)
from src.services.calculator import (
    calculate_voltage_divider,
    calculate_best_parallel,
    calculate_divider_resistors,
)
from lib.common import convert_to_shorthand

router = APIRouter()


@router.post("/calculate-missing")
async def calculate_missing(request: VoltageDividerRequest):
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
async def best_parallel(request: TargetResistanceRequest):
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
async def divider_resistors(request: ResistorDivRequest):
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
                "current_amps": current,
                "current_ma": current * 1000,
            },
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
