import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.voltage_divider_calculations import voltage_divider_calculations
from src.core.common import convert_to_shorthand
from src.core.closest_parallel_resistors import (
    find_best_parallel_combination,
    convert_resistor_value,
)
from src.core.voltage_divider_resistors_calculator import find_resistor_values

client = TestClient(app)


def test_voltage_divider_calculations_core():
    # Vin calculation
    vin = voltage_divider_calculations(vout=5.0, r1=1000.0, r2=1000.0)
    assert vin == 10.0

    # Vout calculation
    vout = voltage_divider_calculations(vin=10.0, r1=1000.0, r2=1000.0)
    assert vout == 5.0

    # Error handling
    with pytest.raises(ValueError, match="Insufficient data"):
        voltage_divider_calculations(vin=10.0, r1=1000.0)

    with pytest.raises(ValueError, match="Too many arguments"):
        voltage_divider_calculations(vin=10.0, vout=5.0, r1=1000.0, r2=1000.0)


def test_shorthand_conversions():
    assert convert_to_shorthand(4700) == "4.7k"
    assert convert_to_shorthand(1000000) == "1M"
    assert convert_resistor_value("4k7") == 4700.0
    assert convert_resistor_value("10R") == 10.0


def test_parallel_combination():
    r1, r2, error = find_best_parallel_combination(500.0)
    assert r1 > 0
    assert r2 > 0
    parallel_val = (r1 * r2) / (r1 + r2)
    assert abs(parallel_val - 500.0) < 5.0


def test_api_serve_frontend():
    response = client.get("/")
    assert response.status_code == 200
    assert "OhmCalculators" in response.text


def test_api_calculate_missing():
    # Calculate Vin
    response = client.post(
        "/api/calculate-missing",
        json={"vout": 5.0, "r1": 1000.0, "r2": 1000.0},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["calculated_parameter"] == "vin"
    assert data["data"]["value"] == 10.0


def test_api_best_parallel():
    response = client.post(
        "/api/best-parallel",
        json={"target_value": 500.0},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "r1" in data["data"]
    assert "r2" in data["data"]


def test_api_divider_resistors():
    response = client.post(
        "/api/divider-resistors",
        json={"vin": 12.0, "vout": 5.0, "maximum_current": 10.0},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "r1" in data["data"]
    assert "r2" in data["data"]
