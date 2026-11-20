# Lab 7 - Fuel Station Fuzz Testing

**Student:** Yashas  
**SRN:** PES2UG24CS609

The assigned repository names the program `fuel_station.py` and its tests `test_fuel_station.py`; the handout's generic example refers to `processor.py` and `test_processor.py`. These files retain the names already used by the assigned repository.

## Run

Install `pytest` and `hypothesis`, then run `python -m pytest -q test_fuel_station.py` from this folder. Run the example program with `python fuel_station.py`.

The tests cover arbitrary text and `None` values, valid input properties, malformed separators, empty entries, unsupported grades, negative numbers, and non-finite amounts. The final run passed 26 tests.

`Lab7_Execution_Transcript.pdf` records the actual command outputs. It is a text transcript, not a screenshot; the handout's requested screenshots still need to be captured from the student's environment.
