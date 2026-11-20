import pytest

from fuel_station import fuel_bill, pump_allowed, session_status


@pytest.mark.parametrize(
    ("grade", "litres", "tier", "expected"),
    [
        ("regular", 8, "silver", 0),
        ("premium", 20, "gold", 0),
        ("diesel", 25, "silver", 450),
        ("regular", 20, "silver", 1050),
        ("regular", 45, "silver", 35 * 99),
        ("premium", 51, "gold", 31 * 95),
    ],
)
def test_fuel_bill_decision_branches(grade, litres, tier, expected):
    assert fuel_bill(grade, litres, tier) == expected


@pytest.mark.parametrize(
    ("grade", "litres", "tier", "message"),
    [
        ("unknown", 20, "silver", "unknown fuel grade"),
        ("regular", -1, "silver", "invalid litres"),
    ],
)
def test_fuel_bill_validation_branches(grade, litres, tier, message):
    with pytest.raises(ValueError, match=message):
        fuel_bill(grade, litres, tier)


@pytest.mark.parametrize(
    ("litres", "containers", "fleet", "expected"),
    [
        (200, 2, True, True),
        (201, 1, True, False),
        (61, 1, False, False),
        (60, 1, False, True),
        (60, 2, False, False),
    ],
)
def test_pump_allowed_decision_branches(litres, containers, fleet, expected):
    assert pump_allowed(litres, containers, fleet) is expected


@pytest.mark.parametrize(
    ("seconds", "card", "night", "expected"),
    [
        (60, True, False, "active"),
        (59, True, False, "warning"),
        (44, True, False, "timed_out"),
        (30, False, False, "active"),
        (15, False, False, "warning"),
        (14, False, False, "timed_out"),
        (90, True, True, "active"),
        (75, True, True, "warning"),
        (74, True, True, "timed_out"),
    ],
)
def test_session_status_decision_branches(seconds, card, night, expected):
    assert session_status(seconds, card, night) == expected
