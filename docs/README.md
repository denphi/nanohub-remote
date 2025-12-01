# Documentation

This directory contains the Sphinx documentation for nanohub-remote.

## Building Documentation Locally

### Install Requirements

```bash
pip install -r requirements-dev.txt
```

### Build HTML Documentation

```bash
cd docs
make html
```

The built documentation will be in `docs/build/html/index.html`.

### Build PDF Documentation

```bash
cd docs
make latexpdf
```

### Clean Build Files

```bash
cd docs
make clean
```

## ReadTheDocs

The documentation is automatically built and hosted on ReadTheDocs when pushed to GitHub.

Configuration file: `.readthedocs.yaml` in the repository root.

## Documentation Structure

```
docs/
├── source/
│   ├── conf.py              # Sphinx configuration
│   ├── index.rst            # Main page
│   ├── installation.rst     # Installation guide
│   ├── quickstart.rst       # Quick start guide
│   ├── testing.rst          # Testing information
│   ├── changelog.rst        # Changelog
│   ├── api/                 # API documentation
│   │   ├── index.rst
│   │   ├── session.rst
│   │   ├── tools.rst
│   │   ├── sim2l.rst
│   │   ├── project.rst
│   │   ├── params.rst
│   │   └── output.rst
│   └── examples/            # Usage examples
│       ├── index.rst
│       ├── basic_session.rst
│       ├── tools_example.rst
│       ├── project_files.rst
│       └── advanced_usage.rst
├── Makefile                 # Build commands
└── README.md               # This file
```

## Contributing to Documentation

1. Edit `.rst` files in `docs/source/`
2. Build locally to verify: `make html`
3. Check for warnings and errors
4. Submit pull request

## Sphinx Extensions Used

- `sphinx.ext.autodoc` - Auto-generate API docs from docstrings
- `sphinx.ext.napoleon` - Support for Google/NumPy style docstrings
- `sphinx.ext.viewcode` - Add links to source code
- `sphinx.ext.intersphinx` - Link to other project docs
- `sphinx_rtd_theme` - ReadTheDocs theme
