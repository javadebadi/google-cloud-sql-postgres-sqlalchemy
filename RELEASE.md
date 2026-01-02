# Release Guide

This guide explains how to publish new versions of `google-cloud-sql-postgres-sqlalchemy` to PyPI.

## Prerequisites

### 1. Set up PyPI API Tokens

You need to create API tokens for both Test PyPI and PyPI, then add them as GitHub secrets.

#### Create PyPI API Token
1. Go to https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Give it a name (e.g., "google-cloud-sql-postgres-sqlalchemy-github-actions")
4. Scope: "Entire account" (initially) or "Project: google-cloud-sql-postgres-sqlalchemy" (after first publish)
5. Copy the token (starts with `pypi-`)

#### Create Test PyPI API Token (Optional, for testing)
1. Go to https://test.pypi.org/manage/account/token/
2. Follow the same steps as above
3. Copy the token

#### Add Tokens to GitHub Secrets
1. Go to your repository: https://github.com/javadebadi/google-cloud-sql-postgres-sqlalchemy
2. Click Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add two secrets:
   - Name: `PYPI_API_TOKEN`, Value: (your PyPI token)
   - Name: `TEST_PYPI_API_TOKEN`, Value: (your Test PyPI token, optional)

## Publishing a New Release

### Automated Release (Recommended)

The package automatically publishes to PyPI when you push a version tag:

```bash
# 1. Update version in pyproject.toml if needed (optional - workflow updates it)
# 2. Commit any pending changes
git add .
git commit -m "Prepare release v0.2.0"
git push

# 3. Create and push a version tag
git tag v0.2.0
git push origin v0.2.0

# 4. GitHub Actions will automatically:
#    - Run all tests
#    - Build the package
#    - Publish to Test PyPI (if token configured)
#    - Publish to PyPI
#    - Create a GitHub Release
```

### What Happens Automatically

When you push a tag like `v0.2.0`:
1. ✅ CI tests run on all Python versions (3.10-3.14)
2. ✅ Version is extracted from tag (e.g., `v0.2.0` → `0.2.0`)
3. ✅ `pyproject.toml` version is updated
4. ✅ Package is built
5. ✅ Published to Test PyPI (optional, skips if exists)
6. ✅ Published to PyPI
7. ✅ GitHub Release is created with release notes

### Manual Release

If you prefer to publish manually:

```bash
# 1. Update version in pyproject.toml
# version = "0.2.0"

# 2. Run tests
invoke code.ci

# 3. Build package
python -m build

# 4. Publish to Test PyPI (optional)
python -m twine upload --repository testpypi dist/*

# 5. Test installation
pip install --index-url https://test.pypi.org/simple/ google-cloud-sql-postgres-sqlalchemy

# 6. Publish to PyPI
python -m twine upload dist/*

# 7. Create git tag
git tag v0.2.0
git push origin v0.2.0
```

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** version (v1.0.0): Incompatible API changes
- **MINOR** version (v0.2.0): New functionality, backwards compatible
- **PATCH** version (v0.1.1): Bug fixes, backwards compatible

## Checklist Before Release

- [ ] All tests pass (`invoke code.ci`)
- [ ] CHANGELOG.md updated (if you have one)
- [ ] README.md is up to date
- [ ] Version number follows semver
- [ ] PyPI API token is configured in GitHub secrets

## First Release

For the first release to PyPI:

1. The package name must be available on PyPI
2. Use scope "Entire account" for the API token initially
3. After first successful publish, you can create a project-scoped token
4. Update the GitHub secret with the project-scoped token for better security

## Monitoring

After pushing a tag, monitor the release:
- **GitHub Actions**: https://github.com/javadebadi/google-cloud-sql-postgres-sqlalchemy/actions
- **PyPI Package**: https://pypi.org/project/google-cloud-sql-postgres-sqlalchemy/
- **GitHub Releases**: https://github.com/javadebadi/google-cloud-sql-postgres-sqlalchemy/releases

## Troubleshooting

### Error: 403 Forbidden (PyPI)
- Check that your API token is correct in GitHub secrets
- Ensure the package name is available on PyPI
- For first publish, use "Entire account" scope

### Error: File already exists
- You cannot re-upload the same version to PyPI
- Increment the version number and create a new tag

### Tests failing in workflow
- Run `invoke code.ci` locally first
- Fix any issues before pushing the tag
- Delete and recreate the tag if needed:
  ```bash
  git tag -d v0.2.0
  git push origin :refs/tags/v0.2.0
  # Fix issues, then recreate tag
  git tag v0.2.0
  git push origin v0.2.0
  ```
