# Source of this code

This simulation code is taken from the open-source repository
**physio-key-gen** by Adrián Constante (originally published as SenoReload/PhysioKeyGen, 2020):

https://github.com/adcondev/physio-key-gen

It is used under the MIT License (see `LICENSE`).

## Changes made for this project (Mohammad Hatim Thaher)

- `BloomFilter.py`: fixed `check()`, which returned after testing only the first of the
  k hash positions. It now checks all k positions. This lowered the measured false-positive rate
  from 49.5% to 0.093% (design target 0.096%).
- `KeyAgreement.py`: added an execution-time measurement for key generation and agreement.

The ECG data in `physionet2/` is Record 103 of the MIT-BIH Arrhythmia Database (PhysioNet).
