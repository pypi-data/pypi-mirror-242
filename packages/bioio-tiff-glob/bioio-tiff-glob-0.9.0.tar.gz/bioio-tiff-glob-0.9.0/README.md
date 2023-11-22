# bioio-tiff-glob

[![Build Status](https://github.com/bioio-devs/bioio-tiff-glob/actions/workflows/ci.yml/badge.svg)](https://github.com/bioio-devs/bioio-tiff-glob/actions)
[![Documentation](https://github.com/bioio-devs/bioio-tiff-glob/actions/workflows/docs.yml/badge.svg)](https://bioio-devs.github.io/bioio-tiff-glob)

A BioIo reader for reading Tiff Glob images

This plugin is intended to be used in conjunction with [bioio](https://github.com/bioio-devs/bioio)
---

## Installation

**Stable Release:** `pip install bioio-tiff-glob`<br>
**Development Head:** `pip install git+https://github.com/bioio-devs/bioio-tiff-glob.git`

## Quickstart

```python
from bioio_tiff_glob import Reader 

r = Reader("my-image.ext")
r.dims
```

## Documentation

For full package documentation please visit [bioio-devs.github.io/bioio-tiff-glob](https://bioio-devs.github.io/bioio-tiff-glob).

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for information related to developing the code.

**MIT License**
