# Wave Cracker

[![PyPI Version](https://img.shields.io/pypi/v/wavecracker.svg)](https://pypi.org/project/wavecracker/)
[![License](https://img.shields.io/pypi/l/wavecracker.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/wavecracker.svg)](https://pypi.org/project/wavecracker/)

## Abstract

Wave Cracker

Python batch tool for signal time/frequency analysis (input data: CSV or audio files).

Detailed documentation: [here](https://github.com/pmatteo68/wavecracker)

This project was formerly known as [bytecrafters](https://pypi.org/project/bytecrafters)

## Installation

You can install the package using pip:

```bash
python -m pip install wavecracker
```

## Python Dependencies

- Python: >= 3.7 (preferably: > 3.8 and < 3.12, ref. documentation for additional details)

- numpy >= 1.23.5
- PyYAML >= 6.0
- pandas >= 2.0.1
- chardet >= 4.0.0
- scipy >= 1.10.1
- matplotlib >= 3.7.1

Optionally (for wavelet transform):
- PyWavelets >= 1.4.1

Optionally (for audio file processing):
- pydub >= 0.25.1
- moviepy >= 1.0.3

Optionally (for hardware detailed diagnostics upon boot):
- psutil >= 5.9.5

## Installing extras

The following commands allow the installation of the extras correspondent to the optional dependencies above mentioned:

```bash
python -m pip install wavecracker[wavelet]
python -m pip install wavecracker[audio]
python -m pip install wavecracker[hwdiagnostics]
```

Note that some of these extras may or may not work depending on the Python version. More information in the documentation.

## Other Dependencies

The following directory are needed in the `PATH`:
- `PYTHON_HOME` and `PYTHON_HOME/Scripts`
- The directory containing the FFMPEG executable (6.0 or upper; note, needed only for audio files processing)

## Usage
Assuming `${PACKAGE_HOME}` is where the package is available after the install (typically under `${PYTHON_HOME}/Lib/site-packages/wavecracker` or alike),
enter the following command from a command shell:

```bash
python "${PACKAGE_HOME}/signalanalyzer.py" <parameters>
```

## Example (CSV file processing)

```bash
... .. /signalanalyzer.py --input-path ./inputdata.csv --qplot time_1 signal_1 --include-histogram --out-directory ./out
```

Explanation:
This would process a csv file named inputdata.csv, placed in the current directory, looking for a header with columns
named 'time_1' and 'signal_1', saving the results into a subdirectory of the current directory named 'out'.
Plots typically generated are Fourier Transform and others. Also, a CSV of the Fourier Transform is saved.
Note: the destination directories need to be existing. Also: a directory named 'logs' has to be created in the current directory
for the logs to be saved.

Many other details about the available flags and parameters can be found in the documentation.
