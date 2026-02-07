# GitHub Setup Guide for Stellar Compass

This guide will help you connect your Stellar Compass project to your GitHub repository.

## Prerequisites
- Git installed on your computer
- GitHub account
- Stellar Compass project files (already created)

## Step 1: Initialize Git Repository (if not done)

```bash
# Navigate to your project directory
cd stellar-compass

# Initialize git (if not already initialized)
git init

# Add all files to staging
git add .

# Create initial commit
git commit -m "Initial commit: Stellar Compass AI DeFi Assistant"
```

## Step 2: Connect to Your GitHub Repo

### Option A: If you already created a repo on GitHub

```bash
# Add your GitHub repo as remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Verify the remote
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

### Option B: Create a new repo on GitHub first

1. Go to https://github.com/new
2. Enter repository name (e.g., `stellar-compass`)
3. Make it **Public** or **Private**
4. **DO NOT** initialize with README (we already have one)
5. Click "Create repository"
6. Follow the commands shown on GitHub (similar to Option A)

## Step 3: Verify Upload

```bash
# Check status
git status

# View commit history
git log --oneline
```

Visit your GitHub repo URL to see all files uploaded!

## Common Commands

### Making Changes

```bash
# See what changed
git status

# Add specific files
git add frontend/app.js

# Or add all changes
git add .

# Commit with message
git commit -m "Add new feature: XYZ"

# Push to GitHub
git push
```

### Pulling Latest Changes

```bash
# Get latest from GitHub
git pull origin main
```

### Creating Branches

```bash
# Create and switch to new branch
git checkout -b feature/new-feature

# Push branch to GitHub
git push -u origin feature/new-feature
```

## Project Structure Uploaded

```
stellar-compass/
├── .gitignore                          ✅ Uploaded
├── README.md                           ✅ Uploaded
├── GITHUB_SETUP.md                     ✅ This file
├── frontend/
│   ├── index.html                      ✅ Uploaded
│   ├── styles.css                      ✅ Uploaded
│   └── app.js                          ✅ Uploaded
└── backend/
    ├── app.py                          ✅ Uploaded
    ├── stellar_horizon.py              ✅ Uploaded
    ├── stellar_defi_algorithms.py      ✅ Uploaded
    ├── stellar_ai_agents.py            ✅ Uploaded
    └── requirements.txt                ✅ Uploaded
```

## Troubleshooting

### Error: "remote origin already exists"
```bash
# Remove existing remote
git remote remove origin

# Add your remote again
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

### Error: "Permission denied"
```bash
# Use HTTPS instead of SSH
git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Or setup SSH keys (recommended)
# Follow: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
```

### Large files warning
```bash
# Check file sizes
du -sh backend/* frontend/*

# If you have large files, add them to .gitignore
echo "large-file.bin" >> .gitignore
```

## Best Practices

1. **Commit often** - Small, focused commits are better
2. **Write clear messages** - Describe what and why
3. **Use branches** - Keep main branch stable
4. **Pull before push** - Avoid conflicts
5. **Review before commit** - Check what you're committing

## Next Steps

1. ✅ Push code to GitHub
2. 🔧 Set up GitHub Actions (CI/CD)
3. 📝 Add GitHub Issues for tasks
4. 🌟 Add topics to your repo (stellar, defi, ai)
5. 📱 Enable GitHub Pages for frontend (optional)

## Setting Up GitHub Pages (Optional)

To host your frontend for free:

```bash
# Create gh-pages branch
git checkout -b gh-pages

# Copy frontend files to root
cp -r frontend/* .

# Commit and push
git add .
git commit -m "Setup GitHub Pages"
git push origin gh-pages
```

Then enable GitHub Pages in repo Settings → Pages → Source: gh-pages

Your app will be live at: `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/`

---

**You're all set! Happy coding! 🚀**
