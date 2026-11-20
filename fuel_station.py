"""Parse fuel purchases and calculate pump-volume and payment values."""

import math

FUEL_GRADES = {"diesel", "regular", "premium"}


def _finite_nonnegative(value: float, label: str) -> float:
    """Validate a numeric amount used by the public input functions."""
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"{label} must be a finite, non-negative number")
    return value


def parse_purchase(text: str) -> tuple[str, float]:
    """Parse ``grade:litres`` and reject incomplete or invalid purchases."""
    if not isinstance(text, str):
        raise ValueError("purchase must be text in grade:litres format")
    parts = text.split(":")
    if len(parts) != 2:
        raise ValueError("purchase must contain exactly one ':' separator")
    grade_text, litres_text = (part.strip() for part in parts)
    grade = grade_text.casefold()
    if grade not in FUEL_GRADES:
        raise ValueError("grade must be diesel, regular, or premium")
    if not litres_text:
        raise ValueError("litres cannot be empty")
    try:
        litres = float(litres_text)
    except ValueError as exc:
        raise ValueError("litres must be numeric") from exc
    return grade.title(), _finite_nonnegative(litres, "litres")


def volume_average(volumes_csv: str) -> int:
    """Return the floor average of a non-empty CSV of whole litre values."""
    if not isinstance(volumes_csv, str):
        raise ValueError("pump volumes must be supplied as CSV text")
    tokens = [token.strip() for token in volumes_csv.split(",")]
    if not tokens or any(not token for token in tokens):
        raise ValueError("pump volumes cannot be empty")
    try:
        values = [int(token) for token in tokens]
    except ValueError as exc:
        raise ValueError("pump volumes must be whole numbers") from exc
    if any(value < 0 for value in values):
        raise ValueError("pump volumes cannot be negative")
    return sum(values) // len(values)


def payable_bill(text: str) -> float:
    """Calculate tax-inclusive bill less discount, with a zero floor."""
    if not isinstance(text, str):
        raise ValueError("bill must be text in bill|discount format")
    parts = text.split("|")
    if len(parts) != 2:
        raise ValueError("bill must contain exactly one '|' separator")
    bill_text, discount_text = (part.strip() for part in parts)
    try:
        bill = _finite_nonnegative(float(bill_text), "bill")
        discount = _finite_nonnegative(float(discount_text), "discount")
    except ValueError as exc:
        raise ValueError(
            "bill and discount must be finite non-negative numbers"
        ) from exc
    return max(bill * 1.18 - discount, 0.0)


def main() -> None:
    """Run the three examples, reporting invalid input without a traceback."""
    actions = (
        (
            "parse_purchase",
            "Enter grade:litres (e.g. diesel:25): ",
            parse_purchase,
        ),
        (
            "volume_average",
            "Enter pump volumes as CSV (e.g. 10,25,40): ",
            volume_average,
        ),
        (
            "payable_bill",
            "Enter bill|discount (e.g. 2500|100): ",
            payable_bill,
        ),
    )
    for label, prompt, action in actions:
        print(f"==== Running {label} ====")
        try:
            print("Result:", action(input(prompt)))
        except ValueError as exc:
            print("Invalid input:", exc)
        print()


if __name__ == "__main__":
    main()
