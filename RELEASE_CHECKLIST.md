# Release Checklist for nanohub-remote v0.2.0

## Pre-Release Checklist

### Code Quality
- [x] All tests pass (25/25 tests)
- [x] No linting errors
- [x] Code formatted and reviewed
- [x] No security vulnerabilities

### Documentation
- [x] README.md updated with new features
- [x] CHANGELOG.md updated with version 0.2.0 changes
- [x] API documentation complete (ReadTheDocs)
- [x] Examples added
- [x] Testing documentation complete

### Package Configuration
- [x] Version bumped to 0.2.0 in `_version.py`
- [x] Dependencies updated in `setup.py`
- [x] Dependencies updated in `pyproject.toml`
- [x] MANIFEST.in includes all necessary files
- [x] .gitignore updated

### Build and Test
- [x] Package builds successfully: `python3 -m build`
- [x] Twine check passes: `python3 -m twine check dist/*`
- [ ] Test installation from Test PyPI
- [ ] Verify imports work correctly
- [ ] Run examples to verify functionality

## Release Steps

### 1. Clean Build
```bash
rm -rf build dist *.egg-info
python3 -m build
python3 -m twine check dist/*
```

### 2. Test on Test PyPI (Optional but Recommended)
```bash
python3 -m twine upload --repository testpypi dist/*

# In a clean environment
pip install --index-url https://test.pypi.org/simple/ \
            --extra-index-url https://pypi.org/simple/ \
            nanohub-remote
```

### 3. Upload to PyPI
```bash
python3 -m twine upload dist/*
```

### 4. Tag Release
```bash
git tag -a v0.2.0 -m "Release version 0.2.0 - Session improvements"
git push origin v0.2.0
```

### 5. Create GitHub Release
1. Go to https://github.com/denphi/nanohub-remote/releases
2. Click "Create a new release"
3. Select tag `v0.2.0`
4. Title: "v0.2.0 - Session Improvements"
5. Copy content from CHANGELOG.md for release notes
6. Publish release

### 6. Setup ReadTheDocs
1. Go to https://readthedocs.org/
2. Import project from GitHub
3. Build documentation
4. Verify docs at https://nanohub-remote.readthedocs.io/

## Post-Release Checklist

### Verification
- [ ] Package appears on PyPI
- [ ] Installation works: `pip install nanohub-remote`
- [ ] Version correct: `import nanohubremote; print(nanohubremote.__version__)`
- [ ] ReadTheDocs builds successfully
- [ ] GitHub release published
- [ ] Git tag pushed

### Communication
- [ ] Announce release (if applicable)
- [ ] Update project homepage (if applicable)
- [ ] Notify users of breaking changes (none in this release)

## Quick Commands

```bash
# Build package
rm -rf build dist *.egg-info && python3 -m build

# Check package
python3 -m twine check dist/*

# Test locally
pip install -e .
python3 -c "import nanohubremote as nr; print(nr.__version__)"
pytest

# Upload to Test PyPI
python3 -m twine upload --repository testpypi dist/*

# Upload to PyPI
python3 -m twine upload dist/*

# Build documentation
cd docs && make html

# Tag and push
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0
```

## What's New in v0.2.0

### Major Features
- ✅ Proper `requests.Session` support with connection pooling
- ✅ HTTP methods: PUT, DELETE, PATCH
- ✅ JSON support for all HTTP methods
- ✅ Automatic retry logic (configurable)
- ✅ Context manager support
- ✅ Comprehensive test suite (25 tests)
- ✅ Complete ReadTheDocs documentation with examples

### Bug Fixes
- ✅ Fixed token refresh grant_type bug
- ✅ Replaced bare except clauses with specific exceptions
- ✅ Fixed Tools.list() to use session properly

### Documentation
- ✅ Complete ReadTheDocs with Sphinx
- ✅ API reference documentation
- ✅ 4 comprehensive example pages
- ✅ Updated README with Session docs
- ✅ Testing guide

### Infrastructure
- ✅ pytest configuration
- ✅ Development requirements
- ✅ MANIFEST.in for proper packaging
- ✅ .readthedocs.yaml for auto-building

## Troubleshooting

### Build Fails
- Clean build artifacts: `rm -rf build dist *.egg-info`
- Check dependencies in setup.py match pyproject.toml
- Verify version is updated

### Upload Fails
- Check PyPI API token is correct
- Verify version hasn't been used before
- Ensure all required metadata is present

### Documentation Doesn't Build
- Install sphinx: `pip install -r requirements-dev.txt`
- Check for RST syntax errors
- Verify all referenced files exist

## Notes

- **Backward Compatibility**: All changes are backward compatible
- **Python Versions**: 3.8, 3.9, 3.10, 3.11, 3.12
- **License**: MIT
- **Dependencies**: requests, urllib3, fs

## Contact

Issues: https://github.com/denphi/nanohub-remote/issues
