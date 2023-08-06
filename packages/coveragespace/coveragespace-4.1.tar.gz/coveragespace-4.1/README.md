# Overview

The official command-line client for [The Coverage Space](http://coverage.space).

[![Unix Build Status](https://img.shields.io/travis/jacebrowning/coverage-space-cli/main.svg?label=unix)](https://travis-ci.org/jacebrowning/coverage-space-cli)
[![Windows Build Status](https://img.shields.io/appveyor/ci/jacebrowning/coverage-space-cli/main.svg?label=window)](https://ci.appveyor.com/project/jacebrowning/coverage-space-cli)
[![Coverage Status](https://img.shields.io/coveralls/jacebrowning/coverage-space-cli/main.svg)](https://coveralls.io/r/jacebrowning/coverage-space-cli)
[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/jacebrowning/coverage-space-cli.svg)](https://scrutinizer-ci.com/g/jacebrowning/coverage-space-cli/?branch=main)
[![PyPI Version](https://img.shields.io/pypi/v/coveragespace.svg)](https://pypi.org/project/coveragespace)
[![PyPI License](https://img.shields.io/pypi/l/coveragespace.svg)](https://pypi.org/project/coveragespace)

# Setup

## Requirements

- Python 3.6+

## Installation

Install this tool globally with [pipx](https://pipxproject.github.io/pipx/) (or pip):

```text
$ pipx install coveragespace
```
or add it to your [Poetry](https://python-poetry.org/docs/) project:

```text
$ poetry add coveragespace
```

# Usage

To update the value for a test coverage metric:

```text
$ coveragespace update <metric>
```

where `<metric>` is one of:

- **unit**
- **integration**
- **overall**

For example, after running unit tests with code coverage enabled:

```text
$ coveragespace update unit
```

which will attempt to extract the current coverage data from your project directory and compare that with the last known value. The coverage value can also be manually specified:

```text
$ coveragespace update <metric> <value>
```
