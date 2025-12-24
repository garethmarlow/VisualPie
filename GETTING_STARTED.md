# 🚀 Quick Start: Get This Running in 5 Minutes

## Step 1: Create GitHub Repository (2 minutes)

1. Go to https://github.com/new
2. Repository name: `VisualPie`
3. Description: "Psychedelic music visualizer for Raspberry Pi"
4. Choose Public or Private
5. **Don't** check "Initialize with README"
6. Click "Create repository"
7. **Copy the repository URL** (looks like: `https://github.com/yourusername/VisualPie.git`)

## Step 2: Initialize Git & Push (1 minute)

Extract the archive and run:

```bash
tar xzf VisualPie.tar.gz
cd VisualPie
./init-git.sh
# Paste your GitHub repo URL when prompted
```

Done! Your code is now on GitHub.

## Step 3: Deploy to Raspberry Pi (2 minutes)

SSH to your Pi and run:

```bash
git clone https://github.com/yourusername/VisualPie.git
cd VisualPie
./deploy.sh
```

The script will:
- ✓ Install all dependencies
- ✓ Ask for your Icecast stream URL
- ✓ Offer to test the visualizer
- ✓ Set up auto-start service

**That's it!** Your visualizer is running.

## Making Changes

**On your dev machine:**
```bash
cd VisualPie
vi config.yaml              # Make changes
git add .
git commit -m "Changed color speed"
git push
```

**On your Pi:**
```bash
cd ~/VisualPie
git pull
sudo systemctl restart VisualPie
```

## Efficient Workflow Tip

Add to your Pi's `~/.bashrc`:

```bash
alias vv-update='cd ~/VisualPie && git pull && sudo systemctl restart VisualPie'
```

Then just type `vv-update` to deploy latest changes!

## Documentation

- **README.md** - Project overview
- **GIT_WORKFLOW.md** - Git commands reference
- **QUICKREF.md** - Command cheat sheet
- **DEPLOYMENT.md** - Detailed Pi setup guide

## Need Help?

```bash
# View logs
sudo journalctl -u VisualPie -f

# Test manually
./test.sh

# Check service status
sudo systemctl status VisualPie
```

Enjoy! 🎵✨
