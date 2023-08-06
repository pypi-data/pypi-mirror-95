# lektor-youtube-embed

[![Run tests](https://github.com/cigar-factory/lektor-youtube-embed/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/cigar-factory/lektor-youtube-embed/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/cigar-factory/lektor-youtube-embed/branch/main/graph/badge.svg?token=2bz0MnPazy)](https://codecov.io/gh/cigar-factory/lektor-youtube-embed)
[![PyPI Version](https://img.shields.io/pypi/v/lektor-youtube-embed.svg)](https://pypi.org/project/lektor-youtube-embed/)
![License](https://img.shields.io/pypi/l/lektor-youtube-embed.svg)
![Python Compatibility](https://img.shields.io/badge/dynamic/json?query=info.requires_python&label=python&url=https%3A%2F%2Fpypi.org%2Fpypi%2Flektor-youtube-embed%2Fjson)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)


Lektor template filter to convert youtube links to embeds

## Installation

```
pip install lektor-youtube-embed
```

## Usage

```
{{ "https://www.youtube.com/watch?v=9Yk9iRDESDo" | youtube }}
```

```
{{ "https://youtu.be/BdXDT-5jci0" | youtube(width=640, height=480, attrs={'class': 'video'}) }}
```
