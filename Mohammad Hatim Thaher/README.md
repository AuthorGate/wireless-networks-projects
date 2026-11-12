# Physiological-Signal-Based Key Agreement for WBAN (IEEE 802.15.6)

Wireless Networks project report, An-Najah National University.

- **Student:** Mohammad Hatim (12217371)
- **Instructor:** Dr. Jihad Hamamreh

📄 **Report PDF:** [main.pdf](main.pdf)

## Summary

Two sensors on the same body derive an identical cryptographic key from the patient's ECG
(inter-pulse intervals), so the key is never transmitted over the air. A Bloom filter reconciles
the sensors' features without revealing them, and HMAC confirms the agreement. Simulated on the
MIT-BIH Arrhythmia Database (Record 103).

The simulation code is based on [adcondev/physio-key-gen](https://github.com/adcondev/physio-key-gen).

## Build

Open the folder in VS Code with the LaTeX Workshop extension and save `main.tex`, or run:

```
pdflatex main
bibtex main
pdflatex main
pdflatex main
```
