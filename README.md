Cognite Python Utilities
========================
[![Test and Build](https://github.com/cognitedata/cognite-python-utils/workflows/test_and_build/badge.svg)](https://github.com/cognitedata/cognite-python-utils/actions?query=workflow:test_and_build)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](https://cognitedata.github.io/cognite-python-utils/development/covenant.html)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a package of utilities extending the use of Cognite products. Its aim is to assist
Cognite users with common/recurrent workflows and applications.

## Directory Structure

```
├── cognite                         <- Source code
│   └── utils
│       ├── contextualization       <- Functionalities relating to contextualization
│       ├── infrastructure          <- Functionalities relating to infrastructure
│       ├── ...
│       └── __init__.py
```

## Getting Started

To install this package, run:

```bash
$ pip install cognite-utils
```

Or, if using [poetry](https://python-poetry.org/docs/), run:

```bash
$ poetry add cognite-utils
```

The following shows how you can load functionalities in the package:

```python
>>> from cognite.utils.contextualization import EntityMatchCategorizer
>>> from cognite.utils.infrastructure import ProjectArchiver
```

## Documentation

- [Cognite Python Utilities](https://cognitedata.github.io/cognite-python-utils/) (current project)
- [Cognite Python SDK](https://cognite-docs.readthedocs-hosted.com/en/latest/)
- [Cognite Python Experimental SDK](https://cognite-sdk-experimental.readthedocs-hosted.com/en/latest/)

To update project documentation, follow instructions [here](https://cognitedata.github.io/cognite-python-utils/development/basics.html#updating-project-documentation).

## Contributing

Want to contribute? Check out [Development](https://cognitedata.github.io/cognite-python-utils/development/index.html) page.
As an open source project, we abide by the [Contributor Covenant](https://cognitedata.github.io/cognite-python-utils/development/covenant.html).
