# Mail2PDF NextGen - GitHub Actions CI/CD

**Automatic Testing & Deployment Workflow**

---

## 🚀 Overview

GitHub Actions automates:
- ✅ Testing on multiple Python versions
- ✅ Linting and code quality checks
- ✅ Building Docker images
- ✅ Pushing to Docker Hub (optional)
- ✅ Releasing to PyPI (optional)

---

## 📋 Setup GitHub Actions

### 1. Create Workflow Directory

```bash
mkdir -p .github/workflows
```

### 2. Create Test Workflow

File: `.github/workflows/test.yml`

```yaml
name: Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.8', '3.9', '3.10', '3.11']

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        python -m pip install -r requirements.txt
    
    - name: Lint with flake8 (optional)
      run: |
        pip install flake8
        flake8 main.py app.py config.py utils.py --count --select=E9,F63,F7,F82 --show-source --statistics
      continue-on-error: true
    
    - name: Run validation tests
      run: python validate.py
    
    - name: Run examples
      run: python examples.py
```

---

## 🐳 Docker Build Workflow

File: `.github/workflows/docker.yml`

```yaml
name: Docker Build

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Build Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: false
        tags: mail2pdf-nextgen:latest
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

### Push to Docker Hub (Optional)

Add Docker Hub credentials as secrets:
1. GitHub Repo → Settings → Secrets → New Repository Secret
2. Add: `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`

```yaml
    - name: Login to Docker Hub
      if: github.event_name == 'push'
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}
    
    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: |
          ${{ secrets.DOCKERHUB_USERNAME }}/mail2pdf-nextgen:latest
          ${{ secrets.DOCKERHUB_USERNAME }}/mail2pdf-nextgen:${{ github.ref_name }}
```

---

## 📦 Publish Release Workflow

File: `.github/workflows/release.yml`

```yaml
name: Release to PyPI

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    permissions:
      contents: read
      id-token: write
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install build dependencies
      run: |
        python -m pip install --upgrade pip
        python -m pip install build twine
    
    - name: Build distribution
      run: python -m build
    
    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}
```

Add `PYPI_API_TOKEN` as repository secret for publishing.

---

## 🔍 Code Quality Workflow

File: `.github/workflows/quality.yml`

```yaml
name: Code Quality

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  quality:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install linting tools
      run: |
        pip install flake8 black pylint
    
    - name: Check formatting with black
      run: black --check main.py app.py config.py utils.py
      continue-on-error: true
    
    - name: Lint with flake8
      run: flake8 main.py app.py config.py utils.py
      continue-on-error: true
    
    - name: Check types with pylint
      run: pylint main.py app.py config.py utils.py
      continue-on-error: true
```

---

## 📋 Requirements for Secrets

To use CI/CD fully, add these to GitHub Secrets:

### For Docker Hub Publishing
```
DOCKERHUB_USERNAME: your-docker-username
DOCKERHUB_TOKEN: your-docker-api-token
```

### For PyPI Publishing
```
PYPI_API_TOKEN: your-pypi-token
```

Get tokens from:
- **Docker Hub:** Settings → Security
- **PyPI:** Settings → API tokens

---

## 🎯 Automatic Release

File: `.github/workflows/auto-release.yml`

```yaml
name: Auto Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Create Release
      uses: softprops/action-gh-release@v1
      with:
        body_path: CHANGELOG.md
        draft: false
        prerelease: false
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## 🧪 Coverage Report

File: `.github/workflows/coverage.yml`

```yaml
name: Coverage Report

on:
  push:
    branches: [ main ]

jobs:
  coverage:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install coverage pytest
    
    - name: Run tests with coverage
      run: |
        coverage run -m pytest
        coverage report
        coverage xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml
```

---

## 📊 Badges for README

Add to `README.md`:

```markdown
[![Tests](https://github.com/YOUR_USERNAME/mail2pdf-nextgen/workflows/Tests/badge.svg)](https://github.com/YOUR_USERNAME/mail2pdf-nextgen/actions)
[![Docker Build](https://github.com/YOUR_USERNAME/mail2pdf-nextgen/workflows/Docker%20Build/badge.svg)](https://github.com/YOUR_USERNAME/mail2pdf-nextgen/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
```

---

## 🔄 Workflow Triggers

Workflows run on:

- `push` to main branch
- `pull_request` to main branch
- `tags` matching version pattern (v*.*.*)
- Manual trigger (optional)

Add manual trigger:

```yaml
on:
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to release'
        required: true
```

---

## 🚀 Complete Setup Checklist

- ✅ Create `.github/workflows/` directory
- ✅ Add `test.yml` workflow
- ✅ Add `docker.yml` for Docker builds
- ✅ Add `release.yml` for PyPI (optional)
- ✅ Configure secrets in GitHub
- ✅ Tag releases as `v2.0.0`
- ✅ Push and verify workflows run
- ✅ Add badges to README

---

## 🎯 Common Tasks

### Run Tests Manually

```bash
# Local
python -m pytest validate.py

# Or just
python validate.py
```

### Build Docker Manually

```bash
docker build -t mail2pdf:latest .
docker run -p 5000:5000 mail2pdf:latest
```

### Create Release

```bash
# Tag version
git tag -a v2.0.1 -m "Release 2.0.1"
git push origin v2.0.1

# GitHub auto-creates release via Actions
```

---

## 📝 Matrix Testing

Test on multiple Python versions:

```yaml
strategy:
  matrix:
    python-version: ['3.8', '3.9', '3.10', '3.11']
    os: [ubuntu-latest, macos-latest, windows-latest]
```

This creates 12 test jobs (4 × 3).

---

## 🔗 Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Checkout Action](https://github.com/actions/checkout)
- [Setup Python](https://github.com/actions/setup-python)

---

**CI/CD Setup Complete!** Your project now has:
- ✅ Automated testing
- ✅ Docker builds
- ✅ Code quality checks
- ✅ Automated releases
