# Git Workflow for CreditPathAI Project

Guide for using Git with both frontend and backend in the same repository.

## 📍 Repository Structure for Git

```
ai-creditPath/                    ← Main Git repository root
├── .git/                         ← Git metadata (created by git init)
├── .gitignore                    ← Git ignore rules
├── README.md                     ← Main project readme
├── SETUP.md                      ← Setup instructions
├── frontend/                     ← Frontend tracked by Git
│   ├── .gitignore                ← Frontend-specific ignores
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── node_modules/             (ignored by .gitignore)
└── backend/                      ← Backend tracked by Git
    ├── .gitignore                ← Backend-specific ignores
    ├── *.py files
    ├── requirements.txt
    ├── venv/                     (ignored by .gitignore)
    └── *.pkl files              (model files, ignored)
```

## ✅ Initial Git Setup (Already Done)

The repository is already initialized with:
- `.gitignore` in root (ignores node_modules, venv, etc.)
- `.gitignore` in frontend/
- `.gitignore` in backend/

## 🔄 Daily Git Workflow

### Check Status

```bash
# From project root (e:\Infosys spring board\ai-creditPath)
git status

# Shows:
# - Modified files in frontend/
# - Modified files in backend/
# - Untracked files
```

### Add and Commit Changes

#### Option 1: Commit All Changes

```bash
git add .
git commit -m "Update features"
```

#### Option 2: Commit Specific Directory

```bash
# Only backend changes
git add backend/
git commit -m "[backend] Add new API endpoint"

# Only frontend changes
git add frontend/
git commit -m "[frontend] Update dashboard UI"
```

#### Option 3: Commit Specific Files

```bash
git add backend/milestone5_api.py frontend/src/App.js
git commit -m "[both] Update integration"
```

### Push and Pull

```bash
# Push to remote repository
git push origin main

# Pull latest changes
git pull origin main
```

## 📝 Commit Message Convention

Use tags to indicate which part was changed:

```bash
# Backend only
git commit -m "[backend] Add CORS middleware"

# Frontend only
git commit -m "[frontend] Add loading spinner"

# Both
git commit -m "[both] Update API integration"

# Root level (setup, docs, config)
git commit -m "[root] Update README"
```

## 🔍 Viewing Changes

### See What Changed

```bash
# All changes
git diff

# Only backend changes
git diff backend/

# Only frontend changes
git diff frontend/

# Changes in specific file
git diff backend/milestone5_api.py
```

### View Commit History

```bash
# Full history
git log

# Short format
git log --oneline

# Last 5 commits
git log --oneline -5

# Changes in a specific directory
git log --oneline -- backend/
git log --oneline -- frontend/
```

## 🌿 Branching Strategy

### Create Feature Branch

```bash
# Create and switch to new branch
git checkout -b feature/add-oauth

# Make changes
git add .
git commit -m "[backend] Add OAuth authentication"

# Push to remote
git push origin feature/add-oauth
```

### Merge Back to Main

```bash
# Switch to main
git checkout main

# Pull latest
git pull origin main

# Merge feature branch
git merge feature/add-oauth

# Delete feature branch
git branch -d feature/add-oauth
```

## 🚫 What's Ignored (Not Tracked)

### Automatically Ignored

```
# Frontend (from frontend/.gitignore)
node_modules/
build/
.env.local

# Backend (from backend/.gitignore)
venv/
__pycache__/
*.pkl                    ← Model files
*.joblib               ← Saved models
.env                   ← Environment variables

# Root level
.DS_Store              ← macOS files
Thumbs.db             ← Windows thumbnails
```

### Exception: Add if Needed

If you need to track a `.pkl` file:
```bash
# Force add despite .gitignore
git add -f backend/model.pkl

# This is usually NOT recommended for large model files
# Better to use Git LFS (Large File Storage)
```

## 🔐 Never Commit

**Do NOT commit:**
- `venv/` directory
- `node_modules/` directory
- `.env` files with secrets
- `*.pkl` model files (>5MB)
- `*.csv` data files (>10MB)

Use `.gitignore` to prevent accidental commits.

## 📦 Git with Large Files (Optional)

For large model files, use Git LFS:

```bash
# Install (on system, not in repo)
git lfs install

# Track .pkl files
git lfs track "*.pkl"

# Commit normally
git add model.pkl
git commit -m "Add trained model"
```

## 🔄 Handling Conflicts

If conflicts occur when pulling:

```bash
# See the conflict
git status

# Open the conflicted file and fix manually
# Look for markers:
# <<<<<<< HEAD
# your changes
# =======
# their changes
# >>>>>>> branch-name

# After fixing
git add <resolved-file>
git commit -m "Resolve merge conflict"
```

## 📊 Useful Git Commands

```bash
# Undo uncommitted changes
git checkout -- path/to/file

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Remove file from Git (keep locally)
git rm --cached filename

# Rename file
git mv oldname newname

# Show who changed a line
git blame filename

# Export repository
git bundle create repo.bundle --all
```

## 🚀 Deployment with Git

### Automated Deployment (Future)

The `.git` folder enables:
- Automatic deployment on push
- CI/CD pipelines
- Automatic testing
- Version tracking

### Tagging Releases

```bash
# Create release tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tags
git push origin --tags

# List tags
git tag -l
```

## 📋 Best Practices

✅ **DO:**
- Commit frequently with clear messages
- Use meaningful branch names
- Pull before pushing
- Test before committing
- Use `.gitignore` properly
- Keep commits focused

❌ **DON'T:**
- Commit large files directly
- Mix multiple features in one commit
- Push to main without testing
- Commit secrets or credentials
- Force push without reason
- Ignore `.gitignore` files

## 🔍 Git Status Examples

### After Frontend Changes

```
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update the cached index)
  
    modified:   frontend/src/App.js
    modified:   frontend/src/components/Form.js
    
Untracked files:
  (use "git add <file>..." to include in what will be committed)
    frontend/src/new_component.js
```

Solution:
```bash
git add frontend/
git commit -m "[frontend] Update form and app components"
```

### After Backend Changes

```
On branch main
Changes not staged for commit:
  
    modified:   backend/milestone5_api.py
    modified:   backend/requirements.txt
```

Solution:
```bash
git add backend/
git commit -m "[backend] Add new dependencies and API features"
```

## 📞 Common Scenarios

### Scenario 1: Both Frontend and Backend Changed

```bash
git add .
git commit -m "[both] Integrate new features"
git push origin main
```

### Scenario 2: Only Config Files Changed

```bash
git add README.md SETUP.md .gitignore
git commit -m "[root] Update documentation"
git push origin main
```

### Scenario 3: Accidental Commit to Wrong Branch

```bash
# Create new branch with current work
git branch new-feature

# Go back to main
git checkout main

# Undo last commit
git reset --hard HEAD~1

# Switch to new branch
git checkout new-feature
```

---

**Now your CreditPathAI project is properly tracked with Git! 🎉**

Both frontend and backend changes are stored in the same repository for easy management.
