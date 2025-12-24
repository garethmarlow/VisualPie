#!/bin/bash
# Initialize Git repository and push to GitHub
# Run this ONCE after creating your GitHub repo

set -e

echo "╔════════════════════════════════════════╗"
echo "║    Git Repository Initialization       ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Check if already initialized
if [ -d ".git" ]; then
    echo "⚠ Git repository already exists"
    read -p "Reinitialize? This will lose current git history. (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf .git
    else
        echo "Aborted."
        exit 0
    fi
fi

# Get GitHub repo URL
echo "First, create a repository on GitHub:"
echo "  1. Go to https://github.com/new"
echo "  2. Name: VisualPie"
echo "  3. Don't initialize with README"
echo ""
read -p "Enter your GitHub repo URL (e.g., https://github.com/username/VisualPie.git): " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "✗ No URL provided"
    exit 1
fi

echo ""
echo "Initializing Git repository..."

# Initialize
git init
git add .
git commit -m "Initial commit: MVP psychedelic visualizer

- Icecast stream support (OGG/FLAC)
- Psychedelic spectrum visualization
- Auto-start systemd service
- Modular architecture for future extensions
- Raspberry Pi 3 optimized (1080p@60fps)"

# Set default branch to main
git branch -M main

# Add remote
git remote add origin "$REPO_URL"

echo ""
echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "✓ Repository initialized and pushed!"
echo ""
echo "Your code is now at: ${REPO_URL%.git}"
echo ""
echo "Next steps:"
echo "  1. On your Pi: git clone $REPO_URL"
echo "  2. cd VisualPie"
echo "  3. ./deploy.sh"
echo ""
echo "See GIT_WORKFLOW.md for daily usage."
echo ""
