"""Property-based fuzz tests for the fuel station input functions."""

import math

import pytest
from hypothesis import given, strategies as st

from fuel_station import parse_purchase, payable_bill, volume_average


@given(st.one_of(st.text(), st.none()))
def test_parse_purchase_fuzzes_arbitrary_text(value):
    if value is None:
        with pytest.raises(ValueError):
            parse_purchase(value)
        return
    try:
        grade, litres = parse_purchase(value)
    except ValueError:
        return
    assert grade in {"Diesel", "Regular", "Premium"}
    assert math.isfinite(litres)
    assert litres >= 0


@given(st.one_of(st.text(), st.none()))
def test_volume_average_fuzzes_arbitrary_text(value):
    if value is None:
        with pytest.raises(ValueError):
            volume_average(value)
        return
    try:
        average = volume_average(value)
    except ValueError:
        return
    assert isinstance(average, int)
    assert average >= 0


@given(st.one_of(st.text(), st.none()))
def test_payable_bill_fuzzes_arbitrary_text(value):
    if value is None:
        with pytest.raises(ValueError):
            payable_bill(value)
        return
    try:
        amount = payable_bill(value)
    except ValueError:
        return
    assert math.isfinite(amount)
    assert amount >= 0


@given(
    st.sampled_from(["diesel", "regular", "premium", "DIESEL"]),
    st.floats(
        min_value=0,
        max_value=1_000_000,
        allow_nan=False,
        allow_infinity=False,
    ),
)
def test_valid_purchase_round_trips(grade, litres):
    result_grade, result_litres = parse_purchase(f"{grade}:{litres}")
    assert result_grade == grade.title()
    assert result_litres == litres


@given(st.lists(st.integers(min_value=0, max_value=1_000_000), min_size=1))
def test_volume_average_is_floor_average(values):
    csv = ",".join(str(value) for value in values)
    assert volume_average(csv) == sum(values) // len(values)


@given(
    st.floats(
        min_value=0,
        max_value=1_000_000,
        allow_nan=False,
        allow_infinity=False,
    ),
    st.floats(
        min_value=0,
        max_value=1_000_000,
        allow_nan=False,
        allow_infinity=False,
    ),
)
def test_payable_bill_is_taxed_and_never_negative(bill, discount):
    result = payable_bill(f"{bill}|{discount}")
    assert result == max(bill * 1.18 - discount, 0.0)


@pytest.mark.parametrize(
    "value",
    [
        None,
        "",
        "diesel",
        "diesel:abc",
        "diesel:nan",
        "diesel:-1",
        "petrol:1",
        "diesel:1:2",
    ],
)
def test_parse_purchase_rejects_invalid_values(value):
    with pytest.raises(ValueError):
        parse_purchase(value)


@pytest.mark.parametrize("value", [None, "", "1,,2", "x", "-1", "1,2,3.5"])
def test_volume_average_rejects_invalid_values(value):
    with pytest.raises(ValueError):
        volume_average(value)


@pytest.mark.parametrize(
    "value", [None, "", "no|1", "100|-1", "nan|0", "100|0|1"]
)
def test_payable_bill_rejects_invalid_values(value):
    with pytest.raises(ValueError):
        payable_bill(value)
