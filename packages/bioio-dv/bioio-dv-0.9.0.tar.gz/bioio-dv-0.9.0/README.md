# bioio-dv

[![Build Status](https://github.com/bioio-devs/bioio-dv/actions/workflows/ci.yml/badge.svg)](https://github.com/bioio-devs/bioio-dv/actions)
[![Documentation](https://github.com/bioio-devs/bioio-dv/actions/workflows/docs.yml/badge.svg)](https://bioio-devs.github.io/bioio-dv)

A BioIO reader plugin for reading Digital Video (DV) files.

This plugin is intended to be used in conjunction with [bioio](https://github.com/bioio-devs/bioio)
---

## Installation

**Stable Release:** `pip install bioio-dv`<br>
**Development Head:** `pip install git+https://github.com/bioio-devs/bioio-dv.git`

## Quickstart

```python
from bioio_dv import Reader 

r = Reader("my-image.ext")
r.dims
```

## Documentation

For full package documentation please visit [bioio-devs.github.io/bioio-dv](https://bioio-devs.github.io/bioio-dv).

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for information related to developing the code.

**MIT License**
