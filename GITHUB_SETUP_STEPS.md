# Mail2PDF NextGen - GitHub Setup Guide

**Complete Repository Setup Instructions**

---

## 📋 Step 1: Create GitHub Repository

### On GitHub.com

1. **Login** to GitHub
2. **Click** "+" → "New repository"
3. **Name:** `mail2pdf-nextgen`
4. **Description:** "Advanced Email to PDF Converter"
5. **Visibility:** Public
6. **Skip:** Initialize with README (we have one)
7. **Click:** "Create repository"

### Get Your Repo URL

From the repo page:
```
https://github.com/YOUR_USERNAME/mail2pdf-nextgen.git
```

---

## 📂 Step 2: Prepare Local Project

```bash
# Navigate to project
cd mail2pdf-nextgen

# Initialize git (if not already)
git init

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/mail2pdf-nextgen.git

# Verify
git remote -v
```

---

## ✅ Step 3: Configure Git

```bash
# Set user info
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Verify
git config --list
```

---

## 📝 Step 4: Commit Files

```bash
# Add all files
git add .

# Check status
git status

# Commit
git commit -m "Initial commit: Mail2PDF NextGen v2.0.0"
```

---

## 🚀 Step 5: Push to GitHub

```bash
# Push to main branch
git branch -M main
git push -u origin main

# Verify on GitHub
# https://github.com/YOUR_USERNAME/mail2pdf-nextgen
```

---

## 🔑 SSH Setup (Optional but Recommended)

```bash
# Generate key
ssh-keygen -t ed25519 -C "your.email@example.com"

# Start SSH agent
eval "$(ssh-agent -s)"

# Add key
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub  # Copy output

# On GitHub:
# Settings → SSH and GPG keys → New SSH key
# Paste public key

# Test
ssh -T git@github.com
# Should output: Hi YOUR_USERNAME! You've successfully authenticated.
```

---

## 📚 Step 6: Add Documentation Links

Edit **README.md** replace placeholders:

```markdown
# Original version
https://gitlab.villejuif.fr/depots-public/mail2pdf

# Your GitHub
https://github.com/YOUR_USERNAME/mail2pdf-nextgen
```

---

## 🏷️ Step 7: Create Release Tags

```bash
# Create tag
git tag -a v2.0.0 -m "Release version 2.0.0"

# Push tags
git push origin v2.0.0

# On GitHub:
# Go to Releases → Create release
# Tag: v2.0.0
# Title: v2.0.0
# Description: See CHANGELOG.md
```

---

## 🔄 Step 8: Setup CI/CD (Optional)

### GitHub Actions Workflow

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run validation
      run: python validate.py
    
    - name: Run examples
      run: python examples.py
```

---

## 📖 Step 9: GitHub Pages (Optional)

### Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. **Source:** Deploy from a branch
3. **Branch:** main, /docs folder
4. **Save**

Your docs will be at: `https://YOUR_USERNAME.github.io/mail2pdf-nextgen`

---

## 🎯 Step 10: Configure Repository Settings

### GitHub Settings

**General:**
- ✅ Issue templates (optional)
- ✅ Discussion enabled
- ✅ Branch protection rules

**Collaborators:**
- Add team members if needed

**Secrets:**
- Add any API keys if needed (none for this project)

**Actions:**
- Enable GitHub Actions (already enabled)

---

## 🔗 File Structure on GitHub

Your repository will have:

```
your-username/mail2pdf-nextgen/
├── main branch
│   ├── main.py
│   ├── app.py
│   ├── config.py
│   ├── utils.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── FULL_DOCUMENTATION.md
│   ├── PROJECT_STATUS.md
│   ├── DEPLOYMENT_*.md
│   ├── GITHUB_*.md
│   ├── templates/
│   ├── data/
│   ├── examples.py
│   ├── validate.py
│   ├── quickstart.py
│   ├── setup.py
│   ├── LICENSE
│   ├── .gitignore
│   └── .dockerignore
├── Releases (v2.0.0, etc.)
├── Issues (bug reports, features)
└── Discussions (Q&A)
```

---

## 📊 GitHub Badges (Optional)

Add to README.md:

```markdown
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![DockerHub](https://img.shields.io/badge/docker-ready-blue.svg)](https://hub.docker.com/r/yourusername/mail2pdf-nextgen)
```

---

## 🔄 Common Git Commands

```bash
# Check status
git status

# Add files
git add .
git add filename.py

# Commit
git commit -m "message"

# Push
git push origin main

# Pull updates
git pull origin main

# Create branch
git checkout -b feature/new-feature

# Switch branch
git checkout main

# Merge branch
git merge feature/new-feature

# View log
git log --oneline
```

---

## ✨ Next Steps

1. **Share** repository link
2. **Star** on GitHub (if you like it!)
3. **Watch** for updates
4. **Create issues** for bugs/features
5. **Open discussions** for Q&A

---

## 📞 Support

**GitHub Resources:**
- [GitHub Docs](https://docs.github.com)
- [Git Guide](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com)

---

**Your Mail2PDF NextGen repository is ready!** 🎉
