# plot-wav

[![PyPi](https://badge.fury.io/py/plot-wav.svg)](https://pypi.python.org/pypi/plot-wav/)
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

This project is a tool for drawing wav files with various acoustic transformations.

## Requirement

- Python3

## Usage

```sh
$ plot-wav --<type> -i <input file> # -o <output file>
```

If no `-o` option is specified, the image will be displayed directly.

The types of conversion are as follows.

- `--wave` - original wave
- `--spec` - spectrogram
- `--mfcc` - MFCC

### Show help

```sh
$ plot-wav -h
```

## Installation

```sh
$ pip install plot-wav
```
