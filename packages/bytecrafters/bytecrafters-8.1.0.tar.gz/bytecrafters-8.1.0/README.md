# bytecrafters

[![PyPI Version](https://img.shields.io/pypi/v/bytecrafters.svg)](https://pypi.org/project/bytecrafters/)
[![License](https://img.shields.io/pypi/l/bytecrafters.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/bytecrafters.svg)](https://pypi.org/project/bytecrafters/)

## Abstract

This is a package containing various utilities and libraries. So far:

- Signal Analyzer (to plot diagrams about a mono-dimensional signal meant as a y=y(t), where you have times and values in a CSV, or in audio files)

This README is supposed to be very high level and summarized. More details are available in the 'docs' subfolder of the package.

## Installation

You can install the package using pip:

```bash
pip install bytecrafters
```

## Python Dependencies

- Python: from 3.8 to 3.11.6

- numpy >= 1.23.5
- PyYAML >= 6.0
- pandas >= 2.0.1
- chardet >= 4.0.0
- scipy >= 1.10.1
- matplotlib >= 3.7.1

Optionally (for advanced plots):
- PyWavelets >= 1.4.1

Optionally (for audio file processing):
- pydub >= 0.25.1
- moviepy >= 1.0.3

## Other Dependencies

- on Windows: FFMPEG executable (6.0 or upper) available in the system PATH (note, needed only for audio files processing)
- on Unix: unknown (tests pending)

## Usage
Assuming `${PACKAGE_HOME}` is where the package is available after the install (typically under `${PYTHON_HOME}/Lib/site-packages/bytecrafters` or alike),
enter the following command from a command shell:

```bash
python "${PACKAGE_HOME}/signalprocessing.py" <parameters>
```
## Example (CSV file processing)

```bash
... .. /signalprocessing.py --input-path ./inputdata.csv --qplot time_1 signal_1 --include-histogram --out-directory ./out
```

Explanation:
This would process a csv file named inputdata.csv, placed in the current directory, looking for a header with columns
named 'time_1' and 'signal_1', saving the results into a subdirectory of the current directory named 'out'.
Plots typically generated are Fourier Transform and others. Also, a CSV of the Fourier Transform is saved.
Note: the destination directories need to be existing. Also: a directory named 'logs' has to be created in the current directory
for the logs to be saved.

Many other details about the available flags and parameters can be found in the documentation downloaded.
