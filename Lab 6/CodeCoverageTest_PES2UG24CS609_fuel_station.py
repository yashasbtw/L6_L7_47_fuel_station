import pytest

from fuel_station import fuel_bill, pump_allowed, session_status


def test_fuel_bill_rejects_unknown_grade():
    with pytest.raises(ValueError, match="unknown fuel grade"):
        fuel_bill("kerosene", 20, "silver")


def test_fuel_bill_rejects_negative_litres():
    with pytest.raises(ValueError, match="invalid litres"):
        fuel_bill("regular", -1, "silver")


def test_fuel_bill_litres_covered_by_voucher():
    assert fuel_bill("regular", 8, "silver") == 0


def test_fuel_bill_gold_non_diesel_voucher():
    assert fuel_bill("premium", 20, "gold") == 0


def test_fuel_bill_regular_extra_uses_standard_rate():
    assert fuel_bill("regular", 20, "silver") == 1050


def test_fuel_bill_diesel_uses_diesel_rate():
    assert fuel_bill("diesel", 25, "silver") == 450


def test_fuel_bill_large_extra_applies_regular_discount():
    assert fuel_bill("regular", 45, "silver") == 35 * 99


def test_fuel_bill_large_extra_applies_gold_discount():
    assert fuel_bill("premium", 51, "gold") == 31 * 95


def test_pump_allowed_fleet_limit():
    assert pump_allowed(200, 3, True) is True


def test_pump_rejects_fleet_over_limit():
    assert pump_allowed(201, 1, True) is False


def test_pump_rejects_non_fleet_over_60_litres():
    assert pump_allowed(61, 1, False) is False


def test_pump_allows_single_container_non_fleet():
    assert pump_allowed(60, 1, False) is True


def test_pump_rejects_multiple_containers_non_fleet():
    assert pump_allowed(60, 2, False) is False


def test_card_day_active_at_cutoff():
    assert session_status(60, True, False) == "active"


def test_cash_day_warning_at_cutoff_minus_15():
    assert session_status(15, False, False) == "warning"


def test_night_cash_active_at_adjusted_cutoff():
    assert session_status(60, False, True) == "active"


def test_card_night_warning():
    assert session_status(75, True, True) == "warning"


def test_session_times_out_below_warning_window():
    assert session_status(14, False, False) == "timed_out"
