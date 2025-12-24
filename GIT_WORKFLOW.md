# Git Workflow Guide

Quick reference for managing this project with Git and GitHub.

## Initial Setup (Do Once)

### 1. Create GitHub Repository

Go to https://github.com/new and create a new repository:
- Name: `VisualPie`
- Description: "Psychedelic music visualizer for Raspberry Pi"
- Public or Private (your choice)
- **Don't** initialize with README (we already have one)

### 2. Initialize Local Repository

On your development machine (or Pi):

```bash
cd ~/VisualPie

# Initialize git
git init

# Add all files
git add .

# First commit
git commit -m "Initial commit: MVP psychedelic visualizer"

# Link to GitHub (replace with your actual repo URL)
git remote add origin https://github.com/YOUR-USERNAME/VisualPie.git

# Push to GitHub
git branch -M main
git push -u origin main
```

Done! Your code is now on GitHub.

## Daily Workflow

### Making Changes

```bash
# Edit files
vi visualizations/psychedelic_spectrum.py
vi config.yaml

# Test locally
./test.sh

# See what changed
git status
git diff

# Add changes
git add .

# Commit with descriptive message
git commit -m "Increased color cycling speed"

# Push to GitHub
git push
```

### Deploying to Pi

```bash
# SSH to Pi
ssh pi@raspberrypi.local

# Pull latest changes
cd ~/VisualPie
git pull

# Restart service
sudo systemctl restart VisualPie

# Check it's working
sudo systemctl status VisualPie
```

## Common Tasks

### See History

```bash
git log                    # Full history
git log --oneline         # Compact view
git log -n 5              # Last 5 commits
```

### Undo Changes

```bash
# Discard uncommitted changes
git checkout visualizer.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Revert to specific commit
git log --oneline
git checkout abc1234      # Replace with actual commit hash
```

### Check Differences

```bash
# Changes not yet staged
git diff

# Changes staged for commit
git diff --staged

# Compare with specific commit
git diff abc1234
```

### Branch for Experiments

```bash
# Create new branch
git checkout -b feature/lyrics-display

# Work on feature...
git add .
git commit -m "Add lyrics display module"

# Push branch
git push -u origin feature/lyrics-display

# Switch back to main
git checkout main

# Merge feature when ready
git merge feature/lyrics-display
git push
```

## GitHub Integration

### Clone on Another Machine

```bash
git clone https://github.com/YOUR-USERNAME/VisualPie.git
cd VisualPie
./deploy.sh
```

### Pull Requests (If Collaborating)

1. Create branch: `git checkout -b feature/new-viz`
2. Make changes and commit
3. Push: `git push -u origin feature/new-viz`
4. Go to GitHub → "Pull Requests" → "New Pull Request"
5. Review and merge on GitHub
6. Pull merged changes: `git checkout main && git pull`

### Viewing on GitHub

Your repo will be at: `https://github.com/YOUR-USERNAME/VisualPie`

GitHub automatically renders:
- README.md as homepage
- Code with syntax highlighting
- Commit history
- Issues and pull requests

## Efficient Workflow

### Development Machine → GitHub → Pi

```bash
# On dev machine (your laptop/desktop)
vi visualizations/psychedelic_spectrum.py
./test.sh
git add .
git commit -m "Tweaked bass boost"
git push

# On Pi (can be automated)
ssh pi@raspberrypi.local
cd ~/VisualPie && git pull && sudo systemctl restart VisualPie
```

### One-Liner Deploy to Pi

Add this to your Pi's `~/.bashrc`:

```bash
alias vv-update='cd ~/VisualPie && git pull && sudo systemctl restart VisualPie && sudo systemctl status VisualPie'
```

Then just: `vv-update`

### Auto-Update Script for Pi

Create `~/VisualPie/update.sh`:

```bash
#!/bin/bash
cd ~/VisualPie
echo "Pulling latest changes..."
git pull
echo "Restarting service..."
sudo systemctl restart VisualPie
echo "Status:"
sudo systemctl status VisualPie --no-pager
```

Then: `./update.sh` to deploy latest changes.

## Backup & Safety

### Before Major Changes

```bash
# Create backup branch
git checkout -b backup-before-refactor
git push -u origin backup-before-refactor
git checkout main

# Now safe to experiment
```

### Regular Backups

Git already backs up to GitHub, but you can also:

```bash
# Clone to external drive
cd /mnt/external-drive
git clone https://github.com/YOUR-USERNAME/VisualPie.git
```

## Troubleshooting

### Merge Conflicts

```bash
# If git pull shows conflicts:
git status                # Shows conflicting files
vi conflicting-file.py    # Edit and resolve conflicts
git add conflicting-file.py
git commit -m "Resolved merge conflict"
git push
```

### Accidentally Committed Secrets

```bash
# Remove from history (use carefully!)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch config.yaml" \
  --prune-empty --tag-name-filter cat -- --all
git push --force
```

Better: Add sensitive files to `.gitignore` BEFORE committing!

### Reset to GitHub State

```bash
# Discard all local changes and match GitHub
git fetch origin
git reset --hard origin/main
```

## Best Practices

1. **Commit often** - Small, focused commits are better than big ones
2. **Descriptive messages** - "Fixed color cycling" not "Fixed bug"
3. **Test before pushing** - Run `./test.sh` first
4. **Pull before editing** - `git pull` to avoid conflicts
5. **Don't commit secrets** - Keep API keys out of config.yaml

## Quick Reference Card

```bash
# Daily workflow
git pull              # Get latest
# ... make changes ...
git add .             # Stage all changes
git commit -m "msg"   # Commit
git push              # Upload to GitHub

# Deployment
ssh pi@raspberrypi.local
git pull && sudo systemctl restart VisualPie

# Safety
git status            # See what changed
git diff              # See exact changes
git log --oneline     # See history

# Undo
git checkout file     # Discard changes to file
git reset --hard      # Discard all changes
```

## Next Steps

Once comfortable:
- Use branches for experiments
- Tag releases: `git tag v1.0 && git push --tags`
- Add GitHub Actions for automated testing
- Enable GitHub Issues for tracking features

Happy coding! 🎵
