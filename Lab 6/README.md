# Lab 6 — Code and Branch Coverage

**Student:** Yashas  
**SRN:** PES2UG24CS609

The supplied fuel station application is tested with separate line and branch suites, using the required `CodeCoverageTest_...` and `BranchCoverageTest_...` file naming pattern.

## Run

Install `coverage` and `pytest`, then from this folder run:

```sh
coverage erase
coverage run --source=fuel_station -m pytest CodeCoverageTest_PES2UG24CS609_fuel_station.py
coverage report -m
coverage erase
coverage run --branch --source=fuel_station -m pytest BranchCoverageTest_PES2UG24CS609_fuel_station.py
coverage report -m
```

## Results

- Line coverage: 100% (18 tests passed).
- Branch coverage: 100% (22 tests passed; 26 of 26 branch paths covered).
- `CodeCoverageResults.txt` and `BranchCoverageResults.txt` contain the final terminal output transcripts.

The handout also requests terminal screenshots for both runs; the attached files are text transcripts rather than screenshots.
